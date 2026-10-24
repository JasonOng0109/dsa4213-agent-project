"""M29: passengers evacuated from the stalled Corvanne Funicular Railway.

Incident status report, directness dimension, tier T1.
"""

CASE = {
    "case_id": "M29",
    "domain": "incident_status",
    "question": (
        "How many passengers were evacuated from the stalled Corvanne Funicular "
        "Railway?"
    ),
    "world_truth": "42 passengers",
    "distractors": ["30 passengers", "48 passengers"],
    "screen_partial": (
        "The number of passengers evacuated from the stalled Corvanne Funicular "
        "Railway is between 39 and 51."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "directness",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the passengers evacuated from "
        "the stalled Corvanne Funicular Railway, with different values, the same "
        "scope and precision, and no reference to a change or to each other (R1). "
        "T1: A's cue is the hedge 'It is suspected that' (R16), not used by any "
        "other case. "
        "Directness only: A and B are both messages from passengers "
        "('individual'), but A repeats what another rider heard while B was "
        "written by a passenger who was on the stalled car, so the pair differs "
        "in directness, not authority, medium or method (R2, R19). B, C and D "
        "all count everyone brought off the stalled car, so the three agreeing "
        "sources state the same figure in A7. "
        "The options are evenly spaced, with the truth and A's claim as the two "
        "interior values (R8). The screen sentence gives a range whose bounds "
        "sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words passengers, evacuated, "
        "stalled, Corvanne, Funicular and Railway (R13); A, B, C and D use four "
        "different frames (R17). "
        "Filler describes one part of the line per set (the lower station, the "
        "track, the summit), shares no meaningful word across sets, and never "
        "mentions people, faults, rescue, weather or quantities (R9-R12). "
        "Each filler set is 79 words and A and B are 14 and 12 words, so long "
        "reports are 93 and 91 words (R20)."
    ),
    "filler_sets": [
        [
            "The lower station of the Corvanne Funicular Railway faces the square.",
            "It is a building of red sandstone with a glass canopy over the entrance.",
            "Arched doors of dark wood open onto the platform.",
            "A carved stone crest is set above the doors.",
            "Railings painted black enclose the forecourt of the station.",
            "A bronze lamp hangs from a bracket by the entrance.",
            "A bench with armrests stands beside the station doors.",
            "Fluted pillars support the roof of the platform.",
        ],
        [
            "The track climbs straight up the wooded hillside.",
            "It runs on a bed of crushed granite between parallel rails.",
            "Pine trees grow on either side of the line.",
            "Partway up, the track crosses a ravine on a viaduct of iron.",
            "Wooden fences mark the edge of the track through the forest.",
            "Ferns cover the banks of the cutting.",
            "Brick retaining walls hold back the slope where the hill is cut.",
            "A footpath follows the rails a short way off.",
        ],
        [
            "At the summit is a terminus built of pale timber.",
            "A viewing terrace with marble balustrades looks over the valley.",
            "Fixed telescopes face the peaks.",
            "A whitewashed cafe with blue shutters adjoins the terrace.",
            "Gravel paths lead to a chapel on the summit.",
            "A flagpole carries a pennant in green and yellow.",
            "A weathervane shaped like a fish sits on the terminus.",
            "Marble urns are placed beside the gravel paths.",
            "The chapel has slate tiles and a bell tower.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "36 passengers",
            "provenance": {
                "type": "passenger's message relaying another rider's account",
                "authority": "individual",
                "quality": "weak",
                "why": "secondhand: repeats what another rider said they had "
                    "heard",
            },
            "content": ("It is suspected that 36 passengers were evacuated from "
                        "the stalled Corvanne Funicular Railway."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "42 passengers",
            "provenance": {
                "type": "passenger's message sent from on board",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand: written by a passenger who was on the stalled "
                    "car and saw everyone brought off",
            },
            "content": ("The stalled Corvanne Funicular Railway saw 42 passengers "
                        "evacuated off its car."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "42 passengers",
            "provenance": {
                "type": "mountain rescue incident log",
                "authority": "institutional",
                "quality": "strong",
                "why": "lists each passenger brought off the stalled car",
            },
            "content": ("Rescue teams led 42 people to safety when the Corvanne "
                        "Funicular Railway stalled."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "42 passengers",
            "provenance": {
                "type": "operator's boarding tally",
                "authority": "institutional",
                "quality": "strong",
                "why": "counts everyone who boarded the stalled trip, all of "
                    "whom were brought off",
            },
            "content": ("Every one of the 42 people aboard the Corvanne "
                        "Funicular Railway was evacuated."),
            "n_paraphrases_needed": 1,
        },
    },
}