"""M21: Evacuation radius for the Brackenford depot gas leak.

Incident status domain, authority quality dimension, tier T1.
"""

CASE = {
    "case_id": "M21",
    "domain": "incident_status",
    "question": "What is the evacuation radius for the Brackenford depot gas leak?",
    "world_truth": "780 metres",
    "distractors": ["460 metres", "940 metres"],  # [460, 620, 780, 940]
    "screen_partial": (
        "The evacuation radius for the Brackenford depot gas leak is between 540 metres and 860 metres."
    ),  # keeps 620 and 780 (truth); rules out 460 and 940; both survivors sit 80 metres inside bounds (R15)
    "quality_dimension": "authority",
    "difficulty_tier": "T1",
    "design_notes": (
        "Authority dimension, T1. A and B state the same proposition (the evacuation radius "
        "for the Brackenford depot gas leak) as single sentences with identical scope (R1). Both contain "
        "the same six question content-words: evacuation, radius, Brackenford, depot, gas, and leak (R13). "
        "The T1 cue is A's clause-level hedge 'is assumed to be' (R16), also used in M34 & M38 (all 3 slots full). "
        "Quality resides purely in provenance (R2, R19): both writers attend on-site perimeter response briefings, "
        "holding directness, setting, and methodology constant while isolating authority: A is an entry-level "
        "volunteer trainee ('depot safety trainee briefing notes'), whereas B is the governing on-scene authority "
        "('incident commander perimeter directive log') (R19). Neither type name leaks authority clues or methodology "
        "into content, and 'independent' is strictly omitted (R19). Sources B, C, and D state the truth using distinct "
        "syntactic frames to keep pairwise bigram overlap strictly below 0.40, fully satisfying A7 (R17). Options form "
        "an evenly spaced spread [460, 620, 780, 940] metres, with the truth (780) and A's claim (620) occupying interior "
        "positions (R8). The screen sentence uses two bounds (540 and 860 metres), placing both survivors equidistant "
        "at exactly 80 metres inside the bounds (R15). Content lengths are A=15 and B=14 words (|A - B| <= 2). "
        "Each filler set is 77 words, landing every long report within the tight "
        "91-93 band after accepted rewording (R20). Fillers describe neutral physical depot infrastructure across three "
        "distinct zones with distinct vocabulary and no repeated non-stopword content words across sets (R12), containing "
        "no numbers, time or presence markers, process or register wording, or gas incident vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "A paved avenue crosses a broad forecourt beside pale concrete kerbs and a low masonry wall.",
            "Flat ochre slabs form a walkway beside a square planter filled with clipped shrubs and gravel.",
            "A circular canopy covers a loading platform beside a tall brick facade with narrow arches.",
            "Smooth basalt paving surrounds a shallow ornamental pool beside plain stone posts.",
            "The entrance facade has a blue metal canopy, steps, and a round clock set above the entrance doors.",
        ],
        [
            "A long shed has pale timber boards, a shallow roof, and wide canvas panels along one side.",
            "Grey paving surrounds a low round planter filled with lavender, thyme, and small white stones.",
            "A wooden bench stands beside a square noticeboard with a plain green frame and blank centre.",
            "Tall cypress shrubs line a gravel path beside a low wall topped with terracotta tiles.",
            "The shelter facade has cream plaster, dark blue shutters, and a broad rectangular doorway.",
        ],
        [
            "A low office wing has white rendered walls, a slate roof, and tall arched windows with alder foliage.",
            "Pale gravel borders a rectangular lawn with a stone sundial near the centre.",
            "A covered walkway links the wing to a round courtyard enclosed by brick posts.",
            "The side wall has green shutters, a copper drainpipe, and a narrow wooden door with trim.",
            "Several ornamental pear trees stand beside a tiled terrace and a shallow brick parapet near offices.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "620 metres",
            "content": (
                "For the Brackenford depot gas leak, the evacuation radius is assumed to be 620 metres."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "depot volunteer safety trainee response log",
                "authority": "safety trainee",
                "quality": "weak",
                "why": "on-site response log kept by an entry-level volunteer safety trainee attending the response staging",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "780 metres",
            "content": (
                "At the Brackenford depot, a 780-metre evacuation radius applies around the gas leak perimeter."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "depot incident commander response log",
                "authority": "incident commander",
                "quality": "strong",
                "why": "on-site response log kept by the commanding depot emergency official directing the perimeter",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "780 metres",
            "content": (
                "Residents within 780 metres of the Brackenford depot gas leak were evacuated."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "police cordon officer's own log",
                "authority": "police cordon officer",
                "quality": "strong",
                "why": "the officer's own record of where the cordon was set up, measured from the depot",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "780 metres",
            "content": (
                "The Brackenford depot gas leak led to an evacuation 780 metres in every direction."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "gas utility's evacuation map",
                "authority": "gas utility engineers",
                "quality": "strong",
                "why": "the utility's engineers marked every street they cleared on their own map",
            },
        },
    },
}