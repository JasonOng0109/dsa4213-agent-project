"""The acceptance filter and freezing, with a scripted rater. These prove the plumbing
-- a false rubric flag rejects, an unparseable rating rejects, ties break toward
diversity -- not that a live rater returns the right flags."""

import json

from cases import CASES
from pipeline.llm import MockBackend
from pipeline.reporter import (RUBRIC_FLAGS, RUBRIC_PROMPT, freeze_order, freeze_sources,
                               generate_and_freeze, select)

M1 = CASES["M1"]


class ScriptedRater:
    """Returns the rubric a correct rater would give, per candidate text."""
    name = "scripted"

    def __init__(self, verdicts, raw=None):
        self.verdicts, self.raw = verdicts, raw

    def complete(self, system, user, temperature=0.9, max_tokens=300):
        if self.raw is not None:
            return self.raw
        cand = user.split("Candidate report: ", 1)[1].split("\n", 1)[0]
        flags = dict({f: True for f in RUBRIC_FLAGS}, **self.verdicts.get(cand, {}))
        return json.dumps(dict(flags, score=100))


def _select(cands, key, n, rater, avoid=()):
    return select(cands, M1["sources"][key], n, rater, question=M1["question"], avoid=avoid)


def test_rubric_asks_all_four_questions():
    for f in RUBRIC_FLAGS:
        assert f"- {f}:" in RUBRIC_PROMPT
    assert "denominator or scope" in RUBRIC_PROMPT


def test_dropped_detail_is_rejected():
    drop = "The lab logbook carries 15% of the final module grade."   # module code dropped
    ok = "For ME2103, the lab logbook is 15% of the final module grade."
    res = _select([drop, ok], "B", 1, ScriptedRater({drop: {"all_details": False}}))
    assert [a["text"] for a in res["accepted"]] == [ok]
    rejected = next(s for s in res["all_scored"] if s["text"] == drop)
    assert rejected["rubric"]["failed"] == ["all_details"]
    assert "rubric false: ['all_details']" in rejected["rejected_because"]


def test_change_of_whole_is_rejected():
    """scope_kept catches a change to a DIFFERENT whole, which would make A's and B's
    claims compatible and quietly empty the conflict block."""
    other = "The ME2103 lab logbook carries 15% of the continuous-assessment mark."
    b1 = "Fifteen percent of the final ME2103 module grade comes from the lab logbook."
    res = _select([other, b1], "B", 1, ScriptedRater({other: {"scope_kept": False}}))
    assert [a["text"] for a in res["accepted"]] == [b1]
    res = _select([other], "B", 1, ScriptedRater({other: {"scope_kept": False}}))
    assert not res["sufficient"]        # never accepted, even when it is the only one


def test_unparseable_rating_rejects():
    res = _select(["The lab logbook is 15% of the ME2103 final module grade."], "B", 1,
                  ScriptedRater({}, raw="95"))
    assert not res["accepted"]
    assert res["all_scored"][0]["rubric"]["failed"] == list(RUBRIC_FLAGS)


def test_ties_break_toward_diversity():
    """Four candidates for M1/A, all rated 1.00. Taking them in generation order would
    freeze the first: the source sentence with one word changed."""
    cands = [
        "The ME2103 lab logbook counts for 25% of the final module grade.",
        "The lab logbook for ME2103 constitutes 25% of the final grade for the module.",
        "Twenty-five percent of the final ME2103 module grade comes from the lab logbook.",
        "A 25% share of the ME2103 final grade is derived from the lab logbook.",
    ]
    res = _select(cands, "A", 2, ScriptedRater({}))
    picked = [a["text"] for a in res["accepted"]]
    assert cands[0] not in picked and len(picked) == 2


def test_cross_source_backstop():
    """A near copy across sources: D1 overlaps an accepted B1 at 0.61. With B1 in `avoid`,
    that D candidate is refused and a distinct one taken instead."""
    b1 = "Fifteen percent of the final grade for the ME2103 module is derived from the lab logbook."
    d1 = "Fifteen percent of the final grade for module ME2103 is derived from the lab logbook."
    d_ok = "Towards a student's overall ME2103 result, the lab logbook contributes a 15% share."
    res = _select([d1, d_ok], "D", 1, ScriptedRater({}), avoid=[b1])
    assert [a["text"] for a in res["accepted"]] == [d_ok]
    rejected = next(x for x in res["all_scored"] if x["text"] == d1)
    assert rejected["cross_overlap"] > 0.5
    assert any("cross-source" in why for why in rejected["rejected_because"])


def test_report_far_from_the_source_length_is_rejected():
    """R20: a report more than 3 words longer or shorter than its source would not fit the
    filler written for the source, so it is refused unless the check is off (a mock's
    padded rewordings)."""
    long = "In the ME2103 module, the lab logbook carries exactly 15% of the overall final grade."
    ok = "For ME2103, the lab logbook is 15% of the final module grade."
    res = _select([long, ok], "B", 1, ScriptedRater({}))
    assert [a["text"] for a in res["accepted"]] == [ok]
    why = next(s for s in res["all_scored"] if s["text"] == long)["rejected_because"]
    assert why == ["length +4 words > 3 from the source"]
    res = select([long], M1["sources"]["B"], 1, ScriptedRater({}), question=M1["question"],
                 check_length=False)
    assert res["sufficient"]


def test_rejection_reasons_cover_copies_leaks_and_spares():
    copy = M1["sources"]["A"]["content"]
    leak = "Per the wiki, the ME2103 lab logbook is a quarter of your final module grade."
    a1 = "A quarter of your final ME2103 module grade comes from the lab logbook."
    a2 = "Your lab logbook in ME2103 makes up 25% of your final module grade."
    a3 = "Of your final module grade in ME2103, the lab logbook accounts for 25%."
    res = _select([copy, leak, a1, a2, a3], "A", 2, ScriptedRater({}))
    why = {s["text"]: s["rejected_because"] for s in res["all_scored"]}
    assert "copy overlap" in why[copy][0]
    assert why[leak] == ["leak ['wiki']"]
    assert sum(s["accepted"] for s in res["all_scored"]) == 2
    assert ["eligible but not needed (quota filled first)"] in why.values()


def test_six_candidates_per_round():
    calls = []

    class Reporter:
        def complete(self, system, user, temperature=0.9, max_tokens=300):
            calls.append(user)
            return f"Candidate number {len(calls)} says the lab logbook is 15% of ME2103."
    res = generate_and_freeze(M1["sources"]["D"], M1["question"], 1, Reporter(),
                              ScriptedRater({}), max_rounds=1)
    assert len(calls) == 6 and res["calls"] == 12


def test_freeze_order_is_r18():
    assert freeze_order(M1) == ["B", "A", "C", "D"]


def test_mock_freezes_every_m1_source_in_one_round():
    results = list(freeze_sources({"M1": CASES["M1"]}, MockBackend(), MockBackend()))
    assert [k for _, k, _ in results] == ["B", "A", "C", "D"]
    for _, key, res in results:
        assert res["sufficient"] and res["rounds_needed"] == 1, key
        assert len(res["accepted"]) == M1["sources"][key]["n_paraphrases_needed"]


def test_only_sources_without_hand_written_mock_rewordings_are_padded():
    """M1's sentences are in the mock's table, so their reports are realistic lengths and
    keep the length check; a sentence the table lacks gets the padded relay."""
    results = list(freeze_sources({"M1": M1}, MockBackend(), MockBackend()))
    assert not any(res.get("padded") for _, _, res in results)
    assert MockBackend().pads("A sentence no case has written yet.")
