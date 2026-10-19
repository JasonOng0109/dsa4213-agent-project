"""M14: Cooling loop heat dissipation rate at the Halcyon substation.

Incident status domain, method quality dimension, T2.
Also selected for the length arm and the wording ladder (R20 tight band applies).
"""

CASE = {
    "case_id": "M14",
    "domain": "incident_status",
    "question": "What is the heat dissipation rate of the Halcyon substation cooling loop?",
    "world_truth": "48 kilowatts",
    "distractors": ["36 kilowatts", "62 kilowatts"],  # options: [36, 42, 48, 62]
    "screen_partial": (
        "The heat dissipation rate of the Halcyon substation cooling loop exceeds 40 kilowatts but is below 50 kilowatts."
    ),  # true, keeps 42 and 48 (truth), rules out 36 and 62: exactly half
    "quality_dimension": "method",
    "difficulty_tier": "T2",
    "design_notes": (
        "T2 control case in incident_status, method dimension, also in the length-arm and "
        "wording-ladder subset. A and B state the same proposition as flat, confident, single "
        "sentences with no hedge (R1). Both A and B omit 'rate' from the content, so they share "
        "exactly the same set of question content-words (R13). All quality sits in provenance (R2, R19): "
        "an uncalibrated handheld thermal scan against a calibrated in-line calorimetric audit,"
        "so a reader shown only the two type names prefers the audit. Sources use distinct "
        "frames (R17): A leads with the quantity and 'stands at', B leads with the loop and 'sustains', "
        "C is place-fronted, D is number-fronted. Content lengths are A=12 and B=14 words, within 2 of "
        "each other (R20). Filler set are  77-79 words, any reporter rewording within 3 words still lands in 88-96. "
        "Filler contains no word that appears only in a source's provenance type, no option value, "
        "and no document-type or second-person wording (R9, R10)."
    ),
    "filler_sets": [
        [
            "Perimeter fencing around the transformer yard is inspected along the northern boundary on regular rounds.",
            "Gravel access roads leading to the switchyard are graded and kept clear of loose debris.",
            "Backup diesel generators stay fuelled and connected to the auxiliary supply panels in the plant room.",
            "Lighting masts around the switchyard are checked on routine walkabouts and replaced when a lamp fails.",
            "Surge arresters on the incoming lines sit within fenced compounds beside the main gate and control building.",
        ],
        [
            "Drainage ditches beside the access road are cleared of leaves and silt on a fixed rota.",
            "Cable trenches between the switchgear hall and the yard are covered with marked concrete slabs.",
            "Warning signs at each gate tell visitors to stay on the painted walkways inside the compound.",
            "Spare insulators and fuses are stored on labelled shelves in the maintenance store beside the workshop.",
            "Vegetation along the outer fence is trimmed back so that branches stay clear of the conductors.",
        ],
        [
            "Staff car parking is arranged along the eastern wall, leaving the main gate clear for deliveries.",
            "Fire extinguishers in the switchgear hall are tagged and mounted at head height near each doorway.",
            "Storm drains around the control building are rodded so that rainfall runs off towards the road.",
            "Transformer bunds are fitted with oil sensors, and their covers are lifted for inspection visits.",
            "Visitor safety briefings take place in the entrance lobby before anyone walks through to the yard.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "42 kilowatts",
            "content": (
                "Heat dissipation at the Halcyon substation cooling loop stands at 42 kilowatts."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "uncalibrated handheld thermal scan",
                "authority": "individual",
                "quality": "weak",
                "why": "approximate surface thermography conducted without baseline calibration or thermodynamic modeling",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "48 kilowatts",
            "content": (
                "The cooling loop of the Halcyon substation sustains 48 kilowatts in dissipation of heat."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "calibrated in-line calorimetric audit",
                "authority": "instrument",
                "quality": "strong",
                "why": "precision multi-point enthalpy balance calculation measuring mass flow and temperature differentials",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "48 kilowatts",
            "content": (
                "At Halcyon substation, dissipated heat from the cooling loop totals forty-eight kilowatts."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "thermodynamic mass flow calculation",
                "authority": "instrument",
                "quality": "strong",
                "why": "steady-state thermal balance based on flow meters and calibrated heat sensors",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "48 kilowatts",
            "content": (
                "Forty-eight kilowatts leave the Halcyon substation's cooling loop as dissipated heat."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "chilled water loop energy balance log",
                "authority": "instrument",
                "quality": "strong",
                "why": "continuous automated digital logging of heat transfer across the heat exchanger",
            },
        },
    },
}