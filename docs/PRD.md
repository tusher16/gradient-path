# Gradient Path — Product Requirements Document

_Last verified: 2026-09-21 · against: working tree (HEAD 57245e8 + uncommitted docs)_

## Overview

Gradient Path is a static, self-contained HTML study site for AI/ML engineering interview preparation. Each "card" is a bite-sized concept (meant to be read in ~10 minutes before bed) that encodes the *follow-up question*, not the definition — what the interviewer asks next, the wrong sentence candidates say, and the decision to make with the numbers in front of you.

**Fact** — `generator/BRIEF.md`: "Each card is meant to be read in ten minutes before bed and to survive contact with a real interview the next morning."
**Fact** — `docs/learning-audit-2026-09-07.md`: 217 cards/patterns across six modules; 597 revealable drill questions.

## Problem

Interview prep for AI/ML engineering is either too shallow (Wikipedia first-paragraph summaries) or too dense (textbooks with no guidance on what the interviewer actually asks). Candidates waste time memorising definitions instead of practising the specific wrong claims, follow-up questions, and numerical trade-offs that interviews test.

## Goals

1. **Encode the follow-up, not the definition.** Every card carries the trap sentence, the drill question, and the real system failure with a number.
2. **Two-mode accessibility.** A "Simple" layer with zero notation stands alone for readers outside the field; a "Technical" layer carries full math, code, and interview-grade answers. **Fact** — `generator/SCHEMA.md`: "The simple layer contains no math notation at all."
3. **Local-first, zero-backend operation.** No accounts, no server-side state, no tracking. Progress lives in `localStorage` only. **Fact** — `SESSION-CONTEXT.md`: "Every page stores theme/mode/progress in `localStorage`."
4. **Portable delivery.** Single static container, any static host, no build step at deploy time.

## Users

- **Primary**: AI/ML engineers preparing for technical interviews.
- **Secondary**: Data engineers crossing into ML; researchers brushing up on production constraints.
- **Tertiary**: Hiring managers reviewing what candidates are expected to know.

## MVP Scope

| Feature | Status | Evidence |
|---|---|---|
| Six content modules (Linear Algebra, ML, LLMs, Statistics, System Design, Blind 75) | ✅ Shipped | `index.html` module grid; `docs/learning-audit-2026-09-07.md` table |
| Two-layer content (Simple / Technical) | ✅ Shipped | `generator/gpkit/build.py` two-layer contract; `generator/SCHEMA.md` hard rule #1 |
| Per-card drills (3 per card) | ✅ Shipped | `generator/SCHEMA.md`: "exactly 3 drills, each with q, a and a_simple" |
| Progress picker (New / Fuzzy / Solid) | ✅ Shipped | `index.html` `.mark` classes; `generator/gpkit/page.js` |
| Dark / light mode | ✅ Shipped | `index.html` `prefers-color-scheme` + `data-theme` CSS |
| Static Docker image, K3s deploy | ✅ Shipped | `Dockerfile`, `k8s/deployment.yaml`, `.github/workflows/deploy.yml` |
| TLS via cert-manager + Cloudflare DNS-01 | ✅ Shipped | `k8s/ingress.yaml`, `k8s/cluster-issuer.yaml`; `docs/2026-08-28-gradientpath-tls-dns.md` |
| Card authoring pipeline with validator | ✅ Shipped | `generator/check.py`, `generator/assemble.py` |

## Out of Scope

- Account-based sync or server-side state. `localStorage` is intentional; cross-device sync is a future "Next" item per `docs/learning-audit-2026-09-07.md`.
- Real-time AI tutor in the page. The tutor prompts exist in `generator/gpkit/prompts.py` and `docs/curriculum-prompts.md`, but the site does not host a conversational agent.
- Video or animated interactive figures. Static SVG figures are in scope; interactive drag/vector/gradient-descent demos are "Next" items.
- Mobile app or PWA wrapper.
- User-generated content or community contributions.

## Success Metrics

| Metric | Target | How Measured |
|---|---|---|
| Page weight (gzipped) | < 500 KB per module page | `curl -s -H 'Accept-Encoding: gzip' ...` per `DEPLOY-RUNBOOK.md` |
| Build reproducibility | Byte-identical output given same cards | SHA-256 of generated HTML; generator pipeline is deterministic |
| Validator pass rate | 100% before any build commit | `python3 generator/check.py <module>` must exit 0 |
| Availability | 99% uptime on home cluster | K3s readiness probe on `/healthz`; `kubectl get pods` |
| Content coverage | 250+ cards across 7+ modules | Audit in `docs/learning-audit-2026-09-07.md` |
| Accessibility (Math) | MathML present for all KaTeX output | **Not met, and now precisely located**: `generator/render_math.js:10` passes `output: 'html'`, so zero MathML is emitted. Resolving change and its acceptance criterion: TASKS.md #6 |
