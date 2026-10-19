"""The reply parser and the trial record: every status, the derived fields (coherence,
margin, the probability of the truth and of the majority claim), and the fields the
analysis groups by."""

from cases import CASES
from pipeline.conditions import FACTORS, build_repeat, build_screen
from pipeline.judge import parse, run_trials
from pipeline.llm import MockBackend
from pipeline.prompt import ABSTAIN

OPTS = ["15%", "25%", "10%", "30%"]


def _parse(raw, **k):
    return parse(raw, OPTS, "15%", majority_claim="25%", **k)


def test_parser_statuses():
    ok = _parse('{"answer": "25%", "p": {"15%": 30, "25%": 50, "10%": 10, "30%": 15}}')
    assert ok["parsing_status"] == "ok" and ok["forced_choice_decision"] == "25%"
    assert round(sum(ok["p"].values())) == 100 and ok["coherent"] is True
    assert ok["p_majority"] == ok["p"]["25%"] and ok["p_truth"] == ok["p"]["15%"]
    assert _parse('{"answer": "20%", "p": {}}')["parsing_status"] == "no_match"
    assert _parse('{"p": {}}')["parsing_status"] == "ambiguous"
    assert _parse("not json")["parsing_status"] == "failed_fallback"
    far = _parse('{"answer": "15%", "p": {"15%": 80, "25%": 80, "10%": 0, "30%": 0}}')
    assert far["parsing_status"] == "p_sum_out_of_range" and far["p_truth"] is None
    assert far["forced_choice_decision"] == "15%"     # a usable decision is never discarded
    part = _parse('{"answer": "15%", "p": {"15%": 100}}')
    assert part["parsing_status"] == "p_incomplete" and part["forced_choice_decision"] == "15%"
    tie = _parse('{"answer": "15%", "p": {"15%": 40, "25%": 40, "10%": 10, "30%": 10}}')
    assert tie["coherent"] is None


def test_parser_tolerates_fences_and_formatting_drift():
    fenced = _parse('```json\n{"answer": "15 %", "p": {"15%": 70, "25%": 20, "10%": 5, "30%": 5}}\n```')
    assert fenced["parsing_status"] == "ok" and fenced["forced_choice_decision"] == "15%"


def test_abstention_is_its_own_outcome():
    ab = _parse(f'{{"answer": "{ABSTAIN}", "p": {{"15%": 40, "25%": 40, "10%": 10, "30%": 10}}}}',
                allow_abstain=True)
    assert ab["abstained"] and ab["parsing_status"] == "ok"
    assert ab["forced_choice_decision"] is None and ab["confidence_elicited"] is None
    # without the abstain arm, the sentinel is just not an option
    assert _parse(f'{{"answer": "{ABSTAIN}", "p": {{}}}}')["parsing_status"] == "no_match"


def test_indifference_is_coherent_with_a_tiny_margin():
    """34/33/33 passes the coherence check -- the flag sees only inversion -- while the
    margin sees the indifference it hides."""
    flat = _parse('{"answer": "15%", "p": {"15%": 34, "25%": 33, "10%": 33, "30%": 0}}')
    assert flat["coherent"] is True and flat["margin"] == 1.0
    sharp = _parse('{"answer": "25%", "p": {"15%": 10, "25%": 70, "10%": 10, "30%": 10}}')
    assert sharp["coherent"] is True and sharp["margin"] == 60.0
    inverted = _parse('{"answer": "25%", "p": {"15%": 50, "25%": 40, "10%": 5, "30%": 5}}')
    assert inverted["coherent"] is False


def test_margin_is_none_where_there_is_nothing_to_measure():
    ab = _parse(f'{{"answer": "{ABSTAIN}", "p": {{"15%": 40, "25%": 40, "10%": 10, "30%": 10}}}}',
                allow_abstain=True)
    assert ab["margin"] is None
    assert _parse('{"answer": "15%", "p": {"15%": 100}}')["margin"] is None    # p_incomplete
    assert _parse('{"p": {}}')["margin"] is None                               # ambiguous
    assert _parse("not json")["margin"] is None                                # failed_fallback
    # the margin is taken on the rescaled p, not the raw numbers
    scaled = _parse('{"answer": "15%", "p": {"15%": 55, "25%": 25, "10%": 15, "30%": 15}}')
    assert scaled["margin"] == round(50.0 - 22.73, 2)
    # so 50 against 40 written with a total of 105 is 47.62 against 38.10, and falls under
    # H6's 10-point cut-off (docs/methods.md, "Margin")
    over = _parse('{"answer": "25%", "p": {"15%": 40, "25%": 50, "10%": 10, "30%": 5}}')
    assert over["margin"] == 9.52


def test_records_carry_the_analysis_fields(frozen):
    m1, case = frozen["M1"], CASES["M1"]
    trials = (build_repeat("M1", case, m1, 1) + build_repeat("M1", case, m1, 2, length="long")
              + build_repeat("M1", case, m1, 3, allow_abstain=True)
              + build_screen("M1", case, m1))
    records = run_trials(trials, MockBackend(), run_index=1)
    need = {"trial_id", "judge_model", "arm", "condition", "factors", "allow_abstain", "length",
            "cue_position", "option_rotation", "wrong_offset", "indep_slot", "answer_options",
            "majority_claim", "abstained", "p", "p_raw", "p_truth", "p_majority", "margin",
            "coherent", "decision_correct", "serving_provider", "usage", "reasoning_tokens",
            "logprobs_available", "parsing_status", "raw_judge_output"}
    for rec in records:
        assert need <= set(rec), need - set(rec)
        assert set(FACTORS["X1"]) <= set(rec["factors"])
        assert rec["parsing_status"] == "ok"
    assert any(rec["abstained"] for rec in records)
    assert all(rec["trial_id"] == f"M1_{rec['condition']}_{rec['arm']}_run1" for rec in records)
