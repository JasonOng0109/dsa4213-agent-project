# Work plan

Who does what next, in small steps. Written for someone who has never seen this project.
Every task says **why** it matters, **what to read** first, **what to do**, and **when it
is done**. Do the tasks in order. If you are stuck for more than 30 minutes, ask Jason.

Plan written 2026-10-12. The status changes as work is merged, so look it up where it is
kept:

- The code is built and tested: `uv run pytest` must pass.
- How many cases are merged: README, "Status and open items". Writing cases is the
  slowest part of the project.
- The pilot ran on 2026-10-19 (Phase 3); its output is `runs/score-pilot.txt`. The main
  run's stage 1 ran on 2026-10-25 (Phase 5); its output is `runs/main/score-stage1.txt`.
  Stage 2 ran on 2026-10-27 and 2026-10-28; its output is `runs/main/score-stage2.txt`.
- What is still open: the "Open questions" board in `knowledge-graph.html`.

---

## Who does what

| Member | Role | Writes (pilot) | Reviews (pilot) | Owns this open item |
|---|---|---|---|---|
| **Jason** | Runs the paid steps, holds the API key, merges pull requests | — | final check of every case | what the pilot runs (2E); the pilot run (Phase 3) |
| **Crystal** | Case author | M2 | M5 | the H6 margin cut-off (2B) |
| **Rachel** | Case author | M3 | M2 | the wording ladder's sentence (2A) |
| **Kathleen** | Case author | M4 | M3 | — |
| **Kai Rong** | Case author, corpus coordinator | M5 | M4 | the discrimination pass mark (2C); which ten cases form the subset (2D) |

Nobody reviews their own case. Rule from `docs/authoring-rules.md`: the worst defect
"cannot be caught by any script", so a second person must read every case.

## The order of work

```
Phase 0  everyone learns the basics
   │
   ├── Phase 1  write and review 4 pilot cases (M2–M5)      ┐ at the same time
   └── Phase 2  settle the open decisions (2A–2E)           ┘
   │
   ├── Phase 3  pilot run on M1–M5 (Jason, paid)            ┐ at the same time
   └── Phase 4  write the other 35 cases (M6–M40)           ┘ (merged after the pilot)
   │
Phase 5  main run, analysis, write-up (detailed after the pilot)
```

---

## Words you need

Learn these first. Each points to where it is explained in full.

| Word | Meaning in one line | Read more |
|---|---|---|
| **Case** | One made-up question, its right answer, and four sources | `cases/m1.py` |
| **Source A** | The weak source. It states a **wrong** answer | `docs/authoring-rules.md`, R14 |
| **Sources B, C, D** | Strong sources. All state the **right** answer | same |
| **Content** | The one sentence a source says | `docs/authoring-rules.md`, top |
| **Provenance** | Who made a source and how good it is. Kept hidden from the reporter | same, R2 |
| **Reporter** | An AI model that rewords each source into a short report | README, "Two agent roles" |
| **Paraphrase / report** | A reworded copy of a source's content | same |
| **Judge** (orchestrator) | The AI model we study. It reads reports and picks an answer | same |
| **Options** | The 4 answers the judge picks from: truth, A's claim, 2 distractors | README, "Task and cases" |
| **Distractor** | A believable answer that no source supports | `docs/authoring-rules.md`, R8 |
| **Condition** | What the judge is shown. A0–A7, X1–X5 and W1–W3 | README, "Two blocks" |
| **Agreement block** | A0–A7: all reports agree. Measures how sure the judge is | same |
| **Conflict block** | X1–X5: two reports of weak A against one of strong B | same |
| **Arm** | One version of the run: short, abstention, screen, length, ladder | README, "Arms" |
| **Tier T1 / T2** | T1: a small hint in the wording survives rewording. T2: no hint | `docs/authoring-rules.md`, "Tiers" |
| **Quality dimension** | Why the strong source is better: authority, directness, method or primary source | same, R19 |
| **Linter** | A script that checks a case against the rules it can check | `pipeline/lint.py` |
| **Frozen reports** | The accepted paraphrases, saved once and reused in every condition | README, "Two agent roles" |
| **Dry run** | A free practice run with a fake judge. Spends no money | README, "Running the study" |
| **Knowledge graph** | The clickable map of the whole project | `knowledge-graph.html` |

---

## Phase 0 — Everyone: get set up and learn the basics

All five members do every task here.

### 0.1 Install and run the tests

