# Gradient Path — Design System

_Last verified: 2026-09-21 · against: working tree (HEAD 57245e8 + uncommitted docs)_

## Purpose

This document captures the visual direction (the *how it currently looks*) so a future redesign does not require re-deriving the product's purpose. Product truth (audience, constraints, voice) lives in `PRD.md`.

## Colour Palette

CSS custom properties, dual-value for light/dark mode. **Fact** — `index.html` `:root` and `@media (prefers-color-scheme: dark)`.

| Token | Light | Dark | Usage |
|---|---|---|---|
| `--ground` | `#EFF3F2` | `#0C1211` | Page background |
| `--surface` | `#FFFFFF` | `#141C1B` | Cards, top bar |
| `--sunk` | `#E6ECEA` | `#101817` | Secondary panels, `.howto` |
| `--line` | `#D2DBD9` | `#283432` | Borders, dividers |
| `--line-soft` | `#E3E9E8` | `#1E2827` | Subtle separators |
| `--ink` | `#131C1A` | `#E7EEEC` | Primary text |
| `--ink-2` | `#3B4B48` | `#B6C4C1` | Secondary text |
| `--muted` | `#687975` | `#84948F` | Labels, meta, timestamps |
| `--signal` | `#C11E5C` | `#FF6A9C` | Accent, CTAs, active state, favicon gradient start |
| `--signal-soft` | `#FBE6EE` | `#33141F` | Signal tint background |
| `--memory` | `#0C7A70` | `#42D3BF` | Progress, success, done state, favicon gradient end |
| `--memory-soft` | `#DCF0ED` | `#0C2B28` | Memory tint background |
| `--code-bg` | `#101A19` | `#080E0D` | Code blocks |
| `--code-ink` | `#D6E2DF` | `#D6E2DF` | Code text |
| `--code-mut` | `#7E938E` | `#71857F` | Code comments/meta |

No pure black (`#000000`) or pure gray (`#808080`) is used. Every neutral is tinted toward the palette's cool green undertone.

**Token duplication warning.** These tokens are declared in three places, by copy rather than by import: `index.html` `:root`, `generator/gpkit/page.css` (inherited by every generated module), and `blind75nightlyreview.html` `:root`. **Fact** — the `:root` block in `blind75nightlyreview.html` repeats all fifteen tokens verbatim. A palette change must be made in all three or the pages drift. There is no automated check for this — TASKS.md #20.

## Typography

**Fact** — `index.html` Google Fonts link and CSS rules.

| Role | Font | Weights | Usage |
|---|---|---|---|
| Display / H1-H3 | Bricolage Grotesque | 500, 700, 800 | Headlines, card titles, masthead |
| Body | IBM Plex Sans | 400, 500, 600, italic 400 | Prose, descriptions, notes |
| Labels / Code | IBM Plex Mono | 400, 600, 700 | Eyebrows, pills, progress numbers, code |

- Body: `16px`, line-height `1.62`
- H1: `clamp(2.6rem, 7vw, 4.2rem)`, weight 800, letter-spacing `-0.015em`
- H2 (cards): `1.55rem`, weight 700
- Eyebrows / labels: `11px`, letter-spacing `0.14em`, uppercase, `--muted`
- Pills: `10px`, letter-spacing `0.12em`, uppercase

## Spacing & Layout

- Max content width: `1180px`, centred with `margin: 0 auto`
- Page padding: `28px` horizontal, `64px` top, `90px` bottom
- Card grid: `repeat(auto-fill, minmax(330px, 1fr))`, gap `22px`
- Card internal padding: `28px 28px 24px`
- Section gap: `52px` vertical
- Mobile breakpoint: `980px` — single column, reduced padding (`22px` / `44px` / `70px`)

## Component Patterns

### Card (`.mod`)
- `background: var(--surface)`, `border: 1px solid var(--line)`, `border-radius: 16px`
- `box-shadow: var(--shadow)` — subtle layered shadow, not heavy drop shadow
- Hover: `transform: translateY(-2px)`, `border-color: var(--ink-2)`, `transition: .14s ease`
- Internal: flex column, `gap: 14px`

### Pill (`.pill`)
- `border: 1px solid var(--line)`, `border-radius: 999px`, `padding: 2px 9px`
- `.live` variant: `color: var(--memory); border-color: var(--memory)`
- `.soon` variant: `color: var(--muted)`

### Button / CTA (`.btn`, `.cta`)
- `border-radius: 999px`, `border: 1px solid var(--line)`, `padding: 11px 18px`
- `.cta` (filled): `background: var(--memory)`, `color: var(--surface)`
- Hover: `opacity: .88` or `border-color: var(--ink-2)`

### How-to panel (`.howto`)
- `background: var(--sunk)`, `border-radius: 12px`, `padding: 20px 22px 18px`
- Numbered list with custom counter, mono font, `--signal` colour

### Study path item (`.stop`)
- Grid: `auto minmax(0,1fr) auto`, `gap: 14px`
- Status dot (`.mark`): `15px × 15px`, `border-radius: 50%`
- Active state (`.is-now`): `background: var(--memory-soft)`, `border-color: var(--memory)`
- Done state (`.is-done`): `.mark { background: var(--memory); border-color: var(--memory) }`
- Partial state (`.is-part`): `linear-gradient(90deg, var(--memory) 50%, transparent 50%)`

