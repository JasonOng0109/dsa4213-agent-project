"""
The reporter stage (proposal §3): generate candidate reports for each source, check
them against the acceptance criteria, select the number needed, and freeze them.

The reporter is handed a source's `content` only, never its provenance. A candidate is
accepted only if
  (a) an independent rater passes it on a four-flag equivalence rubric,
  (b) it is not a near copy of the source, and its bigram overlap with the other
      selected candidates is at most 0.50,
  (c) it uses no word found only in the source's type description, and no invented
      attribution phrase,
  (d) its length is within 3 words of the source's, so filler written for the source
      sentence still fits the long-report band (R20),
and, as the R17 backstop, it is no more alike than 0.50 to the accepted reports of any
source that can share a trial with it.

Failure means regenerate, never hand-edit: six candidates per round, at most two rounds,
the second re-rating the first round's candidates alongside its own. A source still
short after that stops the run; no threshold is ever loosened.
"""

from __future__ import annotations
import json
import re

CANDIDATES_PER_ROUND = 6
MAX_ROUNDS = 2
SEMANTIC_MIN = 0.80     # rubric score; used for ranking, the four flags do the gating
COPY_MAX = 0.70         # bigram overlap with the source itself
PAIR_MAX = 0.50         # bigram overlap between two accepted reports of one source
CROSS_MAX = 0.50        # ... and of two sources that can share a trial (R17)
LENGTH_DIFF_MAX = 3     # words a report may differ from its source's length (R20)

# Sources that can appear in the same trial: A with B in the conflict block, and B, C
# and D together in A7. R17 keeps their reports from reading like copies of one another.
CO_OCCURRING_PAIRS = [("A", "B"), ("B", "C"), ("B", "D"), ("C", "D")]

REPORTER_PROMPT = """You will be shown a single source document and a question. Write ONE short
report (1-2 sentences) that faithfully conveys what this source says about
the question.

Rules:
- State only the proposition and evidential content contained in the source.
- Include EVERY factual detail the source gives (e.g. day, time, location,
  model numbers, bands). Do not drop a detail just because the question
  only asks about one of them -- you are relaying the source, not answering
  the question.
- Preserve the source's evidential strength exactly: if the source is
  tentative, hedged, or secondhand, your report must sound equally
  tentative; if it is stated as direct fact, state it as fact.
- Do not add outside knowledge, interpretation, certainty, or uncertainty
  beyond what the source contains.
- Do not mention the source's name, format, or type (e.g. do not say
  "according to this document" or "the spec sheet says") -- write as if you
  personally found this out.
- Vary sentence structure and wording from any other report you produce for
  the same source.
{avoid_block}{forbid_block}
What it says:
{source_content}

Question: {question}

Report:"""

FORBID_BLOCK = """
Your earlier reports were rejected for mentioning where the information
came from. Do NOT use any of these words: {words}.
"""

# Each reporter call is independent, so the model cannot "vary from other reports" it
# never saw -- left alone it collapses to one phrasing. We show it the wordings already
# produced for this source and ask for something new.
AVOID_BLOCK = """
Reports already written for this source (do NOT reuse their sentence
structure or wording; say the same thing a genuinely different way):
{prior}
"""

# One overall 0-100 score saturates -- a strict rater gives almost every faithful-looking
# candidate 100 -- so a threshold on it never binds. Four booleans, each a separate reason
# to reject, plus a score kept for ranking.
RUBRIC_PROMPT = """RUBRIC CHECK. You are checking whether a candidate report faithfully
restates a source statement. Judge each point strictly and literally.
Rewording, reordering and changes of grammatical form are fine; any change
of meaning is not.

Source statement: {source_text}
Candidate report: {candidate_text}

Answer each question true or false:
- all_details: does the candidate state EVERY factual detail the source
  states -- every entity, value, unit, condition and qualifier?
- nothing_added: does the candidate avoid adding anything the source does
  not contain -- no extra fact, detail, certainty, hedge, or description of
  where the information came from?
- values_unchanged: is every value (number, name, place, date, quantity)
  exactly the same as in the source?
- scope_kept: does the candidate keep the source's denominator or scope
  wording -- naming the same whole, total or population, not a broader,
  narrower or differently named one? For example, "the annual household
  budget" and "the household's yearly budget" name the same whole; "the
  total budget" and "the monthly budget" do not.
Then score: an integer 0-100 for overall equivalence of meaning and
evidential strength.

Respond with ONLY a JSON object in exactly this format, nothing else:
{{"all_details": true, "nothing_added": true, "values_unchanged": true, "scope_kept": true, "score": 100}}"""

