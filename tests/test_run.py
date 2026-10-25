"""The runner: the programme matches the proposal's run plan, the dry run works end to
end, and the real paths (generate, judge) behave correctly with OpenRouter replaced by
the mock -- every stop condition included. Sockets are disabled throughout."""

import contextlib
import hashlib
import io
import json
import os

import pytest

from cases import CASES
from pipeline import run, score
from pipeline.conditions import LONG_ARM
from pipeline.llm import MockBackend
from pipeline.prompt import render

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
    21,720 calls and $37.48 for the 40-case main programme. The P0 check added after the
    pilot (docs/decisions.md, 2026-10-21) adds 12 calls per case, 480 at 40 cases."""
    rows = {name: (calls, cost) for name, calls, cost in run.plan(1)}
    every_case = ["generate and accept reports", "agreement", "conflict", "abstain", "screen"]
    assert [rows[n][0] for n in every_case] == [48, 144, 180, 72, 36]
    assert round(sum(rows[n][1] for n in every_case), 2) == 0.78
    rows40 = {name: (calls, cost) for name, calls, cost in run.plan(40)}
    assert rows40["long-conflict"][0] == 1200 and rows40["long-agreement"][0] == 240
    assert rows40["ladder"][0] == 1080
    proposal = {n: v for n, v in rows40.items() if n != "abstain-p0"}
    assert sum(c for c, _ in proposal.values()) == 21720
    assert round(sum(c for _, c in proposal.values()), 2) == 37.48
    assert rows["abstain-p0"][0] == 12 and rows40["abstain-p0"][0] == 480


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


# -- the main programme is what stage 1 judged and stage 2 will judge ------------------

MAIN = "runs/main"
# what stage 1's logs keep of each trial's design, beside the judge's reply
DESIGN = ("case_id", "domain", "condition", "arm", "factors", "world_truth", "majority_claim",
          "answer_options", "quality_dimension", "difficulty_tier", "allow_abstain", "length",
          "cue_position", "option_rotation", "wrong_offset", "indep_slot", "reports",
          "presentation_order_realized", "provenance_note")
STAGE1_LOGS = {"agreement": "trials-agreement.jsonl", "conflict": "trials-conflict.jsonl",
               "abstain": "trials-abstain.jsonl", "abstain-p0": "trials-abstain-p0.jsonl",
               "screen": "trials-screen.jsonl"}
# sha256 over every trial and its prompt, built from runs/main/frozen_reports.json on
# 2026-10-26, before the optional sub-experiments were added (docs/decisions.md)
MAIN_DIGESTS = {"agreement": "34b944518893fd0b", "conflict": "237a3afcfbca77e1",
                "abstain": "400cbed086cfa297", "abstain-p0": "e41cc37b31c91df9",
                "screen": "97fe97378c4753ee", "long-conflict": "391e2ad10c3cdb1a",
                "long-agreement": "692cae6a8f50b6bf", "ladder": "793cc9126a2fe3ac"}


@pytest.fixture(scope="module")
def main_frozen():
    with open(os.path.join(MAIN, "frozen_reports.json")) as f:
        return json.load(f)


def test_the_main_programme_rebuilds_what_stage_1_judged(main_frozen):
    """Every record in stage 1's logs shows the trial the code builds today, and every
    trial the code builds was judged."""
    for entry in run.PROGRAMME:
        if entry.name not in STAGE1_LOGS:
            continue
        built = {(t["case_id"], t["condition"], r): t
                 for r, trials in run.build_entry(entry, CASES, main_frozen) for t in trials}
        seen = set()
        for rec in score.load(os.path.join(MAIN, STAGE1_LOGS[entry.name])):
            key = (rec["case_id"], rec["condition"], rec["run_index"])
            assert {k: rec[k] for k in DESIGN} == {k: built[key][k] for k in DESIGN}, key
            seen.add(key)
        assert seen == set(built), entry.name


def test_the_main_programme_builds_the_same_trials_and_prompts(main_frozen):
    """Stage 2 runs from this code: its trials and prompts, and stage 1's, are the ones
    built before the optional sub-experiments were added."""
    def digest(entry):
        h = hashlib.sha256()
        for r, trials in run.build_entry(entry, CASES, main_frozen):
            for t in trials:
                h.update(json.dumps([r, t, render(t)], sort_keys=True).encode())
        return h.hexdigest()[:16]
    assert {e.name: digest(e) for e in run.PROGRAMME} == MAIN_DIGESTS



# -- the optional sub-experiments (docs/decisions.md, 2026-10-26) -----------------------

def _optional(name):
    return next(e for e in run.OPTIONAL if e.name == name)


def test_optional_entries_are_chosen_by_name_and_never_by_default():
    assert run.select_entries(None) == run.PROGRAMME
    assert [r[0] for r in run.plan(40)[1:]] == [e.name for e in run.PROGRAMME]
    assert run.select_entries("cross-check,long-neff") == [_optional("cross-check"),
                                                           _optional("long-neff")]
    calls = {name: c for name, c, _ in run.plan(40, run.OPTIONAL)[1:]}
    assert calls == {"reasoning-off-short": 72, "reasoning-off-long": 72,
                     "reasoning-on-short": 72, "reasoning-on-long": 72, "cross-check": 360,
                     "long-neff": 162}


def test_optional_trials_keep_to_their_cases_and_never_share_a_main_trial_id(frozen):
    main_ids = {(t["case_id"], t["condition"], t["arm"], r) for e in run.PROGRAMME
                for r, trials in run.build_entry(e, CASES, frozen) for t in trials}
    for entry in run.OPTIONAL:
        built = [(r, t) for r, trials in run.build_entry(entry, CASES, frozen) for t in trials]
        assert {t["case_id"] for _, t in built} == set(entry.cases), entry.name
        assert {t["condition"] for _, t in built} == set(entry.conditions), entry.name
        assert {t["arm"] for _, t in built} == {entry.arm}, entry.name
        assert {t.get("by_number", False) for _, t in built} == {entry.by_number}, entry.name
        if entry.name != "long-neff":     # long A4, A6 and A7 never ran in the main programme
            assert not main_ids & {(t["case_id"], t["condition"], t["arm"], r) for r, t in built}
        long = entry.length == "long" or entry.arm == "long"
        assert {t["length"] for _, t in built} == {"long" if long else "short"}, entry.name
    assert not main_ids & {(t["case_id"], t["condition"], t["arm"], r) for r, trials in
                           run.build_entry(_optional("long-neff"), CASES, frozen) for t in trials}


def test_long_neff_length_checks_a7_and_so_leaves_out_m38(main_frozen):
    """M38's C report comes to 87 words in every slot, one under the floor: its A7 cannot
    be built long, but the main programme's long entries never judge A7, so they build."""
    entry = _optional("long-neff")
    assert len(run.build_entry(entry, CASES, main_frozen)) == 6
    with pytest.raises(ValueError, match="M38: long reports off target"):
        run.build_entry(entry._replace(cases=("M38",)), CASES, main_frozen)
    long_conflict = next(e for e in run.PROGRAMME if e.name == "long-conflict")
    assert any(t["case_id"] == "M38"
               for _, trials in run.build_entry(long_conflict, CASES, main_frozen) for t in trials)


