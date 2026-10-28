"""The judge prompt: numbered options, the abstain option only when the arm offers it,
provenance shown only where the condition shows it."""

import pytest

from cases import CASES
from pipeline.conditions import build_repeat
from pipeline.prompt import ABSTAIN, NO_REPORTS, NUMBER_TEMPLATE, TEMPLATE, render

CASE = CASES["M1"]


@pytest.fixture
def by_condition(frozen):
    return lambda r, **kw: {t["condition"]: t for t in build_repeat("M1", CASE, frozen["M1"], r, **kw)}


def test_options_numbered_and_abstain_only_when_offered(by_condition):
    t = by_condition(2, allow_abstain=True)["X5"]
    p = render(t)
    assert "\n".join(f"  {i}. {o}" for i, o in enumerate(t["answer_options"], 1)) in p
    assert "A. " not in p and "(A)" not in p   # numbered, never lettered
    assert ABSTAIN in p and "same underlying source" in p
    assert ABSTAIN not in render(by_condition(2)["X5"])


def test_no_reports_and_provenance_rendering(by_condition):
    t = by_condition(1)
    assert NO_REPORTS in render(t["A0"])
    assert "(source: S-001) says:" in render(t["A5"])
    x2 = render(t["X2"])
    assert "(source: student-run module wiki page) says:" in x2
    assert "(source: ME2103 assessment brief, section 4) says:" in x2
    assert "(source:" not in render(t["X1"]) and "Note:" not in render(t["X1"])


def test_the_cross_check_prompt_asks_for_numbers_and_changes_nothing_else(by_condition):
    """docs/decisions.md, 2026-10-26: only the format lines differ, so the cross-check's
    trials ask what the main run's ask."""
    changed = [(a, b) for a, b in zip(TEMPLATE.splitlines(), NUMBER_TEMPLATE.splitlines())
               if a != b]
    assert len(TEMPLATE.splitlines()) == len(NUMBER_TEMPLATE.splitlines())
    assert changed == [
        ('{{"answer": "<one of the possible answers, verbatim>",',
         '{{"answer": <the number of one of the possible answers>,'),
        (' "p": {{"<answer text>": <integer 0-100>, ...}}}}',
         ' "p": {{"<answer number>": <integer 0-100>, ...}}}}'),
        ("answer text as the key, and the values must sum to 100.",
         "answer number as the key, and the values must sum to 100.")]
    t = by_condition(1)["X1"]
    assert "<the number of one of the possible answers>" in render(dict(t, by_number=True))
    assert "<one of the possible answers, verbatim>" in render(t)
