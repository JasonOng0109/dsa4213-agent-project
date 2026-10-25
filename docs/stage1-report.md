# Stage 1 of the main run: what it found

Stage 1 ran on 2026-10-25 on all 40 cases. This report says what it found, hypothesis by
hypothesis, and what is still to check. Every number comes from one of three files in
`runs/main/`, all read from the same five judge logs:

| File | Made by |
|---|---|
| `score-stage1.txt` | `uv run python -m pipeline.score --show-excluded runs/main/trials-*.jsonl` |
| `tally-stage1.txt` | `uv run python -m tools.tally runs/main/trials-*.jsonl` (counts and means over the 40 cases) |
| `tally-stage1-without-echoes.txt` | the same, with `--without M3,M9,M13,M23,M28,M38,M40` |

"P(truth)" is the probability a judge stated on the right answer, averaged over a
condition's trials. "Right" counts decisions that match the world truth. The README's
table "What counts as support, fixed before any data" decides what each result means;
this report only lines the results up against it.

## In short

The three judges count reports, not evidence. Three reports from one source raised their
belief as much as three independent sources did. When two reports from a weak source
disagreed with one from a strong source, every judge almost always sided with the two.
Saying that the two share a source moved belief but seldom the decision. Saying which
source is more reliable made every judge right in every trial. Naming each source's type
helped part of the way, more for some judges than others. No judge abstained where its
own numbers did not back its answer.

## What ran

| | |
|---|---|
| Cases | all 40: 30 T1, 10 T2. The reading before judging relabelled none (`runs/main/reading-3.4.md`) |
| Judges | Claude Opus 5, Claude Sonnet 5 and GPT-5.4, reasoning off, each on its pinned provider |
| Entries | agreement, conflict, abstain, abstain-p0 and screen |
| Trials | 17,760. 17,741 parsed cleanly, one did not parse, and no call failed |
| Cost | $36.78, against $34.74 planned (`docs/work-plan.md`, Phase 5) |

## Can we use the judges' stated numbers?

