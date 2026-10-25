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
  (Corrected on 2026-10-26: the judges' endpoints take no temperature, but a judge still
  answers one prompt almost alike; see that day's first entry.)
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

### 2026-10-22 — A screen sentence with bounds keeps both options equally far inside two

- **Decision**: a `screen_partial` that rules options out with a bound uses two bounds,
  and the two options it keeps sit the same distance inside them, so "pick the survivor
  nearest the bound" cannot find the truth. R15 in `docs/authoring-rules.md` now says so.
  M1, M3, M4 and M5 each had one bound with the truth as the survivor nearest it; each
  gained the missing bound and keeps the same two survivors, e.g. M3's "less than 15
  metres" is now "between 10 and 15 metres" (`cases/m3.py`). P1 is the authored sentence
  used as written, never reworded or frozen (`build_screen` in
  `pipeline/conditions.py`), so nothing else in those cases changes; the mock's key for
  M1 (`_SCREEN_TABLE` in `pipeline/llm.py`) follows the new sentence. Open cases that
  broke the rule were changed the same way in their pull requests. Decided after the
  pilot and before the main run.
- **Why** [STATED: team decision, 2026-10-22]: Kai Rong asked for it, as optional, on the
  M22 and M23 pull requests, and Jason made it a rule. [INFERRED: from `screen_verdict`
  in `pipeline/score.py`] the ordering check asks whether P(truth) rises from P0 to P1 to
  P2, and P1 is this sentence, so a cue that lifts P(truth) at P1 for any reason but the
  narrowing makes ordering easier to pass. [INFERRED: from the cases' `screen_partial`]
  a reader takes "less than 15 metres" to mean just under 15, and in all seven cases
  written with one bound (M1, M3, M4, M5, M15, M22 and M39) the truth was the survivor
  nearest it, so the cue always pushed toward the truth; every other case already kept
  both survivors equally far inside two bounds. [STATED: `runs/score-pilot.txt`] in the
  pilot, every judge's P1 in M1, M3, M4 and M5 was above 50, from 50.2 to 70.0, while
  M2, whose survivors sit 5 Wh inside each of two bounds, got 49.8 and 55.0 from Opus and
  Sonnet but 72.2 from GPT-5.4. That is a preview, so the rule rests on the design, not
  on these numbers.
- **Rejected**: leaving the pilot cases as they ran, as R19 did for their type names,
  which keeps a push toward the truth in four of the 40 screen sentences; one bound with
  the truth farther from it, which reverses the push instead of removing it.
- **Breaks if changed**: with one bound, the survivor nearest it draws belief for a
  reason other than the narrowing; where that survivor is the truth, P1 rises without
  the judge using the sentence, and the ordering check retains judges for it.

### 2026-10-22 — The main run goes in two stages, split by programme entry

- **Decision**: the main run (Phase 5 in `docs/work-plan.md`) runs in two stages, each
  programme entry into its own log as in the pilot (`judge --arms`). Stage 1 is
  generation and every entry that runs on all cases: `screen`, `conflict`, `agreement`,
  `abstain`, `abstain-p0`, and any entry added to `PROGRAMME` later that does not run on
  the ten-case subset. Stage 2 is the three subset entries, `long-conflict`,
  `long-agreement` and `ladder`, then the optional sub-experiments, once the key is
  topped up. The corpus is not split: stage 1 starts only when all 40 cases are merged.
- **Why** [STATED: team decision, 2026-10-22]: the course coordinator raised the API
  key's limit to $50 in all and tops it up again only after he sees that money spent, so
  Jason chose to spend it on a first stage and then ask for more. [STATED: `pipeline.run
  balance`, 2026-10-22] $38.93 of the $50 was left. [INFERRED: from each judge's cost per
  call by arm in `runs/score-pilot.txt` (HEALTH), applied to the calls `plan --cases 40`
  prints] at the pilot's measured rates stage 1 costs about $34.74 (generation $0.48,
  `screen` $2.40, `conflict` $13.78, `agreement` $11.02, `abstain` $6.11, `abstain-p0`
  $0.95, the last from `runs/trials-abstain-p0.jsonl`) and stage 2 about $5.11
  (`long-conflict` $2.39, `long-agreement` $0.48, `ladder` $2.24). The whole programme,
  about $39.84, would leave nothing for an entry that stops, and a stopped log
  cannot be resumed (the 2026-10-18 pilot entry). [STATED: README, "Arms"] stage 1 holds
  every condition behind H1-H6 and the confidence screen, while stage 2 holds the checks
  that need long reports or graded wording: the length arm tells token volume from
  redundancy, and "the wording ladder is H4's defence".
- **Rejected**: splitting the corpus and starting now on the merged cases, since rules
  still change while cases are written (the entry above changed four merged cases),
  `judge` requires every registered case to be frozen (`check_frozen` in
  `pipeline/run.py`), and real results would exist while cases are still unwritten;
  running the whole programme on what is left, which a stopped entry would leave
  unfinished.
- **Breaks if changed**: running a stage 2 entry in stage 1 uses up the money kept for an
  entry that stops; starting before all 40 cases are merged lets results exist while
  rules can still change.

### 2026-10-24 — A hedge carries at most three T1 cases

- **Decision**: up to three T1 cases may share a hedge, counted by its main word, so "is
  likely to", "it is likely that" and "is likely to have" are one hedge. An author picks
  a hedge with fewer than three cases, on `main` or in an open pull request, preferring
  one already in use to a new one, or another kind of cue. R16 in
  `docs/authoring-rules.md` and work-plan step 1.4 now say so. This replaces "pick the
  one used least" from the 2026-10-18 entry; varying the hedge stays.
- **Why** [STATED: team decision, 2026-10-24]: Kathleen asked whether the repeats were
  acceptable, with six hedges then on two or three cases each, and Jason decided.
  [STATED: R16] varying the hedge exists so that one phrase does not carry many T1
  cases; at three, losing one hedge relabels at most three of the 30 T1 cases, and "a T2
  case is a legitimate control". [STATED: `runs/frozen_reports.json`] in the pilot, all
  eight accepted rewordings of A in M2 to M5 kept a hedge, and two changed its word: M4's
  "is thought to be" came back as "A water lift of 4000Pa is suspected for the Yhotak
  B162 Vacuum." and M5's "is believed to have been" as "The water supply at Kestrel Court
  is thought to have been disconnected for 9 hours." So the reporter keeps the doubt
  rather than the word. [STATED: team decision, 2026-10-24] once every common hedge had a
  case, "least used" sent authors to new hedges that read as something other than doubt,
  which Kai Rong found reviewing the Phase 4 pull requests: "is expected to be" can read
  as a planned figure, so both claims can be true; "is considered to be" as an official
  ruling; "is taken as" as a set working value. [INFERRED: from `ATTRIBUTION_PHRASES` in
  `pipeline/reporter.py`] "It appears that" rewords easily to "apparently", which the
  linter rejects in a case but the reporter's checks do not catch in a rewording.
- **Rejected**: a new hedge for every case, which "pick the one used least" asks for once
  every common hedge has a case; no limit, which is how three of the four T1 pilot cases
  came to share one phrase.
- **Breaks if changed**: with no limit, one hedge can again carry many T1 cases, and the
  T1/T2 balance rests on whether the reporter keeps it; with one hedge per case, authors
  reach for hedges that break R1 or turn into hearsay.

### 2026-10-24 — B, C and D each reach the figure by their own route

- **Decision**: in A7, B, C and D must each reach the figure by their own route, so that a
  slip in one could not reach the others. Readings of one printed figure (a box, a
  datasheet, a register filled in from it) are one origin. For a figure an institution
  sets, such as a loan period, a deposit or a credit total, the fact is the decision
  itself: a record made where it was decided, or someone seeing the rule applied, is its
  own route; a copy of the governing document, or the minutes it was drafted from, is
  not. Each source's `why` names its route. `docs/authoring-rules.md`, "Checks no script
  performs".
- **Why** [STATED: team decision, 2026-10-24]: Jason asked for it reviewing M15 and M36,
  where B, C and D each read one printed figure. Kai Rong applied it reviewing the Phase
  4 pull requests and asked on M16, M17 and M24 how strict it is for a figure an
  institution sets, since every record of such a figure goes back to one decision. Jason
  decided. [STATED: README, "Measures, in order of weight"] normatively n_eff(A4) = 1,
  "three reports, one source", and n_eff(A7) = 3, so A7 must hold three sources;
  [STATED: README, "Two blocks, thirteen conditions"] A4 against A7 tests "true
  independence at equal report count". [STATED: `cases/m15.py`] "B, C and D each have
  their own origin so A7 does not read as one source three times".
- **Rejected**: any three different documents, which lets C and D pass on B's figure, so
  that A7 shows one source three times, which is A4's job; a separate measurement for
  every source, which a figure set by a decision cannot have.
- **Breaks if changed**: A7 no longer holds three sources, so n_eff(A7) = 3 is false by
  design, and A4 against A7 (H2) compares one source with one source.

### 2026-10-24 — Cases may share an attribute, not a scenario

- **Decision**: two cases may ask about the same attribute of different things, such as
  the battery capacity of a laptop (M2) and of a phone (M22). A case that repeats another
  case's scenario with new names takes a new topic. `docs/authoring-rules.md`, "Checks
  no script performs". M29, drafted as the number of passengers evacuated from a stalled
  funicular, repeated M38's question, the number of passengers evacuated from a stalled
  train, so M29 takes a new topic in its pull request.
- **Why** [STATED: team decision, 2026-10-24]: Kathleen listed similar pairs (M29 and M38,
  M25 and M31, M2 and M22, M4 and M20, M5 and M26) and asked whether any needed changing,
  and Jason decided. [STATED: `pipeline/prompt.py`] a judge prompt holds one
  "Question: {question}", so two cases never meet in a trial. [STATED: proposal §3, in
  the 2026-10-21 entry on type names] results are broken down by dimension, and a
  scenario repeated with new names makes one topic count twice in the results.
- **Rejected**: one topic per case, which would rewrite merged cases such as M2 and M22
  for no gain; keeping M29 as drafted.
- **Breaks if changed**: nothing the scorer reads; scenarios repeated with new names
  narrow the range of facts the results cover.

### 2026-10-24 — Authors count the hedges in use with tools/case_index.py

- **Decision**: R16 in `docs/authoring-rules.md` and work-plan step 1.4 send authors to
  `uv run python tools/case_index.py --all-branches`, which lists the cases on `main` and
  on every pull-request branch, with A's hedge, and then each hedge in use with how many
  of its three slots are left. The index is printed, never committed. It replaces the
  `grep` of the 2026-10-18 entry.
- **Why** [STATED: team decision, 2026-10-24]: Kathleen wrote the script, and Jason asked
  that R16 point to it once it was merged. [STATED: R16] most cases are drafted on
  pull-request branches, which a `grep` of `cases/*.py` cannot see, since it reads only
  the author's own branch. [STATED: `tools/case_index.py`] "The index is printed, not
  committed: it reads everyone's branches, so a saved copy goes stale with every push."
- **Rejected**: the `grep`, which misses every case drafted on another branch; a
  generated `docs/case-index.md` committed with the script, which goes stale with every
  push and would make every case pull request conflict on it, as they all do on
  `cases/__init__.py`.
- **Breaks if changed**: an author who checks only their own branch can pick a hedge that
  is already full on other branches, and one hedge ends up carrying more than three T1
  cases.

### 2026-10-25 — Neither A nor B is the question turned into a statement

- **Decision**: if A or B keeps the question's words in the question's order, with the
  answer filled in, while the other rewords it, the one that echoes the question is
  reworded. `docs/authoring-rules.md`, R13 and "Checks no script performs"; a reviewer's
  check, not linted. Applied the same day to M30, M31, M34 and M36 on `main` and to M6,
  M12, M13, M27 and M38 in their pull requests. M29 is taking a new topic, and M3, M4 and
  M5 keep their sentences: they ran in the pilot.
- **Why** [STATED: team decision, 2026-10-25]: Kai Rong and Kathleen raised it reviewing
  Phase 4 pull requests, as "R13 in spirit", and Jason decided to apply it to every case.
  [STATED: R13] the question's wording must not distinguish the competing pair, "so the
  question cannot lean toward one side"; the linter compares only the sets of words.
  [INFERRED: from `pipeline/prompt.py`, which puts "Question: {question}" above the
  reports] a report that is the question with the answer filled in reads as the direct
  reply to what the judge was asked, and in a T2 case it is the only difference left
  between A and B.
- **Rejected**: leaving it to the reporter, whose faithful rewordings keep a source's
  subject and verb, so the echo reaches the judge; rewording M3, M4 and M5 after they ran,
  as with their type names (2026-10-21).
- **Breaks if changed**: a case whose wrong claim echoes the question pulls the judge
  toward A for a reason no condition varies, and one whose true claim echoes pulls toward
  the truth; either moves that case's results by something other than provenance.

### 2026-10-25 — In a method case, A's hedge names no method

- **Decision**: in a method case, A's T1 cue may not name a way of finding the figure:
  not "is estimated to be", "is guessed to" or "is reckoned at" (R16 in
  `docs/authoring-rules.md`; work-plan step 1.4). An approximation stays allowed, since it
  says how exact a figure is, not how it was found (M35). M12 moves off "is estimated to
  be"; M20 had already moved to "is suspected to".
- **Why** [STATED: team decision, 2026-10-25]: Rachel raised it reviewing M12, and Jason
  decided. [STATED: R2] "Everything about who produced a source, how, and how reliable it
  is goes in `provenance`." [STATED: R19] "H5 asks whether a judge infers quality from a
  named source type alone": if A's sentence already names its method, the type names in
  X2 add less in method cases than in the other three dimensions. [STATED:
  `cases/m37.py`] the 3.4 check on A's rewordings, because "all of these would put the
  method into the content".
- **Rejected**: any hedge R16 lists, which lets a method case state its dimension in
  content; ruling out approximations too, which would rewrite M35 for a cue about
  precision rather than method.
- **Breaks if changed**: method cases carry their dimension in the sentence, so results
  broken down by dimension stop comparing like with like.

### 2026-10-25 — M3, M4 and M5 are reworded too

- **Decision**: M3's A and M4's and M5's B, each the question turned into a statement,
  are reworded like the other cases; this drops the pilot exemption in the entry above.
  The pilot's outputs in `runs/` stay as they are, and M1-M5 keep their type names
  (2026-10-21).
- **Why** [STATED: team decision, 2026-10-25]: Jason decided, since the main run
  generates every case's reports afresh. [STATED: `pipeline/run.py`] "Real outputs go to
  runs/ and are never overwritten: frozen reports and trial logs are evidence, so a step
  whose output exists refuses to start until the old file is moved."
- **Rejected**: keeping the pilot's sentences, which would leave three of the ten subset
  cases with a pull toward one side that no condition varies.
- **Breaks if changed**: nothing the pilot reported changes; only the main run reads the
  reworded sentences.

### 2026-10-25 — No content word is in two filler sets

- **Decision**: no content word is in two of a case's filler sets, counting forms such as
  "sits" and "sit" as one; the case's subject may be named in every set
  (`docs/authoring-rules.md`, R12 and "Checks no script performs"; a reviewer's check,
  not linted). Applied the same day to all 32 cases on `main`: M7, M30, M31 and M32
  first, then M1-M5 and eight cases with one or a few shared words (M14, M15, M22, M23,
  M28, M33, M34, M39). Every set keeps its word count, so R20's lengths hold. The eight
  proposals posted on open pull requests (M10-M13, M18, M19, M21, M29) already meet it.
- **Why** [STATED: `cases/m34.py`]: authors already held their own cases to it, "so the
  slots stay apart (R12)"; [STATED: team decision, 2026-10-25] Jason decided to clean
  every case on `main` to it before the main run. [INFERRED: from R12 and
  `build_conditions` in `pipeline/conditions.py`] the builder gives set *i* to slot *i*
  whichever source fills it, so a word two sets share lands on whichever two reports fill
  those slots: two reports of one source, which then show the dependence the opaque
  conditions hide, or two independent ones, which then look copied.
- **Rejected**: leaving single shared words such as "sit" or "lie" in eight cases, and the
  pilot cases' sets as they ran. [STATED: the 2026-10-15 entry on padded mock
  rewordings] "fixing filler there costs nothing: filler is added after rewording, so the
  paid reports are reused."
