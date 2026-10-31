# Gradient Path

_Last verified: 2026-09-21 · against: working tree (HEAD 57245e8 + uncommitted docs)_

Free, no-signup study site for AI/ML engineering interviews at gradientpath.site — 217 static, self-contained HTML cards across six modules, each encoding the follow-up question the interviewer asks next, the specific wrong sentence candidates say, and a real production failure with numbers. Every card has a Simple mode (zero notation, stands alone) and a Technical mode (interview-grade). Local-first: progress lives in the visitor's localStorage; no backend, no accounts, no tracking.

## Stack

- Static HTML/CSS/JS — no framework, no build step at deploy time; module pages are **generated artifacts**, produced by the Python pipeline in `generator/` (validate → assemble → katexify → index)
- KaTeX pre-rendered at build time; inline SVG figures via `generator/gpkit/figkit.py`
- nginx:1.27-alpine Docker image → ghcr.io/tusher16/gradient-path → K3s (namespace `apps`, Traefik ingress, cert-manager DNS-01 TLS)
- CI: GitHub Actions on push to main — image build + SSH rollout to the homelab node. **A push to main is a production deploy.**

## Universal rules

- After every command or tool call, state the observed result before deciding the next step.
- Generated module pages (`01-`, `03-`, `04-`, `05-`, `06-*.html`) are never hand-edited — edit sources in `generator/content/` and rebuild. `blind75nightlyreview.html` (module 02) is the exception: it is hand-maintained, so edit it directly.
- Check new UI work against docs/DESIGN.md's anti-patterns before considering it done.
- Every factual content claim needs a source or a real system with a number — "used in many companies" is rejected by the validator.
- `DEPLOY-RUNBOOK.md`, `SESSION-CONTEXT.md`, and `docs/2026-08-28-gradientpath-tls-dns.md` are gitignored on purpose (public repo, operator secrets inside) — never commit them or quote their contents into committed files.
- Read-only/inspect tools are auto-approved; anything that pushes, applies to the cluster, deletes, or publishes requires explicit confirmation (full tiers in docs/TOOLS.md).

## Session start

Read docs/MEMORY.md for handoff state (active tasks, blocker, next action).

## Before marking any task Done

Run the review gate at the top of docs/TASKS.md: re-check the diff against the task's acceptance criteria, docs/RULES.md, and docs/TEST_PLAN.md; if UI was touched, against docs/DESIGN.md anti-patterns. Record the verdict as the task's Verification evidence. A task authored and reviewed by the identical unexamined pass is not verified.

## After finishing a task

Follow the reflect-and-promote step in docs/LEARNINGS.md — log any generalizable lesson there; on its second occurrence, promote it to RULES.md and log the promotion in docs/DECISIONS.md.

## Reference on demand

- docs/PRD.md — task changes requirements or scope
- docs/ARCHITECTURE.md — task touches structure, pipeline, or adds modules
- docs/RULES.md — full conventions, build safety, content voice
- docs/DESIGN.md — task touches UI (anti-patterns list lives here)
- docs/SECURITY.md — task touches secrets, cluster access, data handling
- docs/TOOLS.md — before calling any tool tier above "auto-approved"
- docs/TEST_PLAN.md — task implements or validates behavior
- docs/TASKS.md — find/update task status, criteria, evidence
- docs/DECISIONS.md — log decisions with real trade-offs
- docs/LEARNINGS.md — check before a task resembling a past correction
- docs/MARKETING.md — task touches positioning, launch, or growth
- docs/SEO.md — task touches meta tags, sitemap, structured data, agent discoverability
- generator/SCHEMA.md — writing or editing card content
- generator/BRIEF.md — content voice and quality bar

## Commands

Verified 2026-09-21 on Python 3.14.2, Docker 29.7.2, node v22.21.0, npm 10.9.4.

```bash
# Validate card sources (run before every build; errors refuse the build).
# Works from the repo root — no cd needed. Observed on 2026-09-21:
python3 generator/check.py mod05   # → 40 cards | 0 errors | 0 warnings  (exit 0)
python3 generator/check.py mod06   # → 22 cards | 0 errors | 0 warnings  (exit 0)
python3 generator/check.py mod07   # →  1 cards | 0 errors | 0 warnings  (exit 0)
python3 generator/check.py mod08   # → 23 cards | 0 errors | 0 warnings  (exit 0)
# One expected SyntaxWarning on 3.14 (check.py:9 docstring) — TASKS.md #18.
# Any OTHER warning is a real signal.

# Rebuild one module: assemble → katexify → rebuild hub
cd generator
python3 assemble.py content/mod05 mod05.py 05-statistics.html
python3 katexify.py 05-statistics.html
python3 build_index.py
# mod07 has a CFG (generator/mod07.py); mod08 does NOT — TASKS.md #7.
# WARNING 2026-10-30: build_index.py currently DELETES committed audit content
# from index.html (template drift) — do not run it until TASKS.md #27 is done.

# Rebuild the AWS AI Practitioner page (validates, then writes the root HTML)
node generator/cert/aif-c01/build.js   # → 30 topics | motion 24 | practice 57 | Mock A 13/16/18/9/9 | Mock B 13/16/18/9/9

# Local serve check (post-deploy verification set in docs/TEST_PLAN.md)
docker build -t gradient-path . && docker run -p 8080:80 gradient-path
curl -s http://localhost:8080/healthz   # expect: ok
# NOT run in this session — it builds and runs a container. Unverified.

# Deploy = git push to main (builds image, rolls out via SSH). Confirm first.
# Never run end-to-end successfully — TASKS.md #1.
```

There is **no test suite and no lint step**; `check.py` is the only automated gate. See docs/TEST_PLAN.md § Reality Check.
