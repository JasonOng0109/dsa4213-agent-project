"""
Judge calls (proposal §3): render each trial's prompt, call the judge at temperature 0,
parse its JSON reply, and return one record per trial for the JSONL trial log.

A reply that does not parse is logged with an explicit status, never guessed at, and is
left out of decision denominators by the scorer.
"""

from __future__ import annotations
import json
import re

from pipeline.prompt import ABSTAIN, render

JUDGE_SYSTEM = "You are a careful, literal reader of the reports you are given."
# 700, not 150: a four-option "p" object is tight in 150, and a judge that reasons anyway
# would truncate and waste the call
MAX_TOKENS = 700
# statuses with no usable decision; no_match is a coherent answer outside the options,
# which is a result, not a parse failure
PARSE_FAILURES = ("ambiguous", "failed_fallback")


def _norm(text) -> str:
    """Tolerate formatting drift: "8200 mAh" for "8,200 mAh", case, spacing."""
    return re.sub(r"[\s,.]", "", str(text)).lower()


def parse(raw: str, options: list[str], world_truth: str | None = None,
          majority_claim: str | None = None, allow_abstain: bool = False) -> dict:
    """Statuses:
    ok                 -- a decision (or abstention) and a usable "p"
    no_match           -- a coherent answer string that is not an option
    ambiguous          -- no answer string at all
    failed_fallback    -- no JSON object could be read
    p_incomplete       -- decision kept; "p" misses an option or is not numeric
    p_sum_out_of_range -- decision kept; "p" sums outside 90-110
    An abstention is a third outcome, not a failure and not an error."""
    try:
        # tolerate the model wrapping the JSON in stray text or markdown fences
        m = re.search(r"\{.*\}", raw, re.S)
        obj = json.loads(m.group(0)) if m else json.loads(raw)
        return _parse_object(obj, options, world_truth, majority_claim, allow_abstain)
    except Exception:
        return _fail("failed_fallback")


def _parse_object(obj: dict, options, world_truth, majority_claim, allow_abstain) -> dict:
    by_norm = {_norm(o): o for o in options}
    answer = obj.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        return _fail("ambiguous")
    abstained = allow_abstain and _norm(answer) == _norm(ABSTAIN)
    if not abstained:
        answer = answer if answer in options else by_norm.get(_norm(answer))
        if answer is None:
            return _fail("no_match")
    raw_p = obj.get("p")
    out = {"forced_choice_decision": None if abstained else answer, "abstained": abstained,
           "parsing_status": "ok", "p_raw": raw_p, "p": None, "p_truth": None,
           "p_majority": None, "coherent": None, "margin": None, "confidence_elicited": None}
    p = {}
    for k, val in (raw_p.items() if isinstance(raw_p, dict) else []):
        opt = k if k in options else by_norm.get(_norm(k))
        if isinstance(val, str) and val.strip().isdigit():
            val = int(val)
        if opt is not None and isinstance(val, (int, float)) and not isinstance(val, bool) \
                and 0 <= val <= 100:
            p[opt] = val
    if set(p) != set(options):
        out["parsing_status"] = "p_incomplete"
        return out
    total = sum(p.values())
    if not 90 <= total <= 110:
        out["parsing_status"] = "p_sum_out_of_range"
        return out
    p = {o: round(100 * p[o] / total, 2) for o in options}
    out.update(p=p, p_truth=p.get(world_truth),
               p_majority=p[majority_claim] if majority_claim in p else None)
    if not abstained:
        out["confidence_elicited"] = p[answer]
        top = [o for o in options if p[o] == max(p.values())]
        out["coherent"] = answer == top[0] if len(top) == 1 else None
        # coherence sees inversion only; the margin sees indifference (34/33/33 is
        # coherent and means nothing)
        ranked = sorted(p.values(), reverse=True)
        out["margin"] = round(ranked[0] - ranked[1], 2)
    return out


def _fail(status: str) -> dict:
    return {"forced_choice_decision": None, "abstained": False, "parsing_status": status,
            "p_raw": None, "p": None, "p_truth": None, "p_majority": None, "coherent": None,
            "margin": None, "confidence_elicited": None}


def run_trials(trials: list[dict], judge, run_index: int = 1) -> list[dict]:
    """One record per trial: the trial's design fields, the raw reply, the parse, and
    what the backend reports about the call (serving provider, usage, reasoning)."""
    records = []
    for trial in trials:
        raw = judge.complete(system=JUDGE_SYSTEM, user=render(trial), temperature=0.0,
                             max_tokens=MAX_TOKENS)
        parsed = parse(raw, trial["answer_options"], trial["world_truth"],
                       majority_claim=trial.get("majority_claim"),
                       allow_abstain=trial.get("allow_abstain", False))
        decision = parsed["forced_choice_decision"]
        usage = getattr(judge, "last_usage", None)
        record = {
            "trial_id": f"{trial['case_id']}_{trial['condition']}_{trial['arm']}_run{run_index}",
            "judge_model": judge.name,
            "run_index": run_index,
            **{k: trial[k] for k in (
                "case_id", "domain", "condition", "arm", "factors", "world_truth",
                "majority_claim", "answer_options", "quality_dimension", "difficulty_tier",
                "allow_abstain", "length", "cue_position", "option_rotation", "wrong_offset",
                "indep_slot", "reports", "presentation_order_realized", "provenance_note")},
            "raw_judge_output": raw,
            **parsed,
            "decision_correct": decision == trial["world_truth"] if decision is not None else None,
            # which endpoint actually served the call, and what it cost
            "serving_provider": getattr(judge, "last_provider", None),
            "logprobs_available": getattr(judge, "logprobs_available", False),
            "token_logprobs": getattr(judge, "last_logprobs", None),
            "usage": usage,
            # logged always: which cells a judge reasoned in, and how much
            "reasoning_tokens": ((usage or {}).get("completion_tokens_details")
                                 or {}).get("reasoning_tokens"),
            "reasoning_param": getattr(judge, "reasoning", "n/a"),
        }
        records.append(record)
    return records


def write_jsonl(records: list[dict], path: str) -> None:
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
