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
