"""M20: Continuous runtime of the AeroGlide T5 vacuum cleaner.

Product specifications domain, method quality dimension, tier T1.
"""

CASE = {
    "case_id": "M20",
    "domain": "product_spec",
    "question": "What is the continuous runtime of the AeroGlide T5 vacuum cleaner?",
    "world_truth": "50 minutes",
    "distractors": ["30 minutes", "60 minutes"],  #[30, 40, 50, 60] 
    "screen_partial": (
        "The continuous runtime of the AeroGlide T5 vacuum cleaner is between 35 minutes and 55 minutes."
    ),  # keeps 40 and 50 (truth); rules out 30 and 60; both survivors sit 5 minutes inside bounds (R15)
    "quality_dimension": "method",
    "difficulty_tier": "T1",
    "design_notes": (
        "Method dimension, T1. A and B state the same proposition (the continuous runtime "
        "of the AeroGlide T5 vacuum cleaner) as single sentences with identical scope (R1). "
        "Both share the exact same six question content-words: continuous, runtime, AeroGlide, "
        "T5, vacuum, and cleaner (R13). The T1 cue is A's clause-level hedge 'is anticipated to be' "
        "(R16), which survives faithful rephrasing and is verified unused across other active cases. "
        "Quality resides purely in provenance (R2, R19): both sources share identical author standing "
        "as appliance testing technicians, isolating method quality via an informal manual stopwatch "
        "observation against an automated digital discharge logging cycle (R19). Neither type name "
        "leaks methodology or authority clues into content, and 'independent' is strictly omitted (R19). "
        "Sources B, C, and D state the truth using distinct syntactic frames to keep pairwise bigram "
        "overlap strictly below 0.40, fully satisfying A7 (R17). Options form a balanced spread "
        "[30, 40, 50, 60] minutes, with the truth (50) and A's claim (40) occupying interior positions "
        "(R8). The screen sentence uses two bounds (35 and 55 minutes), placing both survivors equidistant "
        "at exactly 5 minutes inside the bounds (R15). Content lengths are A=15 and B=14 words "
        "(|A - B| = 0 <= 2). Each filler set is exactly 77 words, landing long reports at exactly "
        "92 words (77 + 15), within the tight 91-93 band (R20). Fillers describe neutral physical "
        "hardware aspects across three separate assemblies (brush head wand, dust cyclone assembly, "
        "charging cradle) with zero content-word overlap across sets (R12), containing no numbers, "
        "time markers, or battery runtime vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "The aluminium tubular extension wand clicks securely into place using a coiled spring-loaded mechanical catch latch.",
            "Soft velvet brush rollers sweep smoothly across polished wooden floorboards without creating visible scratch marks.",
            "Dual articulated swivel pivot joints allow agile steering navigation around low wooden dining room furniture.",
            "An integrated forward lighting strip illuminates shadowed floor corners beneath heavy wardrobes during regular cleaning tasks.",
            "Durable thermoplastic bumper guards shield baseboards from accidental scrapes during active forward floor sweeping passes.",
        ],
        [
            "The transparent debris collection cylinder empties directly downward through an intuitive rapid-action hinged bottom hatch mechanism.",
            "A fine conical metal mesh separator spins incoming air to remove coarse dirt debris immediately.",
            "Washable multi-layer pleated fabric intake inserts capture fine airborne particles before exhausting ventilation air completely outside.",
            "Flexible silicone sealing rings maintain full airtight pressure integrity between interior filtration compartments without leakage.",
            "An ergonomic top grip handle incorporates tactile patterned ribbing to prevent slipping while carrying containers.",
        ],
        [
            "The modular wall hanging charging cradle features twin magnetic contact pins designed for seamless conductive coupling.",
            "Rigid polymer storage slots hold spare crevice nozzles and narrow upholstery dusting attachments completely safely.",
            "Sturdy steel mounting screws anchor the backplate firmly against solid masonry walls or timber studs.",
            "A compact external transformer plug converts alternating mains domestic electricity through a reinforced insulated conduit lead.",
            "Subtle status illumination diodes pulse gently while docking station connections establish stable domestic contact cycles.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "40 minutes",
            "content": (
                "The continuous runtime of the AeroGlide T5 vacuum cleaner is anticipated to be 40 minutes."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "technician manual stopwatch observation",
                "authority": "testing technician",
                "quality": "weak",
                "why": "informal manual timing logged by an individual technician observing bench operation with a hand stopwatch",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "50 minutes",
            "content": (
                "Under continuous operation, the AeroGlide model T5 vacuum cleaner maintains a 50 minutes runtime."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "technician automated digital logger",
                "authority": "testing technician",
                "quality": "strong",
                "why": "systematic automated electronic test bench logging continuous battery discharge voltage to exhaustion",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "50 minutes",
            "content": (
                "Model T5 cordless appliances by AeroGlide sustain a fifty minutes continuous operating cycle."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "quality assurance bench verification",
                "authority": "inspection specialist",
                "quality": "strong",
                "why": "bench verification ledger stamped during scheduled production quality assurance audits",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "50 minutes",
            "content": (
                "Fifty minutes measures the continuous discharge period of the AeroGlide T5 vacuum cleaner."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "factory endurance test certificate",
                "authority": "certification engineer",
                "quality": "strong",
                "why": "formal industrial endurance certificate verifying continuous operation compliance standards",
            },
        },
    },
}