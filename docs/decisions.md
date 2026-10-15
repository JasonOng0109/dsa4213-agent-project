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

### 2026-10-12 — Long reports are held to 88-96 words

- **Decision**: every long report is 88 to 96 words, and the longest in a trial is at
  most 1.10 times the shortest (`pipeline/conditions.py`, `LONG_WORDS`, `LONG_MATCH`).
- **Why** [STATED: proposal §4.1]: "long reports of 88 to 96 words, with the longest
  report in a trial at most 1.10 times the shortest ... 96 divided by 88 is 1.091". The
  band and the cap agree: a band reaching 100 would permit 100 / 88 = 1.14, which the
  cap forbids.
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
  proposal fixes the three intensity words but not the full sentence around them, so
  **the sentence above needs the team's review before the main run.**
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
  dropped silently or guessed."
- **Breaks if changed**: a judge with more parse failures would look less accurate,
  mixing an instrument failure into the measured behaviour.

### 2026-10-12 — A negative one-report step makes n_eff an anomaly

- **Decision**: where `w = l(A1) - l(A0)` is negative, n_eff is not computed; the cell is
  reported as an anomaly and counts toward the judge's undefined rate
  (`pipeline/score.py`, `neff`). Where `|w| < 0.2` logits it is undefined.
- **Why** [INFERRED: from proposal §4.2]: the index "requires the repeated evidence to
  support the truth", which is why the agreement block always repeats the strong source.
  One report of that source should therefore raise belief in the truth. A judge whose
  belief falls instead has a backwards unit, and every value divided by it would come
  out inverted.
- **Rejected**: guarding only `|w| < 0.2`, which would still divide by a large negative
  step.
- **Breaks if changed**: an inverted unit turns correlation neglect into its opposite
  for that cell, silently.

### 2026-10-12 — Decision stability is read against its own chance baseline

- **Decision**: each cell prints, beside its stability, the stability expected from
  random answering at that cell's repeat count (`pipeline/score.py`,
  `stability_chance`). It is computed exactly over every way the answers can split,
  over the four options plus the abstain option where the arm offers it.
- **Why** [STATED: proposal §5]: "The floor is not the 0.25 chance of any single option,
  because the measure takes the largest of four counts: under random answering the
  expected value is about 0.41 at twelve repeats, 0.47 at six and 0.53 at four, so the
  base-line is simulated per repeat count rather than assumed." Exact computation gives
  the value a simulation estimates.
- **Breaks if changed**: against 0.25, a judge answering at random over four repeats
  (0.53) would look twice as stable as chance.

### 2026-10-12 — The discrimination check is reported, with no pass mark yet

- **Decision**: the scorer reports, per judge and condition on the short arm, the AUROC
  of the stated probability of the chosen answer for correct against incorrect
  decisions, with both class counts (`pipeline/score.py`, `report_discrimination`). It is
  undefined only when a class is empty. It does not yet exclude any judge: only the
  ordering check does.
- **Why** [STATED: proposal §5]: a stated probability is admitted as evidence only if it
  passes both ordering and discrimination, "each run and reported per judge whatever the
  outcome", computed "within condition, since pooling across conditions would conflate a
  judge's confidence with the manipulation itself". The proposal fixes neither the AUROC
  a judge must reach nor the smallest class size worth reporting, so neither is set
  here. **Open: the team sets both before the main run.**
- **Breaks if changed**: pooled across conditions, a high AUROC would largely show that
  the manipulation worked, not that the number tracks being right.

### 2026-10-12 — The runner encodes the proposal's main programme as one table

- **Decision**: `pipeline/run.py` holds the main programme as `PROGRAMME`: the agreement
  block at 6 repeats, the conflict block at 12, the abstention arm (X1-X5 and A7) at 4,
  the screen at 4 rotations, all on every case with the three primary judges; the length
  arm (X1-X5 at 12 repeats, A1 and A2 at 6) with Sonnet 5 and GPT-5.4 only; and the
  wording ladder at 12 repeats with all three judges. `plan` prices it at the proposal's
  per-call rates and, at 40 cases, reproduces the proposal's 21,720 calls and $37.48.
- **Why** [STATED: proposal §5, "Run plan and cost"]: one table is the single place the
  repeat counts, judges and case scope live, so the plan, the dry run and the real run
  cannot disagree.
