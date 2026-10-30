# Glossary source — work in progress (paused 2026-10-30)

116 hand-written entries covering the **107 terms that 2+ cards name but no card teaches**.
Each entry: a one-line meaning and a one-line "when it comes up", in the eli5 register.

- `terms.json` — the merged, link-resolved data. **This is the deliverable.** Each entry:
  `{s: section, t: term, m: meaning, w: when it comes up, n: how many cards name it, cards: [[title, href#anchor, modnum], ...]}`
- `gloss_a..d.py` — the editable sources (stats / linalg / ml / retrieval+serving+quant).
- `_vocab-raw.json` — all 241 cards with their chips, as parsed from the built pages + mod07/08 sources.
- `_vocab-uncovered.json` — the uncovered-term counts the scope decision was based on.

**Build:** `python3 generator/glossary/build_glossary.py` writes `glossary.html` to the repo root from
`terms.json` (the pre-review draft, left untouched) plus `review.py` (grounding-rule overrides and sources,
TASKS.md #24) and `glossary.tpl.html`. It refuses on an unresolved card anchor, a repeated review key,
or palette drift from `index.html`. Edit `review.py`, never the built page.

This directory is under `generator/` on purpose — `Dockerfile`'s `COPY *.html` matches the
repo ROOT only, so nothing here is published until a built page is moved to the root.

## Scope decision (do not silently widen it)
979 terms are genuinely uncovered; 872 of those are named by exactly one card and are
incidental. Only the 107 named by 2+ cards were written. Mass-generating the rest would put
~1,700 unreviewed technical claims on a site whose own rule (docs/RULES.md, The Grounding Rule)
is that every factual claim needs a source.

## Grounding review (done 2026-10-30, TASKS.md #24)
Hybrid policy (DECISIONS.md): definitions stay uncited; anything asserting a number, comparison,
frequency or named-system behaviour carries a source in `review.py` (51 of 116) or was reworded.
`terms.json` still holds the unreviewed draft wording. Do not build from it without `review.py`.
