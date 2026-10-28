# The optional sub-experiments: what they found so far

The four optional sub-experiments ran on 2026-10-28, after stage 2, in the proposal's
order (`docs/decisions.md`, 2026-10-26). This report says what each found so far. The
same day, an independent review of PR #55, made in Kai Rong's place, checked them, and two
decisions came of it (`docs/decisions.md`, 2026-10-28): the trace rule settles its edge
cases and blinds its coders, and the cross-check reads M12 in M10's place. Then the
wording-robustness rerun was judged, and the 32 reasoning traces with thinking text were
coded by the settled rule.

Every result comes from one of the files below. The commands name their logs in the
order `runs/main/trials-*.jsonl` lists them, since the scorer's output follows that order.
The run times and the generation cost were read off the runs as they went.

| File | Made by |
|---|---|
| `runs/main/score-optional.txt` | `uv run python -m pipeline.score --show-excluded runs/main/trials-{abstain-p0,abstain,agreement,conflict,cross-check-m12,cross-check,ladder,long-agreement,long-conflict,long-neff,reasoning-off,reasoning-on,screen}.jsonl`, all thirteen judge logs |
| `runs/main/crosscheck.txt` | `uv run python -m tools.crosscheck runs/main/trials-cross-check.jsonl runs/main/trials-cross-check-m12.jsonl` |
| `runs/robustness/score.txt` | `uv run python -m pipeline.score --show-excluded runs/robustness/trials.jsonl`, read beside `runs/main/score-stage1.txt` |
| `runs/main/traces/reading.txt` | `uv run python -m tools.traces runs/main/traces runs/main/trials-reasoning-on.jsonl` |

`score-optional.txt` repeats every stage 1 and stage 2 cell of `score-stage2.txt`
unchanged; Sonnet's long-arm cells gain the rows A4, A6 and A7.

## In short

Reasoning changed nothing Sonnet decided: with thinking allowed, it chose as it did
without, in every trial, and it thought in only 32 of 144 trials. Each time it thought
in X3, its thinking said that two of the reports share a source, and it still chose
their claim: it noticed the dependence and did not act on it. Both auxiliary models'
stated numbers rise from an irrelevant report to one that names the answer, as their
token probabilities do. The two rank trials alike, though mostly through the gap between
those levels; given only an irrelevant report, the tokens lean on one option far more
than the stated numbers. With long reports Sonnet still counts three copies of one source
and three independent sources alike, as about two sources each. On a second set of
reports for M1 and M2, the conflict block's decisions held; only X2 moved, toward more
right decisions.

## What ran

| Entry | Judge | Trials | Cost |
|---|---|---|---|
| `reasoning-off-short`, `reasoning-off-long` | Sonnet, reasoning off | 144 | $0.25 |
| `reasoning-on-short`, `reasoning-on-long` | Sonnet, a 2,000-token thinking budget | 144 | $0.29 |
| robustness: `generate --cases M1,M2` | the reporter | 96 calls | about $0.07 |
| `cross-check` | Qwen 3.6 27B and Llama 4 Maverick | 360 | $0.05 |
| `long-neff` | Sonnet | 162 | $0.36 |
| `cross-check-m12`, after the review | Qwen 3.6 27B and Llama 4 Maverick | 24 | $0.004 |
| robustness: `judge --cases M1,M2 --arms conflict`, after the review | Opus, Sonnet and GPT-5.4 | 360 | $0.70 |

The first five ran from 01:00 to 01:49, one entry at a time, and none stopped. The last
two ran from 17:49 to 18:09 the same day, side by side, once Jason had approved judging
the rerun, and neither stopped. The judge costs are the sum of each log's call costs;
generation records none, so its cost is the fall in the key's balance while it ran. No
call failed. Sonnet stayed on its pinned provider; the auxiliary models are not pinned,
and Qwen answered on Alibaba and Reka, Llama on DigitalOcean and Parasail. Of the 360
cross-check trials read, 4 of Qwen's named no option, answering with an option's value
(179 or 137 passengers in M38), and 5 stated probabilities whose sum was out of range, 4
of Llama's and 1 of Qwen's; they are left out below.

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
weak. X3's P(truth) is higher with reasoning on in all four cells, by 1 to 7 points; X5's
is higher in its two short cells, by 2.3 and 2.5, and mixed in its long ones; X1's barely
moves. Both modes kept the main prompt's last line, "Do not include any explanation or
reasoning -- output only the JSON object.", so they differ only in the thinking allowed;
that line may be why Sonnet so seldom used it.

**The traces: noticed, and not acted on.** Since no X3 trial in either mode chose the
independent report, the coding can only tell whether Sonnet missed the shared source or
noticed it and still followed the two reports. The 112 traces with no thinking text code
as *none*. Two fresh Claude agents coded the other 32 apart, by the rule as settled on
2026-10-28 (`docs/decisions.md`), shuffled and without case, condition or result. They
agreed on 31; Jason settled the last as *noticed*, and the codes were committed before
any was joined to its trial (`runs/main/traces/coding.txt`). All 32 noticed: each says
that two of the reports share a source, or restates the note's sentences about sources.

