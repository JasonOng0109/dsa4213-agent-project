# Methods

How the study's statistical methods work, in plain English with worked examples. This
is the shared dictionary: the knowledge graph's concept nodes summarise its entries and
quote them, and `docs/decisions.md` says why each method was chosen.

Every entry has the same five parts: **In one line**, **How it works**, **Worked
example**, **Reading the number**, and **In the code**. Add an entry when a method or
term needs more than a sentence to explain.

- [Page's test](#pages-test)
- [Significance level](#significance-level)

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
