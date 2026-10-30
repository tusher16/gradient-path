# Gradient Path — Rules & Conventions

_Last verified: 2026-10-30 · against: working tree (HEAD 57245e8 + uncommitted docs)_

## Code Conventions

### General
- Python 3.11+ for generator scripts. **Fact** — `generator/check.py` shebang.
- No `node_modules` or build artifacts committed in `generator/` — `.gitignore` excludes them.
- All HTML output must be well-formed XML where figures are concerned — `ET.parse` in `check.py` validates SVG.

### Content (Cards)
- British spelling: `generalise`, `behaviour`, `modelling`. **Fact** — `generator/BRIEF.md`.
- `&mdash;` for em dashes, `&rsquo;` for apostrophes in prose, `&amp;` for every ampersand.
- Never the word "delve". Never open a paragraph with "In essence" or "it is important to note".
- Confidence without hedging. Name the thing that is actually hard.
- Second person, direct.
- `&#36;` for currency symbols — bare `$` pairs with the next one and KaTeX renders the prose between as math. **Fact** — `generator/check.py` `math_smells_like_prose()`.

### HTML / CSS
- CSS custom properties for theming; never hard-code colours outside `:root`.
- Dark mode via `prefers-color-scheme: dark` AND `data-theme="dark"` override.
- `prefers-reduced-motion: reduce` must disable transitions. **Fact** — `index.html` media query.
- All fonts loaded via `preconnect` to `fonts.googleapis.com` and `fonts.gstatic.com`. **Fact** — `index.html`.

## Git Workflow

- `main` is the only branch. No feature branches — this is a personal project.
- Every push triggers the deploy workflow. The workflow builds a new image and rolls it out.
- Generated HTML files (01-*.html, 03-*.html, etc.) are committed. They are the deployable artifact. **Fact** — `generator/gpkit/README.md`: "The HTML in the repo *is* the generated output."
- `DEPLOY-RUNBOOK.md` and `SESSION-CONTEXT.md` are **never committed** — they contain LAN IPs, SSH port, and usernames. **Fact** — `.gitignore`.
- Commit messages: plain English, present tense. Example: "fix(cards): qualify PCA claim by solver".

## The Grounding Rule

Every factual claim in content must be anchored to a source, a checked date, or a specific real system with a number. "Used in ML applications" is rejected by the validator. "Netflix reduced buffer events by 43% using this approach" is accepted. If you cannot verify the number, cut the claim. **Fact** — `generator/SCHEMA.md` hard rule #6.

## Secrets Screening (before committing any doc)

The repo is **public**. Before a new or changed file under `docs/` — or any Markdown at the repo root — is committed, ask whether it contains: LAN IPs, hostnames, non-standard ports, usernames, cluster paths, kubeconfig or token material, or anything about a real person.

- **If yes** — keep the file, add it to `.gitignore` **by explicit filename**, and record the exclusion and its reason in `DECISIONS.md`. Never exclude `docs/` wholesale: that hides the product docs too. **Fact** — this is why `.gitignore` names `docs/2026-08-28-gradientpath-tls-dns.md` individually rather than the directory (DECISIONS.md, 2026-09-20).
- **If no** — it is committable.
- Either way, state the verdict per file in the run's report. A doc that has never been screened is not committable, however harmless it looks.
- Secret-bearing docs may be *referenced by filename* from committed docs (as SECURITY.md does) but their contents are never quoted into a committed file.

## Build Safety

1. Run `python3 generator/check.py <module>` before any build. Errors refuse the build.
2. Run `python3 generator/checkfile.py <file>` for single-file validation.
3. Only after zero errors, run the full pipeline: assemble → katexify → build_index.
4. Verify the built page in browser (both Simple and Technical mode, dark and light theme).
5. `git diff --stat` the HTML. A 2 MB diff is expected for a full module; a 200 KB diff on an unchanged module is a bug.

## Publishing Boundary

**Any `.html` file in the repo root is published to gradientpath.site.** `Dockerfile` line 9 is `COPY *.html /usr/share/nginx/html/` — a root-level glob with no recursion and no allowlist, so a file is live the moment it lands in the root and the next deploy runs, linked or not. **Fact** — `Dockerfile:9`; `generator/templates/index-base.html` is the existing proof that subdirectory HTML stays private.

- Learner-facing pages go in the root. Today: the six module pages, `index.html`, `roadmap.html`, `chips-and-gaps.html`.
- Everything else — experiments, scratch renders, drafts — goes in a subdirectory.
- **A page moved into the root is being published.** Strip `noindex`, add a meta description, and re-read the copy as a visitor before moving it: a page written for the maintainer reads as a leak when a stranger finds it.
- Do not put a draft in the root "just to look at it". Open it from a subdirectory or serve it locally.

## Content Editing Boundary

- **Do not hand-edit** `01-linear-algebra.html`, `03-machine-learning.html`, `04-llms.html`, `05-statistics.html`, or `06-system-design.html`. These are generator output. Edit the source Python files in `generator/content/` and rebuild. **Fact** — `generator/gpkit/README.md`.
- `index.html` is hand-edited. It is the hub and is rebuilt by `build_index.py` from module metadata, but the template in `generator/templates/index-base.html` is the source of truth for structure.
- `blind75nightlyreview.html` (Module 02) **is hand-edited** — it is not generator output, so edit the HTML directly and do not attempt to rebuild it through the pipeline. Resolved 2026-09-21 (was Unknown; TASKS.md #2). Evidence and marker counts: `ARCHITECTURE.md` → Open Architecture Questions #3.
  - It re-uses the palette by **copy**, not by import: its `:root` block duplicates the tokens in `index.html`. A token change in `DESIGN.md` must be applied to this file by hand or the two pages drift.
