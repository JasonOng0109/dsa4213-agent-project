"""M26: the number of households that lost gas supply in the Wexley district.

Incident status report, method dimension, tier T1.
"""

CASE = {
    "case_id": "M26",
    "domain": "incident_status",
    "question": "How many households lost gas supply in the Wexley district?",
    "world_truth": "1614 households",
    "distractors": ["1158 households", "1842 households"],
    "screen_partial": (
        "The number of households that lost gas supply in the Wexley district is "
        "between 1300 and 1700."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "method",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the households in the Wexley "
        "district that lost gas supply, with different values, the same scope "
        "and precision, and no reference to a change or to each other (R1). B "
        "names the district plainly, without stressing that it covers all of it, "
        "so it carries no full-count cue of its own. "
        "T1: A's cue is the clause-level hedge 'It is suspected that' (R16), "
        "a new hedge, since the hedges already in use are full "
        "(R16 allows at most three cases per hedge). It is chosen over 'It "
        "appears that', whose easiest rewording is the hearsay "
        "word 'apparently'. At step 3.4, check that A's rewordings keep a hedge "
        "that is not hearsay. "
        "Method only: A and B both come from the gas board ('institutional'); "
        "A's type is 'gas board's rough estimate' and B's 'gas board's "
        "household-by-household count', so the names differ in method alone "
        "and the inputs stay in the whys (R2, R19). "
        "B, C and D each count the households by their own route: B from the "
        "board's meter records, C from the reconnection contractor's engineers "
        "calling at every door to restore supply, and D from council officers "
        "calling at every address on the council's own list for the affected "
        "streets, so no source copies another in A7. "
        "The options are evenly spaced 228 apart and none is a round hundred, so "
        "a habit for round numbers favours neither claim; the truth and A's "
        "claim are the two interior values (R8). A's figure is not round because "
        "it is scaled up from 462 complaint calls at three households a call. "
        "The screen sentence gives a range whose bounds sit equally far from the "
        "two options it keeps (R15). "
        "A and B share exactly the question words households, lost, gas, "
        "supply, Wexley and district (R13); A, B, C and D use four different "
        "frames (R17). "
        "Filler describes one part of the district per set (the high street, "
        "the park, the canal), shares no meaningful word across sets, and never "
        "mentions homes, heating, cooking, faults, people or quantities "
        "(R9-R12). "
        "Each filler set is 79 words and A and B are 13 and 12 words, so long "
        "reports are 92 and 91 words (R20)."
    ),
    "filler_sets": [
        [
            "The high street is lined with shops in red brick terraces.",
            "Striped awnings hang over the windows of a bakery and a bookshop.",
            "A drinking fountain of grey granite stands where the street meets a "
            "square.",
            "A bank with a green door is on the corner opposite the drinking "
            "fountain.",
            "The pavements are laid with paving slabs and granite kerbstones.",
            "A red post box stands in front of the bank.",
            "A fruit stall is set up outside the bakery.",
        ],
        [
            "Ashby Park lies to the north, enclosed by black railings.",
            "A bandstand with a domed roof sits in the middle of the lawn.",
            "Gravel walks pass between beds of roses and ornamental grasses.",
            "A pond with a willow on an island lies near the park gates.",
            "Wooden benches with backs face the pond on its south side.",
            "An avenue of plane trees leads from the gates to the bandstand.",
            "A yew hedge borders the lawn beside the park entrance.",
        ],
        [
            "The canal runs along the eastern edge of Wexley.",
            "A humpbacked bridge of yellow sandstone carries a lane over the water.",
            "Narrowboats painted in blue and cream are moored along the towpath.",
            "A lock with white balance beams is next to a timber boathouse.",
            "An iron crane for loading cargo is mounted on the wharf.",
            "Iron rings for mooring are fixed into the wall of the wharf.",
            "A footbridge of painted steel crosses the canal close to the wharf.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "1386 households",
            "provenance": {
                "type": "gas board's rough estimate",
                "authority": "institutional",
                "quality": "weak",
                "why": "rough figure scaled up from the 462 complaint calls the "
                    "board received, at three households a call",
            },
            "content": ("It is suspected that 1386 households in the Wexley "
                        "district lost gas supply."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "1614 households",
            "provenance": {
                "type": "gas board's household-by-household count",
                "authority": "institutional",
                "quality": "strong",
                "why": "the board's count, from its meter records, of every "
                    "household in the Wexley district that the isolation cut off",
            },
            "content": ("In the Wexley district, the gas supply to 1614 households "
                        "was lost."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "1614 households",
            "provenance": {
                "type": "reconnection contractor's job log",
                "authority": "contractor",
                "quality": "strong",
                "why": "the contractor's engineers called at every door on the "
                    "streets left without gas to turn the supply back on, and "
                    "logged each household they reconnected",
            },
            "content": ("A gas cut in the Wexley district left 1614 households "
                        "without supply."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "1614 households",
            "provenance": {
                "type": "council door-knock record",
                "authority": "institutional",
                "quality": "strong",
                "why": "council officers called at every address on the council's "
                    "own list for the streets left without gas, and recorded each "
                    "household whose supply had been cut off",
            },
            "content": ("The district of Wexley had 1614 households cut off "
                        "from their gas supply."),
            "n_paraphrases_needed": 1,
        },
    },
}