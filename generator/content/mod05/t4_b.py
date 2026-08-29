CARDS = [

    # ------------------------------------------------------------------ 1
    dict(
        id='oec-guardrails',
        tier='production',
        title='The OEC and its guardrails',
        kicker='One metric decides the launch. Everything else exists to stop it &mdash; and you name all of them, with numbers, before you look at the data',
        simple=[
            'Every experiment needs one number that decides it. Pick that number before you start, '
            'write it down, and agree that the team will be judged on it. Everything else you '
            'measure is a guardrail: something you have promised not to break. Latency, cost per '
            'request, crash rate, unsubscribes, how often the model refuses, how often it makes '
            'something up.',
            'The two kinds are read in opposite directions. For the deciding metric you ask '
            'whether the improvement is real and big enough to be worth having. For a guardrail '
            'you ask the reverse: can you rule out a harm you would not accept? That means '
            'holding the whole range of plausible harms against a limit you set in advance &mdash; '
            'not asking whether the harm happened to be visible. A guardrail that came back quiet '
            'on a small sample has told you nothing at all.',
        ],
        analogy=('<b>Like a pilot&rsquo;s checklist before takeoff.</b> One number decides whether '
                 'you fly: are you at the speed where the wing works. Everything else on the list '
                 '&mdash; fuel, flaps, weight, ice &mdash; cannot make you take off, but any one '
                 'of them can stop you. And nobody writes the limits down while the plane is '
                 'already rolling.'),
        simple_extra=('The obvious metric is usually the one that is easiest to collect, and that is '
                      'why it is usually wrong. For a feature that writes text for people, the '
                      'easy metric is the thumbs-up button &mdash; but almost nobody presses it, '
                      'and the few who do are the delighted and the furious. Pick the thing you '
                      'would still defend a quarter later: did the person finish what they came '
                      'to do, and did they come back. Keep thumbs-up as a guardrail.'),
        trap_simple=('Choosing the deciding metric after seeing the results, or bringing a '
                     'dashboard of twenty numbers to the review and letting the loudest person '
                     'pick one. The quieter version: a harm check came back with nothing visible, '
                     'so somebody writes &ldquo;no harm&rdquo; in the summary &mdash; when the '
                     'range of plausible harms still runs from nothing to a serious regression.'),
        tech=[
            'The OEC is one metric, chosen in advance, that the team agrees to be judged on; '
            'everything else is secondary or a guardrail. The distinction is not seniority, it is '
            'which test you run. The OEC gets a superiority test: is the effect real, and is the '
            'interval far enough from zero to be worth shipping. Guardrails get non-inferiority '
            'tests: for a metric you must not increase, the question is whether the <i>upper</i> '
            'end of the interval sits inside a tolerance written down before launch &mdash; never '
            'whether $p < 0.05$.',
            'Two consequences. First, &ldquo;the guardrail was not significant&rdquo; is not a '
            'pass. Kohavi&rsquo;s Rule 5 has Bing experiments moving clicks enormously while user '
            'abandonment came back at p = 0.64, 0.71, 0.83, 0.92 and 0.93, and a 12% ad-revenue '
            'decline moved it not at all; on a metric that hard to shift, a large p-value is '
            'close to no information. Second, put the guardrail into the OEC&rsquo;s currency '
            'wherever you can. Bing published roughly +0.6% revenue per 100 ms of speedup, so a '
            '40 ms p95 regression is about 0.24% of revenue &mdash; a number you can hold against '
            'a 0.8% gain and argue about honestly.',
            'The habit that goes with all of this is Twyman&rsquo;s law: any figure that looks '
            'unusually interesting is usually wrong. Check the instrumentation before you '
            'celebrate the win.',
        ],
        tech_note=('The tolerance is a business decision, not a statistical one, and it is the '
                   'part nobody wants to own. If nobody set one, that is the finding &mdash; say '
                   'so in the readout instead of inventing a threshold afterwards. And a '
                   'guardrail you were never powered to check is not a guardrail: on a rare event '
                   'like a crash or a harmful completion, seeing nothing is compatible with a '
                   'rate you would never accept, so quote the upper bound rather than the point '
                   'estimate.'),
        math=dict(
            tex=r'\text{ship} \iff \underbrace{\text{CI}^{\text{lower}}_{\text{OEC}} > 0}'
                r'_{\text{superiority}} \;\wedge\; \underbrace{\text{CI}^{\text{upper}}'
                r'_{\text{guardrail}} < \tau}_{\tau \text{ fixed before launch}}',
            note='The right-hand half is the one candidates drop. A guardrail with a wide '
                 'interval fails that test even when its p-value is large, which is exactly the '
                 'case where people write "no harm".',
            cost='non-inferiority, one-sided, tolerance set in advance'),
        fig=dict(
            kind='blocks',
            h=286,
            head=['THE ONE THAT DECIDES', 'THE ONES THAT VETO'],
            boxes=[
                dict(x=34, y=40, w=200, h=58, t='OEC: task success',
                     sub='+0.8% (p = 0.01)', tone='mem'),
                dict(x=300, y=40, w=150, h=58, t='SHIP?', sub='one veto is enough', tone='plain'),
                dict(x=34, y=182, w=150, h=58, t='p95 latency',
                     sub='+40 ms vs cap 25 ms', tone='sig'),
                dict(x=201, y=182, w=150, h=58, t='cost per task',
                     sub='+2% vs cap +10%', tone='mem'),
                dict(x=368, y=182, w=150, h=58, t='refusal rate',
                     sub='flat vs cap +0.5pt', tone='mem'),
                dict(x=535, y=182, w=150, h=58, t='escalation rate',
                     sub='-0.3% vs cap flat', tone='mem'),
            ],
            links=[
                dict(a=0, b=1, label='proposes'),
                dict(a=2, b=1, side='up', tone='sig', label='blocks it'),
                dict(a=3, b=1, side='up'),
                dict(a=4, b=1, side='up'),
                dict(a=5, b=1, side='up'),
            ],
            foot='the caps are the part you write down before the experiment, not after',
            alt='One decision metric proposing a launch, with four guardrail metrics below it '
                'that each point back at the decision; the latency guardrail is over its '
                'pre-registered cap and blocks the launch while the other three are inside '
                'theirs'),
        caption=('The OEC proposes and every guardrail can veto. The only thing that turns this '
                 'into a decision rather than an argument is the cap written under each guardrail '
                 'before the experiment started &mdash; and the comparison is interval against '
                 'cap, not p-value against 0.05.'),
        caption_simple=('One metric proposes the launch; any safety metric can block it. The small '
                        'numbers underneath are the limits agreed in advance, and they are what '
                        'turn this picture into a decision instead of an argument.'),
        when=[
            'Three people give three different answers to "what does this launch on?"',
            'The primary metric is up and p95 latency is up along with it',
            'Someone brings a dashboard of twenty metrics to a ship review',
            'A PM proposes thumbs-up rate as the metric for a new LLM feature',
        ],
        trap=('Inventing the OEC after the results land: the readout that says "revenue was flat '
              'but engagement is up 3%, so we ship" when engagement was never the agreed '
              'criterion. The second version is quieter and more common &mdash; "latency was not '
              'significant, so no harm" &mdash; when the interval on latency runs from &minus;5 '
              'ms to +85 ms against a 25 ms tolerance. That interval does not clear the guardrail, '
              'it fails to test it.'),
        real=('Kohavi, Tang &amp; Xu&rsquo;s <i>Trustworthy Online Controlled Experiments</i> '
              '(Cambridge, 2020) is the reference text, and the free Seven Rules of Thumb paper '
              'carries the numbers: Bing experiments that shifted clicks hugely left user '
              'abandonment at p = 0.64, 0.71, 0.83, 0.92 and 0.93, and a 12% ad-revenue decline '
              'did not move it at all. Booking.com runs more than a thousand concurrent '
              'experiments and reports that around 90% fail to produce the expected win &mdash; '
              'which is precisely why the criterion is agreed first.'),
        drills=[
            dict(q='Your primary metric is up 0.8% (p = 0.01) and latency p95 is up 40 ms (p = 0.03). Ship?',
                 a=('<b>Not until you say what latency tolerance you set before the test.</b> This '
                    'is a decision, not a test. If 40 ms was inside the pre-registered tolerance, '
                    'you ship and record it; if it was outside, you do not, whatever the OEC did. '
                    'If nobody set a tolerance, that is the finding and it goes in the readout. '
                    'Then make it one argument instead of two: at Bing&rsquo;s published +0.6% '
                    'revenue per 100 ms, 40 ms is roughly 0.24% against a 0.8% gain.'),
                 a_simple=('<b>Not until you say what delay limit you agreed before the test.</b> '
                           'This is a decision, not a statistics question. If forty milliseconds '
                           'was inside the limit you wrote down, ship it and record that you did. '
                           'If it was outside, you do not ship, however good the main metric '
                           'looks. If nobody wrote a limit down, that is the real finding. What '
                           'settles the room is putting both into the same units: published '
                           'figures from large search engines price a tenth of a second of extra '
                           'delay at well under one per cent of revenue, so you can weigh the two '
                           'against each other directly.')),
            dict(q='You are shipping an LLM-written summary on a product page. The PM wants thumbs-up rate as the OEC. What do you say?',
                 a=('<b>Thumbs-up is a guardrail, not the criterion.</b> The response rate is tiny '
                    'and self-selected &mdash; the delighted and the furious press it &mdash; so '
                    'it measures strength of feeling among people who felt something, not whether '
                    'the feature worked. For a GenAI feature the OEC is usually task success or '
                    'retained usage: did the person get what they came for, and did they come '
                    'back. The guardrails are the LLM-specific ones: p95 latency, cost per '
                    'resolved task, refusal and over-refusal rate, hallucination rate on a '
                    'sampled audit, and escalation to a human.'),
                 a_simple=('<b>Thumbs-up belongs on the safety list, not on the decision.</b> '
                           'Almost nobody presses it, and the few who do are the delighted and the '
                           'furious, so it measures strong feelings rather than whether the '
                           'feature worked. The deciding metric should be the thing you would '
                           'still defend three months later: did the person finish what they came '
                           'to do, and did they come back. Keep thumbs-up alongside cost, delay, '
                           'refusals and how often a human has to take over &mdash; things that '
                           'can block the launch but never justify it.')),
            dict(q='A guardrail metric came back at p = 0.71. Is that "no harm"?',
                 a=('<b>No &mdash; that is absence of evidence, and on some metrics it is close to '
                    'no information at all.</b> Ask for the interval and compare its bad end with '
                    'the tolerance. Bing&rsquo;s abandonment metric produced p-values from 0.64 to '
                    '0.93 while clicks moved enormously, so a metric that stubborn will hand you a '
                    'large p-value almost regardless of what happened. If the interval&rsquo;s bad '
                    'end is inside tolerance you have a genuine non-inferiority pass; if it runs '
                    'well past tolerance, you were never powered to check that guardrail and the '
                    'readout should say so.'),
                 a_simple=('<b>No &mdash; nothing was detected, which is not the same as nothing '
                           'happened.</b> Ask for the range of plausible harms and compare its '
                           'worst end with the limit you agreed. Some metrics barely budge even '
                           'when something serious is going on: large search experiments have '
                           'shifted clicks enormously while the measure of users giving up sat '
                           'perfectly still. If the worst plausible harm is inside your limit, '
                           'that is a real pass. If it runs well past the limit, the check was too '
                           'small to mean anything and you should say that instead.')),
        ],
        anchor=dict(
            formula=r'one OEC, tested for superiority &nbsp;&middot;&nbsp; every guardrail tested '
                    r'for non-inferiority against a $\tau$ fixed before launch',
            formula_simple='One metric decides it. Everything else can only stop it, and each one '
                           'has a limit you agreed in advance.',
            bullets=[
                'Name the OEC in writing before the experiment, or the PM names it afterwards',
                'Guardrails ask whether the whole interval clears a tolerance, not whether the '
                'p-value is small',
                'A quiet guardrail on a metric nobody can move is not a pass',
                'Convert the guardrail into the OEC&rsquo;s currency and it becomes one argument, '
                'not two',
            ]),
        chips=['non-inferiority test', 'pre-registration', 'Twyman&rsquo;s law',
               'guardrail metrics', 'p95 latency', 'absence of evidence'],
        followup='Your primary metric is up 0.8% (p = 0.01) and latency p95 is up 40 ms (p = 0.03). Ship?',
    ),

    # ------------------------------------------------------------------ 2
    dict(
        id='eval-set-size',
        tier='production',
        title='82% on 50 prompts is not a result',
        kicker='The interval runs from roughly 71% to 93%, which cannot separate your new model from the one you are replacing',
        simple=[
            'An eval score is a poll. You drew fifty prompts, the model got forty-one of them '
            'right, and you wrote down 82%. Draw a different fifty from the same pool and you '
            'would have written down something else. The honest version of the number carries its '
            'range, and at fifty items that range is roughly 71% to 93% &mdash; about eleven '
            'points either side.',
            'The width is the whole problem. A model that is truly 75% and a model that is truly '
            '90% both sit comfortably inside it, so this eval cannot rank two models, cannot '
            'justify a launch, and certainly cannot support blocking a release over a two-point '
            'drop. Narrowing the range is expensive: four times the prompts to halve it. Another '
            'fifty prompts is not a fix; another nine hundred is.',
            'So report the range with every score, size the eval from the smallest difference you '
            'actually need to see, and wherever you can, score both models on the same prompts.',
        ],
        analogy=('<b>Like a poll of fifty voters.</b> Nobody calls an election off fifty '
                 'responses, because the margin of error is about ten points and the race is '
                 'closer than that. Your eval set is a poll of the prompts your users will '
                 'actually send, and fifty of them buys you exactly the same margin as fifty '
                 'voters.'),
        simple_extra=('Two things make small evals worse than the arithmetic suggests. Below '
                      'roughly three hundred items the ordinary textbook range is not just wide '
                      'but wrong at the edges &mdash; near the top it will happily run past 100%. '
                      'Use a Wilson interval instead, which for those fifty prompts gives about '
                      '69% to 90%: lower, and lopsided. And if you sample at any temperature above '
                      'zero, the same prompt gives different answers on different days, so run '
                      'every item several times and you will see how much of your score was '
                      'weather.'),
        trap_simple=('Saying &ldquo;the new prompt gets 84 and the old one gets 82 on our two '
                     'hundred item set, so it is a win&rdquo;. Two points on two hundred items is '
                     'well inside the noise. The quieter version: your eval is forty documents '
                     'with five questions each, and you treated it as two hundred independent '
                     'tries. It is closer to forty.'),
        tech=[
            r'For a binary pass/fail eval the standard error is $\sqrt{\bar{s}(1-\bar{s})/n}$. At '
            r'$\bar{s} = 0.82$ and $n = 50$ that is 5.4 percentage points, so the 95% interval is '
            r'about $[71\%, 93\%]$ &mdash; and because $n$ is small and the score sits near the '
            r'boundary you should be quoting Wilson, which returns roughly $[69\%, 90\%]$ and is '
            r'asymmetric. Halving an interval costs $4\times$ the data. Resolving a two-point gap '
            r'between two models takes thousands of items, unless you pair them.',
            'Anthropic&rsquo;s error-bars paper is the de facto standard, and its five '
            'recommendations are worth saying in order: standard errors from the CLT; '
            '<i>clustered</i> standard errors when questions come in related groups; variance '
            'reduction by resampling answers and using next-token probabilities; inference on '
            'question-level <i>paired</i> differences when comparing two models; and a power '
            'analysis before you build the eval at all.',
            r'Then invert it when someone asks how big the eval should be. To detect a three-point '
            r'difference, $n \approx 16p(1-p)/\delta^{2} \approx 16(0.25)/0.03^{2} \approx 4{,}400$ '
            r'items &mdash; far fewer if both systems are scored on the same items and their '
            r'errors are correlated. That is the number to bring to the labelling-budget '
            r'conversation.',
        ],
        tech_note=(r'All of this assumes the benchmark measures something. Scale AI&rsquo;s GSM1k '
                   r'rebuilt GSM8K from scratch and found accuracy drops of up to 8%, with a '
                   r'Spearman $r^{2}$ of 0.36 between a model&rsquo;s probability of generating '
                   r'GSM8K items and the size of its drop. MMLU-Redux re-annotated 5,700 questions '
                   r'across all 57 subjects and put the error rate at 6.49% &mdash; 57% in the '
                   r'analysed Virology items. On that subset your ceiling is the noise floor, and '
                   r'a gap smaller than the label-error rate is not a measurement.'),
        math=dict(
            tex=r'\mathrm{SE} = \sqrt{\frac{\bar{s}\,(1-\bar{s})}{n}} '
                r'= \sqrt{\frac{0.82 \times 0.18}{50}} = 5.4\,\text{pp} '
                r'\quad\Longrightarrow\quad 82\% \pm 10.6\,\text{pp}',
            note='This is the Wald interval, and at n = 50 near the boundary it is the wrong one: '
                 'Wilson gives roughly [69%, 90%]. The formula also assumes the 50 items are '
                 'independent &mdash; five questions per document and they are not.',
            cost='binary outcome, independent items'),
        code=dict(
            label='The interval, and the eval size you actually need',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
                 '<span class="k">def</span> wilson(k, n, z=<span class="s">1.96</span>):\n'
                 '    p, d = k / n, <span class="s">1</span> + z**<span class="s">2</span> / n\n'
                 '    c = (p + z**<span class="s">2</span> / (<span class="s">2</span>*n)) / d\n'
                 '    h = z / d * np.sqrt(p*(<span class="s">1</span>-p)/n '
                 '+ z**<span class="s">2</span>/(<span class="s">4</span>*n*n))\n'
                 '    <span class="k">return</span> c - h, c + h\n\n'
                 '<span class="k">print</span>(wilson(<span class="s">41</span>, '
                 '<span class="s">50</span>))       '
                 '<span class="c"># (0.692, 0.902) -- what you may claim</span>\n\n'
                 'p = <span class="s">0.82</span>\n'
                 'se = np.sqrt(p*(<span class="s">1</span>-p)/<span class="s">50</span>)   '
                 '<span class="c"># 0.0543 -- the Wald version, for comparison</span>\n'
                 '<span class="k">print</span>(p - <span class="s">1.96</span>*se, '
                 'p + <span class="s">1.96</span>*se)   '
                 '<span class="c"># (0.714, 0.927)</span>\n\n'
                 '<span class="c"># width of the 95% interval, in points, as the eval grows</span>\n'
                 '<span class="k">for</span> n <span class="k">in</span> '
                 '(<span class="s">50</span>, <span class="s">200</span>, '
                 '<span class="s">900</span>):\n'
                 '    <span class="k">print</span>(n, '
                 '<span class="k">round</span>(<span class="s">2</span>*'
                 '<span class="s">1.96</span>*np.sqrt(p*(<span class="s">1</span>-p)/n)*'
                 '<span class="s">100</span>, <span class="s">1</span>))\n'
                 '<span class="c"># 50 -> 21.3    200 -> 10.6    900 -> 5.0</span>')),
        fig=dict(
            kind='plot',
            xr=(0, 1000), yr=(0, 26), ph=200,
            head=['WHAT 50 PROMPTS BUYS YOU', 'WHAT IT COSTS TO DO BETTER'],
            xlab='items in the eval set', ylab='width of the 95% interval, in points',
            xticks=[(50, '50'), (200, '200'), (400, '400'), (600, '600'), (800, '800'),
                    (1000, '1000')],
            yticks=[(5, '5'), (10, '10'), (15, '15'), (20, '20'), (25, '25')],
            bands=[dict(x0=0, x1=300, tone='sig', op=0.10,
                        label='below 300 items: use Wilson, not this')],
            vlines=[dict(x=50, tone='sig')],
            curves=[dict(pts=[(50, 21.3), (75, 17.4), (100, 15.1), (150, 12.3), (200, 10.6),
                              (300, 8.7), (400, 7.5), (500, 6.7), (700, 5.7), (900, 5.0),
                              (1000, 4.8)],
                         tone='sig', label='interval width at a score of 82%',
                         lat=-1, la='end', dx=-8, dy=14)],
            marks=[dict(x=50, y=21.3, label='21 points wide: [71%, 93%]', tone='sig',
                        dx=10, dy=-6),
                   dict(x=900, y=5.0, label='5 points wide costs 900 items', tone='mem',
                        la='end', dx=-8, dy=-18)],
            foot='four times the items to halve the width: 50 buys 21 points, 200 buys 11, 900 buys 5',
            alt='A falling curve showing the width of the 95% confidence interval against the '
                'number of eval items: 21 points wide at 50 items, 11 at 200, 5 at 900, with the '
                'region below 300 items shaded as the place where the ordinary interval breaks '
                'down'),
        caption=('Your score is a point on this curve, and the curve is why "we ran it on 50 '
                 'prompts" is not a measurement. Everything inside the shaded region is territory '
                 'where the Wald interval is not merely wide but wrong &mdash; quote Wilson there, '
                 'and a smooth bootstrap for continuous scores.'),
        caption_simple=('The picture is a price list. Fifty prompts buys a range twenty-one points '
                        'wide; two hundred buys eleven; nine hundred buys five. Inside the shaded '
                        'strip the simple textbook range stops being trustworthy at all.'),
        when=[
            'Someone reports an eval score with no interval attached',
            'A two-point drop on a 200-item golden set is about to block a release',
            'You are deciding how many prompts to pay humans to label',
            'Your eval reuses the same 40 documents with five questions each',
        ],
        trap=('"The new model got 84% and the old one got 82% on our 200-prompt set, so it is a '
              'two-point win." At 200 items the standard error is about 2.6 points on one score '
              'and 3.8 points on the gap, so the gap is deep inside the noise &mdash; and if both '
              'models saw the same prompts, you threw away the paired analysis that could have '
              'rescued it. The quieter version is running 50 prompts five times each and computing '
              'the interval on 250: that is 50 items, not 250.'),
        real=('Miller&rsquo;s <i>Adding Error Bars to Evals</i> (Anthropic, arXiv:2411.00640, Nov '
              '2024) exists because bare accuracies were being shipped as findings, and its five '
              'recommendations &mdash; CLT standard errors, clustered standard errors, resampling '
              'to cut variance, question-level paired differences, and a power analysis before you '
              'build the eval &mdash; are now the default. The small-N companion guidance is '
              'blunter still: below about 300 items, stop trusting plain standard errors and use '
              'Wilson intervals or a smooth bootstrap. At 82% on 50 items the standard error is '
              '5.4 points.'),
        drills=[
            dict(q='You got 82% on 50 prompts. What is your confidence interval, and what does it stop you claiming?',
                 a=(r'<b>Roughly $[71\%, 93\%]$, and it stops you claiming nearly everything.</b> '
                    r'The standard error is $\sqrt{0.82 \times 0.18 / 50} = 5.4$pp, so the 95% '
                    r'interval is $82\% \pm 10.6$pp; at this $n$ quote Wilson instead, about '
                    r'$[69\%, 90\%]$. A model that is truly 75% and one that is truly 90% both '
                    r'sit inside that, so the eval cannot rank two models, cannot support a '
                    r'launch and cannot detect a two-point regression. It can rule out 50% '
                    r'&mdash; which is occasionally the question you were actually asked.'),
                 a_simple=('<b>Roughly 71% to 93%, and that range stops you claiming almost '
                           'anything.</b> Forty-one right out of fifty gives you about eleven '
                           'points either side. A system that is truly 75% and one that is truly '
                           '90% both fit inside the range, so this eval cannot rank two models, '
                           'cannot justify a launch and cannot spot a small regression. It can '
                           'still rule out something dreadful &mdash; a coin-flip model is well '
                           'outside &mdash; which is sometimes the question you were really '
                           'asked.')),
            dict(q='How many eval examples do you actually need?',
                 a=(r'<b>Ask what difference you need to see, then invert the standard error.</b> '
                    r'The practical anchors: 50&ndash;100 items per slice to see a five-point '
                    r'shift at all, and hundreds to low thousands for one or two points. Written '
                    r'out, $n \approx 16p(1-p)/\delta^{2}$, so a three-point difference near 50% '
                    r'needs about $16(0.25)/0.03^{2} \approx 4{,}400$ items. That falls sharply '
                    r'if both systems are scored on the same items and you test the per-item '
                    r'difference. Bring that number to the labelling budget rather than "a few '
                    r'hundred should be fine".'),
                 a_simple=('<b>Work backwards from the smallest difference you must be able to '
                           'see.</b> Rough anchors: fifty to a hundred items per slice to notice a '
                           'five-point shift, hundreds to low thousands to see one or two points. '
                           'To detect three points you are looking at a few thousand items &mdash; '
                           'unless you score both systems on the same prompts and compare them '
                           'item by item, which cuts the requirement a long way. Take that number '
                           'to the labelling budget instead of "a few hundred should be fine".')),
            dict(q='Your eval is 40 documents with 5 questions each. You reported an interval on 200 items. What is wrong?',
                 a=('<b>The 200 items are not independent, so your interval is too narrow.</b> '
                    'Questions drawn from one document share its difficulty, its formatting and '
                    'its retrieval failures: if the document is missing from the index, all five '
                    'fail together. Cluster the standard errors at the document level &mdash; this '
                    'is Anthropic&rsquo;s second recommendation &mdash; or bootstrap whole '
                    'documents rather than rows. The effective sample size lies between 40 and '
                    '200, closer to 40 as the within-document correlation rises, and the headline '
                    'interval widens accordingly.'),
                 a_simple=('<b>Those two hundred questions are not two hundred independent tries, '
                           'so the range you reported is too narrow.</b> Five questions about the '
                           'same document rise and fall together: if that document is missing from '
                           'the index, all five fail at once. Treat the document as the unit '
                           '&mdash; resample whole documents rather than single questions &mdash; '
                           'and the honest range is much closer to what forty items would give you '
                           'than what two hundred would.')),
        ],
        anchor=dict(
            formula=r'$\mathrm{SE}=\sqrt{\bar{s}(1-\bar{s})/n}$ &nbsp;&middot;&nbsp; '
                    r'$82\%$ on $50$ items $\Rightarrow \pm 10.6$pp',
            formula_simple='The range narrows with the square root of the number of items. Four '
                           'times the prompts to halve it.',
            bullets=[
                'Never report an eval score without its interval &mdash; the interval is the result',
                'Below about 300 items quote Wilson, not the textbook formula',
                'Related questions cluster: the unit is the document, not the question',
                'Size the eval from the difference you need to detect, before you pay for labels',
            ]),
        chips=['Wilson interval', 'clustered standard errors', 'paired eval comparison',
               'power analysis', 'smooth bootstrap', 'benchmark contamination'],
        followup='How many eval examples do you actually need?',
    ),

    # ------------------------------------------------------------------ 3
    dict(
        id='llm-judge-agreement',
        tier='production',
        title='Validating an LLM judge',
        kicker='92% agreement is not a validation. The bar is how often two humans agree, and the number that survives scrutiny is chance-corrected',
        simple=[
            'A judge model marks your outputs so people do not have to. Before you trust it, two '
            'questions. First: how often do two humans agree with each other on the same items? '
            'That is the ceiling, not perfection. If your own annotators agree 85% of the time, a '
            'judge that agrees 85% of the time is simply another annotator, and you can stop '
            'apologising for it.',
            'Second: how much of that agreement is luck? If 95 out of every 100 outputs pass, a '
            'judge that says "pass" to everything agrees with you 95% of the time and has learned '
            'nothing whatsoever. So report a chance-corrected score &mdash; Cohen&rsquo;s kappa '
            '&mdash; which subtracts the agreement you would get by guessing and then asks how '
            'much of the room that was left you actually covered. Print the table of who said what '
            'beside it, because that is where you find out which mistakes the judge is making.',
        ],
        analogy=('<b>Like bringing in a second examiner.</b> You do not test a new marker by '
                 'counting how often they agree with you. You find out how often two experienced '
                 'markers agree with each other, then ask whether the new one lands in the same '
                 'band &mdash; and you look at <i>which</i> papers they disagree on, because '
                 'agreeing on the obvious ones is free.'),
        simple_extra=('Then the biases, each of which you can test in an afternoon. Show the judge '
                      'the same two answers in the opposite order and count how often the verdict '
                      'flips: in the MT-Bench study the strongest judge held its answer only about '
                      'two thirds of the time, and a weaker one under a quarter. Judges also '
                      'prefer longer answers, and they prefer their own family&rsquo;s writing. So '
                      'run every comparison in both orders, count the pairs that flipped as ties, '
                      'and never let a model be the only judge of itself.'),
        trap_simple=('Saying &ldquo;the judge agrees with our humans 92% of the time, so it is '
                     'validated&rdquo;. Ninety-two per cent of what? If nine in ten of your '
                     'examples pass anyway, a judge that always says pass scores ninety per cent '
                     'and is useless. And nobody asked how often two of your own annotators agree, '
                     'which is the number the judge is really competing against.'),
        tech=[
            r'Report a chance-corrected coefficient, never raw agreement: Cohen&rsquo;s '
            r'$\kappa = (p_o - p_e)/(1 - p_e)$, read against Landis and Koch&rsquo;s bands '
            r'&mdash; 0.41&ndash;0.60 moderate, 0.61&ndash;0.80 substantial, above 0.81 almost '
            r'perfect. Pick the right member of the family: Cohen&rsquo;s for two raters on '
            r'nominal labels, Fleiss&rsquo; for more than two, weighted kappa for ordinal 1&ndash;5 '
            r'scales where off-by-one should not cost the same as off-by-four, Krippendorff&rsquo;s '
            r'alpha with missing data, ICC for continuous scores.',
            r'Two things kill a naive validation. The kappa paradox: on a 95%-pass label a judge '
            r'agreeing 94% of the time can have $\kappa \approx 0$, so always publish the '
            r'confusion matrix next to the coefficient. And the bar is human&ndash;human '
            r'agreement, not 100% &mdash; in the MT-Bench work GPT-4 reached 85% agreement with '
            r'human experts on MT-Bench and 87% on Chatbot Arena, against human&ndash;human '
            r'agreement of 81&ndash;82% and about 87%.',
            'Name the biases with their numbers. Position: GPT-4 gave a consistent verdict on only '
            '65% of swapped pairs, Claude-v1 on 23.8%, GPT-3.5 on 46.2% &mdash; so score both '
            'orders and treat a flip as a tie. Verbosity: a repetitive-list attack fooled Claude-v1 '
            'and GPT-3.5 91.3% of the time. Self-enhancement: GPT-4 favoured its own outputs by '
            'about 10 points of win rate, Claude-v1 by about 25.',
        ],
        tech_note=('Then pin the judge. If the provider upgrades the model underneath you, every '
                   'comparison across that boundary is made with a different instrument and your '
                   'quarterly quality trend is partly measuring the judge. Pin a version string, '
                   'keep a frozen set of items you re-score whenever the judge changes, and treat '
                   'a judge upgrade as an experiment in its own right rather than a dependency '
                   'bump.'),
        math=dict(
            tex=r'\kappa = \frac{p_o - p_e}{1 - p_e} \qquad\text{here}\qquad '
                r'\frac{0.940 - 0.941}{1 - 0.941} = -0.02',
            note='94% of the items agreed and the coefficient is still zero, because "always say '
                 'pass" already earns 94.1% on this label distribution. Kappa asks what you did '
                 'with the 5.9% of room that was actually left.',
            cost='two raters, nominal labels'),
        code=dict(
            label='The 94% that means nothing',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
                 '<span class="c"># 200 items. humans passed 190 of them; the judge passed 198</span>\n'
                 '<span class="c">#                 judge pass   judge fail</span>\n'
                 'M = np.array([[<span class="s">188</span>,         '
                 '<span class="s">2</span>],   <span class="c"># human pass</span>\n'
                 '              [ <span class="s">10</span>,         '
                 '<span class="s">0</span>]])  <span class="c"># human fail</span>\n\n'
                 'n  = M.sum()\n'
                 'po = np.trace(M) / n                  '
                 '<span class="c"># 0.940 -- the number in the slide</span>\n'
                 'pe = (M.sum(<span class="s">0</span>) @ M.sum(<span class="s">1</span>)) '
                 '/ n**<span class="s">2</span>     '
                 '<span class="c"># 0.941 -- what "always pass" earns</span>\n'
                 '<span class="k">print</span>((po - pe) / '
                 '(<span class="s">1</span> - pe))       '
                 '<span class="c"># -0.02  <- the honest number</span>\n'
                 '<span class="k">print</span>(M[<span class="s">1</span>].sum(), '
                 'M[<span class="s">1</span>, <span class="s">1</span>])       '
                 '<span class="c"># 10 real failures, 0 of them caught</span>')),
        fig=dict(
            kind='grid',
            head=['WHAT THE JUDGE SAID', 'WHAT IT MISSED'],
            xlab='the judge', ylab='the humans',
            cols=['judge: pass', 'judge: fail'],
            rows=['human: pass', 'human: fail'],
            cells=[
                [dict(t='188', sub='agreed, and easy', tone='mem', fill=True),
                 dict(t='2', sub='false alarms', tone='plain')],
                [dict(t='10', sub='every real failure', tone='sig', fill=True),
                 dict(t='0', sub='caught none of them', tone='sig')],
            ],
            foot='94% raw agreement, kappa -0.02: the judge has learned to say pass',
            alt='A two by two table of judge verdicts against human labels: 188 agreed passes, 2 '
                'false alarms, 10 real failures the judge passed anyway and 0 failures caught, '
                'giving 94 per cent raw agreement and a kappa of about zero'),
        caption=('94% raw agreement and $\\kappa = -0.02$. The judge flagged two good answers and '
                 'waved through all ten failures &mdash; the only items anyone cared about. Raw '
                 'agreement is dominated by the easy cells on the diagonal, which is exactly why '
                 'it flatters.'),
        caption_simple=('The judge agrees with the humans on 94 items out of every 100 and is '
                        'still useless: it missed every single real failure and raised two false '
                        'alarms. Raw agreement counts all the easy items, which is why it '
                        'flatters.'),
        when=[
            'Someone reports that the judge agrees with humans 92% of the time',
            'Your labels are 95% pass and the other 5% is the whole point of the eval',
            'The judge is scoring A against B and nobody has swapped the order',
            'The judge model was silently upgraded between last quarter and this one',
        ],
        trap=('"The judge agrees with our humans 92% of the time." No class balance, no kappa, no '
              'human&ndash;human baseline, and no idea whether the 8% of disagreements are '
              'borderline safety calls or trivia. The paired version is scoring A against B in one '
              'fixed order: on MT-Bench, GPT-4 kept its verdict on only 65% of swapped pairs and '
              'Claude-v1 on 23.8%, so a single fixed order is not measuring quality alone, it is '
              'partly measuring which answer came first.'),
        real=('Zheng et al., <i>Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena</i> (NeurIPS '
              '2023), is the paper to quote: over roughly 3,000 expert votes and 30,000 arena '
              'votes, GPT-4 agreed with humans 85% of the time on MT-Bench and 87% on Chatbot '
              'Arena, against human&ndash;human agreement of 81&ndash;82% and about 87%. The same '
              'paper measured the failure modes: 65% position-swap consistency for GPT-4 and 23.8% '
              'for Claude-v1, a verbosity attack succeeding 91.3% of the time, and self-preference '
              'worth about 10 and 25 points of win rate.'),
        drills=[
            dict(q='Your judge agrees with your human labels 92% of the time. Is the judge good?',
                 a=('<b>Not knowable from that number.</b> Four questions first. What is the class '
                    'balance &mdash; on a 92%-pass eval, "always pass" also scores 92%. What is '
                    'Cohen&rsquo;s kappa, and what does the confusion matrix look like per class? '
                    'What is your human&ndash;human agreement on those same items; if two '
                    'annotators agree 88%, then 92% is above the ceiling and you should suspect an '
                    'easy sample rather than a brilliant judge. And where does the 8% sit &mdash; '
                    'spread over obvious cases is survivable, concentrated on borderline safety '
                    'calls is not.'),
                 a_simple=('<b>You cannot tell yet.</b> Ask four things. How many items pass '
                           'anyway &mdash; if nine in ten do, a judge that always says pass scores '
                           'ninety per cent. What does the score look like once you subtract the '
                           'agreement you would get by guessing? How often do two of your own '
                           'annotators agree on the same items, since that is the real target '
                           'rather than perfection? And are the disagreements on the easy items or '
                           'on the borderline ones the eval exists to catch?')),
            dict(q='What are the known biases of an LLM judge, and what do you do about each?',
                 a=('<b>Three, and each has a cheap control.</b> Position bias: on MT-Bench, GPT-4 '
                    'was consistent on only 65% of swapped pairs, Claude-v1 on 23.8%, GPT-3.5 on '
                    '46.2% &mdash; so evaluate both orders and count flips as ties. Verbosity '
                    'bias: a repetitive-list attack beat Claude-v1 and GPT-3.5 91.3% of the time '
                    '&mdash; so control for length, or score against a rubric with explicit '
                    'criteria. Self-enhancement: GPT-4 preferred its own outputs by around 10 '
                    'points of win rate and Claude-v1 by around 25 &mdash; so never let a model '
                    'family be the sole judge of its own outputs.'),
                 a_simple=('<b>Three, and each has a cheap control.</b> Order: swap which answer '
                           'comes first and the verdict often changes &mdash; the strongest judge '
                           'in the MT-Bench study held its answer about two thirds of the time, a '
                           'weaker one under a quarter. So run both orders and treat the flips as '
                           'ties. Length: judges reward padding, and a repetitive-list trick fooled '
                           'two of them nine times in ten, so score against explicit criteria. '
                           'Family loyalty: a judge favours its own model&rsquo;s writing by ten '
                           'to twenty-five points, so it must never be the only judge of '
                           'itself.')),
            dict(q='Design the validation study for a new judge. How many items, who labels them, what do you report?',
                 a=('<b>Two humans first, on the same stratified sample, then the judge on those '
                    'same items.</b> A few hundred items, stratified so rare-but-important classes '
                    'are not one example each, with borderline cases deliberately over-sampled. '
                    'Measure human&ndash;human agreement and kappa <i>before</i> you look at the '
                    'judge, because that is the target. Then report judge&ndash;human kappa '
                    '(weighted, if the scale is ordinal 1&ndash;5), the confusion matrix, per-class '
                    'agreement, position-swap consistency, and the judge version string. Re-run it '
                    'whenever the judge changes.'),
                 a_simple=('<b>Two humans first, on the same sample, then the judge on those same '
                           'items.</b> Take a few hundred items, deliberately including the hard '
                           'and rare ones rather than a random dribble of easy cases. Have two '
                           'people label them independently and see how often they agree &mdash; '
                           'that is your target. Only then bring in the judge, and report how it '
                           'did after subtracting chance, the full table of who said what, how '
                           'often it changes its mind when you swap the order, and exactly which '
                           'version of the judge you used.')),
        ],
        anchor=dict(
            formula=r'$\kappa = \dfrac{p_o - p_e}{1 - p_e}$ &nbsp;&middot;&nbsp; and the bar is '
                    r'human&ndash;human agreement, not $100\%$',
            formula_simple='Agreement, minus the agreement you would get by guessing, divided by '
                           'the room that was left. The target is how often two people agree.',
            bullets=[
                'Raw agreement is inflated by chance and by class imbalance &mdash; report kappa '
                'and the confusion matrix together',
                'The bar is human&ndash;human agreement on the same items, not perfection',
                'Score both orders and treat a flipped verdict as a tie',
                'Pin the judge version, or your quarterly trend is measuring the judge',
            ]),
        chips=['Cohen&rsquo;s kappa', 'weighted kappa', 'position bias', 'human&ndash;human baseline',
               'judge drift', 'confusion matrix'],
        followup='Your judge agrees with your human labels 92% of the time. Is the judge good?',
    ),

    # ------------------------------------------------------------------ 4
    dict(
        id='prompt-variants',
        tier='production',
        title='Twelve prompt variants is twelve tests',
        kicker='The best of twelve on one eval set is a maximum, and the maximum of noisy scores is biased upward by construction',
        simple=[
            'You wrote twelve prompts, ran all of them against the same two hundred examples, and '
            'the best scored 88 against a baseline of 81. Two separate things went wrong on the '
            'way to that number. The first is familiar: twelve comparisons, each with roughly a '
            'one-in-twenty chance of looking exciting by luck, gives you close to a coin flip that '
            'at least one of them does.',
            'The second is worse and far less known. You did not pick a prompt at random, you '
            'picked the highest &mdash; and the highest of twelve noisy scores is high partly '
            'because it got lucky on those particular examples. So 88 is not that prompt&rsquo;s '
            'quality; it is its quality plus the luck that won it the contest. On a two hundred '
            'item set with twelve variants, the luck alone is worth about four points.',
            'The fix is cheap. Hold out a slice of the eval before you start, never look at it '
            'during the sweep, and report the winner&rsquo;s score on that slice.',
        ],
        analogy=('<b>Like twelve people each flipping a coin ten times.</b> Somebody gets nine '
                 'heads. Report that as "our best flipper&rsquo;s ability" and you have reported '
                 'luck &mdash; next week they flip like everyone else. Hand the winner a fresh ten '
                 'flips before you write anything down.'),
        simple_extra=('The same shape hides in places nobody calls a sweep: hyperparameter '
                      'searches, chunking strategies for retrieval, picking a judge prompt, "we '
                      'tried six models and took the best". An automatic prompt optimiser is the '
                      'worst case rather than the best one &mdash; two hundred candidates scored '
                      'against your dev set is two hundred rolls of the dice with a gradient '
                      'pointing straight at the noise. And reusing one dev set across weeks of '
                      'hand-tuning does exactly the same thing, only slowly.'),
        trap_simple=('Saying &ldquo;we tried twelve prompts and the best got 88&rdquo; as though '
                     '88 were a measurement of that prompt. Then production comes in five points '
                     'lower and the team calls it drift.'),
        tech=[
            r'Two errors stacked on each other. The familiar one is family-wise error: '
            r'$1 - 0.95^{12} \approx 46\%$ chance of at least one spurious winner. The one that '
            r'costs you the launch is selection bias in the estimate itself &mdash; the reported '
            r'score is a maximum, and $\mathbb{E}[\max]$ over noisy estimates sits above the '
            r'truth. This is the winner&rsquo;s curse, Type M error, running inside the '
            r'prompt-engineering loop.',
            r'Put numbers on it. At 85% on a 200-item eval each variant carries a standard error '
            r'of 2.5pp, so twelve <i>equally good</i> variants produce a winner about 4 points '
            r'above the common truth, and a 200-candidate optimiser about 7. Meanwhile the '
            r'observed 88 against 81 is a 7-point gap whose own standard error is 3.6pp before any '
            r'selection effect. Most of what you are about to report can be manufactured.',
            r'Three fixes, in order. Hold out a fresh eval set for the selected prompt &mdash; the '
            r'only fully honest one. Holm or Benjamini&ndash;Hochberg across the variants if you '
            r'need p-values. Max-T or bootstrap-max so the interval accounts for the selection: '
            r'resample items, recompute all twelve scores on every resample, and take the '
            r'distribution of the <i>maximum</i> as your null. Max-T beats Bonferroni here because '
            r'it uses the correlation between variants, which on a shared eval set is high.',
        ],
        tech_note=('Adaptive overfitting happens without an explicit sweep too: reuse one dev set '
                   'across weeks of hand-tuning and you are the optimiser. Recht et al. rebuilt '
                   'the CIFAR-10 and ImageNet test sets following the original collection '
                   'protocols and every model lost 3&ndash;15% &mdash; years of community-wide '
                   'tuning against a fixed public set, with the rankings largely surviving while '
                   'the absolute numbers did not.'),
        math=dict(
            tex=r'\Pr(\text{at least one false winner}) = 1 - (1-\alpha)^{12} = 1 - 0.95^{12} '
                r'\approx 0.46 \qquad\text{and}\qquad \mathbb{E}\!\left[\max_i \hat{s}_i\right] '
                r'> \max_i s_i',
            note='The left half is the one everybody quotes; the right half is the one that costs '
                 'you the launch. Even with the multiplicity corrected, the score of the selected '
                 'variant is still biased upward &mdash; only fresh data removes that.',
            cost='independent variants; correlated ones are milder, not exempt'),
        code=dict(
            label='How much of the win is the sweep',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
                 '<span class="c"># 200-item eval, and every variant is EXACTLY as good as the rest</span>\n'
                 'n, p = <span class="s">200</span>, <span class="s">0.85</span>\n\n'
                 '<span class="k">for</span> k <span class="k">in</span> '
                 '(<span class="s">1</span>, <span class="s">12</span>, '
                 '<span class="s">200</span>):\n'
                 '    s = rng.binomial(n, p, size=(<span class="s">200_000</span>, k)) / n\n'
                 '    <span class="k">print</span>(k, '
                 '<span class="k">round</span>((s.max(axis=<span class="s">1</span>) - p).mean()'
                 '*<span class="s">100</span>, <span class="s">1</span>))\n\n'
                 '<span class="c"># 1   -> 0.0 points   the honest estimate</span>\n'
                 '<span class="c"># 12  -> 4.1 points   a hand sweep, all variants identical</span>\n'
                 '<span class="c"># 200 -> 6.9 points   an optimiser, same null</span>')),
        fig=dict(
            kind='plot',
            xr=(0, 200), yr=(0, 8), ph=190,
            head=['ALL VARIANTS EQUALLY GOOD', 'WHAT THE WINNER SCORES ANYWAY'],
            xlab='prompt variants you tried', ylab='points of pure inflation in the winner',
            xticks=[(1, '1'), (12, '12'), (50, '50'), (100, '100'), (200, '200')],
            yticks=[(2, '2'), (4, '4'), (6, '6'), (8, '8')],
            hlines=[dict(y=7, tone='mem', label='the 88 vs 81 gap you were about to report')],
            vlines=[dict(x=12, tone='sig', label='a hand sweep'),
                    dict(x=200, tone='sig', label='an auto-optimiser')],
            curves=[dict(pts=[(1, 0.0), (2, 1.4), (3, 2.1), (4, 2.6), (6, 3.2), (8, 3.6),
                              (12, 4.1), (20, 4.7), (50, 5.7), (100, 6.3), (200, 6.9)],
                         tone='sig', label='inflation from keeping the best', lat=6,
                         dx=10, dy=-9)],
            marks=[dict(x=12, y=4.1, label='4.1 points', tone='sig', dx=8, dy=15),
                   dict(x=200, y=6.9, label='6.9 points', tone='sig', la='end', dx=-8, dy=17)],
            foot='simulated: a 200-item eval on which every variant is genuinely equally good',
            alt='A rising curve showing how many points the best-scoring variant gains purely by '
                'being selected, against the number of variants tried: about four points at '
                'twelve variants and about seven at two hundred, with a reference line at the '
                'seven-point gap the sweep appeared to produce'),
        caption=('Every variant in this simulation is exactly as good as every other, so the whole '
                 'curve is luck. Twelve prompts on a 200-item eval manufacture around four points '
                 'of improvement and a 200-candidate optimiser around seven &mdash; which is the '
                 'entire gap you were about to take to the PM.'),
        caption_simple=('In this picture every prompt is genuinely equally good. The line is what '
                        'the winner scores anyway, because the winner is whichever one got lucky. '
                        'Twelve tries buys about four points of imaginary improvement; two hundred '
                        'tries buys about seven.'),
        when=[
            'You swept prompts and one of them won',
            'An automated prompt optimiser reports a gain on your dev set',
            'The same golden set has carried six weeks of hand-tuning',
            'Somebody says "we tried six models and picked the best"',
        ],
        trap=('"We tried twelve prompts and the best got 88%." Reporting a selected maximum as '
              'though it were an unbiased estimate, then calling the five-point drop in production '
              'drift or distribution shift. The subtler version: running the sweep, picking the '
              'winner, and then bootstrapping a confidence interval on the winner alone &mdash; '
              'the bootstrap faithfully reproduces the bias, because it never sees the eleven '
              'prompts you rejected.'),
        real=('Recht et al., <i>Do ImageNet Classifiers Generalize to ImageNet?</i> (ICML 2019), '
              'built fresh CIFAR-10 and ImageNet test sets following the original collection '
              'protocols. Accuracy fell 3&ndash;15% across every model, with relative rankings '
              'largely preserved &mdash; years of community-wide tuning against one fixed public '
              'test set, and nobody ran an explicit sweep. The eval-statistics guidance for LLMs '
              'flags the same thing at project scale: a bootstrap interval on "best prompt from a '
              'sweep" needs a max-T correction before it means anything.'),
        drills=[
            dict(q='You swept 12 prompts on a 200-item dev set and the best got 88% against the baseline&rsquo;s 81%. What do you tell your PM?',
                 a=('<b>That 88% is an upward-biased estimate, not a measurement.</b> Three '
                    'sentences. The gap&rsquo;s standard error on 200 items is about 3.6 points '
                    'before any selection effect. Twelve variants that were all equally good would '
                    'still hand you a winner around 4 points above the truth, by construction. So '
                    'the honest line is "promising, needs confirmation on data the sweep never '
                    'saw" &mdash; then get the real number from a held-out slice and expect it to '
                    'land between 81 and 88.'),
                 a_simple=('<b>That 88 is inflated by the way you chose it, not a measurement of '
                           'the prompt.</b> Two facts to say out loud. On two hundred items a '
                           'seven-point gap wobbles by roughly four points either way even without '
                           'a sweep. And twelve equally good prompts would still produce a winner '
                           'about four points above the truth, purely because you kept the '
                           'luckiest one. So call it promising, confirm it on examples the sweep '
                           'never touched, and expect the confirmed number to land between the old '
                           'score and 88.')),
            dict(q='Your automated prompt optimiser tried 200 candidates and gained 6 points on the dev set. Better or worse than a hand sweep of twelve?',
                 a=('<b>Statistically worse, even though it searched better.</b> Two hundred '
                    'candidates is 200-fold selection: on a 200-item dev set where every candidate '
                    'is equally good, the expected inflation is about 7 points &mdash; more than '
                    'the 6 points reported. The optimiser is an extremely efficient dev-set '
                    'fitter, and its score is a training score. Hold out a set it can never query, '
                    'report only that number, and treat any gain that survives as the real one.'),
                 a_simple=('<b>Worse, even though the search itself was better.</b> Two hundred '
                           'attempts means two hundred chances to get lucky, and on a two hundred '
                           'item set that is worth about seven points of imaginary gain &mdash; '
                           'more than the six points it reported. The optimiser is superb at '
                           'fitting the set you gave it, so its score is a training score. Keep a '
                           'set the optimiser can never see, report only that one, and believe '
                           'whatever survives.')),
            dict(q='You have one eval set and no budget to build a second. What is the least-bad option?',
                 a=('<b>Split the one you have, before you look at it.</b> Randomly hold out a '
                    'third, sweep on the remaining two thirds, report the winner on the held-out '
                    'third once, and stop &mdash; the moment you sweep again on the same holdout '
                    'it is a dev set. If the split leaves too few items to say anything, use '
                    'max-T: bootstrap the items, recompute all twelve scores on each resample, and '
                    'use the distribution of the maximum gap as the null. That corrects the '
                    'interval for the selection and, unlike Bonferroni, exploits the correlation '
                    'between variants.'),
                 a_simple=('<b>Split the set you already have, before you look at it.</b> Put a '
                           'third of the items aside at random, run the whole sweep on the rest, '
                           'then score the winner on the reserved third exactly once and stop. '
                           'Sweep on that reserve a second time and it stops being a reserve. If '
                           'the set is too small to split, the fallback is to rebuild the '
                           'comparison by resampling your items many times, recomputing all twelve '
                           'scores each time, and asking how big the best-of-twelve gap gets by '
                           'luck alone. Judge your winner against that.')),
        ],
        anchor=dict(
            formula=r'$1 - 0.95^{12} \approx 46\%$ &nbsp;&middot;&nbsp; and '
                    r'$\mathbb{E}[\max]$ of twelve noisy scores sits above the truth',
            formula_simple='Twelve tries at a one-in-twenty risk is close to a coin flip. And the '
                           'winner of twelve is high partly because it was lucky.',
            bullets=[
                'Twelve variants is twelve tests, and the reported winner is a maximum',
                'A held-out set the sweep never saw is the only fully honest fix',
                'An optimiser with 200 candidates is 200-fold selection, not a smarter search',
                'Bootstrapping the winner alone reproduces the bias &mdash; correct with max-T',
            ]),
        chips=['max-T correction', 'held-out eval set', 'Holm', 'Benjamini&ndash;Hochberg',
               'winner&rsquo;s curse', 'adaptive overfitting'],
        followup='You swept 12 prompts on a 200-item dev set and the best got 88% vs the baseline&rsquo;s 81%. What do you tell your PM?',
    ),

    # ------------------------------------------------------------------ 5
    dict(
        id='paired-comparisons',
        tier='production',
        title='Pairing, win rates and the rank that has an interval',
        kicker='Scoring both models on the same prompts turns an inconclusive result into a decision &mdash; and a leaderboard position is an interval, not a rank',
        simple=[
            'To find out whether model A beats model B, score them on the same prompts and look at '
            'the difference item by item. Most of the noise in an eval is that some prompts are '
            'hard, and pairing cancels it: a hard prompt was hard for both. Two separate runs on '
            'two different samples throw that away, which is how a real difference ends up looking '
            'like nothing.',
            'Worked through. Model A gets 82% and model B gets 79% on the same five hundred '
            'prompts. Compare the two scores separately and their ranges overlap, so the honest '
            'conclusion is "we could not tell". Compare them prompt by prompt and you find thirty '
            'prompts where A was right and B was wrong against fifteen the other way &mdash; a '
            'difference that comfortably clears the noise. Same data, opposite decision, and the '
            'only thing that changed was which comparison you ran.',
        ],
        analogy=('<b>Like timing two runners.</b> Race them side by side on the same hilly course '
                 'on the same morning and a two-second gap means something. Time them on different '
                 'days on different courses and most of the gap is hills and wind. The prompts are '
                 'the course, and you get to decide whether both runners face the same one.'),
        simple_extra=('Two cautions on top. A win rate needs its tie rate printed beside it: '
                      'winning 55% of the time with four ties in every ten is a different claim '
                      'from winning 55% with almost no ties. And a leaderboard position is an '
                      'estimate with a range around it. Put ranges on the scores and three or more '
                      'models routinely turn out to share a place, so "we are third" usually means '
                      '"we are somewhere between first and sixth".'),
        trap_simple=('Saying &ldquo;their ranges overlap, so the two models are the same&rdquo;. '
                     'Overlapping ranges are not a test, and when both models answered the same '
                     'prompts they are the wrong ranges to be looking at. The other one is quoting '
                     'a leaderboard position as though it were a property of the model rather than '
                     'a fact about who else happened to be on the board that week.'),
        tech=[
            r'Pair whenever the same items can be scored by both systems and test the per-item '
            r'difference, $\mathrm{SE} = \sqrt{\mathrm{Var}(s_A - s_B)/n}$. That removes item '
            r'difficulty from the variance and is commonly 3&ndash;10$\times$ more efficient than '
            r'comparing marginal means. Checking two marginal intervals for overlap is not a test '
            r'of the difference at all, and it is the most common way a real win gets thrown '
            r'away.',
            r'The arithmetic, because you will be asked to do it out loud. 500 items, A at 82%, B '
            r'at 79%. Unpaired, the standard error of the difference is '
            r'$\sqrt{0.82(0.18)/500 + 0.79(0.21)/500} = 2.5$pp, so 3 points is $1.2$ standard '
            r'errors and the marginal intervals $[78.6, 85.4]$ and $[75.4, 82.6]$ overlap. Paired '
            r'on the very same items &mdash; 380 both right, 30 A only, 15 B only &mdash; the '
            r'per-item difference has mean 3pp and $\mathrm{SE} = 1.34$pp, giving $t = 2.25$ and '
            r'$p \approx 0.025$.',
            r'A win rate is a paired statistic: $\mathrm{SE} = \sqrt{w(1-w)/n}$ on the non-tie '
            r'subset, with the tie rate reported next to it. Bradley&ndash;Terry and Elo compress '
            r'pairwise outcomes into a scalar but assume conditionally random matchups and a '
            r'stable model pool, which arena leaderboards routinely violate. For ranks, run '
            r'directional pairwise tests, apply Holm, and report the <i>set</i> of ranks each '
            r'model could occupy.',
        ],
        tech_note=('And the leaderboard itself is a selected maximum. <i>The Leaderboard '
                   'Illusion</i> documented 27 private Llama-4 variants tested pre-release with '
                   'only the winner disclosed, alongside data-access asymmetry &mdash; Google '
                   '19.2% and OpenAI 20.4% of all arena data against 29.7% shared between 83 '
                   'open-weight models &mdash; and estimated relative gains of up to 112% on the '
                   'arena distribution from that access. Best-of-N submission with selective '
                   'disclosure is the winner&rsquo;s curse at industry scale.'),
        math=dict(
            tex=r'\mathrm{SE}_{\text{unpaired}} = \sqrt{\frac{\sigma_A^2 + \sigma_B^2}{n}} '
                r'\qquad\qquad \mathrm{SE}_{\text{paired}} '
                r'= \sqrt{\frac{\sigma_A^2 + \sigma_B^2 - 2\rho\,\sigma_A\sigma_B}{n}}',
            note='The entire gain is that last term. Two models that fail on the same hard prompts '
                 'are strongly correlated, and pairing subtracts exactly that correlation. It buys '
                 'you nothing when the two systems make unrelated errors &mdash; which is itself '
                 'worth knowing.',
            cost='requires the same items scored by both systems'),
        code=dict(
            label='The same 500 items, two ways',
            cost='scipy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 '<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
                 '<span class="c"># 380 both right, 30 only A, 15 only B, 75 neither</span>\n'
                 'A = np.array([<span class="s">1</span>]*<span class="s">380</span> + '
                 '[<span class="s">1</span>]*<span class="s">30</span> + '
                 '[<span class="s">0</span>]*<span class="s">15</span> + '
                 '[<span class="s">0</span>]*<span class="s">75</span>)\n'
                 'B = np.array([<span class="s">1</span>]*<span class="s">380</span> + '
                 '[<span class="s">0</span>]*<span class="s">30</span> + '
                 '[<span class="s">1</span>]*<span class="s">15</span> + '
                 '[<span class="s">0</span>]*<span class="s">75</span>)\n'
                 '<span class="k">print</span>(A.mean(), B.mean())              '
                 '<span class="c"># 0.82 0.79</span>\n\n'
                 '<span class="k">print</span>(stats.ttest_ind(A, B, equal_var=<span class="k">'
                 'False</span>).pvalue)  <span class="c"># 0.232 -- as two separate samples</span>\n'
                 '<span class="k">print</span>(stats.ttest_rel(A, B).pvalue)              '
                 '<span class="c"># 0.025 -- the same data, paired</span>\n\n'
                 '<span class="c"># nothing changed but the question: 30 wins against 15 losses,</span>\n'
                 '<span class="c"># and 455 items where both models did the same thing</span>')),
        fig=dict(
            kind='plot',
            xr=(60, 80), yr=(0.4, 6.2), ph=200,
            head=['THE LEADERBOARD', 'WHAT IT CAN SUPPORT'],
            xlab='benchmark score',
            xticks=[(62, '62'), (66, '66'), (70, '70'), (74, '74'), (78, '78')],
            yticks=[(5, 'model A'), (4, 'model B'), (3, 'model C'), (2, 'model D'),
                    (1, 'model E')],
            bands=[dict(x0=72.1, x1=74.4, tone='sig', op=0.12,
                        label='all three intervals cover this')],
            curves=[dict(pts=[(72.1, 5), (76.1, 5)], tone='sig', sw=3.2),
                    dict(pts=[(70.9, 4), (74.9, 4)], tone='sig', sw=3.2),
                    dict(pts=[(70.4, 3), (74.4, 3)], tone='sig', sw=3.2),
                    dict(pts=[(66.0, 2), (70.0, 2)], tone='mem', sw=3.2),
                    dict(pts=[(62.0, 1), (66.0, 1)], tone='mem', sw=3.2)],
            marks=[dict(x=74.1, y=5, label='74.1', tone='sig', la='middle', dx=0, dy=-10),
                   dict(x=72.9, y=4, label='72.9', tone='sig', la='middle', dx=0, dy=-10),
                   dict(x=72.4, y=3, label='72.4', tone='sig', la='middle', dx=0, dy=-10),
                   dict(x=68.0, y=2, label='68.0', tone='mem', la='middle', dx=0, dy=-10),
                   dict(x=64.0, y=1, label='64.0', tone='mem', la='middle', dx=0, dy=-10)],
            foot='illustrative: five models with 95% intervals. A, B and C share one rank',
            alt='A leaderboard drawn as five horizontal confidence intervals, one per model: the '
                'intervals for the top three models overlap heavily so their ranks cannot be '
                'separated, while the fourth and fifth models sit clearly below them'),
        caption=('A leaderboard prints the middle dots and hides the bars. Draw the bars and models '
                 'A, B and C occupy one rank &mdash; "we are third" then carries no information '
                 'that "we are in the top group" did not already carry, and a 1.2-point row '
                 'difference carries none at all.'),
        caption_simple=('A leaderboard shows you the dots and hides the bars. With the bars drawn, '
                        'the top three models are a single group: being third in that group and '
                        'being first are the same claim.'),
        when=[
            'Two models were scored on the same prompts and their intervals overlap',
            'A vendor quotes a 1.2-point lead on a public benchmark',
            'Someone reports a 55% win rate and no tie rate',
            'Marketing asks what being third on an arena board is worth',
        ],
        trap=('"The confidence intervals overlap, so the models are the same." Overlapping marginal '
              'intervals are not a test of the difference, and when both models were scored on the '
              'same items you should never have been looking at the marginal intervals in the '
              'first place: on identical numbers the paired test can come back at p = 0.025 while '
              'the marginals overlap. The second version is treating an Elo gap as a property of '
              'the model when it is a function of which opponents happened to be in the pool that '
              'week.'),
        real=('Neuhof &amp; Benjamini, <i>Quantifying Ranking Uncertainty in LLM Benchmarks</i> '
              '(arXiv:2607.16259, June 2026), built confidence intervals on <i>ranks</i> over MMLU '
              'using PromptEval &mdash; 15 models, 57 subjects, 100 prompt variations, paired '
              't-tests with a Holm correction at the 5% level. Two findings worth quoting: '
              'subject-level variability substantially exceeds prompt-variant variability, and '
              'overlapping intervals routinely put three or more models at the same rank. "We are '
              'third" is usually a claim about a group, not a position.'),
        drills=[
            dict(q='Model A is 1.2 points above Model B on the leaderboard. Is A better?',
                 a=('<b>You cannot tell from a leaderboard row.</b> Four questions: how many items, '
                    'was the comparison paired on the same prompts, what is the standard error of '
                    'the difference, and is 1.2 points larger than the swing you would get from a '
                    'different prompt template? Then the rank question. The June 2026 MMLU '
                    'rank-uncertainty work &mdash; 15 models, 57 subjects, 100 prompt variations '
                    '&mdash; found three or more models routinely sharing a rank once intervals '
                    'were drawn, and 1.2 points is usually inside that.'),
                 a_simple=('<b>Not from a leaderboard row.</b> Ask how many items were scored, '
                           'whether both models saw exactly the same prompts, how much the scores '
                           'wobble, and whether rewriting the prompt template would move things by '
                           'more than one and a bit points &mdash; it usually would. Recent work '
                           'that put ranges around leaderboard positions found three or more '
                           'models sharing a place as a matter of routine. A gap that small is '
                           'normally inside the wobble.')),
            dict(q='Model A 82%, Model B 79% on the same 500 items, and their confidence intervals overlap. Is A better?',
                 a=(r'<b>Probably yes, and the overlapping intervals are the wrong test.</b> '
                    r'Unpaired, the difference has $\mathrm{SE} = 2.5$pp, so 3 points is 1.2 '
                    r'standard errors and the marginals $[78.6, 85.4]$ and $[75.4, 82.6]$ overlap. '
                    r'But the items are shared: with 380 both right, 30 A only and 15 B only, the '
                    r'per-item difference has mean 3pp and $\mathrm{SE} = 1.34$pp, so $t = 2.25$ '
                    r'and $p \approx 0.025$. Report the paired test, the win/loss/tie counts, and '
                    r'the interval on the difference.'),
                 a_simple=('<b>Probably yes, and those overlapping ranges are the wrong thing to '
                           'look at.</b> Both models answered the same five hundred prompts, so '
                           'the question is not how each scored on its own but how often one beat '
                           'the other. If A was right on thirty prompts where B was wrong, and B '
                           'was right on fifteen where A was wrong, that thirty against fifteen is '
                           'the evidence, and it is strong enough to act on. The separate ranges '
                           'hid it because most of their width is prompts being hard, which hit '
                           'both models equally.')),
            dict(q='Your model is third on a public leaderboard. What do you tell the marketing team?',
                 a=('<b>That third means "in the top group", and that is all that goes in '
                    'writing.</b> Rank is an estimate, so give it an interval: directional pairwise '
                    'tests with a Holm correction return the set of ranks the model could occupy, '
                    'and the June 2026 MMLU study found three or more models routinely sharing one. '
                    'Then two caveats. An Elo number is relative to the opponent pool and moves '
                    'when the pool changes. And public boards permit best-of-N private submission '
                    'with only the winner disclosed &mdash; 27 private Llama-4 variants in one '
                    'documented case.'),
                 a_simple=('<b>That third place means "in the leading group", and nothing '
                           'narrower.</b> A rank is a number with a range around it, and when the '
                           'ranges are drawn, three or more models often share a place. Two further '
                           'warnings for anyone writing copy: an arena rating depends on which '
                           'other models happened to be in the pool that week, and teams are '
                           'allowed to enter many private versions of a model and reveal only the '
                           'one that did best &mdash; one study documented twenty-seven private '
                           'variants from a single family.')),
        ],
        anchor=dict(
            formula=r'$\mathrm{SE}_{\text{paired}} = \sqrt{\mathrm{Var}(s_A - s_B)/n}$ '
                    r'&nbsp;&middot;&nbsp; overlapping marginal intervals are not a test',
            formula_simple='Score both models on the same prompts and compare them prompt by '
                           'prompt. Ranges that overlap are not a verdict.',
            bullets=[
                'Pair on the same items and test the difference &mdash; often 3 to 10 times more '
                'efficient',
                'Overlapping marginal intervals are not a test of the difference',
                'A win rate needs its tie rate printed next to it',
                'Ranks have intervals too: three or more models routinely share one',
            ]),
        chips=['paired t-test', 'win rate', 'tie rate', 'Bradley&ndash;Terry', 'Elo',
               'rank confidence intervals'],
        followup='Model A is 1.2 points above Model B on the leaderboard. Is A better?',
    ),
]