- **Breaks if changed**: a shared word links two reports in every trial of the case, a
  cue of shared origin that no condition controls, which in an opaque condition can fall
  on the two reports of the shared source.

### 2026-10-25 — A second filler pass counts every form of a word

- **Decision**: under the rule above, a word's other forms count as the word itself:
  "left" and "leave", "held" and "hold", "taken" and "take", "slotted" and "slot",
  "modelled" and "model", "lower" and "low", "crosses" and "cross". A second pass the
  same day swapped one word for each such pair the first pass had left on `main`: three
  in M1 and one each in M2, M3, M28 and M33. M4's "holds" and "holder" and M14's
  "building" and "built", related words rather than forms of one, were swapped too. Every
  set keeps its word count, so M1's sets stay at 80 words (`tests/test_conditions.py`).
- **Why** [STATED: team decision, 2026-10-25]: Jason decided to swap words in all seven
  cases before the main run, the two related-word pairs included. [STATED: the entry
  above] "a shared word links two reports in every trial of the case".
- **Rejected**: swapping words only in the five cases with forms of one word, and leaving
  M4's and M14's related words.
- **Breaks if changed**: as in the entry above, a shared word links two reports in every
  trial, a cue of shared origin that no condition controls.

### 2026-10-25 — The truth and A's claim sit equally far from the middle of the options

