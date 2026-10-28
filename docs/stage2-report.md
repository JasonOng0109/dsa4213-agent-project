# Stage 2 of the main run: what it found

Stage 2 ran on 2026-10-27 and 2026-10-28 on the ten-case subset. It answers the three
questions stage 1 left for it (`docs/stage1-report.md`, "What stage 1 leaves for later").
Every number comes from one of three files in `runs/main/`, all read from the eight judge
logs, stage 1's five and stage 2's three. The commands name the logs in the order
`runs/main/trials-*.jsonl` listed them then, since the scorer's output follows that order:

| File | Made by |
|---|---|
| `score-stage2.txt` | `uv run python -m pipeline.score --show-excluded runs/main/trials-{abstain-p0,abstain,agreement,conflict,ladder,long-agreement,long-conflict,screen}.jsonl` |
| `tally-stage2.txt` | `uv run python -m tools.tally` over the same eight logs; its section "stage 2's entries" sets each stage 2 cell beside the same judge's short cells on the same ten cases |
| `tally-stage2-without-echoes.txt` | the same, with `--without M3,M9,M13,M23,M28,M38,M40`, which leaves M3 and M38 out of the subset |

"P(truth)" and "right" mean what they mean in stage 1's report. The README's table "What
counts as support, fixed before any data" decides what each result means; this report
only lines the results up against it. "Short" marks stage 1's cells, judged on
2026-10-25, so every comparison with them crosses days (see H2).

## In short

Told only that one source is "somewhat more reliable", the judges still went with it:
Opus and GPT-5.4 in all 120 trials, Sonnet in 91. Their belief in the truth grew with the
wording's strength. So H4's result is not just obedience to blunt wording. Long reports
changed little in the conflict block: saying that two reports share a source still moved
belief in every case but few decisions, at most 18 of 120, and saying which source is
better still made both judges right every time. For Sonnet, three reports in one message raised belief more when the
reports were long, which the table reads as an effect of more words. GPT-5.4 is too near
its ceiling with long reports for that check to tell.

## What ran

| | |
|---|---|
| Cases | the ten-case subset: M1-M6, M14, M22, M30 and M38, seven T1 and three T2 |
| Entries, in order | `ladder`: W1-W3, all three judges, 1,080 trials; `long-agreement`: A1 and A2 with long reports, Sonnet and GPT-5.4, 240; `long-conflict`: X1-X5 with long reports, Sonnet and GPT-5.4, 1,200 |
| When | 2026-10-27 21:42 to 2026-10-28 01:00, one entry at a time |
| Trials | 2,520. All parsed cleanly, no call failed, no judge reasoned, and each judge stayed on its pinned provider |
| Cost | $5.25 for the three logs scored, against $5.11 planned (`docs/work-plan.md`, Phase 5), plus $1.60 for long-conflict's first try: $6.85 in all |

long-conflict's first try stopped at 762 of its 1,200 trials, when one GPT-5.4 call came
back overloaded with the error inside a 200 response, which the backend did not retry.
The backend now retries it. long-conflict was rerun in full into a new log, and the
stopped log is kept in `runs/main/stopped/` and not scored (`docs/decisions.md`,
2026-10-27).

## Results by question

### H4: following an instruction, or weighing evidence? (`ladder`)

X5 says the strong report's source "is a primary, authoritative record" and the shared
source "a secondhand or unofficial one". The ladder keeps X5's reports and dependence
note and softens only that sentence: the strong report's source is "somewhat",
"considerably" or "far" "more reliable than the source shared by" the other two
(`pipeline/conditions.py`).

| Right, of 120 | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| X3: dependence stated, quality not (short) | 1 | 1 | 3 |
| W1: "somewhat more reliable" | 120 | 91 | 120 |
| W2: "considerably more reliable" | 120 | 120 | 120 |
| W3: "far more reliable" | 120 | 120 | 120 |
| X5: "a primary, authoritative record" (short) | 120 | 120 | 120 |

| P(truth) | Opus | Sonnet | GPT-5.4 |
|---|---|---|---|
| X3 (short) | 39.5 | 32.0 | 29.1 |
| W1 | 53.7 | 50.2 | 52.8 |
| W2 | 64.8 | 65.5 | 70.5 |
| W3 | 69.1 | 71.1 | 76.5 |
| X5 (short) | 68.4 | 67.9 | 74.0 |

**Against the table: Support, and the nuisance does not hold for any judge.** The table
reads H4 as driven by a nuisance if "decisions change only under the strongest wording".
Here the weakest wording already made Opus and GPT-5.4 right in every trial and Sonnet in
three of four. Belief followed the wording: mean P(truth) rose from W1 to W3 for every
judge, by 15 to 24 points. At W1 it sat near 50, so the judges picked the better source
without being sure of it. Sonnet's 29 wrong answers at W1 all name A's claim
(`runs/main/trials-ladder.jsonl`). They fall in eight cases, 16 of them in the three T2
cases, where A's reports carry no hedge.

