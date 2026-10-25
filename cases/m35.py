"""M35: the length of the covered walkway between Fennick Hall and the Rowe Building.

Institutional logistics domain, method dimension, tier T1. A's cue is not a hedge but an
approximation, "about 370 metres", and is meant to survive rewording (R16).
"""

CASE = {
    "case_id": "M35",
    "domain": "institutional_logistics",
    "question": ("How long is the covered walkway between Fennick Hall and the Rowe "
                 "Building?"),
    "world_truth": "430 metres",
    "distractors": ["310 metres", "490 metres"],   # plausible, unsupported, same kind
                                                   # as the truth; even steps of 60 m
    "screen_partial": (
        "The covered walkway between Fennick Hall and the Rowe Building is between 340 "
        "and 460 metres long."
    ),   # screen level P1: true, keeps 370 and 430 metres, each 30 metres inside a
         # bound, and rules out 310 and 490 metres
    "quality_dimension": "method",
    "difficulty_tier": "T1",            # A's approximation is part of how it states the
                                        # value, which a faithful rewording keeps (R16);
                                        # confirm in the frozen reports, and relabel T2
                                        # if it is lost
    "design_notes": (
        "A and B state the same proposition, the length of the covered walkway between "
        "Fennick Hall and the Rowe Building, with different values, in one sentence each. "
        "Both name the same walkway between the same two buildings, a fixed structure "
        "rather than a route, so neither can mean a different way between them; both give "
        "the length in metres and refer to no change and to no other source (R1). Read "
        "without provenance, neither is narrower or an exception to the other. The quality "
        "dimension, method, lives in provenance; the one cue in the content is A's "
        "approximation, 'about 370 metres', a kind of T1 cue R16 names beside hedges. It "
        "changes how exactly A states its value, not what A measures, so the two still "
        "have the same scope. B's figure is given to the same ten metres as A's, so only "
        "the word 'about' separates their precision, and the 60-metre gap is far more than "
        "'about' allows, so the two claims still contradict. When this case was written no "
        "other case used an approximation as its cue, while the hedges in use were already "
        "spread over many cases, so this case takes another kind of cue, as R16 asks. "
        "Whether the cue survives is only known once the frozen reports are read; if it is "
        "lost, the case is relabelled T2. B is flat and carries no cue. The two type names "
        "carry the method dimension and nothing else: both are student volunteers', so the "
        "writers have the same standing, and both walked the walkway, so neither is closer "
        "to it; they differ only in how the length was found, by pacing it out or by a "
        "measuring wheel (R19). Neither says 'independent', and both name the source "
        "rather than the subject, so no word a rewording needs is banned (R2a). The "
        "options are 310, 370, 430 and 490 metres, evenly spaced, so the truth and A's "
        "claim are both interior and equally close to the average: neither 'avoid the "
        "extremes' nor 'pick the middle' finds the truth (R8). None is a round figure, and "
        "A's claim is the lower one, so neither a habit for round numbers nor a belief "
        "that wrong figures run high finds the truth. The options carry their unit, as the "
        "content does. The screen sentence keeps 370 and 430, each 30 metres inside a "
        "bound, so 'pick the survivor nearest the bound' does not find the truth (R15). A "
        "and B use the same question words and both leave out 'long' and 'between' (R13). "
        "B, C and D state the fact in three different frames (R17). C and D are separate "
        "findings of the same length, the estates office's site plan and a surveying "
        "class's laser measurement, so neither depends on the volunteers' guide or on each "
        "other, and neither's sentence says how its value was found (R2, R6). All three "
        "give the walkway's length end to end, so B, C and D support one proposition in A7 "
        "(R1). The buildings, the walkway and its length are invented (R4). Filler "
        "describes the walkway itself in set 1, Fennick Hall in set 2 and the Rowe "
        "Building in set 3, with nothing about length, distance, walking time or "
        "measuring, no figures and no second person, written as a plain description rather "
        "than as notes for an accessibility guide, so no slot carries the feel of either "
        "source (R3, R9, R10). No distinctive word is in more than one set, so the slots "
        "stay apart (R12). Each filler set is 78 words and A's and B's sentences are both "
        "14 words, so every long report starts at 92 words and stays inside 88 to 96 after "
        "rewording (R20). When the frozen reports are read (step 3.4), check that A's and "
        "B's rewordings still give the length of the walkway itself: 'the walk from "
        "Fennick Hall' or 'the distance between the buildings' could name a different "
        "route or a straight line. Read D's report the same way: its frame, 'reaches the "
        "Rowe Building after 430 metres', describes the walkway as a trip, and a rewording "
        "such as 'the Rowe Building is 430 metres from Fennick Hall' would drop the "
        "walkway."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # the walkway itself
            "The covered walkway has a green metal roof on wooden beams.",
            "Roses trained up the posts flower on the side that faces the lawn.",
            "Low clipped box shrubs border the other side.",
            "Lamps hang from the beams on black iron chains.",
            "The path underfoot is paved with square grey slabs.",
            "Slatted wooden benches stand in arched alcoves of stone.",
            "The gutters are painted the same green as the roof.",
            "Swallows make nests under the eaves above the path.",
        ],
        [   # Fennick Hall
            "Fennick Hall is a residence with a red brick front and white window frames.",
            "Its lobby has a porter's desk, pigeonholes for letters and a sofa.",
            "A laundry in the basement holds washers, dryers and sinks.",
            "Bicycles are kept in a locked shed at the rear.",
            "A lounge on the ground floor has a television and a pool table.",
            "Ivy grows thickly over the gable beside the car park.",
            "Each floor shares a kitchen and a large fridge.",
        ],
        [   # the Rowe Building
            "The Rowe Building houses lecture theatres, seminar spaces and a computer lab.",
            "Its glass entrance opens onto a bright atrium with a cafe.",
            "A wide staircase rises from the atrium to the upper levels.",
            "Coat hooks line the corridor outside the theatres.",
            "Plants in tall planters soften the concrete walls.",
            "A mosaic of blue tiles decorates the stairwell.",
            "Printers in the computer lab take swipe cards for payment.",
            "Display screens in the atrium show which spaces are free.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "370 metres",
            "provenance": {
                "type": "student volunteer's paced-out estimate",
                "authority": "individual",
                "quality": "weak",
                "why": "a volunteer for the student accessibility guide counted paces "
                       "along the whole walkway, end to end, and turned the count into "
                       "metres",
            },
            "content": ("The covered walkway linking Fennick Hall with the Rowe Building "
                        "stretches about 370 metres."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "430 metres",
            "provenance": {
                "type": "student volunteer's measuring-wheel reading",
                "authority": "individual",
                "quality": "strong",
                "why": "a volunteer for the same guide pushed a measuring wheel along "
                       "the whole walkway, end to end",
            },
            "content": ("Joining Fennick Hall to the Rowe Building, the covered walkway "
                        "runs for 430 metres."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "430 metres",
            "provenance": {
                "type": "estates office site plan",
                "authority": "institutional",
                "quality": "strong",
                "why": "the architect's plan of the walkway, held by the university's "
                       "estates office, gives its length end to end",
            },
            "content": ("Fennick Hall and the Rowe Building are linked by 430 metres of "
                        "covered walkway."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "430 metres",
            "provenance": {
                "type": "surveying class field exercise",
                "authority": "institutional",
                "quality": "strong",
                "why": "a surveying class measured the walkway end to end, section by "
                       "section along its centre line, with a laser distance meter as a "
                       "field exercise",
            },
            "content": ("The covered walkway from Fennick Hall reaches the Rowe Building "
                        "after 430 metres."),
            "n_paraphrases_needed": 1,
        },
    },
}
