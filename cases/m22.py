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
        "The battery capacity of the Persian X5 Smartphone is under 5000mAh."
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
        "authority: A relays a friend's remark, while B's poster checked their "
        "own unit, so the pair differs in directness alone, not in authority, "
        "medium or method (R19). C and D also come from people who handled the "
        "device. "
        "Type names avoid every subject word a paraphrase would need (R2a). "
        "The options are evenly spaced 600mAh apart (4100, 4700, 5300, 5900mAh), "
        "so the truth and A's claim are the two interior values (R8). "
        "The screen sentence keeps 4100mAh and 4700mAh and rules out 5300mAh and "
        "5900mAh (R15). "
        "A and B share exactly the question words battery, capacity, Persian, X5 "
        "and Smartphone (R13), but use different frames. C ('a ... capacity "
        "battery sits in') and D ('the battery inside each ... has ... of "
        "capacity') use two further frames, so no co-occurring pair shares more "
        "than three bigrams (R17). "
        "Filler describes only the casing, the display and the frame edges and box "
        "contents, never the battery, charging, power use or running time, so it "
        "bears on no option (R9-R12). It never implies that its writer opened the "
        "box or handled the device, so no slot carries a directness cue (R10). "
        "Each filler set is exactly 81 words, and A's and B's sentences are 12 and "
        "10 words, so the set plus A is 93 words and the set plus B is 91 words, "
        "and any accepted rewording still lands between 88 and 96 (R20)."
    ),
    "filler_sets": [
        [
            "The device has a flat glass front and a matte aluminium frame.",
            "Its rear panel is made of frosted glass in a deep blue shade.",
            "Two camera lenses sit in a raised square near the top corner.",
            "A small flash and a microphone hole sit beside the camera lenses.",
            "The volume buttons and the power button run along the right edge of "
            "the frame.",
            "The corners of the frame are rounded.",
            "A thin antenna line crosses the frame near each end.",
        ],
        [
            "The display stretches almost to the edges of the front glass.",
            "A small round cutout near the top of the display holds the front "
            "camera.",
            "A thin earpiece slot runs along the upper edge above the display.",
            "The screen can be split so that two apps show side by side.",
            "A fingerprint reader is built into the lower part of the display.",
            "The screen shows its home and back controls as "
            "small white icons in a strip along the lower edge.",
        ],
        [
            "A SIM tray sits in the left edge of the frame and opens with a small "
            "pin.",
            "The bottom edge holds a speaker grille and a single port.",
            "A clear protective case in the box fits around the frame.",
            "The device comes in a white cardboard box with the model name on the "
            "lid.",
            "Transparent rubber seals around the buttons help keep out dust and "
            "splashes.",
            "A soft cloth for wiping the glass also comes with the device in the "
            "box.",
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
                "why": "first-hand: the poster checked the capacity on a "
                    "unit they own",
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
                "why": "first-hand: a repairer noted the capacity while replacing "
                    "a cracked back panel on an opened unit",
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
                "why": "first-hand: a reviewer recorded the capacity from the "
                    "device's own settings screen",
            },
            "content": ("The battery inside each Persian X5 Smartphone "
                        "has 4700mAh of capacity."),
            "n_paraphrases_needed": 1,
        },
    },
}