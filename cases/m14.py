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
        "so the method differs while authority is held constant (both 'individual'). B's why "
        "describes a direct instrument reading, not a calculation, to match its type name. "
        "C and D each have their own origin, distinct from B's in-loop calorimeter and from each "
        "other: C is the equipment contractor's full-load test and D is the grid operator's "
        "remote monitoring. Their whys name who produced the figure and from where, not a shared "
        "flow-and-temperature balance, so A7 does not read as one method three times. "
        "'Commissioning' was avoided in C's type because it reads as an older measurement (R3). Sources use "
        "distinct frames (R17): A leads with the quantity and 'stands at', B leads with the loop "
        "and describes heat dissipation, C is place-fronted, D is number-fronted. Content lengths "
        "are A=12 and B=14 words, within 2 of each other (R20). Each filler set is exactly 79 "
        "words. Filler describes the physical site only, as three parts of the same "
        "compound (the fenced perimeter, a brick building, the approach road), each with its own "
        "nouns and adjectives, so reports in one trial stay on the site without repeating "
        "features or phrasing across slots (R12). The only shared word is 'compound'. It is "
        "written as plain factual statements, one register throughout, so it does not read as story writing (R10). "
        "It describes the site in a clean, neutral condition, with no damage, wear, age or cordon "
        "wording, so it carries neither a hazard cue nor a staleness cue that would grow with "
        "report length (R3, R9, R10). It avoids "
        "ways of checking or observing, anything about heat, cooling or electrical plant, and any "
        "insider vantage (R9, R10). It contains no word that appears only in a source's "
        "provenance type, no option value and no time marker (R2a, R3, R8)."
    ),
    "filler_sets": [
        [
            "The compound is enclosed by a chain-link fence with a single gate on its southern side.",
            "A strip of gravel sits inside the fence, and shrubs are planted along its outer boundary on every side.",
            "The gate is made of steel bars and opens inward onto a gravel apron.",
            "Wooden posts mark each corner of the fenced area, and a lock secures the gate.",
            "The fence is covered with a grey mesh screen that hides the ground behind it.",
        ],
        [
            "A single-storey brick building stands in the middle of the compound.",
            "The roof is flat and coated with tar, and a short step leads up to the entrance.",
            "The entrance has a pair of green doors with brass handles and a small window above.",
            "Three arched windows face the front path, and each has a white frame and a stone sill.",
            "A metal gutter runs along the front of the roof, and a concrete slab lies outside the entrance.",
        ],
        [
            "One narrow road reaches the compound from the main highway and ends at a turning circle.",
            "The road is surfaced with asphalt, with a yellow line along its centre and a ditch at each edge.",
            "A bus shelter with a timber bench is built beside the road about halfway along.",
            "Rounded boulders lie on the grassy slope above the road, and a dirt track branches off near the bend.",
            "A signpost near the turn points straight toward the compound.",
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
                "why": "direct reading from a calorimeter fitted in the loop and calibrated against a reference standard, so the figure is measured rather than estimated",
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
                "type": "contractor full-load test record",
                "authority": "contractor",
                "quality": "strong",
                "why": "the equipment contractor ran the loop at its full duty on a dedicated test rig of its own and recorded the heat the loop rejected",
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
                "type": "grid operator monitoring feed",
                "authority": "operator",
                "quality": "strong",
                "why": "the grid operator's control centre tracks the substation's heat output through its own remote telemetry, separate from the equipment on site",
            },
        },
    },
}