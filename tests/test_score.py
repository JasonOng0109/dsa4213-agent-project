"""The scorer's derived quantities: decision stability, the independence index and its
guard, and the confidence screen's ordering test. All arithmetic on records already
collected, so no backend is needed."""

import contextlib
import io
import math

from pipeline.score import (auroc, cell, neff, page_test, report_discrimination,
                            report_ladder, report_neff, screen_verdict, stability,
                            stability_chance)

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


def test_stability_chance_is_not_one_over_k():
    """The proposal's baselines: about 0.53 at 4 repeats, 0.47 at 6, 0.41 at 12."""
    for n, want in ((4, 0.53), (6, 0.47), (12, 0.41)):
        assert abs(stability_chance(n) - want) < 0.006, (n, stability_chance(n))
    assert stability_chance(1) == 1.0
    assert stability_chance(4, 5) < stability_chance(4)    # abstention adds a fifth value


def test_cell_carries_margin_and_stability():
    c = cell([_rec("15%", margin=1.0), _rec("15%", margin=3.0)])
    assert c["stability"] == 1.0 and c["n_stability"] == 2 and c["margin"] == 2.0
    assert c["stability_chance"] == round(stability_chance(2), 2)


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


def test_page_test_exact_values():
    """Exact p-values small enough to check by hand: one case has 6 equally likely orders."""
    up, down = [10, 50, 90], [90, 50, 10]
    assert page_test({"M1": up}) == (14, 1.0, 1 / 6, 1)        # the top of 6 orders
    assert page_test({"M1": down})[:2] == (10, -1.0)
    # ties are midranks and the null permutes them: (1.5, 1.5, 3) gives L = 13.5, which
    # 2 of the 6 orders reach
    assert page_test({"M1": [25, 25, 90]})[2] == 1 / 3
    assert page_test({"M1": [50, 50, 50]})[2] == 1.0
    assert page_test({"c0": up, "c1": up})[2] == 1 / 36
    # a case missing a level is left out
    assert page_test({"M1": up, "M2": [None, 50, 90]})[3] == 1


def test_screen_ordering_is_a_test_across_cases():
    """Proposal §5: a rank correlation and a test for ordered alternatives, not
    inspection. Retained only when Page's test gives one-sided p < 0.05."""
    up, down, flat = [10, 50, 90], [90, 50, 10], [50, 50, 50]
    assert screen_verdict({"c0": up, "c1": up})[0] == "retained"
    # one case can never pass, however well ordered: its best p is 1/6
    verdict, detail = screen_verdict({"M1": up})
    assert verdict == "EXCLUDED" and "too few cases" in detail
    assert screen_verdict({f"c{i}": up for i in range(5)} | {"c5": down})[0] == "retained"
    assert screen_verdict({f"c{i}": up for i in range(3)} | {f"b{i}": down for i in range(3)})[0] \
        == "EXCLUDED"
    assert screen_verdict({f"c{i}": flat for i in range(40)})[0] == "EXCLUDED"
    # a judge that always puts the irrelevant report lowest but swaps P1 and P2 in half
    # the cases still tracks informativeness; a per-case strict rule would exclude it
    half = {f"c{i}": up for i in range(20)} | {f"s{i}": [25, 60, 55] for i in range(20)}
    assert screen_verdict(half)[0] == "retained"


def test_auroc():
    assert auroc([90, 80], [10, 20]) == 1.0          # confident only when right
    assert auroc([10], [90]) == 0.0                  # confident only when wrong
    assert auroc([50, 50], [50]) == 0.5              # ties carry no information
    assert auroc([90], []) is None and auroc([], [10]) is None


def test_discrimination_is_within_condition_on_the_short_arm():
    def rec(cond, correct, conf, arm="short"):
        return {"judge_model": "mock", "arm": arm, "condition": cond,
                "decision_correct": correct, "confidence_elicited": conf}
    records = [rec("X1", True, 80), rec("X1", False, 40), rec("X1", False, 60),
               rec("A4", True, 95), rec("X1", True, 10, arm="long")]
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_discrimination(records)
    line = out.getvalue()
    assert "X1 1.00 (1/2)" in line and "A4 n/a (1/0)" in line


def test_ladder_reads_rungs_up_to_the_x5_ceiling():
    def recs(cond, arm, wording, answers):
        return [dict(_rec(a), judge_model="mock", case_id="M1", arm=arm, condition=cond,
                     factors={"quality_wording": wording}) for a in answers]
    records = (recs("W1", "ladder", "somewhat", ["25%", "25%"])
               + recs("W2", "ladder", "considerably", ["15%", "25%"])
               + recs("W3", "ladder", "far", ["15%", "15%"])
               + recs("X5", "short", "categorical", ["15%", "15%"])
               + recs("X5", "long", "categorical", ["25%", "25%"]))   # other arms ignored
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_ladder(records)
    assert ("W1 somewhat 0.00 (None) -> W2 considerably 0.50 (None) -> W3 far 1.00 (None) "
            "-> X5 categorical 1.00 (None)") in out.getvalue()