- **Decision**: in a case with numeric options, the truth and A's claim sit the same
  distance from the middle of the four options, as evenly spaced options give, so "pick
  the option nearest the middle" cannot find the truth (R8, `docs/authoring-rules.md`; a
  reviewer's check, not linted). The pre-run review applied it to M3, whose 11, 14, 17
  and 19 metres put the truth nearest the middle: 19 became 20. A distractor appears in
  no report, so no report changes. M1's 10, 15, 25 and 30 already meet it, since 15 and
  25 sit 5 either side of 20.
- **Why** [STATED: team decision, 2026-10-25]: Jason decided after the pre-run review of
  all 40 cases. [STATED: Kathleen's reviews of M14 and M21] there "closest to the mean"
  found the truth, and both cases were respaced. [STATED: R8] interior options are
  preferred so "avoid the extremes" is not a winning heuristic; the middle is the same
  kind of shortcut.
- **Rejected**: keeping M3's options as they ran in the pilot.
- **Breaks if changed**: a judge that leans to the middle of the range when evidence is
  thin picks the truth, a pull toward one side that no condition varies.

### 2026-10-25 — The pre-run review fixes M14's A and M1's C

- **Decision**: M14's A no longer keeps the question's words in the question's order: it
  reads "Dissipation carries heat away from the Halcyon substation cooling loop at 42
  kilowatts." M1's C now names a route of its own: the faculty's own record, entered when
  its board approved the module's weighting, not copied from the module brief. Both
  follow rules already decided, the question turned into a statement (2026-10-25) and B,
  C and D each reaching the figure by their own route (2026-10-24), which the pre-run
  review found these two cases had missed.
- **Why** [STATED: team decision, 2026-10-25]: Jason decided after the pre-run review.
  [STATED: the 2026-10-25 entry] in a T2 case the echo "is the only difference left
  between A and B", and M14 is T2. [STATED: the 2026-10-24 entry] "a copy of the
  governing document, or the minutes it was drafted from, is not" a route of its own, and
  M1's C was a "faculty-level record compiled from approved module briefs".
- **Rejected**: running M14 and M1 as they were.
- **Breaks if changed**: M14's results move toward A for a reason no condition varies,
  and M1's A7 holds two origins, not three, by its own record.

### 2026-10-25 — Stage 1's judge entries run in three lanes

- **Decision**: stage 1's five judge entries run as three processes at once, each entry
  still into its own log: `conflict`; `agreement`, then `abstain-p0`; `screen`, then
  `abstain`. An entry starts only if `balance` covers its cost plus 10% after keeping
  back what the running entries still need plus 10%, and nothing new starts once any
  entry stops. Each process keeps the runner's pace of 18 calls a minute
  (`pipeline/llm.py`) and its retries, unchanged. Generation and stage 2 are not
  affected.
- **Why** [STATED: team decision, 2026-10-25]: Jason chose three lanes over one entry at
  a time, and no change to the retries. [INFERRED: from `plan --cases 40` and the limiter
  in `pipeline/llm.py`] one process at 18 calls a minute takes about 16.4 hours for stage
  1's 17,760 judge calls; three lanes take about 6.7, the time `conflict` alone needs, so
  a fourth lane would save nothing. [INFERRED: from `judge_all` in `pipeline/run.py` and
  `OpenRouterBackend`] a call still failing after five tries, about 30 seconds of
  backoff, stops its entry, and a stopped log cannot be resumed, so the shorter the run,
  the fewer outages it can meet. [STATED: OpenRouter's documentation, "API rate limits"]
  paid models have "no platform-level request cap"; the 20 a minute that the limiter's
  comment cites is the cap on free models.
- **Rejected**: one entry at a time, as in the pilot (2E), which leaves the run exposed
  to a stop for about 16 hours; a faster pace per process or a longer retry window, which
  would change the pipeline's code during the main run.
- **Breaks if changed**: no log changes, since each entry's trials are built the same way
  in any order; only the hours the run is exposed to a stop change.

### 2026-10-25 — The main run's frozen reports are read before judging, by Jason

- **Decision**: for the main run, Jason reads all 40 cases' frozen reports (step 3.4 in
  `docs/work-plan.md`: hint, same whole, no leaks, near-copies in A7) before any judging,
  and relabels T2 any T1 case whose hint did not survive before judging starts. Each
  case's author and reviewer then check his summary for their case while judging runs.
- **Why** [STATED: team decision, 2026-10-25]: Jason decided, so judging can start the
  same day. [INFERRED: from `build_conditions` in `pipeline/conditions.py` and the record
  fields in `pipeline/judge.py`] every trial record stores the case's `difficulty_tier`
  as it was at judging time, so a relabel after judging would leave the logs with the old
  tier.
- **Rejected**: each author and reviewer reading their case before judging, as in the
  pilot, which would hold judging until all five members had read.
- **Breaks if changed**: a relabel made after judging disagrees with the tier stored in
  that case's trial records.

### 2026-10-26 — The judges' endpoints take no temperature, so each runs at its provider's default

- **Decision**: the runner sends every judge call with temperature 0 (`run_trials` in
  `pipeline/judge.py`), but none of the endpoints OpenRouter lists for Claude Sonnet 5,
  GPT-5.4 or Claude Opus 5 takes a temperature, so the 0 is most likely dropped and each
  judge runs at its provider's default. The judges still answer one prompt almost alike:
  six identical calls on 2026-10-26 gave one answer six times (Sonnet) and five times
  (Opus and GPT-5.4), the answer the main run had logged for that prompt. Across days
  they drift a little: the A0 prompts the pilot and the main run share, six days apart on
  the same providers, got the same decision in 22 of 24 pairs for each judge. No scoring
  changes. The equivalence rater, also Claude Sonnet 5, is sent temperature 0 the same
  way (`rate` in `pipeline/reporter.py`). The README, `docs/methods.md` and the code's
  comments now say this, and the write-up reports it as a departure from the proposal's
  "Judging runs at temperature 0" (§3).
- **Why** [STATED: `pipeline/run.py`, `cmd_probe`]: "OpenRouter drops unsupported
  parameters silently, so a null is an answer." [STATED:
  `runs/main/probe-2026-10-26.json`] no endpoint of the three judges lists `temperature`
  among its parameters, while every endpoint of the reporter and the auxiliary models
  does; the six repeats per judge are in the same file. [INFERRED: from the A0 records of
  `runs/trials-agreement.jsonl` and `runs/main/trials-agreement.jsonl`, whose prompts are
  identical: same question, options, template and system prompt] 13, 11 and 17 of the 24
  pairs (Opus, Sonnet, GPT-5.4) are the same text, and P(truth) moves by 1.0, 2.7 and 0.5
  points on average.
