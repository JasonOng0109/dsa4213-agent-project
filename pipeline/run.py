"""
The command line. Real steps spend money and each needs explicit approval; `dry` and
`plan` spend nothing.

    python -m pipeline.run dry                  # the whole programme on the mock backend
    python -m pipeline.run plan [--cases 40]    # pre-flight call and cost estimate

    uv run --env-file .env python -m pipeline.run balance
    uv run --env-file .env python -m pipeline.run probe
    uv run --env-file .env python -m pipeline.run generate --max-calls N
    uv run --env-file .env python -m pipeline.run judge --max-calls N [--arms conflict,...]

`--arms` also selects the optional sub-experiments by name (OPTIONAL), and `--cases M1,M2`
keeps only those cases, for the wording-robustness rerun (docs/decisions.md, 2026-10-26).

Real outputs go to runs/ and are never overwritten: frozen reports and trial logs are
evidence, so a step whose output exists refuses to start until the old file is moved.
"""

from __future__ import annotations
import argparse
import json
import math
import os
from typing import NamedTuple

from pipeline.conditions import (ABSTAIN_ARM, AGREEMENT_BLOCK, CONFLICT_BLOCK, LADDER,
                                 LONG_AGREEMENT, LONG_ARM, SCREEN_LEVELS, build_repeat,
                                 build_screen, rotation_schedule)
from pipeline.judge import PARSE_FAILURES, run_trials, write_jsonl
from pipeline.llm import MockBackend, OpenRouterBackend, key_status
from pipeline.reporter import attribution_in, freeze_sources, leak_terms, leaks_in
from pipeline import score

# -- models (proposal §3): the one place model ids live in code -------------------------

REPORTER = "google/gemma-4-31b-it"       # a family no judge comes from
RATER = "anthropic/claude-sonnet-5"      # also a primary judge: a stated limitation
PRIMARY_JUDGES = ["anthropic/claude-sonnet-5", "openai/gpt-5.4", "anthropic/claude-opus-5"]
LENGTH_JUDGES = ["anthropic/claude-sonnet-5", "openai/gpt-5.4"]   # one per developer
# never judge a main-arm trial; they return token probabilities for the optional
# confidence cross-check. Routed only to endpoints honouring every parameter.
AUXILIARY = ["qwen/qwen3.6-27b", "meta-llama/llama-4-maverick"]
AUXILIARY_ROUTING = {"require_parameters": True}
# the reasoning parameter each one is sent (runs/main/probe-2026-10-26.json): Qwen thinks
# unless told not to, and Llama's endpoints take no reasoning parameter, which under
# AUXILIARY_ROUTING would leave it no endpoint at all
AUXILIARY_REASONING = {"qwen/qwen3.6-27b": {"enabled": False}, "meta-llama/llama-4-maverick": None}
# Each primary judge is pinned to one serving provider, so a difference between
# conditions cannot come from the router sending them to different hosts of the same
# model. Value: (OpenRouter provider slug, provider name as reported in responses).
PINS = {"anthropic/claude-sonnet-5": ("claude-on-aws", "Claude Platform on AWS"),
        "openai/gpt-5.4": ("openai", "OpenAI"),
        "anthropic/claude-opus-5": ("claude-on-aws", "Claude Platform on AWS")}

# -- the main programme (proposal §5, "Run plan and cost") ------------------------------


class Entry(NamedTuple):
    name: str               # what --arms selects
    arm: str                # the trial's arm, as the scorer groups it
    conditions: list[str]
    repeats: int
    judges: list[str]
    subset: bool            # True: only the first SUBSET_SIZE cases
    # set only by the optional sub-experiments (docs/decisions.md, 2026-10-26)
    cases: tuple = ()       # only these cases, overriding subset
    length: str = ""        # "short" or "long"; empty: long only for the arm "long"
    reasoning: dict | None = None   # sent to the judges instead of judge --reasoning
    by_number: bool = False         # the judges answer with option numbers


