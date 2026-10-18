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
            "Each filler set is exactly 81 words and A's and B's sentences are 12 and 10 "
            "words, so the set plus either sentence is 91 to 93 words, "
            "and any accepted rewording still lands between 88 and 96 (R20)."
    ),
"filler_sets": [
        [
            "The plastic body houses the main motor, "
            "and the rubber wheels roll smoothly across hard floors.",
            "A flexible intake hose connects to the front port, "
            "while the metal extension wand locks into position.",
            "Standard floor brushes attach firmly to the end of the wand. ",
            "A rotating bristle brush handles deep carpets while a "
            "parquet tool protects hard floors.",
            "The retractable power cord spools inside the housing.",
            "A paper dust bag fits inside the main compartment "
            "behind the hinged front access door.",
        ],
        [
            "An ergonomic upper carrying handle moulded in the body provides a "
            "comfortable grip.",
            "Dual bright LED headlights with three adjustable "
            "intensity settings illuminate dark areas "
            "underneath heavy furniture.",
            "The main structural body is sleek metallic silver in colour "
            "with contrasting blue bumpers to cushion impact.",
            "A large foot pedal at the back of the body "
            "switches the machine on and off.",
            "A washable exhaust filter captures microscopic allergens.",
            "A transparent dust level indicator window shows when the "
            "dust bag needs emptying.",
        ],
        [
            "A flexible swivel steering neck pivots smoothly around "
            "narrow furniture legs and tight room corners.",
            "A fully charged battery provides forty-five minutes of "
            "continuous cleaning runtime with "
            "remaining charge shown clearly on "
            "an LED display.",
            "Advanced noise reduction insulation layers line "
            "the inner motor chamber for very quiet operation.",
            "A touch-free debris release latch empties collected "
            "contents directly into outdoor bins without hand contact.",
            "Three adjustable suction intensity settings "
            "handle different floor types.",
            "A blowing function clears away loose debris quickly.",
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
                "type": "accredited laboratory report",
                "authority": "institutional",
                "quality": "strong",
                "why": "independent laboratory test report using calibrated pressure sensors",
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
