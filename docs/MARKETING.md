# Gradient Path — Marketing & Distribution Plan

_Last verified: 2026-09-21 · against: working tree (HEAD 57245e8 + uncommitted docs)_

## Product Positioning

**Gradient Path** is a free, no-signup, no-tracking study site for AI/ML engineering interviews. It is not a course and not a textbook. Every card is built around the follow-up question, not the definition — the specific wrong sentence candidates say, and the decision you make with the numbers in front of you.

**Fact** — `generator/BRIEF.md`: "Each card is meant to be read in ten minutes before bed and to survive contact with a real interview the next morning."

## Target Audiences

| Segment | Where They Hang Out | Pain Point | Hook |
|---|---|---|---|
| ML engineers interviewing at FAANG/startups | Reddit (r/MachineLearning, r/cscareerquestions), Blind, Hacker News | "I know the concepts but freeze on follow-ups" | Drill-driven, follow-up-first cards |
| Data engineers moving into ML | LinkedIn, Towards Data Science, internal Slack communities | "I understand the data pipeline but not the model math" | Simple mode: zero notation, stands alone |
| CS students (final year, new grad) | Reddit, Discord study groups, campus career centres | "Textbooks are too dense; LeetCode doesn't cover ML" | Blind 75 + ML modules in one place |
| Hiring managers & interviewers | LinkedIn, Twitter/X, conference talks | "Candidates give Wikipedia answers, not real decisions" | Cards encode the specific traps they see |
| Self-taught builders (AI agents, indie ML) | Hacker News, Indie Hackers, Twitter/X | "I built it but can't explain the trade-offs" | Production-tier cards: sizing, budgets, failures |

## Distribution Channels

### 1. Organic Community (High Trust, Zero Cost)

**Reddit**
- r/MachineLearning — share a single high-quality card with the title "What the interviewer actually asks about [topic]" and a link to the module
- r/cscareerquestions — post the Blind 75 module, positioning it as "the ML/DS path nobody talks about"
- r/LocalLLaMA, r/ollama — LLM module cards on RAG, quantisation, serving; relevant to the builder community
- Format: screenshot the card's drill section (the bold verdict + reasoning), link to the full page. Reddit rewards content previews over bare links.

**Hacker News**
- "Show HN" post when a major milestone ships (new module, quiz feature, 250+ cards)
- Comment on relevant threads: "LLM serving costs" → link to System Design sizing card
- Never spam. One genuine contribution per thread.

**LinkedIn**
- Long-form posts about specific interview traps (e.g. "The cosine similarity mistake every candidate makes")
- Carousel PDFs of 3-4 cards, last slide links to the site
- Tag hiring managers and ML engineers in the comments, not the post body

**Twitter/X**
- Thread: "5 things candidates say about [topic] that are wrong" — each tweet is a card's trap + drill verdict
- Screenshots of the two-mode switch (Simple vs Technical) — visual, shareable
- Reply to ML influencers when they mention interview prep; offer a relevant card link

### 2. Content SEO (See `docs/SEO.md` for technical implementation)

- Each card title and kicker are keyword-rich: "p-value", "gradient descent", "attention mechanism", "RAG chunking"
- Long-tail: "what is a p-value interview question", "AdamW vs Adam interview", "vector database sizing system design"
- Blog-style expansion: turn 3-5 related cards into a long-form article on the site's domain (e.g. `gradientpath.site/blog/adamw-decoupled-weight-decay.html`), linking back to the module

### 3. Referral / Network Effects

- **Per-card sharing**: Add a "Copy link to this card" button that generates a URL fragment (`#p-value`) + Open Graph preview. Currently no per-card URLs exist — all cards live inside single-page modules. **Proposed**: see SEO.md for per-card anchor strategy.
- **Progress bragging**: Let users screenshot their "Solid" count ring. The hub already shows a progress ring per module — screenshot-friendly.
- **Study group bundles**: A single URL parameter that pre-selects a subset of cards: `?mode=interview&topics=linear-algebra,llms&time=30min`. **Proposed**.

### 4. Partnerships & Integration

- **Resume review services** (e.g. Interviewing.io, Levels.fyi): offer a free "interview prep companion" link they can include in their materials
- **ML Bootcamps**: provide the site as a free supplement; no revenue share needed (this is a personal project)
- **Open-source communities**: contribute the card schema / authoring brief to ML curriculum projects; brand attribution back to the site
- **GitHub**: The repo is public (`github.com/tusher16/gradient-path`). README is the landing page for developers. Add a prominent link to the live site.

### 5. Paid (Defer — Zero Budget Today)

| Channel | Cost | When to Activate | Hypothesis |
|---|---|---|---|
| Reddit promoted posts | $50–200/test | 1,000+ organic monthly visits | A/B test card screenshots vs. hub screenshot |
| Google Ads (long-tail keywords) | $100–300/mo | 2,000+ monthly, blog posts live | "ML interview questions" $2-5 CPC, low competition |
| Newsletter sponsorship (TLDR, The Batch) | $500–2,000 | 5,000+ monthly, content proven | ML-specific newsletters, high trust |
| LinkedIn sponsored content | $200–500/test | Hiring-manager audience built | Job-title targeting: "Machine Learning Engineer" |

