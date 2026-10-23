"""M28: the burn time of the Tavrenne T4 candle.

Product specification, primary source dimension, tier T1.
"""

CASE = {
    "case_id": "M28",
    "domain": "product_spec",
    "question": "What is the burn time of the Tavrenne T4 candle?",
    "world_truth": "40 hours",
    "distractors": ["30 hours", "60 hours"],
    "screen_partial": (
        "The burn time of the Tavrenne T4 candle is between 25 and 45 hours."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the burn time of the Tavrenne "
        "T4 candle, with different values, the same scope and precision, and no "
        "reference to a change or to each other (R1). "
        "T1: A's cue is the hedge 'is taken as' (R16), not used by any other "
        "case. "
        "Primary source only: A and B both come from the brand "
        "('institutional'), but A is a social media post restating the figure "
        "while B is the product specification that defines it, so the pair "
        "differs in primary versus secondary source, not authority or method "
        "(R2, R19). B, C and D all give the rated burn time, so the three "
        "agreeing sources state the same figure in A7. "
        "The options are evenly spaced, with the truth and A's claim as the two "
        "interior values (R8). The screen sentence gives a range whose bounds "
        "sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words burn, time, Tavrenne, T4 and "
        "candle (R13); A, B, C and D use four different frames (R17). "
        "Filler describes one part of the candle per set (the jar, the lid, the "
        "underside), shares no meaningful word across sets, and never mentions "
        "the wick, the flame, the amount of wax, size or packaging (R9-R12). "
        "Each filler set is 80 words and A and B are 13 and 11 words, so long "
        "reports are 93 and 91 words (R20)."
    ),
    "filler_sets": [
        [
            "The candle is set in a jar of frosted green glass.",
            "The jar has straight sides and a rounded rim.",
            "The wax inside the jar is a pale cream colour.",
            "The brand name is printed in white on the front of the jar.",
            "A raised pattern of leaves runs around the lower part of the jar.",
            "A ridge of glass circles the jar just below the rim.",
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
            "The grain of the wood crosses the lid from edge to edge.",
        ],
        [
            "The underside rests on a disc of grey wool felt.",
            "The felt is trimmed to a circle.",
            "A logo in the shape of a sun is pressed into the felt.",
            "The felt is glued in position over the bottom surface.",
            "A model code is stamped in black beside the logo.",
            "The disc has a stitched border in black thread.",
            "Rubber dots are spaced evenly along the outside of the disc.",
            "The sun in the logo is coloured gold and orange.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "50 hours",
            "provenance": {
                "type": "brand's social media post",
                "authority": "institutional",
                "quality": "weak",
                "why": "secondary: a promotional post restating the figure from "
                    "the brand's specification",
            },
            "content": ("The burn time of the Tavrenne T4 candle is taken as "
                        "50 hours."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "40 hours",
            "provenance": {
                "type": "brand's product specification",
                "authority": "institutional",
                "quality": "strong",
                "why": "primary: the specification that defines the rated burn "
                    "time",
            },
            "content": ("Each Tavrenne T4 candle lasts for 40 hours of burn "
                        "time."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "40 hours",
            "provenance": {
                "type": "retailer's burn test record",
                "authority": "institutional",
                "quality": "strong",
                "why": "a retailer's standard test confirmed the rated burn time",
            },
            "content": ("Tavrenne rates the T4 candle at 40 hours of burning."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "40 hours",
            "provenance": {
                "type": "trade association register",
                "authority": "institutional",
                "quality": "strong",
                "why": "lists the rated burn time filed for the candle",
            },
            "content": ("Once lit, a Tavrenne T4 candle goes out after 40 "
                        "hours."),
            "n_paraphrases_needed": 1,
        },
    },
}