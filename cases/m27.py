"""M27: the key deposit for the practice rooms at Halvercombe College.

Institutional logistics, authority dimension, tier T1.
"""

CASE = {
    "case_id": "M27",
    "domain": "institutional_logistics",
    "question": "What is the key deposit for the practice rooms at Halvercombe College?",
    "world_truth": "40 dollars",
    "distractors": ["20 dollars", "50 dollars"],
    "screen_partial": (
        "The key deposit for the practice rooms at Halvercombe College is between 35 "
        "and 55 dollars."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "authority",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the key deposit for the "
        "practice rooms at Halvercombe College, with different values, the same "
        "scope and precision, and no reference to a change or to each other "
        "(R1). "
        "T1: A's cue is the hedge 'is probably' (R16), not used by any other "
        "case. "
        "Authority only: A and B are the same kind of document, a notice, but A "
        "is posted by a student society ('individual') with no say over the "
        "charge and B by the college office that sets it ('institutional'), so "
        "the pair differs in who issued it, not in document type, directness or "
        "method (R2, R19). B, C and D all give the deposit held for each practice "
        "room key, so the three agreeing sources state the same figure in A7. "
        "The options are evenly spaced, with the truth and A's claim as the two "
        "interior values (R8). The screen sentence gives a range whose bounds "
        "sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words key, deposit, practice, "
        "rooms, Halvercombe and College (R13); A, B, C and D use four different "
        "frames (R17). "
        "Filler describes one part of the college per set (the front court, the "
        "tower, the river meadow), shares no meaningful word across sets, and "
        "never mentions music, rooms, keys, money or people (R9-R12). "
        "Each filler set is 77 words and A and B are 14 words each, so long "
        "reports are 91 words (R20)."
    ),
    "filler_sets": [
        [
            "Halvercombe College is entered through a gatehouse on the main road.",
            "Beyond the gatehouse is a square court paved with stone.",
            "A stone basin stands in the centre of the court.",
            "Gates close off the opposite side of the court.",
            "Windows look onto the court from the buildings around it.",
            "A coat of arms is fixed above the inner doorway.",
            "Lanterns hang on metal brackets beside the doorway.",
            "A bench is placed next to the inner doorway.",
        ],
        [
            "A tower rises from the north of the grounds.",
            "The walls of the tower are made of grey flint.",
            "A dome covers the top of the tower.",
            "Slits are cut into the tower in a spiral.",
            "A weathervane shaped like a heron is mounted on the dome.",
            "A lightning rod runs from the dome to the ground.",
            "A ledge circles the tower just below the dome.",
            "The base of the tower leads into a cloister with arches.",
        ],
        [
            "A meadow to the south slopes down to the river.",
            "A gravel path follows the bank under willow trees.",
            "A boathouse with a tiled roof sits at the water's edge.",
            "Wildflowers grow in the meadow grass near the path.",
            "A brick bridge crosses the river to the far bank.",
            "Reed beds line the shallows by the near shore.",
            "A jetty reaches out from the boathouse into the river.",
            "Hawthorn hedges mark the far boundary of the meadow.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "30 dollars",
            "provenance": {
                "type": "student-run music society notice",
                "authority": "individual",
                "quality": "weak",
                "why": "unofficial notice from a student society with no say "
                    "over the charge",
            },
            "content": ("The key deposit for the practice rooms at Halvercombe "
                        "College is probably 30 dollars."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "40 dollars",
            "provenance": {
                "type": "college bursary office notice",
                "authority": "institutional",
                "quality": "strong",
                "why": "official notice from the office that sets the deposit "
                    "for each practice room key",
            },
            "content": ("Students at Halvercombe College pay 40 dollars as a key "
                        "deposit on practice rooms."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "40 dollars",
            "provenance": {
                "type": "college finance policy",
                "authority": "institutional",
                "quality": "strong",
                "why": "the policy that fixes the deposit held for each practice "
                    "room key",
            },
            "content": ("Halvercombe College holds 40 dollars against each practice "
                        "room key it lends out."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "40 dollars",
            "provenance": {
                "type": "porters' lodge sign-out sheet",
                "authority": "institutional",
                "quality": "strong",
                "why": "records the deposit taken each time a practice room key "
                    "is signed out",
            },
            "content": ("Borrowing a key for a Halvercombe College practice room "
                        "requires a deposit of 40 dollars."),
            "n_paraphrases_needed": 1,
        },
    },
}