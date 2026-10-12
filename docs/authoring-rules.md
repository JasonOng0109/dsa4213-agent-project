# Rules for writing cases

Every case is the study's raw material, so a careless case can make a whole condition
measure nothing. This file is the single source for how cases are written. Each case is
checked against it by its author and **again by a reviewer who did not write it**: the
most damaging defect, specificity asymmetry, cannot be caught by any script.

Terms: **content** is the one operative sentence stating a source's claim; **filler** is
the neutral padding used to build long reports; **provenance** is the structured record of
who produced a source and how good it is, which the reporter model never sees.

## What a case contains

| Field | What it holds |
|---|---|
| `case_id` | short id, e.g. `M1` |
| `domain` | `institutional_logistics`, `product_spec` or `incident_status` |
| `question` | an open-valued question about a fictional fact |
| `world_truth` | the correct answer |
| `distractors` | exactly two plausible answers that no source supports |
| `screen_partial` | one sentence for the confidence screen (R15) |
| `quality_dimension` | `authority`, `directness`, `method` or `primary_source` |
| `difficulty_tier` | `T1` if a mild content cue survives paraphrasing, `T2` if the pair is near-symmetric |
| `design_notes` | the author's reasoning, for the reviewer |
| `filler_sets` | exactly three lists of filler sentences, one per report slot (R12) |
| `sources` | exactly `A` (weak, wrong claim) and `B`, `C`, `D` (strong, the truth) |

Each source holds `quality`, `claim`, `content`, `n_paraphrases_needed` and
`provenance = {type, authority, quality, why}`. The answer options are **not** a field:
the builder assembles them from the truth, A's claim and the distractors (R5).

**Tiers.** Aim for about three T1 cases per T2 case (roughly 30 and 10 at 40 cases), with
the T2 cases spread across domains and quality dimensions. T1 is where a decision-level
result is possible; T2 is the control for whether a dependence statement discounts the
count at all, so for T2 the outcome to read is belief, not accuracy.

---

## The rules

Rules marked **[lint]** are checked by the static linter. The rest need a person.
Run it after every edit to a case, and before asking for review:

```bash
uv run python -m pipeline.lint
```

Register a new case in `cases/__init__.py` first, or the linter will not see it.

**R1 — Symmetry of the competing pair.** A and B state the same proposition with
different values, as flat, confident, equally specific assertions. Neither refers to the
other, to a change, a revision or an "original" value. *Equally specific includes naming
the same denominator or scope*: if B says "of the final module grade", A may not leave
the denominator implicit. **[lint]** for supersession, staleness and hearsay wording.

**R2 — Quality lives in provenance.** Everything about who produced a source, how, and
how reliable it is goes in `provenance`. The reporter is handed `content` only. At most a
**mild** cue may survive into content, such as an impersonal register against a
conversational one. **[lint]** for attribution words and a complete provenance record.

**R2a — Write `provenance.type` with words the content does not need.** Every word in
`type` that appears in neither the content nor the question becomes a banned word for
that source's paraphrases, so an ordinary word there rejects good paraphrases. "Module
coordinator announcement to enrolled students" bans *module*, which any paraphrase of a
module's grade might use; "coordinator announcement" is safer. **Name the source, not its
subject.**

**R3 — No time markers.** Content, filler and the screen sentence carry no dates,
recency words or staleness markers. Source quality must not be readable as recency.
**[lint]**

**R4 — Fictional facts.** Entities and their facts are invented, so no judge can answer
from prior knowledge. Realistic naming (a plausible course code) is fine; a checkable
real-world fact is not.

**R5 — Options are built, not authored.** The author supplies the truth and two
distractors. Option order comes from the builder's rotation, so position balance is
guaranteed by construction. **[lint]**

**R6 — C and D may be more direct than B.** They appear only where all three reports
agree, never opposite a conflicting report, so they cannot supply a comparison cue.

**R7 — Content is self-contained.** Each content sentence names its own subject and
never relies on provenance for a referent.

**R8 — Distractors.** Exactly two. Each is the same kind of answer as the truth, is
supported by no source, is excluded by no report, and appears nowhere in any content,
filler or provenance. Prefer option sets where the truth and the wrong claim are both
interior values, so "avoid the extremes" is not a winning heuristic. **[lint]** for the
count and for mentions.

**R9 — Filler does not bear on the question.** It may not support, exclude or hedge any
option, and may not mention one. **[lint]** for mentions.

