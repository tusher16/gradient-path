# Gradient Path — Decision Log

_Last verified: 2026-10-30 · against: working tree (HEAD 57245e8 + uncommitted docs)_

Newest first. Each entry: date, decision, trade-offs, [impact: low|med|high].

---

## 2026-10-30 — The docs suite goes public, except SECURITY.md [impact: high]

First push of `docs/` and `AGENTS.md` (TASKS.md #19), screened per RULES.md § Secrets Screening: a grep for LAN IP ranges, usernames, absolute home paths, key and token markers, and 4–5 digit ports across every `docs/*.md`, `AGENTS.md` and `PRODUCT.md`. The only hard hits were in `docs/2026-08-28-gradientpath-tls-dns.md` (node hostname, personal domain), which was already gitignored. Everything else mentions only the "Node-1" label, `~/.kube/config` as a generic path, and the already-public GitHub handle. **`docs/SECURITY.md` is excluded by filename anyway**: it holds no credential, but it lists open weaknesses (a cluster-admin kubeconfig on the node, a passphrase-less deploy key, fail2ban status unknown on an internet-facing SSH port), and in a public repo that is a target list. Trade-off: contributors lose the threat model, and committed docs still link to it by filename (allowed by the rule). Revisit once TASKS.md #15 and #17 close those items. The owner chose this option on 2026-10-30. The root pages `roadmap.html`, `chips-and-gaps.html` and `glossary.html` stay uncommitted for now (glossary definitions are unreviewed, #24).

## 2026-10-30 — Chips and Gaps becomes a public page [impact: med]

Reversing the 2026-09-22 placement. The concept map was put in `generator/reports/` on the argument that it is a maintainer tool and that a public gap list advertises what the curriculum does not cover. The owner's call is to publish it, so it moved to the repo root and now ships on every deploy. What changed with it: `noindex` stripped, a meta description added, and the copy re-read as a visitor — "Concepts with no card" became "Not written yet", and the gap table is now framed as terms to look up elsewhere in the meantime rather than as a backlog. Trade-off accepted knowingly: the site states its own coverage holes in public, in exchange for a map that shows a learner where the material converges and an honest account of what it does not teach. The underlying `COPY *.html` publishing boundary in RULES.md is unchanged — it is what made the move a one-line operation.

---

## 2026-09-22 — A study plan ships as a static page, not as pipeline output (yet) [impact: med]

`roadmap.html` splits the existing `PATH` order into thirteen weeks, deep-links all 217 cards, and shows the 45 genuine prerequisite links recoverable from `chips`. It was generated once, by hand, and committed as a finished artefact — the same status the module pages have, but without a generator behind it. Trade-off accepted deliberately: the plan is useful now and the pipeline for it is not worth writing until modules 07 and 08 land and change the card count anyway (TASKS.md #22). `Dockerfile`'s `COPY *.html` picks the file up with no change. The related finding that shaped the page: `chips` resolves to another card only 14% of the time, so it is a vocabulary field, not a link field — a prerequisite graph built from it is real but sparse, and only 45 of 199 cards carry a usable "builds on" edge.

---

## 2026-09-21 — Module 02 is Blind 75; the numbering gap was an artefact of the naming scheme [impact: low]

ARCHITECTURE.md carried two linked Unknowns: a "missing module 02" and uncertain provenance for `blind75nightlyreview.html`. Both resolve to one fact — module 02 *is* Blind 75, and it is hand-maintained rather than generator output, so it never took a numeric filename the way the generated modules did. Trade-off accepted: the filename stays topic-based rather than being renamed `02-blind75.html`, because the hub, the `PATH` array and any existing bookmark all reference the current name, and renaming would break saved links for zero functional gain. Consequence recorded in RULES.md: this page is edited directly, and its copy of the palette tokens must be updated by hand when the design system changes. Evidence in TASKS.md #2.

## 2026-09-21 — Docs get a verification stamp and the review gate gets reviewer tiers [impact: med]

Every living doc now opens with `_Last verified: <date> · against: <tree>_`; none had one before, so a reader could not tell a fact checked today from one inherited three weeks ago. The TASKS.md review gate additionally names three reviewer tiers (isolated subagent > deterministic check > self re-read), adds the `Rework` status for a failed gate, and defines evidence as *a command and its observed output* rather than prose. Trade-off: every future doc edit must also move the stamp, and a stale stamp is now visibly stale — which is the point. The weakness this closes is specific: an author reviewing their own change reproduces the blind spot that produced it, and a prose verdict ("looks correct") is indistinguishable from not having checked.

---

## 2026-09-20 — Vault relocated into `knowledge-vault/` [impact: med]

The adopted vault previously lived at the repo root (`.obsidian/`, `wiki/`, `inbox/`, `.raw/`, `.vault-meta/`, `Projects/` alongside product files). Moved all of it into a self-contained `knowledge-vault/` directory. Because the tool expects the workspace config inside the vault root (otherwise it flags `legacy_layout`), the canonical `.claude-obsidian.json` now sits inside `knowledge-vault/` and a root-level pointer config directs agents running from the repo root. Verified with `doctor` from both locations: `ok: true`, `legacy_layout: false`. Trade-off: two config files to keep consistent vs. a clean repo root and a vault that can be opened or moved as one directory.

## 2026-09-20 — Adopt project-local Obsidian vault instead of separate Documents vault [impact: low]

An initial vault was created at `~/Documents/MyKnowledgeVault`, then a second, project-specific vault was adopted into this repo (`adopt` transaction, 13 files: `.claude-obsidian.json`, `.obsidian/`, `.raw/`, `inbox/`, `wiki/`). Trade-off: the repo now doubles as the Obsidian vault for this project's knowledge (wiki/ carries notes about the code), versus keeping vaults separate from code. Existing project files were untouched.

## 2026-09-20 — Split the docs/ gitignore exclusion; product docs become committable [impact: med]

`.gitignore` previously excluded `docs/` wholesale because it contained the TLS/DNS session log with LAN IPs and the SSH port. Changed to exclude only `docs/2026-08-28-gradientpath-tls-dns.md` (and the already-excluded root-level operator files). Trade-off: future docs must be screened for secrets before committing — the sanitisation warning inside that file still applies. `DEPLOY-RUNBOOK.md` and `SESSION-CONTEXT.md` remain gitignored.

## 2026-09-20 — Documentation suite added under docs/ [impact: med]

Created PRD, ARCHITECTURE, RULES, DESIGN (with anti-patterns), TASKS (with review gate), TEST_PLAN, SECURITY, TOOLS, DECISIONS, MEMORY, LEARNINGS, plus MARKETING and SEO on request, and AGENTS.md at repo root. Trade-off: maintenance burden of 13 living documents vs. institutional memory that survives session boundaries. Facts cited from repo files; gaps marked Unknown rather than invented.

## 2026-09-07 — Learning audit corrections applied [impact: high]

Seven content corrections from the audit (AdamW decay, scikit-learn PCA scoping, cosine similarity reframing, dot-product projection labelling, notation-free Simple mode for 137 cards, suggested-order phrasing, generated narrative counts). Evidence and status per row in `docs/learning-audit-2026-09-07.md`. Citation sweep and corpus-wide agreement check remain open (TASKS.md #10).

## 2026-08-28 — ClusterIssuer gets a third DNS-01 solver for gradientpath.site [impact: high]

Root cause of the TLS outage: every solver on `letsencrypt-prod` carries a `selector.dnsZones` gate, so a zone matching nothing gets **no solver at all** and cert-manager fails the Order before creating a Challenge. Fixed by adding a gradientpath.site solver reusing the All-zones `cert-manager-homelab` token. Rule going forward: **every new Cloudflare zone needs its own solver entry.** Full log in the (gitignored) session doc.

## 2026-08-28 — Deploy workflow pins `KUBECONFIG=$HOME/.kube/config` explicitly [impact: high]

k3s bundles kubectl as a symlink to the k3s binary, which hardcodes `KUBECONFIG=/etc/rancher/k3s/k3s.yaml` (root:root 0600) instead of falling back to `~/.kube/config` like upstream kubectl. Every repo on this cluster had green builds with silent failed rollouts because of it. Fix: copy kubeconfig to tusher16's home on the node; export KUBECONFIG explicitly in the workflow. Same fix applies to flashdeutsch-vocab and rag-studio.

## 2026-08-28 — Dedicated passphrase-less SSH deploy key [impact: med]

The laptop key has a passphrase and cannot be used by Actions. Generated `~/.ssh/gradientpath_deploy`, authorised on Node-1. Whether the `SSH_KEY` repo secret was updated is **Unknown — needs confirmation** (automated rollout never succeeded end-to-end; TASKS.md #1).

## 2026-08-28 — Docker image instead of ConfigMap for page delivery [impact: med]

6.4 MB of HTML exceeds the practical ~1 MiB ConfigMap limit. nginx:1.27-alpine image, wildcard `COPY *.html` so new modules need no Dockerfile change.

## Pre-history — Generator pipeline made permanent [impact: high]

The content pipeline was ephemeral twice and had to be rebuilt from scratch both times; it now lives in `generator/` with the validator, schema docs, and authoring brief committed. Trade-off: generated HTML (~2 MB/module) is committed to git, growing repo history permanently on each rebuild.
