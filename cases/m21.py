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
        "Quality resides purely in provenance (R2, R19): both sources are response logs kept on site, so "
        "the kind of document, closeness and method are the same and only standing differs: A is an "
        "entry-level volunteer trainee's log ('depot volunteer safety trainee response log'), B the incident "
        "commander's ('depot incident commander response log') (R19). Neither type name leaks authority clues or methodology "
        "into content, and 'independent' is strictly omitted (R19). Sources B, C, and D state the truth using distinct "
        "syntactic frames to keep pairwise bigram overlap strictly below 0.40 (R17). B, C and D each reach "
        "the figure by their own route (A7): B is the commander directing the perimeter, C the police "
        "cordon officer's own record of where the cordon stood, measured from the depot, and D the gas "
        "utility engineers' own map of the streets they cleared. B's sentence gives the radius around the "
        "leak itself, the same measure as A's (R1). Options form "
        "an evenly spaced spread [460, 620, 780, 940] metres, with the truth (780) and A's claim (620) occupying interior "
        "positions (R8). The screen sentence uses two bounds (540 and 860 metres), placing both survivors equidistant "
        "at exactly 80 metres inside the bounds (R15). Content lengths are A=15 and B=14 words (|A - B| <= 2). "
        "Each filler set is 77 words, so long reports start at 91 or 92 words (R20). Filler describes the "
        "gatehouse and approach road, the office building and the trees along the boundary, in plain "
        "one-fact sentences with no content word in two sets (R12). It has nothing about gas, pipes, "
        "people, gathering places, clocks or numbers, and no site-plan wording (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "The Brackenford depot is reached along a straight approach road.",
            "A small gatehouse with a flat roof stands beside the entrance.",
            "The gatehouse is painted cream, with a green door.",
            "A barrier arm in red and white stripes spans the road.",
            "Low kerbs edge the road, and cat's eyes mark its centre.",
            "A company sign with blue lettering is mounted on steel posts.",
            "Concrete bollards flank the barrier.",
            "Grass verges run on each side of the approach.",
        ],
        [
            "The depot office is a long building of yellow brick.",
            "Its windows have black frames and slate sills.",
            "A glass canopy juts out over the porch.",
            "Climbing roses are trained up a trellis by the porch.",
            "The office name appears in brass capitals above the canopy.",
            "A magnolia grows against the end wall.",
            "Hanging baskets of fuchsias hang from the eaves.",
            "A paved apron lines the front of the office.",
            "Its chimneys are capped with clay pots.",
        ],
        [
            "Silver birches follow the far boundary of the depot.",
            "Beneath them, the ground is sown with wild flowers.",
            "Poppies and cornflowers mix with ox-eye daisies.",
            "A hawthorn hedge borders the back lane.",
            "Blackbirds nest in the hedge.",
            "Horse chestnuts shade the corner by the lane.",
            "Ferns spread thickly at the foot of the hedge.",
            "A wooden fence divides the meadow from the lane.",
            "Rabbits graze on the short turf.",
            "Wrens flit among the brambles below the birches.",
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
                "The Brackenford depot gas leak has an evacuation radius of 780 metres around it."
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