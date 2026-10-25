# Methods

How the study's statistical methods work, in plain English with worked examples. This
is the shared dictionary: the knowledge graph's concept nodes summarise its entries and
quote them, and `docs/decisions.md` says why each method was chosen.

Every entry has the same five parts: **In one line**, **How it works**, **Worked
example**, **Reading the number**, and **In the code**. Add an entry when a method or
term needs more than a sentence to explain.

- [Page's test](#pages-test)
- [Significance level](#significance-level)
- [Margin](#margin)
- [AUROC](#auroc)

---

## Page's test

**In one line.** A test of whether a judge's numbers rise in a predicted order, across
many cases at once. The confidence screen uses it to check that P(truth) rises from P0
(an irrelevant report) to P1 (a report narrowing the options to two) to P2 (a report
naming the answer).

**How it works.**

1. **Rank within each case.** A case's three P(truth) values become ranks: lowest 1,
   highest 3. Ranks ignore the judge's scale: 25, 50, 55 and 40, 60, 99 are both in the
   predicted order, and both rank 1, 2, 3. Tied values share the average of their
   ranks, so 25, 25, 90 ranks 1.5, 1.5, 3.
2. **Score each case.** Multiply each rank by its predicted position (P0 is 1, P1 is
   2, P2 is 3) and add:

   | The case's order | Ranks of P0, P1, P2 | Score |
   |---|---|---|
   | as predicted | 1, 2, 3 | 1×1 + 2×2 + 3×3 = 14 |
   | P1 and P2 swapped | 1, 3, 2 | 13 |
   | P0 and P1 swapped | 2, 1, 3 | 13 |
   | P2 lowest | 2, 3, 1 | 11 |
   | P0 highest | 3, 1, 2 | 11 |
   | reversed | 3, 2, 1 | 10 |
   | all three tied | 2, 2, 2 | 12 |

   A judge guessing at random averages 12. A case that is nearly right still scores
   above 12, so a judge gets partial credit for it, unlike a rule that counts only
   perfectly ordered cases.
3. **Add up over cases.** The total is Page's L.
4. **Compare with chance.** If a judge's numbers had nothing to do with how informative
   a report is, each case would land in one of its six orders at random, like a roll of
   a die. The cases are independent, so the chance that such a judge's L comes out at
   least as high as the one observed can be counted exactly. That chance is the p-value.
   With ties, the count runs over the orders of the tied ranks.

Each case is compared only with itself, so differences between cases, such as some
questions simply feeling more certain than others, cancel out. A case's four rotations
are averaged before ranking: they share one case, so they are not independent evidence.

**Worked example.** A judge gives 25, 50, 90 on one case and 25, 90, 50 on another.
The scores are 14 and 13, so L = 27. Of the 36 equally likely pairs of orders, 5 reach
27 or more, so p = 5/36 = 0.139: not enough to pass. Add three more cases in the
predicted order and L = 69 over five cases, with p = 0.0014: it passes.

**Reading the number.** The scorer prints L, the p-value and a rank correlation: L
rescaled to run from −1 (every case reversed) through 0 (no ordering) to +1 (every case
in order). For n cases it is L ÷ 2n − 6. Without ties it equals the mean Spearman
correlation between the predicted and the observed order, which is the "rank
correlation" the proposal asks for. The worked example's L of 27 over two cases gives
0.75.

**In the code.** `page_test` and `screen_verdict` in `pipeline/score.py`. Why this
test and not another: `docs/decisions.md`.

---

## Significance level

**In one line.** The pass mark for a p-value. The screen's level is 0.05, one-sided: a
judge passes the ordering check when p is below 0.05.

**How it works.** A p-value answers one question: if the judge's numbers carried no
ordering at all, how often would luck alone produce a result at least this good? The
level is where the line is drawn. At 0.05, a judge whose numbers carry no ordering
still passes 1 time in 20. That is the false-pass rate the study accepts.

It is not "95% sure the judge is good". A p-value measures how surprising the result
would be from a judge with no ordering, not how likely this judge is to be a good one.

**Worked example.** Dice make it concrete. With no ordering, one case lands in the
predicted order 1 time in 6.

| Cases, all in the predicted order | p | Passes at 0.05? |
|---|---|---|
| 1 | 1/6 = 0.167 | no: luck does this too often |
| 2 | 1/36 = 0.028 | yes |
| 3 | 1/216 = 0.005 | yes |

The level also sets how many cases a fair test needs. Here one case is fully reversed
and the rest are in the predicted order:

| Cases | p | Passes at 0.05? |
|---|---|---|
| 2 | 0.639 | no |
| 3 | 0.278 | no |
| 4 | 0.109 | no |
| 5 | 0.039 | yes |

So 5 is the fewest cases at which one bad case cannot fail a judge by itself, which is
why the pilot uses 5.

**Reading the number.** One-sided means only rising numbers count as evidence: a judge
whose numbers fall gets a large p and never passes. A stricter level, such as 0.01,
lets fewer judges with no ordering through, but a real judge then needs more cases to
pass. The level is fixed before the pilot, because choosing it after seeing results
would let the data pick its own pass mark.

**In the code.** `SCREEN_ALPHA` in `pipeline/score.py`. The team's decision, and the
pilot size it implies, are in `docs/decisions.md`.

---

## Margin

**In one line.** How far the judge's top option leads the runner-up: its highest stated
probability minus its second highest, in points. H6 counts a margin below 10 as near
indifference.

**How it works.**

1. The judge states a probability for each of the four options. The scorer rescales
   them to sum to 100, and takes the margin after rescaling: numbers that add up to
   more than 100 shrink the lead, and numbers that add up to less stretch it.
2. Sort them from highest to lowest. The margin is the first minus the second. A tie at
   the top is a margin of 0.
3. H6 flags a forced-choice record whose numbers do not identify the answer it gave:
   either the answer is not its highest option (incoherent), or the margin is below 10.

Coherence and the margin catch different things. Coherence catches a judge that thinks
one answer and gives another. The margin catches a near-level spread behind a
confident-looking answer: 34/33/33/0 is coherent, yet says almost nothing.

**Worked example.** The judge gives the first option as its answer each time.

| Stated probabilities | Margin | Flagged? |
|---|---|---|
| 34 / 33 / 33 / 0 | 1 | yes: near indifference |
| 50 / 45 / 3 / 2 | 5 | yes: near indifference |
| 50 / 40 / 5 / 5 | 10 | no: it leans one way |
| 50 / 40 / 10 / 5 | 9.52 | yes: they add up to 105, so rescaled it is 47.62 against 38.10 |
| 90 / 5 / 3 / 2 | 85 | no |
| 40 / 50 / 5 / 5 | 10 | yes: incoherent, since the answer is not the top option |

**Reading the number.** Below 10 counts a tie, or a lead of a few points such as 50
against 45, as near indifference; for a judge that writes in steps of 5 and whose
numbers add up to 100, that is a tie or one step from one. H6 then asks whether the
judge, when it is allowed to abstain, abstains more in those same trials than in the
rest, against its own abstention rate in A7. It compares inside each condition and
then combines the conditions: pooled, a condition with more of both close numbers and
abstaining would look like H6 even if no single trial showed it. The scorer also prints
that comparison at margins of 5 and 20, declared in advance to show how much the result
depends on the cut-off; the conclusion rests on 10.

**In the code.** `margin` and `coherent` in `_parse_object` in `pipeline/judge.py`;
`MARGIN_THRESHOLD`, `unbacked`, `_mh_difference` and `report_h6` in `pipeline/score.py`.
Why 10: `docs/decisions.md`.

---

## AUROC

**In one line.** The chance that a right decision carries a higher stated probability
than a wrong one. 0.5 means the number carries no information about being right. The
discrimination check uses it; since the pilot that check is reported beside the
confidence screen, not part of it.

**How it works.**

1. Take one judge and one condition on the short arm. Split its decisions into right
   and wrong, and note the probability it stated for the answer it gave.
2. Compare every right decision with every wrong one. Count 1 when the right one
   carries the higher number, ½ when they tie, 0 otherwise.
3. AUROC is that count divided by the number of pairs.

It is computed within one condition. Across conditions it would mostly measure the
manipulation: a judge is right more often, and surer, in some conditions than in others.

The p-value says how often a judge whose numbers carry no information would reach at
least this AUROC by luck. The unit is the case, not the decision. A case's repeats are
near-copies: only the order of the options and reports changes, and a judge asked one
prompt again answers almost alike (`docs/decisions.md`, 2026-10-26), so the judge
answers them almost alike, and twelve copies of one answer are not twelve pieces of
evidence. So the p-value shuffles whole cases. Each shuffle scores every
case's stated numbers against another case's right-and-wrong record, repeat by repeat,
and p is the share of 2,000 shuffles, from a fixed seed, that reach at least the
observed AUROC. Counting each decision instead, as the Mann-Whitney test does, makes p
far too small: with ten cases of twelve repeats, a judge whose numbers carry no
information would pass about 1 time in 4. With few cases, luck alone moves AUROC far
from 0.5; with many, it stays close.

**Worked example.** Stated probabilities when right: 90, 80. When wrong: 70, 85. The
pairs: 90 > 70 yes, 90 > 85 yes, 80 > 70 yes, 80 > 85 no. That is 3 of 4, so
AUROC = 0.75. If each decision comes from a different case, the shuffles deal the four
numbers into two right and two wrong in six ways: 90 and 85 right gives 1, 90 and 80
gives 0.75, 90 and 70 or 85 and 80 give 0.5, 85 and 70 gives 0.25, 80 and 70 gives 0.
Two of the six reach 0.75, so luck does this 1 time in 3: p = 1/3.

**Reading the number.**

- Above 0.5, the judge is surer when it is right; below 0.5, surer when it is wrong. A
  judge that states the same number on every answer scores exactly 0.5, with p = 1.
- The check, as first registered, passes a judge when at least one condition with 10
  right and 10 wrong decisions has p below 0.05 divided by the number of such
  conditions; A0 never counts. Dividing keeps the false-pass rate at about 1 in 20
  however many conditions count, since each extra condition is one more chance to pass
  by luck.
- Since the pilot that verdict is printed but excludes no judge. In this study a
  condition fixes what the judge sees, and in the pilot every wrong answer was the two
  agreeing reports' claim, so a low AUROC there shows a judge surer when it follows
  them, not numbers without information.
- A fixed AUROC mark would not hold that rate. At 12 right and 48 wrong independent
  decisions, a judge whose numbers carry no information reaches 0.60 by luck more than
  1 time in 10, but passes the test about 1 time in 20.

**In the code.** `auroc`, `auroc_p` (with `SHUFFLES` and `SHUFFLE_SEED`),
`discrimination_verdict` and `report_discrimination` in `pipeline/score.py`. Why this
rule, why the case is the unit, and why the check no longer excludes: `docs/decisions.md`.
