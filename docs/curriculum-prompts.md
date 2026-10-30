# Curriculum-addition prompts

Six briefs for the gaps in *Curriculum additions for AI/ML engineering*
(`learning-audit-2026-09-07.md`), written to be pasted into Claude Cowork or
ChatGPT.

**How to use these.** Paste **Block A** once at the top of a session — or put it
in the Cowork project instructions / a ChatGPT Custom GPT — then paste one
numbered part per session. One part per session, not six: a module is 16–30
cards and quality collapses when you ask for all of it at once.

Work a tier at a time inside a part. Ask for the Foundation tier, read three
cards properly, correct the voice, then ask for Core. The generator does not
care how many files a module arrives in.

---

## Block A — the contract (paste first, every session)

```
You are writing content for Gradient Path, an interview-prep site for AI/ML
engineering. Output is a Python file that exports CARDS = [ {...}, {...} ].
A validator refuses the build if any hard rule below is broken.

THE TWO MODES. Every page has a Simple mode and a Technical mode. Simple mode
is not the technical card with a friendlier opening paragraph: the formula
slab, the code block and the interview-grade drill answers are REMOVED from
the page. So the simple layer must stand on its own. A reader who never
touches the switch still has to finish the card able to say something true and
useful.

THE CARD:

CARDS = [dict(
  id    = 'window-functions',        # kebab-case, unique in the module
  tier  = 'foundation',              # foundation | core | advanced | production
  title = 'Window Functions',        # HTML entities allowed; write &amp; not &
  kicker= 'One line naming what the interviewer is really checking',

  # ---- SIMPLE LAYER (never any notation) ----
  simple = '...',                    # str or list[str], 110-190 words total
  analogy= '<b>Like a ...</b> ...',  # one everyday analogy, 35-60 words
  simple_extra = '...',              # optional second plain paragraph
  trap_simple  = '...',              # optional plain-word version of the trap

  # ---- TECHNICAL LAYER ----
  tech     = '...',                  # str or list[str], 130-230 words
  tech_note= '...',                  # optional caveat paragraph, 50-90 words
  math = dict(tex=r'...', note='what the formula does not say', cost='...'),
  code = dict(label='...', cost='postgres', src='<span class="k">select</span> ...'),

  # ---- SHARED, shown in BOTH modes ----
  fig      = dict(kind='...', ...),  # see FIGURES
  caption  = '...',
  caption_simple = '...',            # optional plainer caption
  when     = ['...', '...', '...'],  # 3-5 bullets: when you reach for it
  trap     = '...',                  # the specific wrong sentence a candidate says
  real     = '...',                  # a REAL system/company/incident, WITH a number
  drills   = [dict(q='...', a='<b>verdict.</b> ...', a_simple='<b>verdict.</b> ...'),
              ..., ...],             # exactly 3
  anchor   = dict(formula='...', formula_simple='...', bullets=['...','...','...']),
  chips    = ['...', '...', '...'],  # what this unlocks
  followup = 'the question the interviewer actually asks next',
)]

HARD RULES (the validator enforces these):
1. The simple layer contains NO math notation at all. No $, no ^, no _, no
   Greek letters, no P(, no E[, no log, no sqrt, no O(, no "x = 3". Write "the
   square root of the row count", never a symbol. This applies to simple,
   analogy, simple_extra, trap_simple, anchor.formula_simple and EVERY
   a_simple.
2. Exactly 3 drills, each with q, a and a_simple.
3. Every drill answer opens with a bolded verdict — <b>No.</b>, <b>Two weeks
   is not the answer.</b> — then the reasoning. "Well, it depends" is rejected.
4. Write & as &amp;. Never write an entity as &mdash\; with a backslash.
5. id is kebab-case and unique. Cards are listed in tier order:
   foundation, then core, then advanced, then production.
6. real must name a real system, company, paper or incident AND carry a
   number. "Used in many companies" is rejected.
7. Every figure needs an alt string and must be well-formed XML.

RULES THE VALIDATOR CANNOT CHECK, WHICH MATTER MORE:
8.  Encode the follow-up, not the definition. Anyone can look up what a window
    function is. The card exists to carry what the interviewer asks NEXT.
    followup is that question verbatim, and drill 1 is usually it.
9.  The trap names a specific wrong sentence a candidate says — the actual
    words, not "people find this confusing".
10. Every card ends in a decision. Given these two facts, what do you do
    first? If it cannot be turned into a decision it is a definition and does
    not belong.
11. The simple layer teaches, it does not water down. Same conclusion,
    different vocabulary. If the plain version and the technical version
    disagree about what to do, the plain version is wrong.
12. a_simple answers the same question as a, at the same level of
    correctness, in words a smart person outside the field would follow.
13. British spelling: generalise, regularisation, behaviour, modelling. Use
    &mdash; for em dashes and &rsquo; for apostrophes in prose. Straight
    quotes only inside code.
14. Do not use the word "delve". Do not open a paragraph with "In essence".
    Do not write three-item lists where two items are real and the third is
    filler.
15. when, real, chips and the drill QUESTIONS appear in both modes, so keep
    them free of notation too.

FIGURES. Canvas is 720 wide. Tones: sig (pink, what breaks), mem (teal, what
holds), plain, mute. Pick the kind that matches the SHAPE of the idea, and
make the figure carry information the prose does not — a picture of the words
is worse than no picture. Available kinds:

  pipeline  boxes left to right, with head=[...], steps=[dict(t=,sub=,tone=)]
  grid      a lookup table; best for "which of these two problems do I have"
  plot      curves on axes; xr, yr, xticks, yticks, hlines, vlines, bands,
            curves, marks
  bars      horizontal bars for magnitudes
  scatter   points in groups with an optional boundary curve
  stack     one bar split into segments; latency and cost budgets
  blocks    free-form architecture, boxes placed by hand with links
  tree      a decision tree, nodes + edges
  loop      a cycle with a dashed return arrow
  panels    two or three nested figures side by side

BUILD TRAPS THAT HAVE ALREADY COST REBUILDS:
- Currency. A stray $ pairs with the next one and renders the prose between
  them as maths, silently. Write every dollar sign as &#36;. Never put a $
  inside a figure string at all.
- Do not use LaTeX's \; thin space in math.tex. \, and \quad are fine.

LENGTH: simple 110-190 words, analogy 35-60, tech 130-230, tech_note 50-90,
each drill answer 45-90, real 55-95.

VOICE: direct, second person, no throat-clearing, no "it's important to note".
Confidence without hedging. Name the thing that is actually hard.

Acknowledge this contract in one line, then wait for the module brief.
```