## Content Calendar (Proposed — 12 Weeks)

| Week | Channel | Content | Goal |
|---|---|---|---|
| 1 | HN + Reddit | "Show HN: 217 interview cards for ML engineering, zero signup" | Baseline traffic, feedback |
| 2 | LinkedIn + Twitter | Thread: "The 7 traps candidates fall into on p-values" | Establish voice, build following |
| 3 | Reddit r/ML | Screenshot post: "How I explain attention to a non-technical friend" | Simple-mode awareness |
| 4 | Blog (site) | "AdamW decoupled weight decay: why every candidate gets this wrong" | SEO anchor, long-tail traffic |
| 5 | Twitter | Poll: "Which follow-up stumped you?" + link to relevant card | Engagement, topic discovery |
| 6 | Reddit r/cscareerquestions | "The ML interview path I wish I'd found earlier" | Audience crossover |
| 7 | HN (comment) | Relevant thread → link to System Design sizing card | Comment-driven traffic |
| 8 | LinkedIn | Carousel: "3 cards that changed how I think about RAG" | Professional audience |
| 9 | Blog (site) | "System design for LLM serving: a worked example" | SEO, credibility |
| 10 | Reddit r/LocalLLaMA | "Quantisation trade-offs in 10 minutes" | Builder audience |
| 11 | Twitter | "Before vs after: my interview answers after studying these cards" | Social proof |
| 12 | All channels | "250 cards, 750 drills — here's what's next" | Milestone, community input |

## Metrics & Measurement

| Metric | Tool | Target (Month 3) | Target (Month 6) |
|---|---|---|---|
| Monthly unique visitors | Plausible (privacy-friendly, lightweight) | 500 | 2,000 |
| Avg. session duration | Plausible | 4 min | 6 min |
| Module start rate | `localStorage` events (if instrumented) | 40% of visitors | 50% |
| Card completion rate | `localStorage` events | 20% of starts | 30% |
| Organic search traffic | Search Console | 20% of total | 40% |
| Social referral traffic | Plausible / UTM params | 30% of total | 25% |
| GitHub stars | GitHub API | 50 | 200 |
| Newsletter signups (if added) | Button clicks | N/A | 100 |

**Fact** — Currently no analytics are installed. The site is intentionally zero-tracking. Adding privacy-first analytics (Plausible, Fathom, or self-hosted Umami) is a Proposed decision requiring a `DECISIONS.md` entry.

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| "Just another study site" perception | High | Emphasise the follow-up-first angle, the two-mode design, and the real-system+number grounding rule in all copy |
| Single-page modules hurt SEO | High | See `SEO.md` — implement per-card fragments, sitemap, and structured data |
| No social proof / testimonials | Medium | Add a "Used by" or "Quoted in" section once hiring managers reference it; start with GitHub stars |
| Content accuracy disputes | Medium | Cite sources on every card (audit in progress per `docs/learning-audit-2026-09-07.md`); add a "Report an error" link |
| Platform algorithm changes | Low | Diversify across 4+ channels; never rely on one |
| Competitor copies the format | Low | Open-source the schema; brand around quality and maintenance velocity, not format lock-in |

## Assets Needed

| Asset | Status | Owner |
|---|---|---|
| Open Graph image (1200×630) | Not created | Proposed |
| Twitter Card image (1200×600, dark variant) | Not created | Proposed |
| Short demo video / GIF (mode switch, progress ring) | Not created | Proposed |
| "Share this card" button + URL fragment | Not built | Proposed |
| Press kit (screenshots, one-paragraph description, logo SVG) | Not created | Proposed |
| Analytics dashboard (Plausible self-hosted) | Not installed | Proposed |

## Competitive Landscape

| Competitor | What they do | Gradient Path's differentiation |
|---|---|---|
| LeetCode | Coding interviews only | ML theory, system design, and conceptual follow-ups |
| NeetCode | Video + coding patterns | Written, self-paced, drill-first; no video dependency |
| Machine Learning Mastery (Jason Brownlee) | Textbook-style tutorials | Follow-up-first, not definition-first; interview-specific traps |
| Chip Huyen's ML Interviews Book | Book format | Free, web-native, interactive progress; always updated |
| Towards Data Science (Medium) | Article aggregation | Curated, validated, no clickbait; every claim grounded |
| Interviews.school (various) | Q&A lists | Two-layer accessibility; real systems with numbers |

## Call to Action Hierarchy

Every piece of outbound content should end with ONE of these, matched to the channel:

1. **Direct**: "Study the full card at gradientpath.site →"
2. **Curiosity**: "The follow-up question most candidates miss: [link]"
3. **Community**: "What trap did you fall into? Reply and I'll link the card."
4. **Contribution**: "Found an error? Open an issue: github.com/tusher16/gradient-path"