- **Rejected**: saying the judges run at temperature 0, which the endpoint lists
  contradict; dropping temperature from the request, which changes nothing the judges
  receive and would change the code before stage 2.
- **Breaks if changed**: nothing in the results, since every judge call ran the same way.
  A comparison across days, as between stage 1 and stage 2, carries the small drift above.

### 2026-10-26 — Stage 2 runs one entry at a time: the ladder, then long-agreement, then long-conflict

- **Decision**: stage 2 waits for the coordinator's top-up. Jason asks for the $25 left
  of the proposal's $75, with $10 as the least that covers stage 2 and the optional
  sub-experiments. Stage 2 runs `probe` first, then its three entries one after another,
  each into its own log in `runs/main/`: `ladder`, then `long-agreement`, then
  `long-conflict`. Before each entry, `balance` must cover its cost plus 10%, and nothing
  starts after an entry stops. Its results are read twice: with all ten subset cases, and
  without M3 and M38, the two echo cases among them (`tools/tally.py --without`).
- **Why** [STATED: team decision, 2026-10-26]: Jason agreed to the order and to reading
  the results both ways. [INFERRED: from `plan --cases 40` and the runner's pace of 18
  calls a minute] stage 2's 2,520 judge calls take about 2.3 hours, so lanes would save
  little, and one entry at a time keeps a stopped entry from leaving the others to spend.
  [STATED: proposal §4.1] the ladder runs in the main programme "because it is H4's only
  defence against its most obvious alternative explanation"; [STATED: proposal §5] "the
  length arm is the first thing trimmed". [STATED: `runs/main/reading-3.4.md`] in M3 and
  M38, among others, the reporter rewrote one of A's reports as "the question turned into
  a statement". [INFERRED: from `build_entry` in `pipeline/run.py` on
  `runs/main/frozen_reports.json`, 2026-10-25] all 2,520 trials build, and every long
  report is inside 88-96 words.
