"""M23: the number of lockers in the basement of Brackwell Hall.

Institutional logistics, method dimension, tier T1.
"""

CASE = {
    "case_id": "M23",
    "domain": "institutional_logistics",
    "question": "How many lockers are in the basement of Brackwell Hall?",
    "world_truth": "260",
    "distractors": ["180", "300"],  # plausible, unsupported, same kind
    "screen_partial": (
        "The number of lockers in the basement of Brackwell Hall is more than 240."
    ),  # screen level P1:
        # true, keeps the truth, rules out 180 and 220 of the four options.
    "quality_dimension": "method",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the lockers in the whole "
        "basement of Brackwell Hall, with different values, the same scope and "
        "precision, and no reference to a change or to each other (R1). "
        "T1: A's cue is the hedge 'is believed to' (R16). "
        "Method only: A and B are both student volunteers ('individual') who "
        "walked through the basement, but A judged by eye while B counted item "
        "by item, so the pair differs in method, not authority or directness "
        "(R2, R19). "
        "The options are evenly spaced, with the truth and A's claim as the two "
        "interior values (R8). "
        "A and B share exactly the question words lockers, basement, Brackwell "
        "and Hall (R13), and A, B, C and D use four different frames (R17). "
        "Filler never mentions lockers, quantities or ways of counting (R9-R12). "
        "Each filler set is 82 words and A and B are 11 and 9 words, so long "
        "reports are 93 and 91 words (R20)."
    ),
    "filler_sets": [
        [
            "Brackwell Hall is a red brick building with a slate roof and tall "
            "arched windows.",
            "A wide flight of stone steps leads up to the main entrance on the "
            "north face.",
            "Glass doors at the front entrance slide open as people walk towards them.",
            "A ramp beside the steps gives step-free access to the building.",
            "Bicycle racks are bolted to the paving beside the path to the west.",
            "A steel flagpole rises from a square patch of grass near the front "
            "corner.",
        ],
        [
            "The basement walls are painted pale green, with grey vinyl laid "
            "underfoot throughout.",
            "Plain white plastic covers sit snugly over the overhead lights.",
            "Cool air flows in through metal vents fitted near the ceiling.",
            "A water fountain stands at the far end of the long corridor.",
            "A seating area with padded benches sits halfway along the corridor.",
            "A fire extinguisher is mounted on a bracket beside a small "
            "noticeboard.",
            "Coat hooks are screwed into a wooden rail along one stretch of wall.",
        ],
        [
            "The upper floors hold lecture rooms, offices and a cafe.",
            "A balcony on the top floor looks out over the central lawn.",
            "A printing room on the first floor has copiers lined up beneath a "
            "deep shelf.",
            "Each floor has a set of washrooms near its centre.",
            "Framed photographs of the campus hang in the space outside the "
            "offices.",
            "Potted plants are placed around the cafe, where soft music plays.",
            "The lecture rooms have tiered seats, fixed desks and pull-down "
            "projector screens.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "220",
            "provenance": {
                "type": "student volunteer's rough guess",
                "authority": "individual",
                "quality": "weak",
                "why": "rough guess: the volunteer walked through the basement "
                    "but named a figure by eye without counting",
            },
            "content": ("The basement of Brackwell Hall is likely "
                        "to contain 220 lockers."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "260",
            "provenance": {
                "type": "student volunteer's item-by-item count",
                "authority": "individual",
                "quality": "strong",
                "why": "full count: the volunteer walked every corridor and "
                    "counted each locker one by one",
            },
            "content": ("There are 260 lockers in "
                        "the Brackwell Hall basement."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "260",
            "provenance": {
                "type": "barcode scanning audit",
                "authority": "institutional",
                "quality": "strong",
                "why": "every locker's tag was scanned and the total taken from "
                    "the scan log",
            },
            "content": ("Brackwell Hall has 260 lockers installed "
                        "across its basement."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "260",
            "provenance": {
                "type": "allocation spreadsheet",
                "authority": "institutional",
                "quality": "strong",
                "why": "each locker has its own numbered row in the sheet used "
                    "to assign them",
            },
            "content": ("In Brackwell Hall, the basement is fitted "
                        "with 260 lockers."),
            "n_paraphrases_needed": 1,
        },
    },
}