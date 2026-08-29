# The card contract — Gradient Path modules 05 and 06

You are writing Python files that export `CARDS = [ {...}, {...} ]`.
`check.py` refuses to build if any rule below is broken, so read it once properly.

The page has **two modes** and this is the whole point of the module. Simple
mode is not the technical card with a friendlier first paragraph — the math
slab, the code block and the interview-grade drill answers are **removed from
the page** in simple mode. So the simple layer has to stand on its own: a
reader who never touches the switch must still finish the card able to say
something true and useful.

---

## The card

```python
CARDS = [dict(
  id    = 'p-value',                 # kebab-case, unique across the module
  tier  = 'foundation',              # foundation | core | advanced | production
  title = 'The p-value',             # HTML entities allowed; write &amp; not &
  kicker= 'Not the probability you are wrong, and the follow-up finds out whether you know that',

  # ---------------- SIMPLE LAYER (no notation, ever) ----------------
  simple = '...',                    # str or list[str]. Plain English. NO math notation.
  analogy= 'Like a ...',             # one everyday analogy, opens with <b>Like a ...</b>
  simple_extra = '...',              # optional second plain paragraph
  trap_simple  = '...',              # optional plain-word version of the trap

  # ---------------- TECHNICAL LAYER ----------------
  tech     = '...',                  # str or list[str]. Interview-grade. $...$ allowed.
  tech_note= '...',                  # optional caveats paragraph
  math = dict(tex=r'\bar{x} \pm 1.96\frac{s}{\sqrt{n}}',
              note='what the formula does not say',
              cost='normal approximation only'),   # optional; tech mode only
  code = dict(label='Read it off a bootstrap', cost='scipy',
              src='<span class="k">import</span> numpy ...'),  # optional; tech mode only

  # ---------------- SHARED ----------------
  fig      = dict(kind='plot', ...),  # see FIGURES below
  caption  = '...',                   # technical caption
  caption_simple = '...',             # optional plainer caption
  when     = ['...', '...', '...'],   # 3-5 bullets: when you reach for it
  trap     = '...',                   # the specific wrong thing candidates say
  real     = '...',                   # a REAL system or failure, with a number
  drills   = [dict(q='...', a='<b>verdict.</b> ...', a_simple='<b>verdict.</b> ...'), ...],  # exactly 3
  anchor   = dict(formula='...', formula_simple='...', bullets=['...','...','...']),
  chips    = ['...', '...', '...'],   # what this unlocks
  followup = 'the question the interviewer actually asks next',
)]
```

### Optional blocks (module 06 mostly)

```python
  nums = [dict(k='TIME TO FIRST TOKEN', v='300 ms', s='what a chat UI can hide')],
  ask  = [dict(q='How fresh does the index need to be?',
               a='Usually: minutes for support docs, seconds for code.')],
  estimate = dict(label='Sizing it out loud', cost='order of magnitude',
                  rows=[dict(l='documents', w='10M x 4 chunks', r='40M chunks'),
                        dict(l='index size', w='40M x 768 x 4 B', r='123 GB', tot=True)],
                  note='optional sentence'),
  tradeoffs = [dict(k='HNSW vs IVF', v='<b>HNSW</b> for recall at low QPS, ...')],
  verdict = dict(no='what a no-hire says', yes='what a strong answer says'),
  when_label = 'The interviewer is really testing',   # overrides the block heading
  real_label = 'Where this has actually broken',
```

---

## Hard rules (check.py enforces these)

1. **The simple layer contains no math notation at all.** No `$`, no `^`, no `_`,
   no Greek letters, no `P(`, no `E[`, no `log`, no `sqrt`, no `O(`, no `x = 3`.
   Write "the square root of the sample size", not `√n`. This applies to
   `simple`, `analogy`, `simple_extra`, `trap_simple`, `anchor.formula_simple`
   and **every `a_simple`**.
2. **Exactly 3 drills**, each with `q`, `a` and `a_simple`.
3. **Every drill answer opens with a bolded verdict** — `<b>No.</b>`,
   `<b>Two weeks is not the answer.</b>` — then the reasoning. A drill answer
   that opens with "Well, it depends" is rejected.
