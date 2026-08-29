CARDS = [dict(
    id='fraud-realtime',
    tier='production',
    title='Design: fraud scoring inside the authorisation path',
    kicker='You are inside someone else&rsquo;s hundred-millisecond timeout, and the budget deletes most of the feature ideas before anyone proposes them',

    # ---------------- SIMPLE LAYER ----------------
    simple=[
        'A card payment is waiting for an answer. The whole authorisation round trip is about a '
        'tenth of a second, and fraud scoring gets somewhere between ten and fifty milliseconds '
        'of that &mdash; a slice of a window you do not own. That single fact settles most of the '
        'design before anyone opens a modelling discussion. Anything you cannot fetch, assemble '
        'and run inside fifty milliseconds is not a feature, however predictive it would be. So '
        'the work moves earlier: counts per card, per device, per shipping address are maintained '
        'continuously as payments arrive and held in memory, so that at decision time the system '
        'reads a number rather than computing one.',
        'Then comes the arithmetic that decides the product rather than the model. About one '
        'payment in a thousand is fraud. A system that wrongly blocks one in a thousand good '
        'payments is, at five thousand payments a second, turning away roughly five honest '
        'customers every second &mdash; which is about the same number of frauds there are to '
        'catch in that second. Those two numbers side by side, not the choice of architecture, '
        'are the argument you are actually having.',
        'And the answers arrive late. You learn a payment was fraud when the cardholder disputes '
        'it, thirty to ninety days later, and you never learn anything about the ones you '
        'declined, because they did not happen. So the training data is written by the model you '
        'already deployed, and accuracy is a thing you cannot measure for two months. Everything '
        'in this design that looks paranoid &mdash; a rules path kept warm and fed real traffic, '
        'a record of the exact numbers the model saw, a small slice of risky payments approved on '
        'purpose so you can watch what happens &mdash; exists because of that delay.',
    ],
    analogy=('<b>Like a bouncer with a two-second look.</b> He cannot run a background check while '
             'the queue waits, so everything useful has to already be on the clipboard he is '
             'holding: who came in tonight, which card was trouble last month. And he finds out '
             'he was wrong about someone weeks later, from someone else, long after the door '
             'closed behind them.'),
    trap_simple=('Saying you will fetch the thousand things the model needs when the payment '
                 'arrives. That is a thousand separate lookups per payment, five million a second '
                 'across the traffic, and it is the design that actually fails &mdash; not '
                 'because the store is slow, but because you asked it a thousand questions '
                 'instead of one. The other one is treating a blocked good customer and a missed '
                 'fraud as the same size of mistake. They are not the same size, and they are not '
                 'even on the same clock: the customer leaves today, the fraud turns up as a '
                 'dispute in two months.'),

    # ---------------- TECHNICAL LAYER ----------------
    tech=[
        'Spend the budget before you choose a model. The authorisation window is ~100 ms end to '
        'end and fraud scoring gets <b>10&ndash;50 ms</b> of it. Allocate it out loud: ~10 ms of '
        'network, ~10 ms for one batched feature read, 10&ndash;20 ms of inference, ~2 ms of '
        'rules and ~10 ms for the decision, the log write and headroom. That totals '
        '<b>42&ndash;52 ms</b> against a 50 ms slice, which is the point &mdash; there is no room '
        'for a network hop to a Python service, a second model, or anything that reads a '
        'relational database. The model is compiled and runs in-process or as a sidecar, and on '
        'timeout the request takes the rules-only path and is approved with monitoring. A late '
        'model is no model.',
        'The feature fetch is where naive designs die. 1,000 features at 5,000 TPS is '
        '$5{,}000 \\times 1{,}000 = 5\\text{M}$ feature reads per second. A 20-node Redis cluster '
        'is reported to sustain 100M ops/s at sub-millisecond latency, so the capacity is there '
        'with an order of magnitude spare &mdash; but only if that is one batched pipeline per '
        'transaction over pre-aggregated values, never 1,000 individual GETs. Say the batching '
        'constraint out loud; the naive version is the actual failure. Velocity features '
        'are per-entity sliding windows &mdash; sorted sets keyed by card, device, IP, email and '
        'shipping address, written with a timestamp score and trimmed on read &mdash; and '
        'distinct counts come from HyperLogLog at ~12 KB with under 1% standard error.',
        'The path, in order: decision service holding the deadline &rarr; parallel online feature '
        'read and request-derived features (amount, MCC, geo, BIN) &rarr; feature assembly '
        '<i>through the same code path used offline</i> &rarr; model &rarr; rules engine for hard '
        'blocks, allowlists and regulatory holds &rarr; decision with reason codes. '
        'Asynchronously, every scored transaction and its exact feature vector goes to a decision '
        'log. Chargebacks and manual-review outcomes arrive weeks later and join to that log on '
        'transaction ID; that join <i>is</i> the training set. A feature definition registry '
        'materialises each feature to both the offline table and the online store, and shadow '
        'scoring runs the candidate on live traffic without acting on it.',
        'Failure modes, named before you are asked. <b>Training&ndash;serving skew</b>: the '
        'offline pipeline computes a feature one way and the online store another &mdash; fix it '
        'structurally with one definition and two materialisations, plus a continuous audit that '
        're-scores sampled live traffic offline and diffs the vectors. <b>Time travel</b>: '
        'joining features as of label time rather than decision time produces a model that is '
        'excellent offline and useless online. <b>Censored labels</b>: you never observe the '
        'outcome of a transaction you declined, so a small randomised approve-and-monitor holdout '
        'is the only honest way to keep the label distribution unbiased. '
        '<b>Adversarial drift</b>: patterns change <i>because</i> you deployed, so monitor feature '
        'and score distributions rather than accuracy, which is unmeasurable for 60 days. '
        '<b>The fallback rotting</b>: keep a small always-on percentage of traffic on the '
        'rules-only path so you do not discover it broken during an incident. '
        '<b>Explainability</b>: reason codes are an output of the model, not a post-hoc addition.',
    ],
    tech_note=('Separate what is published from what you just computed. Stripe&rsquo;s '
               'under-100 ms decision, its 1,000+ characteristics per transaction and its 0.1% '
               'block rate are published. The 10&ndash;50 ms scoring envelope, the 100M ops/s '
               'Redis figure and the card-network 500-attributes-in-1-ms number are vendor '
               'reports rather than anything you measured, so say &ldquo;reported&rdquo;. The '
               '42&ndash;52 ms allocation, the 5M reads per second, the ~432,000 good payments a '
               'day and the ~1B transactions needed to collect 1M fraud examples are arithmetic '
               'you did in the room. The 5:1 false-positive-to-true-positive figure is a stated '
               'target, not a measurement of anything.'),

    # ---------------- FIGURE ----------------
    fig=dict(
        kind='blocks', h=310,
        boxes=[
            dict(x=16,  y=44,  w=92,  h=48, t='auth request', sub='5,000 TPS'),
            dict(x=120, y=44,  w=126, h=48, t='decision service', sub='50 ms, hard', tone='sig'),
            dict(x=258, y=44,  w=118, h=48, t='feature assembly', sub='one code path', tone='mem'),
            dict(x=388, y=44,  w=104, h=48, t='model', sub='10-20 ms', tone='mem'),
            dict(x=504, y=44,  w=88,  h=48, t='rules', sub='2 ms floor'),
            dict(x=604, y=44,  w=100, h=48, t='decision', sub='and reason codes', tone='mem'),
            dict(x=16,  y=136, w=170, h=46, t='online feature store', sub='5M reads/s, batched', tone='mem'),
            dict(x=214, y=136, w=160, h=46, t='rules-only fallback', sub='on timeout, 1% always on', dash='4 3'),
            dict(x=394, y=136, w=146, h=46, t='shadow score', sub='live, acts on nothing', tone='mem'),
            dict(x=560, y=136, w=144, h=46, t='decision log', sub='the exact vector'),
            dict(x=16,  y=234, w=124, h=48, t='chargebacks', sub='30 to 90 days', tone='sig'),
            dict(x=156, y=234, w=134, h=48, t='join on txn id', sub='point-in-time'),
            dict(x=306, y=234, w=124, h=48, t='training set', sub='1B txns, 1M frauds'),
            dict(x=446, y=234, w=112, h=48, t='retrain', sub='under 2 hours'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3), dict(a=3, b=4), dict(a=4, b=5),
            dict(a=6, b=2, side='up'),
            dict(a=1, b=7, side='down', tone='sig', dash='4 3'),
            dict(a=7, b=5, side='up', dash='4 3'),
            dict(a=5, b=9, side='down'),
            dict(a=9, b=11, side='down'),
            dict(a=10, b=11), dict(a=11, b=12), dict(a=12, b=13),
            dict(a=13, b=8, side='up'),
            dict(a=8, b=3, side='up', dash='4 3'),
        ],
        labels=[
            dict(x=16, y=22, t='REQUEST PATH, 50 MS HARD', a='start'),
            dict(x=16, y=122, t='WHAT FEEDS IT', a='start'),
            dict(x=16, y=214, t='OFFLINE, AND THE LABELS ARE LATE', a='start'),
        ],
        foot='two clocks you do not own: fifty milliseconds one way, sixty days the other',
        alt=('Architecture diagram in three rows. The top row is the request path under a hard '
             'fifty-millisecond deadline: an authorisation request enters a decision service, '
             'features are assembled through one shared code path, a compiled model scores, a '
             'rules engine applies hard blocks, and a decision leaves with reason codes. A middle '
             'row holds the online feature store that feeds assembly, a dashed rules-only '
             'fallback taken on timeout, a shadow scorer that acts on nothing, and the decision '
             'log. The bottom row is offline: chargebacks arriving thirty to ninety days later '
             'join the decision log on transaction ID to build the training set, which retrains '
             'the model into the shadow scorer.')),
    caption=('The pink boxes are the two clocks you do not control: a hard 50 ms on the way in, '
             'and 30 to 90 days before you learn whether the decision was right. Everything teal '
             'is what carries the answer &mdash; one batched read of pre-aggregated features, one '
             'assembly path shared with training, a compiled model. The dashed box is what runs '
             'when the deadline is missed, which is why it needs live traffic on it every day '
             'rather than a unit test.'),
    caption_simple=('The pink boxes are the two clocks you do not control: fifty milliseconds to '
                    'answer, and up to three months before you find out whether you were right. '
                    'The teal boxes are the ones that produce the decision. The dashed box is '
                    'what runs when the clock beats you, and it only works if you keep a little '
                    'traffic on it every day.'),

    # ---------------- SHARED ----------------
    when_label='The interviewer is really testing',
    when=[
        'Whether you ask for the latency budget before you name a model',
        'Whether you notice that a thousand features per transaction is five million reads a second',
        'Whether you can price a blocked customer against a missed fraud in the same sentence',
        'Whether label delay changes your architecture or only your retraining schedule',
    ],
    trap=('Saying &ldquo;we fetch the features the model needs at scoring time&rdquo;. At 1,000 '
          'features and 5,000 TPS that is five million reads a second arriving as a thousand '
          'separate round trips per transaction, and it is the design that actually fails &mdash; '
          'not because the store is slow, but because you asked it a thousand questions instead '
          'of one. The second version, and the one interviewers press harder: &ldquo;we retrain '
          'nightly on the latest labels&rdquo;. There are no latest labels. Chargebacks arrive 30 '
          'to 90 days later, so a nightly retrain is a nightly refit on two-month-old outcomes. '
          'The only signals that move faster are proxies &mdash; manual review outcomes and '
          'step-up failures &mdash; and they are biased by the decisions your current model '
          'already made.'),

    nums_label='The numbers you design against',
    nums=[
        dict(k='PEAK LOAD', v='5,000 TPS', s='authorisations, and every one is blocking'),
        dict(k='YOUR SLICE', v='10&ndash;50 ms', s='inside a ~100 ms authorisation window'),
        dict(k='BASE RATE', v='~1 in 1,000', s='so 1M fraud examples needs ~1B transactions'),
        dict(k='FEATURES', v='1,000+', s='per transaction &mdash; which is 5M reads a second'),
        dict(k='LABEL DELAY', v='30&ndash;90 days', s='chargebacks; some fraud is never labelled at all'),
        dict(k='FALSE POSITIVES', v='0.1%', s='~432,000 good payments a day at this volume'),
    ],

    ask=[
        dict(q='What is the latency budget, and is it hard or soft?',
             a='Hard. The authorisation window is ~100 ms and fraud scoring gets 10&ndash;50 ms of it. Ask first; it deletes half the ideas in the room.'),
        dict(q='What happens if we time out?',
             a='Fall back to rules and approve with monitoring. A late model is no model, so the fallback is a designed path rather than an error handler.'),
        dict(q='What is the fraud base rate?',
             a='Roughly 1 in 1,000 payments. It sets the class imbalance and how much traffic you need before you have labels worth training on.'),
        dict(q='What does a false positive cost against a false negative?',
             a='A blocked good customer costs more in lifetime value than most single frauds. That ratio sets the threshold, not your taste in metrics.'),
        dict(q='When do labels arrive?',
             a='Chargebacks 30&ndash;90 days later, and some fraud is never labelled. This is the constraint the rest of the design bends around.'),
        dict(q='What is peak throughput?',
             a='~5,000 TPS. Multiply it by your feature count before you say anything at all about a feature store.'),
        dict(q='Is there a human review queue?',
             a='Yes, for a step-up and manual band. That gives you a third action besides approve and decline, and it is where the cost asymmetry gets managed.'),
        dict(q='Do decisions have to be explainable?',
             a='Yes, to merchants and to regulators. Reason codes are an output of the model, not something bolted on after the fact.'),
    ],

    estimate=dict(
        label='Spending the fifty milliseconds', cost='derived against a sourced envelope',
        rows=[
            dict(l='your slice', w='~100 ms window, minus everything else', r='10&ndash;50 ms'),
            dict(l='network in and out', w='two hops you do not control', r='~10 ms'),
            dict(l='feature reads per second', w='5,000 TPS x 1,000 features', r='5M reads/s'),
            dict(l='feature fetch', w='one batched pipeline, not 1,000 GETs', r='~10 ms'),
            dict(l='inference', w='compiled, in-process, no network hop', r='10&ndash;20 ms'),
            dict(l='rules engine', w='hard blocks, allowlists, regulatory', r='~2 ms'),
            dict(l='decide, log, headroom', w='reason codes and the decision log write', r='~10 ms'),
            dict(l='spent', w='against a 50 ms slice', r='42&ndash;52 ms', tot=True),
        ],
        note=('The total is the argument. There is nothing left over, which is why the model is '
              'compiled and in-process, why the features are pre-aggregated, and why a language '
              'model in this path is not a cost question but an arithmetic one. The 5M-reads row '
              'is the one that kills naive designs: the capacity exists, the round trips do '
              'not.')),

    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='MODEL VS BUDGET',
             v='<b>Whatever you pick is compiled and in-process.</b> A gradient-boosted ensemble '
               'is fast, strong on tabular features and explainable; a DNN captures interactions '
               'better and is where Stripe went in 2022. Argue from the budget rather than from '
               'taste &mdash; 10&ndash;20 ms with no network hop is the requirement, and either '
               'family can meet it or miss it depending on how you deploy it.'),
        dict(k='FEATURES VS FETCH',
             v='<b>Features earn their place by lift per millisecond.</b> A thousand of them is '
               'achievable only as pre-aggregated values read in one batched pipeline. If a '
               'feature cannot be maintained as a rolling aggregate, it is an offline feature '
               '&mdash; and it belongs in the training set only if you can also serve it, or you '
               'have built skew on purpose.'),
        dict(k='THRESHOLD IS ECONOMICS',
             v='<b>Not a modelling preference.</b> Compute the expected cost of each error type '
               'and set the threshold there. Then say the part people miss: the two errors run on '
               'different clocks. A false positive costs lifetime value today; a false negative '
               'costs a chargeback in 60 days. A mature card programme aims at a '
               'false-positive-to-true-positive ratio near 5:1 or better, which is a target '
               'rather than a measurement.'),
        dict(k='RULES AND MODEL',
             v='<b>Ship both, and keep traffic on the fallback.</b> Rules are instant, auditable '
               'and brittle; the model is accurate and opaque. Rules are the hard floor and the '
               'timeout path, the model is the scorer, and a small always-on percentage keeps the '
               'fallback exercised so nobody discovers it broken during an incident.'),
        dict(k='RETRAIN VS LABEL DELAY',
             v='<b>You cannot retrain meaningfully faster than labels arrive.</b> Proxy labels '
               '&mdash; manual review outcomes, step-up failures &mdash; shorten the loop and are '
               'biased by the decisions the current model made, so say that when you propose '
               'them. A weekly cadence on 60-day-old chargebacks is honest; a nightly one is '
               'theatre.'),
        dict(k='ONE MODEL VS PER-SEGMENT',
             v='<b>One model with segment features to start.</b> Per-segment models fit better '
               'and multiply the monitoring and retraining burden by the number of segments, each '
               'with its own label delay. Split only when a segment has enough labelled volume to '
               'be monitored on its own.'),
    ],

    verdict=dict(
        no='Designs an offline batch scoring pipeline and notices the latency constraint only '
           'when prompted. Proposes a thousand individual feature lookups. Treats labels as if '
           'they arrive with the transaction. Never prices a false positive against a false '
           'negative. Suggests a language model in the authorisation path.',
        yes='Opens by asking for the latency budget and the cost of each error type. Allocates '
            'the 50 ms out loud and lands at 42&ndash;52. Catches the five-million-reads-a-second '
            'problem and names batching as the fix. Calls label delay the defining constraint of '
            'the whole design rather than a retraining detail. Describes point-in-time '
            'correctness without being asked. Designs the rules fallback as a first-class path '
            'with real traffic on it.'),

    real_label='Where the numbers come from',
    real=('Stripe Radar decides in under 100 ms using more than 1,000 characteristics per '
          'transaction. In mid-2022 it replaced a Wide-and-Deep ensemble of XGBoost and a DNN '
          'with a single ResNeXt-inspired network, cutting training time by more than 85% to '
          'under two hours while training on 10&times; the data &mdash; the retraining loop, not '
          'the score, was the rebuild. The number to carry is the error one: Radar '
          '&ldquo;incorrectly blocks just 0.1%&rdquo; of legitimate payments. At this '
          'design&rsquo;s 5,000 TPS that is about five good customers turned away every second, '
          'roughly 432,000 a day.'),

    math=dict(
        tex=r'\underbrace{0.001 \times 5{,}000/\text{s}}_{\text{5 good payments declined}} '
            r'\quad \text{against} \quad '
            r'\underbrace{0.001 \times 5{,}000/\text{s}}_{\text{5 frauds available to catch}}',
        note='What it does not say: the two sides settle on different days. The left-hand five '
             'walk out today; the right-hand five come back as chargebacks in 60 days. Discount '
             'them accordingly before you quote a threshold.',
        cost='per second, at a 0.1% false-positive rate'),

    drills=[
        dict(q='Your model&rsquo;s offline AUC is 0.95 and production performance is much worse. Why?',
             a=('<b>Three candidates, ranked, and none of them is the architecture.</b> First, '
                'point-in-time leakage in the training join: features joined as of label time '
                'rather than decision time, so the model trained on values that did not exist '
                'when the decision was made. Second, feature skew &mdash; the offline pipeline '
                'and the online store compute the same named feature differently. Third, censored '
                'labels: the training set contains only transactions the current model approved, '
                'so it has never seen the fraud it already blocks. Then say how you separate '
                'them. Replay live traffic through the offline pipeline and diff the feature '
                'vectors field by field; that catches the first two in an afternoon, and if the '
                'vectors match you are left with the label problem, which needs the randomised '
                'approve-and-monitor holdout.'),
             a_simple=('<b>Three suspects, in order, and none of them is the model.</b> First, the '
                       'training data may have been built using facts that only became known '
                       'after the payment was decided, so the model learned to read the future '
                       'and cannot do it in production. Second, the same feature may be '
                       'calculated one way in the training pipeline and another way in the live '
                       'one, so the model is being fed numbers it never trained on. Third, the '
                       'training set contains only payments the current system let through, so it '
                       'has never seen the frauds it already stops. To tell them apart, take real '
                       'live traffic, push it back through the training pipeline and compare the '
                       'two sets of numbers line by line. If they match, it is the third.')),
        dict(q='A new fraud pattern appears on Monday. When do you catch it?',
             a=('<b>Not through the retraining loop &mdash; that is 30 to 60 days away.</b> '
                'Chargebacks are the only clean label and they arrive after the dispute window, '
                'so anything that waits for them responds two months late. You catch Monday '
                'through unsupervised signals: a shift in feature distributions, a sharp change '
                'in manual-review outcomes, a spike in step-up failures, and merchant reports. '
                'The designed answer is two paths at two speeds &mdash; a rules hotfix that ships '
                'in hours and is auditable, and a model retrain that follows in weeks once labels '
                'exist. If retraining is your only lever, you have built a system that cannot '
                'respond to Monday at all.'),
             a_simple=('<b>Not by retraining &mdash; the answers are two months away.</b> You only '
                       'find out a payment was fraud when the cardholder disputes it, so any '
                       'response that waits for that is a response in sixty days. What moves on '
                       'Monday is everything that does not need an answer key: the mix of '
                       'payments suddenly looks different, the human reviewers start rejecting a '
                       'new shape of order, more customers fail the extra verification step, '
                       'merchants ring up. So you build two speeds &mdash; a rule you can write '
                       'and ship the same afternoon, and a retrained model that follows weeks '
                       'later when the real answers land.')),
        dict(q='Can you use an LLM here?',
             a=('<b>Not in the scoring path, and saying so is the answer.</b> The budget is 10 to '
                '50 ms; a language model call is two to three orders of magnitude outside it, and '
                'it is not explainable to a regulator on a per-decision basis. Where it fits is '
                'everywhere the clock is not running: generating plain-language explanations of a '
                'decision for an analyst, summarising case evidence for the manual review queue, '
                'and feature engineering over unstructured evidence &mdash; merchant '
                'descriptions, dispute text &mdash; which lands in the online store as a '
                'precomputed feature like any other. Being willing to say &ldquo;no LLM in the '
                'hot path&rdquo; is a signal, not a failure.'),
             a_simple=('<b>Not in the ten-to-fifty-millisecond path.</b> A language model takes '
                       'roughly a hundred to a thousand times longer than the whole budget you '
                       'have, and you cannot hand a regulator its reasoning for a single '
                       'decision. It earns its place everywhere the clock is not running: writing '
                       'the plain-English explanation an analyst reads, summarising the evidence '
                       'in a case for the human review queue, and reading the messy text nobody '
                       'else can use &mdash; merchant descriptions, dispute write-ups &mdash; '
                       'into a number that is ready and waiting before the payment arrives. '
                       'Saying no here is the point of the question.')),
    ],

    anchor=dict(
        formula=r'$0.001 \times 5{,}000/\text{s} = 5$ good declined &nbsp;&middot;&nbsp; '
                r'$0.001 \times 5{,}000/\text{s} = 5$ frauds to catch',
        formula_simple=('At five thousand payments a second, blocking one in a thousand good ones '
                        'turns away about five honest customers every second. There are also '
                        'about five frauds in that second. Those two numbers, side by side, are '
                        'the whole product argument.'),
        bullets=[
            'You are inside someone else&rsquo;s timeout, so the budget picks the features',
            'The two error types run on different clocks &mdash; today against 60 days',
            'Labels are the binding constraint, not the model architecture',
        ]),
    chips=['online feature store', 'point-in-time correctness', 'rules fallback',
           'shadow scoring', 'reason codes'],
    followup='Your model&rsquo;s offline AUC is 0.95 and production performance is much worse. Why?',
),
dict(
    id='home-feed-recsys',
    tier='production',
    title='Design: a home feed recommender',
    kicker='Candidate generation and ranking are the easy half &mdash; the feed trains on what it chose to show, and that is the part that rots',

    # ---------------- SIMPLE LAYER ----------------
    simple=[
        'A billion items, twenty slots, three hundred milliseconds. Nothing can look at the whole '
        'corpus, so the work happens in stages, each handing a smaller pile to the next. A cheap '
        'retrieval stage pulls about a thousand plausible items from several sources at once '
        '&mdash; things similar to what you engaged with, things from accounts you follow, things '
        'trending, and a deliberate pool of new items nobody has seen. A much better and much '
        'slower model scores those thousand. A final pass reorders the top for variety, safety '
        'and freshness, and twenty go out. Each stage is cheap enough to run on everything it '
        'receives and good enough to be trusted with the shortlist.',
        'What decides how good this system is in two years is none of those stages. It is that the '
        'feed learns from the feed. Only items you were shown can be clicked, so only shown '
        'items generate training data, and the model grows more confident about exactly what it '
        'was already confident about while never finding out what it was wrong to hide. That is '
        'why a fraction of the slots is reserved for items the model is unsure about, and why '
        'the reservation is written down as a cost rather than treated as a bug.',
        'Then the three cold starts, which are three different problems wearing one name. A new '
        'user has no history, so you fall back to what people like them enjoy and design the '
        'first session to collect signal fast. A new item has no engagement, so it is described '
        'by its own content and given a guaranteed budget of impressions to earn its keep. A new '
        'market has neither, so you borrow from a similar one and expect the borrowing to be '
        'wrong. And when product asks for a written summary on every card, write them once when '
        'the item arrives rather than every time a card is drawn: the same feature costs a couple '
        'of hundred thousand dollars one way and something absurd the other.',
    ],
    analogy=('<b>Like a shop that only restocks what sold.</b> The shelf decides the sales and '
             'the sales decide the shelf, so within a year the shop sells six things very well '
             'and has forgotten it could sell anything else. The only way out is to give a few shelf '
             'slots to products nobody has bought yet, and to accept that they earn less this '
             'week.'),
    trap_simple=('Saying the model will learn what users want. It learns what users clicked among '
                 'the things it decided to show them, which is a much smaller and much more '
                 'flattering question. Say instead that the training data is written by last '
                 'week&rsquo;s ranker, and name the budget you are spending to keep it honest. '
                 'The other trap is answering the summary request with &ldquo;we generate it when '
                 'the card renders&rdquo;. Two billion feed loads times twenty cards is not a '
                 'cost problem you optimise later, it is four orders of magnitude, and the fix is '
                 'a job that runs once per item on the way in.'),

    # ---------------- TECHNICAL LAYER ----------------
    tech=[
        'Size it before you draw it. 100M DAU at ~20 feed loads is 2B requests/day &mdash; ~23K '
        'QPS average, <b>60&ndash;70K peak</b>. 1B items, retrieve ~1,000 candidates, rank to 20, '
        'p95 300 ms server-side. The item index at 256 dimensions is '
        '$1\\text{B} \\times 256 \\times 4\\,\\text{B} = 1.02$ TB in fp32, <b>~256 GB at int8</b>, '
        'plus an HNSW graph at $M=16$ of $1\\text{B} \\times 16 \\times 2 \\times 4 = 128$ GB '
        '&mdash; call it ~384 GB across 8&ndash;16 nodes. At 1,536 dimensions the same index is '
        '6.1 TB fp32 or 1.5 TB int8, so the dimension is a six-fold infrastructure decision '
        'rather than a modelling detail. DoorDash shipped 256 dimensions via Matryoshka for '
        'exactly this reason.',
        'Then the compute, and then the number that binds. Ranking is '
        '$60\\text{K} \\times 1{,}000 = 60\\text{M}$ item-scorings per second; a ~10M-parameter '
        'ranker at 2 FLOPs per parameter is ~20 MFLOPs an item, so ~1.2 PFLOP/s, which at 20% '
        'model-FLOP utilisation on H100s is <b>~6 H100s for ranking alone</b> &mdash; before '
        'feature fetch, before headroom, and flag that 20% as an assumption before you are '
        'asked. Now the binding one: 60M scorings a '
        'second against ~50 item features each is <b>3B feature reads per second</b> if you do it '
        'naively. It is only tractable because item features live in the ranker&rsquo;s memory or '
        'arrive pre-packed with the candidate, never as a per-item lookup.',
        'The request path in order, with the 300 ms spent as you go: user context from a '
        'real-time store plus a long-term embedding &rarr; parallel candidate generation over the '
        'two-tower ANN index, a following source, a trending source and an explicit exploration '
        'pool of fresh, low-impression items (~30 ms) &rarr; dedup and merge &rarr; feature '
        'hydration (~40 ms) &rarr; ranking (~60 ms) &rarr; policy filters, source dedup and '
        'already-seen (~20 ms) &rarr; blending and diversity &rarr; summary cache join (~10 ms) '
        '&rarr; content hydration and serialisation (~60 ms) &rarr; gateway and network (~50 ms), '
        'leaving ~30 ms of headroom. Offline: the event stream feeds point-in-time training joins '
        '&rarr; two-tower plus ranker &rarr; batch item embeddings with incremental re-embedding '
        'of changed items only &rarr; ANN index build and rollout &rarr; a summary job writing to '
        'a KV cache. Impressions are logged back with the ranker version <i>and</i> the candidate '
        'source that produced each item, or you cannot attribute anything later.',
        'The LLM summary is settled by subtraction: <b>~&#36;225,000</b> to summarise 1B items once at '
        '~150 output tokens each and ~&#36;225/day to keep up, against <b>6T output tokens a day</b> '
        'if you generate at render time &mdash; four orders of magnitude, decided in one line. '
        'Failure modes worth naming unprompted. <b>The feedback loop</b>: the model recommends '
        'what it has data on and gathers more data on it &mdash; mitigate with exploration slots, '
        'inverse-propensity weighting, and a monitored coverage metric for what fraction of the '
        'corpus is ever shown. <b>Embedding version mismatch during rollout</b>: user and item '
        'vectors land in different spaces and recall collapses with nothing thrown. '
        '<b>Cold start, three kinds</b>, with three different answers. '
        '<b>A diversity penalty set too weak</b> produces near-duplicate feeds that score well, '
        'so monitor intra-list similarity as a guardrail. <b>Stale summaries</b> after an edit: '
        'invalidate by item ID, never by TTL alone.',
    ],
    tech_note=('Tag your numbers. The 256-dimension production choice, the HNSW graph formula, the '
               'Pinterest rollout mechanism and the token prices are published; the 2B requests, '
               'the 1.02 TB, the ~384 GB, the 60M scorings, the ~6 H100s, the 3B reads and the '
               '&#36;225,000 are arithmetic you performed on top of them. The 20% model-FLOP '
               'utilisation is the weakest link in that chain &mdash; it is an assumption, it '
               'swings the GPU count by 2&ndash;3&times; either way, and volunteering that before '
               'you are asked is worth more than the estimate itself.'),

    # ---------------- FIGURE ----------------
    fig=dict(
        kind='blocks', h=306,
        boxes=[
            dict(x=16,  y=40,  w=86,  h=46, t='request', sub='60K QPS peak'),
            dict(x=114, y=40,  w=128, h=46, t='candidate sources', sub='ANN, follow, fresh'),
            dict(x=254, y=40,  w=128, h=46, t='feature hydration', sub='3B reads if naive', tone='sig'),
            dict(x=394, y=40,  w=104, h=46, t='ranker', sub='60M scorings/s', tone='mem'),
            dict(x=510, y=40,  w=106, h=46, t='policy + diversity', sub='dedup, seen'),
            dict(x=628, y=40,  w=76,  h=46, t='20 cards', sub='300 ms p95', tone='mem'),
            dict(x=16,  y=132, w=140, h=44, t='ANN index', sub='384 GB, versioned', tone='mem'),
            dict(x=176, y=132, w=150, h=44, t='exploration pool', sub='fresh, low-impression', tone='mem'),
            dict(x=346, y=132, w=140, h=44, t='summary cache', sub='precomputed on ingest'),
            dict(x=520, y=132, w=184, h=44, t='impression stream', sub='ranker version, source'),
            dict(x=16,  y=228, w=124, h=48, t='event stream', sub='clicks, dwell, saves'),
            dict(x=156, y=228, w=138, h=48, t='point-in-time join', sub='no time travel'),
            dict(x=310, y=228, w=140, h=48, t='two-tower + ranker', sub='trained on shown items'),
            dict(x=466, y=228, w=160, h=48, t='embed + index build', sub='256 dims, changed only'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3), dict(a=3, b=4), dict(a=4, b=5),
            dict(a=6, b=1, side='up'),
            dict(a=7, b=1, side='up'),
            dict(a=8, b=5, side='up'),
            dict(a=5, b=9, side='down'),
            dict(a=9, b=10, side='down', tone='sig', dash='4 3'),
            dict(a=10, b=11), dict(a=11, b=12), dict(a=12, b=13),
            dict(a=13, b=6, side='up', dash='4 3'),
        ],
        labels=[
            dict(x=16, y=22, t='REQUEST PATH, 300 MS P95', a='start'),
            dict(x=246, y=118, t='POOLS, CACHES AND THE LOG', a='start'),
            dict(x=16, y=212, t='OFFLINE, HOURS TO NIGHTLY', a='start'),
        ],
        foot='the dashed arrow is the whole problem: tomorrow it trains on what it chose to show today',
        alt=('Architecture diagram in three rows. The top row is the request path inside a 300 '
             'millisecond budget: a request fans out to candidate sources, features are hydrated, '
             'a ranker scores sixty million items a second, policy and diversity filters run, and '
             'twenty cards are returned. A middle row holds the ANN index, the exploration pool '
             'and the precomputed summary cache that the path reads, plus the impression stream '
             'it writes. A bottom offline row runs the event stream through point-in-time joins '
             'to the two-tower and ranking models and on to embedding and index build, which '
             'refreshes the index. A dashed arrow returns from the impression stream to the event '
             'stream, closing the loop that trains the model on its own output.')),
    caption=('The pink box is where the design is actually decided: 60M scorings a second against '
             '50 item features each is 3B reads a second, which is why features ride in the '
             'ranker&rsquo;s memory instead of being fetched. The teal boxes are what carries the '
             'answer. The dashed return arrow is the loop everyone draws and nobody budgets for '
             '&mdash; the exploration pool above it is the only thing paying to keep that loop '
             'from closing.'),
    caption_simple=('The pink box is where this design is really decided: the ranker needs so '
                    'many facts per second that fetching them one at a time is impossible, so '
                    'they travel with the candidates instead. The teal boxes are what produces '
                    'the feed. The dashed arrow going back along the bottom is the loop &mdash; '
                    'tomorrow the model learns from what today&rsquo;s model chose to show.'),

    # ---------------- SHARED ----------------
    when_label='The interviewer is really testing',
    when=[
        'Whether you size the item index before you name a vector store',
        'Whether exploration comes up before someone asks you about cold start',
        'Whether you can kill per-request generation with one subtraction',
        'Whether you know which metric decides the launch, and over what window',
    ],
    trap=('Saying &ldquo;we train on engagement data, so the model learns what users want&rdquo;. '
          'It learns what users clicked among the items it chose to show them, which is a '
          'strictly easier and self-confirming question: unshown items generate no engagement, '
          'stay unshown, and quietly leave the corpus. The concrete version an interviewer wants '
          'is the number &mdash; what fraction of 1B items was ever impressed last month, and '
          'what fraction of slots you are spending to keep that number from collapsing. The '
          'second trap is answering the summary twist with &ldquo;we generate it at render '
          'time&rdquo;: 2B requests &times; 20 cards &times; 150 tokens is 6T output tokens a '
          'day, against ~&#36;225,000 to write all 1B once and ~&#36;225/day to keep up.'),

    nums_label='The numbers you design against',
    nums=[
        dict(k='REQUESTS', v='2B/day', s='100M DAU at ~20 feed loads, ~23K QPS average'),
        dict(k='PEAK', v='60&ndash;70K QPS', s='what you size the ranker against, not the average'),
        dict(k='CORPUS', v='1B items', s='retrieve ~1,000, rank to 20'),
        dict(k='INDEX', v='~384 GB', s='256 dims at int8 plus the HNSW graph'),
        dict(k='RANKING LOAD', v='60M scorings/s', s='~6 H100s at an assumed 20% utilisation'),
        dict(k='SUMMARIES', v='~&#36;225,000 once', s='~&#36;225/day after &mdash; or 6T tokens/day per request'),
    ],

    ask=[
        dict(q='What are we optimising?',
             a='Long-term engagement: a weighted blend of clicks, dwell and saves with a negative term for reports. Ask for the blend rather than inventing it.'),
        dict(q='How many users, how many items?',
             a='~100M DAU and ~1B items. Both numbers change the design; the item count decides the index, the user count decides the QPS.'),
        dict(q='What is the latency SLO for a feed load?',
             a='p95 under 300 ms server-side, of which gateway and network take ~50 before you have done anything.'),
        dict(q='How fresh do new items have to be?',
             a='Minutes. That is the cold-start question wearing a different hat, and it is what forces a small fresh index beside the big one.'),
        dict(q='How much of the feed is following versus discovery?',
             a='Mixed, and the ratio is a product lever. Ask to control it, because it is also your exploration budget in disguise.'),
        dict(q='What are the hard policy constraints?',
             a='No policy-violating content, plus diversity and source-dedup rules. These are filters with veto power, not ranking features.'),
        dict(q='Do we have to explain recommendations?',
             a='Increasingly yes in some jurisdictions, which means the candidate source and ranker version have to be carried through to the response.'),
        dict(q='Is the LLM summary per item or per request?',
             a='Per item and precomputable. Establish this in the first two minutes; it decides whether the feature is affordable at all.'),
    ],

    estimate=dict(
        label='Sizing the ranker out loud', cost='derived; the utilisation is an assumption',
        rows=[
            dict(l='requests', w='100M DAU x 20 feed loads', r='2B/day, ~23K QPS'),
            dict(l='peak', w='roughly 3x average', r='60&ndash;70K QPS'),
            dict(l='item scorings', w='60K QPS x 1,000 candidates', r='60M/s'),
            dict(l='per item', w='10M params x 2 FLOPs', r='20 MFLOPs'),
            dict(l='ranking compute', w='60M/s x 20 MFLOPs', r='1.2 PFLOP/s'),
            dict(l='GPUs, at 20% utilisation', w='1.2 PFLOP/s / 198 TFLOP/s effective', r='~6 H100s'),
            dict(l='feature reads, naive', w='60M scorings/s x 50 item features', r='3B reads/s', tot=True),
        ],
        note=('The GPU line is affordable and the read line is not, which is why the last row is '
              'the total that matters: item features ride in the ranker&rsquo;s memory or arrive '
              'pre-packed with the candidate, never as a lookup. Say the 20% utilisation is an '
              'assumption before you are asked &mdash; it moves the GPU count by two or three '
              'times in either direction, and it is the only soft number in the chain.')),

    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='RECALL VS RANKING COST',
             v='<b>1,000 candidates is a tuned number, so justify it with a curve.</b> More '
               'candidates raise the ceiling and cost ranking compute linearly. Say you would '
               'show the recall curve flattening around a thousand rather than defending the '
               'number itself &mdash; the defensible claim is the shape, not the constant.'),
        dict(k='TWO-TOWER VS SEQUENCE',
             v='<b>Both, split by which side can be precomputed.</b> A two-tower model lets you '
               'compute item embeddings in batch and serve them cheaply; a sequence model is more '
               'accurate and cannot be precomputed. Pinterest&rsquo;s resolution is a user tower '
               'carrying long-term engagement plus a real-time transformer over the recent '
               'sequence, with the item tower kept precomputable.'),
        dict(k='ENGAGEMENT VS RETENTION',
             v='<b>Optimising click-through produces a feed that degrades retention.</b> Use '
               'multi-objective ranking with explicit negative signals, and settle launches on a '
               '28-day retention holdout rather than session clicks &mdash; that is precisely '
               'where engagement-optimised models lose, and it is why the holdout has to exist '
               'before you need it.'),
        dict(k='EXPLORATION VS EXPLOITATION',
             v='<b>Reserve slots and call the reservation a cost.</b> Without a deliberate '
               'budget, items the model does not show get no engagement data and therefore stay '
               'unshown; the loop is closed and the corpus shrinks to whatever was popular when '
               'you launched. Pair the slots with inverse-propensity weighting and a coverage '
               'metric.'),
        dict(k='FRESHNESS VS REBUILD COST',
             v='<b>Two indexes, not one schedule.</b> A full ANN rebuild over 1B items is a batch '
               'job; new items must be reachable in minutes. The standard resolution is a small, '
               'frequently rebuilt fresh index queried in parallel with the large stable one, '
               'with incremental re-embedding of changed items only.'),
        dict(k='PER-REQUEST VS PRECOMPUTE',
             v='<b>Settled by arithmetic, in one line.</b> ~&#36;225,000 to summarise 1B items once '
               'and ~&#36;225/day to keep up, against 6T output tokens a day if you generate at '
               'render time. Doing that subtraction out loud is the whole answer to the LLM '
               'twist, and it takes ten seconds.'),
    ],

    verdict=dict(
        no='Draws candidate generation into ranking with no numbers on either. Never sizes the '
           'index. Treats the LLM summary as a per-request call and offers to &ldquo;cache it '
           'later&rdquo;. Does not mention exploration or cold start until asked, and then treats '
           'cold start as one problem rather than three.',
        yes='Computes 1.02 TB against ~384 GB and points out that the dimension choice is a '
            'six-fold infrastructure decision. Does the &#36;225K-against-6T-tokens subtraction in '
            'one line to kill per-request generation. Names the feedback loop early and budgets '
            'exploration slots for it as a cost. Describes the embedding-version rollout problem '
            'with a concrete fix. Knows the launch is decided on 28-day retention, not clicks.'),

    real_label='Where this has actually broken',
    real=('Pinterest runs learned retrieval over 500M+ monthly actives with a two-tower model, and '
          'the failure it had to engineer around is the quiet one: during an index rollout some ANN '
          'hosts serve model version N while others serve N+1, so user and item vectors land in '
          'different spaces and recall collapses with nothing thrown and nothing logged. The fix '
          'is per-host model-version metadata, keeping the mapping from model name to latest '
          'version coherent mid-rollout and retaining the latest N viewer-model versions for '
          'rollback. It is invisible in every offline metric you own.'),

    math=dict(
        tex=r'\underbrace{1\text{B} \times 256 \times 4\,\text{B}}_{\text{1.02 TB fp32}} '
            r'\quad\longrightarrow\quad '
            r'\underbrace{256\,\text{GB}}_{\text{int8}} + '
            r'\underbrace{1\text{B} \times 16 \times 2 \times 4\,\text{B}}_{\text{128 GB HNSW graph}}',
        note='What it does not say: $256$ is a decision. At $1{,}536$ dimensions the same corpus '
             'is 6.1 TB fp32 and 1.5 TB int8, so the embedding dimension sets your node count '
             'before any recall number does.',
        cost='one copy of a 1B-item index'),

    drills=[
        dict(q='Prove the new model is better without shipping it to everyone.',
             a=('<b>Three stages, cheapest first, and the arbiter is not the one you expect.</b> '
                'Start with offline replay using counterfactual estimators to shortlist '
                'candidates &mdash; and say its weakness in the same breath, because replay is '
                'scored on traffic the incumbent policy chose and therefore flatters models that '
                'agree with the incumbent. Then run an interleaving experiment, both rankers&rsquo; '
                'items merged into one feed, which controls for the user and gives a '
                'high-sensitivity read on far less traffic than an A/B. Then a small A/B for the '
                'business metrics, with a 28-day retention holdout as the arbiter, because '
                'engagement-optimised models win the first two stages and lose there.'),
             a_simple=('<b>Three tests, cheapest first, and the last one settles it.</b> First, '
                       'replay past traffic through the new model and estimate what would have '
                       'happened &mdash; cheap, and biased towards models that agree with the '
                       'current one, since the old model chose which items appear in that history '
                       'at all. Second, mix both models&rsquo; picks into a single feed for the '
                       'same users, so each person is their own comparison; this needs far less '
                       'traffic to give a clear answer. Third, a small live split for the '
                       'business numbers, judged on whether people are still coming back four '
                       'weeks later &mdash; which is exactly where a model that chases clicks '
                       'stops looking good.')),
        dict(q='Half your traffic is new users. What changes?',
             a=('<b>Retrieval changes shape, and the first session becomes the product.</b> '
                'Personalised ANN over a user embedding gives way to cohort-level and contextual '
                'signals &mdash; locale, entry point, device, referrer, time of day. The '
                'first-session design is now load-bearing: a small number of fast, high-signal '
                'choices that populate an embedding within minutes rather than days. The ranker '
                'needs an explicitly cold-start-aware feature set, with missing-history flags '
                'rather than a model silently reading zeros and treating a new user as an '
                'inactive one. And say the honest bit: cold-start items inherit popularity bias '
                'even under cold-start-specific methods, so this is a known open problem you are '
                'managing, not solving.'),
             a_simple=('<b>The personalised half of retrieval stops working, so the first session '
                       'becomes the product.</b> With no history there is nothing to be similar '
                       'to, so you lean on what people like this person &mdash; same place, same '
                       'entry point, same time of day &mdash; tend to enjoy, and you design the '
                       'first few minutes to collect real signal fast rather than to look '
                       'impressive. The ranking model has to be told a user is new, not left to '
                       'read blanks and treat them as someone who has been ignoring you for a '
                       'year. And be honest that new items stay disadvantaged even under methods '
                       'built for this &mdash; it is managed, not solved.')),
        dict(q='The LLM summary occasionally says something wrong about the item. What now?',
             a=('<b>Treat it as a generated artefact with a source, not as product copy.</b> '
                'Ground it in item metadata only, so there is a checkable provenance for every '
                'claim; gate on a groundedness check before anything is written to the cache; '
                'sample the cache for judge scoring so you know the rate rather than the '
                'anecdote; and make any single summary suppressible per item ID within minutes, '
                'because the first thing you will need is an off switch for one card. The one '
                'thing you do not do is regenerate at request time to fix it &mdash; that '
                'reintroduces the 6T-token-a-day cost you designed out ten minutes earlier.'),
             a_simple=('<b>It is a generated claim with a source, so treat it the way you treat '
                       'any claim.</b> Write it only from the item&rsquo;s own metadata, check '
                       'before storing that every statement in it is traceable back to that '
                       'metadata, grade a sample regularly so you know how often it is wrong '
                       'rather than arguing about one screenshot, and be able to switch off a '
                       'single item&rsquo;s summary in minutes. What you must not do is start '
                       'writing them fresh at the moment the card is drawn to make them better '
                       '&mdash; that is the enormous bill you just avoided, walking back in '
                       'through the door.')),
    ],

    anchor=dict(
        formula=r'$1\text{B} \times 256 \times 4\,\text{B} = 1.02\ \text{TB}$ '
                r'&nbsp;&middot;&nbsp; int8 + graph &nbsp;&middot;&nbsp; $\approx 384\ \text{GB}$',
        formula_simple=('A billion items, each described by 256 numbers. At four bytes a number '
                        'that is about a terabyte; at one byte a number, plus the graph that '
                        'makes search fast, it is under four hundred gigabytes across a handful '
                        'of machines.'),
        bullets=[
            'The embedding dimension is a six-fold infrastructure decision, not a modelling detail',
            'The feed trains on what it showed, so exploration is a budget line rather than a bug',
            'Precompute anything per item &mdash; per-request generation is four orders of magnitude out',
        ]),
    chips=['two-tower retrieval', 'exploration budget', 'interleaving', 'cold start',
           'embedding versioning'],
    followup='Prove the new model is better without shipping it to everyone.',
),
dict(
    id='genai-eval-harness',
    tier='production',
    title='Design: the eval harness itself',
    kicker='Not the three tiers &mdash; the storage, the gate and the bill. Four and a half minutes and twelve dollars a run is the constraint the whole thing is built around',

    # ---------------- SIMPLE LAYER ----------------
    simple=[
        'You have a product built on a language model and a team changing prompts every week. The '
        'harness answers &ldquo;is this change safe&rdquo; before it ships, and it has four '
        'parts. A case store: a few hundred to a thousand real questions, each with '
        'the properties a good answer must have, a note on which failure it was added to catch, '
        'and where it came from. A runner that executes the product at a pinned version of every '
        'moving piece. A set of graders, some plain checks on whether a phrase appears, some '
        'another model marking the work against a rubric. And a results store '
        'that files every score under the case, the grader and the exact version of the system '
        'that produced it.',
        'The design constraint is not accuracy, it is friction. A full run is about eighteen '
        'thousand gradings, which comes to roughly twelve dollars and four and a half minutes if '
        'you run a hundred at a time. That matters more than it sounds: a gate that takes twenty '
        'minutes gets routed around within a fortnight, and a bypassed gate is worse than none '
        'because everyone still believes it is running. So the fast, free '
        'checks run first and block immediately, and the slower graded ones follow.',
        'Two things then decide whether anyone should believe the numbers. The first is whether '
        'the grader agrees with people: about a hundred examples marked by an expert, roughly '
        'five hours of their time, once per version of the grader. Teams skip this and it is not '
        'because of the cost. The second is how you change the question set without destroying '
        'your own history. Never edit a case in place &mdash; retire it and add a new one with a '
        'new identifier &mdash; because every score you have ever recorded is filed under the '
        'case it came from, and comparing two releases only means something if they answered the '
        'same questions.',
    ],
    analogy=('<b>Like a taste panel with a fixed menu.</b> The same twelve dishes go out every '
             'week, so when Thursday&rsquo;s batch scores worse you know it is the batch and not the '
             'panel. Change the menu and last month is no longer comparable. Change the panel and '
             'you have to check they still agree with the head chef before you trust a card.'),
    trap_simple=('Saying you would use one of the standard evaluation libraries and track how '
                 'faithful the answers are. That names a package and one number. The interviewer '
                 'is waiting to hear where the questions came from, whether anyone has checked '
                 'that the automatic grader agrees with a human, what score blocks a release, how '
                 'much of live traffic gets graded afterwards, and what happens when the '
                 'dashboard is green and users are still complaining. The other trap is quietly '
                 'measuring only the search half: a product can find exactly the right documents '
                 'and still invent the answer, and one blended score hides precisely that case.'),

    # ---------------- TECHNICAL LAYER ----------------
    tech=[
        'The pipeline, in order. <b>Case store</b>: a versioned golden dataset of 300&ndash;1,000 '
        'cases, each tagged with failure mode, domain and difficulty, carrying '
        '<code>must_include</code> and <code>must_not_include</code> assertions plus per-case '
        'threshold overrides. <b>Runner</b>: executes the system under test at a pinned prompt, '
        'model and index version &mdash; all three, or you cannot attribute a regression. '
        '<b>Metric bank</b>: six RAG metrics split explicitly into a retrieval layer and a '
        'generation layer, each returning a score, an explanation and its own cost in dollars. '
        '<b>Judge service</b>: three independent passes with chain-of-thought and rubric anchors, '
        'flagging variance across passes rather than silently averaging it. <b>Results store</b>, '
        'keyed by (case, metric, system version), feeding three consumers: the CI gate, a '
        'dashboard broken down by failure mode, and alerting.',
        'The economics decide whether it gets built. One full run is '
        '$1{,}000 \\times 6 \\times 3 = 18{,}000$ judge calls at ~1,500 input and ~300 output '
        'tokens each, which on a nano-class model is about <b>&#36;12</b> and ~&#36;600 a week across '
        '50 PRs. Wall clock: 18,000 calls at 100-way concurrency and ~1.5 s each is '
        '<b>~4.5 minutes</b> &mdash; the number that matters, because a gate slower than a coffee '
        'gets routed around. Online monitoring at 10% of 200K queries/day is 120K judge calls a '
        'day, roughly <b>&#36;1,800/month</b>. Total eval spend lands near &#36;4,400/month, so '
        '&ldquo;we cannot afford to gate every PR&rdquo; is not a real objection.',
        'The gate and the human loop. Deterministic assertions run first, free and instant; judged '
        'metrics are the slow second stage. '
        'Block on absolute thresholds <i>plus</i> a 5% regression tolerance &mdash; faithfulness '
        '0.85 (0.95 if the stakes are high), context recall 0.80, context precision 0.75, answer '
        'relevancy 0.80 &mdash; and leave everything else advisory. The judge earns trust from '
        '50&ndash;100 human labels '
        'split roughly 10 excellent, 10 poor, 30 ambiguous, and you use the cheapest judge that '
        'clears Spearman &ge;0.85 against them (&ge;0.70 is only good enough for low-stakes work). '
        'That is ~5 hours of expert time per judge version. Online, sample 5&ndash;10%, alert when '
        'rolling faithfulness falls below 0.75 and page at 0.85 of the threshold. A trace '
        'harvester pulls production traces flagged by negative feedback, sub-threshold scores or '
        'p99 latency and proposes them as new cases, each with a changelog entry.',
        'Versioning without invalidating history falls out of the key: every result is filed under '
        '(case, metric, system version), so history lives per case and you never mutate a case in '
        'place. An edited case is retired with a date and a new ID minted, and two system '
        'versions are compared on the intersection of the case IDs both ran. Adding cases then '
        'changes coverage rather than the comparison, and every aggregate is reported beside the '
        'count it came from. Re-check the distribution against production query clusters '
        'quarterly, and hold out a slice never used for iteration and reported only at release, '
        'or the team will tune prompts '
        'until the golden set is green. Two more to name unprompted: an uncalibrated judge '
        'carries position bias, verbosity preference and a preference for outputs that look like '
        'its own, so publish the human-agreement number beside the scores; and a base-model swap '
        'moves every score for reasons unrelated to quality, so pin the judge model version '
        'independently and re-baseline deliberately.',
    ],
    tech_note=('The thresholds, the three-pass recipe, the 50&ndash;100 label calibration split '
               'and the 5% regression tolerance are published guidance; the 300&ndash;1,000 case '
               'range is an <i>estimate</i>, because the handbook specifies the properties a '
               'golden set must have and not a size &mdash; say so rather than quoting it as a '
               'standard. The &#36;12 run, the &#36;600/week, the &#36;1,800/month and the &#36;4,400/month '
               'total are arithmetic on published token prices, and they move with your judge '
               'choice by roughly an order of magnitude, which is exactly why the judge is '
               'chosen empirically rather than by reputation.'),

    # ---------------- FIGURE ----------------
    fig=dict(
        kind='blocks', h=306,
        boxes=[
            dict(x=16,  y=40,  w=124, h=48, t='case store', sub='versioned, tagged', tone='mem'),
            dict(x=156, y=40,  w=124, h=48, t='runner', sub='pinned versions'),
            dict(x=296, y=40,  w=134, h=48, t='metric bank', sub='retrieval + answer'),
            dict(x=446, y=40,  w=118, h=48, t='judge', sub='3 passes, CoT', tone='mem'),
            dict(x=572, y=40,  w=132, h=48, t='results store', sub='case, metric, version', tone='mem'),
            dict(x=130, y=136, w=150, h=44, t='CI gate', sub='blocks the PR, 4.5 min', tone='sig'),
            dict(x=300, y=136, w=150, h=44, t='dashboard', sub='by failure mode'),
            dict(x=470, y=136, w=110, h=44, t='alerting', sub='online 10%'),
            dict(x=600, y=136, w=104, h=44, t='human labels', sub='100, five hours', tone='mem'),
            dict(x=536, y=228, w=168, h=48, t='production traffic', sub='200K/day, 10% sampled'),
            dict(x=296, y=228, w=180, h=48, t='trace harvester', sub='bad feedback, low scores'),
            dict(x=16,  y=228, w=180, h=48, t='proposed cases', sub='with a changelog entry'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3), dict(a=3, b=4),
            dict(a=4, b=5, side='down'),
            dict(a=4, b=6, side='down'),
            dict(a=4, b=7, side='down'),
            dict(a=8, b=3, side='up'),
            dict(a=9, b=10, side='left'),
            dict(a=10, b=11, side='left'),
            dict(a=11, b=0, side='up', dash='4 3'),
        ],
        labels=[
            dict(x=16, y=22, t='ONE RUN, 4.5 MINUTES', a='start'),
            dict(x=130, y=122, t='WHO READS IT', a='start'),
            dict(x=130, y=212, t='THE LOOP BACK, WEEKLY', a='start'),
        ],
        foot='the gate is the only box with teeth, and it costs about twelve dollars a run',
        alt=('Architecture diagram in three rows. The top row is one evaluation run: a versioned '
             'case store feeds a runner pinned to specific prompt, model and index versions, '
             'through a metric bank split into retrieval and answer layers, into a judge running '
             'three passes, into a results store keyed by case, metric and system version. The '
             'middle row holds the three consumers of that store: a CI gate that blocks the pull '
             'request, a dashboard broken down by failure mode, and alerting on the ten '
             'percent online sample, plus the hundred human labels that calibrate the judge. The bottom row runs right to left: production traffic feeds a trace '
             'harvester that proposes new cases, which return to the case store on a dashed '
             'arrow.')),
    caption=('The pink box is the only one with teeth, and everything upstream is shaped by it: '
             'the run has to finish in about four and a half minutes and cost about twelve '
             'dollars, or developers route around the gate and you keep the dashboard without '
             'the safety. The teal boxes are what makes the numbers mean anything &mdash; a case '
             'store you never edit in place, a judge calibrated against human labels, and results '
             'keyed so two releases can be compared on the cases they both ran.'),
    caption_simple=('The pink box is the only one with real power: it stops a change from '
                    'shipping. Everything to its left is shaped by the need to finish in minutes '
                    'and cost about twelve dollars, because a slow gate gets bypassed. The teal '
                    'boxes are what makes the scores trustworthy &mdash; a question set you never '
                    'quietly edit, a grader checked against people, and results filed so two '
                    'releases can be compared fairly.'),

    # ---------------- SHARED ----------------
    when_label='The interviewer is really testing',
    when=[
        'Whether &ldquo;we would evaluate it&rdquo; turns into a system with thresholds and an owner',
        'Whether you know what one run costs and how long it takes',
        'Whether you separate retrieval metrics from generation metrics without being asked',
        'Whether you can name the smallest version of this that is still worth building',
    ],
    trap=('Saying &ldquo;we would use RAGAS and track faithfulness&rdquo;. That is a library and '
          'one number, and the follow-ups it invites are all fatal: where did the cases come '
          'from, has anyone checked the judge against a human, what score blocks a merge, what '
          'fraction of live traffic gets scored, and what do you do on the day the dashboard is '
          'green and users are angry. The sharper version of the trap is reporting one blended '
          'quality score. A system can score high on faithfulness while failing on context '
          'recall, and the reverse &mdash; recall@10 of 0.91 with faithfulness at 0.6 is a '
          'product confidently inventing answers out of the correct documents, and a single '
          'average is precisely the shape of number that hides it.'),

    nums_label='The numbers you design against',
    nums=[
        dict(k='TRAFFIC', v='200K queries/day', s='the pool the online sample is drawn from'),
        dict(k='CHANGE RATE', v='~50 PRs/week', s='prompts weekly, retrieval monthly, model quarterly'),
        dict(k='GOLDEN SET', v='300&ndash;1,000 cases', s='an estimate &mdash; the handbook specifies properties, not a size'),
        dict(k='ONE FULL RUN', v='~&#36;12, 4.5 min', s='18,000 judge calls at 100-way concurrency'),
        dict(k='MONITORING', v='~&#36;1,800/month', s='10% sampling, six metrics, one pass'),
        dict(k='CALIBRATION', v='100 labels', s='~5 hours of expert time, once per judge version'),
    ],

    ask=[
        dict(q='What is the product surface, and what does a wrong answer cost?',
             a='Internal assistant; a wrong answer causes rework rather than regulatory harm. That one sentence sets every threshold below.'),
        dict(q='What changes, and how often?',
             a='Prompts weekly, retrieval config monthly, base model quarterly. Three blast radii, so three different gates rather than one.'),
        dict(q='Do we have human labels?',
             a='A little, and getting more is the constraint. Budget the expert hours explicitly &mdash; about 5 per judge version.'),
        dict(q='What is the traffic volume?',
             a='~200K queries/day, which is what makes a 10% online sample cost ~&#36;1,800/month rather than nothing or everything.'),
        dict(q='Per-component evaluation, or end to end?',
             a='Both, and this is the key design decision. Gate on end to end; diagnose with components.'),
        dict(q='Is there a cost or latency budget for evaluation itself?',
             a='Yes. It runs on every PR without blocking developers, which means minutes and single-digit dollars, not hours.'),
        dict(q='Who acts on a regression?',
             a='The team that shipped it. The gate fails their PR; it does not file a ticket for someone else to triage next week.'),
    ],

    estimate=dict(
        label='What the harness costs to run', cost='derived from published token prices',
        rows=[
            dict(l='judge calls per run', w='1,000 cases x 6 metrics x 3 passes', r='18,000'),
            dict(l='tokens per run', w='18,000 x (1,500 in, 300 out)', r='27M in, 5.4M out'),
            dict(l='cost per run', w='at &#36;0.20 / &#36;1.25 per M', r='~&#36;12'),
            dict(l='wall clock', w='18,000 calls, 100-way, ~1.5 s each', r='~4.5 min'),
            dict(l='gate bill', w='~&#36;12 x 50 PRs/week', r='~&#36;600/week'),
            dict(l='online monitoring', w='10% of 200K/day x 6 metrics x 1 pass', r='~&#36;1,800/month'),
            dict(l='total eval spend', w='gate plus monitoring', r='~&#36;4,400/month', tot=True),
        ],
        note=('That total is the answer to the objection you will get, so have it ready. The '
              'wall-clock row is the one that actually decides adoption: at 4.5 minutes the gate '
              'is respected, at twenty it is routed around, and a gate everybody bypasses is '
              'worse than none because the dashboard still looks like coverage.')),

    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='COMPONENT VS END-TO-END',
             v='<b>Gate on end to end, diagnose with components.</b> End-to-end alone tells you '
               'something broke but not what; isolated retrieval metrics tell you where and can '
               'be green while the product is bad. Run both and be explicit about which one has '
               'the power to fail a build.'),
        dict(k='JUDGE COST VS AGREEMENT',
             v='<b>Use the cheapest judge that clears Spearman &ge;0.85 against your labels.</b> '
               'A frontier judge agrees better and costs roughly 10&times; more; a cheap one is '
               'affordable at 10% online sampling and drifts from human judgement. This is '
               'settled empirically on 100 labels, not by argument &mdash; and the calibration '
               'number belongs on the dashboard.'),
        dict(k='SET SIZE VS STALENESS',
             v='<b>The failure is drift, not size.</b> A larger set is more sensitive and costlier '
               'to maintain, but the thing that actually kills a golden set is that it was '
               'curated six months ago and no longer looks like traffic. Version it, and re-check '
               'its cluster distribution against production quarterly.'),
        dict(k='BLOCKING VS ADVISORY',
             v='<b>Blocking on absolutes plus a 5% regression tolerance, advisory on everything '
               'else.</b> Blocking gates get respected until they are flaky, and then they get '
               'routed around permanently. The tolerance exists so that judge variance does not '
               'fail an innocent PR, which is the thing that destroys trust in the gate.'),
        dict(k='ASSERTIONS VS JUDGED SCORES',
             v='<b>Assertions are the fast gate, judged metrics the slow one.</b> A '
               '<code>must_not_include</code> string check is free, instant and catches the worst '
               'regressions &mdash; a leaked internal hostname, a banned phrase. Judged scores '
               'catch quality. Run the free ones first and fail early.'),
        dict(k='OFFLINE VS ONLINE',
             v='<b>Budget for both or keep being surprised.</b> Offline is where you catch '
               'regressions on failures you already know about; online is where you discover the '
               'failure modes nobody thought to write a case for. The trace harvester is the '
               'structural connection between them, not a nice-to-have.'),
    ],

    verdict=dict(
        no='&ldquo;We would use RAGAS and track faithfulness.&rdquo; No provenance for the golden '
           'set, no judge calibration, no gate, no online sampling, and no distinction at all '
           'between retrieval metrics and generation metrics.',
        yes='Names a judge calibration number unprompted &mdash; Spearman &ge;0.85 on 100 human '
            'labels &mdash; and says what it costs in expert hours. Gives concrete gate '
            'thresholds with a regression tolerance. Sources the golden set from production '
            'failures and tags each case by failure mode. Computes what the eval itself costs and '
            'how long a run takes. Explains how the case store is versioned so last '
            'quarter&rsquo;s numbers still mean something.'),

    real_label='Where this has actually paid off',
    real=('Uber rebuilt evaluation for Genie, its internal on-call support assistant, around an '
          'LLM judge scoring answers 0&ndash;5 against a curated set &mdash; which cut an '
          'evaluation cycle from weeks of manual review to minutes, and that speed is what made '
          'the rest possible. With the enhanced agentic RAG pipeline it reports a 27% relative '
          'increase in acceptable answers and a 60% relative reduction in incorrect advice. The '
          'sequencing is the lesson: they did not improve the product and then measure it, they '
          'built a measurement loop fast enough to iterate against and the improvements followed.'),

    math=dict(
        tex=r'\underbrace{1{,}000}_{\text{cases}} \times \underbrace{6}_{\text{metrics}} '
            r'\times \underbrace{3}_{\text{passes}} = 18{,}000 \text{ judge calls} '
            r'\quad\Rightarrow\quad \text{4.5 min}, \ \text{about 12 USD}',
        note='What it does not say: three passes is a variance measurement, not a vote. If the '
             'three disagree on a case, that case has an ambiguous rubric and belongs in front of '
             'a human &mdash; averaging it away is how a judge stays uncalibrated for a year.',
        cost='one full run, 100-way concurrency'),

    drills=[
        dict(q='Your judge and your humans disagree on 30% of cases. What do you do?',
             a=('<b>Do not touch the judge yet &mdash; read the disagreements first.</b> They '
                'almost always cluster, and the cluster tells you which problem you have. Before '
                'blaming the judge, measure inter-human agreement on the same cases: if two '
                'experts agree with each other at only 0.6, you do not have a judge problem, you '
                'have a rubric problem, and tuning the judge against inconsistent labels will '
                'just fit the noise. If the humans agree with each other and not with the judge, '
                'look at the classic biases &mdash; position, verbosity, and a preference for '
                'outputs that read like its own &mdash; then tighten the rubric anchors and '
                're-run the calibration. Only after that do you consider a more expensive judge, '
                'and you re-measure Spearman rather than assuming it improved.'),
             a_simple=('<b>Read the disagreements before you change the grader.</b> They almost '
                       'never scatter randomly; they clump around one kind of case, and the clump '
                       'is the diagnosis. The first thing to measure is whether your human '
                       'markers agree with <i>each other</i> on those same cases. If two experts '
                       'only agree about six times in ten, the instructions are ambiguous and the '
                       'automatic grader is being blamed for a badly written question sheet. If '
                       'the humans do agree with each other, then the grader has a habit worth '
                       'naming &mdash; it tends to prefer longer answers, or whichever one it '
                       'saw first, or writing that sounds like its own. Fix the instructions, '
                       'then re-check the agreement rather than assuming it got better.')),
        dict(q='How do you evaluate an agent, where there is no single right answer?',
             a=('<b>Shift from output matching to trajectory evaluation.</b> Decompose the task '
                'into sub-goals and verify each one independently, so a run that gets three of '
                'four steps right scores as such instead of as a binary failure. Score tool usage '
                'as its own dimension &mdash; redundant calls, missing calls, mis-ordered calls '
                '&mdash; because that is where cost and latency regressions show up long before '
                'quality does. And check reasoning coherence separately from correctness: an '
                'agent that reaches the right answer by a wrong route has not solved the task, it '
                'has got lucky, and it will fail on the next input. The final answer is one '
                'signal among four, not the score.'),
             a_simple=('<b>Grade the route, not just the destination.</b> Break the task into the '
                       'steps a competent person would take and check each one, so a run that '
                       'gets most of the way is scored as most of the way rather than as a flat '
                       'failure. Score the tool use on its own &mdash; calls it repeated, calls '
                       'it skipped, calls it made in the wrong order &mdash; because that is '
                       'where cost and slowness appear first. And check whether the reasoning '
                       'holds together separately from whether the answer was right, because an '
                       'agent that stumbles onto the correct answer by a wrong route has not '
                       'learned anything and will miss the next one.')),
        dict(q='Give me the smallest version of this that is still worth building.',
             a=('<b>One hundred cases, two metrics, one judge pass, one blocking gate, one weekly '
                'review.</b> The hundred cases are harvested from real complaints rather than '
                'invented, which is what makes them worth running. The two metrics are '
                'faithfulness and context recall, because they sit on opposite sides of the '
                'retrieval and generation split and between them catch most of what breaks. One '
                'judge pass instead of three, accepting the variance and knowing you have '
                'accepted it. A blocking CI gate on prompt changes only. And a weekly manual '
                'review of 20 sampled production traces, which is how the next hundred cases get '
                'found. Everything else in this design is an extension of those five things, and '
                'being able to name the minimum is the senior signal in the question.'),
             a_simple=('<b>A hundred real cases, two measures, one grading pass, one gate, one '
                       'weekly read.</b> Take a hundred questions from actual complaints, not '
                       'from imagination. Measure two things: whether the right source material '
                       'was found, and whether the answer actually followed from it &mdash; one '
                       'from each half of the system, which between them catch most failures. '
                       'Grade once rather than three times and know that you are living with '
                       'noise. Block only prompt changes. And read twenty real conversations '
                       'every week, which is where the next hundred cases come from. Everything '
                       'else here is an extension of those five, and knowing which five is the '
                       'point.')),
    ],

    anchor=dict(
        formula=r'$1{,}000 \times 6 \times 3 = 18{,}000$ judge calls '
                r'&nbsp;&middot;&nbsp; ~&#36;12 &nbsp;&middot;&nbsp; ~4.5 minutes',
        formula_simple=('A thousand cases, six things measured on each, three independent '
                        'gradings apiece. That is eighteen thousand gradings: about twelve '
                        'dollars and four and a half minutes, which is precisely why it can run '
                        'on every change.'),
        bullets=[
            'The gate has to be fast enough that nobody routes around it &mdash; minutes, not hours',
            'Results are keyed by case, metric and system version, so never edit a case in place',
            'An uncalibrated judge is a number without units; 100 human labels buys it units',
        ]),
    chips=['golden set provenance', 'judge calibration', 'regression tolerance',
           'trace harvester', 'held-out slice'],
    followup='Your judge and your humans disagree on 30% of cases. What do you do?',
)]
