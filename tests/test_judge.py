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


def test_an_answer_written_with_its_option_number_is_read():
    """The prompt numbers the options, and in the pilot GPT-5.4 copied the number into
    three A7 replies; this one is verbatim. The number must be the option's own, so a
    reply whose number and text disagree is still not an option."""
    opts = ["25%", "10%", "30%", "15%"]
    raw = '{"answer":"4. 15%","p":{"1. 25%":0,"2. 10%":0,"3. 30%":0,"4. 15%":100}}'
    r = parse(raw, opts, "15%")
    assert r["parsing_status"] == "ok" and r["forced_choice_decision"] == "15%"
    assert r["p_truth"] == 100.0 and r["coherent"] is True
    bad = parse('{"answer": "2. 15%", "p": {}}', opts, "15%")
    assert bad["parsing_status"] == "no_match"


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


def test_a_reply_naming_options_by_number_is_read():
    """The confidence cross-check asks for option numbers (docs/decisions.md, 2026-10-26).
    A number that is no option's is not guessed at, and an answer written as text is
    still read."""
    by = lambda raw: _parse(raw, by_number=True)
    ok = by('{"answer": 2, "p": {"1": 10, "2": 70, "3": 10, "4": 10}}')
    assert ok["parsing_status"] == "ok" and ok["forced_choice_decision"] == "25%"
    assert ok["p"] == {"15%": 10.0, "25%": 70.0, "10%": 10.0, "30%": 10.0}
    assert ok["p_truth"] == 10.0 and ok["coherent"] is True
    named = by('{"answer": "2", "p": {"1": 10, "2": 70, "3": 10, "4": 10}}')
    assert named["p_majority"] == 70.0
    assert by('{"answer": 5, "p": {}}')["parsing_status"] == "no_match"
    assert by('{"answer": "25%", "p": {"1": 10, "2": 70, "3": 10, "4": 10}}')["parsing_status"] == "ok"


def test_a_thinking_budget_comes_on_top_of_the_answer_and_its_text_is_kept(frozen):
    """OpenRouter needs max_tokens above the thinking budget, so a judge sent one gets the
    budget plus the answer's 700; its thinking text goes into the record."""
    class Judge(MockBackend):
        def __init__(self, reasoning):
            super().__init__()
            self.name, self.reasoning, self.asked = "judge", reasoning, []
            thinks = reasoning.get("max_tokens")
            self.last_reasoning = "B and C share one source." if thinks else None

        def complete(self, system, user, temperature=0.9, max_tokens=300):
            self.asked.append(max_tokens)
            return super().complete(system, user, temperature, max_tokens)

    trial = build_repeat("M1", CASES["M1"], frozen["M1"], 1)[8]          # X1
    thinking, off = Judge({"max_tokens": 2000}), Judge({"enabled": False})
    rec = run_trials([trial], thinking)[0]
    assert thinking.asked == [2700] and rec["reasoning_text"] == "B and C share one source."
    assert rec["reasoning_param"] == {"max_tokens": 2000}
    assert run_trials([trial], off)[0]["reasoning_text"] is None and off.asked == [700]