SUBSET_SIZE = 10            # the length arm and the wording ladder share these cases
PROGRAMME = [
    # agreement-block comparisons are belief movements: 6 repeats
    Entry("agreement", "short", AGREEMENT_BLOCK, 6, PRIMARY_JUDGES, False),
    # 12: every (truth position, wrong-claim offset) pairing once
    Entry("conflict", "short", CONFLICT_BLOCK, 12, PRIMARY_JUDGES, False),
    # 4: every truth position once; A7 is each judge's own no-conflict baseline
    Entry("abstain", "abstain", ABSTAIN_ARM, 4, PRIMARY_JUDGES, False),
    # added after the pilot: P0 offered the abstain option, a check beside A7 -- does the
    # judge abstain where one irrelevant report cannot settle the answer?
    Entry("abstain-p0", "abstain", ["P0"], 4, PRIMARY_JUDGES, False),
    Entry("screen", "screen", list(SCREEN_LEVELS), 4, PRIMARY_JUDGES, False),
    # the length arm crosses the conflict block (H3, H4) and A1, A2 (H2)
    Entry("long-conflict", "long", CONFLICT_BLOCK, 12, LENGTH_JUDGES, True),
    Entry("long-agreement", "long", LONG_AGREEMENT, 6, LENGTH_JUDGES, True),
    Entry("ladder", "ladder", LADDER, 12, PRIMARY_JUDGES, True),
]

# -- the optional sub-experiments (proposal §6; docs/decisions.md, 2026-10-26) ---------
# Selected by name with judge --arms, never part of the default run or of plan's totals.
# Each fixes its cases and its arm label, so no trial shares an id or a scorer cell with
# the main programme's.

SONNET = "anthropic/claude-sonnet-5"
THINKING = {"max_tokens": 2000}     # reasoning on, at a budget of 2,000 thinking tokens
REASONING_CASES = ("M1", "M2")      # the first two cases: one T2, one T1
REASONING_CONDITIONS = ["X1", "X3", "X5"]
OFF = OpenRouterBackend.REASONING_OFF
OPTIONAL = [
    # one model in both modes, crossed with length; both modes run on the same day
    Entry("reasoning-off-short", "reasoning-off-short", REASONING_CONDITIONS, 12, [SONNET],
          False, REASONING_CASES, "short", OFF),
    Entry("reasoning-off-long", "reasoning-off-long", REASONING_CONDITIONS, 12, [SONNET],
          False, REASONING_CASES, "long", OFF),
    Entry("reasoning-on-short", "reasoning-on-short", REASONING_CONDITIONS, 12, [SONNET],
          False, REASONING_CASES, "short", THINKING),
    Entry("reasoning-on-long", "reasoning-on-long", REASONING_CONDITIONS, 12, [SONNET],
          False, REASONING_CASES, "long", THINKING),
    # stated against token probabilities: the screen on the first 15 cases
    Entry("cross-check", "cross-check", list(SCREEN_LEVELS), 4, AUXILIARY, False,
          ("M1", "M2", "M3", "M4", "M5", "M6", "M14", "M22", "M30", "M38",
           "M7", "M8", "M9", "M10", "M11"), by_number=True),
    # n_eff at long length, A0 coming from the short arm; the subset but M38, whose A7
    # cannot be built long (one of its reports is one word short)
    Entry("long-neff", "long", ["A4", "A6", "A7"], 6, [SONNET], False,
          ("M1", "M2", "M3", "M4", "M5", "M6", "M14", "M22", "M30")),
]

# $ per call (proposal §5): measured on the sample case, except the long-report rate,
# which is estimated
RATE_GENERATION = 0.00025
RATE_SHORT = 0.00178        # blended over the three primary judges
RATE_LONG = 0.0030          # the Sonnet and GPT-5.4 pair
RATE_OPTIONAL = 0.0025      # assumed for the optional sub-experiments (§6)
GENERATION_CALLS = (12, 30)  # per source: round 1 suffices, or both rounds run
SOURCES_PER_CASE = 4


def rate(entry: Entry) -> float:
    """An entry's $ per call, at the proposal's rates."""
    return (RATE_OPTIONAL if entry in OPTIONAL else
            RATE_LONG if entry.arm == "long" else RATE_SHORT)


