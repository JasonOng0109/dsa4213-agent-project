"""M28: the burn time of the Tavrenne T4 candle.

Product specification, primary source dimension, tier T1.
"""

CASE = {
    "case_id": "M28",
    "domain": "product_spec",
    "question": "What is the burn time of the Tavrenne T4 candle?",
    "world_truth": "32 hours",
    "distractors": ["26 hours", "44 hours"],
    "screen_partial": (
        "The burn time of the Tavrenne T4 candle is between 29 and 41 hours."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the burn time of the Tavrenne "
        "T4 candle, with different values, the same scope and precision, and no "
        "reference to a change or to each other (R1). "
        "T1: A's cue is the clause-level hedge 'is understood to have' (R16), "
        "shared with M2 (R16 allows at most three per hedge). "
        "Primary source only: A and B both come from the brand "
        "('institutional'), but A is a social media post restating the figure "
        "while B is the product specification that defines it, so the pair "
        "differs in primary versus secondary source, not authority or method "
        "(R2, R19). "
        "B, C and D each come from their own run of the standard burn test (the "
        "brand's own, a retailer's on a candle from its stock, and a trade "
        "association lab's on another shop-bought candle), so no source copies "
        "another in A7. All three give the total hours of burning until the "
        "candle is used up, so they state one measure. "
        "The options are evenly spaced 6 hours apart and none is a round ten, "
        "so neither claim matches a usual burn time printed on candle jars; the "
        "truth and A's claim are the two interior values (R8). The screen "
        "sentence gives a range whose bounds sit equally far from the two "
        "options it keeps (R15). "
        "A and B share exactly the question words burn, time, Tavrenne, T4 and "
        "candle (R13); A, B, C and D use four different frames (R17). "
        "Filler describes one part of the candle per set (the jar, the lid, the "
        "underside), shares no word across sets, and never mentions the wick, "
        "the flame, the amount of wax, size or packaging (R9-R12). "
        "Each filler set is 79 words and A and B are 14 and 13 words, so long "
        "reports are 93 and 92 words (R20)."
    ),
    "filler_sets": [
        [
            "The candle is set in a jar of frosted green glass.",
            "The jar has straight sides and a rounded rim.",
            "The wax inside the jar is a pale cream colour.",
            "The name Tavrenne is printed in white on the front of the jar.",
            "A raised pattern of leaves runs around the base of the jar.",
            "A ridge of glass surrounds the jar just below the rim.",
            "The green of the glass becomes darker near the rim of the jar.",
        ],
        [
            "The lid is made from a single piece of ash wood.",
            "A brass knob is fixed to the centre of the lid.",
            "A ring of cork is fitted beneath the lid.",
            "The upper face of the lid is engraved with a spiral.",
            "The wood has an oiled finish with visible grain.",
            "The edge of the lid is cut at an angle.",
            "The knob is shaped like an acorn.",
            "The grain of the wood crosses the lid edge to edge.",
        ],
        [
            "The underside rests on a disc of grey wool felt.",
            "The felt is trimmed to a circle.",
            "A logo in the shape of a sun is pressed into the felt.",
            "The felt is glued in position over the bottom surface.",
            "A model code is stamped in black beside the logo.",
            "The disc has a stitched border in black thread.",
            "Rubber dots are spaced along the outside of the disc.",
            "The sun in the logo is coloured gold and orange.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "38 hours",
            "provenance": {
                "type": "brand's social media post",
                "authority": "institutional",
                "quality": "weak",
                "why": "secondary: a promotional post restating the figure from "
                    "the brand's specification",
            },
            "content": ("The Tavrenne T4 candle is understood to have a burn time "
                        "of 38 hours."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "32 hours",
            "provenance": {
                "type": "brand's product specification",
                "authority": "institutional",
                "quality": "strong",
                "why": "primary: the specification that defines the rated burn "
                    "time, taken from the brand's own run of the standard burn "
                    "test",
            },
            "content": ("Each Tavrenne T4 candle lasts for 32 hours of burn time "
                        "in all."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "32 hours",
            "provenance": {
                "type": "retailer's burn test record",
                "authority": "institutional",
                "quality": "strong",
                "why": "a retailer's own burn of a T4 candle from its stock, run to "
                    "the standard burn test and timed until the candle was used up",
            },
            "content": "A Tavrenne T4 candle burns for a total of 32 hours.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "32 hours",
            "provenance": {
                "type": "trade association test report",
                "authority": "institutional",
                "quality": "strong",
                "why": "the association's lab burned another shop-bought T4 candle "
                    "to the same standard burn test and timed it until it was "
                    "used up",
            },
            "content": ("It takes 32 hours of burning to use up a Tavrenne T4 "
                        "candle."),
            "n_paraphrases_needed": 1,
        },
    },
}