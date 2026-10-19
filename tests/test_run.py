"""The runner: the programme matches the proposal's run plan, the dry run works end to
end, and the real paths (generate, judge) behave correctly with OpenRouter replaced by
the mock -- every stop condition included. Sockets are disabled throughout."""

import contextlib
import io
import json
import os

import pytest

from cases import CASES
from pipeline import run
from pipeline.conditions import LONG_ARM
from pipeline.llm import MockBackend

# what one generate or judge run makes for the corpus in cases/: the plan's own counts,
# so adding a case changes no number here
GENERATE_CALLS = run.plan(len(CASES))[0][1]
JUDGE_CALLS = sum(calls for _, calls, _ in run.plan(len(CASES))[1:])


def _quiet(fn, *args, **kw):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        result = fn(*args, **kw)
    return result, out.getvalue()


def test_plan_reproduces_the_proposal_budget():
    """Proposal §5: 480 calls and $0.78 per case for the arms run on every case;
    21,720 calls and $37.48 for the 40-case main programme."""
    rows = {name: (calls, cost) for name, calls, cost in run.plan(1)}
    every_case = ["generate and accept reports", "agreement", "conflict", "abstain", "screen"]
    assert [rows[n][0] for n in every_case] == [48, 144, 180, 72, 36]
    assert round(sum(rows[n][1] for n in every_case), 2) == 0.78
    rows40 = {name: (calls, cost) for name, calls, cost in run.plan(40)}
    assert rows40["long-conflict"][0] == 1200 and rows40["long-agreement"][0] == 240
    assert rows40["ladder"][0] == 1080
    assert sum(c for c, _ in rows40.values()) == 21720
    assert round(sum(c for _, c in rows40.values()), 2) == 37.48


def test_length_arm_runs_exactly_the_conditions_that_are_length_checked():
    long = [c for e in run.PROGRAMME if e.arm == "long" for c in e.conditions]
    assert sorted(long) == sorted(LONG_ARM)


def test_built_trials_match_the_plan(frozen):
    planned = dict((e.name, c) for e, c in run.planned_calls(run.PROGRAMME, CASES, frozen))
    assert planned == {name: calls for name, calls, _ in run.plan(len(CASES))[1:]}


def test_each_entry_builds_only_its_conditions_and_arm(frozen):
    for entry in run.PROGRAMME:
        for r, trials in run.build_entry(entry, CASES, frozen):
            assert {t["condition"] for t in trials} == set(entry.conditions), entry.name
            assert {t["arm"] for t in trials} == {entry.arm}, entry.name


def test_dry_run_end_to_end(tmp_path):
    _, out = _quiet(run.main, ["dry", "--out", str(tmp_path)])
    assert f"{JUDGE_CALLS} trials logged" in out and "0 parse failures" in out
    for section in ("SCREEN judge", "LADDER judge", "DISCRIMINATION judge", "N_EFF judge",
                    "H6 judge", "HEALTH judge"):
        assert section in out, section
    recs = [json.loads(line) for line in open(tmp_path / "trials.jsonl")]
    per_arm = {}
    for r in recs:
        per_arm.setdefault(r["arm"], set()).add(r["judge_model"])
    assert per_arm["long"] == {f"mock:{m}" for m in run.LENGTH_JUDGES}
    assert per_arm["short"] == {f"mock:{m}" for m in run.PRIMARY_JUDGES}
    assert len({(r["trial_id"], r["judge_model"]) for r in recs}) == len(recs)


class FakeRouter(MockBackend):
    """OpenRouterBackend's constructor, the mock's behaviour, and the provider the pin
    would serve -- unless told to substitute another."""
    substitute = {}

    def __init__(self, model, reasoning=None, provider=None, track_usage=False, **kw):
        super().__init__()
        self.name, self.reasoning, self.provider = f"openrouter:{model}", reasoning, provider
        self.last_provider = self.substitute.get(model) or run.PINS.get(model, (None, None))[1]


