# Gradient Path — Architecture

_Last verified: 2026-10-30 · against: working tree (HEAD 57245e8 + uncommitted docs)_

## Stack

| Layer | Technology | Rationale |
|---|---|---|
| Content | Static HTML/CSS/JS, no framework | Portable to any static host; no build step at deploy time |
| Math rendering | KaTeX (pre-rendered at build time) | Zero runtime JS dependency; `generator/katexify.py` bakes HTML+CSS inline |
| Figures | Declarative SVG via `gpkit/figkit.py` | Scalable, dark/light theme-aware via CSS custom properties |
| Fonts | Google Fonts CDN: Bricolage Grotesque, IBM Plex Mono, IBM Plex Sans | **Fact** — `index.html` `<link>` tags |
| Container | `nginx:1.27-alpine` | Single-purpose static file server; ~7 MB image |
| Orchestration | K3s, namespace `apps` | Personal homelab; shared with policypulse, flashdeutsch, rag-studio |
| Ingress | Traefik + cert-manager (DNS-01 via Cloudflare) | `traefik.ingress.kubernetes.io/router.entrypoints: websecure`; `cert-manager.io/cluster-issuer: letsencrypt-prod` **Fact** — `k8s/ingress.yaml` |
| CI/CD | GitHub Actions → ghcr.io → SSH into Node-1 → `kubectl set image` | Runner cannot reach private LAN API directly; deploys via `appleboy/ssh-action` **Fact** — `.github/workflows/deploy.yml` |

## Folder Structure

```
Gradient Path/
├── index.html                  ← Hand-edited hub page; module grid, progress picker
├── 01-linear-algebra.html      ← Generated (generator output; do not hand-edit)
├── 03-machine-learning.html    ← Generated
├── 04-llms.html                ← Generated
├── 05-statistics.html          ← Generated
├── 06-system-design.html       ← Generated
├── blind75nightlyreview.html   ← Module 02. Hand-maintained, NOT generator output
├── chips-and-gaps.html         ← Public concept map — prerequisite graph + uncovered terms
├── roadmap.html                ← Hand-generated study plan (13 weeks). Self-contained;
│                                 rebuild with the scripts noted in TASKS.md #22
├── Dockerfile                  ← nginx:1.27-alpine, COPY *.html, EXPOSE 80
├── nginx.conf                  ← /healthz, gzip, try_files
├── .github/workflows/deploy.yml← Build → ghcr.io → SSH rollout
├── k8s/
│   ├── deployment.yaml         ← 1 replica, readiness/liveness on /healthz
│   ├── service.yaml            ← ClusterIP, selector app=gradient-path
│   ├── ingress.yaml            ← TLS, traefik, gethomepage.dev annotations
│   └── cluster-issuer.yaml   ← Stopgap copy of shared infra (to move to homelab repo)
├── generator/                  ← Content pipeline — ephemeral twice, rebuilt from scratch
│   ├── gpkit/
│   │   ├── build.py            ← Cards → page shell; two-layer contract
│   │   ├── figkit.py           ← SVG figure generator, 720 wide, CSS-variable colours
│   │   ├── prompts.py          ← Tutor prompt templates
│   │   ├── page.css            ← Extracted verbatim from built page, then extended
│   │   └── page.js             ← Theme toggle, progress, localStorage
│   ├── assemble.py             ← Collect → validate → build → fix entity bug
│   ├── check.py                ← Schema validator; refuses build on errors
│   ├── checkfile.py            ← Single-file validator
│   ├── katexify.py             ← Pre-render $...$ with local KaTeX install
│   ├── build_index.py          ← Rebuilds hub from each page's own rail
│   ├── retrofit.py             ← Back-ports Simple mode onto pre-existing pages
│   ├── SCHEMA.md               ← Card contract for content authors
│   ├── BRIEF.md                ← Authoring voice and quality brief
│   ├── content/mod05/          ← Statistics card sources (Python dicts)
│   ├── content/mod06/          ← System Design card sources
│   ├── mod05.py / mod06.py / mod07.py ← Per-module CFG (title, deck, tiers, prompt role)
│   ├── content/mod07/          ← Module 07 Data & Serving Infrastructure (1 card, unbuilt)
│   ├── content/mod08/          ← Module 08 SQL & Data Manipulation (23 cards, unbuilt, no CFG)
│   └── research/               ← Interview questions, failures, sources
├── docs/                       ← Product documentation (this directory)
└── claude-obsidian/            ← Knowledge vault tooling (separate product checkout)
```

## Module Inventory

Canonical structural table for modules. Other docs link here rather than restating counts.