def subset(cases: dict) -> list[str]:
    """The cases the length arm and wording ladder run on: the first SUBSET_SIZE in
    corpus order. Which ten is not fixed by the proposal; see docs/decisions.md."""
    return list(cases)[:SUBSET_SIZE]


def build_entry(entry: Entry, cases: dict, frozen: dict, seed: int = 42):
    """[(run_index, trials)] for one programme entry. Within a repeat, every arm shows the
    same reports in the same order, so arms differ only by what they vary. Every trial
    carries the entry's arm label, and the conditions an entry judges long are
    length-checked."""
    ids = list(entry.cases) or (subset(cases) if entry.subset else list(cases))
    length = entry.length or ("long" if entry.arm == "long" else "short")
    checked = LONG_ARM + [c for c in entry.conditions if c not in LONG_ARM]
    out = []
    for r in range(1, entry.repeats + 1):
        if set(entry.conditions) <= set(SCREEN_LEVELS):
            s = rotation_schedule(r)
            trials = [t for cid in ids
                      for t in build_screen(cid, cases[cid], frozen[cid], s["option_rotation"],
                                            s["wrong_offset"],
                                            allow_abstain=entry.arm == "abstain")]
        else:
            trials = [t for cid in ids
                      for t in build_repeat(cid, cases[cid], frozen[cid], r, seed,
                                            length=length, allow_abstain=entry.arm == "abstain",
                                            checked=checked)]
        out.append((r, [dict(t, arm=entry.arm, **({"by_number": True} if entry.by_number else {}))
                        for t in trials if t["condition"] in entry.conditions]))
    return out


def plan(n_cases: int, entries: list[Entry] = PROGRAMME) -> list[tuple[str, int, float]]:
    """(row, calls, cost) for generating reports for n_cases cases and running `entries`
    on them, at the proposal's per-call rates. Generation is costed at one round; the
    worst case is printed separately."""
    n_sub = min(n_cases, SUBSET_SIZE)
    gen = n_cases * SOURCES_PER_CASE * GENERATION_CALLS[0]
    rows = [("generate and accept reports", gen, gen * RATE_GENERATION)]
    for e in entries:
        n = len(e.cases) if e.cases else n_sub if e.subset else n_cases
        calls = len(e.conditions) * e.repeats * len(e.judges) * n
        rows.append((e.name, calls, calls * rate(e)))
    return rows


def print_plan(n_cases: int) -> None:
    rows = plan(n_cases)
    print(f"Pre-flight estimate for {n_cases} case(s); length arm and ladder on "
          f"{min(n_cases, SUBSET_SIZE)}. No calls are made.\n")
    print(f"  {'':30s} {'calls':>7s} {'cost':>9s}")
    for name, calls, cost in rows:
        print(f"  {name:30s} {calls:7d} {f'${cost:.2f}':>9s}")
    calls, cost = sum(r[1] for r in rows), sum(r[2] for r in rows)
    print(f"  {'main programme':30s} {calls:7d} {f'${cost:.2f}':>9s}")
    extra = n_cases * SOURCES_PER_CASE * (GENERATION_CALLS[1] - GENERATION_CALLS[0])
    print(f"\n  If every source needs a second round: +{extra} calls, "
          f"+${extra * RATE_GENERATION:.2f}.")


# -- guards shared by the real steps ----------------------------------------------------


class CallCeiling(RuntimeError):
    pass


class Stop(Exception):
    """A stop condition fired during judging."""


class Budget:
    """One call ceiling shared by every backend in a run."""

    def __init__(self, ceiling: float):
        self.ceiling, self.used = ceiling, 0


