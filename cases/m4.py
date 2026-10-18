"""M4: the water lift of the Yhotak B162 Vacuum.

Product specification, method dimension, tier T1.
"""

CASE = {
    "case_id": "M4",
    "domain": "product_spec",
    "question": "What is the water lift of the Yhotak B162 Vacuum?",
    "world_truth": "6000Pa",
    "distractors": ["2000Pa", "8000Pa"],      # plausible, unsupported, same kind as the truth
    "screen_partial": (
        "The water lift of the Yhotak B162 Vacuum is more than 5000Pa."
    ),   # screen level P1:
        #true, keeps the truth, rules out 2000Pa and 4000Pa.
    "quality_dimension": "method",
    "difficulty_tier": "T1",

"design_notes": (
        "A and B state the same proposition with different values (4000Pa vs 6000Pa), in "
        "one sentence each, naming the same metric, with no reference to any change or to "
        "each other. The quality dimension is method (provenance), while the intended "
        "textual cue is A's hedge ('is understood to be'), chosen to "
        "survive paraphrasing (R1, R2, R16). "
        "All quality information sits in provenance, which the reporter never sees. "
        "B, C, and D state the fact in three different sentence frames "
        "so their paraphrases cannot converge (R17). "
        "Filler is neutral and assigned by report slot, not source (R9-R12). "
        "Each filler set is exactly 78 words and A's and B's sentences are 12 and 10 "
        "words, so every long report lands between 88 and 90 words, meeting the "
        "required 88 minimum with room for rewording (R20)."
    ),
# Filler sets with exactly 78 words each.
"filler_sets": [
        [
            "The plastic body houses the main motor assembly, "
            "and the rubber wheels roll smoothly across hard floors.",
            "A flexible black intake hose connects securely to the front port, "
            "while the metal extension wand locks into position.",
            "Standard floor brushes attach firmly to the end of the wand, "
            "and the retractable power cord spools inside the housing.",
            "A disposable paper dust bag fits snugly inside the main compartment"
            "behind the hinged front access door.",
            "The machine features a finish.",
        ],
        [
            "The robust outer body shields internal components, "
            "while smooth caster wheels support very easy maneuverability.",
            "A reinforced suction hose attaches near the base, "
            "and the telescoping wand adjusts to user height.",
            "Interchangeable brush heads clip onto the nozzle fitting,"
            "and the electrical cord winds around side hooks.",
            "A cloth dust bag captures fine debris before exhaust air"
            "passes through the final filter.",
            "The primary chassis is painted in a metallic silver tone"
            "with contrasting dark blue protective bumpers.",
        ],
        [
            "The lightweight polycarbonate body balances stability,"
            "and rubberized wheels prevent scratching on timber floors.",
            "A corrugated intake hose channels airflow upward, "
            "and the rigid metal wand connects to the cleaning head.",
            "Rotating bristle brushes agitate carpet fibers during operation,"
            "and the bright yellow power cord remains visible.",
            "A synthetic dust bag slides into internal tracks, "
            "sealing completely when the lid is closed.",
            "The machine sports a matte white color scheme accented"
            "by chrome trim along the upper edge.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "4000Pa",
            "provenance": {
                "type": "retailer Q&A reply",
                "authority": "individual",
                "quality": "weak",
                "why": "based on informal estimate by store customer service "
                    "without standardized testing controls",
            },
            "content": ("For the Yhotak B162 Vacuum, "
                        "water lift is understood to be 4000Pa."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "6000Pa",
            "provenance": {
                "type": "independent laboratory report",
                "authority": "institutional",
                "quality": "strong",
                "why": "accredited laboratory test report using calibrated pressure sensors",
            },
            "content": ("The water lift of the Yhotak B162 Vacuum "
                        "is 6000Pa."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "6000Pa",
            "provenance": {
                "type": "certified datasheet",
                "authority": "institutional",
                "quality": "strong",
                "why": "the manufacturer's own engineering measurement",
            },
            "content": ("A 6000Pa water lift rating is "
                        "specified for the Yhotak B162 Vacuum."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "6000Pa",
            "provenance": {
                "type": "third-party audit report",
                "authority": "institutional",
                "quality": "strong",
                "why": "a separate test of a shop-bought unit by an outside auditor",
            },
            "content": ("The Yhotak B162 Vacuum delivers "
                        "6000Pa of water lift."),
            "n_paraphrases_needed": 1,
        },
    },
}
