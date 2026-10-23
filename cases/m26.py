"""M26: the number of households that lost gas supply in the Wexley district.

Incident status domain, method dimension, tier T1.
"""

CASE = {
    "case_id": "M26",
    "domain": "incident_status",
    "question": "How many households lost gas supply in the Wexley district?",
    "world_truth": "1500 households",
    "distractors": ["1200 households", "2100 households"],
    "screen_partial": (
        "The number of households that lost gas supply in the Wexley district is "
        "between 1100 and 1600."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "method",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the households across the "
        "whole Wexley district that lost gas supply, with different values, the "
        "same scope and precision, and no reference to a change or to each "
        "other (R1). "
        "T1: A's cue is the hedge 'It appears that' (R16), not used by any other "
        "case. "
        "Method only: A and B both come from the gas board ('institutional'), "
        "but A is an estimate scaled up from complaint calls while B is a count "
        "from meter records, so the pair differs in method, not authority or "
        "directness (R2, R19). B, C and D all count every household on the "
        "isolated section, so the three agreeing sources state the same figure "
        "in A7. "
        "The options are evenly spaced, with the truth and A's claim as the two "
        "interior values (R8). The screen sentence gives a range whose bounds "
        "sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words households, lost, gas, "
        "supply, Wexley and district (R13); A, B, C and D use four different "
        "frames (R17). "
        "Filler describes one part of the district per set (the high street, "
        "the park, the canal), shares no meaningful word across sets, and never "
        "mentions homes, heating, cooking, faults, people or quantities "
        "(R9-R12). "
        "Each filler set is 79 words and A and B are 12 and 13 words, so long "
        "reports are 91 and 92 words (R20)."
    ),
    "filler_sets": [
        [
            "The high street is lined with shops in red brick terraces.",
            "Striped awnings hang over the windows of a bakery and a bookshop.",
            "A drinking fountain of grey granite stands where the street meets a "
            "square.",
            "A red post box stands in front of the bank.",
            "The pavements are laid with paving slabs and granite kerbstones.",
            "A bank with a green door is on the corner opposite the drinking fountain.",
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
            "claim": "1800 households",
            "provenance": {
                "type": "gas board estimate from complaint calls",
                "authority": "institutional",
                "quality": "weak",
                "why": "rough figure scaled up from the number of complaint "
                    "calls the board received",
            },
            "content": ("It appears that 1800 households in the Wexley district "
                        "lost gas supply."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "1500 households",
            "provenance": {
                "type": "gas board count from meter records",
                "authority": "institutional",
                "quality": "strong",
                "why": "a count of every household meter on the isolated section "
                    "of the network",
            },
            "content": ("Across the whole of the Wexley district, 1500 "
                        "households lost their gas supply."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "1500 households",
            "provenance": {
                "type": "network engineer's isolation sheet",
                "authority": "institutional",
                "quality": "strong",
                "why": "lists every household behind the valves closed on the "
                    "isolated section",
            },
            "content": ("A gas cut in the Wexley district left 1500 households "
                        "without supply."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "1500 households",
            "provenance": {
                "type": "council welfare visit register",
                "authority": "institutional",
                "quality": "strong",
                "why": "lists every household on the isolated section, each "
                    "checked by council staff",
            },
            "content": ("The district of Wexley had 1500 households cut off "
                        "from their gas supply."),
            "n_paraphrases_needed": 1,
        },
    },
}