- **Rejected**: three lanes, as in stage 1, a decision made for stage 1 only (the
  2026-10-25 entry); the proposal's table order, with the length arm first.
- **Breaks if changed**: if the length arm runs first and costs more than planned, the
  ladder may go unfunded; read only with the echo cases in, two of the ten subset cases'
  pull toward A could pass for an effect of length or wording.

### 2026-10-26 — The optional sub-experiments are entries of their own, built in a second folder

- **Decision**: the four optional sub-experiments are entries in a list of their own,
  `OPTIONAL` in `pipeline/run.py`. `judge --arms` selects them by name, but they are never
  part of the default run or of `plan`'s totals. Each one fixes in the code its cases,
  its arm label, its report length and, where it differs, its reasoning setting, so its
  trials never share an id or a scorer cell with the main programme's. `generate` and
  `judge` take `--cases`, a list of case ids, for the wording-robustness rerun, which
  writes to its own folder, `runs/robustness/`. A test checks that the main programme
  still builds the trials and prompts that stage 1 judged and stage 2 will judge
  (`tests/test_run.py`). The code is written on the branch `optional-arms`, in a second
  folder made with `git worktree`, so the main folder never switches branch, and it
  merges into `main` only when Jason agrees. The sub-experiments run in the proposal's
  order (reasoning, wording robustness, cross-check, n_eff at long length), each only if
  `balance` covers it plus 10%. Each one's design is an entry below.