Yes, for all three. A judge's numbers count only if its P(truth) rises from an irrelevant
report (P0) to one that rules out two options (P1) to one that names the answer (P2).
All three passed on the 40 cases, with rank correlations of 0.95 to 0.99 and p below
0.0001 (Page's test).

One limit: GPT-5.4 put 100 on one option in 62% of its agreement-block answers. Its
independence index (below) therefore mostly reads "at ceiling", a bound rather than a
value. Its decisions are not affected.

## Results by hypothesis

### H1: repeating one source raises confidence, and can beat a better source

| | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| P(truth): one report (A1) → three reports of one source (A4) | 77.4 → 93.8 | 76.4 → 95.2 | 91.1 → 99.5 |
| Cases where it rose | 40 of 40 | 40 of 40 | 40 of 40 |
| Right when two weak reports face one strong one (X1) | 1 of 480 | 2 of 480 | 26 of 480 |

**Against the table: Support.** The rise appears in every case and in all three domains.
The table's other nuisance, a rise only when the repeated reports sit in particular
positions, cannot arise in A4, where the one source fills all three positions. In X1 the
two weak reports won wherever the strong one was placed. GPT-5.4 rises least when the
truth is the first option, because one report already gets 98.2 there.

### H2: the rise comes from repetition and separate messages, not agents' names

| P(truth) | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| A1: one report | 77.4 | 76.4 | 91.1 |
| A2: three reports in one message | 81.2 | 84.2 | 96.8 |
| A3: three separate messages | 91.4 | 94.8 | 99.6 |
| A4: three named agents | 93.8 | 95.2 | 99.5 |
| A7: three independent sources | 94.4 | 95.8 | 99.5 |

A3 and A4 are above A2 in 39 or 40 of the 40 cases, and on average within 0.4 to 2.4
points of each other. For Opus and Sonnet the biggest step is splitting the reports into
separate messages (A2 → A3). GPT-5.4 is near its ceiling from A2 on.

**Against the table: Support, at short length.** Still to check, in stage 2: whether the
A1 → A2 rise is larger with long reports, which would point to token volume.

### How many sources the judges think they saw (n_eff)

n_eff is the independence index: how many independent sources a judge acted as if it saw.
Three reports of one source should count as 1 (A4), and three independent sources as 3
(A7). The values are medians over the cases.

| | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| A4 (should be 1) | 1.64 | 1.88 | at ceiling in 35 of 40 cases |
| A7 (should be 3) | 1.69 | 1.98 | |
| Extra credit for repetition (A4 − 1) | 0.64 | 0.88 | |
| Credit for real independence (A7 − A4; should be 2) | 0.05 | 0.09 | |
| Clawed back by "same source" (A4 − A6) | 0.40 | 0.29 | |

Opus and Sonnet treat three copies of one source and three independent sources almost
alike: both count as less than two sources. Stating that the reports share a source claws
back about a third of a source. For Opus, most of the fall in P(truth) from A4 to A6
already comes with the opaque source ID (A5), before any dependence is stated: 93.8 →
88.3 → 85.6.

### H3: "these two share a source" moves belief, not the decision (primary)

| | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| P(truth): X1 → X3 (dependence stated) | 25.7 → 41.2 | 20.2 → 32.5 | 22.6 → 29.9 |
| Cases where it rose | 40 of 40 | 40 of 40 | 37 of 40 |
| Right: X1 → X3, of 480 | 1 → 63 | 2 → 8 | 26 → 27 |

**Against the table: Support for Sonnet and GPT-5.4**: belief moved toward the truth and
decisions did not. For Opus, belief moved and some decisions moved too, 63 of 480. All 63
are in T1 cases, spread over 14 of them, where A's reports still sound unsure. In T2
cases no judge changed a single decision, yet belief rose there too. So the belief shift
appears with or without the hedge, but Opus's few changed decisions appear only with it.
The table's nuisance column, "movement only where a mild content cue survives", is the
check to report this under.

### H4: "this source is better" changes the decision (primary)

| Right, of 480 | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| X3: dependence stated | 63 | 8 | 27 |
| X4: quality stated | 480 | 480 | 480 |
| X5: both | 480 | 480 | 480 |

**Against the table: Support, so far.** Still to check, in stage 2: X4 and X5 say outright
which source is the primary record, so a judge may just be following the instruction.
The ladder repeats X5 with weaker wording ("somewhat", "considerably", "far more
reliable"). If the weaker wording also changes decisions, the judges are weighing
evidence. If only the strongest does, the table counts it as the nuisance.

### H5: judges read quality from a source's named type (secondary)

| | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| Right: X1 → X2 (each source's type named), of 480 | 1 → 403 | 2 → 193 | 26 → 283 |
| Cases with more right decisions | 38 of 40 | 24 of 40 | 33 of 40 |

**Against the table: Support, varying by judge.** Still to check, by reading the cases:
whether the gain comes only where a type name matches a familiar real institution.

### H6: forced choice hides belief, and "cannot be determined" is taken where the numbers do not back the answer (primary)

- Few forced-choice answers were unbacked by the judge's own numbers: 30 (Opus), 3
  (Sonnet) and 7 (GPT-5.4) of each judge's 2,400 conflict-block records.
- Opus and Sonnet abstained when shown one irrelevant report (P0: 160 of 160 and 153 of
  160), so they can abstain. But they never abstained in the conflict block. By the
  cut-offs fixed before the main run, that is a clean null.
- GPT-5.4 abstained in 9 of its 800 conflict-block trials, all in X1, and in none of the
  unbacked records. Its test applies and gives +0.00.

**Against the table: no support for any judge.** The proposal says the write-up shows one
answer in full whose own numbers favour another option. Ten such answers exist (nine in
the screen, one in the abstention arm), none in the conflict block.

## Checks already done

- **The seven echo cases.** In seven cases, one of A's reports came out as the question
  turned into a statement (`runs/main/reading-3.4.md`). With those cases left out, every
  direction above holds and the counts barely move. For example, X2 is right 350 of 396
  (Opus), 156 of 396 (Sonnet) and 243 of 396 (GPT-5.4).
- **Discrimination**, reported beside the screen: under its first rule, which is no longer
  applied, Sonnet and GPT-5.4 would have been excluded. Here a wrong answer is almost
  always the two agreeing reports' claim, so it mostly shows how sure a judge is when it
  follows them (`docs/decisions.md`, 2026-10-21).

## Notes for the write-up

- In the screen's P1, where the report leaves two options, the judges seem to lean toward
  the first of the two listed. It shows in the repeat that lists the truth last: eight of
  the ten answers that contradict their own numbers are there, each naming the first
  option while its numbers favour the truth. The screen reads P(truth), not decisions, so
  its verdict is unaffected.
- Two of the three judges come from one developer, and the run uses one generated set of
  reports. The proposal states both as limits (§5 and §6). The optional wording-robustness
  rerun would test the second.

## What stage 1 leaves for later

| Still open | Answered by |
|---|---|
| H2: is the A1 → A2 rise larger with long reports? | stage 2, `long-agreement` |
| H3 and H4 with long reports | stage 2, `long-conflict` |
| H4: following an instruction, or weighing evidence? | stage 2, `ladder` |
| H5: only for familiar institutions? | reading the 40 cases' type names |
| Reasoning on and off; wording robustness; stated against token probabilities; n_eff with long reports | the optional sub-experiments, if built and funded |
