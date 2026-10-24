"""M34: the packed weight of the Torvik Ridgeline tent.

Product specifications domain, authority dimension, tier T1. A's hedge, "is assumed to",
is the one mild cue, and is meant to survive rewording (R16).
"""

CASE = {
    "case_id": "M34",
    "domain": "product_spec",
    "question": "What is the packed weight of the Torvik Ridgeline tent?",
    "world_truth": "2.9 kg",
    "distractors": ["1.3 kg", "3.7 kg"],   # plausible, unsupported, same kind as the
                                           # truth; even steps of 0.8 kg
    "screen_partial": (
        "The Torvik Ridgeline tent has a packed weight between 2 and 3 kg."
    ),   # screen level P1: true, keeps 2.1 and 2.9 kg, each 0.1 kg inside a bound, and
         # rules out 1.3 and 3.7 kg
    "quality_dimension": "authority",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, the packed weight of the Torvik Ridgeline "
        "tent, with different values, in one sentence each. Both name the same tent and "
        "the same measure, its packed weight, give it in kilograms to one decimal place, "
        "and refer to no change and to no other source (R1). Read without provenance, "
        "neither is narrower, an exception to the other, or more precise. The quality "
        "dimension, authority, lives in provenance; the one cue in the content is A's "
        "clause-level hedge, 'is assumed to', a hedge of the size a faithful rewording "
        "should keep (R16). Whether it survives is only known once the frozen reports "
        "are read; if it is lost, the case is relabelled T2. When this case was written "
        "'assumed to' was in one case, M38 ('are assumed to'), so it was among the "
        "least used. B is flat and carries no cue. The two type names carry the "
        "authority dimension: both are buying guides, so the kind of document is the "
        "same, and they differ only in who stands behind them, a volunteer-run community "
        "newsletter against the maker that sets the tent's specifications (R19). "
        "Neither name says how its figure was found, how close its writer was or that "
        "it copies another; a newsletter, unlike a hiking club, does not suggest people "
        "who weighed the tent themselves. Neither says 'independent', and both name the "
        "source rather than the subject, so no word a rewording needs is banned (R2a). "
        "The maker has the usual interest in a light tent; since its figure is the "
        "higher one, a judge who suspects makers of quoting low weights has a further "
        "reason to back B in X2, so M34's X2 gain may read slightly high. The options "
        "are 1.3, 2.1, 2.9 and 3.7 kg, evenly spaced, so the truth and A's claim are "
        "both interior and equally close to the average: neither 'avoid the extremes' "
        "nor 'pick the middle' finds the truth (R8). The steps are 0.8 kg, so A's "
        "figure cannot be read as the same tent's minimum weight, which sits a few "
        "hundred grams under its packed weight; a gap this wide could suggest a "
        "different size of tent, but that favours neither figure. None is a round "
        "figure, and A's claim is the lower one, so neither a habit for round numbers "
        "nor a belief that unofficial figures run high finds the truth. The options "
        "carry their unit, as the content does. The screen sentence keeps 2.1 and "
        "2.9 kg, each 0.1 kg inside a bound, so 'pick the survivor nearest the bound' "
        "does not find the truth (R15). A and B use the same question words (R13). B, "
        "C and D state the fact in three different frames (R17). C and D are separate "
        "weighings, an outdoor magazine's lab test of a tent it bought for the test and "
        "a consumer association's test of a tent bought from a shop, so neither depends "
        "on the maker's guide or on each other, and neither's sentence says how its "
        "value was found (R2, R6). All three give the packed weight, the tent with its "
        "poles and pegs in its bag, in their content as well as their whys, so B, C and "
        "D support one proposition in A7 (R1). The brand, the tent and its weight are "
        "invented (R4). Filler describes the flysheet and porch in set 1, the inner "
        "tent in set 2, and how the tent is pitched in set 3, with nothing about the "
        "tent's weight, size or packing, nothing that makes it sound heavy-duty or "
        "light, no figures and no second person, written as a plain description, so no "
        "slot carries the feel of either source (R3, R9, R10). No distinctive word is "
        "in more than one set, so the slots stay apart (R12). Each filler set is 79 "
        "words and A's and B's sentences are 14 and 12 words, so every long report "
        "starts at 91 to 93 words and stays inside 88 to 96 after rewording (R20). When "
        "the frozen reports are read (step 3.4), check that A's, B's and C's rewordings "
        "still give the packed weight: 'weighs 2.9 kg' with 'packed' or 'in its bag' "
        "dropped, or a 'trail', 'minimum' or 'carry' weight, would name a different "
        "whole."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # the flysheet and the porch
            "The Torvik Ridgeline tent has a green flysheet with reflective guy lines.",
            "Its seams are taped to seal out driving rain.",
            "A porch at the front is closed by a single zip running from the peak.",
            "The flysheet sits low on every side, close to the grass.",
            "Zip pulls on the flysheet are knotted cords in the same green.",
            "A small vent near the peak can be propped open with a stiff strut.",
            "The finish is dull, not glossy.",
        ],
        [   # the inner tent
            "Inside, the sleeping area is lined with breathable mesh panels.",
            "Pockets sewn into each corner hold torches, phones and glasses.",
            "A ring at the apex takes a hanging lantern.",
            "The groundsheet is a darker shade and curves up at the edges like a tub.",
            "Doors at either end roll back and tie with fabric straps.",
            "Plastic clips let the inner lining be unhooked and dried separately.",
            "The lining is a pale yellow, with a darker trim around the doors.",
        ],
        [   # how the tent is pitched
            "Colour-coded sleeves and hooks show which part fits where.",
            "The poles cross at the top and slot into the sleeves.",
            "Pegging points have short loops of plain black webbing.",
            "Adjustable tensioners keep the walls taut as the wind shifts.",
            "A narrow canopy above the entrance sheds water.",
            "The pole sleeves stand out in a vivid orange.",
            "Pole tips seat in eyelets on tabs along the base.",
            "Pitching starts with the poles, then the hooks are fixed on in turn.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "2.1 kg",
            "provenance": {
                "type": "community newsletter's buying guide",
                "authority": "informal",
                "quality": "weak",
                "why": "a volunteer-run community newsletter's guide, with no standing to "
                       "set or vouch for Torvik's own figures",
            },
            "content": ("The Torvik Ridgeline tent is assumed to have a packed weight of "
                        "2.1 kg."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "2.9 kg",
            "provenance": {
                "type": "manufacturer's buying guide",
                "authority": "manufacturer",
                "quality": "strong",
                "why": "Torvik's own guide to its range, from the maker that sets and "
                       "stands behind the tent's specifications, giving the packed weight "
                       "of the tent with its poles and pegs in its bag",
            },
            "content": "Torvik's Ridgeline tent has a packed weight that comes to 2.9 kg.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "2.9 kg",
            "provenance": {
                "type": "outdoor magazine's lab test",
                "authority": "press",
                "quality": "strong",
                "why": "the magazine's testers weighed a tent they bought for the test on "
                       "lab scales, packed in its bag with its poles and pegs",
            },
            "content": ("Ready to carry in its bag, the Torvik Ridgeline tent weighs "
                        "2.9 kg."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "2.9 kg",
            "provenance": {
                "type": "consumer association test report",
                "authority": "consumer group",
                "quality": "strong",
                "why": "the association weighed a tent bought from a shop, packed in its "
                       "bag with its poles and pegs",
            },
            "content": "A packed Torvik Ridgeline tent tips the scales at 2.9 kg.",
            "n_paraphrases_needed": 1,
        },
    },
}
