"""The linter: the corpus lints clean, and on the leaky fixture every planted fault is
flagged under its rule and nothing else is -- including the specificity asymmetry,
which no script can see."""

import contextlib
import copy
import io

from cases import CASES
from pipeline.lint import length_notes, lint
from tests.leaky_cases import CASES as FIXTURE, EXPECTED


def _quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def test_corpus_is_clean():
    assert _quiet(lint, CASES) == []


def test_fixture_flags_exactly_the_plants():
    flagged = {cid: set() for cid in FIXTURE}
    for cid, rule, _ in _quiet(lint, FIXTURE):
        flagged[cid].add(rule)
    bad = {cid: (EXPECTED[cid], flagged[cid]) for cid in FIXTURE
           if flagged[cid] != EXPECTED[cid]}
    assert not bad, f"expected vs flagged: {bad}"
    assert flagged["S01_specificity_asymmetry"] == set()
    assert flagged["S02_screen_names_options"] == set()   # no R8 / R9 on the screen sentence


def test_every_case_has_a_screen_sentence():
    for case in CASES.values():
        assert case.get("screen_partial")


def test_short_filler_gets_a_length_warning():
    """M1's filler set 0 makes 91-92-word long reports; one sentence fewer falls short."""
    case = copy.deepcopy(CASES["M1"])
    assert not any(n.startswith("filler_sets[0]") for n in length_notes(case))
    case["filler_sets"][0] = case["filler_sets"][0][:-1]
    assert any(n.startswith("filler_sets[0]") for n in length_notes(case))
