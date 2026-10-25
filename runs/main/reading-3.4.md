# Reading the main run's frozen reports (step 3.4)

Read by Jason on 2026-10-25, before any judging, from `runs/main/frozen_reports.json`.
Generation froze every source of all 40 cases in 1,956 calls; only M1's B and M25's A
needed a second round. It cost about $1.49 (planned: $0.48, at the proposal's rate).

## Result: judging can go ahead

| Check | Result |
|---|---|
| Hint (T1 cases) | All 30 kept: both of A's reports still sound unsure. No case is relabelled; the corpus stays 30 T1 and 10 T2. |
| Same whole | All 40: A's and B's reports describe the same quantity. |
| No leaks | None: the runner's leak check is clean, and no report names its writer. |

## Notes, not fails (for the analysis)

- **A's report turned into the question.** The reporter rewrote one of A's two reports as
  the question turned into a statement in M9 and M40 (both T2), and in M3, M13, M23, M28
  and M38 (T1, where A's hedge still marks it). Each case shows the same reports in every
  condition, so this moves that case's baseline, not the comparisons. Worth a check of the
  results without these cases.
- **A7 reports that read alike:** M10's B and D (overlap 0.41), M36's B and D (0.40), and
  M35's B and D, which open the same way (0.32).
- **Wording the sentence did not have:** M3's D, shown only in A7, begins "Based on
  hydrostatic sounding". M22's B reports (T2) sound like a spec sheet ("is specified
  with", "is rated at"); A's do not. One of M14's A reports (T2) brings back the question's
  word "rate".

## For authors and reviewers

Find your case above. If you read a hint differently, tell Jason. A relabel now would
disagree with the tier stored in the trial records, so it would be handled in the analysis.