RUBRIC_FLAGS = ("all_details", "nothing_added", "values_unchanged", "scope_kept")
RATER_SYSTEM = "You are a strict, literal semantic-equivalence rater."
REPORTER_SYSTEM = "You are relaying information you found, faithfully and concisely."

_STOP = set("""a an the of for from by to in on at with and or is are was were
this that these those it its his her their your our who which what when where
into via per as be been has have had not no yes""".split())


def _words(text: str) -> set[str]:
    """Lowercased content words, possessive/quote stripped, crude singular."""
    out = set()
    for w in re.findall(r"[a-z][a-z'-]{3,}", text.lower()):
        w = w.replace("'s", "").strip("'-")
        if w.endswith("ies"):
            w = w[:-3] + "y"
        elif w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if len(w) >= 4 and w not in _STOP:
            out.add(w)
    return out


def word_ngram_jaccard(a: str, b: str, n: int = 2) -> float:
    """Lexical overlap: Jaccard similarity of word n-grams."""
    def ngrams(text: str) -> set:
        words = text.lower().split()
        if len(words) < n:
            return {tuple(words)}
        return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}
    ga, gb = ngrams(a), ngrams(b)
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


def leak_terms(source: dict, question: str) -> set[str]:
    """Words of provenance["type"] that appear in neither the content nor the question:
    banned from this source's reports. The one implementation; lint imports it.

    The reporter never sees provenance, so this guards against it INVENTING a correct
    attribution. `why` and the labels are shown to nothing, so they are not policed;
    doing so only rejects good paraphrases (R2a)."""
    return _words(source["provenance"]["type"]) - _words(source["content"]) - _words(question)


def leaks_in(candidate: str, terms: set[str]) -> list[str]:
    return sorted(terms & _words(candidate))


# Paired with leak_terms: invented sourcing, whatever its wording. Phrases only -- a
# bare "official" or "record" is a legitimate paraphrase word.
ATTRIBUTION_PHRASES = [
    r"\baccording to\b", r"\b(reportedly|allegedly)\b",
    r"\b(the|this|a|an) (page|document|source|table|brief|announcement|notice|wiki|"
    r"schedule|timetable|post|email|message|site|website|listing|sheet|manual) "
    r"(says|said|states|stated|lists|listed|shows|showed|notes|noted)\b",
    r"\b(i|we) (read|was told|were told|heard)\b",
]


def attribution_in(candidate: str) -> list[str]:
    return [m.group(0) for p in ATTRIBUTION_PHRASES
            for m in [re.search(p, candidate, re.I)] if m]


def rate(source_text: str, candidate: str, rater) -> dict:
    """{flag: bool, ..., "score": 0-1, "ok": bool, "failed": [...], "raw": str}.
    Any false flag, or a reply that is not the four booleans, rejects -- an unparseable
    rating never passes a candidate by default."""
    raw = rater.complete(system=RATER_SYSTEM,
                         user=RUBRIC_PROMPT.format(source_text=source_text,
                                                   candidate_text=candidate),
                         temperature=0.0, max_tokens=80)
    try:
        obj = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
    except (AttributeError, ValueError):
        obj = {}
    flags = {f: obj.get(f) for f in RUBRIC_FLAGS}
    failed = [f for f, v in flags.items() if v is not True]
    score = obj.get("score")
    score = max(0, min(100, score)) / 100.0 if isinstance(score, (int, float)) \
        and not isinstance(score, bool) else 0.0
    return dict(flags, score=score, ok=not failed, failed=failed, raw=raw)