---

## Using `/eli5` in the loop

`/eli5` is a ten-line skill: *"Explain like I'm someone who knows nothing about
this topic, using a HTML artifact with big pictures and few words."* It is
useful here, but not as a generator &mdash; it returns an HTML artifact, not a
`CARDS = [...]` file, so nothing it produces can be pasted into a module.

The mismatch to watch is register. `/eli5` targets someone who knows nothing
and uses **few words**. The card contract targets a smart adult outside the
field and gives the simple layer **110&ndash;190 words**, with rule 11 saying
the simple layer *teaches, it does not water down*. Hand `/eli5` output
straight into a card and you get something charming that fails rule 11 and
tells the reader nothing they can use in an interview.

Where it earns its place is one step earlier, on the cards whose simple layer
you cannot find the words for:

1. `/eli5 <the concept>` &mdash; e.g. `/eli5 exactly-once delivery`. Read the
   artifact and take two things from it: the everyday framing, and the picture
   it reached for.
2. Feed that back as raw material, not as copy:

```
Here is an ELI5 explanation of <concept>:
<paste the plain framing and the analogy>

Use it as raw material for the SIMPLE layer only. Lift the register: the
reader is a smart adult outside the field, not a child. Keep the framing and
the analogy if they survive that lift, drop them if they only worked because
they were childish. The simple layer still has to reach a conclusion an
interviewer would accept &mdash; same conclusion as the technical layer,
different vocabulary. Then write the full card to the contract.
```

3. Check the result against rule 11 yourself. If the plain version and the
   technical version disagree about what to *do*, the plain version is wrong.

The other honest use is as a reader's test. Once a tier is built, open it in
Simple mode and ask whether it would survive being explained back at `/eli5`
level. If a card cannot be, it is usually because the simple layer is a
summary of the technical one rather than an explanation in its own right
&mdash; which is exactly the defect the audit found in modules 01, 03 and 04.

---

## Part 1 — SQL & Data Manipulation

