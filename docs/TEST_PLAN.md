# Gradient Path — Test Plan

_Last verified: 2026-09-21 · against: working tree (HEAD 57245e8 + uncommitted docs)_

## Reality Check

**Fact**: this project has no automated test suite. There is no pytest config, no CI test job, no test directory for the site itself. Verification today is a mix of a schema validator (`generator/check.py`), bash spot-checks documented in `DEPLOY-RUNBOOK.md`, and manual browser verification. This document records what exists and what each change type must run. Building real automated coverage is task #17 candidate (see TASKS.md).

## Test Levels

### 1. Schema validation (unit-equivalent) — run before every build

```bash
cd generator
python3 check.py mod05        # validate a module's cards pre-build
python3 checkfile.py content/mod05/<file>.py   # single file
```

**Covers**: required fields, kebab-case unique ids, tier vocabulary, exactly 3 drills, bolded verdicts, no math notation in the simple layer, balanced `$`, `&mdash\;` entity bug, bare `&`, well-formed figure XML, `real` carries a number.

**Pass**: exits 0 with zero errors. Warnings need a reason to ignore.

**Observed 2026-09-21** (Python 3.14.2, from the repo root — the path form in `AGENTS.md` works without `cd generator`):

```
python3 generator/check.py mod05  →  40 cards  |  0 errors  |  0 warnings   (exit 0)
python3 generator/check.py mod06  →  22 cards  |  0 errors  |  0 warnings   (exit 0)
python3 generator/check.py mod07  →   1 cards  |  0 errors  |  0 warnings   (exit 0)
python3 generator/check.py mod08  →  23 cards  |  0 errors  |  0 warnings   (exit 0)
```

Card counts agree with `ARCHITECTURE.md` → Module Inventory.

**Interpreter warning (not a validator failure).** On Python 3.14.2 every run emits, before its output:

```
generator/check.py:9: SyntaxWarning: "\;" is an invalid escape sequence.
Such sequences will not work in the future.
```

The sequence is inside `check.py`'s own module docstring, where it documents the `&mdash\;` entity bug. It is cosmetic today and a `SyntaxError` on a future interpreter. Tracked as TASKS.md #18. Treat a *new* warning from this command as a real signal — this is the only one currently expected.

### 2. Build determinism (integration-equivalent)

```bash
python3 assemble.py content/mod05 mod05.py 05-statistics.html
python3 katexify.py 05-statistics.html
python3 build_index.py
git diff --stat
```

**Pass**: on unchanged inputs, `git diff` shows no change to built HTML (byte-identical rebuild). A hard-coded count disagreeing with `len(cards)` stops the build — this has shipped before.

### 3. Manual browser verification (e2e-equivalent, currently the only UI check)

Per changed module, check in a real browser:

- [ ] Technical mode: math renders, code blocks render, drills reveal
- [ ] Simple mode: **zero** rendered math reachable (audit verified 0 for 01/03/04 — keep it that way)
- [ ] Dark and light themes (both `prefers-color-scheme` and the manual toggle)
- [ ] Figures render at 390px phone width without breaking layout
- [ ] Progress marks (New/Fuzzy/Solid) persist across reload (localStorage)
- [ ] Module appears on hub with correct card count

### 4. Deployment checks (from DEPLOY-RUNBOOK.md — tested against a real nginx, not assumed)

```bash
# after deploy, or via port-forward locally:
kubectl port-forward -n apps svc/gradient-path 8080:80
curl -s http://localhost:8080/healthz                 # expect: ok
curl -sI http://localhost:8080/ | head -1             # expect: 200
curl -s -H 'Accept-Encoding: gzip' -o /dev/null -w '%{size_download}\n' \
  http://localhost:8080/04-llms.html                  # expect: far below 2.2MB
curl -sI http://localhost:8080/nonexistent            # expect: 404
```

**Also verified working (Fact, DEPLOY-RUNBOOK.md)**: ETag + Last-Modified produce 304s on repeat visits.

### 5. CI (deploy pipeline — the only automated gate today)

`.github/workflows/deploy.yml` runs on every push to main: build image → push to ghcr → SSH rollout with `kubectl rollout status --timeout=120s`. A red rollout step means the pod never passed its readiness probe on `/healthz`.

## What Must Run Per Change Type

| Change type | Must run |
|---|---|
| Card content edit | Level 1 + rebuild + Level 3 for the changed module |
| Generator/gpkit change | Level 1 on all modules + rebuild all + Level 3 on hub + one module |
| nginx.conf / Dockerfile change | Level 4 locally (docker run) before push |
| k8s manifest change | Cluster diff review + Level 4 after apply |
| New module | Levels 1–3 + hub rebuild + sitemap entry (once SEO P2 lands) |
| Cert page content (`generator/cert/*`) | `node generator/cert/aif-c01/build.js` exits 0 (it is the validator) + Level 3 at 1440 and 390: answer a question, sit and submit a mock. Reels: a reel plays when it fills the screen, Pause holds, the down arrow moves on, a `#r-<topic>` link opens on its reel; with sound, captions are spoken and the feed advances (a stubbed `speechSynthesis.speak` that ends at once runs a reel in seconds). Answer-key changes need a reviewer who did not write them |

## Gaps (honest)

- No automated check that Simple mode is notation-free **post-build** — the validator checks source dicts, but a builder regression could reintroduce notation. The 2026-09-07 audit had to verify this by hand.
- No link checker for internal anchors (the audit found forward-reference corrections needed).
- No MathML assertion (task 6 will need a check to prevent regression).
- No render test for figures across themes.
