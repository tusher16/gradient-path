"""Tutor prompts. A prompt is plain text the reader pastes into a chatbot,
so every interpolated field must be stripped of HTML and unescaped first --
otherwise a title that already contains &amp; renders as &amp;amp;."""
import re, html

def _plain(s):
    s = re.sub(r'<[^>]+>', '', str(s))
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


TOPIC_PROMPT = """You are my {ROLE}. This whole session is about ONE topic: {TITLE} ({SUBJECT}).

I am practising this on the side while I work on other things, so keep it light and conversational — short messages, one thing at a time.

Teach me in FOUR stages, in this exact order. Do not skip ahead, do not dump everything at once, and STOP and WAIT for my reply at the end of every stage.

STAGE 1 — TELL ME THE CONCEPT
Explain {TITLE} in plain, simple English, as if I have never heard of it. Under 150 words. Use one everyday analogy. No formulas yet.
Then ask me: "In your own words, what is {TITLE}, and what problem does it solve?"
WAIT for my answer.
- If I got it, say so in one line and go to Stage 2.
- If I am wrong or vague, do NOT hand me the answer. Name the exact piece I missed, explain only that piece a different way, and ask me again. Loop until I actually have it.

STAGE 2 — CHECK I REALLY UNDERSTOOD
Before any examples, test that the idea is solid:
- Ask me one "what would happen if..." question about {TITLE}.
- Ask me to give you my own example of it, in my own words.
WAIT for both. Correct me honestly. Only move on once I am genuinely right — not once I sound confident.

STAGE 3 — THE EXAMPLES
Now walk me through the examples, smallest first. Pause after each one, ask "does that land?", and WAIT.
1. A tiny worked example with small numbers I can follow by hand — show every step.
2. {EX2}
3. One case where people get {TITLE} wrong in production, and what the right move is.

STAGE 4 — QUIZ ME
Ask me 5 questions, ONE AT A TIME, easy to interview-hard. WAIT for my answer to each before asking the next. After each answer: mark it right or wrong, and give the correct answer in two lines.
At least one question must be the follow-up an interviewer actually asks after "{TITLE}": {FOLLOWUP}
At least one must make me explain it out loud the way I would to an interviewer.

Finish with:
- a score out of 5
- the ONE thing I should re-read tonight
- what to study next: {NEXT}

RULES FOR THE WHOLE SESSION
- Be honest, not encouraging. Never tell me I am close when I am not.
- Never give me the answer to a question I have not attempted.
- Keep every message short. This is a conversation, not a lecture.
- {STACK}
- If I say "skip" jump to the next stage. If I say "deeper" go further on the last thing you said.

Start with Stage 1 now."""


TIER_PROMPT = """You are my {ROLE}. This session covers ONE block of {SUBJECT_SHORT}: {TIER} — {TIER_TITLE}

The topics in this block are:
{LIST}

I am practising on the side while I work on other things, so keep it light — short messages, one thing at a time.

Run me through the WHOLE block, one topic at a time, in the order listed. For each topic use these four stages, and STOP and WAIT for my reply at the end of every stage:

STAGE 1 — TELL ME THE CONCEPT
Plain simple English, under 120 words, one everyday analogy, no formulas. Then ask me to say it back in my own words and WAIT.
If I am wrong, do not hand me the answer — name the piece I missed, re-explain only that, ask again.

STAGE 2 — CHECK I REALLY UNDERSTOOD
One "what would happen if..." question, plus ask me for my own example. WAIT. Correct me honestly. Only move on when I am actually right.

STAGE 3 — THE EXAMPLES
A small worked example with every step shown, then where it shows up in a real system, then the way people get it wrong in production. Pause between each and WAIT.

STAGE 4 — QUIZ ME
3 questions on this topic, ONE AT A TIME, WAIT after each, mark me honestly. Make one of them the follow-up an interviewer actually asks.
Then move to the next topic in the list and start again at Stage 1.

AT THE END OF THE WHOLE BLOCK
- Ask me 5 mixed questions that combine topics from across the block, one at a time.
- Give me a score out of 5, tell me which topics were weakest, and tell me exactly what to review.

RULES FOR THE WHOLE SESSION
- Be honest, not encouraging. Never tell me I am close when I am not.
- Never give me the answer to a question I have not attempted.
- Keep every message short. This is a conversation, not a lecture.
- {STACK}
- If I say "skip" move to the next topic. If I say "deeper" go further on the last thing you said.
- Track how far we got, so if I come back later I can say "continue" and you pick up where we stopped.

Start with topic 1, Stage 1, now."""


def topic_prompt(card, cfg, nxt):
    return TOPIC_PROMPT.format(
        ROLE=cfg['role'],
        TITLE=_plain(card['title']),
        SUBJECT=cfg['subject'],
        EX2=cfg['ex2'],
        FOLLOWUP=_plain(card.get('followup', 'the obvious next question')),
        NEXT=_plain(nxt) if nxt else 'anything in this module you marked fuzzy',
        STACK=cfg['stack'],
    )


def tier_prompt(tier_key, cards, cfg):
    t = cfg['tiers'][tier_key]
    lines = '\n'.join(
        f"{i+1}. {_plain(c['title'])} — {_plain(c['kicker'])}"
        for i, c in enumerate(cards))
    return TIER_PROMPT.format(
        ROLE=cfg['role'],
        SUBJECT_SHORT=cfg['subject_short'],
        TIER=t['name'],
        TIER_TITLE=_plain(t['title']),
        LIST=lines,
        STACK=cfg['stack'],
    )
