"""The scorer's derived quantities: decision stability, the independence index and its
guard, the confidence screen's ordering and discrimination checks, and H6's test. All
arithmetic on records already collected, so no backend is needed."""

import contextlib
import io
import math
import random
from collections import Counter

from pipeline.score import (auroc, auroc_p, cell, discrimination_verdict, neff, page_test,
                            report, report_discrimination, report_h6, report_ladder,
                            report_neff, screen_verdict, stability, stability_chance,
                            unbacked)

OPTS = ["15%", "25%", "10%", "30%"]


def _by_case(correct, incorrect, repeats=1):
    """One condition as `auroc_p` reads it, {case_id: {run_index: (stated, correct)}}: each
    stated probability is its own case, repeated `repeats` times as exact copies."""
    decisions = [(s, True) for s in correct] + [(s, False) for s in incorrect]
    return {f"c{i:02d}": {run: d for run in range(1, repeats + 1)}
            for i, d in enumerate(decisions)}


def _mann_whitney_p(correct, incorrect):
    """The decision-level test 2C first used, kept here only to show what it gets wrong:
    the Mann-Whitney normal approximation, every decision counted as independent."""
    n1, n2 = len(correct), len(incorrect)
    n = n1 + n2
    u = sum((a > b) + 0.5 * (a == b) for a in correct for b in incorrect)
    ties = sum(t ** 3 - t for t in Counter(correct + incorrect).values())
    var = n1 * n2 / 12 * ((n + 1) - ties / (n * (n - 1)))
    if var <= 0:
        return 1.0
    return 0.5 * math.erfc((u - n1 * n2 / 2) / math.sqrt(var) / math.sqrt(2))


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
    # docs/methods.md's worked example: one case in order, one with P1 and P2 swapped
    assert page_test({"c0": [25, 50, 90], "c1": [25, 90, 50]})[:3] == (27, 0.75, 5 / 36)
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


def test_pilot_size_is_the_fewest_cases_that_survive_one_reversed_case():
    """docs/decisions.md: the pilot uses 5 cases, the fewest at which one fully reversed
    case does not fail an otherwise perfectly ordered judge at the fixed level."""
    up, down = [10, 50, 90], [90, 50, 10]
    verdicts = {n: screen_verdict({f"c{i}": up for i in range(n - 1)} | {"bad": down})[0]
                for n in range(2, 6)}
    assert verdicts == {2: "EXCLUDED", 3: "EXCLUDED", 4: "EXCLUDED", 5: "retained"}


def test_auroc():
    assert auroc([90, 80], [10, 20]) == 1.0          # confident only when right
    assert auroc([10], [90]) == 0.0                  # confident only when wrong
    assert auroc([50, 50], [50]) == 0.5              # ties carry no information
    assert auroc([90], []) is None and auroc([], [10]) is None


def test_discrimination_is_within_condition_on_the_short_arm():
    def rec(case, cond, correct, conf, arm="short"):
        return {"judge_model": "mock", "arm": arm, "condition": cond, "case_id": case,
                "run_index": 1, "decision_correct": correct, "confidence_elicited": conf}
    records = [rec("M1", "X1", True, 80), rec("M2", "X1", False, 40),
               rec("M3", "X1", False, 60), rec("M1", "A4", True, 95),
               rec("M4", "X1", True, 10, arm="long")]
    with contextlib.redirect_stdout(io.StringIO()) as out:
        excluded = report_discrimination(records)
    line = out.getvalue()
    assert "X1 1.00 (1/2)" in line and "A4 n/a (1/0)" in line
    # a perfect AUROC on three decisions is not evidence: no condition has 10 per class
    assert "not assessable" in line and excluded == {"mock"}


