"""M22: the battery capacity of the Persian X5 Smartphone.

Product specification, directness dimension, tier T2.
"""

CASE = {
    "case_id": "M22",
    "domain": "product_spec",
    "question": "What is the battery capacity of the Persian X5 Smartphone?",
    "world_truth": "4700mAh",
    "distractors": ["4100mAh", "5900mAh"],
    "screen_partial": (
        "The battery capacity of the Persian X5 Smartphone is "
        "between 3800mAh and 5000mAh."
    ),  # screen level P1:
        # true, keeps the truth, rules out 5300mAh and 5900mAh.
    "quality_dimension": "directness",
    "difficulty_tier": "T2",

    "design_notes": (
        "A and B state the same proposition with different values (5300mAh vs "
        "4700mAh), in one flat sentence each, both naming the battery capacity of "
        "the whole device, with no hedge, no reference to any change and no "
        "reference to each other (R1). The gap is about 13%, too wide to be read "
        "as a typical capacity against a rated one, so the two claims cannot both "
        "be true and the conflict holds. "
        "The case is T2: A ('has a battery with a capacity of') and B ('the "
        "battery capacity is') share one plain register and neither carries a "
        "textual cue, so the pair is near-symmetric and the outcome to read is "
        "belief, not accuracy. "
        "The quality dimension is directness, held entirely in provenance (R2): "
        "A and B are both forum posts by ordinary posters with 'individual' "
        "authority: A relays a friend's remark, while B's poster read the rated "
        "capacity off their own unit, so the pair differs in directness alone, "
        "not in authority, medium or method (R19). C and D also come from people "
        "who handled the device, and B, C and D all report the rated capacity, "
        "so the three agreeing sources state the same figure in A7. "
        "Type names avoid every subject word a paraphrase would need (R2a). "
        "The options are evenly spaced 600mAh apart (4100, 4700, 5300, 5900mAh), "
        "so the truth and A's claim are the two interior values (R8). "
        "The screen sentence keeps 4100mAh and 4700mAh, each 300mAh inside a "
        "bound, and rules out 5300mAh and 5900mAh (R15). "
        "A and B share exactly the question words battery, capacity, Persian, X5 "
        "and Smartphone (R13), but use different frames. C ('a ... capacity "
        "battery sits in') and D ('the battery inside each ... has ... of "
        "capacity') use two further frames, so no co-occurring pair shares more "
        "than three bigrams (R17). "
        "Filler describes only the device's appearance, one part per set (the "
        "back, the front, the sides), with no meaningful word shared across sets. "
        "It never mentions the battery, charging, power or size, never packaging "
        "or handling, and never the device being switched on, so it bears on no "
        "option and carries no directness cue (R9-R12). "
    ),

    "filler_sets": [
        [
            "The back of the handset is a panel of frosted glass in a deep navy "
            "shade.",
            "A raised square in one corner of the panel holds the camera lenses "
            "and a flash.",
            "Polished metal rings encircle the lenses, and the flash sits between "
            "them.",
            "A microphone opening lies just beside the raised square, level with "
            "the flash.",
            "The brand logo is etched into the middle of the panel in silver.",
            "Below the logo, the model name is printed in grey lettering.",
        ],
        [
            "The front of the device is covered almost entirely by its display.",
            "A black border of uniform width surrounds the whole display.",
            "A round cutout is placed near the top of the display.",
            "An earpiece slot is cut along the top, just above the display.",
            "The display curves at its margins to follow the outline of the device.",
            "Its surface has a glossy finish, in contrast to the black border.",
            "A dark sensor window is placed just beside the earpiece slot.",
        ],
        [
            "A matte aluminium band runs around the sides of the phone.",
            "The volume keys are on the right, next to a longer key in the same "
            "colour.",
            "A SIM tray with a pinhole is set into the band on the left.",
            "The bottom of the band carries a speaker grille of evenly spaced "
            "holes.",
            "Plastic antenna lines cross the band near its ends.",
            "The band has a brushed grain that runs lengthwise.",
            "Clear rubber seals line the gaps around the keys.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "5300mAh",
            "provenance": {
                "type": "forum post relaying a friend's remark",
                "authority": "individual",
                "quality": "weak",
                "why": "secondhand: the poster repeats what a friend told them "
                    "and never handled the device",
            },
            "content": ("The Persian X5 Smartphone has a battery "
                        "with a capacity of 5300mAh."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "4700mAh",
            "provenance": {
                "type": "forum post on the poster's own unit",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand: the poster read the rated capacity "
                "off the settings screen of a unit they own",
            },
            "content": ("For the Persian X5 Smartphone, "
                        "the battery capacity is 4700mAh."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "4700mAh",
            "provenance": {
                "type": "repair job sheet",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand: a repairer noted the rated capacity printed "
                "on the cell while replacing a cracked back panel",
            },
            "content": ("A 4700mAh capacity battery sits in "
                        "the Persian X5 Smartphone."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "4700mAh",
            "provenance": {
                "type": "reviewer's first-hand notes",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand: a reviewer recorded the rated capacity "
                "from the device's own settings screen",
            },
            "content": ("The battery inside each Persian X5 Smartphone "
                        "has 4700mAh of capacity."),
            "n_paraphrases_needed": 1,
        },
    },
}