class Capped:
    """Wraps a backend and counts its calls against a shared Budget. The call that would
    exceed the ceiling is refused, never made. A failed judge call is a failed trial,
    logged with its error, not a crash."""

    def __init__(self, inner, role: str, budget: Budget, log: list | None = None):
        self.inner, self.role, self.budget, self.log = inner, role, budget, log
        self.name = inner.name
        self.last_error = None

    def __getattr__(self, attr):      # last_provider, last_usage, ... of the inner backend
        return getattr(self.inner, attr)

    def complete(self, system, user, temperature=0.9, max_tokens=300):
        if self.budget.used >= self.budget.ceiling:
            raise CallCeiling(f"call ceiling {self.budget.ceiling} reached; refused call "
                              f"{self.budget.used + 1} ({self.role})")
        self.budget.used += 1
        self.last_error = None
        try:
            out = self.inner.complete(system, user, temperature=temperature,
                                      max_tokens=max_tokens)
        except RuntimeError as e:
            if self.role != "judge":
                raise
            self.last_error, out = str(e)[:500], ""
        if self.log is not None:
            self.log.append({"n": self.budget.used, "role": self.role, "model": self.name,
                             "provider": getattr(self.inner, "last_provider", None),
                             "output": out})
        return out


def refuse_existing(*paths: str) -> None:
    """Fail before spending, not after: real outputs are never overwritten."""
    for p in paths:
        if os.path.exists(p):
            raise SystemExit(f"{p} exists; move it aside first -- real outputs are not overwritten")


def write_json(path: str, obj) -> None:
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


# -- the steps --------------------------------------------------------------------------


def generate(cases: dict, reporter, rater, out_dir: str, budget: Budget | None = None) -> dict:
    """Generate, accept and freeze every source's reports, case by case in R18 order.
    The first source still short after two rounds stops the run (proposal §3); nothing is
    loosened or hand-edited. Writes frozen_reports.json, generation_report.json and, if
    the backends logged their calls, generation_calls.jsonl. Returns the frozen set."""
    frozen = {}
    report = {"reporter": reporter.name, "rater": rater.name, "sources": {}, "stopped": None}
    try:
        for case_id, key, res in freeze_sources(cases, reporter, rater):
            frozen.setdefault(case_id, {})[key] = res
            status = "OK" if res["sufficient"] else "SHORT"
            needed = cases[case_id]["sources"][key]["n_paraphrases_needed"]
            report["sources"][f"{case_id}/{key}"] = {
                "status": status, "needed": needed, "generated": len(res["all_scored"]),
                "accepted": len(res["accepted"]), "rounds": res["rounds_needed"],
                "calls": res["calls"],
                "candidates": [{k: s[k] for k in ("text", "semantic", "copy_overlap", "rubric",
                                                  "accepted", "rejected_because")}
                               for s in res["all_scored"]]}
            print(f"  [{case_id}/{key}] {status}: {len(res['accepted'])}/{needed} accepted "
                  f"of {len(res['all_scored'])} in {res['rounds_needed']} round(s), "
                  f"{res['calls']} calls")
            if status == "SHORT":
                report["stopped"] = f"{case_id}/{key} SHORT"
                break
    except CallCeiling as e:
        report["stopped"] = str(e)
    # the budget also counts calls of a source the ceiling cut short
    report["calls"] = budget.used if budget else sum(s["calls"] for s in report["sources"].values())
    padded = sorted({cid for cid, fc in frozen.items()
                     for res in fc.values() if res.get("padded")})
    if padded:
        print(f"Long-report length not checked for {', '.join(padded)}: the mock has no "
              f"hand-written rewordings of these sentences, so the lint's R20 warning is "
              f"the check.")
    write_json(os.path.join(out_dir, "frozen_reports.json"), frozen)
    write_json(os.path.join(out_dir, "generation_report.json"), report)
    calls_log = getattr(reporter, "log", None)
    if calls_log is not None:
        with open(os.path.join(out_dir, "generation_calls.jsonl"), "w") as f:
            f.writelines(json.dumps(row) + "\n" for row in calls_log)
    print(f"{report['calls']} calls. Stopped: {report['stopped']}")
    return frozen