@pytest.fixture
def router(monkeypatch):
    FakeRouter.substitute = {}
    monkeypatch.setattr(run, "OpenRouterBackend", FakeRouter)
    return FakeRouter


def _generate(tmp_path, max_calls=GENERATE_CALLS):
    return _quiet(run.main, ["generate", "--out", str(tmp_path), "--max-calls", str(max_calls)])


def test_generate_writes_outputs_and_never_overwrites(tmp_path, router):
    _, out = _generate(tmp_path)
    assert f"{GENERATE_CALLS} calls. Stopped: None" in out
    report = json.load(open(tmp_path / "generation_report.json"))
    assert report["calls"] == GENERATE_CALLS and report["reporter"] == f"openrouter:{run.REPORTER}"
    assert all(s["status"] == "OK" for s in report["sources"].values())
    calls = [json.loads(line) for line in open(tmp_path / "generation_calls.jsonl")]
    assert len(calls) == GENERATE_CALLS and {c["role"] for c in calls} == {"reporter", "rater"}
    with pytest.raises(SystemExit, match="exists"):
        _generate(tmp_path)


def test_generate_stops_at_the_ceiling(tmp_path, router):
    _generate(tmp_path, max_calls=20)
    report = json.load(open(tmp_path / "generation_report.json"))
    assert "ceiling 20" in report["stopped"] and report["calls"] == 20


def _judge(tmp_path, *extra):
    return _quiet(run.main, ["judge", "--out", str(tmp_path), "--max-calls", str(JUDGE_CALLS),
                             *extra])


def test_judge_runs_the_programme_with_pins_and_reasoning_off(tmp_path, router):
    _generate(tmp_path)
    _, out = _judge(tmp_path)
    assert f"{JUDGE_CALLS} trials logged" in out and "stopped: None" in out
    recs = [json.loads(line) for line in open(tmp_path / "trials.jsonl")]
    assert recs[0]["judge_model"] != recs[1]["judge_model"]          # interleaved
    assert {r["reasoning_param"] == {"enabled": False} for r in recs} == {True}
    assert all(r["call_error"] is None and r["parsing_status"] == "ok" for r in recs)
    assert {r["serving_provider"] for r in recs} == {p[1] for p in run.PINS.values()}


def test_judge_stops_when_a_pinned_judge_is_served_elsewhere(tmp_path, router):
    _generate(tmp_path)
    router.substitute = {"anthropic/claude-opus-5": "Amazon Bedrock"}
    _, out = _judge(tmp_path, "--arms", "conflict", "--log", "staged.jsonl")
    assert "pinned to 'Claude Platform on AWS'" in out
    assert sum(1 for _ in open(tmp_path / "staged.jsonl")) == 3     # stopped on the 3rd call


def test_judge_refuses_a_plan_above_the_ceiling(tmp_path, router):
    _generate(tmp_path)
    with pytest.raises(SystemExit, match="stop before spending"):
        _quiet(run.main, ["judge", "--out", str(tmp_path), "--max-calls", "100"])
    assert not os.path.exists(tmp_path / "trials.jsonl")


def test_judge_refuses_a_leaking_frozen_set(tmp_path, router):
    _generate(tmp_path)
    path = tmp_path / "frozen_reports.json"
    frozen = json.load(open(path))
    frozen["M1"]["A"]["accepted"][0]["text"] = "The wiki puts the ME2103 lab logbook at 25%."
    json.dump(frozen, open(path, "w"))
    with pytest.raises(SystemExit, match="leak check failed"):
        _judge(tmp_path)
    assert not os.path.exists(tmp_path / "trials.jsonl")


def test_unknown_arm_is_refused(tmp_path, router):
    _generate(tmp_path)
    with pytest.raises(SystemExit, match="unknown arm"):
        _judge(tmp_path, "--arms", "conflict,longg")