| Reasoning on: trials (of them, chose the independent report) | none | noticed | not noticed |
|---|---|---|---|
| X1, short and long | 24 (0) and 24 (0) | 0 | 0 |
| X3, short | 18 (0) | 6 (0) | 0 |
| X3, long | 10 (0) | 14 (0) | 0 |
| X5, short | 20 (20) | 4 (4) | 0 |
| X5, long | 16 (16) | 8 (8) | 0 |

In X3, all 20 traces noticed the shared source, and none of those trials chose the
independent report: when Sonnet thought, it saw the dependence and still followed the
two reports. In X5, all 12 noticed, and all chose the independent report, as every X5
trial did. The one split, settled by Jason, is an X5 trace with short reports; the X3
rows are the same under either coder's codes. The traces come only from the trials where
Sonnet chose to think, 20 of X3's 48, so they say nothing of the trials where it did not.

## The confidence cross-check (Qwen 3.6 27B and Llama 4 Maverick)

The two auxiliary models judged the confidence screen's P0, P1 and P2 at four rotations
on 15 cases, answering by option number: the first 15 in corpus order, with M12 in place
of M10. M10's options are 2, 3, 4 and 5 passes, so an answer of 3 can mean option 3 or 3
passes, and both models often meant the value: with the options shown as 4, 2, 5 and 3
passes, both answered 3, which reads as 5 passes, though their report ruled 5 out. M10's
24 trials stay in the log and are left out; M12, the next case in corpus order, was
judged the same way on the same day (`docs/decisions.md`, 2026-10-28). The token
probability of an option is read at the answer's digit.

| | Llama 4 Maverick | Qwen 3.6 27B |
|---|---|---|
| Stated P(truth), P0 → P1 → P2 | 26.2 → 45.6 → 100.0 | 25.0 → 46.4 → 100.0 |
| Token P(truth), P0 → P1 → P2 | 32.6 → 45.1 → 100.0 | 25.5 → 46.5 → 99.2 |
| Page's test, stated and token | p below 0.0001 for both | p below 0.0001 for both |
| Stated against token P(truth), trial by trial | Spearman 0.83 | Spearman 0.81 |
| The same within P1 alone | Spearman 0.79 | Spearman 0.76 |
| P0: the largest stated p, the largest token probability | 76.0, 91.1 | 25.0, 76.9 |

Both ways of reading confidence order the screen's three levels. They rank trials alike,
though mostly through the gap between levels: within P1 alone the correlation is 0.79
and 0.76, and within P0 Qwen's stated number never changes. They part where nothing
points to the answer: shown an irrelevant report, Qwen states 25 on every option, yet its
tokens put 77% on one number on average; Llama's largest stated number averages 76, its
tokens' 91. The answer was always the number its tokens made most likely, as it must be
at temperature 0, which both models take (`docs/decisions.md`, 2026-10-26); that checks
where the tokens are read and is not a finding. No test was fixed for this comparison, so
it is a description.

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
`runs/robustness/`, and the runner's leak check is clean for both. The step 3.4 reading:
M2's hint survives in both of A's reports ("understood", "thought"); every report of A
and of B states its source's quantity; no two of A7's reports read alike. Two D reports
repeat earlier text word for word: M1's D is the first set's D, and M2's D is B's own
sentence. The rerun judges only the conflict block, where C and D are not shown, so
neither reaches a judge. Jason approved judging on 2026-10-28.

All three judges then judged the conflict block on the second set, 12 repeats, 360
trials, each on its pinned provider; no call failed. Right decisions, M1 and M2
together (24 per cell), first set → second set:

| | X1 | X2 | X3 | X4 | X5 |
|---|---|---|---|---|---|
| Opus | 0 → 0 | 24 → 24 | 0 → 0 | 24 → 24 | 24 → 24 |
| Sonnet | 0 → 0 | 9 → 13 | 0 → 0 | 24 → 24 | 24 → 24 |
| GPT-5.4 | 0 → 0 | 22 → 24 | 0 → 0 | 24 → 24 | 24 → 24 |

Every decision pattern of the first set holds on the second: no judge was right in X1
or X3, and every judge was right in every X4 and X5 trial. Only X2, where each report's
source type is named, moved, and only toward more right decisions. P(truth) moved by at
most 7.5 points in any judge's case and condition (Sonnet, M1, X2). The first set was
judged on 2026-10-25 and the second on 2026-10-28, so a difference can come from the
day as well as from the wording (the first entry of 2026-10-26).

## What is left

Nothing: all four sub-experiments have run and been read.