- **Why** [STATED: team decision, 2026-10-26]: Jason agreed. [STATED: `pipeline/judge.py`]
  a trial's id is `f"{trial['case_id']}_{trial['condition']}_{trial['arm']}_run{run_index}"`,
  and the scorer's cells are judge x arm x case x condition (`pipeline/score.py`), so a
  reasoning-on trial labelled `short` would share both with the main run's. [INFERRED:
  from `cmd_judge` in `pipeline/run.py`] a run reads the code and `cases/` from the folder
  it starts in, so switching that folder's branch during stage 2 would change what stage
  2 runs. [STATED: proposal §6] "They run in priority order, and the write-up states which
  were executed and at what scale."
- **Rejected**: adding them to `PROGRAMME`, which would change `plan`'s totals and the
  default `judge` run; a branch in the main folder; choosing an entry's cases with
  `--cases` at run time, which leaves its trial set out of the code.
- **Breaks if changed**: an optional trial labelled like a main one is scored into the
  main run's cells; without the test, a change to the main programme's trials could pass
  unseen.

### 2026-10-26 — The reasoning comparison: Claude Sonnet 5 on M1 and M2, both modes judged on one day

- **Decision**: Claude Sonnet 5 judges X1, X3 and X5 of M1 and M2, short and long, 12
  repeats, once with reasoning off as in the main run (`{"enabled": false}`) and once with
  reasoning on at a budget of 2,000 thinking tokens (`{"max_tokens": 2000}`): 288 calls in
  four entries, `reasoning-off-short`, `reasoning-off-long`, `reasoning-on-short` and
  `reasoning-on-long`, both modes on the same day. A reasoning-on call may use 2,700
  tokens, the budget plus the 700 an answer always has, and waits up to 150 seconds.
  Every record keeps the thinking text the provider returns (`reasoning_text`). The
  traces are coded by this rule, fixed before any of the arm's traces exist:
  - each trace gets one code, from its text alone: *none* when there is no thinking text;
    *noticed* when, before the answer, it says that two of the reports come from one
    source, repeat one another or are not independent, in any words, a restated note
    included; *not noticed* otherwise, a trace that only says two reports agree included;
  - two coders apply the rule separately, Claude and a second coder given only the texts
    and the rule. Their disagreements are listed and Jason settles them, and the codes
    are committed before they are crossed with decisions;
  - the reading crosses the code with the decision, per condition and length: how many
    traces noticed, and how many of those chose the independent report.