```
Module 08: SQL and Data Manipulation. 28 cards. Write the FOUNDATION tier
first (8 cards) and stop; I will ask for the next tier.

The angle: this is not a SQL tutorial. It is the SQL an AI/ML engineer is
asked to write on a whiteboard, and the follow-up that catches people who
learned SQL from autocomplete. Every card should be recognisable to someone
who has written SQL for years and still gets the follow-up wrong.

foundation (8)
  select-model          what the engine does, and why the clause order you
                        write is not the order it runs
  joins-cardinality     inner/left/right/full, and the row-count blow-up
                        nobody predicts
  null-semantics        three-valued logic; why NOT IN with a NULL returns
                        nothing at all
  distinct-vs-group     when they differ, and which one is lying to you
  order-limit-ties      LIMIT without a deterministic sort is a random sample
  cte-vs-subquery       readability, materialisation, and the optimiser
  types-and-casts       implicit casts, integer division, timezone-naive
                        timestamps
  result-shape          grain: what one row means, and how to say it out loud

core (8)         window frames; ROW_NUMBER vs RANK vs DENSE_RANK; running
                 totals; LAG/LEAD; deduplication patterns; self-joins;
                 pivot/unpivot; conditional aggregation
advanced (7)     temporal and as-of joins; slowly changing dimensions; reading
                 a query plan; when an index does not help; skew and spill;
                 sampling without bias; recursive CTEs
production (5)   idempotent backfills; late-arriving data; the pandas
                 equivalent of each core pattern; pushing work to the database
                 vs pulling into memory; the checks you run before you trust a
                 number

Prefer PostgreSQL syntax and say so when a dialect differs. Every card's real
block should name a real engine behaviour, a real outage pattern or a
published benchmark, with a number.
```

---

## Part 2 — Python Engineering

```
Module 09: Python Engineering. 26 cards. Write the FOUNDATION tier first
(7 cards) and stop.

The angle: the Python an AI/ML engineer is expected to know beyond calling
libraries. Cards should be about behaviour that surprises people in review,
not syntax.

foundation (7)
  object-model          names, objects and references; what assignment does
  mutable-defaults      the shared default argument, and why it bites once a
                        year
  identity-vs-equality  is vs ==, small-int caching, and when it matters
  truthiness            empty containers, zero, None, and the bug in `if x:`
  scope-and-closures    late binding in a loop, and the two standard fixes
  comprehension-vs-gen  memory, laziness, and when a loop is the right answer
  exceptions            what to catch, what to re-raise, and why bare except
                        hides the bug you needed

core (7)         iterators and generators; context managers; dataclasses vs
                 dict vs NamedTuple; typing that earns its keep; itertools,
                 collections and functools; decorators; argument passing
advanced (6)     async I/O — when it helps and when it does nothing; threads
                 vs processes and the GIL; profiling before optimising; memory
                 and copies; why numpy is fast and where the boundary is;
                 caching and its traps
production (6)   pytest — fixtures, parametrise, what to mock and what never
                 to; packaging and pinning; logging vs print; config and
                 secrets; reproducibility; debugging what you cannot reproduce

Target Python 3.11+. Show real tracebacks in code blocks where a traceback is
the clearest explanation.
```

---

## Part 3 — Data & Serving Infrastructure (Module 07)

```
Module 07: Data and Serving Infrastructure. 30 cards. Write the FOUNDATION
tier first (8 cards) and stop.

The config already exists at generator/mod07.py, and generator/content/mod07/
already holds one finished, validated card (health-readiness). Read that card
first and match its density, its directness and its willingness to name a
specific wrong sentence. Do not match its topic. Write the remaining seven.

This module already has a placeholder on the homepage promising: "Docker,
Kubernetes, the pipeline that feeds a model, and the parts of a backend an AI
engineer is still expected to know." Write to that promise.

The angle: an AI engineer is not a platform engineer, and the interview knows
it. These are the infrastructure questions asked of someone who will deploy
and operate a model, not someone who will run the cluster.

foundation (8)
  http-for-ml           request/response, the status codes that matter, and
                        what a timeout actually means
  json-contracts        schemas, versioning, and the field you cannot remove
  auth-basics           API keys, OAuth, service accounts; what goes in an env
                        var and what never does
  container-image       what an image actually is, layer by layer
  dockerfile-cache      layer ordering, and why your build takes nine minutes
  config-vs-secret      environment, configuration and secret are three things
  health-readiness      liveness vs readiness, and the probe that restarts a
                        healthy model server
  the-request-path      one diagram: client to load balancer to pod to model

core (8)         Pod/Deployment/Service/Ingress; requests and limits, and the
                 OOMKill; ConfigMaps and Secrets; rolling updates and
                 rollback; what does not scale horizontally; queues and
                 workers; retries, backoff and idempotency; dead-letter queues
advanced (7)     batch vs streaming; exactly-once vs at-least-once; data
                 contracts and schema evolution; orchestration, DAGs and
                 backfills; object storage, Parquet and partitioning;
                 logs/metrics/traces; cost attribution
production (7)   blue-green, canary and shadow deploys; what artefact you roll
                 back to; GPU scheduling and node pools; autoscaling a model
                 server; an incident on an ML service; the runbook; CI/CD for
                 a model

The repo already has a Dockerfile, an nginx.conf, a k8s/ directory and a
GitHub Actions pipeline. Where a card can point at a real config, prefer a
concrete one over an invented one.
```