def test_auroc_p_shuffles_whole_cases():
    """One-sided p for AUROC above 0.5, the case as the unit. docs/methods.md's worked
    example: AUROC 0.75 on four decisions from four cases. Two of the six ways to split
    those four numbers into two right and two wrong reach 0.75, so luck alone does this
    1 time in 3."""
    assert abs(auroc_p(_by_case([90, 80], [70, 85])) - 1 / 3) < 0.03
    assert auroc_p(_by_case([80] * 10, [80] * 10)) == 1.0     # the same number every time
    assert auroc_p(_by_case([90] * 10, [60] * 10)) < 0.001
    assert auroc_p(_by_case([60] * 10, [90] * 10)) > 0.999    # one-sided: surer when wrong
    assert auroc_p(_by_case([90], [])) is None


def test_copies_of_a_case_add_no_evidence():
    """A case's repeats are near-copies, so twelve copies of each decision are no more
    evidence than one: shuffling whole cases gives exactly the same p, where counting each
    decision calls the copies significant."""
    right, wrong = [90, 85, 80, 70, 60], [88, 75, 65, 55, 50]
    once, twelve = _by_case(right, wrong), _by_case(right, wrong, repeats=12)
    assert auroc_p(twelve) == auroc_p(once) > 0.1
    assert _mann_whitney_p(right, wrong) > 0.05 > _mann_whitney_p(right * 12, wrong * 12)


def test_discrimination_passes_on_one_informative_condition():
    """docs/decisions.md: a condition counts with 10 correct and 10 incorrect decisions, A0
    never. Retained when one counted condition has AUROC above 0.5 at p below 0.05 divided
    by the number counted, even beside one that runs backwards, as X1 can when a judge
    confidently follows the two agreeing reports."""
    informative, backwards = _by_case([90] * 10, [60] * 10), _by_case([60] * 10, [90] * 10)
    flat = _by_case([80] * 10, [80] * 10)
    assert discrimination_verdict({"X1": backwards, "X5": informative})[0] == "retained"
    assert discrimination_verdict({"X1": flat, "X5": flat})[0] == "EXCLUDED"
    verdict, detail = discrimination_verdict({"X5": _by_case([90] * 30, [60] * 9)})
    assert verdict == "EXCLUDED" and "not assessable" in detail
    assert discrimination_verdict({"A0": informative})[0] == "EXCLUDED"
    # p about 0.03 passes alone, but not at 0.05 / 3 beside two more counted conditions
    middling = _by_case([90] * 6 + [80] * 3 + [70], [90] * 2 + [80] * 3 + [70] * 5)
    assert discrimination_verdict({"X3": middling})[0] == "retained"
    assert discrimination_verdict({"X1": flat, "X2": flat, "X3": middling})[0] == "EXCLUDED"


def test_discrimination_test_holds_its_level_where_a_fixed_mark_does_not():
    """docs/decisions.md: at 12 correct and 48 incorrect independent decisions, about one
    conflict condition in the pilot, a judge whose numbers carry no information passes
    the test about 1 time in 20, while a fixed AUROC mark of 0.60 lets it through more
    than 1 time in 10. Its numbers are drawn the same way whether it is right or wrong,
    with ties. The test runs on 200 of the draws, at 200 shuffles each, to stay fast."""
    rng = random.Random(0)
    values, weights = [50, 60, 70, 75, 80, 85, 90, 95, 100], [1, 2, 3, 2, 4, 3, 4, 3, 1]
    draws = [(rng.choices(values, weights, k=12), rng.choices(values, weights, k=48))
             for _ in range(2000)]
    test = sum(auroc_p(_by_case(ok, bad), shuffles=200) < 0.05
               for ok, bad in draws[:200]) / 200
    fixed = sum(auroc(ok, bad) >= 0.60 for ok, bad in draws) / len(draws)
    assert 0.02 < test < 0.09 and fixed > 0.10


