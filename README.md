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

### Multi-agent aggregation

| Paper | What it shows | Why it matters here |
|---|---|---|
| Multiagent debate, Du et al. 2023 ([pdf](related_works/multiagent-debate.pdf), arXiv 2305.14325) | Debate treats agreeing outputs as corroboration, with single-model accuracy as the baseline | Anchors belief from **one report**, and asks whether **distinct agent identities** add anything |
| Minority Sentinel, He et al. 2026 ([pdf](related_works/minority-sentinel.pdf), arXiv 2606.29270) | In 2-vs-1 debate splits the majority can be wrong; a learned classifier decides when to overturn it | Motivates a **two-against-one** conflict baseline. Its correlation comes from agent errors; ours is built at the evidence source |
| FREE-MAD, Cui et al. 2025 ([pdf](related_works/free-mad.pdf), arXiv 2509.11035) | An LLM judge aggregating agents is prone to conformity, effectively majority voting | Count is not weight. Its failure needs interaction; our agents never interact |
| Peacemaker or Troublemaker, Yao et al. 2025 ([pdf](related_works/debate-sycophancy.pdf), arXiv 2509.23055) | Sycophancy pushes debates into premature consensus | False agreement from another direction, and a limitation to state: we study one aggregation step, not a whole pipeline |

### Provenance and correlated evidence

| Paper | What it shows | How we differ |
|---|---|---|
| When Not to Write Memory, Qi et al. 2026 ([pdf](related_works/correlated-agent-traces.pdf), arXiv 2607.02579) | "Repetition is not evidence"; provenance metadata with dependency-aware grouping estimates effective support | It groups evidence by a dependency structure the **system already knows**. We measure what the **judge** does when nobody tells it, and once it is told |
| CAMA, Lin et al. 2026 ([pdf](related_works/cama.pdf), arXiv 2608.19701) | Memory Correlation Bias: shared upstream sources form a false majority; a trained module infers the effective number of sources | Its fix is a module **outside** the model. Ours is one sentence **inside** the message |
| From Agent Traces to Trust, Wang et al. 2026 ([pdf](related_works/agent-traces-to-trust.pdf), arXiv 2606.04990) | Provenance relations (support, derive, depend-on); provenance through paraphrasing is an open challenge | We do not propose a representation; we test whether a **minimal per-trial statement** is used |

### The gap

Where the work that varies *what the model is shown* sits (proposal Figure 1):

| Form of the repeated evidence | Told nothing | Told source identity or type | Told reports share a source | Told relative quality |
|---|---|---|---|---|
| **Independent paraphrases** | **this project** | **this project** | **this project** | **this project** |
| Verbatim copies | | Whose Facts Win? | | |
| Distinct documents | RAMDocs | AuthorityBench | | |

The top row, reworded reports of one source plus a per-trial statement about dependence
or quality, is unoccupied. And the fixes proposed so far each sit somewhere else:

| Work | Where the fix is applied |
|---|---|
| Whose Facts Win? | **the model**: fine-tune it so it stops over-weighting repetition |
| When Not to Write Memory, CAMA | **the system**: aggregate outside the model |
| Minority Sentinel | **the debate log**: a classifier decides when to overturn the vote |
| This project | **the message**: a statement about the specific reports shown, at inference |