def check_frozen(cases: dict, frozen: dict) -> list[str]:
    """The leak check over the frozen reports that must pass before any judging
    (proposal §3): every source frozen in full, and no accepted report containing a
    word of its source's type description or an invented attribution."""
    problems = []
    for case_id, case in cases.items():
        for key, src in case["sources"].items():
            res = (frozen.get(case_id) or {}).get(key)
            if not res or len(res["accepted"]) < src["n_paraphrases_needed"]:
                problems.append(f"{case_id}/{key}: not frozen in full")
                continue
            terms = leak_terms(src, case["question"])
            for rep in res["accepted"]:
                leak = leaks_in(rep["text"], terms) + attribution_in(rep["text"])
                if leak:
                    problems.append(f"{case_id}/{key}: leak {leak} in {rep['text']!r}")
    return problems


def judge_all(cases: dict, frozen: dict, entries: list[Entry], make_backend, log_path: str,
              budget: Budget, seed: int = 42, pins: dict | None = None) -> list[dict]:
    """Judge every trial of `entries` with each entry's judges, interleaved trial by
    trial so the early parse check covers every judge, writing each record as it arrives.

    Stop conditions (proposal §3): the call ceiling; a call that fails; a pinned judge
    served by any other provider (a visible failure beats a silent substitution); more
    than one parse failure in the first 50 trials."""
    names = sorted({m for e in entries for m in e.judges})
    backends = {m: Capped(make_backend(m), "judge", budget) for m in names}
    records, n_fail, stopped = [], 0, None
    with open(log_path, "x") as log:
        try:
            for entry in entries:
                for r, trials in build_entry(entry, cases, frozen, seed):
                    for t in trials:
                        for m in entry.judges:
                            b = backends[m]
                            rec = run_trials([t], b, run_index=r)[0]
                            rec["call_error"] = b.last_error
                            log.write(json.dumps(rec) + "\n")
                            log.flush()
                            records.append(rec)
                            n_fail += rec["parsing_status"] in PARSE_FAILURES
                            err = rec["call_error"] or ""
                            if err and "returned no content" not in err:
                                raise Stop(f"{m} call failed on {rec['trial_id']}: {err[:200]}")
                            want = (pins or {}).get(m)
                            if want and not err and rec["serving_provider"] != want[1]:
                                raise Stop(f"{m} served by {rec['serving_provider']!r}, "
                                           f"pinned to {want[1]!r}, on {rec['trial_id']}")
                            if len(records) == 50 and n_fail > 1:   # > ~2% of the first 50
                                raise Stop(f"{n_fail}/50 parse failures in the first 50")
        except (Stop, CallCeiling) as e:
            stopped = str(e)
    print(f"{len(records)} trials logged -> {log_path}; {n_fail} parse failures; "
          f"stopped: {stopped}")
    return records


def planned_calls(entries: list[Entry], cases: dict, frozen: dict,
                  seed: int = 42) -> list[tuple[Entry, int]]:
    """(entry, judge calls) as actually built, for the pre-spend check."""
    return [(e, sum(len(trials) for _, trials in build_entry(e, cases, frozen, seed)) * len(e.judges))
            for e in entries]


def select_entries(arms: str | None) -> list[Entry]:
    """The main programme, or the entries named, the optional sub-experiments included."""
    if not arms:
        return PROGRAMME
    names = arms.split(",")
    known = PROGRAMME + OPTIONAL
    unknown = set(names) - {e.name for e in known}
    if unknown:
        raise SystemExit(f"unknown arm(s) {sorted(unknown)}; choose from "
                         f"{[e.name for e in known]}")
    return [e for e in known if e.name in names]


def only_cases(cases: dict, ids: str | None) -> dict:
    """The corpus, or only the cases --cases names (M1,M2), in corpus order."""
    if not ids:
        return cases
    names = ids.split(",")
    unknown = sorted(set(names) - set(cases))
    if unknown:
        raise SystemExit(f"unknown case(s) {unknown}")
    return {cid: case for cid, case in cases.items() if cid in names}


# -- commands ---------------------------------------------------------------------------


