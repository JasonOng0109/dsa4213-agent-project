"""
LLM backends.

- OpenRouterBackend: real calls through OpenRouter's OpenAI-compatible endpoint. All
  model access in this study goes through OpenRouter (proposal §3).
- MockBackend: deterministic canned responses, for dry runs and tests with no API key
  and no spend.

Every backend has one method, complete(system, user, temperature, max_tokens) -> str,
so nothing else in the pipeline needs to know which one is in use.
"""

from __future__ import annotations
import hashlib
import json
import os
import re
import threading
import time

import requests

OPENROUTER = "https://openrouter.ai/api/v1"


class _SharedRateLimiter:
    """OpenRouter's request-rate cap is per ACCOUNT, not per model: two backends with
    different models still share one key and one bucket. This limiter is a module-level
    singleton, so every OpenRouterBackend in a process throttles against the same window."""

    def __init__(self, max_per_minute: int = 18, window_seconds: float = 60.0):
        # 18, not the documented 20, to leave a small safety margin
        self.max_per_minute = max_per_minute
        self.window_seconds = window_seconds
        self._calls: list[float] = []
        self._lock = threading.Lock()

    def wait(self) -> None:
        sleep_for = 0.0
        with self._lock:
            now = time.time()
            self._calls = [t for t in self._calls if now - t < self.window_seconds]
            if len(self._calls) >= self.max_per_minute:
                sleep_for = self.window_seconds - (now - self._calls[0]) + 0.1
        if sleep_for > 0:
            time.sleep(sleep_for)
        with self._lock:
            self._calls.append(time.time())


_SHARED_OPENROUTER_LIMITER = _SharedRateLimiter()


class OpenRouterBackend:
    """Real calls via OpenRouter. Needs OPENROUTER_API_KEY (or api_key=...).

    Throttles client-side against the shared per-minute cap and retries with backoff on
    429 and 5xx; any other error fails loudly. After each call, last_provider,
    last_generation_id, last_logprobs and last_usage describe it."""

    REASONING_OFF = {"enabled": False}

    def __init__(self, model: str, api_key: str | None = None, max_retries: int = 5,
                 reasoning: dict | None = REASONING_OFF,
                 provider: dict | None = None, top_logprobs: int | None = None,
                 track_usage: bool = False):
        """reasoning=None omits the field entirely: some logprob endpoints are unroutable
        when it is sent. provider is passed through, e.g. {"require_parameters": True} to
        route only to endpoints honouring every parameter, or an order with fallbacks off
        to pin a judge to one serving stack. top_logprobs requests token logprobs.
        track_usage asks for per-call token counts and cost (last_usage)."""
        self.name = f"openrouter:{model}"
        self.model = model
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("No API key found. Set OPENROUTER_API_KEY or pass api_key=...")
        self.max_retries = max_retries
        self.reasoning, self.provider, self.top_logprobs = reasoning, provider, top_logprobs
        self.track_usage = track_usage
        self.last_provider = self.last_generation_id = self.last_logprobs = None
        self.last_usage = None
        self.logprobs_available = False

    def complete(self, system: str, user: str, temperature: float = 0.9,
                 max_tokens: int = 300) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        # Reasoning models can spend the whole token budget on hidden thinking and
        # return no content, and a judge that reasons unasked is a different
        # instrument. Reasoning is therefore off unless told otherwise.
        if self.reasoning is not None:
            payload["reasoning"] = self.reasoning
        if self.provider is not None:
            payload["provider"] = self.provider
        if self.top_logprobs is not None:
            payload.update(logprobs=True, top_logprobs=self.top_logprobs)
        if self.track_usage:
            payload["usage"] = {"include": True}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "DSA4213 counting reports or counting evidence",
        }

        # so a failed call never leaves the previous call's details behind
        self.last_provider = self.last_generation_id = self.last_logprobs = None
        self.last_usage = None
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            _SHARED_OPENROUTER_LIMITER.wait()
            try:
                resp = requests.post(f"{OPENROUTER}/chat/completions", headers=headers,
                                     json=payload, timeout=30)
            except requests.RequestException as e:
                last_error = e
                time.sleep(2 ** attempt)
                continue

            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", 2 ** attempt))
                last_error = RuntimeError(f"429 rate limited: {resp.text[:200]}")
                time.sleep(retry_after)
                continue
            if resp.status_code >= 500:
                last_error = RuntimeError(f"{resp.status_code}: {resp.text[:200]}")
                time.sleep(2 ** attempt)
                continue
            if resp.status_code != 200:
                # not retryable (bad request, auth error, ...) -- fail loud
                raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text[:300]}")

            data = resp.json()
            self.last_provider = data.get("provider")
            self.last_generation_id = data.get("id")
            self.last_usage = data.get("usage")
            try:
                lp = data["choices"][0].get("logprobs")
                self.last_logprobs = lp.get("content") if lp else None
                self.logprobs_available = bool(self.last_logprobs)
                content = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                raise RuntimeError(f"Unexpected OpenRouter response shape: {data}") from e
            if content is None:
                raise RuntimeError(
                    f"{self.model} returned no content (finish_reason="
                    f"{data['choices'][0].get('finish_reason')}); the model "
                    f"likely spent max_tokens={max_tokens} on reasoning."
                )
            return content.strip()

        raise RuntimeError(f"Gave up after {self.max_retries} attempts. Last error: {last_error}")


def key_status(api_key: str | None = None) -> dict:
    """The key's spending limit, usage and remaining balance. Costs nothing."""
    key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("No API key found. Set OPENROUTER_API_KEY or pass api_key=...")
    resp = requests.get(f"{OPENROUTER}/key", headers={"Authorization": f"Bearer {key}"},
                        timeout=30)
    return resp.json()