- **Why**: you need a working copy before anything else.
- **Do**:
  1. Install `git`, and `uv` from <https://docs.astral.sh/uv/>.
  2. Run:
     ```bash
     git clone https://github.com/JasonOng0109/dsa4213-agent-project.git
     cd dsa4213-agent-project
     uv sync
     uv run pytest
     ```
  3. Optional, on a Mac: `brew install poppler`, so the tests also check quotes from PDFs.
- **Done when**: the last line says `passed`, with no `failed`.

### 0.2 Take the tour of the map

- **Why**: the map explains the project in small pieces, and links each piece to its file.
- **Do**: open `knowledge-graph.html` in a browser. Click **Start the tour**. Go through
  every stop.
- **Done when**: you can say the research question in one sentence.

### 0.3 Read four parts of the README

- **Read**: `README.md`, these sections only: "Research question", "Why this is an agent
  problem", "Task and cases", "Two blocks, thirteen conditions". Skip the rest for now.
- **Done when**: you can explain what X1 and X3 show the judge.

### 0.4 Learn what a case looks like

- **Read**: `cases/m1.py`, next to the table "What a case contains" at the top of
  `docs/authoring-rules.md`.
- **Do**: for each field in the table, find it in `cases/m1.py`.
- **Done when**: you can point to M1's truth, its wrong claim and its two distractors.

### 0.5 See what the judge sees

- **Why**: the whole study is about this one screen of text.
- **Do**:
  1. Run a free practice run: `uv run python -m pipeline.run dry`
  2. Print the judge's prompt for X1 and X3:
     ```bash
     uv run python -c "
     import json
     from cases import CASES
     from pipeline.conditions import build_repeat
     from pipeline.prompt import render
     frozen = json.load(open('runs/mock/frozen_reports.json'))
     for t in build_repeat('M1', CASES['M1'], frozen['M1'], 1):
         if t['condition'] in ('X1', 'X3'):
             print('=====', t['condition']); print(render(t))
     "
     ```
     The reports here are fake, made by the practice run. Real ones come from the reporter.
- **Done when**: you can see the one line that X3 adds to X1: the `Note:` line.

### 0.6 Run the linter

- **Do**: `uv run python -m pipeline.lint`
- **Done when**: it ends with `0 violation(s)`. Read the other lines too: they are notes.

### 0.7 Check yourself

Answer these. The answers are in the files named.