- **Open**: the length arm and the ladder run on "10 of the 40 cases", the same ten for
  both, but the proposal does not say which ten. The code takes the first ten in corpus
  order (`subset`). **The team should choose the ten deliberately**, for example spread
  across domains, dimensions and tiers, and order `cases/__init__.py` to match.
- **Breaks if changed**: the repeat counts carry the rotation balance: 12 gives every
  (truth position, wrong-claim offset) pairing once in the conflict block, and 4 gives
  every truth position once in the abstention arm.

### 2026-10-12 — The frozen reports are leak-checked before any judging

- **Decision**: `judge` refuses to start unless every source is frozen in full and no
  accepted report contains a word of its source's type description or an invented
  attribution (`pipeline/run.py`, `check_frozen`). The dry run applies the same check.
- **Why** [STATED: proposal §3]: "A leak check over the frozen reports runs before any
  judging, and a failed check blocks the run." Candidates are already checked when they
  are selected; this second check also catches a frozen file edited afterwards.
- **Breaks if changed**: a leak in one report would let a judge read provenance in an
  opaque condition, invalidating every comparison that condition enters.

### 2026-10-12 — Judges run with reasoning switched off by default

- **Decision**: `judge` sends `reasoning: {"enabled": false}` unless told otherwise
  (`--reasoning`), and logs reasoning tokens on every trial.
- **Why** [STATED: proposal §6]: "Frontier judges may reason adaptively even when
  reasoning is not requested, and may do so unevenly across conditions, which would make
  a judge a different instrument in one block than in another. Reasoning tokens are
  logged per trial, suppression is attempted explicitly". Omitting the field is not an
  explicit attempt, so the default sends one, and the logged reasoning tokens show
  whether it held.
- **Breaks if changed**: a judge that reasons unevenly across conditions confounds the
  condition contrasts the study exists to make.

### 2026-10-12 — The screen tests ordering with Page's test across cases

- **Decision**: a judge passes the screen's ordering check when Page's test for ordered
  alternatives, with the cases as blocks and P0 < P1 < P2 as the predicted order, gives
  a one-sided p below 0.05 (`pipeline/score.py`, `page_test`, `screen_verdict`). Each
  case enters as its mean P(truth) over the four rotations. The p-value is exact, with
  ties kept as midranks. The matching rank correlation, the mean Spearman correlation
  between predicted and observed order, is printed beside it, with each case's values.
- **Why** [STATED: proposal §5]: ordering is assessed by "Rank correlation and a test
  for ordered alternatives, not inspection". The code had instead required each case's
  values to rise strictly and excluded a judge failing on more than a third of cases, a
  cut-off the proposal does not state. [INFERRED: from the design] Page's test is the
  test for ordered alternatives when every block sees every level, as every case sees
  all three here, and its L is a linear function of the mean Spearman correlation, so
  one statistic gives both the correlation and the test. [STATED: team decision,
  2026-10-12] The proposal names no level; the team fixed it at 0.05, one-sided, before
  the pilot. It is the share of judges whose numbers carry no ordering that pass by luck:
  1 in 20.
- **Rejected**: the per-case strict rule, which has no known false-pass rate and
  excludes a judge that always puts the irrelevant report lowest but swaps P1 and P2 in
  half its cases, although its numbers clearly track informativeness. The
  Jonckheere-Terpstra test, which treats the three levels as independent groups and so
  ignores that they are matched within a case. The four rotations of a case as separate
  blocks: they share a case, so they are not independent and p would come out too small.
- **Breaks if changed**: every probability-based analysis, n_eff included, is reported
  only for retained judges, so this rule decides whose stated numbers count. With fewer
  than two cases no judge can pass, since one case gives at best p = 1/6: the one-case
  dry run excludes every judge and reports n_eff as undefined.

### 2026-10-12 — The pilot runs on 5 cases

- **Decision**: the pilot uses 5 of the 40 cases, so no case is authored only for the
  pilot. The pilot's screen verdict is a preview; the main run's verdict is computed on
  all 40 cases.
- **Why** [STATED: team decision, 2026-10-12]: 5 is the fewest cases at which one badly
  ordered case cannot, on its own, fail a judge on the screen's ordering check. Computed
  with `page_test` at the fixed level of 0.05: with 2 cases a judge passes only if both
  are perfectly ordered; with 3 or 4, one fully reversed case among perfect ones fails
  it (p = 0.28 and 0.11); with 5 it does not (p = 0.039), and a judge passes with one
  neighbouring pair swapped in 4 of its 5 cases. With fewer cases, a fail could not tell
  a broken judge from one bad case.
