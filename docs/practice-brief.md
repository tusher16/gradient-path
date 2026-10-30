# Practice — design brief (TASKS.md #25)

_Written 2026-10-30 · shape only, no code · structure chosen by the user: **The Ledger**_

Tags: **Fact** (file that proves it) · **Proposed** (a design decision for the builder) · **Unknown** (filed as a task).

## 1. Job and audience

Someone who has already read some cards comes back at night for ten minutes to find out what has slipped. Visitor mode: **Operate**. They are tired, often on a phone, and they want to start straight away and get a clear end. They don't want a dashboard.

## 2. Outcome and proof

- One sitting = **15 prompts, about 10 minutes**, ending in a line that says when the next one is due. **Proposed** (agreed in discovery).
- A prompt is either **one interview-drill question** or **one glossary term**:
  - **Fact:** 597 drill questions across the 199 cards in modules 01/03/04/05/06 (`grep '[0-9]+ questions &middot;'` per page). Each has a reveal answer.
  - **Fact:** 116 glossary terms (`generator/glossary/terms.json`).
  - **Fact:** Blind 75 has 0 drill blocks (`grep -c 'class="drill"' blind75nightlyreview.html` → 0), so it stays out of v1.
- Product truth no other flashcard tool can claim: the prompts are the questions an interviewer actually asks next. The answer side links straight back to the card and its production failure.

## 3. Selected direction — The Ledger

