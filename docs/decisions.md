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
  **the sentence above needs the team's review before the main run.** Reviewed and kept
  on 2026-10-18; see that day's entry.
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
  ordering check does (until 2026-10-18, and again from 2026-10-21; see that day's
  entry).
- **Why** [STATED: proposal §5]: a stated probability is admitted as evidence only if it
  passes both ordering and discrimination, "each run and reported per judge whatever the
  outcome", computed "within condition, since pooling across conditions would conflate a
  judge's confidence with the manipulation itself". The proposal fixes neither the AUROC
  a judge must reach nor the smallest class size worth reporting, so neither is set
  here. **Open: the team sets both before the main run.** Both set on 2026-10-18; see
  that day's entry.
- **Breaks if changed**: pooled across conditions, a high AUROC would largely show that
  the manipulation worked, not that the number tracks being right.

### 2026-10-12 — The runner encodes the proposal's main programme as one table

- **Decision**: `pipeline/run.py` holds the main programme as `PROGRAMME`: the agreement
  block at 6 repeats, the conflict block at 12, the abstention arm (X1-X5 and A7) at 4,
  the screen at 4 rotations, all on every case with the three primary judges; the length
  arm (X1-X5 at 12 repeats, A1 and A2 at 6) with Sonnet 5 and GPT-5.4 only; and the
  wording ladder at 12 repeats with all three judges. `plan` prices it at the proposal's
  per-call rates and, at 40 cases, reproduces the proposal's 21,720 calls and $37.48.
  The P0 check added to the abstention arm on 2026-10-21 adds 480 calls at 40 cases.
- **Why** [STATED: proposal §5, "Run plan and cost"]: one table is the single place the
  repeat counts, judges and case scope live, so the plan, the dry run and the real run
  cannot disagree.
- **Open**: the length arm and the ladder run on "10 of the 40 cases", the same ten for
  both, but the proposal does not say which ten. The code takes the first ten in corpus
  order (`subset`). **The team should choose the ten deliberately**, for example spread
  across domains, dimensions and tiers, and order `cases/__init__.py` to match. The rule
  for choosing them was fixed on 2026-10-18; see that day's entry.
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

### 2026-10-15 — Only the conditions the length arm runs are length-checked

- **Decision**: `LONG_ARM` in `pipeline/conditions.py`, the conflict block plus A1 and A2,
  names the conditions run at long length, and `pipeline/run.py` takes its long entries
  from the same names. `build_conditions` still builds every condition at long length,
  but length-checks only the reports used by a condition in `LONG_ARM`.
- **Why** [INFERRED: from M1 built with every rewording 3 words longer]: A7 (B, C and D)
  was built and checked at long length and then never judged. M1's 14-word C sentence
  reworded 3 words longer made a 97-word A7 report and stopped the build, although R20
  and the reporter's length limit allow that rewording. Checking only what is run makes
  R20's guarantee hold without any rule on C's and D's lengths.
- **Rejected**: extending R20 to C and D, so that all four sentences are within 2 words
  of each other, which asks authors to fit a trial that is never run long.
- **Breaks if changed**: a condition added to the length arm but not to `LONG_ARM` would
  go unchecked; `tests/test_run.py` fails when the two disagree.

### 2026-10-18 — Authors do not update the corpus count

- **Decision**: case authors leave the corpus count alone: README's corpus bullet, the
  `open-corpus` node and the "cases written" card in `knowledge-graph.html`. Jason
  updates all three when he merges each case's pull request. Until then, the
  knowledge-graph test (`test_knowledge_graph_checks_clean`) fails on the `open-corpus`
  quote of `cases/__init__.py`, and that is expected.
- **Why** [STATED: team decision, 2026-10-18]: Jason chose this. [INFERRED: from the
  pilot case pull requests] before the rule, authors did it three ways: M2 left the
  count alone, Jason updated M3's himself, and M5 updated it in its own pull request.
  When two branches both changed the count, merging the second needed fixing by hand,
  and lines both branches had changed the same way merged silently and stayed wrong.
- **Rejected**: each author updates the count in their own pull request, and whoever
  merges second fixes it. In Phase 4, 35 cases are written in parallel, so every case
  pull request would conflict with every other.
- **Breaks if changed**: the `open-corpus` node must keep quoting the `CASES` line of
  `cases/__init__.py`. That failing check is what reminds Jason to update the count when
  he merges.

### 2026-10-18 — The wording ladder's sentence is kept as built

- **Decision**: W1-W3 keep the sentence in `pipeline/conditions.py` (`rung`): X5's
  dependence note, then "{independent agent}'s source is *somewhat* / *considerably* /
  *far* more reliable than the source shared by {the other two}." This is the review
  the 2026-10-12 ladder entry asked for.