- **Rejected**: 2 cases, the fewest that can pass at all, where one slip fails the
  judge. 8 cases, which makes a pass likelier for a judge with occasional disordered
  cases, but needs three more cases authored and reviewed before any pilot.
- **Breaks if changed**: below 5, one case decides the pilot's screen verdict. The
  minimum depends on the level: a stricter level needs more cases
  (`tests/test_score.py` pins it at 5 for 0.05).

### 2026-10-15 — Filler sets are 77 to 80 words, and the linter warns when they are not

- **Decision**: each filler set is 77 to 80 words (`docs/authoring-rules.md`, R20), and
  `pipeline/lint.py` (`length_notes`) prints a warning, not a violation, when a set plus
  A's or B's content falls outside the 88-96-word band.
- **Why** [INFERRED: from the case files' word counts]: the band is checked only when the
  length arm is built (`check_long_lengths` in `pipeline/conditions.py`), after reports
  have been generated, and the authoring steps did not mention it. M3's 65-word sets
  would give 77-80-word reports, and M1's 76-word sets with B's 11-word sentence gave 87.
  A 77-80-word set around an 11-15-word sentence lands at 88-95. Jason chose 77-80 over
  76-78 in review for the margin.
- **Rejected**: 76-78 words, which lets an 11-word sentence fall to 87; a violation in
  place of a warning, since the content's length only estimates a paraphrase's length.
- **Breaks if changed**: a set below 77 words can push a long report under 88, and the
  length arm stops on that case after its reports have been paid for.

### 2026-10-15 — The dry run skips the length check for padded mock rewordings

- **Decision**: when the mock has no hand-written rewordings of a source's sentence
  (`MockBackend.pads` in `pipeline/llm.py`), that source's frozen result is marked
  `padded`, and `pipeline/conditions.py` does not length-check long reports built from
  it. Generation prints which cases were skipped. Real reporters never mark a result.
- **Why** [INFERRED: from a dry run of M3]: the mock's fallback wraps the sentence in a
  fixed lead-in and tail, so M3's fake rewordings were 21-29 words. With R20's 78-word
  filler the dry run failed at 99 words, while the 67-word filler that passed it would
  give 77-82-word reports in the real run. No filler length passed both, so the dry run
  was measuring the padding, not the case. The real check still runs in the real run,
  and fixing filler there costs nothing: filler is added after rewording, so the paid
  reports are reused. Jason chose this over per-case mock rewordings.
- **Rejected**: hand-written mock rewordings for every case, as M1 has (seven sentences
  per case, written into pipeline code by each author); a shorter fallback wrapper,
  which cannot give B three rewordings under the 0.50 pairwise overlap limit.
- **Breaks if changed**: without the skip, every new case must either break R20 to pass
  the dry run or fail it.

### 2026-10-15 — Long reports leave 3 words of room for rewording

- **Decision**: the reporter rejects a rewording more than 3 words longer or shorter than
  its source sentence (`LENGTH_DIFF_MAX` in `pipeline/reporter.py`), and each filler set
  plus A's or B's sentence must be 91 to 93 words (R20 in `docs/authoring-rules.md`),
  so A's and B's sentences are within 2 words of each other. The lint's R20 warning now
  checks 91-93 and the A-B gap. This replaces the fixed 77-80-word filler target.
- **Why** [INFERRED: from M3's long reports built with rewordings of chosen lengths]:
  each slot's filler is shared by A's and B's reports, and the band is 8 words wide, so
  the room for rewording is the band minus the A-B gap, halved. M3 with a 15-word A and
  a 10-word B had about 1 word of room: a real rewording 2 words off would stop the
  length arm, and A and B rewordings more than 8 words apart in length could only be
  fixed by paying to generate again. With both limits, every accepted rewording fits:
  91 - 3 = 88 and 93 + 3 = 96, and 96 / 88 stays under the 1.10 cap. Jason chose both
  guards and kept R20 for all 40 cases, since the ten length-arm cases are not chosen.
- **Rejected**: the 77-80-word target alone, which allowed reports one word from the
  band's edge; R20 only for the ten length-arm cases, which would need the ten chosen
  first and their cases reworked afterwards.
- **Breaks if changed**: a wider length limit in the reporter, or filler sized nearer
  the band's edges, lets an accepted rewording push a long report out of 88-96, and the
  length arm stops on that case.
