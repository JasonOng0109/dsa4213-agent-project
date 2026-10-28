# The optional sub-experiments: what they found so far

The four optional sub-experiments ran on 2026-10-28, after stage 2, in the proposal's
order (`docs/decisions.md`, 2026-10-26). This report says what each found so far. Two
parts wait on a person: the reasoning traces are coded only after the trace rule is
reviewed, and the wording-robustness rerun is judged only after Jason reads its new
reports. Every number comes from one of two files in `runs/main/`:

| File | Made by |
|---|---|
| `score-optional.txt` | `uv run python -m pipeline.score --show-excluded runs/main/trials-*.jsonl`, over all twelve judge logs |
| `crosscheck.txt` | `uv run python -m tools.crosscheck runs/main/trials-cross-check.jsonl` |

`score-optional.txt` repeats every stage 1 and stage 2 cell of `score-stage2.txt`
unchanged; Sonnet's long-arm cells gain the rows A4, A6 and A7.

## In short

Reasoning changed nothing Sonnet decided: with thinking allowed, it chose as it did
without, in every trial, and it thought in only 32 of 144 trials. Both auxiliary models'
stated numbers rise from an irrelevant report to one that names the answer, as their
token probabilities do, and the two agree closely trial by trial; given only an
irrelevant report, though, their tokens lean on one option far more than their stated
numbers. With long reports Sonnet still counts three copies of one source and three
independent sources alike, as about two sources each.

## What ran

| Entry | Judge | Trials | Cost |
|---|---|---|---|
| `reasoning-off-short`, `reasoning-off-long` | Sonnet, reasoning off | 144 | $0.25 |
| `reasoning-on-short`, `reasoning-on-long` | Sonnet, a 2,000-token thinking budget | 144 | $0.29 |
| robustness: `generate --cases M1,M2` | the reporter | 96 calls | about $0.07 |
| `cross-check` | Qwen 3.6 27B and Llama 4 Maverick | 360 | $0.05 |
| `long-neff` | Sonnet | 162 | $0.36 |

They ran from 01:00 to 01:49, one entry at a time, and none stopped. The judge costs are
the sum of each log's call costs; generation records none, so its cost is the fall in
the key's balance while it ran. No call failed. Sonnet stayed on its pinned provider;
the auxiliary models are not pinned, and Qwen answered on Alibaba and Reka, Llama on
DigitalOcean and Parasail. Of the 360 cross-check trials, 4 of Qwen's named no option and
5 stated probabilities whose sum was out of range; they are left out below.

## Reasoning on and off (Sonnet, M1 and M2)

Both modes judged X1, X3 and X5 of M1 and M2, short and long, 12 repeats, on the same day.

**Decisions: no change.** In every cell, in both modes, X1 and X3 were right in 0 of 12
trials and X5 in 12 of 12. Every wrong answer named A's claim.

| P(truth), M1 · M2 | off, short | on, short | off, long | on, long |
|---|---|---|---|---|
| X1: nothing disclosed | 20.1 · 19.8 | 20.4 · 20.0 | 18.8 · 20.6 | 17.8 · 20.4 |
| X3: dependence stated | 28.2 · 30.8 | 29.2 · 33.7 | 23.6 · 26.1 | 30.8 · 30.4 |
| X5: dependence and quality | 65.2 · 64.6 | 67.5 · 67.1 | 69.4 · 72.1 | 68.3 · 72.9 |

**Thinking was rare.** A budget caps thinking but cannot force it (the reasoning entry's
"Rejected" field), and Sonnet thought in 32 of the 144 reasoning-on trials: 14 of the 24
X3 trials with long reports, 6 of 24 with short ones, and 8 and 4 of X5's, never in X1.
Averaged over each cell's 24 trials, that is 82 thinking tokens in X3 with long reports,
32 with short ones, and 19 and 10 in X5. With so little thinking, the on/off contrast is
weak, and it shows only in X3's P(truth), which is higher with reasoning on in all four
cells, by 1 to 7 points.

