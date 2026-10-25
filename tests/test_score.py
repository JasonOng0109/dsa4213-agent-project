"""The scorer's derived quantities: decision stability, the independence index and its
guard, the confidence screen's ordering and discrimination checks, and H6's test. All
arithmetic on records already collected, so no backend is needed."""

import contextlib
import io
import math
import random
from collections import Counter

from pipeline.score import (_mh_difference, auroc, auroc_p, cell, discrimination_verdict,
                            h6_reading, neff, page_test, report, report_discrimination,
                            report_h6, report_ladder,
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
        report_discrimination(records)
    line = out.getvalue()
    assert "X1 1.00 (1/2)" in line and "A4 n/a (1/0)" in line
    # a perfect AUROC on three decisions is not evidence: no condition has 10 per class.
    # The rule as first registered would exclude the judge; that verdict is only printed
    assert "not applied: not assessable" in line and "would be excluded" in line


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


def test_only_ordering_decides_whose_numbers_count():
    """docs/decisions.md, 2026-10-21: discrimination no longer excludes. A judge that is
    never wrong cannot be assessed for discrimination, which the rule as first registered
    counted as a fail; on two cases in the predicted order it passes ordering, so its
    n_eff is reported. On one case it fails ordering (p = 1/6), so it gets none, and the
    pilot's --show-excluded prints the arithmetic as a check that still counts as
    undefined."""
    def records(cases):
        p = {"A0": 25.0, "A1": 55.0, "A4": 85.0, "A6": 85.0, "A7": 85.0}
        screen = {"P0": ("irrelevant", 25.0), "P1": ("partial", 50.0),
                  "P2": ("determinate", 90.0)}
        return ([dict(_rec("15%"), judge_model="mock", case_id=cid, arm="short",
                      condition=c, run_index=1, p_truth=v, confidence_elicited=v)
                 for cid in cases for c, v in p.items()]
                + [dict(_rec("15%"), judge_model="mock", case_id=cid, arm="screen",
                        condition=lvl, run_index=1, p_truth=v,
                        factors={"informativeness": inf})
                   for cid in cases for lvl, (inf, v) in screen.items()])

    with contextlib.redirect_stdout(io.StringIO()) as out:
        report(records(["M1", "M2"]))
    text = out.getvalue()
    assert "would be excluded" in text and "-- retained" in text
    assert "judge failed the confidence screen" not in text
    assert "M1: mean P(truth)" in text and "-> {'A4': 2.18" in text
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report(records(["M1"]))
    text = out.getvalue()
    assert "judge failed the confidence screen" in text and "for checking only" not in text
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report(records(["M1"]), show_excluded=True)
    text = out.getvalue()
    assert "'for checking only, not a result': {'A4': 2.18" in text
    assert "N_EFF UNDEFINED judge mock: 1/1 cells (1.00)" in text


def test_neff_at_the_clip_reads_at_ceiling():
    """docs/decisions.md, 2026-10-21: a cell's mean P(truth) outside 1-99 is clipped
    before the logit, so it is a bound, not a value, and so is every number computed from
    it. GPT-5.4's pilot cells at 99.5-100 in A4, A6 and A7 would otherwise read IS 0 and
    RP 0; a clipped A1 clips the unit, so every value is at ceiling, the unit w too."""
    p = lambda **v: {c: {"p_truth": v.get(c, 85.0)} for c in ("A0", "A1", "A4", "A6", "A7")}
    top = neff(p(A0=25.0, A1=90.0, A4=99.5, A6=99.5, A7=100.0))
    assert top["clipped"] == 3
    assert all(top[k] == "at ceiling" for k in ("A4", "A6", "A7", "CN", "IS", "RP"))
    assert isinstance(top["w"], float)
    part = neff(p(A0=25.0, A1=55.0, A7=99.5))
    assert (part["A4"], part["A6"], part["CN"], part["RP"]) == (2.18, 2.18, 1.18, 0.0)
    assert part["A7"] == part["IS"] == "at ceiling"
    unit = neff(p(A0=25.0, A1=99.5))
    assert all(unit[k] == "at ceiling" for k in ("A4", "A6", "A7", "CN", "IS", "RP", "w"))
    assert "at ceiling" not in neff(p(A0=25.0, A1=55.0)).values()


def test_cells_at_ceiling_are_counted_per_judge():
    def recs(case_id, p_a7):
        p = {"A0": 25.0, "A1": 55.0, "A4": 85.0, "A6": 85.0, "A7": p_a7}
        return [dict(_rec("15%"), judge_model="mock", case_id=case_id, arm="short",
                     condition=c, p_truth=v) for c, v in p.items()]

    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_neff(recs("M1", 85.0) + recs("M2", 100.0))
    assert ("N_EFF UNDEFINED judge mock: 0/2 cells (0.00); a value at ceiling in 1/2"
            in out.getvalue())
    # an excluded judge's count reads the values printed for checking
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_neff(recs("M1", 85.0) + recs("M2", 100.0), excluded={"mock"},
                    show_excluded=True)
    assert ("N_EFF UNDEFINED judge mock: 2/2 cells (1.00); a value at ceiling in 1/2"
            in out.getvalue())


def test_answers_stated_at_100_are_counted_beside_neff():
    """docs/decisions.md, 2026-10-21: a judge that states 100 on whatever it picks passes
    ordering, since its mean P(truth) is 100 times its accuracy, so beside n_eff the
    scorer prints how many agreement-block answers put 100 on one option. The conflict
    block, and answers with no usable numbers, are not counted."""
    def rec(condition, top, margin=0.0):
        p = {"15%": top, "25%": 100 - top, "10%": 0.0, "30%": 0.0}
        return dict(_rec("15%", margin=margin), p=p, judge_model="mock", case_id="M1",
                    arm="short", condition=condition, p_truth=top)

    records = [rec("A0", 100.0, 100.0), rec("A1", 100.0, 100.0), rec("A4", 70.0, 40.0),
               rec("A6", 60.0, 20.0), rec("A7", 100.0, 100.0), rec("X1", 100.0, 100.0),
               rec("A2", 100.0, None)]
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_neff(records)
    assert "100 stated on one option in 3/5 (0.60) agreement-block answers" in out.getvalue()


def test_five_cases_give_discrimination_little_room():
    """docs/decisions.md, the pilot entry: shuffling whole cases, 5 cases allow only 120
    arrangements, so even a judge whose numbers separate right from wrong perfectly gets
    p near 1/120, while the pass level is 0.05 over the number of counted conditions
    (0.01 for five). Hence the pilot's --show-excluded."""
    perfect = {f"c{c}": {r: (90.0 if r < c + 3 else 50.0, r < c + 3) for r in range(12)}
               for c in range(5)}
    assert 0.005 < auroc_p(perfect) < 0.01


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
    assert "X1 flagged 2/2 (1.00), not flagged 0/2 (0.00)" in text
    assert "(Mantel-Haenszel): +1.00; own A7 1/4 (0.25)" in text
    # at 5, repeat 1 (margin 5) is no longer flagged; at 20, repeat 4 (margin 10) is
    assert "margin < 5: +0.67; margin < 20: +0.67" in text
    assert "the test applies: abstained in 2/4 conflict-block trials" in text
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_h6(records, excluded={"j"})
    assert "not assessed, the judge failed the confidence screen" in out.getvalue()
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_h6(records, excluded={"j"}, show_excluded=True)
    assert ("H6 judge j (failed the confidence screen: for checking only, not a result): "
            "3/5") in out.getvalue()


def test_h6_prints_the_p0_check_beside_a7():
    """docs/decisions.md, 2026-10-21: P0 offered the abstain option, where one irrelevant
    report cannot settle the answer, is printed beside A7 as a check, outside the test:
    its trials are nobody's twin. Logs without it, like the pilot's, print no line, and
    give no reading."""
    key = dict(judge_model="j", case_id="M1")
    records = ([dict(_rec("25%", margin=30), arm="short", condition="X1", run_index=1,
                     coherent=True, **key),
                dict(_rec(None), arm="abstain", condition="X1", run_index=1, **key)]
               + [dict(_rec(None), arm="abstain", condition="A7", run_index=r, **key)
                  for r in range(1, 5)]
               + [dict(_rec(None, abstained=r < 4), arm="abstain", condition="P0",
                       run_index=r, **key) for r in range(1, 5)])
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_h6(records)
    text = out.getvalue()
    assert "X1 flagged 0/0 (n/a), not flagged 0/1 (0.00)" in text
    assert "own A7 0/4 (0.00)" in text
    assert "not the test: abstained in P0, one irrelevant report, 3/4 (0.75)" in text
    assert "clean null: abstained in at least half of its P0 trials" in text
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_h6([r for r in records if r["condition"] != "P0"])
    text = out.getvalue()
    assert "abstained in P0" not in text and "not assessed: no P0 trials" in text


def test_h6_reading_uses_cut_offs_fixed_before_the_main_run():
    """docs/decisions.md, 2026-10-21: at least half of A7 is abstaining everywhere and
    under half of P0 is abstaining nowhere, either one not testable; at least half of P0
    but never in the conflict block is a clean null; any abstention in the conflict block
    means the test applies."""
    no, yes, half = [False] * 4, [True] * 4, [True, True, False, False]
    assert h6_reading(yes, half, yes).endswith("so it abstains everywhere")
    assert (h6_reading([True] + no, [True] + no, no)
            == "the test applies: abstained in 1/5 conflict-block trials")
    assert h6_reading(no, [True] + no, half).startswith("clean null")
    assert h6_reading(no, no, [True] + no).endswith("so it abstains nowhere")
    assert h6_reading(no, no, []) == "not assessed: no P0 trials"


def test_h6_compares_inside_each_condition_never_pooled():
    """A judge whose abstaining has nothing to do with its numbers inside any condition:
    in X1 half its trials are flagged and it abstains in half of each kind; in X5 a tenth
    are flagged and it never abstains. Pooled over the block, flagged trials would show
    10/24 abstentions against 10/56, an H6 effect no trial shows, made by X1 having more
    of both. Inside each condition the difference is 0."""
    def pair(cond, i, flagged, abstained):
        key = dict(judge_model="j", case_id=f"M{i // 4 + 1}", condition=cond,
                   run_index=i % 4 + 1)
        return [dict(_rec("25%", margin=5 if flagged else 30), arm="short", coherent=True,
                     **key),
                dict(_rec(None, abstained=abstained), arm="abstain", **key)]
    plan = {"X1": [(i < 20, i % 2 == 0) for i in range(40)],
            "X5": [(i < 4, False) for i in range(40)]}
    records = [r for cond, rows in plan.items() for i, (f, a) in enumerate(rows)
               for r in pair(cond, i, f, a)]
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_h6(records)
    text = out.getvalue()
    assert "X1 flagged 10/20 (0.50), not flagged 10/20 (0.50)" in text
    assert "X5 flagged 0/4 (0.00), not flagged 0/36 (0.00)" in text
    assert "(Mantel-Haenszel): +0.00" in text
    assert "10/24" not in text and "10/56" not in text


def test_mh_difference_weighs_each_condition_by_its_counts():
    # +0.5 inside one condition and -0.5 inside an equally sized one cancel
    assert _mh_difference([([1, 1], [1, 0]), ([1, 0], [1, 1])]) == 0.0
    # a condition with only flagged, or only unflagged, trials says nothing
    assert _mh_difference([([1, 1], []), ([], [0])]) is None
    assert _mh_difference([([1, 0], [0, 0]), ([1], [])]) == 0.5


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


def test_long_neff_borrows_a0_from_the_short_arm():
    """docs/decisions.md, 2026-10-26: the long arm's n_eff uses the optional long-neff
    entry's A4, A6 and A7, stage 2's long A1, and the short arm's A0, since A0 shows no
    reports. A long arm without A4, A6 and A7 gets no index."""
    def recs(arm, case_id, **p):
        return [dict(_rec("15%"), judge_model="mock", case_id=case_id, arm=arm, condition=c,
                     p_truth=v) for c, v in p.items()]

    short = recs("short", "M1", A0=25.0, A1=55.0, A4=85.0, A6=85.0, A7=85.0)
    long = recs("long", "M1", A1=55.0, A4=85.0, A6=60.0, A7=90.0)
    only_length_arm = recs("long", "M2", A1=55.0, A2=70.0) + recs("short", "M2", A0=25.0)
    with contextlib.redirect_stdout(io.StringIO()) as out:
        report_neff(short + long + only_length_arm)
    text = out.getvalue()
    assert "N_EFF judge mock | long | M1: mean P(truth) {'A0': 25.0, 'A1': 55.0" in text
    assert "N_EFF judge mock | long | M2" not in text
    assert "N_EFF UNDEFINED judge mock | long: 0/1 cells (0.00)" in text
    # the short arm's lines come first and read as before
    assert text.index("N_EFF judge mock | M1") < text.index("N_EFF judge mock | long | M1")
    assert "N_EFF UNDEFINED judge mock: 1/2 cells" in text
