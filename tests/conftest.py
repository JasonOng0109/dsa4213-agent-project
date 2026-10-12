"""Every test runs offline: any attempt to open a socket fails loudly."""

import socket


def _no_network(*a, **k):
    raise AssertionError("network call attempted")


socket.socket.connect = _no_network
socket.create_connection = _no_network


import pytest  # noqa: E402


@pytest.fixture(scope="session")
def frozen():
    """Every case's reports, frozen on the mock backend: {case_id: {source: result}}."""
    from cases import CASES
    from pipeline.llm import MockBackend
    from pipeline.reporter import freeze_sources
    out = {}
    for case_id, key, result in freeze_sources(CASES, MockBackend(), MockBackend()):
        out.setdefault(case_id, {})[key] = result
    return out