4. **`&` must be written `&amp;`.** Never write an HTML entity as `&mdash\;`.
5. `id` is kebab-case and unique. Cards are listed in tier order.
6. `real` must name a real system, company, paper or incident **and carry a
   number**. "Used in ML applications" is rejected by the validator.
7. The figure must render and be well-formed XML.

## Rules the validator cannot check, which matter more

8. **Encode the follow-up, not the definition.** Anyone can look up what a
   p-value is. The card exists to carry what the interviewer asks *next*.
   `followup` is that question, verbatim, and drill 1 is usually it.
9. **The trap names a specific wrong sentence a candidate says.** Not "people
   find this confusing" — the actual words: *"we only peeked twice, so it's
   fine."*
10. **Every card ends in a decision.** Given these two numbers, what do you do
    first? If the card cannot be turned into a decision, it is a definition and
    does not belong.
11. **The simple layer teaches, it does not water down.** Same conclusion,
    different vocabulary. If the plain version and the technical version
    disagree about what to do, the plain version is wrong.
12. **`a_simple` answers the same question as `a`**, at the same level of
    correctness, in words a smart person outside the field would follow.
13. British spelling to match the rest of the site: *generalise, regularisation,
    behaviour, modelling*. Use `&mdash;` for em dashes, `&rsquo;` for
    apostrophes in prose, and straight quotes only inside code.
14. Do not use the word "delve", do not open a paragraph with "In essence",
    and do not write three-item lists where two items are real and the third is
    filler.

---

## FIGURES

`from gpkit import figkit` is not imported by you — you just write the dict.
Canvas is 720 wide. Tones: `sig` (pink — what moves, where the error is),
`mem` (teal — what survives, the honest answer), `plain`, `mute`.

Pick the kind that matches the *shape of the idea*, and make the figure carry
information the prose does not. A picture of the words is worse than no picture.

