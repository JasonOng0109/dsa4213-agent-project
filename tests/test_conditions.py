"""The condition builder: rotations land where the schedule says, each block draws from
the right sources, long reports stay on target, and the screen is built as specified."""

import copy
import random

import pytest

from cases import CASES
from pipeline.conditions import (CONFLICT_BLOCK, CUE_POSITIONS, FACTORS, LADDER, LONG_MATCH,
                                 LONG_WORDS, LONG_ARM,
                                 build_conditions, build_repeat, build_screen,
                                 check_long_lengths, embed_in_filler, rotation_schedule)

CASE = CASES["M1"]


@pytest.fixture
def m1(frozen):
    return frozen["M1"]


def test_rotation_schedule():
    """12 repeats cover every (slot, truth position) pair once; the first 9 cover every
    (slot, cue) pair once; cue is not in lockstep with slot."""
    s12 = [rotation_schedule(r) for r in range(1, 13)]
    assert len({(s["indep_slot"], s["option_rotation"]) for s in s12}) == 12
    s9 = s12[:9]
    assert len({(s["indep_slot"], s["cue_position"]) for s in s9}) == 9
    assert any(CUE_POSITIONS.index(s["cue_position"]) != s["indep_slot"] for s in s9)


def test_truth_and_wrong_claim_schedule(m1):
    """Every (truth position, wrong-claim offset) pair once in 12 repeats, the offset not
    in lockstep with the slot, and the wrong claim not always next to the truth."""
    s12 = [rotation_schedule(r) for r in range(1, 13)]
    assert len({(s["option_rotation"], s["wrong_offset"]) for s in s12}) == 12
    assert any(s["wrong_offset"] != s["indep_slot"] for s in s12)
    gaps = {(t["answer_options"].index("25%") - t["answer_options"].index("15%")) % 4
            for r in range(1, 13) for t in build_repeat("M1", CASE, m1, r)
            if t["condition"] == "X1"}
    assert gaps == {1, 2, 3}


def test_agreement_offsets_are_even_over_six_repeats():
    assert sorted(rotation_schedule(r)["wrong_offset_agreement"] for r in range(1, 7)) == \
        [0, 0, 1, 1, 2, 2]


