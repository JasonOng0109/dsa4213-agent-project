"""M21: Evacuation radius for the Branford depot gas leak.

Incident status domain, authority quality dimension, tier T1.
"""

CASE = {
    "case_id": "M21",
    "domain": "incident_status",
    "question": "What is the evacuation radius for the Branford depot gas leak?",
    "world_truth": "800 metres",
    "distractors": ["400 metres", "1200 metres"],  # [400, 600, 800, 1200] 
    "screen_partial": (
        "The evacuation radius for the Branford depot gas leak is between 500 metres and 900 metres."
    ),  # keeps 600 and 800 (truth); rules out 400 and 1200; both survivors sit 100 metres inside bounds (R15)
    "quality_dimension": "authority",
    "difficulty_tier": "T1",
    "design_notes": (
        "Authority dimension, T1. A and B state the same proposition (the evacuation radius "
        "for the Branford depot gas leak) as single sentences with identical scope (R1). Both contain "
        "the exact same six question content-words: evacuation, radius, Branford, depot, gas, and leak (R13). "
        "The T1 cue is A's clause-level hedge 'is assumed to be' (R16), which survives faithful reporter "
        "paraphrasing while varying from hedges used in previous cases. "
        "Quality resides purely in provenance (R2, R19): both writers attend on-site perimeter response briefings, "
        "holding directness, setting, and methodology constant while isolating authority: A is an entry-level "
        "volunteer trainee ('depot safety trainee briefing notes'), whereas B is the governing on-scene authority "
        "('incident commander perimeter directive log') (R19). Neither type name leaks authority clues or methodology "
        "into content, and 'independent' is strictly omitted (R19). Sources B, C, and D state the truth using distinct "
        "syntactic frames to keep pairwise bigram overlap strictly below 0.40, fully satisfying A7 (R17). Options form "
        "a balanced spread [400, 600, 800, 1200] metres, with the truth (800) and A's claim (600) occupying interior "
        "positions (R8). The screen sentence uses two bounds (500 and 900 metres), placing both survivors equidistant "
        "at exactly 100 metres inside the bounds (R15). Content lengths are A=15 and B=15 words (|A - B| = 0 <= 2). "
        "Each filler set is exactly 77 words, landing every long report at exactly 92 words (77 + 15), within the tight "
        "91-93 band (R20). Fillers describe neutral physical depot infrastructure across three distinct zones (approach avenue, "
        "maintenance storage shelter, administrative annex) with zero non-stopword content overlap across sets (R12), "
        "containing no numbers, time markers, or gas incident vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "The concrete approach avenue features yellow painted central lane dividers running toward the primary barrier gate.",
            "Dark bronze perimeter stanchions support sturdy linked alloy chains alongside the paved lorry bypass apron.",
            "A raised security checkpoint booth houses tinted shatterproof viewing windows beneath an overhanging aluminium canopy.",
            "Automated license plate recognition cameras mount atop slender galvanised poles beside the main access turning circle.",
            "Precast stone kerbstones border neatly manicured grass verges leading outward facing the outer transit thoroughfare.",
        ],
        [
            "The maintenance storage shelter incorporates corrugated zinc exterior cladding secured over a rigid structural boxwork frame.",
            "Open service parking bays contain durable rubber wheel stops anchored securely into the tarmac floor.",
            "Overhead high-pressure sodium luminaires produce continuous warm amber illumination across the lower industrial service yard.",
            "A freestanding metal shelving rack holds spare silicone hoses, brass pipe fittings, and empty utility toolboxes.",
            "Perforated drainage trenches lined with slotted metallic grates channel surface rainwater runoff into underground sumps.",
        ],
        [
            "The single-storey administrative annex displays exposed light red brickwork accented by broad double-glazed casement window apertures.",
            "Dense hawthorn hedgerows grow along the southern property margin, providing an effective visual screening hedge.",
            "A timber pedestrian boardwalk meanders through planted wildflower beds between the annex and visitor footpaths.",
            "External terracotta masonry sconces project gentle downward lighting along the recessed administrative office entry foyer doorway.",
            "Crushed river gravel pathways crunch softly underfoot while guiding personnel into designated scenic breakout courtyards.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "600 metres",
            "content": (
                "The evacuation radius for the Branford depot gas leak is assumed to be 600 metres."
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
            "claim": "800 metres",
            "content": (
                "Emergency evacuation limits for the Branford depot gas leak establish a radius of 800 metres."
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
            "claim": "800 metres",
            # 14 words: Active agent syntax keeping bigram overlap strictly below 0.40 (R17, A7)
            "content": (
                "Safety officials maintain eight hundred metres as the mandatory protective zone around Branford depot."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "civil protection dispatch register",
                "authority": "dispatch coordinator",
                "quality": "strong",
                "why": "regional civil protection log coordinating emergency perimeter cordons",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "800 metres",
            # 13 words: Quantity-fronted frame ensuring distinct syntax (R17, A7)
            "content": (
                "Eight hundred metres defines the perimeter boundary cordoned off by Branford depot responders."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "municipal emergency response order",
                "authority": "emergency director",
                "quality": "strong",
                "why": "municipal emergency decree establishing statutory exclusion perimeters for civic safety",
            },
        },
    },
}