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

### Controls for other explanations

| Paper | What it shows | The control it motivates |
|---|---|---|
| Explaining Length Bias, Hu et al. 2025 ([pdf](related_works/length-bias.pdf), arXiv 2407.01085) | Length wins only when it adds information: three copies of a response *lose* (50.0 to 13.0 on AlpacaEval) | Report **length** as a trial-level factor, and a cap on length differences within a trial |
| Susceptibility to Influence, Griffin et al. 2023 ([pdf](related_works/llm-susceptibility.pdf), arXiv 2303.06074) | Prior exposure to a statement raises an LLM's later truthfulness rating | **Segmentation** into separate messages gets its own condition |

### Correlation neglect

The quantity we estimate is not new. Correlation neglect, failing to account for
repetition in the information one receives, is formalised by DeMarzo, Vayanos and
Zwiebel (*Persuasion bias, social influence, and unidimensional opinions*, QJE 118(3),
2003) and shown experimentally by Enke and Zimmermann (*Correlation neglect in belief
formation*, REStud 86(1), 2019), both for human decision makers. Measuring it in an LLM
orchestrator, on a benchmark built so the quantity is identifiable, is the
contribution. (Both are journal papers; no PDF is kept here.)

## Hypotheses

H1 and H2 restate effects that prior work already indicates, tested here in a harder
setting. H3 to H6 are the study's own targets.

| | Hypothesis | Status |
|---|---|---|
| H1 | Correlated repetition raises the orchestrator's confidence and can beat a single better-sourced report | Expected from prior work; tested with paraphrases and against ground truth |
| H2 | The rise is driven by report redundancy and segmentation, not by distinct agent identities | Expected from prior work; tested under lexical non-identity |
| H3 | Stating that two reports share a source shifts belief but does not change the decision | **Primary target** |
| H4 | Stating relative source quality does change the decision | **Primary target**, with strength of wording as a factor |
| H5 | Judges infer quality from named source types without being told | Secondary; calibrates against prior work |
| H6 | Forced choice conceals a judge's belief state: where its stated probabilities do not identify the answer it gives (near indifference, or favouring another option), an explicit "cannot be determined" option will be taken when offered | **Primary target** |

**Success** means that for each of H3, H4 and H6 the contrast either shows the predicted
effect, consistent in direction across judges and cases, or rules it out. A null on H3
is as useful as a confirmation: it tells builders a dependency flag alone does not
repair aggregation. The project fails only if the instrument is uninterpretable:
provenance leaking into report text, parse failures, or judges whose stated numbers
carry no information and whose decisions are unstable.

## Contribution

The single claim the design is built to decide: **disclosure about sources changes what
an aggregator believes, while only a statement of relative quality changes what it
chooses.**

1. **The disclosure dissociation.** Dependence, quality, and both, each stated per trial.
2. **Belief versus choice.** A decision *and* a probability for every option, plus an
   abstention arm, so a judge whose numbers disagree with its answer is visible.
3. **Correlated evidence that deduplication does not remove.** Independently generated
   paraphrases that pass an equivalence check and an overlap filter, with provenance
   kept out of the text by construction and by a linter.
4. **Frontier orchestrators**, with a reasoning on/off comparison as optional work.
5. **A quantity, not only accuracy**: the number of independent sources the judge
   behaved as if it saw.

**What we will not claim**: that repeated weaker sources beating one stronger source is
new, that splitting repetition into segmentation and identity is new, or that
majority-following in LLMs is new. Each has a prior anchor above.