### Figure / SVG
- Scrollable wrapper (`.fig-scroll`) for overflow on small screens
- Caption with optional swipe hint: `<span class="swipe">Swipe the picture sideways to see all of it.</span>`
- Dual captions: `.simple-only` and `.tech-only` for the two content modes

### Cert prep page (`aws-ai-practitioner.html`, added 2026-10-30)
Extends the world above; source is `generator/cert/aif-c01/page.html`, never the built file.
- **The question is the headline.** `h1` is deliberately 1.2rem; the scenario `.stem` (Bricolage, up to 2.15rem) outranks it. Do not "fix" the small title.
- **Answer rows** (`.opt`): full-width rows, never pills. Pink (`--signal`) is only ever *your* choice or a wrong answer; teal (`--memory`) is correct and progress. Unchosen wrong rows go `--ink-2` with no border, not faded opacity.
- **One authored motion:** the explanation unfolds in place (`.why`, grid-rows 0fr→1fr, .32s expo ease-out). It is `inert` while collapsed.
- **Topic diagrams** (`.mo`, data in `generator/cert/aif-c01/motion.js`, all 30 topics, added 2026-10-31; `build.js` refuses a topic without one): geometry only (boxes, lines, dots, labels on `--sunk`), never pictures or emoji. The diagram plays once when a topic opens, with step N elements and caption N lighting together, 1.8s apart, .5s expo ease-out entrances and no bounce; **Replay** replays it. At rest the finished diagram shows, so no-JS and `prefers-reduced-motion` readers lose nothing (Replay is hidden for them). The SVG is `aria-hidden`; the numbered captions carry the content as text. The animation marker class is `.a`, because `.s` is already the signal colour.
- **How to use route** (`#howto`, `.route`): five numbered stops on the ground with no cards. The numbers carry the order of the day, which is why they are allowed.
- **Domain weight rails** (`.w .track`): bar length is the domain's exam share scaled to the largest (28%); the teal fill is accuracy.
- **Exam room** (`.exam`): the only modal on the site, justified by a timed exam. `.bar`, `main` and `footer` go `inert` while it is open.
- **New token `--meta`** (`#586864` light / `#84948F` dark): `--muted` measures 3.8–4.1:1 on `--ground`, `--sunk` and both tints, below 4.5:1, so this page uses `--meta` for all small secondary text. This is a fourth copy of the palette (see the duplication warning above, TASKS.md #20); the hub and module pages still use `--muted` on those backgrounds and fail the same check.

## Accessibility

- `prefers-reduced-motion: reduce` disables all transitions (`transition: none !important`). **Fact** — `index.html`.
- `:focus-visible` uses `2px solid var(--signal)`, `outline-offset: 3px`.
- **Known defect**: HTML-only KaTeX output. 3,195 `aria-hidden` spans, zero MathML. Screen readers cannot access math expressions. **Fact** — `docs/learning-audit-2026-09-07.md` for the count; **Fact** — the cause is one option on `generator/render_math.js:10`: `katex.renderToString(it.t, { displayMode: it.display, throwOnError: true, strict: false, output: 'html' })`. Changing `output: 'html'` to `'htmlAndMathml'` and rebuilding every math module is TASKS.md #6. Verified present 2026-09-21.

## Anti-Patterns

These are *actively avoided* in the current design. Do not reintroduce them.

### Typography
- **No default/overused fonts as the sole typeface.** Inter, Arial, and raw `system-ui` are never used alone. Bricolage Grotesque provides intentional character for headlines; IBM Plex Sans and Mono provide engineered neutrality for body and labels.
- **Never use a single font family for every role.** The three-font stack is deliberate: Grotesque for display weight, Sans for reading, Mono for data and code.

### Colour
- **No purple-to-blue gradient as default branding.** The site's identity gradient is pink (`#C11E5C`) to teal (`#0C7A70`), evoking signal-to-memory. A purple-blue gradient would read as generic SaaS.
- **No gray text on coloured backgrounds.** `--ink` or `--ink-2` on `--surface` only. If a background is `--signal-soft` or `--memory-soft`, text is still `--ink` (dark-on-light) or `--ink`/`--ink-2` (light-on-dark), never mid-gray on mid-tone.
- **No pure black or pure gray.** `#000000` and `#808080` are absent. Neutrals are tinted: `#131C1A` is ink with green undertone; `#687975` is muted with a cool cast.

### Layout
- **Do not nest cards inside cards.** A `.mod` card contains prose, pills, and a figure. It never contains another bordered card. Nested borders create visual noise and hierarchy confusion.
- **Do not wrap every section in a card by default.** The study path (`.pathwrap`, `.stop` items) and the how-to panel live on the ground background. Only discrete content units (modules, notes) are card-wrapped.
- **No rounded-square icon tile above every heading, applied uniformly regardless of content.** There are no decorative icon tiles. The favicon's inline SVG path is the only brand mark; it does not repeat as a page decoration.

### Motion
- **No bounce or elastic easing on transitions.** All transitions are `ease` or `ease-out` with durations `0.12s`–`0.4s`. Bounce/elastic (`cubic-bezier(0.68, -0.55, 0.265, 1.55)`) cheapens the experience on a study site.

### Content presentation
- **Do not apply the same decorative element to every card regardless of meaning.** The `.pill` (status) and `.mod-n` (module number) are the only metadata decorations. If a card has no status distinction, it gets no badge — badges are semantic, not ornamental.
