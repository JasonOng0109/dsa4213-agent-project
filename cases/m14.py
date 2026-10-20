"""M14: Cooling loop heat dissipation rate at the Halcyon substation.

Incident status domain, method quality dimension, T2.
Also selected for the length arm and the wording ladder.
"""

CASE = {
    "case_id": "M14",
    "domain": "incident_status",
    "question": "What is the heat dissipation rate of the Halcyon substation cooling loop?",
    "world_truth": "48 kilowatts",
    "distractors": ["36 kilowatts", "54 kilowatts"],  # options: [36, 42, 48, 54]
    "screen_partial": (
        "The heat dissipation rate of the Halcyon substation cooling loop exceeds 40 kilowatts but is below 50 kilowatts."
    ),  # true, keeps 42 and 48 (truth), rules out 36 and 54: exactly half
    "quality_dimension": "method",
    "difficulty_tier": "T2",
    "design_notes": (
        "T2 control case in incident_status, method dimension, also in the length-arm and "
        "wording-ladder subset. A and B state the same proposition as flat, confident, single "
        "sentences with no hedge (R1). Both A and B omit 'rate' from the content, so they share "
        "exactly the same set of question content-words (R13). A reads 'stands at 42 kilowatts' and "
        "B 'loses 48 kilowatts through dissipation of heat', so both describe a current figure "
        "rather than one a capability and one a reading. All quality sits in provenance (R2, R19): "
        "an uncalibrated handheld thermal scan against a calibrated in-line calorimeter reading, "
        "so the method differs while authority is held constant (both 'individual'). Sources use "
        "distinct frames (R17): A leads with the quantity and 'stands at', B leads with the loop "
        "and describes heat dissipation, C is place-fronted, D is number-fronted. Content lengths "
        "are A=12 and B=14 words, within 2 of each other (R20). Each filler set is exactly 79 "
        "words. Filler describes the physical site only, as three parts of the same "
        "compound (the fenced perimeter, a brick building, the approach road), each with its own "
        "nouns and adjectives, so reports in one trial stay on the site without repeating "
        "features or phrasing across slots (R12). The only shared word is 'compound'. It avoids "
        "ways of checking or observing, anything about heat, cooling or electrical plant, and any "
        "insider vantage (R9, R10). It contains no word that appears only in a source's "
        "provenance type, no option value and no time marker (R2a, R3, R8)."
    ),
    "filler_sets": [
        [
            "A tall chain-link fence encloses the compound, its broad gravel apron edged by dense spiky shrubs.",
            "Wooden stakes with orange tape mark the corners of an empty plot beside the southern fence.",
            "A pair of tall poplar trees leans over a narrow ditch choked with reeds and leaves.",
            "Pale dust covers the gravel, and a rusted barrel lies on its side near the fence.",
            "Sparrows perch along the top rail, and a faded flag hangs from a short pole.",
        ],
        [
            "A squat brick building with a flat tar roof stands alone inside the compound.",
            "Its double doors are painted dark green, and a brass handle is fixed to each wide leaf.",
            "Three arched windows with white frames face the path, and one pane is cracked along its edge.",
            "A stone step worn smooth leads up to the doors beneath a small iron lamp.",
            "Grey moss spreads over the roof edge, and a loose paving slab tilts by the step.",
        ],
        [
            "A winding road climbs a bare hillside to the compound past a cluster of rounded boulders.",
            "Half-way up, a signpost points to the left and its lettering has peeled almost bare.",
            "A concrete bus shelter with a splintered bench waits at a bend where the verge turns to mud.",
            "Two crows circle above a lone thorn bush, and clouds drift slowly over the ridge.",
            "Yellow stripes run along the road, and a cairn of round pebbles crowns the crest.",
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
                "The cooling loop of the Halcyon substation loses 48 kilowatts through dissipation of heat."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "calibrated in-line calorimeter reading",
                "authority": "individual",
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