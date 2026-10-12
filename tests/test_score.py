"""The scorer's derived quantities: decision stability, the independence index and its
guard, and the confidence screen's exclusion rule. All arithmetic on records already
collected, so no backend is needed."""

import contextlib
import io
import math

from pipeline.score import cell, neff, report_neff, screen_verdict, stability

OPTS = ["15%", "25%", "10%", "30%"]


def _rec(answer, abstained=False, status="ok", margin=None):
    """One repeat of a cell, trimmed to the fields the scorer reads."""
    return {"forced_choice_decision": answer, "abstained": abstained,
            "parsing_status": status, "decision_correct": answer == "15%" if answer else None,
            "p_truth": None, "p_majority": None, "margin": margin,
            "answer_options": OPTS, "factors": {}}


def test_stability_unanimous_and_even_split():
    """1.0 when every repeat agrees, 0.25 on an even split over four options, and the
    repeat count reported alongside."""
    assert stability([_rec("15%") for _ in range(6)]) == (1.0, 6)
    assert stability([_rec(o) for o in OPTS]) == (0.25, 4)
    assert stability([_rec("15%"), _rec("15%"), _rec("15%"), _rec("25%")]) == (0.75, 4)
    # parse failures are excluded from the denominator, abstentions are not
    assert stability([_rec("15%"), _rec("15%"), _rec(None, status="ambiguous")]) == (1.0, 2)
    assert stability([_rec(None, abstained=True) for _ in range(4)]) == (1.0, 4)
    assert stability([_rec(None, abstained=True), _rec("15%")]) == (0.5, 2)
    # an abstention is its own value, not the same as a no_match with no decision
    assert stability([_rec(None, abstained=True), _rec(None, status="no_match")]) == (0.5, 2)
    assert stability([_rec(None, status="ambiguous")]) == (None, 0)


def test_cell_carries_margin_and_stability():
    c = cell([_rec("15%", margin=1.0), _rec("15%", margin=3.0)])
    assert c["stability"] == 1.0 and c["n_stability"] == 2 and c["margin"] == 2.0


def test_parse_failures_leave_decision_denominators():
    """Two correct and one unparseable: 2/2 correct, not 2/3, and the failure is counted."""
    c = cell([_rec("15%"), _rec("15%"), _rec(None, status="ambiguous")])
    assert c["correct"] == 1.0 and c["parse_fail"] == 1 and c["n"] == 3
    # an off-list answer is a decision, so it stays in, as an incorrect one
    c = cell([_rec("15%"), _rec(None, status="no_match")])
    assert c["correct"] == 0.5 and c["no_match"] == 0.5
    assert cell([_rec(None, status="failed_fallback")])["correct"] is None


def _cells(p_a0, p_a1, p_rest=85.0):
    return {c: {"p_truth": p_a0 if c == "A0" else p_a1 if c == "A1" else p_rest}
            for c in ("A0", "A1", "A4", "A6", "A7")}


def test_neff_undefined_when_one_report_barely_moves_the_judge():
    """w = l(A1) - l(A0) below 0.2 logits is undefined, not a large number."""
    flat = neff(_cells(25.0, 28.0))          # w = 0.15 logits
    assert "undefined" in flat and "0.2 logits" in flat["undefined"] and "A4" not in flat
    moved = neff(_cells(25.0, 55.0))         # w = 1.30 logits
    assert "undefined" not in moved and moved["A4"] == 2.18
    # without the guard this is the "large number" the proposal refuses to report
    lg = lambda p: math.log(p / (1 - p))
    assert (lg(0.85) - lg(0.25)) / (lg(0.28) - lg(0.25)) > 15   # vs a normative 1 to 3


def test_negative_step_is_an_anomaly_not_a_value():
    """A supporting report that LOWERS belief in the truth gives a backwards unit; the
    index is not computed on it, however large the step."""
    backwards = neff(_cells(55.0, 25.0))     # w = -1.30 logits
    assert backwards.get("anomaly") and "negative" in backwards["undefined"]
    assert "A4" not in backwards


def test_undefined_rate_is_reported_per_judge():
    def recs(case_id, p_a1):
        p = {"A0": 25.0, "A1": p_a1, "A4": 85.0, "A6": 85.0, "A7": 85.0}
        return [dict(_rec("15%"), judge_model="mock", case_id=case_id, arm="short",
                     condition=c, p_truth=v) for c, v in p.items()]

    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_neff(recs("flat", 28.0) + recs("moved", 55.0))
    assert "N_EFF UNDEFINED judge mock: 1/2 cells (0.50)" in out.getvalue()


def test_screen_exclusion_rule():
    """Excluded only when failing on MORE than a third of cases."""
    ok, bad = [10, 50, 90], [90, 50, 10]
    assert screen_verdict({f"c{i}": ok for i in range(5)} | {"c5": bad})[0] == "retained"
    assert screen_verdict({f"c{i}": ok for i in range(4)} | {"c4": bad, "c5": bad})[0] == "retained"
    assert screen_verdict({f"c{i}": ok for i in range(3)} | {f"b{i}": bad for i in range(3)})[0] \
        == "EXCLUDED"
    assert screen_verdict({"M1": bad})[0] == "EXCLUDED"
    assert screen_verdict({"M1": ok})[0] == "retained"