def cmd_dry(args, cases):
    """Everything the real run does, on the mock backend: generate and freeze, the leak
    check, every programme entry with each entry's judges, the log, the scorer. Long
    reports of a case the mock has no hand-written rewordings for are not length-checked
    (MockBackend.pads)."""
    out = args.out or os.path.join("runs", "mock")
    os.makedirs(out, exist_ok=True)
    log_path = os.path.join(out, "trials.jsonl")
    if os.path.exists(log_path):
        os.remove(log_path)                      # mock output is scratch
    print(f"== generate and freeze (mock) -> {out} ==")
    frozen = generate(cases, MockBackend(), MockBackend(), out)
    problems = check_frozen(cases, frozen)
    if problems:
        raise SystemExit("frozen set incomplete or leaking: " + "; ".join(problems))
    entries = select_entries(args.arms)
    n = sum(c for _, c in planned_calls(entries, cases, frozen, args.seed))
    print(f"\n== judge (mock): {n} calls ==")

    def named_mock(model):
        b = MockBackend()
        b.name = f"mock:{model}"
        return b
    judge_all(cases, frozen, entries, named_mock, log_path, Budget(math.inf), args.seed)
    print("\n== score ==\n")
    score.main(log_path)


def cmd_plan(args, cases):
    print_plan(args.cases or len(cases))


def cmd_balance(args, cases):
    print(json.dumps(key_status(), indent=2))


def cmd_probe(args, cases):
    """One trivial call per model, recording whether it resolves, which provider served
    it, and whether token logprobs came back. Model ids rotate: run this before spending.
    OpenRouter drops unsupported parameters silently, so a null is an answer."""
    path = os.path.join(args.out or "runs", "probe.json")
    refuse_existing(path)
    results = []
    for model in PRIMARY_JUDGES + AUXILIARY + [REPORTER]:
        aux = model in AUXILIARY
        b = OpenRouterBackend(model=model, top_logprobs=5,
                              reasoning=AUXILIARY_REASONING[model] if aux
                              else OpenRouterBackend.REASONING_OFF,
                              provider=AUXILIARY_ROUTING if aux else
                              ({"order": [PINS[model][0]], "allow_fallbacks": False}
                               if model in PINS else None))
        res = {"model": model, "role": "auxiliary" if aux else
               "primary" if model in PRIMARY_JUDGES else "reporter"}
        try:
            res["content"] = b.complete("", "Reply with only the digit: what is 2 + 2?",
                                        temperature=0, max_tokens=16)
        except RuntimeError as e:      # e.g. 404 when no endpoint honours the parameters
            res["error"] = str(e)
        top = (b.last_logprobs or [{}])[0].get("top_logprobs")
        res.update(provider=b.last_provider, generation_id=b.last_generation_id,
                   logprobs_returned=b.logprobs_available,
                   n_alternatives=len(top) if top else 0)
        results.append(res)
        print(json.dumps({k: res.get(k) for k in ("model", "provider", "logprobs_returned",
                                                  "n_alternatives", "error")}))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_json(path, results)


def cmd_generate(args, cases):
    cases = only_cases(cases, args.cases)
    out = args.out or "runs"
    os.makedirs(out, exist_ok=True)
    refuse_existing(*(os.path.join(out, f) for f in
                      ("frozen_reports.json", "generation_report.json", "generation_calls.jsonl")))
    budget, log = Budget(args.max_calls), []
    reporter = Capped(OpenRouterBackend(model=REPORTER), "reporter", budget, log)
    rater = Capped(OpenRouterBackend(model=RATER), "rater", budget, log)
    worst = sum(GENERATION_CALLS[1] for c in cases.values() for _ in c["sources"])
    print(f"Generating for {len(cases)} case(s): at most {worst} calls, about "
          f"${worst * RATE_GENERATION:.2f}; ceiling {args.max_calls}")
    generate(cases, reporter, rater, out, budget)