| # | Module | Page | Built? | Cards | Storage key | Source |
|---|---|---|---|---|---|---|
| 01 | Linear Algebra, Slowly | `01-linear-algebra.html` | ✅ generated | 38 | `gp-la-status-v2` | pre-`generator/content` |
| 02 | Blind 75 in 18 Moves | `blind75nightlyreview.html` | ✅ **hand-maintained** | 18 patterns / 75 problems | `b75-status-v1` | the HTML file itself |
| 03 | Machine Learning, Model by Model | `03-machine-learning.html` | ✅ generated | 48 | `gp-ml-status-v1` | pre-`generator/content` |
| 04 | LLMs, End to End | `04-llms.html` | ✅ generated | 51 | `gp-llm-status-v1` | pre-`generator/content` |
| 05 | Statistics &amp; Probability | `05-statistics.html` | ✅ generated | 40 | `gp-stats-status-v1` | `content/mod05` + `mod05.py` |
| 06 | ML &amp; GenAI System Design | `06-system-design.html` | ✅ generated | 22 | `gp-sysdesign-status-v1` | `content/mod06` + `mod06.py` |
| 07 | Data &amp; Serving Infrastructure | — | ❌ **unbuilt** | 1 validated | `gp-infra-status-v1` | `content/mod07` + `mod07.py` |
| 08 | SQL &amp; Data Manipulation | — | ❌ **unbuilt, no CFG** | 23 validated | *(none yet)* | `content/mod08`, **`mod08.py` missing** |

**Fact** — counts 01–06 from `index.html` `MODULES` array (`total` field); 38+18+48+51+40+22 = **217**, the headline figure in `AGENTS.md` and `PRD.md`.
**Fact** — 07/08 counts from `python3 generator/check.py mod07` → `1 cards | 0 errors | 0 warnings` and `mod08` → `23 cards | 0 errors | 0 warnings`, run 2026-09-21.
**Fact** — module 07 identity from `generator/mod07.py` `CFG`: `key='gp-infra-status-v1'`, `num='07'`, `h1='Data &amp; Serving Infrastructure'`.
**Fact** — module 08 identity from `generator/content/mod08/t1_a.py` docstring: "Module 08: SQL and Data Manipulation. Foundation only, eight cards. Dialect: PostgreSQL 18". Content has since grown to three tiers (foundation 8, core 8, advanced 7); no `production` tier and no `mod08.py` config exist, so it cannot be assembled yet — TASKS.md #7.

Module 07 is announced on the hub with a `soon` pill and a `Not yet` affordance (**Fact** — `index.html` line 329). Module 08 is not announced at all.

### Cert prep pages (outside the module numbering)

| Page | URL | Built by | Content | Storage keys |
|---|---|---|---|---|
| `aws-ai-practitioner.html` | `/aws-ai-practitioner` | `node generator/cert/aif-c01/build.js` (validates, then inlines `topics.js`, `questions.js`, `extras.js` into `page.html`) | 30 topics, 30 practice + 2×65 mock questions (13/16/18/9/9 per domain), 14-day plan, 25 look-alike pairs, 5 general prompts; scope = AIF-C01 exam guide v1.2 (2026-10-29) | `aif-v1-state`, `aif-v1-mock`; theme shares `gradient_path_theme` |

**Fact** — `node generator/cert/aif-c01/build.js` → `30 topics | practice 30 | Mock A 13/16/18/9/9 | Mock B 13/16/18/9/9 | 188 KB`, run 2026-10-30. The output is generated: edit the sources, never the HTML. It does not use the card schema or `check.py`; `build.js` is its own validator (answer counts, Select TWO wording, mock split, every topic taught in week 1). Clean URLs come from `nginx.conf` `try_files $uri $uri.html $uri/`. It is not in `MODULES`, so it does not count toward the 217.

## Data Flow

### Content Pipeline (write path)

```
Content author writes Python card file
        ↓
generator/check.py  →  schema validation  →  errors? exit 1
        ↓
generator/assemble.py <content-folder> <config> <out.html>
        ↓
generator/katexify.py <out.html>  →  pre-renders KaTeX, mutates in place
        ↓
generator/build_index.py  →  reads each module's rail, rebuilds hub
        ↓
git add *.html  →  commit  →  push
        ↓
GitHub Actions: docker build → push ghcr.io/tusher16/gradient-path:<sha>
        ↓
SSH into Node-1: kubectl set image deployment/gradient-path gradient-path=ghcr.io/...:<sha>
        ↓
K3s rolling update (readiness probe on /healthz must pass)
```

**Fact** — `generator/gpkit/README.md`: rebuild sequence; `generator/assemble.py` comment on entity bug fix; `.github/workflows/deploy.yml` exact steps.

