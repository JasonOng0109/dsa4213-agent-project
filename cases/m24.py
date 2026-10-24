"""M24: the number of credits needed for the Coastal Ecology minor at Marrowdene College.

Institutional logistics, primary source dimension, tier T2.
"""

CASE = {
    "case_id": "M24",
    "domain": "institutional_logistics",
    "question": (
        "How many credits are needed for the Coastal Ecology minor at Marrowdene "
        "College?"
    ),
    "world_truth": "27 credits",
    "distractors": ["19 credits", "31 credits"],
    "screen_partial": (
        "The number of credits needed for the Coastal Ecology minor at Marrowdene "
        "College is between 25 and 33."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "primary_source",
    "difficulty_tier": "T2",

    "design_notes": (
        "A and B state the same proposition about the credits for the whole "
        "Coastal Ecology minor at Marrowdene College, with different values, the "
        "same scope and precision, and no reference to a change or to each "
        "other (R1). "
        "T2: neither sentence carries a hedge or other textual cue, so the pair "
        "is near-symmetric and the outcome to read is belief, not accuracy. "
        "Primary source only: A and B both come from the faculty "
        "('institutional'), but A is a newsletter summary restating the "
        "requirement while B is the degree regulations that set it, so the pair "
        "differs in primary versus secondary source, not authority or method "
        "(R2, R19). C and D reach the total by their own routes: C adds up the "
        "credits of the minor's set modules from each module's own catalogue "
        "entry, and D is a committee member's own notes kept apart from the "
        "minutes the regulations were drafted from, so a slip in one record "
        "would not reach the other two in A7. The total is set by a decision, "
        "so that decision is the true value; what A7 needs is that no source "
        "copies another, not that they share no origin. "
        "The options are evenly spaced, with the truth and A's claim as the two "
        "interior values (R8). The screen sentence gives a range whose bounds "
        "sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words credits, Coastal, Ecology, "
        "minor, Marrowdene and College, and both leave out 'needed' (R13); A, B, C "
        "and D use four different frames (R17). "
        "Filler describes one part of the campus per set (the entrance, the main "
        "hall, the library garden), shares no meaningful word across sets, and "
        "never mentions courses, credits, study or people (R9-R12). "
        "Each filler set is 79 words and A and B are 14 and 13 words, so long "
        "reports are 93 and 92 words (R20)."
    ),
    "filler_sets": [
        [
            "Marrowdene College is entered through an iron gate set between "
            "stone pillars.",
            "A gravel drive leads from the gate to the front of the college.",
            "A lawn lies to the left of the drive, edged by a privet hedge.",
            "A bronze statue of a kneeling figure is placed in the middle of the "
            "lawn.",
            "Lamps on metal posts are set along both edges of the drive.",
            "A flag in the college colours hangs from a pole beside the gate.",
        ],
        [
            "The main hall is a sandstone building with sash windows.",
            "A sandstone porch covers the main doors of the hall.",
            "The doors are made of oak and painted a dark blue.",
            "Ivy clings to the north gable.",
            "A carved crest is fixed into the gable above the porch.",
            "Window troughs on the ground floor hold trailing ferns.",
            "A copper weathervane is mounted on the ridge of the slate roof.",
            "Timber benches sit along the walk just outside the hall.",
        ],
        [
            "Behind the library is a walled garden laid out in square beds.",
            "Brick paths divide the beds and meet at a marble fountain.",
            "Climbing roses grow over a wooden pergola on the eastern boundary "
            "of the garden.",
            "A birdbath on a plinth stands in the centre of the walled garden.",
            "Low box borders surround each of the planted beds.",
            "A teak seat faces the fountain under a cherry tree.",
            "Lavender is planted in the beds nearest the garden arch.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "23 credits",
            "provenance": {
                "type": "faculty newsletter summary",
                "authority": "institutional",
                "quality": "weak",
                "why": "secondary: a newsletter item restating the credit "
                    "requirement from the faculty's regulations",
            },
            "content": ("At Marrowdene College, the Coastal Ecology minor comes "
                        "to a total of 23 credits."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "27 credits",
            "provenance": {
                "type": "faculty degree regulations",
                "authority": "institutional",
                "quality": "strong",
                "why": "primary: the regulations that define the minor and "
                    "set its total credit requirement",
            },
            "content": ("A minor in Coastal Ecology at Marrowdene College is "
                        "27 credits in all."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "27 credits",
            "provenance": {
                "type": "module catalogue",
                "authority": "institutional",
                "quality": "strong",
                "why": "the catalogue's page for the minor adds up the credits of "
                    "its set modules, each taken from that module's own entry, not "
                    "from the regulations' figure for the minor",
            },
            "content": ("To graduate with the Coastal Ecology minor, a Marrowdene "
                        "College student must complete 27 credits."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "27 credits",
            "provenance": {
                "type": "committee member's own meeting notes",
                "authority": "individual",
                "quality": "strong",
                "why": "notes a member of the committee that designed the minor "
                    "took as its credit total was agreed, kept apart from the "
                    "minutes the regulations were drafted from",
            },
            "content": ("The Coastal Ecology minor at Marrowdene College adds up "
                        "to 27 credits."),
            "n_paraphrases_needed": 1,
        },
    },
}