1. What does each of sources A, B, C, D do? (`docs/authoring-rules.md`, R14)
2. Why is every fact made up? (`docs/authoring-rules.md`, R4; README, the ClashEval row)
3. Why must someone else review your case? (`docs/authoring-rules.md`, first paragraph)
4. Why does the study use four options and not two? (`docs/proposal.pdf`, §6, "The answer
   space has four options")

---

## Phase 1 — Write and review the four pilot cases

### The four cases

Together with M1, these cover all 3 domains and all 4 quality dimensions.

| Case | Domain | Quality dimension | Tier | Author | Reviewer |
|---|---|---|---|---|---|
| M1 | `institutional_logistics` | `authority` | T2 | done | done |
| M2 | `product_spec` | `primary_source` | T1 | Crystal | Rachel |
| M3 | `incident_status` | `directness` | T1 | Rachel | Kathleen |
| M4 | `product_spec` | `method` | T1 | Kathleen | Kai Rong |
| M5 | `incident_status` | `authority` | T1 | Kai Rong | Crystal |

Jason does a final check on each case before merging.

### Author tasks (Crystal M2, Rachel M3, Kathleen M4, Kai Rong M5)

Same steps for each author. Replace `m2` with your case.

**1.1 Read the rules once, start to end.**
- **Read**: all of `docs/authoring-rules.md`. Keep it open while you write.

**1.2 Choose your fact.**
- **Why**: everything else is built around it.
- **Do**: make up an entity and one fact about it. Write down the question, the truth,
  A's wrong claim and two distractors.
- **Rules**: R4 (made up, not checkable in real life), R8 (exactly two distractors, same
  kind as the truth). The question must have more than two sensible answers.
- **Tip**: pick values so that the truth and A's claim are both *in the middle*. In M1
  the options are 10%, 15%, 25%, 30%: the truth (15%) and the wrong claim (25%) are
  neither the smallest nor the largest.

**1.3 Copy M1 and register your case.**
- **Do**:
  1. `cp cases/m1.py cases/m2.py`
  2. In `cases/m2.py`, change the top comment, `case_id`, `domain`, `quality_dimension`
     and `difficulty_tier` to your row in the table above.
  3. In `cases/__init__.py`, change `from . import m1` to `from . import m1, m2`, and
     `(m1.CASE,)` to `(m1.CASE, m2.CASE)`.
- Keep `n_paraphrases_needed` as in M1: A 2, B 3, C 1, D 1 (R14).

**1.4 Write the four content sentences.**
- **Do**: one sentence each for A, B, C, D.
- **Rules**:
  - R11: exactly one sentence.
  - R1: A and B are equally flat, sure and specific. They name the same whole ("of the
    final module grade").
  - R3: no dates, no "new", "updated", "now".
  - R7: each sentence names its own subject.
  - R17: B, C and D use different sentence shapes.
  - R13: A and B use exactly the same words from the question.
  - R20: A and B are within 2 words of each other in length.
- **T1 only** (R16): give A one mild hint that survives rewording, such as a hedge ("is
  understood to be"). One small word like "your" does not survive. Use a hedge that
  fewer than three T1 cases use, on `main` or in open pull requests, preferring one
  already in use to a new one, and name it in `design_notes` (R16, "Vary the cue").
  `uv run python tools/case_index.py --all-branches` lists the hedges in use and the
  slots each has left. In a method case, pick one that names no method: not
  "estimated", "guessed" or "reckoned" (R16).

**1.5 Write the provenance.**
- **Do**: fill `type`, `authority`, `quality`, `why` for each source.
- **Rules**: R19: the type name alone should show which source is better. Start from the
  table in R19. A's and B's names differ only in your case's dimension: in a directness,
  method or primary-source case both writers have the same standing (R19). R2a: do not
  use words in `type` that your content needs.

**1.6 Write the screen sentence.**
- **Do**: fill `screen_partial`. One true sentence that keeps the truth and rules out
  exactly two of the four options (R15). A sentence with bounds uses two, with both kept
  options the same distance inside them. Example: M1's "more than a twentieth and less
  than a fifth" keeps 10% and 15%, each 5 points inside a bound, and rules out 25% and
  30%. The other option it keeps can be A's claim or a distractor.

**1.7 Write the filler.**
- **Do**: three lists of five neutral sentences, as in M1.
- **Rules**: R9 (never mention or hint at any option; naming the case's subject is
  fine), R10 (no "you", no "this
  announcement", one plain style), R12 (three sets, never tied to a source).
- **Length** (R20): size each filler set so that the set plus A's sentence and the set
  plus B's sentence are both 91–93 words (about 77–80 words for 12–15-word sentences).
  A rewording may then be up to 3 words longer or shorter and still fit 88–96 words. The
  linter prints an R20 warning when a set is off. The practice run does not check your case's length (it
  says "Long-report length not checked"), so go by the R20 warning.

**1.8 Lint until clean.**
- **Do**: `uv run python -m pipeline.lint`. Fix every violation. Run again.
- **Done when**: `0 violation(s)` and no `R20 warning` lines.

**1.9 Do the checks no script can do.**
- **Read**: "Checks no script performs", at the end of `docs/authoring-rules.md`.
- **Do**: hide the provenance. Read A and B as if two equally trusted strangers said
  them. Does either one win by being narrower, an exception, or more precise? If yes,
  rewrite. Then explain your choices in `design_notes`.

**1.10 Open a pull request.**
- **Do**: `uv run pytest` must pass, apart from the one expected failure below. Then push
  a branch (see "Git in five commands") and open a pull request. Tag your reviewer and
  Jason.
- **Do not update the corpus count.** Leave README's corpus bullet and
  `knowledge-graph.html` alone: Jason updates the count when he merges
  (`docs/decisions.md`, "Authors do not update the corpus count").
- **Expected failure**: once you register your case, `test_knowledge_graph_checks_clean`
  fails on the `open-corpus` quote. Every other test must pass.

### Reviewer tasks (Rachel M2, Kathleen M3, Kai Rong M4, Crystal M5)

**1.11 Review one case.**
- **Why**: the worst defect is invisible to the linter.
- **Do**:
  1. Get the branch: `git fetch` then `git checkout case-m2`.
  2. Run `uv run python -m pipeline.lint`.
  3. Read the case beside `docs/authoring-rules.md`, rule by rule.
  4. Do the specificity test from 1.9 yourself.
  5. The type-name test (R19): show someone only the two type names. Do they prefer one,
     for the case's dimension and not because one writer outranks the other?
  6. The screen test (R15): is the sentence true? Does it keep the truth? Does it rule
     out exactly two options?
  7. Comment on the pull request. Name the rule for each problem ("R13: ...").
- **Done when**: the author has fixed every comment and you approve.

**1.12 Final check and merge (Jason).**
- **Do**: read the case once more, run `uv run pytest`, merge. If two pull requests both
  edit `cases/__init__.py`, merge one, then fix the second by hand.

---

## Phase 2 — Settle the open decisions

Each owner does one item, at the same time as Phase 1. Each item ends the same way: the
group agrees, and the decision is recorded (see "How to record a decision").

**All five were decided on 2026-10-18**, before any pilot result, and are recorded in
`docs/decisions.md`. Each item below starts with what was chosen; the rest of it is how
it was worked out. Only 2D's rule is still to be applied, in Phase 4.

**Agree each number before anyone looks at pilot results.** The README fixes the reading
of results "before any data", so a number chosen after seeing data could be bent to fit
it.

### 2A The wording ladder's sentence — Rachel

- **Decided 2026-10-18**: keep the sentence. W1, W2 and W3 differ only in the intensity
  word, and "more reliable than the shared source" is the proposal's own phrase.
- **Why**: H4 says that telling the judge "this source is better" changes its answer. A
  critic could say the judge just obeyed. The ladder tests this: W1, W2 and W3 say
  "somewhat", "considerably" and "far" more reliable. Only that one word may change. The
  proposal fixes the three words but not the sentence around them.
- **Read**: `docs/decisions.md`, "The graded wording ladder is built as W1-W3, on top of
  X5". README, "Arms", the bullet "The wording ladder". `pipeline/conditions.py`, the
  lines that start `dep =`, `qual5 =` and `rung =`.
- **Do**:
  1. Print the prompts: run the command from 0.5 with `('X5', 'W1', 'W2', 'W3')` in place
     of `('X1', 'X3')`.
  2. Check: do W1, W2 and W3 differ only in that one word?
  3. Read each as if you were the judge. Does it sound natural? Does it hint at anything
     besides quality, such as age or officialness?
  4. Write a short proposal: keep the sentence, or a new one, and one reason.
- **Done when**: the group agrees and it is recorded.

### 2B The H6 margin cut-off — Crystal

- **Decided 2026-10-18**: a margin below 10 points counts as near indifference. The
  entry "Margin" is in `docs/methods.md`, and `report_h6` in `pipeline/score.py` prints
  H6's test.
- **Amended 2026-10-19**: `report_h6` compares the flagged and unflagged trials inside
  each conflict condition, then combines the conditions. Pooled, a condition with more
  of both close numbers and abstaining would look like H6 when no trial shows it
  (`docs/decisions.md`, the H6 entry).
- **Why**: H6 says a judge sometimes picks an answer while its own numbers show it does
  not really know. One sign: the top two probabilities are close. The proposal says
  "below a stated threshold", but no number was ever stated.
- **Read**: README, the H6 row in "Hypotheses". `docs/proposal.pdf`, p.16, the H6 row,
  and Appendix A, p.22–23 (a worked example with a margin of 10 points).
  `pipeline/judge.py`, the lines after the comment "coherence sees inversion only". The
  map's node "Coherence and margin".
- **Do**:
  1. Margin = highest probability minus the second highest. Work out three by hand:
     34/33/33/0 → 1. 50/40/5/5 → 10. 90/5/3/2 → 85.
  2. Draft an entry "Margin" for `docs/methods.md`, in its five-part format. Claude Code
     in this repository can help: it knows the format.
  3. Propose a cut-off, with one reason.
- **Done when**: the group agrees and it is recorded.

### 2C The discrimination pass mark — Kai Rong

- **Decided 2026-10-18**: a condition counts when it has 10 right and 10 wrong decisions
  (A0 never). A judge passes when at least one counted condition has AUROC above 0.5 at
  p below 0.05 divided by the number counted. The entry "AUROC" is in `docs/methods.md`.
  Amended 2026-10-19: the p-value shuffles whole cases, since a case's repeats are
  near-copies and counting each decision makes p far too small. Replaced 2026-10-21,
  after the pilot: the verdict is printed but excludes no judge (`docs/decisions.md`,
  "Only ordering decides whose stated numbers count").
- **Why**: a judge's probabilities count only if they carry information. One check is
  AUROC: when the judge is right, does it state higher confidence than when it is wrong?
  The scorer printed it, but no pass mark was set, so it could not exclude any judge.
- **Read**: `docs/decisions.md`, "The discrimination check is reported, with no pass mark
  yet". `pipeline/score.py`, the function `auroc` and its comment: 0.5 means no
  information.
- **Do**:
  1. Work one example by hand. Confidence when right: 90, 80. When wrong: 70, 85.
     Compare every right–wrong pair: 90>70 yes, 90>85 yes, 80>70 yes, 80>85 no. 3 of 4,
     so AUROC = 0.75. Check it:
     `uv run python -c "from pipeline.score import auroc; print(auroc([90,80],[70,85]))"`
  2. The second number to set: the smallest class size. If a judge was wrong only twice,
     its AUROC rests on two numbers. For scale: in the main run each conflict condition
     has 40 cases × 12 repeats = 480 trials per judge, and each agreement condition 240.
  3. Draft an entry "AUROC" for `docs/methods.md`, in its five-part format.
  4. Propose a pass mark and a smallest class size, with one reason each.
- **Done when**: the group agrees and it is recorded.

### 2D The case register and the ten-case subset — Kai Rong

- **Decided 2026-10-18**: the ten are M1–M5 plus five Phase 4 cases that you mark when
  you assign the batches, before they are written. Two of the five are T2 and three T1;
  every domain has at least 3 of the ten, and every dimension at least 2. A dropped case
  is replaced by the next assigned case with the same domain, dimension and tier
  (`docs/decisions.md`, "The ten-case subset is fixed by a rule before the pilot").
- **Why**: the length arm and the wording ladder run on only 10 cases. The code takes the
  first ten in `cases/__init__.py` (`subset` in `pipeline/run.py`). The ten should be
  chosen on purpose, spread across domains, dimensions and tiers.
- **Read**: `docs/decisions.md`, "The runner encodes the proposal's main programme as one
  table". `docs/authoring-rules.md`, "Tiers".
- **Do now**: after each merge, update the case register in Phase 4 below. The linter's
  "Set-level counts" show the spread.
- **Marked 2026-10-19**, with the first Phase 4 batches, before anyone drafted them: M6,
  M14, M22, M30 and M38, under "Subset" in the case register in Phase 4 below.
- **Backups named 2026-10-21**, when the other 25 cases were assigned, before anyone
  drafted them: M16 for M6, M8 for M14, M9 for M22, M17 for M30 and M32 for M38. Each
  backup has the same domain, dimension and tier as its case, and a different author. A
  backup is written and reviewed like any other case, and joins the ten only if its case
  is dropped.
- **Reordered 2026-10-25**, by Jason for Kai Rong, once all 40 cases were merged and
  before the main run: the tuple in `cases/__init__.py` puts the ten first.
- **Done when**: the five are marked, and the reordered tuple is merged.

### 2E What the pilot runs — Jason, with the group

- **Decided 2026-10-18**: the whole programme on M1–M5, 3,660 calls and $7.03, with the
  group approving up to $10. `generate --max-calls 600`; the judge step runs one
  programme entry at a time, each into its own log with its planned calls as the
  ceiling (`docs/decisions.md`, "The pilot runs the whole programme on M1-M5").
- **Why**: the group fixed the pilot at 5 cases (`docs/decisions.md`, "The pilot runs on
  5 cases"). Nothing said which arms the pilot runs, or its call ceiling.
- **Do**:
  1. `uv run python -m pipeline.run plan --cases 5`. The whole programme on 5 cases is
     3,660 calls, $7.03.
  2. Choose: the whole programme, or some arms only (`judge --arms`).
  3. Set the call ceiling. Get the group's approval to spend.
- **Done when**: recorded, and the spend is approved.

### How to record a decision

1. Open Claude Code in the repository. Say: "Record this team decision: [what we chose],
   because [why], instead of [what we rejected]. Decided [date]."
   It follows `CLAUDE.md`: it writes the entry in `docs/decisions.md`, updates the map,
   and closes the open item.
2. Read what it changed. Run `uv run pytest`.
3. Open a pull request. Jason merges.

Without Claude Code: write the entry yourself in `docs/decisions.md`, using its five
fields, and ask Jason to update the map.

---

## Phase 3 — The pilot run

**Start only when**: M1–M5 are merged, 2E is agreed, and the spend is approved.

In the table, `...` is short for `uv run --env-file .env python -m`.

| Step | Who | Do |
|---|---|---|
| 3.1 | Jason | `uv run --env-file .env python -m pipeline.run balance`: check the key's limit |
| 3.2 | Jason | `... pipeline.run probe`: do the models answer, on the right providers? Output: `runs/probe.json` |
| 3.3 | Jason | `... pipeline.run generate --max-calls 600`. The README allows 120 per case for two rounds; 5 × 120 = 600 |
| 3.4 | each author and reviewer | Read your case in `runs/frozen_reports.json` (see below) |
| 3.5 | Jason | One programme entry at a time (2E), e.g. `... pipeline.run judge --arms conflict --log trials-conflict.jsonl --max-calls 900`. Each entry's calls are in `docs/decisions.md` |
| 3.6 | Jason | `uv run python -m pipeline.score --show-excluded runs/trials-*.jsonl`, all the logs together. `--show-excluded` also prints n_eff and H6 for judges the screen excludes, as checks: on 5 cases, discrimination, then part of the screen, was likely to exclude most judges (`docs/decisions.md`, the pilot entry). Share the output |
| 3.7 | Jason | Commit everything in `runs/`. Record the results in the map |
| 3.8 | Jason | Added after the pilot (`docs/decisions.md`, 2026-10-21): the P0 check once on M1–M5, `... pipeline.run judge --arms abstain-p0 --log trials-abstain-p0.jsonl --max-calls 60`, about $0.10. Then score all the logs together again into `runs/score-pilot-2026-10-21.txt` and commit |

**3.4 Reading the frozen reports.** Never edit them. Check three things:

1. **Hint** (T1 cases only): is A's hint still there after rewording? If not, relabel the
   case T2. Do not rewrite it (R16).
2. **Same whole**: do A's and B's reports talk about the same thing ("of the final
   grade")? If not, the conflict measures nothing.
3. **No leaks**: no report names who wrote it.

Also note, but do not fail, any two of B's, C's and D's reports that read almost alike
while their `cross_overlap` stays under 0.50 (R17), like M4's B and D (0.42) in the pilot.

Tell Jason what you found.

**Pilot numbers are a preview, not findings.** `docs/decisions.md` calls the pilot's
screen verdict "a preview".

---

## Phase 4 — Write the other 35 cases

Same steps as Phase 1. Each author keeps the same reviewer. Kai Rong gives each case its
domain, dimension and tier: two per author on 2026-10-19, the rest on 2026-10-21.

**When**: start drafting now, before the pilot (`docs/decisions.md`, "Phase 4 drafting
starts before the pilot"). Your cases are in the case register below. Use the lessons
from the review comments on the Phase 1 pull requests and the current
`docs/authoring-rules.md`. Keep each case on its own branch until the pilot has run:
Jason merges Phase 4 cases only after it, because the run takes every case in
`cases/__init__.py`, and a case merged earlier would join the pilot.

### Targets for all 40

- About **30 T1 and 10 T2**, with the T2 cases spread across domains and dimensions
  (`docs/authoring-rules.md`, "Tiers").
- All 3 domains and all 4 dimensions. They cannot be perfectly even; that is planned.

### Case numbers

| Author | Cases | How many | Reviewer |
|---|---|---|---|
| Crystal | M6–M13 | 8 | Rachel |
| Rachel | M14–M21 | 8 | Kathleen |
| Kathleen | M22–M29 | 8 | Kai Rong |
| Kai Rong | M30–M37 | 8 | Crystal |
| Jason | M38–M40 | 3 | Kathleen |

### Case register (Kai Rong keeps this current)

| Case | Domain | Dimension | Tier | Author | Reviewer | Status | Subset |
|---|---|---|---|---|---|---|---|
| M1 | institutional_logistics | authority | T2 | — | — | merged | yes |
| M2 | product_spec | primary_source | T1 | Crystal | Rachel | merged | yes |
| M3 | incident_status | directness | T1 | Rachel | Kathleen | merged | yes |
| M4 | product_spec | method | T1 | Kathleen | Kai Rong | merged | yes |
| M5 | incident_status | authority | T1 | Kai Rong | Crystal | merged | yes |
| M6 | institutional_logistics | primary_source | T1 | Crystal | Rachel | merged | yes |
| M7 | product_spec | authority | T1 | Crystal | Rachel | merged | |
| M8 | incident_status | method | T2 | Crystal | Rachel | merged | backup for M14 |
| M9 | product_spec | directness | T2 | Crystal | Rachel | merged | backup for M22 |
| M10 | institutional_logistics | authority | T1 | Crystal | Rachel | merged | |
| M11 | institutional_logistics | directness | T1 | Crystal | Rachel | merged | |
| M12 | product_spec | method | T1 | Crystal | Rachel | merged | |
| M13 | incident_status | primary_source | T1 | Crystal | Rachel | merged | |
| M14 | incident_status | method | T2 | Rachel | Kathleen | merged | yes |
| M15 | institutional_logistics | authority | T1 | Rachel | Kathleen | merged | |
| M16 | institutional_logistics | primary_source | T1 | Rachel | Kathleen | merged | backup for M6 |
| M17 | institutional_logistics | directness | T1 | Rachel | Kathleen | merged | backup for M30 |
| M18 | product_spec | primary_source | T1 | Rachel | Kathleen | merged | |
| M19 | incident_status | directness | T2 | Rachel | Kathleen | merged | |
| M20 | product_spec | method | T1 | Rachel | Kathleen | merged | |
| M21 | incident_status | authority | T1 | Rachel | Kathleen | merged | |
| M22 | product_spec | directness | T2 | Kathleen | Kai Rong | merged | yes |
| M23 | institutional_logistics | method | T1 | Kathleen | Kai Rong | merged | |
| M24 | institutional_logistics | primary_source | T2 | Kathleen | Kai Rong | merged | |
| M25 | product_spec | authority | T1 | Kathleen | Kai Rong | merged | |
| M26 | incident_status | method | T1 | Kathleen | Kai Rong | merged | |
| M27 | institutional_logistics | authority | T1 | Kathleen | Kai Rong | merged | |
| M28 | product_spec | primary_source | T1 | Kathleen | Kai Rong | merged | |
| M29 | incident_status | directness | T1 | Kathleen | Kai Rong | merged | |
| M30 | institutional_logistics | directness | T1 | Kai Rong | Crystal | merged | yes |
| M31 | product_spec | primary_source | T2 | Kai Rong | Crystal | merged | |
| M32 | incident_status | primary_source | T1 | Kai Rong | Crystal | merged | backup for M38 |
| M33 | incident_status | authority | T2 | Kai Rong | Crystal | merged | |
| M34 | product_spec | authority | T1 | Kai Rong | Crystal | merged | |
| M35 | institutional_logistics | method | T1 | Kai Rong | Crystal | merged | |
| M36 | product_spec | directness | T1 | Kai Rong | Crystal | merged | |
| M37 | incident_status | method | T1 | Kai Rong | Crystal | merged | |
| M38 | incident_status | primary_source | T1 | Jason | Kathleen | merged | yes |
| M39 | incident_status | directness | T1 | Jason | Kathleen | merged | |
| M40 | institutional_logistics | method | T2 | Jason | Kathleen | merged | |

**Subset** marks the ten cases the length arm and the wording ladder run on (2D): M1–M5,
and five Phase 4 cases marked on 2026-10-19 with the first batches, before anyone drafted
them. The five are one per author, and two of them are T2. Every domain has at least 3 of
the ten and every dimension at least 2, and the ten's three T2 cases (M1, M14, M22) are
in three different domains and three different dimensions. M1–M5 and the first batches
together have 5 cases in each domain and cover all 12 pairs of domain and dimension.
"Backup for" names the case that takes a marked case's place if it is dropped (2D).

**All 40**, as assigned on 2026-10-21: 13 institutional_logistics, 13 product_spec and 14
incident_status cases; 10 in each dimension; 30 T1 and 10 T2, with T2 cases in every
domain and every dimension; and 3 or 4 cases in each of the 12 pairs of domain and
dimension. Each of the four authors with eight cases has two in each dimension and two
T2, and no pair of domain and dimension twice. A T1 case can still become T2 once its
frozen reports are read (R16).

Every case has a row. Change its status from "assigned" to "merged" when Jason merges it.

---

## Phase 5 — Main run and write-up

Outline only. Detailed tasks will be added after the pilot.

- **Before**: all 40 cases merged. Every open item closed except the optional
  sub-experiments. Spend approved. The proposal asks for $75; the key's limit is $50,
  and the coordinator tops it up again only after seeing it spent. The main programme at
  40 cases is $38.34 at the proposal's rates (`uv run python -m pipeline.run plan --cases
  40`): the proposal's $37.48 plus the P0 check added after the pilot. At the pilot's
  rates it is about $39.84.
- **Run** (Jason): same steps as Phase 3, in two stages (`docs/decisions.md`,
  2026-10-22), except two (`docs/decisions.md`, 2026-10-25): Jason reads the frozen
  reports before judging and the authors and reviewers check his summary, and stage
  1's judge entries run in three lanes, each entry still into its own log.
  Stage 1, $34.74: generate ($0.48), then `screen` ($2.40), `conflict` ($13.78),
  `agreement` ($11.02), `abstain` ($6.11), `abstain-p0` ($0.95) and any entry added
  later that does not run on the ten-case subset. Stage 2, after the top-up, $5.11, one
  entry at a time (`docs/decisions.md`, 2026-10-26): `ladder` ($2.24), then
  `long-agreement` ($0.48), then `long-conflict` ($2.39), then the optional
  sub-experiments. These costs use the pilot's measured cost per call; `judge`
  prints the proposal's rates, which run 16% low for `abstain`. Generation's $0.48 is
  the proposal's rate: it cost $1.49 when measured on 2026-10-25
  (`runs/main/reading-3.4.md`). Run `probe` before each stage, and before each entry
  check that `balance` covers its cost plus 10%.
  Stage 1 ran on 2026-10-25, judging from 13:45 to 20:26, and no entry stopped. It cost
  $36.78 against $34.74 planned: generation $1.49 and judging $35.29, the sum of the
  five logs' call costs. That left $2.11 on the key, so stage 2 waited for the top-up.
  Stage 2 ran after the top-up, from 2026-10-27 21:42 to 2026-10-28 01:00. Its three logs
  cost $5.25 against $5.11 planned: `ladder` $2.31, `long-agreement` $0.40 and
  `long-conflict` $2.53. long-conflict's first try, stopped at 762 of its 1,200 trials
  and rerun in full, cost $1.60 more (`docs/decisions.md`, 2026-10-27).
- **Analysis**: read results only against the table "What counts as support, fixed
  before any data" in the README. Stage 1's first reading, hypothesis by hypothesis:
  `docs/stage1-report.md`. Its counts over cases come from `tools/tally.py`. Stage 2's
  reading: `docs/stage2-report.md`.
- **Optional sub-experiments**: designed on 2026-10-26, each in its own entry in
  `docs/decisions.md`, and built as the entries in `OPTIONAL` (`pipeline/run.py`; the
  commands are in the README, "Running the study"). Only if budget allows, in the order
  the proposal gives (§6).
- **Write-up**: it must include one fully shown prompt and judge answer per block
  (`docs/proposal.pdf`, §5, "Representative evidence").

---

## Rules for everyone

- Never commit `.env` or an API key. Only Jason runs steps that spend money, and only
  after the group approves.
- Never edit anything in `runs/`. Real outputs are evidence.
- Run `uv run pytest` before every pull request.
- Every decision goes into `docs/decisions.md`, so the map stays true (`CLAUDE.md`).
- Not sure what something means? Search for it in `knowledge-graph.html`, or ask Claude
  Code in this repository: it reads the map first.

## Git in five commands

```bash
git checkout main && git pull       # start from the latest version
git checkout -b case-m2             # one branch per task
# ... make your changes ...
uv run pytest                       # must pass
git add cases/m2.py cases/__init__.py && git commit -m "Add case M2"
git push -u origin case-m2          # then open a pull request on GitHub
```

---

## Progress tracker

Change "to do" to "done" when a task is finished.

| Task | Owner | Waits for | Status |
|---|---|---|---|
| 0.1–0.7 Setup and basics | Jason | — | to do |
| 0.1–0.7 Setup and basics | Crystal | — | to do |
| 0.1–0.7 Setup and basics | Rachel | — | to do |
| 0.1–0.7 Setup and basics | Kathleen | — | done |
| 0.1–0.7 Setup and basics | Kai Rong | — | to do |
| 1.1–1.10 Write M2 | Crystal | Phase 0 | done |
| 1.1–1.10 Write M3 | Rachel | Phase 0 | done |
| 1.1–1.10 Write M4 | Kathleen | Phase 0 | done |
| 1.1–1.10 Write M5 | Kai Rong | Phase 0 | done |
| 1.11 Review M2 | Rachel | M2 pull request | done |
| 1.11 Review M3 | Kathleen | M3 pull request | done |
| 1.11 Review M4 | Kai Rong | M4 pull request | done |
| 1.11 Review M5 | Crystal | M5 pull request | done |
| 1.12 Final check and merge, M2–M5 | Jason | each review | done |
| 2A Ladder sentence | Rachel | Phase 0 | done |
| 2B Margin cut-off | Crystal | Phase 0 | done |
| 2C Discrimination pass mark | Kai Rong | Phase 0 | done |
| 2D Case register (ongoing) | Kai Rong | each merge | done |
| 2D Ten-case subset: the rule | Jason + group | — | done |
| 2D Ten-case subset: mark five | Kai Rong | Phase 4 batches | done |
| 2D Ten-case subset: name backups | Kai Rong | all Phase 4 cases assigned | done |
| 2D Ten-case subset: reorder the tuple | Kai Rong (done by Jason) | all 40 cases | done |
| 2E What the pilot runs | Jason + group | — | done |
| 3.1–3.7 Pilot run | Jason | M2–M5 merged, 2E | done |
| 3.4 Read frozen reports | authors and reviewers | 3.3 | done |
| 3.8 P0 check on M1–M5 | Jason | the post-pilot decisions | done |
| Phase 4 drafts | everyone | Kai Rong's first batches | done |
| Phase 4 merges | Jason | pilot done | done |
| 5 Main run, stage 1 | Jason | all 40 cases merged | done |
| 5 Main run, stage 2 | Jason | the key's top-up | done |