### Request Flow (read path)

```
User → DNS (Cloudflare proxied A record) → home router 80/443
        → K3s NodePort/LoadBalancer (Traefik) → Service (ClusterIP) → Pod (nginx)
        → nginx serves static HTML from /usr/share/nginx/html
        → gzip on the wire if client accepts
```

**Fact** — `docs/2026-08-28-gradientpath-tls-dns.md`: actual architecture is "proxied A record → home IP → router port-forward 80/443 → Traefik LoadBalancer"; no Cloudflare Tunnel despite earlier plan.

## Schema

### Card (Python dict)

**Fact** — `generator/SCHEMA.md`:

```python
CARDS = [dict(
    id='kebab-case-unique',           # str, unique across module
    tier='foundation',                # foundation | core | advanced | production
    title='HTML entities allowed',
    kicker='What interviewer is checking',
    simple='...',                      # str or list[str], NO math notation
    analogy='<b>Like a ...</b> ...',  # everyday analogy
    tech='...',                        # str or list[str], interview-grade
    fig=dict(kind='plot', ...),        # declarative figure
    caption='...',
    when=['...', '...'],               # 3-5 bullets
    trap='Wrong sentence candidates say',
    real='Real system + number',
    drills=[dict(q='...', a='...', a_simple='...'), ...],  # exactly 3
    anchor=dict(formula='...', bullets=['...']),
    chips=['...'],                     # what this unlocks
    followup='The question asked next',
)]
```

### Progress (localStorage)

**Fact** — `generator/gpkit/page.js` (inferred from `index.html` progress classes `.mark`, `.is-done`, `.is-part`, `.is-now`):

- Per-card state: `new` → `fuzzy` → `solid`
- Stored as a map keyed by card ID, value is `"done"` or `"part"` or timestamp
- Module progress derived from card states
- `localStorage` is origin-scoped; `file://` progress does not carry to the live site

## Key Decisions

| Decision | Rationale | Date | Impact |
|---|---|---|---|
| Pre-render KaTeX at build time | Zero runtime JS; no CDN dependency at page load | 2026 (initial) | high |
| Inline SVG figures via `figkit.py` | No image requests; dark/light themable via CSS vars | 2026 (initial) | high |
| Two-layer content contract | Simple mode must stand alone, not truncate technical | 2026 (initial) | high |
| `localStorage` only, no backend | No auth, no GDPR/Privacy Policy, no ops burden | 2026 (initial) | med |
| Docker image over ConfigMap | 6.4 MB total; exceeds practical ~1 MiB ConfigMap limit | 2026-08-28 | med |
| SSH deploy from GitHub Actions | Runner cannot reach private LAN API; k3s API is LAN-only | 2026-08-28 | high |
| `nodeSelector` omitted | Both nodes x86_64; mixed-arch not expected **Fact** — `DEPLOY-RUNBOOK.md` | 2026-08-28 | low |

## Open Architecture Questions

1. **Homelab repo migration.** `k8s/cluster-issuer.yaml` is a stopgap copy of shared infra. Canonical home is `tusher16/homelab/apps/infra/` — that repo does not exist yet. **Fact** — `k8s/cluster-issuer.yaml` header comment.
2. **Module 02 gap.** Modules are numbered 01, 03, 04, 05, 06, 07, 08. There is no 02. Unknown whether this is a deliberate skip or a missing module.

   **Resolved 2026-09-21 — there is no gap.** Module 02 *is* the Blind 75 page. **Fact** — `index.html` `MODULES` array: `{"id": "b75", "n": "02", "key": "b75-status-v1", "total": 18, "title": "Blind 75 in 18 Moves", "href": "blind75nightlyreview.html"}`. It is numbered 02 on the hub (`<span class="mod-n">MODULE 02</span>`, pill `live`) but keeps a topic filename rather than a numeric one. The numeric prefixes track *generated* modules; Blind 75 is not generated, so it never acquired one. See the Module Inventory below.
3. **Blind 75 page generator status.** Not clear if `blind75nightlyreview.html` is generator output or hand-maintained.

   **Resolved 2026-09-21 — hand-maintained, not generator output.** **Fact** — marker counts in `blind75nightlyreview.html` vs the known-generated `05-statistics.html`: `simple-only` 0 vs 109, `tech-only` 0 vs 119, `katex` 0 vs 131, `gp-*-status-v*` key 0 vs 1 (`gp-stats-status-v1`). Blind 75 carries its own `b75-status-v1` localStorage key and a bare `KEY` accessor rather than `gpkit/page.js`. It re-uses the design tokens (identical `:root` palette block) but none of the two-layer build contract. Editing boundary is stated in `RULES.md`.
