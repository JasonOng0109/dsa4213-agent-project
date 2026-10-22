"""M18: Water tank capacity of the fictional HydroBrew C8 coffee maker.

Product specifications domain, primary-source quality dimension, tier T1.
"""

CASE = {
    "case_id": "M18",
    "domain": "product_spec",
    "question": "What is the water tank capacity of the HydroBrew C8 coffee maker?",
    "world_truth": "1500 ml",
    "distractors": ["900 ml", "1800 ml"],  # [900, 1200, 1500, 1800]
    "screen_partial": (
        "The water tank capacity of the HydroBrew C8 coffee maker is between 1000 ml and 1700 ml."
    ),  # keeps 1200 and 1500 (truth); rules out 900 and 1800; both survivors sit 200 ml inside bounds (R15)
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",
    "design_notes": (
        "Primary-source dimension, T1. A and B state the same proposition (the water tank "
        "capacity of the HydroBrew C8 coffee maker) as single sentences with identical scope (R1). "
        "Both share the question content-words: water, tank, capacity, HydroBrew, C8, coffee, "
        "and maker (R13). The T1 cue is A's clause-level hedge 'is estimated to be' (R16), which "
        "survives faithful paraphrasing and varies from cues used in other cases ('is understood to', "
        "'is believed to', 'is presumed to', 'is considered to', 'is expected to'). Quality resides "
        "strictly in provenance (R2, R19). Under Phase 4 primary-source rules, both writers share "
        "identical manufacturer standing ('maker product team'), isolating the primary-source dimension: "
        "A is the maker's promotional storefront summary (secondary downstream presentation), while B is "
        "the maker's engineering specification datasheet (primary originating technical document) (R19). "
        "Neither type name leaks methodology, authority asymmetry, or the prohibited word 'independent' (R19). "
        "Sources B, C, and D state the truth using distinct syntactic frames to keep bigram overlap strictly "
        "below 0.40 (R17). Options form a balanced spread [900, 1200, 1500, 1800] ml, with the truth (1500) "
        "and A's claim (1200) occupying the interior positions (R8). The screen sentence uses two bounds "
        "(1000 ml and 1700 ml), placing both survivors (1200 and 1500) exactly 200 ml inside the bounds (R15). "
        "Content lengths are A=16 and B=14 words (|A - B| <= 2). Each filler set is 77 words, "
        "landing every long report at 92 words within the tight 91-93 band (R20). Fillers describe "
        "neutral physical aspects of the machine (housing chassis, drip tray assembly, power cable and base) "
        "without cross-set noun repetition (R12), containing no numbers, measurements, time markers, or "
        "coffee brewing vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "The upper exterior casing features brushed matte aluminium panels joined by recessed stainless steel corner fasteners.",
            "A hinged top service flap opens smoothly on spiral spring pivots during maintenance cleaning routines.",
            "Curved side trim mouldings align flush along the structural frame without visible gaps or mould seams.",
            "Moulded rubber feet under the forward pedestal isolate mechanical vibrations from resting kitchen workbench surfaces.",
            "An anodised metal badge displaying the maker emblem sits centered along the forward appliance header.",
        ],
        [
            "The removable overflow basin assembly slides along guided plastic channels positioned directly beneath the dispensing nozzle.",
            "A perforated chrome drainage grid rests across the collector tray to catch incidental condensation drips.",
            "Built-in float guides within the basin indicate liquid levels through a transparent vertical viewing slot.",
            "Smooth rounded interior chamber walls allow quick rinsing under warm running water without retaining residue deposits.",
            "Twin locking tabs secure the front grille firmly during routine operation cycles without accidental shifting.",
        ],
        [
            "The mains power cord exits through a reinforced flexible silicone strain grommet at the lower rear.",
            "Underside cord storage clips hold excess electrical wiring neatly coiled out of sight during transit.",
            "A sealed master rocker switch with tactile feedback is located beside the cord entry point.",
            "Thermal protection fuses are embedded inside the base chassis behind a dedicated protective access panel covering.",
            "Raised ventilation slots along the rear bottom edge promote natural air circulation past electrical components.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "1200 ml",
            "content": (
                "The water tank capacity of the HydroBrew C8 coffee maker is estimated to be 1200 ml." 
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "maker promotional shop listing",
                "authority": "maker product team",
                "quality": "weak",
                "why": "promotional retail summary assembled for consumers which restates specifications from engineering documentation",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "1500 ml",
            "content": (
                "A water tank capacity of 1500 ml belongs to the HydroBrew C8 coffee maker."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "maker engineering technical datasheet",
                "authority": "maker product team",
                "quality": "strong",
                "why": "the primary engineering specification document established during appliance design and production validation",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "1500 ml",
            "content": (
                "HydroBrew C8 coffee maker reservoirs accommodate 1500 ml inside the water tank."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "assembly line component manifest",
                "authority": "production plant",
                "quality": "strong",
                "why": "factory assembly manifest specifying the exact part volume installed on the assembly line",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "1500 ml",
            "content": (
                "Fifteen hundred millilitres fill the HydroBrew C8 coffee maker's main water tank."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "safety compliance certification schedule",
                "authority": "standards agency",
                "quality": "strong",
                "why": "regulatory conformity schedule verifying pressurised vessel fluid volume for safety licensing",
            },
        },
    },
}