---

## Part 4 — Calculus Prerequisites

```
Module 10: Calculus for Machine Learning. 16 cards. Write the FOUNDATION tier
first (6 cards) and stop.

The angle: this is a bridge module, not a maths course. Its job is to make
the existing Linear Algebra matrix-calculus card and the Machine Learning
optimiser cards readable to someone who has not done calculus in ten years.
Every card should end by pointing forward at where the idea is used.

foundation (6)
  what-a-derivative-is  rate of change, read off a curve, with no limits
                        notation in the simple layer
  rules-you-use         power, product, quotient — only the ones that appear
                        in ML
  chain-rule            the one rule the whole of backpropagation is made of
  ml-derivatives        exp, log, sigmoid, ReLU and softmax, and which are
                        not differentiable everywhere
  partial-derivatives   holding the others still, and what that means for a
                        weight
  the-gradient          a vector of partials, and the direction it points

core (6)         why descent subtracts the gradient; second derivatives and
                 curvature; convexity in one variable; a two-layer
                 backpropagation worked by hand with small numbers;
                 numerical vs analytic gradients and gradient checking; where
                 the chain rule becomes the Jacobian
advanced (4)     Taylor expansion and why second-order methods exist; the
                 Hessian in one picture; Lagrange multipliers in one card;
                 the handoff into matrix calculus and the optimisers

Cross-link explicitly in chips and in the prose: the matrix-calculus card in
Linear Algebra (01-linear-algebra.html#matrix-calculus) and the optimisers
card in Machine Learning (03-machine-learning.html#optimisers).

The simple-layer no-notation rule is hardest here and matters most. "The slope
at that point" is the simple layer. Symbols live in tech and math only.
```

---

## Part 5 — Project & Behavioural Interviews

```
Module 11: Project and Behavioural Interviews. 18 cards. Write the FOUNDATION
tier first (5 cards) and stop.

The angle: this module has no formulas and no code, so the card shape has to
carry the load differently. The trap field becomes the specific weak sentence
a candidate actually says. The real field names a published hiring rubric, a
levelling guide or a documented interview process, with a number where one
exists. Figures are mostly grid and tree kinds — decision tables for "which
story do I tell", not diagrams of feelings.

foundation (5)
  story-structure       situation, task, action, result — named honestly, and
                        the two parts people skip
  your-contribution     what "I" means on a team project, without erasing the
                        team
  level-of-detail       how deep to go before you are asked
  the-numbers           the figures you must have ready about your own project
  what-is-scored        what the interviewer writes down while you talk

core (6)         the approach that failed; the tradeoff and what you gave up;
                 the disagreement and how it ended; the thing you would change;
                 the ambiguous requirement; the deadline you missed
advanced (4)     scaling the same story to IC, senior and staff; the hostile
                 follow-up; saying you do not know; a project under NDA
production (3)   the questions you ask them; levelling and compensation; the
                 debrief you write for yourself afterwards

Do not invent anecdotes. Cards teach the shape of an answer and give a
worked example that is clearly labelled as an example, so the reader fills in
their own project.
```

---

## Part 6 — Applied ML Coding