- **Visual authority:** the site's own world (docs/DESIGN.md tokens, three-font stack). No new identity. This is an extension, so DESIGN.md is not rewritten.
- **Thesis:** tonight's fifteen prompts are ruled rows in a revision log. Each row carries its own history, so you watch the schedule get written. A deck of cards hides the schedule; this layout shows it.
- **First viewport:**
  - The date in display type.
  - A mono line: `15 due · 0 done · next sitting —`.
  - Row 1 already open. The prompt at reading size, a **Reveal** control, and nothing else.
  - Rows 2–15 sit beneath as single ruled lines. Each shows:
    - a short prompt (truncated);
    - a source tag (`05` in that module's colour, or `term`);
    - a strip of up to 8 past-grade marks;
    - a right-aligned "due" column.
- **Signature moment:** grading a row writes into it. A new mark joins the strip, and the due column flips from `today` to a real date (`Tue 4 Nov`). Then the row closes to one line and the next one opens. The interval is visible as a date, never as a score.
- **Marks:** reuse the study path's `.mark` language from DESIGN.md: filled = had it, half = shaky, open ring = missed. Nothing new to learn.

## 4. Scope and boundaries

- One new root page, `practice.html`, **generated** by a new script (pattern: `generator/glossary/build_glossary.py`). Drill text is extracted from the built module pages at build time and embedded, so no fetch happens at runtime. **Proposed.**
- The page reads the module status keys and never writes them. **Fact** (key names, from each page's `KEY=`): `gp-la-status-v2`, `gp-ml-status-v1`, `gp-llm-status-v1`, `gp-stats-status-v1`, `gp-sysdesign-status-v1`. The roadmap key is `gp-roadmap-v1`. All of practice's own state lives in **one** new key.
- **Anti-goals:**
  - no streaks, flames, XP, levels or mastery-percentage rings;
  - no confetti, mascot, emoji, or "Great job!";
  - no 3D card-flip animation;
  - no card nested in a card;
  - no gradient fills.
  - Copy follows generator/BRIEF.md: direct, with real dates and counts.

## 5. Session, selection, persistence, first visit

**What counts as read** (**Proposed**). A card is in the pool when its module key holds `fuzzy` or `solid` for it, or roadmap has ticked it.
- **Fact:** the status values are `new`, `fuzzy` and `solid` (`05-statistics.html` statusbar buttons).
- **Fact:** roadmap stores `{id: 1}`.
- A term enters the pool when at least one of its linked cards is read. Terms with no published card stay out.

**Scheduler** (**Proposed**: fixed boxes, chosen because the interval must be readable as a date in the row; an SM-2 ease factor is invisible and would break the thesis):
- Boxes 1–5 with intervals of **1, 3, 7, 16 and 35 days**.
- Grades:
  - **Missed** → box 1.
  - **Shaky** → same box, interval restarts.
  - **Had it** → next box. Box 5 + Had it → box 5 again, due in 35 days.
- First practice: an item from a `fuzzy` card starts in box 1, and one from a `solid` card starts in box 2.

**Choosing tonight's 15** (**Proposed**):
1. Items due today or overdue, most overdue first.
2. If fewer than 15, add **new** items (read, never practised), capped at **5 per sitting**, oldest-read module first.
3. At most **5 terms** per sitting.
4. Never two rows from the same card back to back.
5. If more than 15 are due, the rest carry over. The header says so (`23 due · 15 tonight`).

The sitting is **frozen for the local calendar day**: reloading resumes the same 15. Finishing shows "Done for tonight. Next sitting: Thu 6 Nov, 11 due." There is no "keep going" button. The fixed end is the point.

**localStorage** (**Proposed**): one key, `gp-practice-v1`. Every read is wrapped in try/catch, as on every page today. Shape:

```
{ v: 1,
  items: { "<page>#<anchor>/q<n>" | "term:<slug>": { box: 1-5, due: "YYYY-MM-DD", hist: [["YYYY-MM-DD","m|s|h"], …≤8] } },
  today: { date: "YYYY-MM-DD", ids: [15 ids], graded: { id: "m|s|h" } },
  seeded: ["05", …] }   // modules the visitor declared already-studied (first-visit path)
```

- Dates are **local** `YYYY-MM-DD`, never UTC, so a sitting after midnight isn't counted twice.
- Size: 713 items (597 + 116) × about 90 bytes ≈ 64 KB, well under the per-origin quota.
- Item ids use the card's anchor, so a card rename that keeps its anchor keeps its history.

**First visit, no history** (**Proposed**). The ledger renders 15 empty ruled rows, which shows what will fill them, plus one line: "The ledger fills from cards you've marked Fuzzy or Solid." Two actions:
1. **Start reading**: links to roadmap week 1.
2. **I've studied some of this already**: pick modules. Their items enter at box 1 (written to `seeded` in practice's own key, never to the module keys).

Storage blocked (private mode): the sitting still works for the session, and one muted line says marks won't be kept.

**Other states:** nothing due today ("Nothing due. Next sitting Thu 6 Nov."); fewer than 15 eligible (a short ledger, not padding); all 713 practised (the same rules simply keep running).

## 6. Interaction and layout

- Keyboard: `Space` reveals, then `1` / `2` / `3` grade Missed / Shaky / Had it; `J` / `K` move between rows. Every control is also a real button. Focus uses the site's `--signal` outline.
- Reveal shows the card's **Simple** answer in place, plus "Technical answer on the card →" (a deep link to `page#anchor`). Grading happens only after reveal.
- Under 760px the row drops its history strip to the last 4 marks. The open row takes the full width, and grade buttons sit within thumb reach at the row's foot.
- Motion: the row closing and the next opening, .2s ease-out, with no bounce (DESIGN.md). `prefers-reduced-motion` makes it instant.

## 7. Constraints and open decisions

- Static only, and published on push (docs/RULES.md § Publishing Boundary). KaTeX inside drill answers needs the KaTeX CSS the module pages already load.
- **Unknown → TASKS.md #27:** roadmap stores bare card ids, and some ids appear in two modules (`kv-cache`, `lora`, `quantization` in 01 and 04). How does a ticked roadmap row map to one card? The builder must not guess.
- **Unknown → TASKS.md #28:** whether extracting drill answers from built HTML survives a module rebuild unchanged. That needs a check like the glossary's link check.
- **Not decided here:** export/import of `gp-practice-v1` (cross-device). Left out of v1 unless the user asks.

**Next step after confirmation:** impeccable's new-work flow records the direction contract in a surface brief, then a code-led build, then the finish review and the detector run.