- **Why** [STATED: team decision, 2026-10-18]: Jason decided, following the review
  steps in `docs/work-plan.md` (2A). [INFERRED: from M1's prompts in a dry run] W1, W2
  and W3 differ only in the intensity word. [STATED: proposal §4.1] the phrase is the
  proposal's own, "from somewhat to considerably to far more reliable than the shared
  source"; the code names the two agents that share it, because the judge sees agents,
  not source names. "More reliable" names quality without hinting at age or
  officialness, and fits all four quality dimensions. X5's clause is a different kind
  of statement: labels ("a primary, authoritative record", "a secondhand or unofficial
  one"), not a comparison. So the write-up reads X5 as the categorical reference the
  proposal calls the ceiling, not as a fourth rung.
- **Breaks if changed**: a rung that changes anything besides the intensity word stops
  being a step on one dose-response curve.

### 2026-10-18 — H6 counts a margin below 10 points as near indifference

- **Decision**: a forced-choice record does not identify the answer given when its
  answer is not its highest-probability option, or when its top two probabilities are
  less than 10 points apart (`MARGIN_THRESHOLD` and `unbacked` in `pipeline/score.py`);
  a tie at the top is a margin of 0. The margin is taken on the stated numbers rescaled
  to sum to 100, so 50 against 40 written with a total of 105 is a margin of 9.52 and is
  flagged. `report_h6` prints, per judge, how many of the short arm's conflict-block
  records are flagged, and how often the judge abstains in their twins in the
  abstention arm (same case, condition and repeat) against the twins of the other
  records, beside its own abstention rate in A7. Amended 2026-10-19: that comparison is
  made inside each conflict condition and then combined (`_mh_difference`, a
  Mantel-Haenszel difference), never on the block pooled, and a p-value on it takes the
  case as the unit, as discrimination's does. It prints the same
  comparison at 5 and 20 points (`MARGIN_SENSITIVITY`), declared in advance as a
  sensitivity check; conclusions rest on 10. Like n_eff, it is reported only for judges
  the confidence screen retains, since the flag reads stated numbers.
- **Why** [STATED: proposal §5]: H6 counts records "whose stated probabilities do not
  identify the answer given, either because the answer is not the highest-probability
  option or because the margin between the top two options falls below a stated
  threshold", and tests "the abstention rate in those same trials, within judge and read
  against that judge's own abstention rate in A7". The proposal states no number.
  [STATED: team decision, 2026-10-18] 10 points, fixed before any pilot result: below
  10, a tie or a lead of a few points, such as 50 against 45, counts as near
  indifference, while 50 against 40 already leans one way. For a judge that writes in
  steps of 5, below 10 means a tie or one step from one. [STATED: `build_repeat` in
  `pipeline/conditions.py`] "every arm of one repeat shows the same reports in the same
  order", so a twin differs from its forced-choice trial only by the abstain option.
  [INFERRED: from a constructed judge in `tests/test_score.py`; Kai Rong raised it
  reviewing this entry] close numbers and abstaining can both be commoner in one
  condition than in another, since X1 leaves the conflict open and X5 settles it, and
  pooling the block turns that into a difference no trial shows. A judge that abstains
  in half its X1 trials whatever its numbers, and never in X5, abstains pooled in 10 of
  24 flagged trials against 10 of 56 others, yet equally often inside each condition.
  Discrimination stays within condition for the same reason. [STATED: team decision,
  2026-10-19] The comparison is made inside each condition, and the margin stays on the
  rescaled numbers: Kai Rong raised both reviewing this entry, and Jason agreed.
  [INFERRED: from `_parse_object` in `pipeline/judge.py`] P(truth), the confidence that
  discrimination reads and coherence all come from the same rescaled numbers, so the
  margin does too. Numbers summing outside 90-110 give no margin at all
  (`p_sum_out_of_range`), so rescaling can move a margin across the cut-off only when
  it lies within a point of 10.
- **Rejected**: 15 or 20, which would count 50/40 or 55/40 as indifferent although they
  lean; a cut-off chosen after seeing the pilot's margins; the conflict block pooled,
  as first written, which can show H6 where no trial does; the margin on the numbers as
  written, which would read H6's flag on a different scale from every other stated
  number.
- **Breaks if changed**: the flagged records, and so H6's test, change with the cut-off.
  Moved after seeing data, it could be bent to fit the result.

### 2026-10-18 — Discrimination passes a judge on one informative condition

- **Decision**: on the short arm, a condition counts when it has at least 10 correct and
  10 incorrect decisions (`MIN_CLASS` in `pipeline/score.py`); A0 never counts. A judge
  passes when at least one counted condition has AUROC above 0.5 with a one-sided p
  below 0.05 divided by the number of counted conditions (`discrimination_verdict`). The
  p-value comes from `auroc_p`, which shuffles whole cases: 2,000 shuffles from a fixed
  seed (`SHUFFLES`, `SHUFFLE_SEED`), each scoring every case's stated probabilities
  against another case's right/wrong record, repeat by repeat. With no counted condition
  the check cannot be assessed, and the judge is excluded. A judge excluded by ordering
  or by discrimination gets no n_eff and no H6 result. This sets what the 2026-10-12
  discrimination entry left open. Amended 2026-10-19: the p-value first counted each
  decision as independent evidence (the Mann-Whitney test); it now shuffles whole cases.
  Replaced 2026-10-21, after the pilot: the verdict is printed but excludes no judge;
  see that day's entry.
- **Why** [STATED: proposal §5]: a stated probability is admitted as evidence "only if
  it passes both checks", discrimination is "computed within condition", and the screen
  guards against "a judge that returns a high number on every answer". [STATED: team
  decision, 2026-10-18] A test at the screen's level, not a fixed AUROC. [INFERRED: from
  the simulations in `tests/test_score.py`] at 12 correct and 48 incorrect independent
  decisions, about one conflict condition in the pilot, a judge whose numbers carry no
  information passes the test about 1 time in 20, but reaches an AUROC of 0.60 by luck
  more than 1 time in 10. A fixed mark is also too strict where decisions are many: it
  fails a judge at 0.58 whose numbers do carry information. [STATED: team decision,
  2026-10-19] The case, not the decision, is the unit of the p-value: Kai Rong raised it
  reviewing this entry, and Jason agreed. [INFERRED: from `build_repeat` in
  `pipeline/conditions.py`] a case's repeats run at temperature 0 and differ only in
  their rotations, so they are near-copies, which the judge answers almost alike.
  [INFERRED: from the near-copies simulation in `tests/test_score.py`] with 10 cases of
  12 repeats, counting each decision passes a judge whose numbers carry no information
  about 1 time in 4 (51 of 200), while shuffling whole cases passes it about 1 time in
  20 (9 of 200). The ordering check already averages a case's rotations for the same
  reason (the 2026-10-12 entry on Page's test). Dividing the level by the number of
  counted conditions keeps the false-pass rate near 1 in 20 however many count. At
  least one condition, not every: in X1, being wrong mostly means following the two
  agreeing reports, which a judge can do confidently, and that is the effect under
  study, so AUROC can fall below 0.5 there for a judge whose numbers carry information.
  A judge stating the same number on every answer sits at 0.5 everywhere and still
  fails. Ten per class: below that, one decision can move AUROC by more than a tenth. A0
  shows no report, so a right answer there is a lucky guess about a made-up fact. Not
  assessable counts as a fail, because the proposal admits a number only once it passes.
- **Rejected**: a fixed pass mark such as 0.60; requiring every counted condition to
  pass, or pooling all conditions into one AUROC, either of which could exclude a judge
  for being confidently wrong where the study predicts it; a p-value that counts each
  decision as independent evidence, the rule's first version, which makes p far too
  small when a case's repeats are near-copies.
- **Breaks if changed**: this rule decides whose stated numbers count, through n_eff and
  H6. Counting decisions instead of cases lets a judge whose numbers carry no
  information pass about 1 time in 4. The pilot has about 60 decisions per judge in each
  conflict condition, so the check is weak there: a pilot fail is a preview, like the
  pilot's screen verdict.

### 2026-10-18 — The ten-case subset is fixed by a rule before the pilot

- **Decision**: the ten cases for the length arm and the wording ladder are M1-M5 plus
  five Phase 4 cases that Kai Rong marks when assigning the batches, before they are
  written. Two of the five are T2 and three T1, so three of the ten are T2. Every domain
  has at least 3 of the ten, and every quality dimension at least 2. A marked case that
  is dropped is replaced by the next assigned case with the same domain, dimension and
  tier. Before the main run, `cases/__init__.py` puts the ten first, since `subset` in
  `pipeline/run.py` takes the first ten. For the pilot, on 5 cases, those are all five.
  Marked 2026-10-19, with the first Phase 4 batches: M6, M14, M22, M30 and M38, one per
  author, of which M14 and M22 are the two T2 (`docs/work-plan.md`, case register).
  A case of the ten that is relabelled T2 once its frozen reports are read (R16) stays
  in the ten, so the ten may end with more than three T2 cases: swapping it out would
  choose cases after seeing results. Amended 2026-10-21: the other 25 cases were assigned
  together, before anyone drafted them, so each marked case's replacement is named in the
  case register as its backup, with the same domain, dimension and tier and a different
  author: M16 for M6, M8 for M14, M9 for M22, M17 for M30 and M32 for M38.
- **Why** [STATED: team decision, 2026-10-18]: the ten are chosen before any of them is
  run, so neither the pilot's results nor how cases turn out can steer the choice.
  [STATED: `docs/work-plan.md`, Phase 1] M1-M5 "cover all 3 domains and all 4 quality
  dimensions". Three T2 in ten is close to the corpus's target of about 10 in 40
  (`docs/work-plan.md`, "Targets for all 40"). [STATED: team decision, 2026-10-19] A
  case relabelled T2 stays in the ten: Kai Rong raised it reviewing this entry, and
  Jason agreed. [STATED: Kai Rong, 2026-10-21] with the other 25 cases assigned
  together, "the next assigned case" can fit two cases, such as M11 and M17 for M30, so
  each backup is named before any of them is written. A different author means one
  author's drafts cannot lose both a marked case and its backup.
- **Rejected**: choosing the ten once all 40 are merged, the earlier plan in
  `docs/work-plan.md` (2D), when the pilot's results on M1-M5 would already be known.
- **Breaks if changed**: a subset chosen after seeing results could favour cases where
  the ladder or the length arm behaves as predicted.

### 2026-10-18 — The pilot runs the whole programme on M1-M5

- **Decision**: the pilot runs every entry of `PROGRAMME` (`pipeline/run.py`) on M1-M5.
  `plan --cases 5` gives 3,660 calls and $7.03, of which 240 calls generate the reports.
  The ceilings are `generate --max-calls 600`, two full rounds for every source, and,
  for the judge step, each entry's planned calls. The judge step runs one entry at a
  time, each into its own log, and the scorer reads the logs together:

  | Entry | Calls | Cost |
  |---|---|---|
  | agreement | 720 | $1.28 |
  | conflict | 900 | $1.60 |
  | abstain | 360 | $0.64 |
  | screen | 180 | $0.32 |
  | ladder | 540 | $0.96 |
  | long-conflict | 600 | $1.80 |
  | long-agreement | 120 | $0.36 |

  The group approves up to $10. Amended 2026-10-19: the pilot is scored with
  `--show-excluded` (`pipeline/score.py`), which also prints n_eff and H6 for the judges
  the confidence screen excludes, marked as checks rather than results.
- **Why** [STATED: team decision, 2026-10-18]: every arm meets real models once before
  the main run, and each can fail in its own way: the long reports' length check,
  parsing the abstain answer, the ladder's notes, the screen. The pilot also measures
  the cost per call by arm (`report_health` in `pipeline/score.py`), including the
  long-report rate, the one rate the proposal estimates rather than measures; the
  budget request for the main run needs it. [INFERRED: from `judge_all` and `cmd_judge`
  in `pipeline/run.py`] the judge step makes one call at a time and stops on a failed
  call, and a stopped log cannot be resumed, only rerun into a new log, so one entry per
  log limits a stop to one entry. $10 leaves room above the $7.03 estimate, since the
  long arm's $2.16 is priced at the estimated rate. [INFERRED: from `auroc_p` and
  `tests/test_score.py`; Kai Rong raised it reviewing this entry] discrimination's
  p-value shuffles whole cases (the discrimination entry, amended 2026-10-19), and 5
  cases allow only 120 arrangements: a judge whose numbers separate right from wrong
  perfectly still gets p near 1/120, while the pass level is 0.05 over the number of
  counted conditions, 0.01 for five. The pilot is therefore likely to exclude most
  judges, and without the option n_eff and H6 would not meet real data before the main
  run. [STATED: team decision, 2026-10-19] The pilot is scored with `--show-excluded`:
  Kai Rong raised it reviewing this entry, and Jason agreed.
- **Rejected**: running only some arms, which would leave the rest untested until the
  main run; showing excluded judges' n_eff and H6 in the main run too, which would set
  numbers the screen disqualifies beside the results.
- **Breaks if changed**: an arm left out of the pilot meets real models for the first
  time in the main run.

### 2026-10-18 — T1 cases vary their hedge

- **Decision**: R16 in `docs/authoring-rules.md` asks authors to vary the T1 cue across
  cases. Before choosing a hedge, an author lists the ones in use with
  `grep -n -i -A1 hedge cases/*.py`, picks the one used least or another kind of cue,
  and names it in `design_notes`. Work-plan step 1.4, which Phase 4 reuses, points to it.
- **Why** [STATED: team decision, 2026-10-18]: Jason added it before Phase 4. [INFERRED:
  from the pilot cases] M3's cue is "is understood to be", and the open pull requests
  for M2 and M4 use "is understood to have" and "is understood to be"; only M5 differs,
  with "is believed to have been". If the reporter drops that one phrase, three of the
  four T1 pilot cases become T2 together. If the other T1 cases copied it as well, the
  corpus's T1/T2 split would rest on whether the reporter keeps one phrase. R16's only
  example hedge was "is understood to be", which is likely why it spread.
- **Rejected**: leaving the choice of hedge to each author with no check, which is how
  three of four T1 pilot cases came to share one phrase.
- **Breaks if changed**: with one hedge on most T1 cases, the T1/T2 balance of the
  corpus depends on whether the reporter keeps that phrase.

### 2026-10-18 — Type names never say "independent"

- **Decision**: no `provenance.type` uses the word "independent". R19's method example in
  `docs/authoring-rules.md` is now "accredited laboratory test report", and R19 says why.
  On 2026-10-21 R19's table took new examples (that day's entry on type names); its
  paragraph on "independent" keeps this one.