**R10 — Filler is document-neutral and register-neutral.** It never identifies or
implies who wrote it, never describes its own document type ("each row", "this
announcement"), and uses one plain register in every set. Filler that drifts toward
administrative wording strengthens a cue as reports get longer, which confounds length
with cue strength. **[lint]** for document-type words and second person.

**R11 — One operative sentence.** Each content field is exactly one sentence. Where it
sits inside a long report is set by the builder, not the author. **[lint]**

**R12 — Filler belongs to the report slot, not the source.** A case carries three
interchangeable filler sets, and the builder gives set *i* to slot *i* whichever source
fills it. **Never attach filler to a source**: two reports of one source would then share
their padding word for word, and the opaque conditions would display the dependence they
exist to hide. **[lint]**

**R13 — The question's wording must not distinguish the competing pair.** A and B must
share **exactly the same set** of question content-words, so the question cannot lean
toward one side. A word used by both is symmetric and harmless. Question words present
in some of B, C, D but not others are reported, not enforced: those three only ever
appear together, where nothing can point at a winner. The screen sentence is exempt.
**[lint]**

**R14 — The shared source is always B, the strong one.** The agreement block repeats
evidence that supports the truth; A appears only in the conflict block, repeated twice
against one report of B. So A needs **two** accepted paraphrases, B **three**, C and D
**one** each. This is what lets the independence index read the probability of the
truth. **[lint]**

**R15 — The screen sentence.** `screen_partial` is **one sentence that is true, keeps the
world truth among the survivors, and rules out exactly half the options.** It is level P1
of the confidence screen; P0 is a filler sentence and P2 is B's first frozen paraphrase,
so only this sentence needs writing. It is not a source: it never appears alongside
other reports, and **R8 and R9 do not apply to it**, because ruling out two options is
its job. R1 to R3 and R10 to R13 still apply, since a judge reads it. **[lint]** for
presence, one sentence, and R3/R10 wording.

**R16 — A T1 cue must survive paraphrasing.** The reporter rewords every source, so a cue
carried by one function word is usually lost: a second-person pronoun does not survive.
Prefer cues at the level of the clause, such as a hedge ("is understood to be"), an
approximation, or a standardised notation, and ask: *would a faithful rewording keep
this?* The tier label stays provisional until the frozen reports are read. A case whose
cue is lost is relabelled T2, not rewritten, because a T2 case is a legitimate control.

**R17 — Sources that share a trial use different sentence frames.** B, C and D appear
together in A7; A and B appear together in the conflict block. If two of them state the
fact in the same frame, their faithful paraphrases converge, and the condition meant to
show *independent* agreement shows two reports that read like copies. Bigram overlap
between the `content` of any two co-occurring sources must be **below 0.40**. **[lint]**
The same idea is enforced on accepted paraphrases at the within-source limit of 0.50: two
reports from *different* documents may not look more alike than two from the *same* one.
If a case cannot meet that, re-frame its sources; never loosen the threshold.
**When R13 and R17 pull apart, R17 wins.**

**R18 — Sources are frozen in descending order of paraphrases needed.** B (three) first,
then A (two), then C and D, ties alphabetical. Each source is checked against paraphrases
already accepted for earlier ones, so the source under the tightest constraint gets the
freest choice. Fixed, so runs are reproducible. (The pipeline does this; authors need
only know why.)

**R19 — The source type name carries the case's quality dimension.** H5 asks whether a
judge infers quality from a named source type alone, so the name must convey the
dimension the case is built on.

| Dimension | A weak type name | A strong type name |
|---|---|---|
| Authority | student-run module wiki page | registrar's official examination timetable |
| Directness | summary circulated by a classmate who attended | security patrol log written at the scene |
| Method | retailer question-and-answer reply from a store representative | independent laboratory test report |
| Primary source | online retailer product listing | manufacturer specification sheet |

The test: strip the content and show only the two type names. Would a reader prefer one?
If not, the case cannot serve H5; mark it as testing the other hypotheses only.

---

## Checks no script performs

- **Specificity asymmetry.** Strip both competing statements of provenance and imagine
  them from two anonymous, equally authoritative sources. If either still dominates, by
  scope, by being an exception to the other's general rule, or by naming its terms more
  precisely, the case is broken and nothing else saves it.
- **R15's meaning.** That `screen_partial` is true, keeps the truth and rules out exactly
  half the options is a meaning check. A linter can confirm the field exists, not that it
  does its job.
- **Denominator consistency across the frozen reports.** A's and B's accepted paraphrases
  must refer to the same whole, or their claims stop contradicting each other and the
  conflict block measures nothing. "The total grade for module ME2103" and "the final
  module grade" are the same whole; "the continuous-assessment mark" is not.
- **Cue survival.** For a T1 case, read the accepted paraphrases and confirm the cue is
  still there. If it is not, relabel the case T2.