class MockBackend:
    """Deterministic stand-in for dry runs. Not a model: it exists so every stage of the
    pipeline has realistic-shaped input to consume.

    - Reporter calls return hand-written paraphrases from a lookup table keyed by the
      start of each source's content, cycling through the variants. A source not in the
      table gets its content back inside rotating lead-ins, which is enough to clear the
      overlap filters.
    - Rater calls pass every rubric flag, with a deterministic score of 80-97.
    - Judge calls pick the option named most often in the reports, with confidence
      rising with report count; offered the abstain option alongside a dependence note,
      it abstains, so that path is exercised too."""

    name = "mock"

    # keyed by a prefix of each source's `content`. Each is 12-15 words, so every long
    # report lands inside 88-96 words around M1's 76-78-word filler sets.
    _PARAPHRASE_TABLE: dict[str, list[str]] = {
        "The ME2103 lab logbook counts for 25%": [
            "A quarter of your final ME2103 module grade comes from the lab logbook.",
            "Your lab logbook in ME2103 makes up 25% of your final module grade.",
            "Of your final module grade in ME2103, the lab logbook accounts for 25%.",
        ],
        "The ME2103 lab logbook carries 15%": [
            "In ME2103, the lab logbook makes up 15% of the final module grade.",
            "Of the final ME2103 module grade, 15% is assigned to the lab logbook.",
            "The final ME2103 module grade takes 15% from the lab logbook component.",
        ],
        "Of the ME2103 marks available": [
            "Fifteen per cent of all ME2103 marks are awarded for work in the lab logbook.",
        ],
        "The lab logbook contributes 15% towards": [
            "Towards a student's overall ME2103 result, the lab logbook contributes a 15% share.",
        ],
    }

    # screen level P1: the options each screen_partial leaves open
    _SCREEN_TABLE: dict[str, list[str]] = {
        "The ME2103 lab logbook is worth less than a fifth": ["15%", "10%"],
    }

    def __init__(self):
        self._call_counters: dict[str, int] = {}

    def complete(self, system: str, user: str, temperature: float = 0.9,
                 max_tokens: int = 300) -> str:
        if user.startswith("RUBRIC CHECK."):
            # table paraphrases are faithful, so every flag holds
            return ('{"all_details": true, "nothing_added": true, "values_unchanged": true, '
                    f'"scope_kept": true, "score": {self._mock_score(user)}}}')
        if "Possible answers:\n" in user:
            return self._mock_judge(user)
        return self._mock_reporter(user)

    # -- internals -----------------------------------------------------

    def _mock_score(self, user: str) -> int:
        # deterministic jitter, always clearing the 0.80 acceptance threshold
        return 80 + int(hashlib.sha256(user.encode()).hexdigest()[:2], 16) % 18

    def _mock_reporter(self, user: str) -> str:
        m = re.search(r"What it says:\n(.*?)\n\nQuestion:", user, re.S)
        source_text = m.group(1).strip() if m else ""
        for key, variants in self._PARAPHRASE_TABLE.items():
            if source_text.startswith(key):
                idx = self._call_counters.get(key, 0)
                self._call_counters[key] = idx + 1
                return variants[idx % len(variants)]
        # Not in the table: relay the content with rotated clauses and a distinct lead-in
        # and tail per variant. A mock cannot truly reword, so this is how it gets under
        # the pairwise bigram-overlap threshold.
        content = source_text.strip().strip("'").rstrip(".")
        segs = [x.strip() for x in re.split(r"\s[—-]\s|;\s|\.\s", content) if x.strip()]
        idx = self._call_counters.get(source_text, 0)
        self._call_counters[source_text] = idx + 1
        k = idx % max(1, len(segs))
        body = " and ".join(segs[k:] + segs[:k])
        frames = [
            "{c}, which is the whole of what I was able to establish on this point.",
            "As I understand it, {c}; that is what the information available to me indicates.",
            "What I found is that {c}, and nothing I saw suggested otherwise.",
            "In short, {c} -- this was consistent everywhere I looked into it.",
            "It turns out {c}, at least as far as I could determine from what I had.",
        ]
        return frames[idx % len(frames)].format(c=body)

    def _mock_judge(self, user: str) -> str:
        # Majority by count over the numbered options, counted in the reports only.
        opts = re.findall(r"^  \d+\. (.+)$", user, re.M)
        body = user.split("Respond with ONLY")[0].split(f"  {len(opts)}. {opts[-1]}\n")[-1]
        counts = {o: len(re.findall(rf"(?<![\w.]){re.escape(o)}(?!\w)", body)) for o in opts}
        if not any(counts.values()):
            # nothing named (A0, screen P0/P1): spread p evenly over the options still
            # open -- all of them, or the survivors of a known screen statement
            keep = next((v for k, v in self._SCREEN_TABLE.items() if k in body), opts)
            open_opts = [o for o in opts if o in keep]
            p = {o: (100 // len(open_opts) if o in open_opts else 0) for o in opts}
            p[open_opts[0]] += 100 - sum(p.values())
            return json.dumps({"answer": open_opts[0], "p": p})
        winner = max(opts, key=lambda o: counts[o])
        n_reports = body.count(" says:")
        conf = min(95, 40 + n_reports * 15)
        rest = 100 - conf
        p = {o: (conf if o == winner else rest // (len(opts) - 1)) for o in opts}
        p[winner] += 100 - sum(p.values())
        answer = winner
        offered = re.search(r'answer exactly "([^"]+)"', user)   # the abstain option
        if offered and "same underlying source" in user:
            answer = offered.group(1)
        return json.dumps({"answer": answer, "p": p})
