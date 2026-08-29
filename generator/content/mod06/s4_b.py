CARDS = [dict(
    id='content-moderation',
    tier='production',
    title='Design: content moderation at 50M posts a day',
    kicker='The cascade is arithmetic, not architecture &mdash; and the 260 reviewers at the end of it are what set every threshold in front of them',
    simple=[
        'Fifty million posts a day is about six hundred a second, and five times that when '
        'something big is happening. You cannot show every one to a large language model: that '
        'design alone runs to about a hundred and fifty thousand dollars a month, and the model '
        'is slower than the half-second you have to decide in. So the system is a cascade. A '
        'small, fast, purpose-trained classifier sees everything and confidently settles the '
        'great majority. What it is unsure about goes to a language model, which is far more '
        'expensive but can read the policy and explain its answer. What that model is still '
        'unsure about, or what is severe enough that no machine should decide alone, goes to a '
        'person.',
        'The percentages are the design. The first stage settles eighty-five to ninety per cent. '
        'The second sees ten to fifteen. Only one or two per cent ever reaches a human &mdash; '
        'and that is still five hundred thousand to a million reviews a day. At ten seconds each '
        'you need somewhere between a hundred and seventy-five and three hundred and fifty '
        'full-time reviewers. If the business will fund a hundred, the thresholds have to move, '
        'and you say out loud which harms will now go unreviewed rather than letting the queue '
        'quietly grow to three days deep.',
        'The second thing to get right is that a rate is not a count. Wrongly removing eight '
        'tenths of a per cent of posts sounds comfortably inside a one per cent target. On fifty '
        'million posts it is four hundred thousand people a day, and none of them experience a '
        'rate. Removing too much costs you trust and an appeals queue; removing too little costs '
        'you harm and a regulator. Both costs are real, they differ by category, and where you '
        'draw the line is a policy decision you make with the business, not a number you tune to '
        'maximise accuracy.',
    ],
    analogy=('<b>Like airport security.</b> Almost everyone walks through the arch in two '
             'seconds. A few get the wand. A very few have a bag opened by a person. It only '
             'works because each stage hands a small fraction to the next, and the whole thing '
             'is sized by how many officers you can staff, not by how many passengers turn '
             'up.'),
    trap_simple=('Saying &ldquo;we send every post to a language model with the policy in the '
                 'prompt&rdquo;. It is the most expensive design available and you can kill it '
                 'with arithmetic in thirty seconds. The quieter mistake is one confidence '
                 'threshold for every category. Getting spam wrong and getting a credible threat '
                 'wrong do not cost the same thing, so a single line drawn across all of them is '
                 'a decision to be badly wrong on at least one.'),
    tech=[
        'Kill the obvious design out loud, first. 50M posts at ~200 input tokens is <b>10B input '
        'tokens a day</b>; at nano-tier rates of &#36;0.15&ndash;0.20 per million in and '
        '&#36;0.60&ndash;1.25 out, <b>&#36;90&ndash;150K a month</b> &mdash; over &#36;300K at '
        '500 tokens a post. The published estimate for the same design is ~&#36;150K/month, so '
        'the arithmetic converges. And say the sensitivity: the answer moves with the token '
        'assumption, which is why you state the assumption before the number.',
        'The path, in order. Post published &rarr; event stream &rarr; a <b>hash-match front '
        'door</b> for known-violating media, exact and near-free, which must run before anything '
        'learned &rarr; <b>tier 1</b>, a fine-tuned multilingual encoder with one head per '
        'category, GPU-batched, <b>under 50 ms</b>, disposing of <b>85&ndash;90%</b> &mdash; at '
        '~2,900 posts/s peak against 1,000+ inferences/s on a batched encoder, <b>3&ndash;6 '
        'GPUs</b> with headroom. Then a three-way split on confidence: clearly safe publishes '
        'and logs; clearly violating is auto-actioned and the user notified; and the '
        'uncertainty band, <b>10&ndash;15%</b> or 5&ndash;7.5M a day, queues for <b>tier 2</b> '
        '&mdash; an LLM holding the policy text, returning a category, a rationale and a '
        'confidence in <b>300&ndash;500 ms</b>. At 250 in and 50 out that is 1.25B input tokens a '
        'day, <b>~&#36;6&ndash;8K a month</b>: a 15&ndash;25&times; reduction. Still uncertain, '
        'or high severity, goes to <b>tier 3</b> humans, queued by predicted harm &times; reach. '
        'Alongside: a policy registry, because policies change weekly and every change is a '
        'model change with its own eval run; an appeals route that re-runs the decision one tier '
        'up and feeds overturns back as labels; and every decision retained with model version, '
        'score and category &mdash; 25 GB/day, ~9 TB/year, trivial and legally necessary.',
        '<b>Tier 3 is the design.</b> 1&ndash;2% of 50M is 500K&ndash;1M reviews a day; at ~10 '
        'seconds each that is 1,400&ndash;2,800 reviewer-hours, or <b>175&ndash;350 full-time '
        'reviewers</b>. It dwarfs the compute bill by an order of magnitude and it is the whole '
        'reason tiers 1 and 2 exist. Treat it as an input, not an output: if finance funds 100 '
        'people, the bands move and you name which categories now go unreviewed.',
        'Failure modes, before you are asked. <b>Adversarial evasion</b>: users adapt within '
        'hours of a policy change &mdash; leetspeak, homoglyphs, text baked into images. '
        'Normalise aggressively, keep a rules path for hotfixes, and read a sudden drop in '
        'per-category volume as evasion rather than compliance. <b>The review feedback '
        'loop</b>: reviewers only see what the model routes to them, so next '
        'year&rsquo;s labels are shaped by this year&rsquo;s blind spots &mdash; inject a random '
        'sample of auto-approved content into the queue, the only unbiased read on what tier 1 '
        'misses. <b>Cascade at peak</b>: a 5&times; spike overwhelms tier 2, so widen the '
        'auto-approve band for low-severity categories while holding the line on high-severity, '
        'and call that a chosen degradation rather than an outage. <b>Appeals that change '
        'nothing</b>: if overturns never become labels the same error repeats forever. And '
        '<b>the aggregate metric</b>: one multilingual model underperforms on low-resource '
        'languages, precisely where failures matter most &mdash; report per language and per '
        'category, or the number&rsquo;s job is to hide the problem.',
    ],
    tech_note=('Be clear about which numbers are which. The 578 posts/s, the token totals, the '
               'tier bills and the 175&ndash;350 reviewer FTE are <i>arithmetic</i> from stated '
               'assumptions &mdash; posts per day, tokens per post, seconds per review &mdash; '
               'not measurements of anything. The tier percentages and latencies come from a '
               'published worked design, and the ~&#36;150K/month all-LLM figure is that '
               'design&rsquo;s own estimate, which our arithmetic independently reproduces. Say '
               'which is which. An interviewer who catches a calculation dressed up as a '
               'benchmark discounts every other number you gave.'),
    fig=dict(
        kind='blocks', h=280,
        boxes=[
            dict(x=16,  y=46, w=100, h=54, t='event stream', sub='50M a day'),
            dict(x=130, y=48, w=100, h=50, t='hash match', sub='known media'),
            dict(x=244, y=50, w=132, h=46, t='tier 1 encoder', sub='85-90% resolved', tone='mem'),
            dict(x=390, y=52, w=126, h=42, t='tier 2 LLM', sub='10-15%, 6M a day', tone='mem'),
            dict(x=530, y=53, w=172, h=40, t='tier 3 humans', sub='1-2%, 260 FTE', tone='sig'),
            dict(x=530, y=184, w=172, h=54, t='reviewer labels', sub='plus appeals'),
            dict(x=306, y=184, w=196, h=54, t='random-sample holdout', sub='of auto-approved', tone='sig'),
            dict(x=16,  y=184, w=262, h=54, t='retrain tier 1', sub='every policy change', tone='mem'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3), dict(a=3, b=4),
            dict(a=4, b=5, side='down'),
            dict(a=5, b=6, side='left'),
            dict(a=6, b=7, side='left'),
            dict(a=7, b=2, side='up', dash='4 3', label='new model version'),
        ],
        labels=[
            dict(x=16, y=30,  t='decision path, under 500 ms', a='start'),
            dict(x=16, y=168, t='the offline loop', a='start'),
        ],
        foot='every stage hands a small fraction to the next, and the last fraction is people',
        alt='Architecture diagram. The top row runs left to right: an event stream of 50 million '
            'posts a day passes a hash-match front door, then a tier 1 encoder that resolves 85 '
            'to 90 per cent in under 50 milliseconds, then a tier 2 language model handling 10 '
            'to 15 per cent, then a human review tier handling 1 to 2 per cent and needing about '
            '260 full-time reviewers. A second row underneath runs the offline loop back the '
            'other way: reviewer labels and appeals overturns, a random sample of auto-approved '
            'posts, and a retraining step whose new model version feeds back up into tier 1.'),
    caption=('Pink is the binding constraint. The size of the human queue is set by the two '
             'thresholds to its left, not by the volume arriving on the far left &mdash; which '
             'is why moving a band by half a point is a headcount decision. Teal is what '
             'actually disposes of posts: one cheap model doing almost all the work, one '
             'expensive model doing the ambiguous remainder. The bottom row is why the top row '
             'keeps working, and the random sample in the middle of it is the only part that '
             'sees what tier 1 waved through.'),
    caption_simple=('The pink box is the part that cannot stretch: people. How many you need is '
                    'decided by the two settings to its left, not by how many posts arrive. The '
                    'teal boxes do almost all the work. The bottom row is what keeps the fast '
                    'model honest &mdash; what reviewers decided, what appeals overturned, and a '
                    'random handful of the posts the fast model waved through, checked by a '
                    'person anyway.'),
    when_label='The interviewer is really testing',
    when=[
        'Whether you kill the all-LLM design with arithmetic instead of describing it politely',
        'Whether human review capacity is a number you computed or a box you drew',
        'Whether your confidence bands are per category or one line across all of them',
        'Whether you can turn a false positive rate into a count of angry people',
        'Whether you know that changing the policy is changing the model',
    ],
    trap=('Saying &ldquo;we route every post through an LLM with the policy in the prompt&rdquo;. '
          'That is 10B input tokens a day and ~&#36;150K a month before you have handled a '
          'single appeal, and it misses the 500 ms budget anyway. The subtler version, and the '
          'one that actually loses offers: &ldquo;we set the confidence threshold at 0.9&rdquo; '
          '&mdash; one global band. Over-removal costs speech and trust, under-removal costs '
          'harm and a regulator, and the exchange rate between those two is different for spam '
          'and for a credible threat, so a single line is a decision to be badly wrong on at '
          'least one category. The third is treating human review as an overflow valve rather '
          'than a sized system with 175&ndash;350 people in it.'),
    nums_label='The numbers you design against',
    nums=[
        dict(k='THROUGHPUT', v='578 posts/s', s='50M a day, with 3&ndash;5&times; peaks to ~2,900/s'),
        dict(k='DECISION BUDGET', v='under 500 ms', s='tier 1 under 50 ms, tier 2 at 300&ndash;500 ms'),
        dict(k='ALL-LLM BILL', v='~&#36;150K/month', s='10B input tokens a day &mdash; the design you kill first'),
        dict(k='TIERED BILL', v='~&#36;6&ndash;8K/month', s='tier 2 only, a 15&ndash;25&times; reduction'),
        dict(k='HUMAN CAPACITY', v='175&ndash;350 FTE', s='1&ndash;2% routed at ~10 s a review &mdash; the binding constraint'),
        dict(k='0.8% FALSE POSITIVES', v='400,000 a day', s='under target, and nobody experiences a rate'),
    ],
    ask=[
        dict(q='Pre-publication or post-publication?',
             a='Post-publication with fast takedown for most categories; pre-publication only for the most severe.'),
        dict(q='What is the latency requirement?',
             a='Under 500 ms for the automated decision. That alone rules out an LLM on the hot path for every post.'),
        dict(q='What are the categories, and what are their base rates?',
             a='A handful of policy categories, all rare &mdash; well under 1% combined. Rarity is what makes precision hard.'),
        dict(q='What does a false positive cost against a false negative?',
             a='Asymmetric and category-dependent. Insist on per-category, because a global answer here is the whole trap.'),
        dict(q='Is there a human review team, and how big may it be?',
             a='Yes, and its capacity is a hard constraint. Ask to size it in the first five minutes.'),
        dict(q='Do we have to explain decisions to users?',
             a='Yes &mdash; appeals are a required path, which makes per-decision audit retention a design input.'),
        dict(q='Multilingual?',
             a='Yes. Which means one model, uneven quality, and metrics reported per language.'),
    ],
    estimate=dict(
        label='The arithmetic, out loud',
        cost='derived from stated assumptions',
        rows=[
            dict(l='arrival rate', w='50M / 86,400 s', r='578 posts/s'),
            dict(l='peak', w='578 x 5', r='~2,900/s'),
            dict(l='all-LLM input', w='50M x 200 tokens', r='10B tokens/day'),
            dict(l='all-LLM bill', w='nano-tier in and out rates', r='~&#36;90-150K/month'),
            dict(l='tier 1 fleet', w='2,900/s / ~1,000 per GPU', r='3-6 GPUs'),
            dict(l='tier 2, 10-15% of posts', w='5M x 250 tokens/day', r='~&#36;6-8K/month'),
            dict(l='tier 3, 1-2% of posts', w='50M x 0.015', r='750K reviews/day'),
            dict(l='reviewer hours', w='750K x 10 s / 3,600', r='2,080 hours/day'),
            dict(l='reviewers, 8-hour shifts', w='2,080 / 8', r='~260 FTE', tot=True),
        ],
        note='The last row is the one to say slowly. 260 reviewers is a headcount request, a '
             'recruiting pipeline and a wellbeing programme, and it falls out of exactly two '
             'numbers you chose &mdash; the fraction you escalate and the seconds a review '
             'takes. Name both as assumptions when you say the answer, because the interviewer '
             'will move one of them and watch whether you can re-derive it.'),
    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='CASCADE VS ONE MODEL',
             v='<b>Cascade, and it is the entire cost argument.</b> Disposing of 85&ndash;90% in '
               'under 50 ms is what turns ~&#36;150K a month into ~&#36;6&ndash;8K. The price is '
               'three systems to calibrate and two thresholds that drift, so name that instead '
               'of pretending tiering is free.'),
        dict(k='WHERE THE BANDS SIT',
             v='<b>Per category, from harm asymmetry, set with the business.</b> Say it as: '
               '&ldquo;over-removal costs trust and appeals, under-removal costs harm and a '
               'regulator, and the exchange rate is different for spam than for a credible '
               'threat.&rdquo; A global threshold is the naive answer and it is visible in one '
               'sentence.'),
        dict(k='PRE- VS POST-PUBLICATION',
             v='<b>Post-publication for almost everything.</b> Pre-publication adds latency to '
               'every post and makes ordinary users pay the false-positive cost. Reserve it for '
               'the narrow set of categories where removal after the fact is not an acceptable '
               'remedy &mdash; and name that set rather than gesturing at it.'),
        dict(k='HUMAN CAPACITY',
             v='<b>An input, not an output.</b> If the sized answer is 350 and the business '
               'funds 100, the bands move and you state which harms now go unreviewed. Making '
               'that trade explicit is the mature answer; letting the queue grow to three days '
               'deep is the same decision taken silently.'),
        dict(k='LLM AS CLASSIFIER VS EXPLAINER',
             v='<b>Explainer.</b> On the common categories a fine-tuned encoder matches an LLM '
               'and costs a fraction of it. What the LLM actually buys is novel and contextual '
               'cases plus a rationale a reviewer can act on in ten seconds. Deploy it where '
               'that is the value, not as a general-purpose classifier.'),
        dict(k='ONE MULTILINGUAL MODEL',
             v='<b>Take it, then refuse to report an aggregate.</b> A single multilingual model '
               'underperforms on low-resource languages, which is exactly where moderation '
               'failures do the most damage. Precision and recall per language, or the global '
               'number is doing public relations rather than measurement.'),
    ],
    verdict=dict(
        no='Routes every post to an LLM and never computes the bill. Draws one confidence '
           'threshold across all categories. Draws a box marked &ldquo;human review&rdquo; '
           'without ever asking how many people are inside it. Reports one aggregate accuracy '
           'number. Has no answer for what a policy change does to the classifier that was '
           'trained on the old policy.',
        yes='Kills the all-LLM design with arithmetic in the first two minutes. Names three '
            'tiers with percentages and latencies attached to each. Computes 175&ndash;350 '
            'reviewer FTE out loud and calls it the binding constraint. Sets per-category bands '
            'from harm asymmetry. Adds a random sample of auto-approved posts to the review '
            'queue to break the feedback loop. And converts every rate into an absolute count '
            'before being asked to.'),
    real_label='The same trade, in a system that publishes its numbers',
    real=('Stripe Radar scores every transaction in under 100 ms against 1,000+ characteristics '
          'on a base fraud rate of roughly 1 in 1,000, and publishes the other side of the '
          'ledger too: <b>0.1% of legitimate payments blocked</b>. That is this card&rsquo;s '
          'argument in another domain &mdash; a rate small enough to print, attached to a count '
          'of wrongly-refused customers the company decided it could live with. '
          'Moderation&rsquo;s version is harsher because the denominator is larger: 0.8% of 50M '
          'posts is 400,000 people a day, and the anger concentrates wherever the errors '
          'cluster.'),
    math=dict(
        tex=r'\text{FTE} = \frac{N \times r \times t_{\text{review}}}{3600 \times h_{\text{shift}}}'
            r'\quad\Rightarrow\quad \frac{50\text{M} \times 0.015 \times 10\,\text{s}}{3600 \times 8} \approx 260',
        note=r'What it does not say: $r$ and $t_{\text{review}}$ are both choices, not constants. '
             r'Move the escalation rate from 1.5% to 1% and 260 becomes 174; assume 25 seconds a '
             r'review for graphic content and it becomes 650. The line is worth writing on the '
             r'board precisely because it drags those two assumptions into the open where they '
             r'can be argued about.',
        cost='one headcount, two assumptions'),
    drills=[
        dict(q='Your false positive rate is 0.8%, comfortably under the 1% target. Users are furious. Why?',
             a='<b>Because 0.8% of 50 million is 400,000 wrongly-actioned posts a day.</b> A rate '
               'under target can still be an enormous absolute number, and nobody experiences a '
               'rate. Two things follow. Report the count next to the rate on every dashboard, '
               'because 400,000 forces a conversation that 0.8% does not. And expect the errors '
               'to be clustered rather than uniform &mdash; by language, by community, by '
               'category &mdash; so a global 0.8% can conceal 6% in the language where the '
               'multilingual model is weakest, which is exactly the group filing the complaints. '
               'Per-cohort rates and per-category counts, and if you cannot produce them, that '
               'is the first thing to fix.',
             a_simple='<b>Because eight tenths of a per cent of fifty million is four hundred '
                      'thousand posts a day.</b> A figure under target can still be an enormous '
                      'number of real people, and none of them experience a percentage. So put '
                      'the count beside the rate everywhere you show it. Then expect the '
                      'mistakes to be lumpy rather than evenly spread: they cluster in one '
                      'language or one community, so a comfortable overall figure can hide a '
                      'terrible one for the group that is actually complaining. Break it down by '
                      'group before you defend it.'),
        dict(q='Add images and video. What changes?',
             a='<b>Hashing moves to the front and sampling replaces exhaustive analysis.</b> '
               'Perceptual hash matching against known-violating media runs before anything '
               'learned: exact, near-free, and it catches most re-uploads, which are the bulk of '
               'the volume. Tier 1 becomes a multimodal encoder rather than a text one. Video is '
               'not one decision &mdash; sample keyframes and run an audio transcript path, so a '
               'ten-minute video becomes tens of frame decisions rather than a single verdict on '
               'a file. Per-item cost rises by roughly an order of magnitude, which pushes '
               'harder in the same direction the text design already went: hash first, sample '
               'rather than analyse everything, and keep the expensive path for the uncertainty '
               'band.',
             a_simple='<b>Fingerprinting comes first, and you stop looking at everything.</b> '
                      'Most bad images and videos are re-uploads of things you have already '
                      'removed, so a fingerprint check catches them for almost nothing before '
                      'any model runs. The fast first stage has to learn to see pictures as well '
                      'as read text. And video is not one decision: you take a still every few '
                      'seconds plus a transcript of the audio, so a ten-minute clip becomes a '
                      'few dozen small decisions. Everything costs roughly ten times more per '
                      'item, which makes the cheap stages matter more, not less.'),
        dict(q='Regulators require you to report precision and recall per category. Can you?',
             a='<b>Not from production decisions &mdash; those are the thing being measured, not '
               'ground truth.</b> You need a labelled random sample: draw a stratified sample '
               'per category per week, have it double-reviewed by humans with disagreements '
               'adjudicated, and report precision and recall with confidence intervals against '
               'that. Then say the part most candidates skip: the sample size sets the interval '
               'width, so it has to be designed against the rarest category rather than scraped '
               'from whatever the queue happened to contain. Rare categories need either much '
               'heavier sampling or much wider stated intervals, and an honest report says '
               'which. That same sample is also your only unbiased read on what tier 1 is '
               'missing.',
             a_simple='<b>Not from the decisions the system already made &mdash; those are the '
                      'thing being graded.</b> You need a separate, honestly drawn sample: a '
                      'random selection from each category every week, two people reviewing each '
                      'item independently, disagreements settled by a third. Report your '
                      'accuracy against that, with a stated margin of error. The part people '
                      'forget is that the rare categories are the hard ones: a random sample '
                      'contains almost none of them, so you either sample far more heavily there '
                      'or admit your figure for that category has a very wide margin.'),
    ],
    anchor=dict(
        formula=r'$0.015 \times 50\text{M} \times 10\,\text{s} \div (3600 \times 8) \approx 260\ \text{reviewers}$',
        formula_simple='One or two posts in every hundred reach a person. At ten seconds a review '
                       'that is somewhere between a hundred and seventy-five and three hundred '
                       'and fifty full-time reviewers &mdash; and that headcount is what every '
                       'threshold above it is really setting.',
        bullets=[
            'The cascade exists because of arithmetic, not elegance &mdash; say the bill you avoided',
            'Human capacity is an input to the thresholds, never an output of them',
            'Rates hide counts: 0.8% of 50M posts is 400,000 people a day',
            'A policy change is a model change &mdash; new eval run, new baseline, every week',
        ]),
    chips=['confidence bands', 'human review capacity', 'hash matching',
           'random-sample holdout', 'per-category thresholds'],
    followup='Your false positive rate is 0.8%, comfortably under the 1% target. Users are furious. Why?',
),
dict(
    id='genai-gateway',
    tier='production',
    title='Design: a multi-tenant GenAI gateway',
    kicker='25 QPS peak &mdash; a governance problem wearing a scale problem&rsquo;s clothes, and the routing policy is worth &#36;140K a month',
    simple=[
        'Thirty teams inside one company are each calling model providers with their own keys, '
        'their own prompts and their own line on the credit card. The platform layer you are '
        'asked to design sits between them and the providers, and the first thing to notice is '
        'how little traffic there is. Sixteen million queries a month is six a second on '
        'average and about twenty-five in the busiest minute &mdash; one stateless proxy on a '
        'handful of machines carries that comfortably. So the interview is not about throughput '
        'at all. It is about governance: who may call what, with which data, at whose expense.',
        'What the gateway gives each team has to be worth more than what it takes. It speaks '
        'the interface everybody already writes against, so existing tools keep working '
        'untouched. It strips personal data on the way out and puts it back on the way in, so '
        'no team has to get that right alone. It remembers the shared opening of every prompt, '
        'which is a large slice off the bill, because re-reading remembered text costs about a '
        'tenth of reading it fresh. It picks a cheaper model for requests that do not need an '
        'expensive one. And it fails over to a second provider when the first is down. Those '
        'are features, not taxes, and that is the only reason anybody uses it instead of going '
        'round it.',
        'Two things will hurt you. Sharing a cache across teams is the first: if one team is '
        'served another team&rsquo;s answer because the questions looked alike, that is a data '
        'incident, not a saving &mdash; every cache key carries the team and the permissions, or '
        'the sharing stays off. The second is model versions. Providers retire models and '
        'quietly repoint the familiar names, so a team that pinned nothing wakes to different '
        'behaviour with no deployment of its own to blame. Pin the version per use case, make an '
        'upgrade something a team opts into after its own tests, and publish a retirement date '
        'with a dashboard of who has not moved.',
    ],
    analogy=('<b>Like a corporate travel desk.</b> Nobody is forced to use it. People use it '
             'because it holds the negotiated rates, it knows which countries need a visa, and '
             'it rebooks you when the airline cancels at midnight. The moment it becomes slower '
             'than booking yourself, everyone books themselves, and the company loses the audit '
             'trail along with the discount.'),
    trap_simple=('Saying &ldquo;we would shard the gateway and put a load balancer in front of '
                 'it&rdquo;. At twenty-five requests a second, that sentence tells the '
                 'interviewer you read the words &ldquo;thirty teams, enterprise&rdquo; and '
                 'reached for a distributed system nobody needs. The other one is offering a '
                 'shared cache as a pure win. Sharing the standing instructions everybody sends '
                 'is safe and valuable; sharing whole answers between teams is a leak, and the '
                 'fix is to key the cache by team and by permissions, or leave it off until '
                 'somebody asks for it.'),
    tech=[
        'Read the prompt correctly and say so in the first minute. 16M queries/month is '
        '<b>~6 QPS average, ~25 QPS peak</b> across ~30 teams and 60+ use cases &mdash; a '
        'stateless Go proxy on a handful of instances. Anyone who spends this interview on '
        'sharding has misread it; the drivers are governance, cost attribution, and not blocking '
        'thirty teams. The scale is in the money. 16M queries at ~3,000 input and 400 output '
        'tokens is <b>48B input and 6.4B output a month</b>: at mid-tier '
        '&#36;2/&#36;10 that is <b>~&#36;160K/month</b>, on a small-model mix at '
        '&#36;0.20/&#36;1.25 it is <b>~&#36;17.6K/month</b>. The routing policy is worth roughly '
        '<b>&#36;140K a month</b> &mdash; the business case for the platform, in one line.',
        'The path, in order. Client SDKs in Go, Java and Python &rarr; the gateway, exposing an '
        '<b>OpenAI-compatible HTTP/JSON interface</b> deliberately, so LangChain and LlamaIndex '
        'keep working unmodified &mdash; Uber&rsquo;s stated choice, and an adoption argument, '
        'not a shortcut &rarr; <b>auth and tenant identification</b> &rarr; a <b>policy '
        'engine</b> deciding which models this team may call, with what data classification, at '
        'what rate &rarr; <b>PII redaction</b>, outbound and inbound &rarr; the <b>prefix '
        'cache</b> &rarr; the <b>router</b>, selecting on task class, cost tier and provider '
        'health, failing over across vendors &rarr; provider adapters &rarr; the response path: '
        'un-redact, output guardrail, <b>metering</b>. Then budget your own overhead before '
        'anyone asks: auth ~2 ms, policy ~2 ms, PII classification 10&ndash;30 ms, routing ~1 '
        'ms, logging async &mdash; <b>under 50 ms added p95</b>. An unbudgeted proxy becomes the '
        'thing everyone blames.',
        'Off the request path is where it earns the word platform. Per-request token and cost '
        'accounting attributed to a team <i>and</i> a use case, because chargeback needs the '
        'model recorded per request, not per team. An audit log of every prompt and response '
        'reference, content capture governed by policy rather than on by default. A <b>prompt '
        'registry</b>, so prompts are versioned artefacts rather than strings in a repository, '
        'and a <b>model catalogue</b> with per-model eval results so teams choose on evidence. '
        'Per-team quota and budget enforcement, with a circuit breaker at <b>3&times; the '
        'rolling hourly average</b>. And the lever that only exists centrally: at 40% shared '
        'system prompts and cached reads billing at ~10% of the input rate, prefix caching is a '
        '<b>36% cut in input spend, ~&#36;35K/month</b> &mdash; captured once, not '
        'reimplemented thirty times badly.',
        'Failure modes. <b>The gateway is a single point of failure</b> and thirty teams go down '
        'together: stateless, multi-region, generous timeouts, and a break-glass path that lets '
        'a critical service bypass it during an incident &mdash; designed before you are asked. '
        '<b>Vendor outage</b>: router-level failover to a second vendor or to self-hosted, with '
        'a quality note in the response metadata so teams react rather than silently degrade. '
        '<b>Redaction misses</b>: redaction is a classifier, so layer it &mdash; schema-aware '
        'rules where the data model is known, plus a policy keeping the most sensitive '
        'categories off vendor APIs entirely. And <b>silent change on deprecation</b>: pin '
        'versions per use case, gate upgrades on the team&rsquo;s own eval suite, never on a '
        'vendor-side alias change you learn about from a support ticket.',
    ],
    tech_note=('The traceable numbers here are Uber&rsquo;s, published July 2024: 16M '
               'queries/month, ~25 QPS peak, ~30 teams, 60+ use cases, a Go proxy with an '
               'OpenAI-compatible interface and PII redaction inside it. The spend figures, the '
               'caching saving and the 50 ms latency budget are <i>arithmetic</i> on top of '
               'those, using published per-million token prices and a stated 40% prefix-sharing '
               'assumption. Hedge that 40% honestly: it is an assumption, it dominates the '
               'caching answer, and measuring whether it holds is week one of the job.'),
    fig=dict(
        kind='blocks', h=262,
        boxes=[
            dict(x=16,  y=46, w=100, h=58, t='client SDKs', sub='OpenAI-shaped'),
            dict(x=135, y=46, w=124, h=58, t='auth + policy', sub='tenant, model, rate', tone='sig'),
            dict(x=278, y=46, w=108, h=58, t='PII redact', sub='10-30 ms', tone='sig'),
            dict(x=405, y=46, w=132, h=58, t='cache + router', sub='prefix, cost, health', tone='mem'),
            dict(x=556, y=46, w=148, h=58, t='providers', sub='vendors + self-hosted', tone='mem'),
            dict(x=16,  y=168, w=150, h=56, t='prompt registry', sub='versioned artefacts'),
            dict(x=182, y=168, w=160, h=56, t='model catalogue', sub='per-team eval deltas', tone='mem'),
            dict(x=358, y=168, w=160, h=56, t='quota + budget', sub='breaker at 3x hourly', tone='sig'),
            dict(x=534, y=168, w=170, h=56, t='metering + audit', sub='per request, per team'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3), dict(a=3, b=4),
            dict(a=5, b=3, side='up'),
            dict(a=6, b=4, side='up'),
            dict(a=7, b=1, side='up', tone='sig'),
            dict(a=4, b=8, side='down'),
        ],
        labels=[
            dict(x=16, y=30,  t='request path, under 50 ms added', a='start'),
            dict(x=16, y=152, t='control plane', a='start'),
        ],
        foot='the traffic is small; the policy, the cache and the ledger are why the box exists',
        alt='Architecture diagram. The top row runs left to right: client SDKs call a gateway '
            'that identifies the tenant and applies policy, redacts personal data in 10 to 30 '
            'milliseconds, consults a prefix cache and a router choosing a model on cost and '
            'health, and reaches provider adapters covering vendor APIs and self-hosted serving. '
            'A second row below is the control plane: a prompt registry and a model catalogue '
            'feeding the router, a per-team quota and budget with a circuit breaker feeding the '
            'policy stage, and metering and audit receiving every response.'),
    caption=('Pink is what makes this a governance system rather than a proxy: tenant policy on '
             'the way in, redaction before anything leaves the network, and a per-team budget '
             'with a breaker on it. Teal is what makes teams want to use it &mdash; a cache and '
             'a router each of them would otherwise build badly, and a catalogue that tells them '
             'which model to pick and why. The control-plane row is the entire difference '
             'between a gateway and a load balancer.'),
    caption_simple=('The pink boxes are what makes this a control system rather than a pipe: who '
                    'may call what, personal data stripped before anything leaves the building, '
                    'and a spending limit per team with a trip switch on it. The teal boxes are '
                    'the reason teams use it instead of going round it &mdash; shared caching, '
                    'automatic failover, and a list of models with test results attached. The '
                    'bottom row is the difference between a platform and a load balancer.'),
    when_label='The interviewer is really testing',
    when=[
        'Whether you notice 25 QPS is not a scale problem, and say so out loud',
        'Whether you can price the routing policy rather than assert that it saves money',
        'Whether the gateway gives teams something or only takes from them',
        'Whether you designed the break-glass path before being asked what happens when it is down',
        'Whether you know why a shared cache across tenants is a data incident',
    ],
    trap=('Saying &ldquo;we shard the gateway and put a load balancer in front of it&rdquo;. At '
          '25 QPS peak, that answer says you pattern-matched on &ldquo;thirty teams, '
          'enterprise&rdquo; and reached for a distributed system nobody needs. The second trap '
          'is the more damaging one in production: &ldquo;we cache responses centrally so every '
          'team benefits&rdquo;. Prefix caching across tenants on shared system prompts is real '
          'and safe and worth ~&#36;35K/month here; <i>semantic</i> caching across tenants is a '
          'data incident waiting for its date, because any key without a tenant and ACL '
          'component can serve one team another team&rsquo;s answer. Off by default, opted into, '
          'keyed by tenant &mdash; and never switched on platform-wide to hit a cost target.'),
    nums_label='The numbers you design against',
    nums=[
        dict(k='TENANTS', v='~30 teams', s='60+ use cases, and rising'),
        dict(k='TRAFFIC', v='25 QPS peak', s='16M queries/month, ~6 QPS average'),
        dict(k='ADDED LATENCY', v='under 50 ms p95', s='PII classification is 10&ndash;30 ms of it'),
        dict(k='SPEND, MID-TIER', v='~&#36;160K/month', s='48B input and 6.4B output tokens'),
        dict(k='SPEND, SMALL MIX', v='~&#36;17.6K/month', s='the routing policy is worth ~&#36;140K'),
        dict(k='CIRCUIT BREAKER', v='3&times; rolling hourly', s='per team &mdash; a runaway loop costs &#36;50&ndash;500 before anyone notices'),
    ],
    ask=[
        dict(q='How many teams, and how many use cases?',
             a='~30 teams and 60+ use cases, and rising. That is what makes this a platform rather than a library.'),
        dict(q='What is the aggregate traffic?',
             a='Single-digit QPS average, tens at peak. Ask early, because it deletes half the answer most people arrive with.'),
        dict(q='What is actually driving this &mdash; cost, safety or velocity?',
             a='Governance and safety first, cost second. Ask, because it decides which half of the design you spend the hour on.'),
        dict(q='Self-hosted models, vendor APIs, or both?',
             a='Both. Which means a uniform adapter layer and a health signal per provider, not one vendor SDK.'),
        dict(q='Is PII allowed to leave the network?',
             a='No. This is usually the hard constraint, and it decides where redaction lives.'),
        dict(q='Do teams bring their own prompts and models?',
             a='Yes &mdash; and the platform must not become a bottleneck on their iteration. A prompt registry, not a review board.'),
        dict(q='Who pays?',
             a='Chargeback per team, which requires per-request cost attribution and therefore the model recorded per request.'),
    ],
    estimate=dict(
        label='The arithmetic, out loud',
        cost='published prices, derived totals',
        rows=[
            dict(l='traffic', w='16M / 2.59M s per month', r='~6 QPS, ~25 peak'),
            dict(l='input tokens', w='16M x 3,000', r='48B/month'),
            dict(l='output tokens', w='16M x 400', r='6.4B/month'),
            dict(l='mid-tier bill', w='48B at &#36;2/M plus 6.4B at &#36;10/M', r='~&#36;160K/month'),
            dict(l='small-model mix', w='48B at &#36;0.20/M plus 6.4B at &#36;1.25/M', r='~&#36;17.6K/month'),
            dict(l='prefix cache, mid-tier', w='40% of input at 10% of rate', r='~&#36;35K/month'),
            dict(l='what routing alone is worth', w='&#36;160K minus &#36;17.6K', r='~&#36;140K/month', tot=True),
        ],
        note='Do not add the last two rows together. The ~&#36;35K caching saving is computed '
             'against mid-tier input spend, so routing traffic to cheaper models shrinks it '
             '&mdash; the levers overlap, and a candidate who sums them has just announced that '
             'they do not check their own arithmetic. Quote them as two independent estimates of '
             'the same order, and say plainly that the 40% prefix-sharing figure is an '
             'assumption the whole caching number rests on.'),
    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='THIN PROXY VS PLATFORM',
             v='<b>Make the paved path cheaper and faster than the alternative.</b> A thin proxy '
               'gets adopted and enforces nothing; an opinionated platform enforces a lot and '
               'gets routed around. The resolution is self-interest, not mandate: free caching, '
               'free observability, free failover. That sentence separates people who have run a '
               'platform from people who have drawn one.'),
        dict(k='CENTRAL LIMITS VS AUTONOMY',
             v='<b>Both, plus a priority class.</b> Global limits protect the vendor '
               'relationship; per-team quotas protect teams from each other. Neither stops an '
               'experimental batch job starving a customer-facing product at 4pm, which is '
               'exactly what the priority class is for.'),
        dict(k='WHERE PII REDACTION LIVES',
             v='<b>In the gateway, and name what it costs.</b> There it is uniform and cheap to '
               'audit, and it adds 10&ndash;30 ms to every request and cannot use application '
               'context. In the application it is precise and inconsistently implemented. Uber '
               'put it in the proxy; the signal is arguing the trade rather than assuming it.'),
        dict(k='CACHING ACROSS TENANTS',
             v='<b>Prefix yes, semantic no.</b> Central prefix caching on shared system prompts '
               'is a large uniform win, ~&#36;35K/month here. Central semantic caching across '
               'tenants is a leak unless every key carries a tenant and an ACL &mdash; off by '
               'default, opted into, and never a platform-wide switch someone flips to hit a '
               'budget.'),
        dict(k='VENDOR LOCK-IN VS ADAPTERS',
             v='<b>OpenAI-shaped for everything, plus a passthrough.</b> One interface across all '
               'providers is the pragmatic choice and it does flatten vendor-specific features. '
               'Expose a raw passthrough for the teams that genuinely need them instead of '
               'pretending the abstraction is lossless.'),
        dict(k='BUILD VS BUY',
             v='<b>Say which constraint decides it.</b> At 25 QPS the engineering cost is '
               'dominated by governance requirements, not traffic. If the PII and audit '
               'requirements are satisfiable off the shelf, buy. If data residency forbids it, '
               'build. Answering &ldquo;build, obviously&rdquo; at this scale is the same misread '
               'as sharding.'),
    ],
    verdict=dict(
        no='Designs a high-throughput distributed system for 25 QPS. Treats the gateway as a '
           'pass-through proxy with a rate limiter bolted on. Has no cost attribution, so '
           'chargeback is impossible. Has no prompt versioning, so nobody can say what changed. '
           'And has no answer at all for what happens when the gateway itself is down.',
        yes='Reads the prompt as governance rather than scale, and says so in the first minute. '
            'Makes the interface OpenAI-compatible for a stated adoption reason. Puts PII '
            'redaction in the proxy and argues the tradeoff instead of assuming it. Computes the '
            'routing and caching savings so the platform&rsquo;s existence carries a number. '
            'Pins model versions per use case. And designs the break-glass path before being '
            'asked what happens when it fails.'),
    real_label='The anchor system, with published numbers',
    real=('Uber&rsquo;s GenAI Gateway, published July 2024, is a Go service acting as an '
          'encompassing layer around third-party vendor clients, deliberately exposing an '
          'OpenAI-compatible interface so existing tooling works unmodified. The published '
          'figures: <b>16M queries a month, ~25 QPS peak, ~30 teams, 60+ use cases</b>, with PII '
          'redaction and un-redaction inside the proxy itself. It is the best public evidence '
          'that an enterprise GenAI platform is a governance artefact running at single-digit '
          'QPS &mdash; and it is the number to quote the moment somebody starts sizing a '
          'cluster.'),
    math=dict(
        tex=r'\text{cost}_{\text{team}} = \sum_{r} \bigl( t^{\text{in}}_{r}\, p^{\text{in}}_{m(r)}'
            r' + 0.1\, t^{\text{cached}}_{r}\, p^{\text{in}}_{m(r)}'
            r' + t^{\text{out}}_{r}\, p^{\text{out}}_{m(r)} \bigr)',
        note=r'What it does not say: $m(r)$ is chosen by <i>your</i> router, not by the team. '
             r'The moment routing policy changes, every team&rsquo;s bill changes without them '
             r'shipping anything &mdash; which is why the model has to be recorded per request, '
             r'why chargeback needs a stated policy version attached to it, and why a routing '
             r'change is a communication before it is a config push.',
        cost='per request, per team'),
    drills=[
        dict(q='A team says the gateway is too slow and wants to bypass it. What do you do?',
             a='<b>Measure first, and produce the gateway&rsquo;s own added-latency p95 against '
               'the budget you published.</b> If it is over 50 ms, fix it &mdash; it is almost '
               'always PII classification on the synchronous path or a log write that should be '
               'async. If it is under, the complaint is about the model and the gateway is being '
               'blamed for physics; show the span breakdown from the trace rather than arguing '
               'about it. Then give the structural answer, which is what is really being tested: '
               'teams bypass platforms that only take. The gateway has to give &mdash; free '
               'prefix caching, free failover, per-request cost data they cannot get anywhere '
               'else &mdash; so that bypassing it is irrational rather than forbidden. A mandate '
               'produces a shadow gateway within six months.',
             a_simple='<b>Measure before you argue.</b> Publish how much delay the gateway '
                      'itself adds and hold it against the budget you promised. If it is over, '
                      'fix it &mdash; it is nearly always the personal-data scan running in line '
                      'with the request, or an audit record being written while the request '
                      'waits instead of afterwards. If it is under, the slowness is the model '
                      'rather than you, and you show them '
                      'the timings instead of debating. Then fix the real problem: people go '
                      'round a platform that only takes things from them. Give them shared '
                      'caching, automatic failover and a per-request bill they cannot get '
                      'anywhere else, and going round stops being worth the effort. Banning it '
                      'just produces a second gateway somebody built in secret.'),
        dict(q='How do you roll out a new model version safely across thirty teams?',
             a='<b>Never globally, and never as a vendor-side alias change.</b> Add it to the '
               'catalogue as a new pinned version. Run it in shadow against sampled production '
               'traffic <i>per use case</i> &mdash; per use case, because a change that improves '
               'summarisation can wreck structured extraction, and an aggregate hides that '
               'completely. Publish per-team eval deltas from the eval harness so each team sees '
               'its own numbers. Let teams opt in with a one-line config change and roll back '
               'the same way. Then deprecate the old version on a published timeline with a '
               'usage dashboard showing exactly who has not migrated &mdash; because the '
               'migration you are not tracking is the one still running the morning the provider '
               'turns the old model off.',
             a_simple='<b>Never all at once, and never because the provider quietly repointed a '
                      'name.</b> Add the new version to the catalogue alongside the old one. Run '
                      'it silently against a sample of real traffic for each separate use case, '
                      'because a change that improves summaries can ruin form-filling and an '
                      'average across everything hides it. Give each team its own before-and-'
                      'after scores rather than a company figure. Let them switch on with one '
                      'line of config and switch back the same way. Then set a retirement date '
                      'for the old version and keep a dashboard of who has not moved &mdash; the '
                      'team you are not tracking is the one still on it the morning it '
                      'disappears.'),
        dict(q='Finance wants to cut LLM spend 40%. What levers do you have that the teams do not?',
             a='<b>Three that only exist centrally, and you can price two on the spot.</b> '
               'Cross-team prefix caching on shared system prompts and tool schemas: at 40% '
               'shared input and cached reads at ~10% of the input rate, a 36% cut in input '
               'spend, ~&#36;35K/month. A routing policy that moves whole <i>classes</i> of '
               'traffic to cheaper models on measured quality rather than each team guessing '
               '&mdash; the gap between the mid-tier and small-model mixes here is ~&#36;160K '
               'against ~&#36;17.6K. And batch-mode conversion at 50% off for everything not '
               'user-facing, which individual teams never bother to set up. Then the caveat, '
               'which is the part that reads as senior: the first two overlap, so you do not add '
               'them, and the 40% sharing figure is the assumption the whole caching estimate '
               'rests on.',
             a_simple='<b>Three levers, and only a platform can pull them.</b> The shared '
                      'opening of every prompt &mdash; the standing instructions thirty teams '
                      'all send &mdash; gets remembered once, centrally, and re-reading '
                      'remembered text costs about a tenth of reading it fresh: roughly a third '
                      'off the input bill on its own. Whole categories of request move to a '
                      'cheaper model on measured quality rather than each team guessing, and the '
                      'gap between the expensive and cheap mixes here is close to ten to one. '
                      'And anything that is not a person waiting for an answer goes into the '
                      'overnight queue at half price, which no individual team sets up. The '
                      'honest caveat: the first two overlap, so you cannot add the savings '
                      'together.'),
    ],
    anchor=dict(
        formula=r'$6\ \text{QPS} \Rightarrow \text{governance} \qquad 48\text{B tokens} \Rightarrow \text{the bill}$'
                r' &nbsp;&middot;&nbsp; ~&#36;160K or ~&#36;17.6K, your choice',
        formula_simple='Six requests a second is not a scale problem. Forty-eight billion input '
                       'tokens a month is a bill of about a hundred and sixty thousand dollars, '
                       'or seventeen and a half thousand if the router sends the easy work to a '
                       'cheap model. The routing policy, not the proxy, is the platform.',
        bullets=[
            '25 QPS is not a scale problem &mdash; say so before you draw anything',
            'The platform must give more than it takes, or teams route around it',
            'Pin model versions per use case: a vendor alias change is a deployment you did not make',
            'Any cache key without a tenant and an ACL in it is a data incident waiting for its date',
        ]),
    chips=['OpenAI-compatible interface', 'PII redaction in the proxy', 'prefix caching',
           'per-tenant quota', 'model version pinning'],
    followup='A team says the gateway is too slow and wants to bypass it. What do you do?',
)]
