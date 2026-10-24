"""M29: how many market stalls flooded when a water main burst on Corvanne High Street.

Incident status report, directness dimension, tier T1.
"""

CASE = {
    "case_id": "M29",
    "domain": "incident_status",
    "question": (
        "How many market stalls were flooded when a water main burst on Corvanne "
        "High Street?"
    ),
    "world_truth": "21 market stalls",
    "distractors": ["11 market stalls", "26 market stalls"],
    "screen_partial": (
        "Between 13 and 24 market stalls were flooded when a water main burst on "
        "Corvanne High Street."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "directness",
    "difficulty_tier": "T1",

    "design_notes": (
        "A scenario of its own: no other case is about a burst water main or a "
        "street market. "
        "A and B state the same proposition about the market stalls flooded "
        "when a water main burst on Corvanne High Street, with different values, "
        "the same scope and precision, and no reference to a change or to each "
        "other (R1). "
        "T1: A's cue is the modal hedge 'may have flooded' (R16), shared with, "
        "M12 ('may well have'), within R16's three cases per hedge. At step 3.4, "
        "check that A's rewordings keep a modal of "
        "doubt ('may', 'might'). "
        "Directness only: A and B are both messages from traders "
        "('individual'), but A repeats what another trader said while B was "
        "written by a stallholder on the street, so the pair differs in "
        "directness, not authority, medium or method (R2, R19). "
        "B, C and D each count the stalls by their own route: B a stallholder who "
        "saw each one, C the water company's assessor calling at every stall, "
        "and D the council's market inspector walking the street on their own "
        "sheet, so no source copies another in A7. "
        "The options are evenly spaced 5 stalls apart, with the truth and A's "
        "claim as the two interior values (R8). The screen sentence gives a range "
        "whose bounds sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words market, stalls, flooded, "
        "water, main, burst, Corvanne, High and Street (R13); A, B, C and D use "
        "four different frames (R17). "
        "Filler describes one building per set (the town hall, the church, the "
        "library and its garden), shares no word across sets, and never "
        "mentions water, drains, slopes, shops, stalls, people, weather, time or "
        "quantities (R9-R12). "
        "Each filler set is 78 words and A and B are 14 words each, so long "
        "reports are 92 words (R20)."
    ),
    "filler_sets": [
        [
            "The town hall of Corvanne stands at the north end of the High Street.",
            "It is made of sandstone, with a tower above the entrance.",
            "A flag on a pole flies from the top of the tower.",
            "Stone steps lead up to the oak doors.",
            "A coat of arms is set into the stonework over the doors.",
            "Lamps on iron brackets hang on either side of the entrance.",
            "A bronze statue stands on a plinth before the hall.",
        ],
        [
            "A church with a spire faces the square from the east.",
            "Its walls are of flint, with a roof of grey slate.",
            "A lychgate with a tiled roof opens onto the churchyard.",
            "Yews line the path to the porch.",
            "Stained glass is fitted in the windows of the nave.",
            "A brass cross crowns the spire.",
            "Ivy climbs the churchyard boundary beside the lychgate.",
            "Headstones rest in the grass beside the path.",
            "The porch has a bench of elm.",
        ],
        [
            "The library is a building of red brick.",
            "A portico with pillars marks its front.",
            "Behind the library is a garden laid out with gravel walks.",
            "Rose beds border the walks, and a birdbath sits in the centre.",
            "A pergola covered in wisteria runs beside the walks.",
            "Seats of teak are placed under a cedar.",
            "Holly grows along the rear of the library.",
            "A hedge with a gate encloses the garden.",
            "Lavender fills a bed by the gate.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "16 market stalls",
            "provenance": {
                "type": "trader's message relaying another trader's account",
                "authority": "individual",
                "quality": "weak",
                "why": "secondhand: repeats what another trader told them",
            },
            "content": ("The burst water main on Corvanne High Street may have "
                        "flooded 16 market stalls."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "21 market stalls",
            "provenance": {
                "type": "trader's message sent from the street",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand: written by a stallholder on the street who saw "
                    "each stall that flooded",
            },
            "content": ("On Corvanne High Street, 21 market stalls were flooded "
                        "after a water main burst."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "21 market stalls",
            "provenance": {
                "type": "water company damage assessor's list",
                "authority": "institutional",
                "quality": "strong",
                "why": "the water company's assessor called at every stall on the "
                    "street and listed each one the water had reached",
            },
            "content": ("Water from the main that burst under Corvanne High Street "
                        "got into 21 stalls in the market."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "21 market stalls",
            "provenance": {
                "type": "council market inspector's record",
                "authority": "institutional",
                "quality": "strong",
                "why": "the council's market inspector walked the street and "
                    "recorded each stall that had flooded, on their own sheet",
            },
            "content": ("The Corvanne High Street burst left 21 of the street's "
                        "market stalls under water."),
            "n_paraphrases_needed": 1,
        },
    },
}