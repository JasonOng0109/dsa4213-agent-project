"""OpenRouterBackend's retry, backoff, routing and rate limiting, with requests.post
patched so no network is needed."""

import time
from unittest.mock import MagicMock, patch

from pipeline.llm import OpenRouterBackend, _SHARED_OPENROUTER_LIMITER

POST = "pipeline.llm.requests.post"


def _response(status_code, json_body=None, headers=None, text=""):
    r = MagicMock()
    r.status_code = status_code
    r.headers = headers or {}
    r.text = text
    r.json.return_value = json_body or {}
    return r


def _ok(content="ok", **extra):
    return _response(200, {"choices": [{"message": {"content": content}}], **extra})


def test_happy_path():
    backend = OpenRouterBackend(model="m", api_key="k")
    with patch(POST, return_value=_ok("Friday")) as m:
        assert backend.complete(system="sys", user="hello") == "Friday"
    assert m.call_count == 1


def test_retries_on_429_then_succeeds():
    backend = OpenRouterBackend(model="m", api_key="k", max_retries=3)
    limited = _response(429, headers={"Retry-After": "0.01"}, text="slow down")
    with patch(POST, side_effect=[limited, _ok()]) as m:
        assert backend.complete(system="sys", user="hello") == "ok"
    assert m.call_count == 2


def test_gives_up_after_max_retries():
    backend = OpenRouterBackend(model="m", api_key="k", max_retries=2)
    limited = _response(429, headers={"Retry-After": "0.01"})
    with patch(POST, return_value=limited) as m:
        try:
            backend.complete(system="sys", user="hello")
        except RuntimeError as e:
            assert "Gave up after 2 attempts" in str(e)
        else:
            raise AssertionError("should have raised")
    assert m.call_count == 2


def test_retries_an_error_in_a_200_body():
    """OpenRouter reports an error met while the model answers with status 200 and the
    error in the body, as GPT-5.4's provider did on 2026-10-27; it is retried like a 502."""
    backend = OpenRouterBackend(model="m", api_key="k", max_retries=3)
    overloaded = _response(200, {"id": "gen-1", "error": {
        "message": "Our servers are currently overloaded. Please try again later.",
        "code": 502, "metadata": {"error_type": "provider_unavailable"}}})
    with patch(POST, side_effect=[overloaded, _ok("Friday")]) as m, \
            patch("pipeline.llm.time.sleep"):
        assert backend.complete(system="sys", user="hello") == "Friday"
    assert m.call_count == 2


def test_non_retryable_error_fails_immediately():
    backend = OpenRouterBackend(model="m", api_key="k", max_retries=5)
    with patch(POST, return_value=_response(400, text="invalid model id")) as m:
        try:
            backend.complete(system="sys", user="hello")
        except RuntimeError as e:
            assert "400" in str(e)
        else:
            raise AssertionError("should have raised")
    assert m.call_count == 1, "a 400 should not be retried"


def test_malformed_response_shape():
    backend = OpenRouterBackend(model="m", api_key="k")
    with patch(POST, return_value=_response(200, {"unexpected": "shape"})):
        try:
            backend.complete(system="sys", user="hello")
        except RuntimeError as e:
            assert "Unexpected OpenRouter response shape" in str(e)
        else:
            raise AssertionError("should have raised")


def test_payload_routing_and_call_details():
    """reasoning=None omits the field; provider and logprobs pass through; the serving
    provider and logprobs are recorded. The default turns reasoning off explicitly."""
    payloads = []
    reply = _ok("4", id="gen-1", provider="DigitalOcean")
    reply.json.return_value["choices"][0]["logprobs"] = {
        "content": [{"token": "4", "logprob": 0, "top_logprobs": []}]}

    def post(url, headers=None, json=None, timeout=None):
        payloads.append(json)
        return reply

    with patch(POST, side_effect=post):
        b = OpenRouterBackend(model="meta-llama/llama-4-maverick", api_key="k", reasoning=None,
                              top_logprobs=5, provider={"require_parameters": True})
        assert b.complete("", "2+2?") == "4"
        OpenRouterBackend(model="x", api_key="k").complete("", "2+2?")
    assert "reasoning" not in payloads[0]
    assert payloads[0]["provider"] == {"require_parameters": True}
    assert payloads[0]["logprobs"] is True and payloads[0]["top_logprobs"] == 5
    assert payloads[1]["reasoning"] == {"enabled": False}
    assert b.last_provider == "DigitalOcean" and b.logprobs_available


def test_shared_rate_limiter_throttles_across_instances():
    """Two backends with DIFFERENT models share one bucket: the cap is per account."""
    _SHARED_OPENROUTER_LIMITER._calls.clear()
    _SHARED_OPENROUTER_LIMITER.max_per_minute = 3      # shrink for a fast test
    _SHARED_OPENROUTER_LIMITER.window_seconds = 0.3
    try:
        a = OpenRouterBackend(model="model-a", api_key="k")
        b = OpenRouterBackend(model="model-b", api_key="k")
        with patch(POST, return_value=_ok("x")):
            t0 = time.time()
            for backend in (a, b, a, b):     # the 4th call must wait for the shared window
                backend.complete(system="s", user="u")
            elapsed = time.time() - t0
        assert elapsed > 0.05, f"4th call was not throttled ({elapsed:.3f}s)"
    finally:
        _SHARED_OPENROUTER_LIMITER.max_per_minute = 18
        _SHARED_OPENROUTER_LIMITER.window_seconds = 60.0
