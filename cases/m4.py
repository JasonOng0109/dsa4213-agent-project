"""M4: the water lift of the Yhotak Model B162 MagicWonder Vacuum Cleaner.

Product specification, method dimension, tier T1. The proposal's Appendix A shows
this case in condition X3.
"""

CASE = {
    "case_id": "M4",
    "domain": "product_spec",
    "question": "What is the water lift of the Yhotak Model B162 MagicWonder Vacuum Cleaner?",
    "world_truth": "6000Pa",
    "distractors": ["2000Pa", "10000Pa"],      # plausible, unsupported, same kind as the truth
    "screen_partial": (
        "The water lift of the Yhotak Model B162 MagicWonder Vacuum Cleaner is more than 5000Pa."
    ),   # screen level P1: true, keeps the truth, rules out 2000Pa and 4000Pa.
    "quality_dimension": "method",
    "difficulty_tier": "T1",          
                                        
    "design_notes": (
        "A and B state the same proposition with different values (4000Pa vs 6000Pa), in "
        "one sentence each, naming the same metric, with no reference to any change or to "
        "each other. The intended cue is method quality -- A relies on an unstandardized "
        "retailer question-and-answer reply, whereas B is from standardized independent laboratory "
        "testing. For T1, A carries a mild hedging hint ('is understood to be') that "
        "survives paraphrasing (R16). All quality information sits in provenance, which the "
        "reporter never sees. B, C, and D state the fact in three different frames so their "
        "paraphrases cannot converge (R17)."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [

        [
            "Inspection logs are collected from the office and signed by a technician before units leave.",
            "Each entry records the apparatus used, pressure measurements taken, and any deviation from standard protocol.",
            "Entries are stored in the asset register, and checklists are attached to the file.",
            "Spare pressure sensors are kept at the counter for anyone who requires one.",
            "Testing shifts are fixed, and the workshop is used.",
        ],  
        [
            "Safety induction is required before anyone may operate high-vacuum test rigs in the workshop.",
            "Laboratory coats and eye protection are provided, and items are left outside.",
            "Apparatus faults are reported to the technician on duty rather than to the department office.",
            "Technician office hours run alongside each session for questions regarding test rigs or procedures.",
            "Units repeating performance audits retain their bench unless a change is requested.",
        ],  
        [
            "Model B162 is a canister vacuum manufactured by Yhotak, and evaluations are conducted.",
            "Bench schedules and unit serial numbers are posted at the workshop entrance and at the office.",
            "Equipment for each suction test is calibrated before the session and returned to storage afterwards.",
            "Technicians work in pairs, and each operator logs independent readings.",
            "Benches are numbered, and the same setup is used for a batch throughout.",
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
                "why": "based on informal estimate by store customer service without standardized testing controls",
            },
            "content": "For the Yhotak Model B162 MagicWonder Vacuum Cleaner, water lift is understood as 4000Pa.",
            "n_paraphrases_needed": 2,  
        },
        "B": {
            "quality": "strong",
            "claim": "6000Pa",
            "provenance": {
                "type": "independent laboratory report",
                "authority": "institutional",
                "quality": "strong",
                "why": "independent laboratory test report using calibrated pressure sensors",
            },
            "content": "The water lift of the Yhotak Model B162 MagicWonder Vacuum Cleaner is 6000Pa.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "6000Pa",
            "provenance": {
                "type": "certified datasheet",
                "authority": "institutional",
                "quality": "strong",
                "why": "official engineering specification derived from lab performance testing",
            },
            "content": "A 6000Pa water lift rating is specified for the Yhotak Model B162 MagicWonder Vacuum Cleaner.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "6000Pa",
            "provenance": {
                "type": "third-party audit report",
                "authority": "institutional",
                "quality": "strong",
                "why": "independent audit verifying compliance with advertised suction specifications",
            },
            "content": "Evaluations show the Yhotak Model B162 MagicWonder Vacuum Cleaner delivers 6000Pa of water lift.",
            "n_paraphrases_needed": 1,
        },
    },
}
