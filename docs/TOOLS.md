# Gradient Path — Tool Inventory

_Last verified: 2026-10-30 · against: working tree (HEAD 57245e8 + uncommitted docs)_

Tiers:
- **Auto-approved** — read-only, local, reversible. Use freely.
- **Needs confirmation** — sends anything external, modifies cluster/remote state, deletes, deploys, or publishes. Announce intent and get a yes first.

## Build & Validate

| Tool | Purpose | Tier | Notes |
|---|---|---|---|
| `python3 generator/check.py <mod>` | Schema-validate card sources | Auto-approved | Read-only; refuses bad builds |
| `python3 generator/checkfile.py <file>` | Validate one card file | Auto-approved | |
| `python3 generator/assemble.py` | Build module HTML | Auto-approved | Writes only the named output file; reversible via git |
| `python3 generator/katexify.py` | Pre-render math in built HTML | Auto-approved | Mutates the output file in place — rebuildable |
| `python3 generator/build_index.py` | Rebuild hub from modules | Auto-approved | Rewrites index.html — verify with `git diff` |
| `python3 generator/retrofit.py` | Back-port Simple mode onto old pages | **Needs confirmation** | Rewrites built HTML broadly |
| `npm install` (generator/) | Local KaTeX for katexify | Auto-approved | Local node_modules, gitignored |
| `chips-and-gaps.html` | Concept map — card prerequisite graph, uncovered-term list, convergence points | Auto-approved | Static, reads nothing. **Now a public page** (repo root), so it ships on every deploy — see DECISIONS.md 2026-10-30 |

## Git & Files

| Tool | Purpose | Tier |
|---|---|---|
| `git status/diff/log/show` | Inspect | Auto-approved |
| `git add/commit` (local) | Stage & commit locally | Auto-approved |
| `git push` | **Publishes** — triggers the deploy workflow (image build + K3s rollout) | **Needs confirmation** — a push to main is a production deploy |
| `git checkout/restore` | Revert working tree | Auto-approved (discards uncommitted work — confirm if changes exist) |

## Docker & Kubernetes (operator)

| Tool | Purpose | Tier |
|---|---|---|
| `docker build` | Local image build | Auto-approved |
| `docker push` | Publishes image to ghcr | **Needs confirmation** |
| `kubectl get/describe/logs` | Inspect cluster | Auto-approved |
| `kubectl apply` | Mutates live cluster | **Needs confirmation** |
| `kubectl set image / rollout` | Production deploy | **Needs confirmation** |
| `kubectl delete` (any object) | Destructive | **Needs confirmation** — extra caution: Certificate deletion burns Let's Encrypt rate-limit budget (5 failed validations/hostname/hour) |
| `kubectl port-forward` | Local tunnel for testing | Auto-approved |

## Cluster/Infrastructure Notes

- The GitHub Actions runner deploys via SSH (`appleboy/ssh-action`) into Node-1 — a push to main is therefore both a publish and a deploy. Treat them as one irreversible action.
- `k8s/cluster-issuer.yaml` is shared cluster infrastructure (policypulse, landing pages, flashdeutsch). **Only ever ADD solvers — never reorder or alter existing ones.** Always confirm before touching.
- Cloudflare DNS/API: any change to zones, tokens, or tunnel config is **Needs confirmation**.

## Host Tooling (agent environment)

| Tool | Purpose | Tier |
|---|---|---|
| `claude-obsidian` CLI (project-local checkout) | Vault ops, lint, capture | Auto-approved for read/lint; `--apply` transactions need confirmation |
| Design linter (e.g. `npx impeccable`) | **Not installed.** Recommendation only — installing requires confirmation | N/A |
