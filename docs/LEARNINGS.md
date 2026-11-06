# Gradient Path — Learnings

_Last verified: 2026-09-21 · against: working tree (HEAD 57245e8 + uncommitted docs)_

Reflection log. Only genuinely generalizable lessons (self-check: "would this help a different future task, or is it one-off?"). A lesson seen a **second time gets promoted to RULES.md**, with the promotion logged in DECISIONS.md.

---

## [impact: high] Selector-gated solver lists fail silently for new zones

When every entry in a config list carries a selector, a domain matching nothing gets **no fallback at all** — the system errors at a stage before the visible one (no Challenge object; the Certificate just sits False). Applies to any selector-gated registry (cert-manager solvers, CI runner filters, webhook routes). Lesson: when adding a new value to a namespaced domain, check the config for selector-gated entries *first*. Source: 2026-08-28 TLS outage.

## [impact: high] Bundled tool binaries don't inherit upstream default behaviour

k3s's kubectl ignores `~/.kube/config` because it's a symlink to the k3s binary with a hardcoded default. "It works on standard kubectl" is not evidence it works here. Lesson: for any platform that ships a wrapped/aliased CLI, verify the config-resolution order explicitly before assuming defaults. Source: deploy workflow fix, 2026-08-28.

## [impact: high] Ephemeral pipelines die at the worst time

The generator pipeline was rebuilt from scratch twice before being committed to the repo. Lesson: anything needed to produce the shipped artifact belongs in version control, with its schema documented, even if the artifact itself is what gets deployed. Source: `generator/gpkit/README.md`.

## [impact: med] Valid-looking TeX can hide prose corruption

A stray `$` pairs with the next one on the line and silently renders the prose between them as math — often valid TeX, so nothing crashes. Lesson: when a build step pairs delimiters, validate semantic content (the validator's "span reads like a sentence" heuristic), not just syntax. Source: `generator/check.py` `math_smells_like_prose()`.

## [impact: med] Character-level entity bugs resist sed

`&mdash\;` can't be fixed by `sed 's/\;/;/g'` because BRE reads `\;` as `;`, and a blanket replace would eat LaTeX's `\;` thin space. Lesson: repairs that need context-awareness belong in a real script with a targeted regex. Source: `generator/assemble.py`.

## [impact: med] "Wrong in a past session" lists are worth their weight

SESSION-CONTEXT.md's Corrections section (six inherited assumptions that failed) prevented the same failures from repeating. Lesson: when inherited facts fail verification, record the *claim and why it was wrong*, not just the correct answer. Promotion candidate: RULES.md already carries the grounding rule; keep logging specific corrections in DECISIONS.md.

## [impact: low] Accessibility bugs cluster at build time

3,195 aria-hidden math spans trace to one line in `render_math.js` choosing HTML-only KaTeX output. Lesson: a single build-config choice can create corpus-wide defects; fix the generator, not the artifacts — and add a regression check so it can't silently return.

## [impact: med] A numbering gap is usually a naming-scheme boundary, not a missing thing

"Modules go 01, 03, 04 — where is 02?" looked like a lost module for three weeks. Module 02 existed the whole time under a topic filename, because the numeric prefix was only ever applied to *generated* pages and this one is hand-maintained. The gap marked the edge of a convention, not an absence. Lesson: before filing a gap in a sequence as missing work, check whether the sequence is produced by one process and the gap by another — enumerate by the *registry* (here `index.html`'s `MODULES` array) rather than by filenames on disk. Corollary that paid off immediately: the registry also confirmed the 217-card headline figure by summing to it, which the filenames could not have. Source: 2026-09-21 documentation audit, TASKS.md #2.

## [impact: med] Copied design tokens drift silently; only an importer or a check prevents it

The fifteen palette tokens are declared three times — `index.html`, `generator/gpkit/page.css`, `blind75nightlyreview.html` — by copy, with no import and no assertion that they agree. Nothing fails when one is edited alone; the pages simply stop matching, and only on a page nobody happened to open. Lesson: whenever a value is duplicated across artefacts that are built by different processes, either make one the importable source or write the equality check at the same time as the second copy. The second copy is the moment the check becomes necessary, not the moment drift is noticed. Source: DESIGN.md token audit, TASKS.md #20.

## [impact: high] A generator is only the source of truth if its output still matches what is committed

`build_index.py` rebuilds `index.html` from `templates/index-base.html`, and the docs (TASKS.md #21) say to edit the template, not the hub. But the 2026-09-07 audit corrections were applied to `index.html` only, so a routine rebuild on 2026-10-30 silently deleted ~30 committed lines; it was caught only because `git diff --stat` ran straight after. Lesson: before trusting any "edit the source, rebuild the artifact" rule, rebuild once and diff against the committed artifact; a non-empty diff you did not intend means the source has drifted and the rule is currently false. This is the second instance of the copy-drift pattern above (tokens, then templates), so it is a promotion candidate for RULES.md. Source: TASKS.md #27.

## [impact: high] Re-read the handoff after any long step when another session shares the checkout

On 2026-10-30 a second session committed and pushed twice while this one worked, updating MEMORY.md with "Do not run `build_index.py`". This session had read MEMORY.md at start, ran `build_index.py` anyway, and reverted 30 committed lines (restored). The same session also committed this session's untracked `docs/practice-brief.md` before its owner had confirmed it. Lesson: a handoff file is a snapshot. Before any step that rewrites a generated artefact or touches git, re-run `git log --oneline -3` and re-read MEMORY.md. A HEAD that moved since session start means someone else is writing. Source: TASKS.md #23, #25, #27.

## [impact: med] A claim-word regex finds unsourced claims, not wrong ones

The grounding sweep over 116 glossary drafts (`most|usually|often|\d…`) flagged entries that needed sources, but every one of the 5 maths errors had no claim word in it ("Bonferroni treats them as independent", "Whitening inverts it"). Only the isolated reviewer subagent found them. Lesson: a mechanical sweep and a domain review answer different questions, so run both on general-knowledge drafts. Source: TASKS.md #24 evidence.

## 2026-10-30 — External model reviews need the same scope check as your own content

Two AI reviews of the AIF-C01 page were applied. Gemini's "missing" list was half out of scope: 11 of its services and concepts appear nowhere in the v1.2 domain pages or in-scope list, apparently carried over from the older guide and from third-party prep material. One of its accuracy claims (b48) was simply wrong. GPT's narrower list was correct. In the other direction, the independent fact-check caught a fact that had gone stale in the last three months (DynamoDB vector search), which turned a "clearly wrong" distractor into a second right answer. Lesson: triage every review claim against the fetched primary source before editing, and re-check distractors as well as keys, because a service launch can silently make a wrong option right. First occurrence.

## [impact: medium] A hidden preview pane freezes the page, so it cannot judge motion

In a hidden browser pane `requestAnimationFrame` and IntersectionObserver stall while timers and scripts keep going, so a healthy page looks stuck or half drawn, and a script-only check still passes. Before calling something a motion or scroll bug, test `requestAnimationFrame`; then verify in a browser that renders, such as headless Chrome through Playwright, and sample `document.getAnimations()` rather than trusting screenshot timing. That sampling is what exposed the Replay bug (#38).
