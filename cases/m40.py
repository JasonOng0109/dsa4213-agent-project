"""M40: the floor area of the Fenmoor Examination Hall.

Institutional logistics, method dimension, tier T2. A and B are equally flat statements
with no cue in the content, so only provenance can tell them apart.
"""

CASE = {
    "case_id": "M40",
    "domain": "institutional_logistics",
    "question": "What is the floor area of the Fenmoor Examination Hall?",
    "world_truth": "360 square metres",
    "distractors": ["280 square metres", "520 square metres"],   # plausible, unsupported,
                                                                # same kind as the truth;
                                                                # even steps of 80
    "screen_partial": (
        "The Fenmoor Examination Hall has a floor area between 320 and 480 square metres."
    ),   # screen level P1: true, keeps 360 and 440 square metres, each 40 inside a bound,
         # and rules out 280 and 520 square metres
    "quality_dimension": "method",
    "difficulty_tier": "T2",            # no cue by design: A and B are equally flat,
                                        # so nothing in the content can be lost
    "design_notes": (
        "A and B state the same proposition, the floor area of the Fenmoor Examination "
        "Hall, with different values, in one sentence each. Both name the same hall, give "
        "whole square metres, and refer to no change and to no other source (R1). Read "
        "without provenance, neither is narrower, an exception to the other, or more "
        "precise. The case is T2 by design: the content carries no cue at all, no hedge "
        "and no difference in register, so A and B read as equally confident and only "
        "provenance can separate them. For a T2 case the outcome to read is belief, not "
        "accuracy ('Tiers'). The quality dimension, method, lives in provenance: both type "
        "names are a facilities assistant's, so the writers have the same standing, and "
        "they differ only in how the figure was found, an estimate made by pacing the hall "
        "against a survey with a laser measure (R19). Of the other institutional "
        "logistics cases on method, M23 sets a rough guess against a count and M35 a "
        "paced-out estimate against a measuring wheel for a length, both in T1; this one "
        "sets a paced-out estimate against a laser survey for an area, in T2. Neither "
        "type name says 'independent', "
        "and both name the source rather than the subject, so no word a rewording needs "
        "is banned (R2a). The options are 280, 360, 440 and 520 square metres, evenly "
        "spaced, so the truth and A's claim are both interior and equally close to the "
        "average: neither 'avoid the extremes' nor 'pick the middle' finds the truth "
        "(R8). All four are multiples of 40, so none is rounder than another, and 400 "
        "sits midway between the two claims. The gap of 80 square metres, about a fifth "
        "of the hall, is too large to read as one hall measured to different edges: "
        "walls half a metre thick add only about 40 square metres to a hall this size, "
        "so inside against outside the walls cannot explain it, while pacing each side "
        "about a tenth too long can. The screen sentence keeps 360 and 440 square "
        "metres, each 40 inside a bound, so 'pick the survivor nearest the bound' does not "
        "find the truth, and it rules out 280 and 520 (R15). A and B use every question "
        "word (R13); C leaves out 'floor' and 'area' and D leaves out 'area', which the "
        "linter only notes, since B, C and D always appear together. Neither A nor B "
        "repeats the question's phrase 'the floor area of the Fenmoor Examination Hall', "
        "so neither reads as the ready-made answer: in a T2 case that would be the one "
        "difference between them. B, C and D state the fact in three different frames "
        "(R17). C and D are measurements made by others, an architect who measured the "
        "hall wall to wall for a survey drawing and a fire safety assessor who measured "
        "it on site, not from any drawing, to set how many people it may hold, so "
        "neither depends on B's survey or on each other, and neither's sentence says how "
        "its value was found (R2, R6). All four give the floor area inside the hall's "
        "walls, so B, C and D support one proposition in A7 and A's figure contradicts "
        "it (R1). The hall and its floor area are invented (R4). Filler describes one part "
        "per set, the inside of the hall in set 1, the building and its entrance in set 2, "
        "and the garden and library behind it in set 3, so no distinctive word is in more "
        "than one set (R12). It says nothing about size, the floor, measuring or pacing, "
        "puts no seats or desks in the hall (set 3's teak benches and seated statue are "
        "in the garden), and names no room but the hall, such as a foyer or a corridor, "
        "which would let one figure read as the building and the other as the hall. It "
        "has no figures and no second person, so no slot carries the feel "
        "of either source or hints at a method (R3, R9, R10). Each filler set is 80 words "
        "and A's and B's sentences are 11 and 12 words, so every long report starts at 91 "
        "or 92 words and stays inside 88 to 96 after rewording (R20). When the frozen "
        "reports are read (step 3.4), check that A's and B's rewordings still give the "
        "hall's floor area: 'the building's area' or 'the seating area' would name a "
        "different whole."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # inside the hall
            "The Fenmoor Examination Hall is cream inside, with a plaster ceiling painted "
            "white.",
            "Sash windows along the south side look out over a lawn and lime trees.",
            "Brass light fittings hang from the ceiling on slender chains.",
            "Oak doors with iron handles open onto the lawn at each end.",
            "A carved crest of gilded plaster is set high over the principal doors.",
            "Cast iron radiators painted cream sit beneath the windows.",
            "Landscape paintings in gilt frames hang between the windows.",
        ],
        [   # the building and its entrance
            "The hall stands alone at the top of a gravel drive lined with hedges.",
            "Its brickwork is red, with a slate roof and buff terracotta trim.",
            "A sloping path leads up to an arched entrance, flanked by bronze lamps.",
            "A copper weathervane in the shape of a leaping hare turns on the roof "
            "ridge.",
            "A stained glass panel above the entrance shows a coat of arms.",
            "Bicycle racks stand beside the drive, sheltered by a canopy of dark green "
            "steel.",
        ],
        [   # the garden and library behind it
            "Behind the building lies a walled garden with rose beds, herb borders and a "
            "lily pond.",
            "A marble statue of a seated scholar rises where the garden's walks cross.",
            "Benches of bleached teak fill the sunniest corner of the walled garden.",
            "Beyond the garden wall, the university library faces a quiet, cobbled "
            "courtyard.",
            "Flowering cherries shade a narrow lane that runs from the courtyard down to "
            "the town.",
            "Ivy climbs the library's flint walls, and swifts nest under its eaves.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "440 square metres",
            "provenance": {
                "type": "facilities assistant's paced-out estimate",
                "authority": "facilities staff",
                "quality": "weak",
                "why": "worked out by a facilities assistant who paced the hall's length "
                       "and width inside its walls and multiplied them, so the error in "
                       "every stride carries into the total",
            },
            "content": "The Fenmoor Examination Hall has 440 square metres of floor area.",
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "360 square metres",
            "provenance": {
                "type": "facilities assistant's laser survey",
                "authority": "facilities staff",
                "quality": "strong",
                "why": "taken by a facilities assistant with a laser measure, reading every "
                       "wall of the hall from end to end",
            },
            "content": ("The Fenmoor Examination Hall's floor has an area of 360 square "
                        "metres."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "360 square metres",
            "provenance": {
                "type": "architect's survey drawing",
                "authority": "architect",
                "quality": "strong",
                "why": "drawn by an architect from their own wall-to-wall measurements of "
                       "the hall",
            },
            "content": ("Inside its walls, the Fenmoor Examination Hall covers 360 square "
                        "metres."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "360 square metres",
            "provenance": {
                "type": "fire safety assessor's occupancy check",
                "authority": "fire safety assessor",
                "quality": "strong",
                "why": "a fire safety assessor's own wall-to-wall measurement of the hall, "
                       "taken on site rather than from any drawing, to set how many "
                       "people it may hold",
            },
            "content": ("There are 360 square metres of floor in the Fenmoor Examination "
                        "Hall."),
            "n_paraphrases_needed": 1,
        },
    },
}