- **Why** [STATED: proposal §4.1]: "crossing reasoning mode with report length on X1, X3
  and X5 for two cases, one model in both modes", and "Traces are logged and read for
  whether the model mentions the shared source before deciding, which separates not
  noticing the dependence from noticing it and not acting on it." [STATED: team decision,
  2026-10-26] Sonnet, M1 and M2, and a trace rule fixed before reading: Jason agreed.
  [STATED: `pipeline/run.py`] Sonnet is one of the two `LENGTH_JUDGES`, so it judges long
  reports in the main run too, and its numbers are not stuck at 100 as GPT-5.4's are
  (`runs/main/tally-stage1.txt`). M1 and M2 are the first two cases, one T2 and one T1,
  and neither is an echo case (`runs/main/reading-3.4.md`). [STATED:
  `runs/main/probe-2026-10-26.json`] with reasoning on, Sonnet returned its thinking text
  as `reasoning`; two identical calls thought for 0 and 180 tokens and gave different
  numbers; the calls cost $0.0012 to $0.0037. Those two traces were read before this rule
  was written; they are not part of the arm. [STATED: the first entry of 2026-10-26] the
  judges' answers drift a little between days, so the main run's trials, judged on other
  days, are not reused as the off half. [STATED: OpenRouter's documentation, "Reasoning
  tokens"] "`max_tokens` must be strictly higher than the reasoning budget".
- **Rejected**: reusing the main run's trials as the off half, which compares across
  days; GPT-5.4, whose numbers mostly sit at 100 and whose output tokens cost more; a
  larger budget, which caps thinking but cannot force it.
- **Breaks if changed**: with the off half from another day, a difference between modes
  may be drift; a trace rule written after reading can be bent toward a result.

### 2026-10-26 — The wording-robustness rerun makes a second report set for M1 and M2

- **Decision**: `generate --cases M1,M2 --out runs/robustness` makes a second,
  independent report set for M1 and M2, for all four sources, since the condition
  builder needs C and D even where only A and B are shown. Jason reads it as in step 3.4
  before judging, and a T1 case whose hint is lost counts as T2 in this rerun. Then
  `judge --cases M1,M2 --arms conflict --out runs/robustness` judges the conflict block
  with all three judges and 12 repeats, 360 calls. It is scored on its own, since its
  trial ids repeat the main run's.
- **Why** [STATED: proposal §5]: "The main run uses one generated report set. A
  wording-robustness check that regenerates the reports for two cases and re-judges the
  conflict block is one of the ranked optional sub-experiments in Section 6". [STATED:
  team decision, 2026-10-26] Jason agreed, with the reading before judging. [INFERRED:
  from `check_frozen` in `pipeline/run.py` and `build_conditions` in
  `pipeline/conditions.py`] judging needs every source of a case frozen, and every repeat
  builds A7 from C and D.
- **Rejected**: regenerating only A and B, which the builder cannot use; judging the old
  reports again beside it on the same day, which doubles the calls.
- **Breaks if changed**: judged without the reading, a lost hint would count among T1's
  results.

### 2026-10-26 — The confidence cross-check runs the screen on the auxiliary models, answering by number

