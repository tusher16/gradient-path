CARDS = [dict(
    id='p-value',
    tier='core',
    title='The p-value',
    kicker='Not the probability you are wrong, and the follow-up finds out whether you know that',
    simple=[
        'A test result of this kind answers exactly one question, and it is a strange one. '
        'Assume for a moment that the change you shipped did nothing at all. In that world, '
        'how often would random noise alone hand you a result at least as lopsided as the one '
        'you are holding? A small answer means the noise story is a poor fit. That is the '
        'whole claim.',
        'It does not tell you the chance your change worked. It does not tell you how big the '
        'effect is. It does not tell you the chance you are wrong. Every one of those is a '
        'different question, and reaching for this number to answer them is the mistake the '
        'interviewer is fishing for.',
    ],
    analogy=('<b>Like a smoke alarm.</b> It tells you the air looks unusual for a house with '
             'nothing burning. It does not tell you the odds the house is on fire, and it '
             'certainly does not tell you how big the fire is. For that you need to know how '
             'often houses catch fire, and you need to go and look.'),
    trap_simple=('Saying it is the chance the change did nothing, or the chance you are wrong. '
                 'Both flip the question round. The number starts by assuming the change did '
                 'nothing, so it cannot then tell you how likely that was.'),
    tech=[
        'Under $H_0$, the p-value is $P(T \\geq t_{obs} \\mid H_0)$ &mdash; the probability of a '
        'test statistic at least as extreme as the observed one, in a world where the null '
        'holds. It is a statement about data given a hypothesis, never a hypothesis given data. '
        'Inverting the conditional is the single most common error in the room, and it is the '
        'error the follow-up is built to catch.',
        'Three consequences to say out loud. It is uniform on $[0,1]$ under the null, which is '
        'why peeking inflates the false positive rate and why twelve metrics give you a coin '
        'flip. It carries no information about magnitude, so a significant result on ten million '
        'users can be an effect nobody will ever notice. And $p > 0.05$ is not evidence of no '
        'effect &mdash; absence of a detectable effect at your sample size is compatible with a '
        'large one you were never powered to see.',
    ],
    tech_note=('The 0.05 threshold is a convention Fisher offered as a rough guide, not a '
               'property of the world. What actually determines whether a significant finding is '
               'true is the base rate of true hypotheses in your pipeline: at a 1-in-500 rate of '
               'real breakthroughs, 80% power and 5% alpha, the positive predictive value is '
               'about 3%.'),
    fig=dict(
        kind='grid',
        head=['WHAT THE NUMBER SAYS', 'WHAT YOU ARE ASKED'],
        xlab='the p-value', ylab='effect size',
        cols=['small p', 'large p'],
        rows=['effect worth having', 'effect nobody notices'],
        cells=[
            [dict(t='SHIP IT', sub='and quote the interval', tone='mem', fill=True),
             dict(t='underpowered', sub='not evidence of nothing', tone='sig')],
            [dict(t='significant, useless', sub='report the interval', tone='sig', fill=True),
             dict(t='nothing here', sub='stop and say so', tone='plain')],
        ],
        foot='the interview lives in the two right-hand cells, not the top-left one',
        alt='A two by two table mapping p-value and effect size onto what you should actually do'),
    caption=('The p-value only picks a column. The row is the confidence interval, and it is the '
             'row that decides whether anyone should care. A candidate who reports only the '
             'column has answered half the question.'),
    caption_simple=('The test result only tells you which column you are in. How big the effect '
                    'is tells you which row &mdash; and the row is what decides whether the '
                    'change was worth shipping.'),
    when=[
        'A PM asks whether the experiment "worked" and wants one number',
        'A result is significant and the effect is 0.4% on a metric nobody tracks',
        'An experiment came back at p = 0.31 and someone concludes the feature does nothing',
        'You are about to test twelve metrics on the same experiment',
    ],
    trap=('Saying it is "the probability the null is true" or "the probability we are wrong". '
          'Both invert the conditional. The sharper version of the trap, and the one Meta '
          'actually asks: p = 0.03 with a confidence interval of [0.1%, 0.9%] and a PM who says '
          '"so there is a 97% chance this is positive" &mdash; the correct response is that the '
          'number does not licence that sentence, and that the interval says the effect is real '
          'but almost certainly too small to matter.'),
    math=dict(
        tex=r'p = P\bigl(T \geq t_{\text{obs}} \mid H_0\bigr) \qquad \text{not} \qquad P\bigl(H_0 \mid \text{data}\bigr)',
        note='The two sides differ by the base rate, which the p-value never sees. Getting from '
             'the left to the right needs Bayes and a prior you have to defend.',
        cost='a conditional, in one direction only'),
    code=dict(
        label='What uniformity under the null actually looks like',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             '<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n'
             'p = [stats.ttest_ind(rng.normal(size=<span class="s">400</span>),\n'
             '                     rng.normal(size=<span class="s">400</span>)).pvalue\n'
             '     <span class="k">for</span> _ <span class="k">in</span> <span class="k">range</span>(<span class="s">20000</span>)]\n\n'
             '<span class="c"># both samples come from the SAME distribution: the null is true</span>\n'
             '<span class="k">print</span>(np.mean(np.array(p) &lt; <span class="s">0.05</span>))  '
             '<span class="c"># ~0.05 -- that is the definition, not a bug</span>\n'
             '<span class="k">print</span>(np.mean(np.array(p) &lt; <span class="s">0.31</span>))  '
             '<span class="c"># ~0.31. uniform. every threshold is its own false positive rate</span>')),
    real=('The 2016 American Statistical Association statement on p-values exists because this '
          'error reached the point of retracting journals: <i>Basic and Applied Social '
          'Psychology</i> banned p-values outright in 2015. The concrete cost shows up in '
          'industry as p-hacking &mdash; Amgen could reproduce only 6 of 53 landmark cancer '
          'studies (Begley &amp; Ellis, Nature 2012), and the surviving explanation is not fraud '
          'but thousands of researchers each testing many hypotheses at 5% and publishing the '
          'ones that cleared it.'),
    drills=[
        dict(q='p = 0.03, the confidence interval is [0.1%, 0.9%], and the PM says there is a 97% chance this is positive. Respond.',
             a=('<b>The 97% sentence is not something this number can support.</b> The p-value is '
                '$P(\\text{data} \\mid H_0)$; the PM has asked for $P(H_0 \\mid \\text{data})$, '
                'and getting between them needs a prior. Then redirect to the interval, which is '
                'the part that actually decides: the effect is almost certainly real and almost '
                'certainly between 0.1% and 0.9%, so the real question is whether a 0.5% lift '
                'pays for the maintenance cost of the feature.'),
             a_simple=('<b>The ninety-seven percent sentence is not something this test can '
                       'support.</b> The test starts by assuming the change did nothing, so it '
                       'cannot then tell you how likely that assumption was. What you can say is '
                       'the useful part: the range of plausible effects runs from about a tenth '
                       'of a percent to about nine tenths of a percent, so the effect is probably '
                       'real and probably too small to be worth the upkeep.')),
        dict(q='The experiment came back at p = 0.31. Can we conclude the feature has no effect?',
             a=('<b>No &mdash; you can only conclude you had insufficient power to detect one.</b> '
                'Absence of evidence is not evidence of absence. Report the interval instead: if '
                'it is $[-2\\%, +6\\%]$ you have learned almost nothing and the honest answer is '
                'that the experiment was underpowered. If it is $[-0.2\\%, +0.3\\%]$ you have '
                'ruled out anything worth having, which is a real and shippable finding. The '
                'width of the interval, not the p-value, is what distinguishes those two cases.'),
             a_simple=('<b>No &mdash; you can only say you could not detect one.</b> Look at the '
                       'range of plausible effects instead. If it stretches from a two percent '
                       'loss to a six percent gain, you have learned nothing and the test was too '
                       'small. If it sits between roughly nothing and roughly nothing, you have '
                       'genuinely ruled out an effect worth caring about. Same test result, '
                       'completely different conclusion.')),
        dict(q='Why does testing twelve metrics on one experiment change how you read each p-value?',
             a=('<b>Because under the null the p-value is uniform, so each test is an independent '
                '5% chance to embarrass you.</b> With twelve independent metrics the probability '
                'of at least one false positive is $1 - 0.95^{12} \\approx 46\\%$. The fix is to '
                'name one OEC before you launch and treat the rest as guardrails with a '
                'correction &mdash; Bonferroni if you want simplicity, Benjamini-Hochberg if you '
                'care about power across many metrics.'),
             a_simple=('<b>Because each extra metric is another roll of the same loaded dice.</b> '
                       'Every metric you check has about a one-in-twenty chance of looking '
                       'exciting by luck alone. Check twelve and the chance that at least one '
                       'does is close to a coin flip. The fix is to pick the one metric that '
                       'decides the launch before you start, and treat everything else as a '
                       'safety check rather than a result.')),
    ],
    anchor=dict(
        formula=r'$P(\text{data} \mid H_0)$ &nbsp;&middot;&nbsp; never &nbsp;&middot;&nbsp; $P(H_0 \mid \text{data})$',
        formula_simple='It assumes nothing happened, then asks how surprising your data would be. That is all.',
        bullets=[
            'It is a statement about data given a hypothesis, never the reverse',
            'It carries no information about size &mdash; the interval does that',
            'A large p-value is not evidence of no effect, it is evidence of no power',
        ]),
    chips=['confidence interval', 'statistical power', 'multiple comparisons',
           'base rate', 'Benjamini-Hochberg'],
    followup='p = 0.03 with a confidence interval of [0.1%, 0.9%] and a PM claiming a 97% chance of a positive effect — what do you say?',
)]
