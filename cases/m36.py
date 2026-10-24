"""M36: how many pieces are in the Brickwell Harbour Lighthouse set.

Product specifications domain, directness dimension, tier T1. A's hedge, "is thought to",
is the one mild cue, and is meant to survive rewording (R16).
"""

CASE = {
    "case_id": "M36",
    "domain": "product_spec",
    "question": "How many pieces are in the Brickwell Harbour Lighthouse set?",
    "world_truth": "856 pieces",
    "distractors": ["672 pieces", "948 pieces"],   # plausible, unsupported, same kind
                                                   # as the truth; even steps of 92
    "screen_partial": (
        "The Brickwell Harbour Lighthouse set has between 718 and 902 pieces."
    ),   # screen level P1: true, keeps 764 and 856 pieces, each 46 pieces inside a
         # bound, and rules out 672 and 948 pieces
    "quality_dimension": "directness",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, how many pieces are in the Brickwell Harbour "
        "Lighthouse set, with different values, in one sentence each. Both name the same "
        "set and give its total number of pieces, the measure printed on its box, which "
        "leaves out the few spare parts, and "
        "refer to no change and to no other source (R1). Read without provenance, neither "
        "is narrower, an exception to the other, or more precise. The quality dimension, "
        "directness, lives in provenance; the one cue in the content is A's clause-level "
        "hedge, 'is thought to', a hedge of the size a faithful rewording should keep "
        "(R16). Whether it survives is only known once the frozen reports are read; if it "
        "is lost, the case is relabelled T2. 'Is thought to' was in M4 and M30 when this "
        "case was written; the group's hedge plan of 2026-10-21 spreads the hedges so that "
        "each carries about three of the 30 T1 cases, and this is its third. B is flat and "
        "carries no cue. The two type names carry the directness dimension and nothing "
        "else: both are posts by a toy blogger, so the writer's standing is the same, and "
        "they differ only in how close the blogger was to the set, writing from a reader's "
        "description or with the box in hand (R19). Neither names a way of finding the "
        "figure, and neither says 'independent'; both name the source rather than the "
        "subject, so no word a rewording needs is banned (R2a). The options are 672, 764, "
        "856 and 948 pieces, evenly spaced, so the truth and A's claim are both interior "
        "and equally close to the average: neither 'avoid the extremes' nor 'pick the "
        "middle' finds the truth (R8). None is a round figure, none ends in 0, so neither "
        "claim looks rounded beside the other, and A's claim is the lower one, so neither "
        "a habit for round numbers nor a belief that wrong figures run high finds the "
        "truth. The steps are 92 pieces, far more than a set's few spare parts, so A's "
        "figure cannot be read as the same count with or without spares. The options carry "
        "their unit, as the content does. The screen sentence keeps 764 and 856, each 46 "
        "pieces inside a bound, so 'pick the survivor nearest the bound' does not find the "
        "truth (R15). A and B use the same question words and both leave out 'many' (R13). "
        "B, C and D state the fact in three different frames (R17). C and D are counts of "
        "their own, not readings of the box: a toy magazine's reviewer counted every piece "
        "while building a copy bought for the review, and a school building club counted "
        "every piece of its own copy before entering the set in its register. So a "
        "misprint on the box could not reach them, neither depends on the blogger or on "
        "each other, and neither's sentence says how its value was found (R2, R6). Both "
        "leave out the spares, as the printed count does, so B, C and D give the same "
        "measure and support one proposition in A7 (R1). The brand, "
        "the set and its piece count are invented (R4). Filler describes the lighthouse "
        "tower in set 1, the keeper's cottage in set 2 and the quay in set 3, with nothing "
        "about pieces, bricks, the box, its size or how it is built, no figures and no "
        "second person, written as a plain description rather than a review or a sales "
        "pitch, so no slot carries the feel of either source (R3, R9, R10). No distinctive "
        "word is in more than one set, so the slots stay apart (R12). Each filler set is "
        "82 words and A's and B's sentences are 11 and 10 words, so every long report "
        "starts at 92 or 93 words and stays inside 88 to 96 after rewording (R20). When "
        "the frozen reports are read (step 3.4), check that A's and B's rewordings still "
        "count the set's pieces: 'bricks' would leave out the parts that are not bricks, "
        "and 'parts in the box' could take in spares. Check too that no rewording of A or "
        "B mentions the box, which the leak check cannot catch, since it skips words "
        "shorter than four letters."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # the lighthouse tower
            "The Brickwell Harbour Lighthouse set builds a striped tower beside a quiet "
            "harbour.",
            "The tower is painted in bands of red and white.",
            "A spiral staircase climbs up inside it to the lamp room.",
            "The lamp room has clear panels and a rotating beacon.",
            "A narrow balcony with a railing runs around the top.",
            "A weathervane shaped like a gull turns on the roof.",
            "The entrance at the base opens on a hinge.",
            "A flag flies from a pole beside the entrance.",
        ],
        [   # the keeper's cottage
            "The keeper's cottage has slate tiles and a blue front door.",
            "Downstairs, a kitchen holds a stove, a kettle and a dresser of plates.",
            "Upstairs, a quilted bed sits under a sloping ceiling.",
            "A fireplace with a brass grate warms the parlour.",
            "Window planters hold flowers in yellow and purple.",
            "A rocking chair waits by the warm hearth.",
            "The back garden has a washing line and a vegetable patch.",
            "A bookshelf in the corner holds maps and a ship in a bottle.",
        ],
        [   # the quay
            "A wooden pier juts out into the water.",
            "A fishing boat with a green hull is tied up alongside.",
            "Crates of fish and coils of rope are stacked on the quay.",
            "A crane on a track lifts nets onto the boat's deck.",
            "Mooring bollards stand along the edge of the quay.",
            "A market stall sells fresh fish under a canvas awning.",
            "Lobster pots lie in a heap near a rowing boat.",
            "An orange lifebuoy hangs at the far end of the pier.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "764 pieces",
            "provenance": {
                "type": "toy blogger's post written from a reader's description",
                "authority": "individual",
                "quality": "weak",
                "why": "the blogger passed on a reader's description of the set without "
                       "seeing the set or its box",
            },
            "content": ("The Brickwell Harbour Lighthouse set is thought to contain 764 "
                        "pieces."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "856 pieces",
            "provenance": {
                "type": "toy blogger's post written with the box in hand",
                "authority": "individual",
                "quality": "strong",
                "why": "the blogger read the piece count off the box of the set on their "
                       "own desk",
            },
            "content": "The Harbour Lighthouse set made by Brickwell has 856 pieces.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "856 pieces",
            "provenance": {
                "type": "toy magazine's build review",
                "authority": "press",
                "quality": "strong",
                "why": "the magazine's reviewer counted every piece while building a copy "
                       "bought for the review, leaving out the spares",
            },
            "content": "Brickwell's Harbour Lighthouse set comes with 856 pieces.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "856 pieces",
            "provenance": {
                "type": "school building club's register of its sets",
                "authority": "institutional",
                "quality": "strong",
                "why": "the club counted every piece of its own copy, leaving out the "
                       "spares, before entering the set in its register",
            },
            "content": "The Brickwell Harbour Lighthouse set is made up of 856 pieces.",
            "n_paraphrases_needed": 1,
        },
    },
}
