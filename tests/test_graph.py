"""The knowledge graph's checker, run as a test: every node quotes a file in this
repository, and a quote that stops matching its file is drift to fix, not to ignore."""

import contextlib
import io
import runpy
from pathlib import Path

CHECKER = Path(__file__).resolve().parent.parent / "tools" / "check_graph.py"


def test_knowledge_graph_checks_clean():
    check = runpy.run_path(str(CHECKER))
    with contextlib.redirect_stdout(io.StringIO()) as out:
        status = check["main"]()
    assert status == 0, out.getvalue()
