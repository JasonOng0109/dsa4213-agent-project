"""M7: Rated brightness of the fictional LumaDesk S3 desk lamp.

Product specifications, authority quality dimension, tier T1.
Tests conflicting brightness ratings from sources of differing authority.
"""

CASE = {
    "case_id": "M7",
    "domain": "product_spec",
    "question": "What is the rated brightness of the LumaDesk S3 desk lamp?",
    "world_truth": "600 lm",
    "distractors": ["400 lm", "700 lm"],
    "screen_partial": (
        "The LumaDesk S3 desk lamp has a rated brightness "
        "greater than 400 lm and less than 700 lm."
    ),
    "quality_dimension": "authority",
    "difficulty_tier": "T1",
    "design_notes": (
        "This case tests the authority quality dimension using conflicting "
        "rated brightness values for the fictional LumaDesk S3 desk lamp. "
        "Source A is a hobbyist's product listing claiming 500 lm, "
        "while Source B is a national standards authority's product "
        "listing supporting the true value of 600 lm. "
        "Both sources use the same document format, so their quality "
        "difference is institutional standing rather than document type (R19). "
        "A and B describe the same lamp and rated brightness with equally "
        "specific claims and no changes or exceptions (R1). "
        "Both identify the same LumaDesk S3 desk lamp and brightness property, "
        "so neither benefits from a difference in question-related wording (R13). "
        "Source A contains the mild clause-level hedge 'is presumed to have', "
        "which is intended to survive faithful reporter paraphrasing (R16). "
        "The T1 classification remains provisional until the frozen reports "
        "are checked; if the hedge disappears, the case is relabelled T2. "
        "Source identity, authority and evidence-production methods remain in "
        "provenance rather than content (R2). "
        "Sources B, C and D support the same rated brightness of 600 lm using "
        "different sentence frames (R17). C is an accredited assessment body "
        "and D is a product compliance organisation, with separately maintained "
        "evaluations rather than copies of B's register. Their independence "
        "must still be checked before interpreting A7 as three independent "
        "sources (R6). "
        "The four options are 400, 500, 600 and 700 lm, with the truth and "
        "A's incorrect claim occupying the two interior positions (R8). "
        "The screening sentence retains 500 and 600 lm while excluding "
        "400 and 700 lm, preserving the world truth (R15). "
        "The three filler sets describe distinct physical aspects: the lamp's "
        "base and underside, its shade and stem, and its packaging and "
        "protective materials, with no content word in two sets. They avoid "
        "brightness, controls, electrical performance and source-identifying "
        "language (R9, R10, R12). "
        "Each filler set contains 78 words, and the A and B sentences contain "
        "15 and 13 words respectively, producing long reports of 93 and 91 "
        "words before paraphrasing (R20)."
        "When reading frozen reports in step 3.4, check that A's and B's "
        "paraphrases preserve the rated-brightness meaning. "
        "A shift from rated brightness to actual light output could "
        "make the two claims appear compatible. "
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The lamp rests on a broad circular foot with a slightly raised and rounded rim along its edge.",
            "Its underside carries a dark rubber ring that grips the surface beneath it.",
            "A shallow groove runs around the edge, separating the upper shell from the lower plate.",
            "The foot has a gently curved profile without sharp corners or exposed fasteners.",
            "A small recessed panel underneath sits flush with the surrounding material and can be lifted using a narrow notch.",
        ],
        [
            "The shade is a wide dome with a neatly rolled lip that frames its opening.",
            "Its outer face is coated in a muted cream colour with a fine, even eggshell texture.",
            "A slim chrome collar joins the shade to the stem at its crown.",
            "The stem has a satin finish.",
            "The shade bears no markings, motifs or lettering of any kind.",
            "A fine seam traces the contour of the dome, and the lip feels smooth to the touch.",
        ],
        [
            "The lamp arrives inside a rectangular cardboard carton with carefully folded flaps at either end and a reinforced bottom board.",
            "Moulded paper inserts hold the loose pieces in place during handling.",
            "A soft fabric sleeve covers the main body, protecting it from scratches inside the box.",
            "The other accessories go in a plain paper envelope tucked beside the inserts.",
            "The carton closes with a tucked tab, and its exterior has a simple geometric pattern printed along the sides.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "500 lm",
            "content": (
                "The LumaDesk S3 desk lamp is presumed to have "
                "a rated brightness of 500 lm."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "hobbyist's product listing",
                "authority": "informal product commentator",
                "quality": "weak",
                "why": (
                    "The website has no recognised institutional standing "
                    "to establish the lamp's rated brightness."
                ),
            },
        },
        "B": {
            "quality": "strong",
            "claim": "600 lm",
            "content": (
                "A rated brightness of 600 lm applies to "
                "the LumaDesk S3 desk lamp."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "national standards authority's product listing",
                "authority": "national standards authority",
                "quality": "strong",
                "why": (
                    "The authority has recognised institutional responsibility "
                    "for maintaining official product ratings."
                ),
            },
        },
        "C": {
            "quality": "strong",
            "claim": "600 lm",
            "content": (
                "The LumaDesk S3 desk lamp is rated "
                "to give 600 lm."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "accredited assessment body",
                "authority": "Accredited lighting assessment organisation",
                "quality": "strong",
                "why": (
                    "The organisation independently evaluates lighting "
                    "performance using its own assessment process."
                ),
            },
        },
        "D": {
            "quality": "strong",
            "claim": "600 lm",
            "content": (
                "For the LumaDesk S3 desk lamp, "
                "600 lm is its rated brightness."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "product compliance organisation",
                "authority": "Recognised lighting compliance organisation",
                "quality": "strong",
                "why": (
                    "The assessor independently evaluates the lamp's "
                    "brightness without relying on the other reports."
                ),
            },
        },
    },
}