- **Why** [STATED: team decision, 2026-10-18]: Kai Rong raised it reviewing M4, whose B
  was named "independent laboratory report" after R19's example, and Jason agreed.
  X2 shows the judge A's and B's type names, and X3's note says the strong report "comes
  from a different, independent source", so the word would give X2 part of X3's job.
  [INFERRED: from `pipeline/conditions.py`] X2 is the only condition that shows type
  names, so X1 against X2 reads H5 only if the names say nothing about dependence.
- **Rejected**: keeping the example, which leaves the next method case to copy it.
- **Breaks if changed**: for any case whose type name says "independent", X1 against X2
  would mix H5's named type with part of the dependence statement that X3 adds.

### 2026-10-19 — Phase 4 drafting starts before the pilot

- **Decision**: authors start drafting their Phase 4 cases now, before the pilot run, once
  Kai Rong has given them their first batch, using the lessons from the Phase 1 review
  comments and the current `docs/authoring-rules.md`. Phase 4 cases are merged only after
  the pilot has run. Kai Rong marks the five subset cases when assigning the batches,
  as the 2026-10-18 subset entry says, so before anyone drafts them.
- **Why** [STATED: team decision, 2026-10-19]: Jason told the team to start writing their
  8 cases early and to draft the base before the pilot run. [INFERRED: from
  `pipeline/run.py`] `generate` and `judge` take every case in `cases/__init__.py`, so a
  Phase 4 case merged before the pilot would join it, while the 2026-10-18 entry fixes
  the pilot at M1-M5.