def cmd_judge(args, cases):
    cases = only_cases(cases, args.cases)
    out = args.out or "runs"
    log_path = os.path.join(out, args.log)
    refuse_existing(log_path)
    with open(os.path.join(out, "frozen_reports.json")) as f:
        frozen = json.load(f)
    problems = check_frozen(cases, frozen)
    if problems:
        raise SystemExit("leak check failed, no judging:\n  " + "\n  ".join(problems))
    entries = select_entries(args.arms)
    missing = sorted({c for e in entries for c in e.cases} - set(cases))
    if missing:
        raise SystemExit(f"the entries need cases --cases left out: {missing}")
    if len({json.dumps(e.reasoning) for e in entries}) > 1:
        raise SystemExit("these entries send different reasoning settings; judge each "
                         "setting in a run of its own")
    planned = planned_calls(entries, cases, frozen, args.seed)
    n = sum(c for _, c in planned)
    cost = sum(c * rate(e) for e, c in planned)
    print(f"planned: {n} calls, about ${cost:.2f}: " + ", ".join(f"{e.name} {c}" for e, c in planned))
    if n > args.max_calls:
        raise SystemExit(f"stop before spending: {n} planned calls > ceiling {args.max_calls}")
    reasoning = (entries[0].reasoning if entries[0].reasoning is not None
                 else None if args.reasoning == "omit" else json.loads(args.reasoning))
    print(f"reasoning parameter sent to every judge: {reasoning!r}")
    aux = sorted({m for e in entries for m in e.judges} & set(AUXILIARY))
    if aux:
        print(f"except the auxiliary models, each sent its own: "
              f"{ {m: AUXILIARY_REASONING[m] for m in aux} }")
    print(f"provider pins: { {m: p[0] for m, p in PINS.items()} }")

    def make(model):
        if model in AUXILIARY:
            return OpenRouterBackend(model=model, reasoning=AUXILIARY_REASONING[model],
                                     provider=AUXILIARY_ROUTING, top_logprobs=5,
                                     track_usage=True)
        pin = {"order": [PINS[model][0]], "allow_fallbacks": False} if model in PINS else None
        # a judge that thinks before it answers needs longer than the usual 30 seconds
        timeout = 150 if (reasoning or {}).get("max_tokens") else 30
        return OpenRouterBackend(model=model, reasoning=reasoning, provider=pin,
                                 track_usage=True, timeout=timeout)
    judge_all(cases, frozen, entries, make, log_path, Budget(args.max_calls), args.seed, PINS)
    score.main(log_path)


def main(argv=None):
    from cases import CASES
    ap = argparse.ArgumentParser(prog="python -m pipeline.run", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, helptext in [("dry", "the whole programme on the mock backend, no spend"),
                           ("plan", "pre-flight call and cost estimate, no spend"),
                           ("balance", "the API key's limit and usage, no spend"),
                           ("probe", "one call per model: resolves? provider? logprobs?"),
                           ("generate", "generate, accept and freeze reports (spends)"),
                           ("judge", "judge the frozen reports (spends)")]:
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--out", help="output directory (default runs/, or runs/mock/ for dry)")
        p.add_argument("--seed", type=int, default=42)
        if name in ("dry", "judge"):
            p.add_argument("--arms", help="comma-separated programme entries: "
                           + ",".join(e.name for e in PROGRAMME) + " (default: all); or "
                           "optional ones: " + ",".join(e.name for e in OPTIONAL))
        if name in ("generate", "judge"):
            p.add_argument("--max-calls", type=int, required=True, help="hard call ceiling")
            p.add_argument("--cases", help="comma-separated case ids: only these cases, "
                           "e.g. M1,M2 for the wording-robustness rerun")
        if name == "plan":
            p.add_argument("--cases", type=int, help="cost a corpus of this size instead")
        if name == "judge":
            p.add_argument("--log", default="trials.jsonl",
                           help="log file name inside --out; a new name per staged run")
            p.add_argument("--reasoning", default='{"enabled": false}',
                           help="'omit', or the JSON sent as the reasoning parameter")
    args = ap.parse_args(argv)
    {"dry": cmd_dry, "plan": cmd_plan, "balance": cmd_balance, "probe": cmd_probe,
     "generate": cmd_generate, "judge": cmd_judge}[args.cmd](args, CASES)


if __name__ == "__main__":
    main()
