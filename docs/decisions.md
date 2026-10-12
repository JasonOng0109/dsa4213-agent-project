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

### 2026-10-12 — Long reports are held to 88-96 words

- **Decision**: every long report is 88 to 96 words, and the longest in a trial is at
  most 1.10 times the shortest (`pipeline/conditions.py`, `LONG_WORDS`, `LONG_MATCH`).
  The pilot's code still checked 88 to 100.
- **Why** [STATED: proposal §4.1]: "long reports of 88 to 96 words, with the longest
  report in a trial at most 1.10 times the shortest ... 96 divided by 88 is 1.091". A
  band reaching 100 permits 100 / 88 = 1.14, which the cap forbids. Decided in the
  pilot on 2026-09-28 and never applied to its code.
- **Rejected**: 88-100 with a 1.15 cap, which loosens the constraint that stops length
  standing in for provenance.
- **Breaks if changed**: a wider band lets one report in a trial be noticeably longer
  than another, a salience cue that could do the work a provenance statement should.

### 2026-10-12 — The graded wording ladder is built as W1-W3, on top of X5

- **Decision**: three extra conditions, W1, W2 and W3, are X5 with its quality statement
  replaced by "{independent agent}'s source is *somewhat* / *considerably* / *far* more
  reliable than the source shared by {the other two}." Same reports, same dependence
  note, same rotation as X5. Their factor vectors are X5's with a ninth factor,
  `quality_wording`, which is `categorical` for X4 and X5 and empty elsewhere
  (`pipeline/conditions.py`). They run as their own arm, `ladder`.
- **Why** [STATED: proposal §4.1]: "Three rungs vary only an intensity phrase, from
  somewhat to considerably to far more reliable than the shared source, turning the
  ladder into a dose-response curve with the categorical wording as its ceiling." The
  pilot moved the ladder into the main programme on 2026-09-28 but never built it, and
  no document fixes its exact sentence. **The sentence above is new and needs the
  team's review before the main run.**
- **Rejected**: rungs on X4 (quality without dependence). "Than the shared source"
  presupposes that the shared source has been identified, and the proposal names X5's
  wording as the ceiling.
- **Breaks if changed**: if a rung changes anything besides the intensity word, the
  ladder stops being a dose-response curve and H4's defence against "it only complied
  with an instruction" is lost.

### 2026-10-12 — Parse failures are excluded from decision denominators

- **Decision**: a cell's correct, abstain and off-list (`no_match`) rates are taken over
  the repeats that parsed (`pipeline/score.py`, `cell`). Parse failures are counted and
  printed beside the cell, never scored as wrong. An abstention or an off-list answer is
  a response and stays in the denominator.
- **Why** [STATED: proposal §3]: "Judge outputs that do not parse are logged with an
  explicit parse-failure flag and excluded from decision denominators rather than
  dropped silently or guessed." The pilot's scorer divided by every record.
- **Breaks if changed**: a judge with more parse failures would look less accurate,
  mixing an instrument failure into the measured behaviour.