def test_discrimination_holds_its_level_when_repeats_are_near_copies():
    """docs/decisions.md: the repeats of a case are near-copies. Here each of 200 judges
    has 10 cases of 12 repeats, states one number per case and is right or wrong at a rate
    set by the case, so its numbers carry no information. Counting each decision as
    evidence passes 51 of them, about 1 in 4; shuffling whole cases passes 9, about 1 in
    20, the level the screen promises."""
    rng = random.Random(0)
    values, weights = [50, 60, 70, 75, 80, 85, 90, 95, 100], [1, 2, 3, 2, 4, 3, 4, 3, 1]
    shuffled = counted = 0
    for _ in range(200):
        condition = {}
        for case in range(10):
            stated = rng.choices(values, weights)[0]      # the judge's number for this case
            p_right = rng.random()                         # how often it gets this case right
            condition[f"c{case}"] = {run: (stated, rng.random() < p_right)
                                     for run in range(1, 13)}
        right = [s for runs in condition.values() for s, ok in runs.values() if ok]
        wrong = [s for runs in condition.values() for s, ok in runs.values() if not ok]
        shuffled += auroc_p(condition, shuffles=200) < 0.05
        counted += _mann_whitney_p(right, wrong) < 0.05
    assert shuffled / 200 < 0.08 and counted / 200 > 0.20


def test_a_judge_failing_discrimination_gets_no_neff():
    """A judge whose numbers cannot be checked for discrimination (here it is never wrong)
    is excluded like one that fails ordering, so its n_eff is not reported."""
    p = {"A0": 25.0, "A1": 55.0, "A4": 85.0, "A6": 85.0, "A7": 85.0}
    records = [dict(_rec("15%"), judge_model="mock", case_id="M1", arm="short", condition=c,
                    run_index=1, p_truth=v, confidence_elicited=v) for c, v in p.items()]
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report(records)
    text = out.getvalue()
    assert "not assessable" in text and "judge failed the confidence screen" in text


def test_unbacked_flags_inversion_and_near_indifference():
    """docs/decisions.md: H6 flags a record whose answer is not its top option, or whose
    top two are less than 10 points apart. The work plan's examples: 34/33/33/0 has a
    margin of 1, 50/40/5/5 of 10 and 90/5/3/2 of 85."""
    r = lambda margin, coherent=True: {"margin": margin, "coherent": coherent}
    assert unbacked(r(1)) and unbacked(r(0, coherent=None))      # a tie at the top
    assert not unbacked(r(10)) and not unbacked(r(85))
    assert unbacked(r(85, coherent=False))                       # thinks one, says another
    assert unbacked(r(None, coherent=None)) is None              # no usable numbers
    assert unbacked(r(10), threshold=20) and not unbacked(r(5), threshold=5)


def test_h6_pairs_each_forced_choice_trial_with_its_abstention_twin():
    """Proposal §5: the abstention rate in the same trials as the flagged forced-choice
    records, against the rest, read beside the judge's own A7 rate. A twin shares the
    case, condition and repeat; repeat 5 has none, so it is only observed."""
    def forced(run, margin, coherent=True):
        return dict(_rec("25%", margin=margin), judge_model="j", case_id="M1", arm="short",
                    condition="X1", run_index=run, coherent=coherent)

    def twin(run, abstained, condition="X1"):
        return dict(_rec(None, abstained=abstained), judge_model="j", case_id="M1",
                    arm="abstain", condition=condition, run_index=run)
    records = ([forced(1, 5), forced(2, 30, coherent=False), forced(3, 40), forced(4, 10),
                forced(5, 0, coherent=None)]
               + [twin(1, True), twin(2, True), twin(3, False), twin(4, False)]
               + [twin(r, r == 1, "A7") for r in range(1, 5)])
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_h6(records)
    text = out.getvalue()
    assert ("3/5 conflict-block records do not identify the answer given (1 incoherent, "
            "2 by margin < 10)") in text
    assert "flagged 2/2 (1.00), not flagged 0/2 (0.00); own A7 1/4 (0.25)" in text
    assert "margin < 5: flagged 1/1 (1.00), not flagged 1/3 (0.33)" in text
    assert "margin < 20: flagged 2/3 (0.67), not flagged 0/1 (0.00)" in text
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_h6(records, excluded={"j"})
    assert "not assessed, the judge failed the confidence screen" in out.getvalue()


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