```python
# boxes left to right
dict(kind='pipeline', head=['WHAT MOVES','WHAT SURVIVES'], foot='one line under it',
     alt='screen-reader description',
     steps=[dict(t='sample', sub='n = 400', tone='sig'), dict(t='estimate'),
            dict(t='interval', tone='mem', sub='the honest answer')])

# a lookup table -- the best kind for "which of these two problems do I have"
dict(kind='grid', head=['WHAT YOU SEE','WHAT YOU DO'], xlab='p-value', ylab='effect size',
     cols=['small p','large p'], rows=['big effect','tiny effect'],
     cells=[[dict(t='SHIP IT', sub='and say the CI', tone='mem', fill=True),
             dict(t='underpowered', sub='do not conclude null', tone='sig')],
            [dict(t='significant, useless', sub='report the CI', tone='sig', fill=True),
             dict(t='nothing here', sub='stop', tone='plain')]],
     foot='a caption line', alt='...')

# curves on axes (data units; you give the ranges)
dict(kind='plot', xr=(0,30), yr=(0,0.30), ph=190, xlab='days running', ylab='false positive rate',
     xticks=[(0,'0'),(10,'10'),(20,'20'),(30,'30')], yticks=[(0.05,'5%'),(0.15,'15%')],
     hlines=[dict(y=0.05, tone='mem', label='what you think you have')],
     vlines=[dict(x=14, tone='sig', label='you peek here')],
     bands=[dict(x0=10,x1=20,tone='sig',label='the peeking zone')],
     curves=[dict(pts=[(0,0.05),(10,0.14),(30,0.26)], tone='sig', label='actual', dy=-8)],
     marks=[dict(x=30,y=0.26,label='26%',tone='sig')],
     foot='...', alt='...')

# horizontal bars for magnitudes
dict(kind='bars', head=['COST','WHAT YOU GET'], lw=180, vmax=100,
     bars=[dict(label='no correction', v=26, tone='sig', note='26% FPR'),
           dict(label='sequential test', v=5, tone='mem', note='5%')],
     xlab='false positive rate', foot='...', alt='...')

# points in groups, optional boundary
dict(kind='scatter', xr=(0,10), yr=(0,10), groups=[dict(pts=[(1,2),(3,4)], tone='sig',
     label='observed', lx=2, ly=8)], curves=[dict(pts=[(0,0),(10,10)], tone='mem')],
     xlab='...', ylab='...', alt='...')

# one bar split into segments -- latency and cost budgets
dict(kind='stack', head=['THE BUDGET','WHERE IT GOES'],
     segs=[dict(t='retrieval', v=40, sub='40 ms', tone='mem'),
           dict(t='rerank', v=90, sub='90 ms', tone='plain'),
           dict(t='generation', v=870, sub='870 ms', tone='sig')],
     foot='...', alt='...')

# free-form architecture -- boxes placed by hand, with arrows
dict(kind='blocks', h=280,
     boxes=[dict(x=34,y=60,w=130,h=54,t='query', tone='sig'),
            dict(x=210,y=60,w=140,h=54,t='hybrid search', sub='BM25 + vector', tone='mem')],
     links=[dict(a=0,b=1,label='embed')],
     labels=[dict(x=360,y=20,t='REQUEST PATH')],
     foot='...', alt='...')

# a decision tree
dict(kind='tree', h=250, nw=150,
     nodes=[dict(id='r',x=360,y=44,t='paired data?'),
            dict(id='y',x=190,y=140,t='paired t-test', tone='mem'),
            dict(id='n',x=530,y=140,t="Welch's t-test", tone='mem')],
     edges=[dict(a='r',b='y',label='yes'), dict(a='r',b='n',label='no')],
     foot='...', alt='...')

# a cycle with a dashed return arrow
dict(kind='loop', loop_label='and the next batch is trained on this',
     steps=[dict(t='model ranks', tone='mem'), dict(t='users click'),
            dict(t='clicks become labels', tone='sig')], foot='...', alt='...')

# two or three nested figures side by side
dict(kind='panels', head=['BEFORE','AFTER'],
     panels=[dict(t='no correction', fig=dict(kind='bars', ...)),
             dict(t='corrected', fig=dict(kind='bars', ...))], alt='...')
```

`alt` is required on every figure and is read by screen readers — describe what
the picture *shows*, not what it is called.

---

## Length

A card is roughly:
- `simple` 110–190 words, `analogy` 35–60
- `tech` 130–230 words, `tech_note` 50–90 when present
- each drill answer 45–90 words; `a_simple` may be shorter
- `real` 55–95 words

Module 06 worked-design cards run longer — 300–500 words in `tech` across
paragraphs, plus `ask`, `estimate`, `tradeoffs` and `verdict`.

Write like the existing modules: direct, second person, no throat-clearing, no
"it's important to note". Confidence without hedging, and name the thing that
is actually hard.

---

## One more rule about shared blocks

`when`, `real`, `chips` and the drill *questions* are shown in **both** modes.
Keep them readable without notation: "an experiment that came back at p = 0.31"
is fine, `$\hat{\theta}$` is not. Anything that genuinely needs notation belongs
in `tech`, `math`, `code` or the `a` answer.

## Before you finish

Run the validator and fix everything it prints:

```
cd /tmp/gp && python3 check.py mod05      # or mod06
```

`/tmp/gp/EXAMPLE_CARD.py` is a complete, passing card. It is the quality bar —
match its density, its directness and its willingness to name a specific wrong
sentence. Do not match its topic.

## Two build traps that have already cost rebuilds

**Currency.** `katexify` pairs `$ ... $` across a line, so a stray currency sign
finds the next one and renders the prose between them as math &mdash; silently,
because the result is often valid TeX. Write every dollar sign as `&#36;`
(`&#36;1.87/GPU-hr`). The validator now rejects unbalanced `$` and any `$...$`
span that reads like a sentence, but write it right the first time. Never put a
`$` inside a figure string at all.

**`\;` in TeX.** Do not use LaTeX's `\;` thin space in `math.tex`. `\,` and
`\quad` are fine.
