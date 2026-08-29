# Brief for card authors — Gradient Path modules 05 and 06

You are writing content for gradientpath.site, a personal interview-prep site
owned by an AI/data engineer. It is not a course and not a textbook. Each card
is meant to be read in ten minutes before bed and to survive contact with a
real interview the next morning.

## Read these first, fully, before writing anything

1. `/tmp/gp/SCHEMA.md` — the card contract. The validator enforces it.
2. `/tmp/gp/EXAMPLE_CARD.py` — one complete passing card. This is the quality
   bar. Match its density and its directness.
3. Your assigned sections of the research file. Everything you need — the real
   failures, the numbers, the follow-ups, the source URLs — is already in there.
   Use it. Do not invent numbers, and do not go and re-research; if the research
   file does not support a claim, cut the claim.

## What makes these cards good, in one paragraph

They encode **the follow-up question, not the definition**. Anyone can look up
what a confidence interval is. The card exists to carry what the interviewer
asks *next*, the specific wrong sentence candidates say, and the decision you
have to make with the numbers in front of you. A card that could be replaced by
a Wikipedia first paragraph has failed.

## The two layers — the point of this module

Simple mode **removes** the math slab, the code block and the technical drill
answers from the page. It is not a friendlier first paragraph on the same card.
So:

- The `simple` layer must be able to stand completely alone. A reader who never
  touches the switch finishes the card able to say something true and act on it.
- It contains **no math notation at all**. Not one `$`, superscript, Greek
  letter, `P(`, `log`, or `x = 3`. Write "the square root of the sample size".
  The validator rejects the file otherwise.
- `a_simple` answers the same drill question as `a`, just as correctly, in words
  a smart person outside the field would follow. It is not a shorter `a`.
- If the plain version and the technical version would lead someone to different
  decisions, the plain version is wrong. Rewrite it, do not soften it.

Think of it as the same expert explaining the same thing twice: once to a
colleague from another team over coffee, once to the interviewer.

## Voice

Second person, direct, British spelling (generalise, behaviour, modelling).
No throat-clearing, no "it is important to note", no "in essence", never the
word "delve". `&mdash;` for em dashes, `&rsquo;` for apostrophes in prose,
`&amp;` for every ampersand. Confidence without hedging. Name the thing that is
actually hard rather than reassuring the reader that it is fine.

## Figures

Every card needs one, and it must carry information the prose does not. A box
with the card's title in it is worse than no figure. Pick the `kind` that
matches the *shape* of the idea: a lookup table for "which of these two problems
do I have", a plot for "what happens as this grows", a stack for a budget, a
loop for a feedback cycle, blocks for an architecture. The `foot` line is the
one sentence the picture is making.

## When you are done

```
python3 /tmp/gp/checkfile.py <your file>
```

Fix every error. Fix the warnings too unless you have a reason. Then report
back: the card ids you wrote, one line each on the angle you took, and anything
you had to leave out because the research did not support it.
