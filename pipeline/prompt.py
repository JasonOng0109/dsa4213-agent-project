"""
The judge prompt (proposal §3): the question, numbered options, the reports and an
optional provenance note, then a request for a JSON object holding the chosen answer as
a verbatim string and a probability for every option. No reasoning is asked for.

Options are numbered, never lettered, so answer labels cannot be confounded with the
indices of the evidence items, and models' prior over option letters is avoided.
"""

TEMPLATE = """You are asked to answer a factual question based on reports from others.
Read all reports below, then give your answer.

Question: {question}
Possible answers:
{numbered_options}

{reports_block}
{provenance_block}
Respond with ONLY a JSON object in exactly this format, nothing else:
{{"answer": "<one of the possible answers, verbatim>",
 "p": {{"<answer text>": <integer 0-100>, ...}}}}

"p" must give a probability for every possible answer listed above, using the
answer text as the key, and the values must sum to 100.
{abstain_line}
Do not include any explanation or reasoning -- output only the JSON object."""

ABSTAIN = "Cannot be determined from the evidence provided"
ABSTAIN_LINE = (f'If the reports do not determine the answer, you may instead answer '
                f'exactly "{ABSTAIN}", still giving "p" over the numbered answers above.\n')
# A0 shows no reports; "read all reports below" followed by nothing would read as a
# truncated prompt.
NO_REPORTS = "(No reports are available for this question.)"


def render_reports(reports: list[dict]) -> str:
    lines = []
    for r in reports:
        suffix = f" (source: {r['provenance_id']})" if r.get("provenance_id") else ""
        lines.append(f"{r['agent_label']}{suffix} says: {r['text']}")
    return "\n".join(lines)


def render(trial: dict) -> str:
    provenance_block = trial["provenance_note"] + "\n" if trial["provenance_note"] else ""
    return TEMPLATE.format(
        question=trial["question"],
        numbered_options="\n".join(f"  {i}. {o}"
                                   for i, o in enumerate(trial["answer_options"], 1)),
        reports_block=render_reports(trial["reports"]) or NO_REPORTS,
        provenance_block=provenance_block,
        abstain_line=ABSTAIN_LINE if trial["allow_abstain"] else "",
    )