- **Decision**: Qwen 3.6 27B and Llama 4 Maverick judge the screen's P0, P1 and P2 at its
  four rotations on the first 15 cases in corpus order (M1-M5, M6, M14, M22, M30, M38 and
  M7-M11): 360 calls, entry `cross-check`. Their prompt asks for the option's number as
  the answer and for "p" keyed by number (`pipeline/prompt.py`), so the token
  probabilities at the answer's digit cover the same four labels as the stated "p". Qwen
  is sent reasoning off; Llama, whose endpoints take no reasoning parameter, is sent none
  (`AUXILIARY_REASONING` in `pipeline/run.py`). How stated and token probabilities
  compare is read after the run.
- **Why** [STATED: proposal §4.1]: "Verbalized probabilities are compared against
  option-index token probabilities on the two auxiliary models, which never judge a
  main-arm trial." [STATED: team decision, 2026-10-26] the screen on 15 cases: Jason
  agreed. [STATED: `runs/main/probe-2026-10-26.json`] with reasoning off, Qwen answered on
  Reka with five alternatives per token; sent no reasoning parameter, it spent its 16
  tokens thinking, as in `runs/main/probe.json`. [INFERRED: from `build_screen` in
  `pipeline/conditions.py`] the screen runs from an irrelevant report to one that names
  the answer, so stated confidence spans the scale, and 15 cases x 3 levels x 4
  rotations x 2 models is the proposal's 360.
- **Rejected**: answering with the option's text, whose first tokens two options can
  share; a substitute for Qwen, no longer needed.
- **Breaks if changed**: with text answers, an answer's token probability is spread over
  several tokens and is no longer a distribution over the four options.

### 2026-10-26 — n_eff at long length: Sonnet on nine subset cases, with A0 from the short arm

- **Decision**: after stage 2, Claude Sonnet 5 judges A4, A6 and A7 with long reports on
  the subset cases except M38, 6 repeats: 162 calls, entry `long-neff`, arm `long`. The
  scorer then computes n_eff on the long arm from those cells and stage 2's long A1, with
  A0 taken from the short arm (`report_neff` in `pipeline/score.py`). M38 is left out
  because its A7 cannot be built long: its C report comes to 87 words in every slot, one
  under the 88-word floor (`check_long_lengths` in `pipeline/conditions.py`).
- **Why** [STATED: proposal §6]: the index at long length "requires the index to be
  computable at short length, which requires at least one judge to pass the confidence
  screen". [STATED: `runs/main/tally-stage1.txt`] Sonnet's index has a value at ceiling in
  1 of its 40 cases, GPT-5.4's in 35. [STATED: team decision, 2026-10-26] Sonnet only,
  after stage 2, with A0 from the short arm: Jason agreed. [INFERRED: from
  `build_conditions` in `pipeline/conditions.py`] A0 shows no reports, so it has no
  length, and A7 is the only one of the three that stage 2 never builds long and checks.
- **Rejected**: both length judges, where GPT-5.4's index would mostly read "at
  ceiling"; M38 with an 87-word report; new filler for M38, which would change the case
  and stage 2's long trials.
- **Breaks if changed**: an A7 report off the band lets length stand in for provenance in
  the one condition with three sources.

### 2026-10-26 — H5's familiar-institution check codes the type names before the split

- **Decision**: H5's nuisance check splits the 40 cases by one rule, applied to A's and
  B's type names alone. A case counts as *familiar institution* when B's name names an
  organisation of a kind that exists in the real world with public or official standing
  (a government body, a council or other public authority, a regulator, a standards or
  consumer-protection body, an emergency service, an accredited laboratory, or a
  university's, college's or library's own office) and A's name does not name that
  organisation. A name that names only a person or role, only a document or only a
  company does not count, and neither does an organisation both names share. Eight cases
  count: M4, M5, M7, M10, M15, M25, M27 and M33. A second reading also counts a company
  that only B names, which adds M2 and M34. For each judge, the gain counts as appearing
  without a familiar institution when, among the other 32 cases (30 on the second
  reading), more cases gain right decisions from X1 to X2 than lose them, at a one-sided
  sign-test p below 0.05; then the nuisance does not hold for that judge.
  `tools/tally.py --only` and `--without` give each group's counts
  (`runs/main/tally-stage1-h5.txt`).
- **Why** [STATED: team decision, 2026-10-26]: Jason decided that we do the check
  ourselves rather than ask a volunteer. [STATED: README, "What counts as support, fixed
  before any data"] the nuisance holds if "the gain appears only for types matching a
  familiar real institution". [INFERRED: from R19 in `docs/authoring-rules.md`] from M6
  on, a directness, method or primary-source case gives A and B the same writer, so a
  familiar institution can set B apart mainly in authority cases. The codes were fixed
  before the split was computed: Claude coded the names, and a second coder given only
  the names and the rule, with no results, made the same 40 codes and the same two
  company flags.
- **Rejected**: asking a volunteer; a keyword list, which would be chosen with the names
  in view; reading the split by eye, without a fixed test.
- **Breaks if changed**: a rule chosen after the split is seen can be bent toward either
  answer.