### H3 and H4 with long reports (`long-conflict`)

Each report is set in hand-written filler, 88-96 words (README, "Arms").

| | Sonnet, short | Sonnet, long | GPT-5.4, short | GPT-5.4, long |
|---|---|---|---|---|
| P(truth): X1 → X3 | 20.3 → 32.0 | 19.8 → 27.5 | 21.4 → 29.1 | 21.9 → 30.3 |
| Cases where it rose | 10 of 10 | 10 of 10 | 10 of 10 | 10 of 10 |
| Right, of 120: X1 → X3 | 0 → 1 | 1 → 1 | 2 → 3 | 4 → 18 |
| Right, of 120: X4 and X5 | 120 and 120 | 120 and 120 | 120 and 120 | 120 and 120 |

**Against the table, H3: Support for Sonnet at long length, as at short.** For GPT-5.4,
belief moved and some decisions moved too: 18 of 120, against 3 with short reports, more
in seven cases and fewer in none. All 18 are in the seven T1 cases, where A's reports
still sound unsure, one to five in each. None is in the three T2 cases, though belief
rose there too. That is the pattern stage 1 found for Opus at short length, and the
table's nuisance column, "movement only where a mild content cue survives", is again the
check to report it under.

**H4: Support at long length.** With quality stated, both judges were right in every
trial. Every wrong answer in long-conflict names A's claim
(`runs/main/trials-long-conflict.jsonl`).

### H5 with long reports

Not among the questions stage 1 left open, but long-conflict runs X2 too.

| Right, of 120 | Sonnet, short | Sonnet, long | GPT-5.4, short | GPT-5.4, long |
|---|---|---|---|---|
| X1: nothing disclosed | 0 | 1 | 2 | 4 |
| X2: each source's type named | 52 | 36 | 87 | 74 |

**Against the table: Support at long length too.** Naming the types still raised right
decisions well above X1. The gain was smaller with long reports: Sonnet had fewer right
X2 decisions at long length in five cases and more in one, while GPT-5.4's cases split
three and three.

### H2: is the A1 → A2 rise larger with long reports? (`long-agreement`)

| P(truth), A1 → A2 | Sonnet | GPT-5.4 |
|---|---|---|
| Short reports | 75.8 → 83.8 (+8.0) | 90.3 → 96.2 (+5.9) |
| Long reports | 78.3 → 91.7 (+13.4) | 94.8 → 95.6 (+0.8) |
| Cases where the rise is larger at long length | 9 of 10 | 0 of 10 |

**Against the table: for Sonnet, the nuisance holds.** The table reads an A1 → A2 effect
"larger at long length than at short" as a nuisance, and the README names it: "a larger
A1 to A2 rise at long length would point to token volume" ("Arms"). So part of what three
reports in one message add for Sonnet is more words, not only more restatements. For
GPT-5.4 the nuisance does not hold, but the check has little room: one long report
already gets 94.8, and in four cases A2 is below A1. Opus is not in the length arm.

The check does not touch H2's later steps, splitting the reports into messages (A2 → A3)
and naming agents (A3 → A4). They ran at short length only, where stage 1 found Support.

These comparisons cross days: the short cells were judged on 2026-10-25 and the long ones
on 2026-10-27, since Jason decided against judging A1 and A2 again beside the length arm
(`docs/decisions.md`, 2026-10-26). On the A0 prompts the pilot and stage 1 share, judged
six days apart, Sonnet's P(truth) moved by 2.7 points on average (same file, 2026-10-26).
The gap here is 5.4 points, and it shows in 9 of the 10 cases.

## Checks already done

- **Without M3 and M38**, the two echo cases in the subset, every direction above holds.
  Sonnet's A1 → A2 rise is +8.7 short and +13.7 long, larger at long length in 7 of 8
  cases. At W1 Sonnet is right in 73 of 96, the other judges in all 96. GPT-5.4's X3 at
  long length is right in 14 of 96, against 3 of 96 short.

## Notes for the write-up

- Every rung of the ladder still says which source is more reliable; only the strength
  changes. The README reads flips at the weaker rungs as weighing evidence. If asked
  whether a judge simply follows a mild statement as it follows a blunt one, the evidence
  to point to is P(truth): near 50 at "somewhat", rising with each rung.
- The ladder's and long-conflict's differences from stage 1 are large against the
  drift across days, such as 1 to 3 of 120 right in X3 against 91 to 120 at W1. H2's
  length check is the closest call.

## What stage 2 leaves for later

| Still open | Answered by |
|---|---|
| Reasoning on and off; wording robustness; stated against token probabilities; n_eff with long reports | the optional sub-experiments (`docs/decisions.md`, 2026-10-26), run from the branch `optional-arms` after stage 2: `docs/optional-report.md` |
