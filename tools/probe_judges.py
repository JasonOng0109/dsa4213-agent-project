"""
A one-off probe, run on 2026-10-26 before the optional sub-experiments were built. It
asks four questions and writes the answers to runs/main/probe-2026-10-26.json:

1. Which parameters each model's endpoints take, from OpenRouter's endpoint list. No
   spend. OpenRouter drops a parameter an endpoint does not take, silently.
2. Does "temperature 0" make a primary judge repeat itself? One A0 prompt (M1, repeat 1),
   sent six times to each judge exactly as the main run sends it.
3. With reasoning on, does Claude Sonnet 5 return its thinking text, and how many tokens
   does it spend? M1's X3 at repeat 1, short twice and long once, at a 2,000-token budget.
4. Does the auxiliary Qwen answer with reasoning off and token probabilities on?

Spends about $0.10.

    uv run --env-file .env python -m tools.probe_judges
"""

import json
import os
import time

import requests

from cases import CASES
from pipeline.conditions import build_repeat
from pipeline.judge import JUDGE_SYSTEM, MAX_TOKENS
from pipeline.llm import OPENROUTER
from pipeline.prompt import render
from pipeline.run import AUXILIARY, AUXILIARY_ROUTING, PINS, PRIMARY_JUDGES, REPORTER

OUT = "runs/main/probe-2026-10-26.json"
REPEATS = 6
THINKING = {"max_tokens": 2000}
PACE = 3.5                  # seconds between calls: under the runner's 18 a minute


def endpoints(model: str) -> list[dict]:
    resp = requests.get(f"{OPENROUTER}/models/{model}/endpoints", timeout=30)
    return [{"provider": e.get("provider_name"), "tag": e.get("tag"),
             "supported_parameters": sorted(e.get("supported_parameters") or [])}
            for e in resp.json()["data"]["endpoints"]]


def call(purpose: str, payload: dict) -> dict:
    """One chat completion, keeping what the runner's backend throws away: the thinking
    text and its details, the finish reason and the time taken."""
    time.sleep(PACE)
    start = time.time()
    resp = requests.post(f"{OPENROUTER}/chat/completions", json=payload, timeout=300,
                         headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                                  "X-Title": "DSA4213 counting reports or counting evidence"})
    out = {"purpose": purpose, "model": payload["model"], "status": resp.status_code,
           "seconds": round(time.time() - start, 1),
           "sent": {k: v for k, v in payload.items() if k != "messages"}}
    data = resp.json()
    if resp.status_code != 200 or "choices" not in data:
        return dict(out, error=str(data)[:500])
    choice = data["choices"][0]
    msg = choice.get("message") or {}
    details = [{k: (v if k != "data" else f"<{len(v)} characters>") for k, v in d.items()}
               for d in msg.get("reasoning_details") or []]
    top = ((choice.get("logprobs") or {}).get("content") or [{}])[0].get("top_logprobs")
    return dict(out, provider=data.get("provider"), finish_reason=choice.get("finish_reason"),
                content=msg.get("content"), reasoning=msg.get("reasoning"),
                reasoning_details=details, usage=data.get("usage"),
                logprob_alternatives=len(top) if top else 0)


def judge_payload(model: str, prompt: str, reasoning: dict, max_tokens: int) -> dict:
    """What the runner sends a primary judge (pipeline/llm.py), pinned as in the main run."""
    return {"model": model, "temperature": 0.0, "max_tokens": max_tokens, "reasoning": reasoning,
            "messages": [{"role": "system", "content": JUDGE_SYSTEM},
                         {"role": "user", "content": prompt}],
            "provider": {"order": [PINS[model][0]], "allow_fallbacks": False},
            "usage": {"include": True}}


def main() -> None:
    if os.path.exists(OUT):
        raise SystemExit(f"{OUT} exists; move it aside first")
    frozen = json.load(open("runs/main/frozen_reports.json"))
    short = {t["condition"]: t for t in build_repeat("M1", CASES["M1"], frozen["M1"], 1)}
    long = {t["condition"]: t for t in build_repeat("M1", CASES["M1"], frozen["M1"], 1,
                                                   length="long")}
    result = {"endpoints": {m: endpoints(m) for m in PRIMARY_JUDGES + AUXILIARY + [REPORTER]},
              "prompts": {"A0 short": render(short["A0"]), "X3 short": render(short["X3"]),
                          "X3 long": render(long["X3"])},
              "calls": []}
    calls = result["calls"]
    for model in PRIMARY_JUDGES:
        for i in range(REPEATS):
            calls.append(call("temperature 0, A0 short", judge_payload(
                model, result["prompts"]["A0 short"], {"enabled": False}, MAX_TOKENS)))
            print(model, i + 1, calls[-1].get("content") or calls[-1].get("error"))
    sonnet = "anthropic/claude-sonnet-5"
    for name in ("X3 short", "X3 short", "X3 long"):
        calls.append(call(f"reasoning on, {name}", judge_payload(
            sonnet, result["prompts"][name], THINKING, THINKING["max_tokens"] + MAX_TOKENS)))
        c = calls[-1]
        print(name, c.get("finish_reason"), c.get("seconds"), "s, reasoning text:",
              len(c.get("reasoning") or ""), "characters, content:", c.get("content") or c.get("error"))
    digit = "Reply with only the digit: what is 2 + 2?"
    for model, reasoning, prompt in [(AUXILIARY[0], {"effort": "none"}, digit),
                                     (AUXILIARY[0], {"enabled": False}, digit),
                                     (AUXILIARY[0], None, digit + " /no_think"),
                                     (AUXILIARY[1], None, digit)]:
        payload = {"model": model, "temperature": 0, "max_tokens": 16, "logprobs": True,
                   "top_logprobs": 5, "provider": AUXILIARY_ROUTING,
                   "messages": [{"role": "user", "content": prompt}]}
        if reasoning is not None:
            payload["reasoning"] = reasoning
        calls.append(call(f"auxiliary, reasoning {reasoning}, prompt {prompt!r}", payload))
        c = calls[-1]
        print(model, reasoning, c.get("provider"), repr(c.get("content")), "alternatives",
              c.get("logprob_alternatives"), c.get("error") or "")
    with open(OUT, "w") as f:
        json.dump(result, f, indent=2)
    print(f"-> {OUT}; cost ${sum((c.get('usage') or {}).get('cost') or 0 for c in calls):.4f}")


if __name__ == "__main__":
    main()