- **Rejected**: waiting for the pilot to finish before drafting, as the work plan's
  tracker had it.
- **Breaks if changed**: a Phase 4 case merged before the pilot is generated and judged
  with M1-M5, so the pilot is no longer the 3,660-call programme on M1-M5 that the group
  approved up to $10 for.

### 2026-10-19 — The parser reads an answer written with its option number

- **Decision**: an answer, or a key of "p", written with the option's number from the
  prompt, such as "4. 15%", is read as that option, but only when the number is that
  option's place in the list (`_option` in `pipeline/judge.py`). A number and a text
  that disagree still give `no_match`. The pilot's logs stay as they were logged.
- **Why** [STATED: `pipeline/prompt.py`] "Options are numbered, never lettered", so a
  judge can copy the number into its reply. [STATED: the pilot's trial logs] GPT-5.4
  answered "4. 15%" and "4. 6 hours" in three A7 trials, with every key of "p" numbered
  the same way, and the parser logged them as `no_match`: three right answers counted
  against its accuracy and lost their stated numbers. [INFERRED: from `_norm` in
  `pipeline/judge.py`] formatting drift is already tolerated, but `_norm` keeps digits,
  so "4. 15%" reads as "415%" and matches nothing. Requiring the number to be the
  option's own keeps the parser from guessing: the number and the text must name the
  same option. [STATED: team decision, 2026-10-19] Jason chose to fix it before the main
  run, in its own pull request.
- **Rejected**: reading the text after any number, which would take "2. 15%" as 15%
  when 15% is option 4; re-parsing the pilot's logs, whose numbers are a preview.
- **Breaks if changed**: a judge that copies the numbers loses those trials as
  `no_match`, counted against its accuracy and without stated numbers, and the loss falls
  on that judge alone, so its accuracy reads lower than it is and its P(truth) misses
  trials.

### 2026-10-21 — Only ordering decides whose stated numbers count

- **Decision**: the confidence screen is the ordering check alone. Discrimination is
  still computed for every judge and condition on the short arm and printed with its
  class counts, but it excludes no judge: beside it the scorer prints the verdict of the
  rule as first registered, marked "not applied" (`report_discrimination` in
  `pipeline/score.py`). A judge that fails ordering is still excluded: it gets no n_eff
  and no H6 result, and its decisions still count. Beside each judge's n_eff the scorer
  prints how many of its agreement-block answers put 100 on one option (`report_neff`),
  a description, not a gate. This replaces the pass rule of the 2026-10-18
  discrimination entry; its test is unchanged. It was decided after the pilot and before
  the main run, and it departs from the proposal, which admits a number "only if it
  passes both checks", so the write-up reports it as a departure.
- **Why** [STATED: team decision, 2026-10-21]: Kai Rong raised it after reading the
  pilot's logs, and Jason agreed. [STATED: `runs/score-pilot.txt`] discrimination
  excluded all three judges in the pilot: Opus and GPT-5.4 could not be assessed, and
  Sonnet's one counted condition, X2, had p 0.24. [INFERRED: from the pilot's trial logs]
  every wrong answer in the conflict block, 379 across the three judges, was A's claim,
  and every parsed answer in A1-A7 was right. So inside every condition, right and wrong
  differed only by whether the judge followed the two agreeing reports. The 2026-10-18
  entry expected AUROC below 0.5 in X1 for that reason, and relied on another condition
  to pass a judge; in the pilot only Sonnet's X2 had 10 decisions of each kind.
  [INFERRED: from the pilot's class counts] counting "not assessable" as "not assessed",
  while a counted condition still decides, would not hold on 40 cases: if the new cases
  behave like M1-M5, GPT-5.4 gets about 24 right decisions in X1 and 48 in X3, and Opus
  about 16 in X3, so those conditions count and fail (AUROC 0.02 to 0.10 in the pilot),
  and a judge would be excluded for how often it resists the majority. [STATED: proposal
  §5] the screen exists because "a judge that returns a high number on every answer
  would make the measure uninformative". Ordering alone does not catch every such judge.
  [INFERRED: from `screen_verdict` in `pipeline/score.py`, Kai Rong's check in review]
  one that states 100 on whatever it picks has a mean P(truth) of 100 times its
  accuracy, which rises from P0 to P2 with the evidence: right 25%, 50% and 95% of the
  time, it is retained at p 0.0005 on 5 cases. So its share of answers stated at 100 is
  printed, a description that picks no rule after seeing data; in the pilot, GPT-5.4's
  was 151 of 239 agreement-block answers. [STATED: `build_screen` in
  `pipeline/conditions.py`] its trials are "graded by informativeness, not by evidence
  count", so ordering does not assume the behaviour under study, while discrimination
  inside the study's own conditions does.
- **Rejected**: keeping the rule, which leaves every belief result unreported because of
  the design, whatever the judges do; counting "not assessable" as "not assessed" while a
  counted condition still decides; reporting an excluded judge's belief results labelled
  as unscreened, which marks the numbers as failed when the check is what failed; adding
  trials with mixed right and wrong decisions, a new design no pilot has run; and resting
  the change on the belief results the pilot previewed, such as X1 to X3, which would let
  a result choose the rule.
- **Breaks if changed**: with discrimination back as a gate, this design excludes a judge
  for following the count where the study predicts it will, and with it every belief
  result. Without the printed verdict of the first rule, the departure from the proposal
  is hidden. Without the share of answers stated at 100, a judge that states 100 on
  whatever it picks passes the screen unseen, and its n_eff reads its accuracy.

### 2026-10-21 — n_eff at the clip reads "at ceiling"

- **Decision**: a cell whose mean P(truth) lies outside 1-99%, where `_logit` in
  `pipeline/score.py` clips it, gives a bound, not a value. Its n_eff reads "at
  ceiling", and so does every CN, IS or RP computed from it; a clipped A0 or A1 clips the
  unit, so then every value does, the unit w included (`neff`). Beside each judge's
  undefined rate, the scorer prints how many of its cases have a value at ceiling. The
  rule applies to every judge.
- **Why** [STATED: team decision, 2026-10-21]: Kai Rong raised it for GPT-5.4, and Jason
  chose a rule for every judge at the existing clip. [STATED: `runs/score-pilot.txt`]
  GPT-5.4's mean P(truth) in A4, A6 and A7 was 99.5 to 100 in M2-M5, so three of its five
  cells were clipped in each of those cases, and its IS and RP read 0.0, set by the clip,
  not by the judge. [INFERRED: from the pilot's trial logs] GPT-5.4 put 100 on one option
  and 0 on the others in 151 of its 239 parsed agreement-block answers; Opus never did,
  and Sonnet did 18 times. [STATED: proposal §5] "Calibration summaries such as the Brier
  score are reported only where stated values have usable spread". The clip was in the
  code before the pilot, so no number is chosen after seeing data.
- **Rejected**: a label for GPT-5.4 alone, a rule written for one judge after seeing its
  numbers; a lower cut-off such as 95, chosen after seeing the pilot; printing the
  clipped values, which read as a judge that ignores independence.
- **Breaks if changed**: a clipped cell printed as a number gives IS and RP near 0 for a
  judge whose numbers stopped at the top of the scale.

### 2026-10-21 — H6 is read from its rates, with P0 as a check beside A7

- **Decision**: H6's test is unchanged. It is reported per judge as the scorer prints it:
  how many conflict-block records do not identify the answer given, and the abstention
  rates inside each condition and in A7. The abstention arm also runs P0, the screen's
  irrelevant report, offering the abstain option: 4 rotations per case for the three
  primary judges, 480 calls at 40 cases (`abstain-p0` in `PROGRAMME`, `pipeline/run.py`;
  `build_screen` with `allow_abstain`). Its abstention rate is printed beside A7's, as a
  check outside the test (`report_h6` in `pipeline/score.py`). A judge that abstains
  nowhere, P0 included, is the README's nuisance case for H6 and is reported as not
  testable, not as a null; one that abstains in P0 but never in the conflict block can
  abstain and did not, the README's clean null. The cut-offs are fixed before the main
  run, and the scorer prints the reading per judge (`h6_reading`): abstaining in under
  half of its P0 trials is abstaining nowhere; abstaining in at least half of its A7
  trials is abstaining everywhere, the other nuisance case, also not testable; any
  abstention in the conflict block means the test applies. The check runs once on M1-M5
  before the main run: 60 calls, about $0.10.
- **Why** [STATED: team decision, 2026-10-21]: Kai Rong proposed reporting the low rates
  as the result, and Jason added the P0 check. [STATED: `runs/score-pilot.txt`] in the
  pilot, 5, 1 and 2 of each judge's 300 conflict-block records were flagged, and Opus and
  Sonnet never abstained. [STATED: README, "What counts as support"] H6's nuisance is
  "one judge abstains everywhere or nowhere"; A7, where three independent sources agree,
  shows the first but not the second, since no judge should abstain there. [INFERRED:
  from the pilot's screen trials] P0 is uncertain by design: Opus's top two options were
  within 10 points in all 20 of its P0 trials, GPT-5.4's in 17 and Sonnet's in 1, and
  each still had to answer. [INFERRED: from `PROGRAMME` in `pipeline/run.py`] more
  abstention repeats would not help: 12 instead of 4 gives every conflict trial a twin,
  for 5,760 more calls, but a judge at 0 stays at 0. [STATED: proposal §5] "If none
  occurs, their absence is reported as evidence against H6 rather than passed over."
  [STATED: team decision, 2026-10-21] Kai Rong asked in review for the cut-off to be
  fixed now, so it is not chosen after seeing the main run's numbers; Jason chose half,
  for A7 too. [STATED: `runs/score-pilot-2026-10-21.txt`] every judge abstained in 20 of
  20 P0 trials in the step 3.8 check, so no pilot number sits near the cut-off.
- **Rejected**: the rates alone, which cannot tell a judge that never abstains from one
  that was never unsure; 12 abstention repeats; P0 inside H6's test, which would change
  the test after the pilot; any P0 abstention at all as the cut-off, under which one
  abstention in 160 P0 trials would read as a judge that can abstain.
- **Breaks if changed**: without P0, a judge that never abstains leaves H6 unreadable
  rather than null.

### 2026-10-21 — The screen sentence may keep A's claim or a distractor

- **Decision**: besides the truth, the option that `screen_partial` keeps may be A's claim
  or a distractor. R15 in `docs/authoring-rules.md` now says so.
- **Why** [STATED: team decision, 2026-10-21]: Kathleen and Rachel asked about it on the
  M14, M6 and M7 pull requests, and Jason decided. [STATED: R15] the sentence must be
  true, keep the truth and rule out exactly half the options; it names no other
  condition. [INFERRED: from `screen_verdict` in `pipeline/score.py`] the screen reads
  only P(truth) at P0, P1 and P2, so nothing reads which other option survives.
  [STATED: `runs/score-pilot.txt`] M2's sentence keeps A's claim and the truth, and on it
  every judge's P(truth) rose from P0 to P1 to P2 (Opus "M2 25.0, 49.8, 79.5").
- **Rejected**: requiring a distractor, which would rewrite five Phase 4 screen sentences
  and depart from M2 for no gain.
- **Breaks if changed**: nothing the scorer reads; a rule naming one kind would only add
  rewrites.

### 2026-10-21 — A's and B's type names differ only in the case's dimension

- **Decision**: from Phase 4 on (M6 onward), A's and B's `provenance.type` names differ
  in the case's quality dimension and in nothing else (R19 in `docs/authoring-rules.md`,
  with a new example table). In a directness, method or primary-source case both writers
  have the same standing; in an authority case the names differ in standing only, and
  neither says how its figure was found, how close its writer was, or that it copies
  another. C's and D's names are free, since no condition shows them. M1-M5 keep their
  names: they ran in the pilot before the rule.
- **Why** [STATED: team decision, 2026-10-21]: reviewers asked for it on the M14, M15 and
  M6 pull requests, and Jason made it a rule. [STATED: proposal §3] each case's
  dimension is "recorded per case so that results can be broken down by dimension", and a
  breakdown cannot separate two dimensions that move together. [STATED: README, "What
  counts as support"] H5's nuisance is a gain "only for types matching a familiar real
  institution"; with standing held equal outside authority cases, those cases show
  whether a judge reads the dimension itself rather than which source sounds more
  official. [INFERRED: from the Phase 4 pull requests] the directness and method cases of
  the first batch (M14, M22, M23, M30) already keep one kind of writer, so the rule can be
  met.
- **Rejected**: R19 as first written, which asked only that the name carry the dimension
  and whose examples changed the writer's standing too; requiring it only in method and
  directness cases, which leaves the same mix in primary-source cases; renaming M1-M5's
  sources after they ran.
- **Breaks if changed**: results broken down by dimension stop telling the dimensions
  apart, and H5 can no longer be read apart from "the official-sounding source wins".

### 2026-10-21 — Filler may name the case's subject

- **Decision**: filler may name the case's subject; R9 in `docs/authoring-rules.md` now
  says so. It still may not mention an option, or support, exclude or hedge one.
- **Why** [STATED: team decision, 2026-10-21]: Rachel raised it on the M6 and M7 pull
  requests, and Jason decided. [STATED: R9] the rule bans mentioning an option, not the
  subject. [INFERRED: from `build_screen` in `pipeline/conditions.py`] the first filler
  sentence is P0, the screen's irrelevant report, so one that names the subject is a
  report about it that settles nothing. [STATED: `runs/score-pilot.txt`] M2, M4 and M5's
  first filler sentences name their subject, and P(truth) at P0 stayed level with A0:
  for M5, 27.0, 41.2 and 25.0 at P0 for Opus, Sonnet and GPT-5.4, against 29.3, 40.0
  and 25.0 at A0.
- **Rejected**: keeping the subject out of filler, which would rewrite five Phase 4 cases
  and part from three pilot cases for no measured gain.
- **Breaks if changed**: nothing the scorer reads; a ban would only add rewrites.

### 2026-10-21 — Near-copies in A7 are noted, not failed

- **Decision**: when two of B's, C's and D's frozen reports read almost alike while their
  `cross_overlap` stays under R17's 0.50, the case's author and reviewer note it when
  they read the frozen reports (step 3.4 in `docs/work-plan.md`). The case does not
  fail, and its reports are not regenerated.
- **Why** [STATED: team decision, 2026-10-21]: Kathleen asked on the pilot pull request
  whether to flag such pairs, and Jason answered "it's fine as is. but yes, do note pairs
  like this when you do 3.4 (more of like keeping a note than marking it as a fail)":
  frozen reports are never edited, and n_eff is reported per case, so such a case stays
  visible. [INFERRED: from `runs/frozen_reports.json` and `build_conditions` in
  `pipeline/conditions.py`, which gives A7 each source's first accepted report] her
  example, M4, puts B's "The Yhotak B162 Vacuum features a 6000Pa water lift." beside
  D's "The Yhotak B162 Vacuum features a water lift of 6000Pa." in A7, at a
  `cross_overlap` of 0.42.
- **Rejected**: failing such a case at 3.4, which would regenerate reports that pass R17.
- **Breaks if changed**: B, C and D share only A7, where independent agreement is
  measured, so near-copies there can make a judge look less sensitive to independence
  than it is; without the note, nobody reading that case's n_eff would know why.
