# Instructions for Claude agents in this repository

Project: DSA4213 Group 14, "Counting Reports or Counting Evidence": a controlled study of
whether an LLM orchestrator can discount correlated agent reports, and which disclosed
provenance repairs it. Start with `knowledge-graph.html`: open it in a browser, or read the
JSON inside its `<script id="kg-data">` block. `README.md` explains how to run everything.

This repository is self-contained. Cite only files that are in it.

## Standing rule: keep the knowledge graph current

`knowledge-graph.html` is the shared map of this project for teammates and Claude agents.
Keep it true without being asked.

**When to update it, in the same session, automatically:**
- a new decision is made, in a document or in conversation;
- an earlier decision is reversed, narrowed or replaced;
- documents and code are found to disagree with each other (drift);
- a run produces new results, or an open item is settled.

**How to update it:**
1. If the decision exists only in conversation, first record it in `docs/decisions.md` in
   that file's five-field format, so the graph has a file to cite. Likewise, a method or
   term that needs more than a sentence to explain goes first into `docs/methods.md`, the
   shared dictionary, as an entry in its five-part format; a concept node then summarises
   the entry, quotes it, and links to `methods-doc` with `"rel": "part-of"`.
2. Edit the JSON inside `<script id="kg-data" type="application/json">`, and the page's
   figure code, between `// VISUALS-START` and `// VISUALS-END`, when a figure is stale or
   a node needs a new one. Never delete a replaced decision: set `"status": "superseded"`
   and link the new node to it with `"rel": "replaces"`. When an open or drift item is
   settled, set its status to `current` and record it under `closed` in the changelog.
3. When an open or drift item is settled, sweep for staleness: every node, figure caption,
   README line, doc and code comment that still describes the old state is corrected in
   the same change. The checker cannot read figure text, so grep the figure code for the
   old wording.
4. Every node needs a plain-English `summary` and at least one `evidence` item whose `quote`
   is copied verbatim from a file in this repository. Link every term a reader must
   understand first with `"rel": "needs"`, until the node can be understood from the graph
   alone.
5. Add a `changelog` entry: the date, a one-line summary, and the node ids added, changed,
   superseded, opened and closed.
6. Run `uv run python tools/check_graph.py` and fix every error. A quote that no longer
   matches its file means the source changed: re-read it, then update or supersede the
   node. `uv run pytest` runs the same check.
7. End the reply with a short **Knowledge graph update** report: what was added, changed or
   superseded, which open or drift items were opened or closed, and what the staleness
   sweep corrected. If nothing needed updating, say so in one line.

After editing anything under `docs/`, `cases/`, `pipeline/` or the README, run the checker
even if no decision changed: a broken quote is how drift is caught.

## Writing rules for the graph

- Simple English. Where a picture explains better than words, give the node a `visual`:
  reuse a figure the page defines, or add one to the figure code, built from the page's
  helpers (`fig`, `svgWrap`, `hbars`, `T`) and colour classes. A figure shows only what
  its node's evidence supports, and numbers it takes from a file go in the node's `data`,
  beside that evidence. The checker cannot read figure code, so open the page at
  `knowledge-graph.html#n=<node id>` and look at the figure in both light and dark mode.
- No statement without a trace. If a claim cannot be quoted from a file in this
  repository, add the source first or leave the claim out.
- Numbers from instrumentation runs, such as a dry run on the mock backend, are marked
  `"internal": true` and must not be carried into the report as findings.
