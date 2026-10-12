# Decisions log

Why the code is the way it is, so nobody has to reconstruct the reasoning from commits.
One entry per decision, newest last. Every entry has five fields:

- **Date**: when it was decided.
- **Decision**: what is true of the code or design now, with a file name.
- **Why**: tagged `[STATED: where]` when a source says it in as many words, or
  `[INFERRED: how]` when it is read off code or data.
- **Rejected**: the alternative that was on the table, where there was one.
- **Breaks if changed**: what stops working or stops being measurable.

Add an entry when you make a choice a reader could not guess from the code.

---

### 2026-10-12 — This repository replaces the pilot codebase

- **Decision**: the study runs from this repository, rebuilt from the pilot directory
  `smoke_test/` to follow the submitted proposal (`docs/proposal.pdf`). One protocol
  only: the pilot's v1 and v2 cases, conditions and code paths are not carried over, and
  M1, the pilot's only case in the current schema, is the first case. No pilot output is
  copied: frozen reports, trial logs and probes are regenerated here.
- **Why** [STATED: request of 2026-10-12]: the pilot kept three protocol generations
  side by side under version-suffixed names (`cases_v3.py`, `run_v3.py`), with no
  version history.
- **Rejected**: copying the pilot's frozen M1 reports and its Stage A log. They came
  from code this repository no longer runs, and the pilot already classes Stage A as
  instrumentation, not evidence.
- **Breaks if changed**: mixing pilot outputs with outputs of this code puts two code
  versions under one analysis.

Where the pilot's files went:

| Pilot (`smoke_test/`) | Here |
|---|---|
| `cases_v3.py` | `cases/m1.py`, registered in `cases/__init__.py` |
| `docs/AUTHORING-RULES.md` | `docs/authoring-rules.md` |
| `llm_backend.py`, `router_credit_check.py` | `pipeline/llm.py` |
| `generate_reports.py` | `pipeline/reporter.py` |
| `build_conditions.py` | `pipeline/conditions.py` |
| `judge_prompt.py` | `pipeline/prompt.py` |
| `run_judge.py` | `pipeline/judge.py` |
| `score_report.py` | `pipeline/score.py` |
| `lint_cases.py` | `pipeline/lint.py` |
| `run_v3.py` | `pipeline/run.py` |
| `tests/`, `test_openrouter_backend.py` | `tests/` |
| `related_works/<arXiv id>.pdf` | `related_works/<short name>.pdf` |
| `cases.py`, `cases_v2.py`, `run_smoke_test.py`, `archive/` | not carried over (v1/v2) |