def test_generate_and_judge_keep_only_the_cases_named(tmp_path, router):
    _, out = _quiet(run.main, ["generate", "--out", str(tmp_path), "--max-calls", "96",
                               "--cases", "M1,M2"])
    assert "96 calls. Stopped: None" in out
    assert set(json.load(open(tmp_path / "frozen_reports.json"))) == {"M1", "M2"}
    _, out = _judge(tmp_path, "--cases", "M1,M2", "--arms", "conflict")
    recs = [json.loads(line) for line in open(tmp_path / "trials.jsonl")]
    assert len(recs) == 2 * 5 * 12 * 3 and {r["case_id"] for r in recs} == {"M1", "M2"}
    with pytest.raises(SystemExit, match="unknown case"):
        _judge(tmp_path, "--cases", "M1,M99", "--log", "other.jsonl")
    with pytest.raises(SystemExit, match="need cases --cases left out"):
        _judge(tmp_path, "--cases", "M1", "--arms", "reasoning-on-short", "--log", "other.jsonl")


def test_judge_sends_each_reasoning_setting_in_a_run_of_its_own(tmp_path, router):
    _generate(tmp_path)
    with pytest.raises(SystemExit, match="different reasoning settings"):
        _judge(tmp_path, "--arms", "reasoning-off-short,reasoning-on-short")
    _, out = _judge(tmp_path, "--arms", "reasoning-on-short,reasoning-on-long", "--log", "on.jsonl")
    assert "144 trials logged" in out and "stopped: None" in out
    recs = [json.loads(line) for line in open(tmp_path / "on.jsonl")]
    assert {r["reasoning_param"] == run.THINKING for r in recs} == {True}
    assert {r["arm"] for r in recs} == {"reasoning-on-short", "reasoning-on-long"}
    assert {r["judge_model"] for r in recs} == {f"openrouter:{run.SONNET}"}


def test_cross_check_answers_by_number_with_each_models_own_settings(tmp_path, router):
    _generate(tmp_path)
    _, out = _judge(tmp_path, "--arms", "cross-check", "--log", "cross.jsonl")
    assert "360 trials logged" in out and "0 parse failures" in out
    assert "each sent its own" in out
    recs = [json.loads(line) for line in open(tmp_path / "cross.jsonl")]
    assert {r["judge_model"] for r in recs} == {f"openrouter:{m}" for m in run.AUXILIARY}
    assert {r["reasoning_param"] == run.AUXILIARY_REASONING[r["judge_model"].split(":", 1)[1]]
            for r in recs} == {True}
    assert all(r["parsing_status"] == "ok" for r in recs)
    assert all(json.loads(r["raw_judge_output"])["answer"] in (1, 2, 3, 4) for r in recs)