def test_builder_realises_the_schedule(m1):
    for r in range(1, 13):
        s = rotation_schedule(r)
        trials = {t["condition"]: t for t in build_repeat("M1", CASE, m1, r, length="long")}
        assert list(trials) == list(FACTORS)
        for t in trials.values():
            opts = t["answer_options"]
            assert opts.index(CASE["world_truth"]) == s["option_rotation"]
            rest = [i for i in range(4) if i != s["option_rotation"]]
            off = (s["wrong_offset"] if t["condition"] in CONFLICT_BLOCK + LADDER
                   else s["wrong_offset_agreement"])
            assert t["wrong_offset"] == off
            assert opts.index(CASE["sources"]["A"]["claim"]) == rest[off]
        x1 = trials["X1"]
        assert x1["reports"][s["indep_slot"]]["source_key"] == "B"
        for rep in x1["reports"]:
            sents = CASE["filler_sets"][rep["slot"]]
            cut = {"start": 0, "middle": len(sents) // 2, "end": len(sents)}[s["cue_position"]]
            assert rep["text"] == " ".join(sents[:cut] + [rep["paraphrase"]] + sents[cut:])


def test_long_word_counts(m1):
    lo, hi = LONG_WORDS
    seen = set()
    for r in range(1, 10):
        for t in build_repeat("M1", CASE, m1, r, length="long"):
            if t["condition"] == "A2":  # three long reports in one message
                continue
            for rep in t["reports"]:
                assert lo <= len(rep["text"].split()) <= hi, (t["condition"], rep["filler_set"])
                seen.add(rep["filler_set"])
    assert seen == {0, 1, 2}


def test_shared_source_reports_carry_different_filler(m1):
    """R12: the two reports of the shared source in the conflict block never share padding."""
    for r in range(1, 13):
        for t in build_repeat("M1", CASE, m1, r, length="long"):
            if t["condition"] not in CONFLICT_BLOCK:
                continue
            pair = [x for x in t["reports"] if x["source_key"] == "A"]
            assert len(pair) == 2 and pair[0]["filler_set"] != pair[1]["filler_set"]
            pads = [x["text"].replace(x["paraphrase"], "") for x in pair]
            assert pads[0] != pads[1]


def test_blocks_draw_from_the_right_sources(m1):
    """R14: agreement from B; A7 from B, C, D; conflict and ladder A twice, B once."""
    for r in range(1, 7):
        for t in build_repeat("M1", CASE, m1, r):
            keys = sorted(x["source_key"] for x in t["reports"])
            if t["condition"] in CONFLICT_BLOCK + LADDER:
                assert keys == ["A", "A", "B"], (t["condition"], keys)
            elif t["condition"] == "A7":
                assert keys == ["B", "C", "D"]
            elif t["condition"] != "A0":
                assert set(keys) == {"B"}, (t["condition"], keys)


def test_short_paraphrase_fails_loudly(m1):
    """A long report off target raises; it is never emitted."""
    short = copy.deepcopy(m1)
    short["A"]["accepted"][0]["text"] = "Logbook: 25%."
    with pytest.raises(ValueError, match="off target"):
        build_conditions("M1", CASE, short, random.Random(1), length="long",
                         cue_position="start")
    build_conditions("M1", CASE, short, random.Random(1))  # short reports are fine


def test_only_conditions_the_length_arm_runs_are_length_checked(m1):
    """A7 (B, C, D) is built long but never judged long, so a 97-word A7 report does not
    stop the build; the same report in the conflict block does."""
    assert "A7" not in LONG_ARM
    over = " ".join(["word"] * 16) + " 15%."             # 17 words + 80 of filler = 97
    in_a7 = copy.deepcopy(m1)
    in_a7["C"]["accepted"][0]["text"] = over
    trials = build_conditions("M1", CASE, in_a7, random.Random(1), length="long",
                              cue_position="start")
    a7 = next(t for t in trials if t["condition"] == "A7")
    assert max(len(r["text"].split()) for r in a7["reports"]) == 97
    in_conflict = copy.deepcopy(m1)
    in_conflict["A"]["accepted"][0]["text"] = over
    with pytest.raises(ValueError, match="off target"):
        build_conditions("M1", CASE, in_conflict, random.Random(1), length="long",
                         cue_position="start")


def test_padded_mock_reports_skip_the_length_check(m1):
    """The same off-target report passes when its source is a mock's padded relay: its
    length is not a reporter's, so R20's lint warning is the check for that case."""
    short = copy.deepcopy(m1)
    short["A"]["accepted"][0]["text"] = "Logbook: 25%."
    short["A"]["padded"] = True
    build_conditions("M1", CASE, short, random.Random(1), length="long",
                     cue_position="start")


def test_band_implies_the_length_cap():
    """88-96 words: inside the band the 1.10 cap cannot be broken (96 / 88 = 1.09),
    whereas a band reaching 100 would allow 100 / 88 = 1.14."""
    lo, hi = LONG_WORDS
    assert (lo, hi) == (88, 96) and hi / lo <= LONG_MATCH


def test_report_above_the_band_fails_loudly():
    # 17 words over slot 0's 80-word filler = 97
    para = " ".join(["word"] * 16) + " 15%."
    reps = [{"source_key": "B", "slot": 0,
             "text": embed_in_filler(CASE["filler_sets"][0], para, "start")}]
    assert len(reps[0]["text"].split()) == 97
    with pytest.raises(ValueError, match="off target"):
        check_long_lengths("M1", reps)


def test_screen_trials(m1):
    """Three levels per option rotation, one report each, no provenance or note; P1 is
    screen_partial and P2 the frozen B report."""
    for r in range(1, 5):
        s = rotation_schedule(r)
        ts = build_screen("M1", CASE, m1, s["option_rotation"], s["wrong_offset"])
        assert [t["condition"] for t in ts] == ["P0", "P1", "P2"]
        assert all(t["arm"] == "screen" and len(t["reports"]) == 1
                   and t["provenance_note"] is None and t["reports"][0]["provenance_id"] is None
                   for t in ts)
        assert ts[1]["reports"][0]["text"] == CASE["screen_partial"]
        assert ts[2]["reports"][0]["text"] == m1["B"]["accepted"][0]["text"]
        assert ts[0]["answer_options"].index("15%") == s["option_rotation"]
        # the abstention arm's P0 check: the same trials, offering the abstain option
        ta = build_screen("M1", CASE, m1, s["option_rotation"], s["wrong_offset"],
                          allow_abstain=True)
        assert all(t["arm"] == "abstain" and t["allow_abstain"] for t in ta)
        assert [t["answer_options"] for t in ta] == [t["answer_options"] for t in ts]


def test_both_lengths_assemble_for_every_condition(m1):
    """Every condition builds at both lengths from the same paraphrases."""
    for r in range(1, 7):
        short = build_repeat("M1", CASE, m1, r)
        long = build_repeat("M1", CASE, m1, r, length="long")
        assert [t["condition"] for t in short] == [t["condition"] for t in long] == list(FACTORS)
        for ts, tl in zip(short, long):
            assert [x["text"] for x in ts["reports"]] == [x["paraphrase"] for x in tl["reports"]]


def test_disclosure_notes(m1):
    """X3 states dependence only, X4 quality only, X5 both; X2 shows the source types."""
    t = {x["condition"]: x for x in build_repeat("M1", CASE, m1, 1)}
    assert "same underlying source" in t["X3"]["provenance_note"]
    assert "primary, authoritative" not in t["X3"]["provenance_note"]
    assert "same underlying source" not in t["X4"]["provenance_note"]
    assert t["X5"]["provenance_note"].startswith(t["X3"]["provenance_note"])
    assert {r["provenance_id"] for r in t["X2"]["reports"]} == {
        CASE["sources"][k]["provenance"]["type"] for k in "AB"}
    assert t["X1"]["provenance_note"] is None


def test_wording_ladder(m1):
    """W1-W3 are X5 with only the intensity phrase of the quality statement changed: same
    reports, same dependence note, same rotation, their own arm."""
    t = {x["condition"]: x for x in build_repeat("M1", CASE, m1, 5)}
    x3_note = t["X3"]["provenance_note"]
    for w, word in zip(LADDER, ["somewhat", "considerably", "far"]):
        rung = t[w]
        assert rung["arm"] == "ladder" and rung["factors"]["quality_wording"] == word
        assert rung["provenance_note"].startswith(x3_note)
        assert f" is {word} more reliable than the source shared by " in rung["provenance_note"]
        for key in ("reports", "answer_options", "indep_slot", "wrong_offset", "majority_claim"):
            assert rung[key] == t["X5"][key], key
        assert {k: v for k, v in rung["factors"].items() if k != "quality_wording"} == \
            {k: v for k, v in FACTORS["X5"].items() if k != "quality_wording"}
    assert t["X5"]["factors"]["quality_wording"] == "categorical"
    assert t["X5"]["arm"] == "short"