**The traces wait for the rule's review.** By the rule fixed before the run, the 112
traces with no thinking text code as *none*. The other 32 go to two coders, Claude and a
second coder given only the texts and the rule. The rule's reading crosses each code with
the decision: since no X3 trial in either mode chose the independent report, the coding
can only tell whether Sonnet missed the shared source or noticed it and still followed
the two reports.

## The confidence cross-check (Qwen 3.6 27B and Llama 4 Maverick)

The two auxiliary models judged the confidence screen's P0, P1 and P2 at four rotations
on the first 15 cases, answering by option number. The token probability of an option is
read at the answer's digit.

| | Llama 4 Maverick | Qwen 3.6 27B |
|---|---|---|
| Stated P(truth), P0 → P1 → P2 | 27.9 → 44.8 → 100.0 | 25.0 → 47.9 → 100.0 |
| Token P(truth), P0 → P1 → P2 | 34.5 → 44.9 → 100.0 | 25.6 → 48.7 → 99.1 |
| Page's test, stated and token | p below 0.0001 for both | p below 0.0001 for both |
| Stated against token P(truth), trial by trial | Spearman 0.83 | Spearman 0.81 |
| P0: the largest stated p, the largest token probability | 76.0, 91.4 | 25.0, 77.0 |

Both ways of reading confidence order the screen's three levels, and they rank trials
much alike. They part where nothing points to the answer: shown an irrelevant report,
Qwen states 25 on every option, yet its tokens put 77% on one number on average; Llama's
largest stated number averages 76, its tokens' 91. In every trial the answer was the number its
tokens made most likely. No test was fixed for this comparison, so it is a description.

## n_eff at long length (Sonnet, nine subset cases)

Sonnet judged A4, A6 and A7 with long reports on the subset cases except M38, whose A7
cannot be built long. The scorer computes n_eff from those cells and stage 2's long A1,
with A0 from the short arm. It is defined in all nine cases, none at ceiling. Short is
stage 1's value on the same nine cases.

| Median over the nine cases | Short | Long |
|---|---|---|
| A4: three reports of one source (should be 1) | 1.86 | 1.95 |
| A7: three independent sources (should be 3) | 1.79 | 1.97 |
| Extra credit for repetition (A4 − 1) | 0.86 | 0.95 |
| Credit for real independence (A7 − A4; should be 2) | 0.09 | −0.03 |
| Clawed back by "same source" (A4 − A6) | 0.23 | 0.47 |

With long reports, as with short ones, Sonnet treats three copies of one source and
three independent sources alike, both as about two sources. A4 is higher at long length
in 5 of the 9 cases, so length moves it in no consistent direction. The "same source"
note claws back about half a source, twice the short figure. The long cells were judged
on 2026-10-27 (A1) and 2026-10-28 (A4, A6, A7), the short ones on 2026-10-25, so the
comparison crosses days.

## Wording robustness (M1 and M2, a second report set)

`generate` froze a second, independent report set for all four sources of M1 and M2 in
`runs/robustness/`, and the runner's leak check is clean for both. A first reading for
Jason, by the step 3.4 checks: M2's hint survives in both of A's reports ("understood",
"thought"); every report of A and of B states its source's quantity; no two of A7's
reports read alike. One note: M2's D report came out word for word as B's own sentence,
which no judge sees here, since the rerun judges only the conflict block, where C and D
are not shown. Judging, 360 calls with all three judges, waits for Jason's reading.

## What is left

| Still open | Next step |
|---|---|
| The reasoning traces | Kai Rong reviews the trace rule (PR #55); then two coders code the 32 traces with text, Jason settles their disagreements, and the codes are committed before they are crossed with decisions |
| Wording robustness | Jason reads the new reports; then the conflict block is judged, 360 calls, and scored on its own |