```
Module 12: Applied ML Coding. 20 cards. Write the FOUNDATION tier first
(5 cards) and stop.

The angle: this is the take-home and the pair-programming round, not theory.
Every card is a thing you type. The code block is the centre of the card
rather than an afterthought, and the trap is a specific line of code that
looks right.

foundation (5)
  read-before-you-model  what to check in the first ten minutes, as code
  the-leak-safe-split    the split, written out, with the two orderings that
                         leak
  pipeline-that-cannot-leak  fit on train inside every fold, structurally
  choosing-validation    picking the scheme from the shape of the data
  the-baseline           the number you must beat before a model is allowed

core (6)         computing metrics correctly and choosing the threshold;
                 debugging a shape error; debugging a loop that does not learn;
                 feature engineering inside the pipeline; categoricals and
                 missing values in code; grouped and time-ordered
                 cross-validation
advanced (5)     a tiny retrieval pipeline end to end; a tiny evaluation
                 harness; a scoring function you can trust; profiling a slow
                 training job; making a run reproducible
production (4)   packaging a model for serving; the inference contract; a
                 smoke test that catches a bad model; the monitoring hooks you
                 add before you ship

Prefer scikit-learn, pandas and PyTorch. Every code block must be runnable as
written, with imports. Where a card fixes a bug, show the broken line and the
fixed line, not a paragraph about the difference.
```

---

## Part 7 — role presets and the diagnostic (not a content module)

The audit's closing line asks for something different in kind: *"Add role
presets and a short diagnostic so the learner can test out of familiar
prerequisites."* That is a product change to `index.html` and the progress
model, not a set of cards, so it does not use Block A.

```
Design a role-preset and diagnostic feature for Gradient Path, a static
interview-prep site. Existing modules: 01 Linear Algebra, 02 Blind 75,
03 Machine Learning, 04 LLMs, 05 Statistics, 06 System Design, and six planned
modules — 07 Infrastructure, 08 SQL, 09 Python, 10 Calculus, 11 Behavioural,
12 Applied ML Coding.

Progress today is per-card New/Fuzzy/Solid, stored in localStorage under a
per-module key. There is no backend.

Produce:
1. Three or four role presets (AI/ML engineer, data engineer, data scientist,
   software engineer) as an explicit weighting over modules and tiers — say
   which tiers each role can skip and which it must not.
2. A diagnostic of 12-20 questions that lets a learner test out of a
   prerequisite tier, drawn from existing card drills. Say how many a learner
   must get right to skip a tier, and justify the threshold as a product
   decision rather than a measurement claim.
3. The localStorage schema change, preserving existing keys and marks.
4. What the homepage shows once a preset is chosen.

Keep the scheduler and progress arithmetic in ordinary application code. Do
not propose a backend.
```

---

## After each part comes back

The generator loads a module's card files in **sorted filename order**, and
`check.py` rejects the build if the cards are not in tier order. So the
filename carries the tier number, exactly as the existing modules do
(`generator/content/mod06/s1_a.py`, `s2_a.py`, `s2_b.py` …).

```bash
# 1. save the tier as generator/content/mod08/t1_a.py  (1=foundation, 2=core,
#    3=advanced, 4=production; the letter splits a long tier across files)

# 2. validate that one file on its own, before you ask for the next tier
python3 generator/checkfile.py generator/content/mod08/t1_a.py

# 3. once every tier is in, validate the module as a whole
cd generator && python3 check.py mod08

# 4. build the page (needs a mod08.py config first - copy mod06.py and edit
#    the header, tier titles and blurbs)
cd generator && python3 assemble.py mod08 mod08.py ../08-sql.html

# 5. render the maths IN PLACE - assemble.py leaves $...$ as plain text
python3 generator/katexify.py 08-sql.html
```

Step 5 is easy to forget and the page looks fine without it until you notice
every formula is raw TeX. `katexify.py` skips anything inside `<pre>`, so the
tutor prompts stay plain text.

Two things to do by hand:

- In the `mod08.py` config, write `{N}` / `{n_word}` / `{n}` in any tier title
  or blurb that counts the block, so the number is filled from `len(cards)`.
  A hard-coded count that disagrees now stops the build.
- Add the module to `index.html` — modules 07 through 12 are either
  placeholders or absent, and nothing links a new page automatically.

Then read three cards on the built page **in Simple mode** before you accept
the batch. The validator checks that notation is absent; it cannot check
whether the plain layer actually teaches, and that is the whole point of the
mode.