def _select_diverse(eligible: list[dict], source_text: str, n_needed: int,
                    avoid: list[str] = ()) -> list[dict]:
    """Highest score first; ties go to the candidate with the LOWEST maximum bigram
    overlap against the source and everything already accepted. Measuring against the
    source matters for the first pick: with nothing accepted yet every candidate would
    tie, and generation order would freeze the least reworded one."""
    accepted, pool = [], eligible[:]
    while pool and len(accepted) < n_needed:
        ref = [source_text] + list(avoid) + [a["text"] for a in accepted]
        pool.sort(key=lambda s: (-s["semantic"],
                                 max(word_ngram_jaccard(s["text"], t) for t in ref)))
        cand = pool.pop(0)
        if all(word_ngram_jaccard(cand["text"], a["text"]) <= PAIR_MAX for a in accepted):
            accepted.append(cand)
    return accepted


def select(candidates: list[str], source: dict, n_needed: int, rater,
           question: str = "", avoid: list[str] = (), check_length: bool = True) -> dict:
    """Rate every candidate, then pick `n_needed` that pass every criterion and are
    pairwise distinct. `avoid` holds the accepted reports of sources that can share a
    trial with this one (R17 backstop). `check_length` is off only for a mock's padded
    rewordings, whose length is not a reporter's. Every candidate carries `accepted` and
    `rejected_because`, so the acceptance rate can be reported.
    Returns {"accepted": [...], "all_scored": [...], "sufficient": bool}."""
    terms = leak_terms(source, question)
    source_text = source["content"]       # what the reporter saw, so what it is held to
    scored = []
    for c in candidates:
        rubric = rate(source_text, c, rater)
        s = {"text": c, "semantic": rubric["score"],
             "copy_overlap": word_ngram_jaccard(c, source_text),
             "leak": leaks_in(c, terms) + attribution_in(c), "rubric": rubric,
             "cross_overlap": max((word_ngram_jaccard(c, t) for t in avoid), default=0.0),
             "length_diff": len(c.split()) - len(source_text.split())}
        why = []
        if not rubric["ok"]:
            why.append(f"rubric false: {rubric['failed']}")
        if s["semantic"] < SEMANTIC_MIN:
            why.append(f"semantic {s['semantic']:.2f} < {SEMANTIC_MIN}")
        if s["copy_overlap"] > COPY_MAX:
            why.append(f"copy overlap {s['copy_overlap']:.2f} > {COPY_MAX}")
        if s["leak"]:
            why.append(f"leak {s['leak']}")
        if s["cross_overlap"] > CROSS_MAX:
            why.append(f"cross-source overlap {s['cross_overlap']:.2f} > {CROSS_MAX}")
        if check_length and abs(s["length_diff"]) > LENGTH_DIFF_MAX:
            why.append(f"length {s['length_diff']:+d} words > {LENGTH_DIFF_MAX} from the source")
        s["rejected_because"] = why
        scored.append(s)

    eligible = [s for s in scored if not s["rejected_because"]]
    accepted = _select_diverse(eligible, source_text, n_needed, avoid)
    for s in scored:
        s["accepted"] = any(s is a for a in accepted)
        if not s["rejected_because"] and not s["accepted"]:
            clash = max((word_ngram_jaccard(s["text"], a["text"]) for a in accepted),
                        default=0.0)
            s["rejected_because"] = [f"pairwise overlap {clash:.2f} > {PAIR_MAX}"
                                     if clash > PAIR_MAX
                                     else "eligible but not needed (quota filled first)"]
    return {"accepted": accepted, "all_scored": scored,
            "sufficient": len(accepted) >= n_needed}


