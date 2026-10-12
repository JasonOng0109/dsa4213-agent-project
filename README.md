# Counting Reports or Counting Evidence

What provenance an LLM orchestrator needs to discount correlated agent reports.

DSA4213 Natural Language Processing for Data Science, Group 14, Semester 1 AY2026/2027.

## Research question

> When several agents report the same claim, can an orchestrating LLM distinguish the
> number of agreeing reports from the number and quality of independent documents
> underlying them, and what information must it be given before it does?

The question has two halves, and the study keeps them apart:

1. **Does the failure happen at all** once the repeated reports are paraphrases rather
   than copies?
2. **Which disclosure repairs it?** Provenance is treated as a graded variable, not as
   something that is either present or absent.

## Why this is an agent problem

In a multi-agent pipeline the orchestrator sees reports, not documents. Agents in one
framework often share a retriever, a tool or a base model, so their outputs are
correlated by construction: one piece of evidence arrives as three apparent witnesses.
An orchestrator that counts them as three independent confirmations becomes confidently
wrong in exactly the situation a multi-agent design is meant to guard against. A single
model reading a single document cannot produce this failure.

The practical question for a system builder is what to put in the message envelope that
passes between agents: a source identifier, a source name, a dependency flag, or a
quality score. Each costs something to plumb through a framework, and we know of no
benchmark that says which of them changes the outcome.

## Setting

Any orchestrator-plus-workers deployment that aggregates reported evidence: research
assistants that fan out sub-queries, triage systems that poll several tools, debate
frameworks that pool agent answers. All of them hand the aggregator reports whose
dependence structure is invisible in the text.

## Related work

Papers live in [`related_works/`](related_works/); the proposal's §2 has the full
discussion and the reference list.

### Where the study sits

| Paper | What it gives us |
|---|---|
| Knowledge conflicts survey, Xu et al. 2024 ([pdf](related_works/knowledge-conflicts-survey.pdf), arXiv 2403.08319) | The name of our setting: **inter-context conflict**. The conflict is between pieces of supplied evidence, not between evidence and what the model already believes. |
| ClashEval, Wu et al. 2024 ([pdf](related_works/clasheval.pdf), arXiv 2404.10198) | The neighbouring case, context against the model's prior: models adopt wrong retrieved content over correct prior knowledge more than 60% of the time. We remove that axis on purpose by using **fictional entities** throughout. |

### The nearest benchmarks, and what each leaves open

| Paper | What it shows | What it leaves open |
|---|---|---|
| RAMDocs / MADAM-RAG, Wang et al. 2025 ([pdf](related_works/ramdocs.pdf), arXiv 2504.13079) | One agent per document, an aggregator combining the debate, and baselines that degrade as the count of documents behind each answer becomes unequal | Every evidence unit is a distinct document, so **report count and source independence move together** and cannot be separated |
| AuthorityBench, Yao et al. 2026 ([pdf](related_works/authoritybench.pdf), arXiv 2603.25092) | Models perceive source authority from the URL alone, and filtering on it helps | Authority is a property of a source, never a statement about the reports in front of the model; whether two documents **share a source** is never stated or varied |
| Whose Facts Win?, Schuster et al. 2026 ([pdf](related_works/whose-facts-win.pdf), arXiv 2601.03746) | A stable credibility hierarchy that repetition reverses, already split into segmentation (gap 33.90 vs 6.17 when merged) and source identity (30.04 under one source) | Repeated evidence is **verbatim copies**, which deduplication would remove; the prompt-level fix fails and the working fix is fine-tuning, so nobody tells the model anything **per trial** |

Whose Facts Win? is why the first two effects we test are *expected* rather than new.
Our version differs in three ways: repeated reports are independently generated
paraphrases, decisions are scored against a known world truth, and the judges are
frontier models.
