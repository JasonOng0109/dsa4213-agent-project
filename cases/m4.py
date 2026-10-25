"""M4: the water lift of the Yhotak B162 Vacuum.

Product specification, method dimension, tier T1.
"""

CASE = {
    "case_id": "M4",
    "domain": "product_spec",
    "question": "What is the water lift of the Yhotak B162 Vacuum?",
    "world_truth": "6000Pa",
    "distractors": ["2000Pa", "8000Pa"],  # plausible, unsupported, same kind as the truth
    "screen_partial": (
        "The water lift of the Yhotak B162 Vacuum is between 5000Pa and 9000Pa."
    ),   # screen level P1:
        #true, keeps the truth, rules out 2000Pa and 4000Pa.
    "quality_dimension": "method",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition with different values (4000Pa vs 6000Pa), in "
        "one sentence each, naming the same metric, with no reference to any change or "
        "to each other. The quality dimension is method (provenance), while the intended "
        "textual cue is A's hedge ('is thought to be'), which should survive "
        "paraphrasing; the frozen reports will show whether it does (R1, R2, R16). "
        "All quality information sits in provenance, which the reporter never sees. "
        "B, C, and D state the fact in three different sentence frames "
        "so their paraphrases cannot converge (R17). "
        "Filler is neutral, assigned by report slot, not source, and no content word "
        "is in two sets (R9-R12). "
        "Each filler set is exactly 81 words and A's and B's sentences are 12 and 10 "
        "words, so the set plus either sentence is 91 to 93 words, "
        "and any accepted rewording still lands between 88 and 96 (R20)."
    ),
    "filler_sets": [
        [
            "The Yhotak B162 Vacuum has a pale grey plastic body with a carry handle "
            "moulded into the top.",
            "Large rear wheels and a small swivelling front castor carry the body "
            "across the floor.",
            "A retractable cord winds into the back of the housing at the press of a "
            "button.",
            "A corrugated hose runs from the front of the body to a curved plastic "
            "grip.",
            "The metal wand slides into the grip and ends in a wide floor head with "
            "soft bristles.",
        ],
        [
            "A hinged cover opens onto the compartment that holds the paper bag.",
            "A clear window in the cover shows how full the bag is.",
            "The bag slots onto a cardboard collar just inside the compartment.",
            "A foot pedal near the compartment switches the vacuum on and off.",
            "Rubber bumpers circle the base to protect furniture from knocks.",
            "A strap holds the folded tubing when it is put away.",
            "Spare bags come in a box of white card with a tear-off lid.",
        ],
        [
            "A crevice tool and a dusting brush clip onto the extension stem.",
            "An upholstery nozzle with a lint strip rests in a cradle.",
            "For upright storage, a hook on the frame takes the extension stem.",
            "A zipped pouch for the tools hangs from a loop on the side.",
            "The model name is printed in neat silver letters on the casing.",
            "A narrow nozzle reaches behind radiators and into tight gaps.",
            "A stair tool with a short stiff brush fits the steps.",
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
                        "water lift is thought to be 4000Pa."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "6000Pa",
            "provenance": {
                "type": "accredited laboratory report",
                "authority": "institutional",
                "quality": "strong",
                "why": "independent laboratory test report using calibrated pressure "
                    "sensors",
            },
            "content": ("Yhotak's B162 Vacuum has a water lift "
                        "that reaches 6000Pa."),
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