def generate_candidates(source: dict, question: str, reporter,
                        n: int = CANDIDATES_PER_ROUND, temperature: float = 0.9,
                        prior: list[str] | None = None,
                        forbidden: set[str] | None = None) -> list[str]:
    out = []
    for _ in range(n):
        seen = list(prior or []) + out
        avoid_block = AVOID_BLOCK.format(
            prior="\n".join(f"- {t}" for t in seen)) if seen else ""
        forbid_block = (FORBID_BLOCK.format(words=", ".join(sorted(forbidden)))
                        if forbidden else "")
        prompt = REPORTER_PROMPT.format(source_content=source["content"], question=question,
                                        avoid_block=avoid_block, forbid_block=forbid_block)
        text = reporter.complete(system=REPORTER_SYSTEM, user=prompt,
                                 temperature=temperature, max_tokens=120)
        out.append(text.strip())
    return out


def generate_and_freeze(source: dict, question: str, n_needed: int, reporter, rater,
                        max_rounds: int = MAX_ROUNDS,
                        n_per_round: int = CANDIDATES_PER_ROUND,
                        avoid: list[str] = (), check_length: bool = True) -> dict:
    """Generate -> rate -> select, regenerating if short.

    A round is a generation batch plus a full re-selection over EVERY candidate so far,
    so round 2 re-rates round 1's candidates and any of them can still be chosen. Round 2
    also raises the temperature slightly, shows the reporter the earlier wordings, and
    forbids the words that caused leak rejections.

    Calls per source: 12 if round 1 suffices (6 generations + 6 ratings), 30 if round 2
    runs (6 more generations + 12 ratings over the pooled set). Still short after
    max_rounds sets `warning`; the caller treats that as a stop."""
    all_candidates: list[str] = []
    leaked: set[str] = set()
    calls = 0
    for round_i in range(max_rounds):
        batch = generate_candidates(source, question, reporter, n=n_per_round,
                                    temperature=0.9 + 0.05 * round_i,
                                    prior=all_candidates, forbidden=leaked)
        all_candidates.extend(batch)
        result = select(all_candidates, source, n_needed, rater, question=question,
                        avoid=avoid, check_length=check_length)
        calls += len(batch) + len(all_candidates)
        result.update(rounds_needed=round_i + 1, calls=calls)
        if result["sufficient"]:
            return result
        leaked |= {w for s in result["all_scored"] for w in s["leak"]}
    result["warning"] = (f"Only {len(result['accepted'])}/{n_needed} candidates passed "
                         f"after {max_rounds} generation rounds.")
    return result


def co_occurring_accepted(frozen_case: dict, source_key: str) -> list[str]:
    """Accepted reports, so far, of the sources that can share a trial with
    `source_key` -- what the R17 backstop checks against."""
    partners = {b if a == source_key else a for a, b in CO_OCCURRING_PAIRS
                if source_key in (a, b)}
    return [x["text"] for k in sorted(partners & set(frozen_case))
            for x in frozen_case[k]["accepted"]]


def freeze_order(case: dict) -> list[str]:
    """R18: descending by reports needed (B, then A, then C and D), ties alphabetical.
    The first source frozen has the freest choice under the cross-source backstop, so it
    goes to the one under the tightest constraint."""
    return sorted(case["sources"], key=lambda k: (-case["sources"][k]["n_paraphrases_needed"], k))


def freeze_sources(cases: dict, reporter, rater):
    """Yield (case_id, source_key, result) for every source, case by case in R18 order.
    The caller collects the results and decides when to stop."""
    for case_id, case in cases.items():
        frozen_case = {}
        for key in freeze_order(case):
            src = case["sources"][key]
            pads = getattr(reporter, "pads", None)     # only the mock has it
            padded = bool(pads and pads(src["content"]))
            result = generate_and_freeze(src, case["question"], src["n_paraphrases_needed"],
                                         reporter, rater,
                                         avoid=co_occurring_accepted(frozen_case, key),
                                         check_length=not padded)
            if padded:
                result["padded"] = True
            frozen_case[key] = result
            yield case_id, key, result
