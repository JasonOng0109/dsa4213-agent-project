"""M17: Package holding limit at Highfield Parcel Centre.

Institutional logistics domain, directness quality dimension, tier T1.
"""

CASE = {
    "case_id": "M17",
    "domain": "institutional_logistics",
    "question": "What is the package holding limit at Highfield Parcel Centre?",
    "world_truth": "19 days",
    "distractors": ["13 days", "22 days"],  # [13, 16, 19, 22]
    "screen_partial": (
        "The package holding limit at Highfield Parcel Centre is between 15 days and 20 days."
    ),  # keeps 16 and 19 (truth); rules out 13 and 22; both survivors sit 1 day inside bounds (R15)
    "quality_dimension": "directness",
    "difficulty_tier": "T1",
    "design_notes": (
        "Directness dimension, T1. A and B state the same proposition (the package holding "
        "limit at Highfield Parcel Centre) as single sentences with identical scope (R1). "
        "Both contain the exact same six question content-words: package, holding, limit, "
        "Highfield, Parcel, and Centre (R13). The T1 cue is A's clause-level hedge "
        "'is presumed to be' (R16), which survives faithful paraphrasing while varying from "
        "cues used in earlier cases ('is understood to', 'is believed to', 'is reckoned to'). "
        "Quality resides strictly in provenance (R2, R19). Under Phase 4 "
        "directness rules, both writers have the same individual standing as logistics couriers, "
        "isolating directness: A relies on second-hand information passed on by a driver who was "
        "not at the depot, whereas B relies on first-hand notes written at the intake desk itself (R19). "
        "Neither type name leaks methodology, authority differences, or the word 'independent' (R19). "
        "Sources B, C, and D state the truth using distinct syntactic frames to keep bigram overlap "
        "below 0.40 (R17). B, C, and D also reach the figure by separate routes: B records the briefing, "
        "C records the decision that set the limit, and D observes the limit applied to an uncollected test "
        "parcel. Distractors form a balanced spread [13, 16, 19, 22], with the truth (19) and "
        "A's claim (16) occupying the interior positions (R8). The screen sentence uses two bounds "
        "(15 and 20 days), placing both survivors (16 and 19) exactly 1 day inside the bounds (R15). "
        "Content lengths are A=14, & B=14 words. Each filler set is 77-79 words, "
        "landing every long report is within the tight 91-93 band (R20). Fillers describe "
        "neutral physical building environments across three separate zones without cross-set noun sharing "
        "(R12), and contain no numbers, time markers, "
        "prohibited words, or package holding vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "The concrete loading apron has yellow perimeter lines beside raised docking platforms and broad metal doors.",
            "A steel roller shutter covers the central machinery ramp above a dark strip of ribbed flooring.",
            "Heavy rubber buffers sit beside wide openings, with square blocks fixed along the concrete wall.",
            "Overhead floodlights cast pale reflections across the tarmac beneath tall lattice supports and roof gutters.",
            "Galvanised drainage grilles cross a shallow trench beside the paving and a low retaining wall.",
        ],
        [
            "Polished terrazzo tiles lead from glass entry partitions toward a curved oak staircase and a tall arched window.",
            "A brass handrail follows the stair curve above pale plaster walls and a dark wooden skirting board.",
            "Soft ceiling panels form a broad pattern beneath pendant lamps and a circular skylight.",
            "A tall ceramic planter holds glossy leaves beside a narrow doorway with frosted glass.",
            "Framed landscape prints hang above a long console with turned legs and a stone surface.",
        ],
        [
            "A gravel driveway curves beside clipped hedges, pale walls, and a low slate roof beyond the entrance.",
            "Cedar shutters frame the tall windows of a detached stone cottage beside a narrow flower border.",
            "A wooden footbridge crosses a shallow ornamental stream between smooth lawns and planted beds.",
            "Smooth paving surrounds a circular fountain with a carved basin and a low surrounding parapet.",
            "Ivy climbs a garden wall beside a small glasshouse with white frames and a peaked roof.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "16 days",
            "content": (
                "Highfield Parcel Centre's holding limit for a package is presumed to be 16 days."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "summary passed on by a courier who missed the intake briefing",
                "authority": "individual",
                "quality": "weak",
                "why": "second-hand information heard from another driver rather than directly recorded during the depot briefing",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "19 days",
            "content": (
                "Packages at Highfield Parcel Centre are stored for a holding limit of 19 days."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "notes taken at the intake desk by a courier at the briefing",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand notes recorded contemporaneously on site during the parcel centre's intake briefing",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "19 days",
            "content": (
                "A parcel-centre entry records that an uncollected package is returned after 19 days."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "warden's own decision notes",
                "authority": "parcel centre warden",
                "quality": "strong",
                "why": "the warden's own entry recording the committee decision that set the package holding limit",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "19 days",
            "content": (
                "A consumer group found that an uncollected package was returned after 19 days at Highfield Parcel Centre."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "consumer group test report",
                "authority": "consumer group",
                "quality": "strong",
                "why": "a consumer group sent test parcels to the centre, left them uncollected and logged the day each was returned once the holding limit ran out",
            },
        },
    },
}