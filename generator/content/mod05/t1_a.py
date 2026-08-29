# Module 05 -- Tier 1 (Foundation), batch A.
# Sources: /tmp/gp/research/stats_research.md sections F1-F5, section 1, Appendix A/B/C.

_SKEW = [(-1.75, 0), (-1.5, 0.021), (-1.25, 0.187), (-1, 0.408), (-0.75, 0.533),
         (-0.5, 0.547), (-0.25, 0.493), (0, 0.413), (0.25, 0.33), (0.5, 0.257),
         (0.75, 0.197), (1, 0.15), (1.25, 0.113), (1.5, 0.085), (1.75, 0.064),
         (2, 0.048), (2.25, 0.036), (2.5, 0.027), (2.75, 0.021), (3, 0.016),
         (3.25, 0.012), (3.5, 0.009), (3.75, 0.007), (4, 0.006), (4.25, 0.004),
         (4.5, 0.003), (4.75, 0.003), (5, 0.002)]

_NORM = [(-3.2, 0.002), (-2.95, 0.005), (-2.7, 0.01), (-2.45, 0.02), (-2.2, 0.035),
         (-1.95, 0.06), (-1.7, 0.094), (-1.45, 0.139), (-1.2, 0.194), (-0.95, 0.254),
         (-0.7, 0.312), (-0.45, 0.361), (-0.2, 0.391), (0.05, 0.398), (0.3, 0.381),
         (0.55, 0.343), (0.8, 0.29), (1.05, 0.23), (1.3, 0.171), (1.55, 0.12),
         (1.8, 0.079), (2.05, 0.049), (2.3, 0.028), (2.55, 0.015), (2.8, 0.008),
         (3.05, 0.004), (3.3, 0.002), (3.55, 0.001)]

# week-1 / week-2 scores for the same simulated users, no intervention at all
_SEL = [(2.8, 4.3), (1.8, 3.6), (2.9, 2.2), (1.9, 2.6), (3.0, 5.5), (0.6, 3.8), (2.5, 5.8)]
_REST = [(5.4, 7.6), (6.0, 3.3), (4.9, 6.5), (3.7, 4.7), (4.5, 3.9), (3.5, 7.5), (5.5, 6.7),
         (7.9, 4.9), (4.5, 5.0), (4.2, 5.7), (6.3, 5.6), (6.1, 6.9), (5.6, 5.4), (3.6, 5.5),
         (5.3, 7.7), (6.7, 5.1), (4.5, 4.2), (5.0, 4.8), (5.9, 7.5), (5.7, 3.5), (5.0, 3.9),
         (4.4, 1.7), (5.3, 4.6), (5.6, 5.4), (4.5, 6.0), (3.5, 3.9), (3.9, 4.0), (7.4, 6.1),
         (3.9, 7.0), (5.3, 4.7), (7.1, 5.8), (4.3, 5.3), (5.2, 5.1), (5.6, 5.2), (5.5, 3.7),
         (3.1, 4.1), (5.5, 4.8)]


CARDS = [

# ============================================================ F1
dict(
    id='bayes-base-rate',
    tier='foundation',
    title='Bayes is a base-rate machine',
    kicker='Everyone can state the rule &mdash; the follow-up finds out whether you noticed the base rate is doing all the work',
    simple=[
        'Two numbers decide whether a positive result means anything, and only one of them is '
        'the accuracy of the test. The other is how common the thing was before you tested. A '
        'model that is right ninety-nine times in a hundred sounds decisive. Point it at '
        'something that happens once in a thousand and screen a thousand cases: one case is '
        'real and the model catches it, but it also mislabels one in every hundred of the 999 '
        'that are fine, which is ten more. Eleven alarms, one of them real. Nine per cent.',
        'Nothing about the model is broken. It is doing exactly what the accuracy figure says '
        'it does. Rare-event arithmetic is what turns a very good detector into a queue of '
        'false alarms, and it is why you cannot judge a screening system by its accuracy '
        'alone. When someone hands you a headline accuracy without a prevalence, you have been '
        'handed half a number, and the missing half is usually the bigger one.',
    ],
    analogy=('<b>Like a metal detector on a beach.</b> It beeps for almost every coin and '
             'hardly ever misses one. But there are ten thousand bottle tops for every ring, '
             'so nearly everything it beeps at is rubbish. Nobody blames the detector. The '
             'beach decides what the beeps are worth.'),
    simple_extra=(
        'The version worth memorising is a multiplication. Start with the odds before you '
        'tested, one in a thousand. Multiply by how much more often the model shouts for a '
        'real case than for a clean one, which here is ninety-nine to one. That leaves you at '
        'roughly one in ten, which is the nine per cent. Every further piece of genuinely new '
        'evidence multiplies again &mdash; and evidence that merely repeats what you already '
        'counted multiplies by one, which is to say it does nothing at all.'),
    trap_simple=(
        'Saying the model is ninety-nine per cent accurate and stopping there. Or flipping the '
        'question round: because the test is right ninety-nine times in a hundred, there is a '
        'ninety-nine per cent chance this flagged account is fraud. That sentence swaps the two '
        'directions of the question and never mentions how rare fraud was to begin with.'),
    tech=[
        r'$P(H \mid D) = P(D \mid H)P(H)/P(D)$, and in every interview version of this the '
        r'prior dominates the answer. At 0.1% prevalence with 99% sensitivity and 99% '
        r'specificity, the positive predictive value is $0.99(0.001) / [0.99(0.001) + '
        r'0.01(0.999)] \approx 9\%$. The textbook screening variant &mdash; 1% prevalence, 99% '
        r'sensitivity, 95% specificity &mdash; comes out at 16.7%. Neither is anywhere near '
        r'99%, and neither number moves if you improve sensitivity, because there was only ever '
        r'one true case to find.',
        r'Say it in odds form and the whole family of these questions collapses to one line: '
        r'prior odds $\times$ likelihood ratio $=$ posterior odds. Prior odds $1{:}999$, '
        r'$LR^{+} = \text{sens}/(1-\text{spec}) = 99$, posterior odds $99{:}999$, the same 9%. '
        r'The odds form is also what makes the next question tractable: a second, '
        r'<i>conditionally independent</i> test multiplies by 99 again, taking you to about '
        r'$9.8{:}1$, or 91%. Conditional independence is the load-bearing phrase, and it is '
        r'exactly what is false when the second test is the same model re-run on the same '
        r'features.',
    ],
    tech_note=(
        r'The same arithmetic runs on your experiment pipeline. At $\alpha = 0.05$ and 80% '
        r'power, the probability that a significant result reflects a real effect is '
        r'$0.8\pi/[0.8\pi + 0.05(1-\pi)]$. At a one-in-three hit rate for your ideas that is '
        r'89%; at Bing&rsquo;s breakthrough rate of one in five hundred it collapses to 3.1%. '
        r'The prior is not a refinement you add at the end. It is most of the answer.'),
    fig=dict(
        kind='blocks', h=208,
        boxes=[
            dict(x=28, y=74, w=144, h=54, t='1,000 accounts', sub='one day of traffic'),
            dict(x=216, y=34, w=150, h=48, t='1 is fraud', sub='the base rate'),
            dict(x=216, y=120, w=150, h=48, t='999 are fine', sub='the other 99.9 per cent'),
            dict(x=414, y=34, w=152, h=48, t='1 flagged', sub='99 in 100 caught', tone='mem'),
            dict(x=414, y=120, w=152, h=48, t='10 flagged', sub='1 in 100 of the 999', tone='sig'),
            dict(x=598, y=74, w=104, h=54, t='11 alarms', sub='9 per cent real', tone='mem'),
        ],
        links=[dict(a=0, b=1), dict(a=0, b=2), dict(a=1, b=3), dict(a=2, b=4, tone='sig'),
               dict(a=3, b=5), dict(a=4, b=5, tone='sig')],
        labels=[dict(x=34, y=16, t='WHAT YOU SCREEN', a='start'),
                dict(x=686, y=16, t='WHAT THE OPS TEAM SEES', a='end')],
        foot='the 99 per cent never changes; the base rate decides everything',
        alt='One thousand accounts split into one fraudulent and 999 clean, then into one true '
            'alarm and ten false alarms, giving eleven alarms of which one is real'),
    caption=('Ten of the eleven alarms come out of the bottom row, and the bottom row is 999 '
             'people. Push specificity from 99% to 99.5% and that row halves, taking precision '
             'from 9% to about 17%. Push sensitivity and almost nothing happens, because there '
             'was one true case available. The figure tells you which knob is worth engineering '
             'effort.'),
    caption_simple=('Ten of the eleven alarms come from the big group at the bottom, and that '
                    'group is 999 people. Making the model better at clearing innocent cases '
                    'halves that row and roughly doubles the share of real alarms. Making it '
                    'better at catching guilty ones barely moves anything, because there was '
                    'only ever one real case to catch.'),
    when=[
        'A model is reported at 99% accuracy and nobody has said how rare the event is',
        'The ops team says the review queue is mostly noise and the model owner says the offline metrics are fine',
        'Someone quotes a test result as if it were the probability the thing is true',
        'You are asked what a second, independent check would actually buy you',
    ],
    trap=(r'"The model is 99% accurate, so a flagged account is 99% likely to be fraud." That '
          r'is the prosecutor&rsquo;s fallacy with a dashboard attached &mdash; it swaps '
          r'$P(\text{flag} \mid \text{fraud})$ for $P(\text{fraud} \mid \text{flag})$. The '
          r'quieter half of the trap is quoting precision measured on a rebalanced test set: a '
          r'90% precision figure from a set that is half fraud tells you nothing at all about a '
          r'stream that is 0.05% fraud.'),
    math=dict(
        tex=r'\underbrace{\frac{P(H)}{P(\lnot H)}}_{\text{prior odds } 1:999} \times '
            r'\underbrace{\frac{P(D \mid H)}{P(D \mid \lnot H)}}_{LR^{+}=99} = '
            r'\underbrace{\frac{P(H \mid D)}{P(\lnot H \mid D)}}_{\approx 1:10}',
        note='Two independent pieces of evidence multiply their likelihood ratios. Two '
             'correlated ones do not, and the second is worth far less than 99 &mdash; often '
             'worth exactly 1.',
        cost='a prior you have to defend out loud'),
    code=dict(
        label='Where the thousand accounts go, and what a second pass buys',
        cost='no dependencies',
        src=('prev, sens, spec = <span class="s">0.001</span>, <span class="s">0.99</span>, '
             '<span class="s">0.99</span>\n\n'
             'tp = prev * sens              '
             '<span class="c"># 0.00099 -- the one real case, caught</span>\n'
             'fp = (<span class="s">1</span> - prev) * (<span class="s">1</span> - spec)  '
             '<span class="c"># 0.00999 -- ten clean accounts, flagged</span>\n'
             '<span class="k">print</span>(tp / (tp + fp))       '
             '<span class="c"># 0.090. nine per cent of the queue is real</span>\n\n'
             '<span class="c"># the same thing in odds, which is the form that scales</span>\n'
             'prior = prev / (<span class="s">1</span> - prev)   '
             '<span class="c"># 1 : 999</span>\n'
             'lr    = sens / (<span class="s">1</span> - spec)   '
             '<span class="c"># 99</span>\n'
             '<span class="k">print</span>(prior * lr)           '
             '<span class="c"># 0.099, so 9 per cent</span>\n'
             '<span class="k">print</span>(prior * lr * lr)      '
             '<span class="c"># 9.81, so 91 per cent -- but ONLY if the two</span>\n'
             '                              '
             '<span class="c"># tests are conditionally independent. Re-running</span>\n'
             '                              '
             '<span class="c"># the same model on the same features is not.</span>')),
    real=('<i>R v Sally Clark</i> (UK, 1999). Roy Meadow testified that the chance of two cot '
          'deaths in one family was "1 in 73 million", multiplying two probabilities that were '
          'not independent and never once comparing the figure against the prior odds of a '
          'mother murdering two of her children. Clark served three years; the conviction was '
          'quashed in 2003 and the Royal Statistical Society issued a formal protest in 2001. '
          'Both failures on this card &mdash; a missing base rate and an assumed independence '
          '&mdash; inside a single sentence spoken in court.'),
    drills=[
        dict(q='Your screening model is 99% accurate on a one-in-a-thousand event, so only 9% of its alerts are real. The team proposes running it twice. What does the second pass buy you?',
             a=(r'<b>Nothing as described &mdash; and a great deal if the second test is '
                r'genuinely independent.</b> In odds form the first pass takes $1{:}999$ to '
                r'about $1{:}10$ by multiplying in a likelihood ratio of 99. A second pass '
                r'multiplies by 99 again, giving roughly $9.8{:}1$, about 91%. That factor '
                r'exists only under conditional independence given the true label. Re-running '
                r'the same model on the same features has $LR \approx 1$: it repeats evidence '
                r'you already counted. What earns the second 99 is a different signal source '
                r'&mdash; device history, a payment-network check, a human reviewer. '
                r'Multiplying dependent evidence is precisely the Sally Clark error.'),
             a_simple=('<b>Nothing, unless the second check looks at something new.</b> The '
                       'first pass moves the odds from one in a thousand to about one in ten. A '
                       'genuinely separate check with the same hit rate would multiply again '
                       'and take you to roughly nine in ten. But running the same model over '
                       'the same data twice just repeats itself, so it multiplies by one and '
                       'you have gained nothing. What earns the improvement is a different kind '
                       'of evidence &mdash; the device, the payment network, a human reviewer '
                       '&mdash; not a second look at the same thing.')),
        dict(q='Your fraud model shows 90% precision on the test set. Fraud is 0.05% of live traffic. What will the ops team actually see, and what do you change?',
             a=('<b>A queue that is almost entirely false positives, and the test set is why '
                'you did not see it coming.</b> A 90% precision figure measured on a balanced '
                'or negatively-downsampled set does not transfer; recompute the positive '
                'predictive value at the true 0.05% prevalence and it collapses by orders of '
                'magnitude. Three moves, in order: raise the threshold and report precision@k '
                'at the volume ops can genuinely review; add a cheap second stage built on '
                'independent features; and change the reported metric from precision on a '
                'curated set to precision at the operating point on live traffic.'),
             a_simple=('<b>A review queue that is almost all false alarms.</b> The ninety per '
                       'cent figure came from a test set where fraud had been made artificially '
                       'common, and it does not survive contact with traffic where fraud is one '
                       'case in two thousand. Recompute the hit rate at the real rate first. '
                       'Then either raise the bar so the model only shouts about the cases it '
                       'is most sure of, sized to what the team can actually review, or add a '
                       'second check that looks at different evidence entirely.')),
        dict(q='An A/B result comes back significant at the 5% level with 80% power. How likely is the effect real?',
             a=(r'<b>Unanswerable without the base rate, which is the whole point of the '
                r'question.</b> The positive predictive value is $0.8\pi/[0.8\pi + '
                r'0.05(1-\pi)]$, where $\pi$ is the share of your ideas that are genuinely '
                r'good. At $\pi = 1/3$ that is 89%; at Bing&rsquo;s breakthrough rate of '
                r'$\pi = 1/500$ it is 3.1%. So the honest answer names $\pi$ for your own team: '
                r'if nine in ten of your experiments come back flat, most of your significant '
                r'results are noise, and the moves that help are better hypotheses, more power, '
                r'and replicating anything surprising.'),
             a_simple=('<b>You cannot say without knowing how often your ideas work at all.</b> '
                       'If about a third of what your team tries is genuinely good, then close '
                       'to nine in ten significant results are real. If only one idea in five '
                       'hundred is a breakthrough, as at Bing, then only about three in a '
                       'hundred significant results are real and the rest are noise that '
                       'cleared the bar. The rate at which your team has good ideas is the '
                       'missing input, and it matters more than the test does.')),
    ],
    anchor=dict(
        formula=r'$\text{prior odds} \times LR^{+} = \text{posterior odds}$ '
                r'&nbsp;&middot;&nbsp; $1{:}999 \times 99 \approx 1{:}10$',
        formula_simple='Start with how common the thing is, then multiply by how much louder '
                       'the model shouts for a real case than a clean one. That product, not '
                       'the accuracy, is your answer.',
        bullets=[
            'Accuracy without prevalence is half a number &mdash; ask for the base rate first',
            'Odds form makes it one multiplication, and makes the independence assumption visible',
            'A second check only multiplies again if it looks at genuinely new evidence',
        ]),
    chips=['positive predictive value', 'precision at k', 'calibration', 'prior odds',
           'conditional independence'],
    followup='Your screening model is 99% accurate on a one-in-a-thousand event, so only 9% of its alerts are real &mdash; what changes if you screen twice?',
),

# ============================================================ F2
dict(
    id='clt-skew',
    tier='foundation',
    title='The CLT does not rescue skewed metrics',
    kicker='"We have well over thirty samples, so it is normal" is the most confidently wrong sentence in a stats round',
    simple=[
        'The rule everyone half-remembers says averages settle into a neat bell shape once the '
        'sample is big enough. That is true, with a catch nobody quotes: how big is big enough '
        'depends entirely on how lopsided your data are. Money metrics are the most lopsided '
        'things you own. Revenue per user is mostly zeros with a handful of people spending '
        'thousands, and the average of a hundred such users is still visibly lopsided, nothing '
        'like a bell.',
        'The consequence is practical rather than theoretical. Every interval and every test '
        'you run on that average quietly assumes the bell shape has already arrived. When it '
        'has not, the error rates your software prints are not the ones you are getting, and '
        'an experiment that looks flat may simply be far too small to see anything. '
        'Microsoft&rsquo;s experimenters put a number on it: for their revenue-per-user metric '
        'you need over a hundred thousand people in each arm before the maths behaves, and most '
        'teams budget a small fraction of that.',
    ],
    analogy=('<b>Like waiting for a queue to average out.</b> Most people at the counter take a '
             'minute. Once an hour, someone takes forty. Average ten customers and that one '
             'visit swamps everything; average ten thousand and it barely registers. The '
             'service is identical either way. Only the number of people decides whether the '
             'average can be trusted.'),
    simple_extra=(
        'You have two honest ways out, and both are decisions rather than tricks. Cap the '
        'metric at a level you announce before you look at the data &mdash; capping revenue per '
        'user at Bing cut its lopsidedness from eighteen to about five, which cut the users '
        'needed by roughly eleven times &mdash; or measure something bounded instead, such as '
        'whether a person bought at all rather than how much they spent. Capping trades a '
        'little bias for a lot of precision. That is a fair trade, and it stops being fair the '
        'moment you choose the cap after seeing the result.'),
    trap_simple=(
        'Reaching for a rank-based test because the data are not bell-shaped, then reporting '
        'the outcome as a percentage lift in revenue. Rank tests answer whether one group tends '
        'to come out ahead of the other. Revenue is a total, and a total is built out of an '
        'average. You have quietly answered a different question from the one the business '
        'asked, and the number you hand over cannot be defended.'),
    tech=[
        r'The theorem is a statement about the sampling distribution of $\bar{X}$, not about '
        r'your data, and the rate of convergence is governed by skewness: '
        r'$\mathrm{skew}(\bar{X}) = s/\sqrt{n}$. Kohavi&rsquo;s Rule 7 turns that into a '
        r'number you can use in a planning meeting &mdash; you need at least $355 s^{2}$ users '
        r'per arm before the t-test&rsquo;s normal approximation is trustworthy, where $s$ is '
        r'the skewness coefficient. Bing&rsquo;s Revenue/User has $s = 17.9$, so '
        r'$355 \times 17.9^{2} \approx 114{,}000$ per arm, and that only buys 4.4% sensitivity.',
        r'Nearly every metric with money or time in it is heavy-tailed: revenue per user, '
        r'session length, items per order, tokens per request, LLM latency. Offer the fixes in '
        r'this order. Cap or winsorise at a pre-declared percentile &mdash; capping at Bing '
        r'took $s$ from 18 to 5.3, and $355 \times 5.3^{2} \approx 10{,}000$, an elevenfold cut '
        r'in the sample required. Switch to a bounded proxy such as purchaser rate. Bootstrap '
        r'the interval. Or change the randomisation and analysis unit. Capping buys variance '
        r'reduction with bias, which is a decision you state before launch, never after seeing '
        r'the lift.',
    ],
    tech_note=(
        r'Two diagnostics that do not work. Shapiro&ndash;Wilk on the raw data answers the '
        r'wrong question and, at $n$ in the hundreds of thousands, rejects every time &mdash; '
        r'you need normality of the sampling distribution, not of the data. And a histogram of '
        r'the metric says nothing directly about the distribution of its mean. What does work: '
        r'bootstrap the mean and look at the shape you get, and run A/A tests to check the false '
        r'positive rate lands near 5%.'),
    fig=dict(
        kind='plot',
        head=['100 USERS PER ARM', '114,000 USERS PER ARM'],
        xr=(-3.3, 5.0), yr=(0, 0.63), ph=196,
        xlab='standard errors from the true mean', ylab='where the average lands',
        xticks=[(-2, '-2'), (0, '0'), (2, '+2'), (4, '+4')],
        vlines=[dict(x=-1.96, tone='mute', label='thinner than 2.5 per cent'),
                dict(x=1.96, tone='mute', label='fatter than 2.5 per cent')],
        curves=[dict(pts=_NORM, tone='mem', label='symmetric by now', lat=6, dx=-6, dy=-9,
                     la='end'),
                dict(pts=_SKEW, tone='sig', label='one long tail, one short', lat=15, dx=10,
                     dy=-12)],
        foot='the average inherits the skew of the data divided by the square root of n',
        alt='Two curves for how a sample average lands. At 100 users per arm it is strongly '
            'lopsided with a long right tail; at 114,000 it is symmetric'),
    caption=('Same metric, same test, same code. Only the sample size differs. At a hundred '
             'users per arm the distribution of the average is still lopsided, so the tail '
             'probabilities your t-test quotes are wrong in both directions at once &mdash; too '
             'little mass on the left, too much on the right. The 355 rule is where that stops '
             'being true.'),
    caption_simple=('Both curves show the same metric measured the same way, and only the '
                    'number of users differs. With a hundred users the average is still '
                    'lopsided, so the error rates your test prints are not the ones you are '
                    'getting: too few surprises on one side and too many on the other. The bell '
                    'shape does arrive. The question is whether it has arrived at your sample '
                    'size.'),
    when=[
        'The metric has money, time or tokens in it and the team wants a t-test',
        'A revenue-per-user experiment came back flat after two weeks and someone calls it a null',
        'Somebody justifies a test with "we have well over thirty samples"',
        'You are asked how long to run a revenue experiment and the honest answer feels absurdly long',
    ],
    trap=(r'"The data are not normal, so I will use Mann&ndash;Whitney." The U test asks '
          r'whether one group stochastically dominates the other; the business asked about '
          r'total revenue, which is a mean. You have changed the question without announcing '
          r'it, and the percentage lift you report afterwards cannot be derived from the test '
          r'you ran. The mirror-image trap is "40,000 per arm, way past 30" &mdash; the 30 rule '
          r'has no skewness term in it, and at $s = 17.9$ you are still four times short.'),
    math=dict(
        tex=r'\mathrm{skew}(\bar{X}) = \frac{s}{\sqrt{n}} \qquad\Longrightarrow\qquad '
            r'n \;\gtrsim\; 355\,s^{2} \quad \text{per arm}',
        note='The 355 is a rule of thumb calibrated for a t-test at 5% with the tails behaving. '
             'The $s^{2}$ is not negotiable: halving the skewness quarters the sample you need.',
        cost='skewness measured on your own metric, before the test'),
    code=dict(
        label='Has the bell shape arrived on your metric yet?',
        cost='numpy, scipy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             '<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
             '<span class="c"># rev: one row per user, revenue over the period</span>\n'
             's = stats.skew(rev)\n'
             '<span class="k">print</span>(s, <span class="s">355</span> * s**<span class="s">2</span>)   '
             '<span class="c"># skewness, and the users per arm it demands</span>\n\n'
             '<span class="c"># the honest check: is the SAMPLING distribution symmetric yet?</span>\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n'
             'idx = rng.integers(<span class="s">0</span>, <span class="k">len</span>(rev), '
             'size=(<span class="s">20000</span>, <span class="s">100</span>))\n'
             '<span class="k">print</span>(stats.skew(rev[idx].mean(axis=<span class="s">1</span>)))\n'
             '<span class="c"># about s / sqrt(100). at s = 17.9 that is 1.8 -- still miles off</span>')),
    real=('Microsoft&rsquo;s <i>Seven Rules of Thumb for Web-Site Experimenters</i> (KDD 2014) '
          'exists because Bing teams repeatedly shipped and killed features on underpowered '
          'revenue metrics. Rule 7 is written as a direct correction, with a table of 355 times '
          'the squared skewness alongside per-metric sensitivities: Revenue/User at a skewness '
          'of 17.9 needs about 114,000 users per arm just to reach 4.4% sensitivity, and capping '
          'the metric cut skewness from 18 to 5.3, an elevenfold cut in the users required. '
          'Those figures came off their own platform, not out of a textbook.'),
    drills=[
        dict(q='Bookings per user is heavily right-skewed with a big spike at zero, and the team wants a t-test. What do you do?',
             a=(r'<b>Work out $355 s^{2}$ before arguing about the test.</b> The spike at zero '
                r'is not the problem; the tail is. If you have far more than $355 s^{2}$ users '
                r'per arm, the t-test is fine and the zeros are irrelevant. If you do not, offer '
                r'three things in order: cap at a percentile you declare now, which is what Bing '
                r'did to take $s$ from 18 to 5.3 and the requirement from about 115,000 to about '
                r'10,000 per arm; split the metric into a bounded conversion rate and a '
                r'conditional amount, which is often the decomposition the business wanted '
                r'anyway; or bootstrap the interval. Do not switch to Mann&ndash;Whitney and '
                r'then quote a mean lift.'),
             a_simple=('<b>Work out how many users the lopsidedness demands before you argue '
                       'about the test.</b> The spike at zero is not the problem; the long tail '
                       'is. Multiply the squared lopsidedness of the metric by 355 and compare '
                       'that with the users you have in each arm. Clear it and the ordinary test '
                       'is fine. Miss it and you cap the metric at a level you announce now, or '
                       'you split the question in two: what share of people booked at all, and '
                       'how much the bookers spent. What you must not do is switch to a '
                       'rank-based test and then report a percentage lift.')),
        dict(q='Someone says we have 40,000 users per arm, which is well past 30, so the central limit theorem applies. What is wrong?',
             a=(r'<b>The 30 rule contains no skewness term, and skewness is the entire '
                r'problem.</b> The mean&rsquo;s skewness is $s/\sqrt{n}$, so the sample you need '
                r'scales with $s^{2}$. At $s = 17.9$ the bar is '
                r'$355 \times 17.9^{2} \approx 114{,}000$ per arm, so 40,000 is roughly a third '
                r'of what is needed and your interval&rsquo;s coverage is not 95%. Two moves '
                r'that follow: measure $s$ on the metric instead of assuming it, and run an A/A '
                r'test &mdash; if the false positive rate comes back well above 5%, the '
                r'approximation has demonstrably not arrived.'),
             a_simple=('<b>The thirty rule says nothing about lopsidedness, and lopsidedness is '
                       'the entire problem.</b> The number of users you need grows with the '
                       'square of how lopsided the metric is. For a metric as skewed as revenue '
                       'per user at Bing the bar is about 114,000 people per arm, so 40,000 is '
                       'roughly a third of what is needed and every interval you print is '
                       'narrower than the truth. Measure the lopsidedness of your own metric, '
                       'then split the control group at random and check that a test on the two '
                       'halves comes back exciting about one time in twenty.')),
        dict(q='Revenue per user has a skewness of 18 and you have 30,000 users per arm. Name your options and pick one.',
             a=(r'<b>You are four times short, so cap, and say the rule out loud now.</b> '
                r'$355 \times 18^{2} \approx 115{,}000$ per arm against the 30,000 you have. '
                r'Option one is to run roughly four times longer, which is rarely on offer. '
                r'Option two is capping: Bing&rsquo;s cap took skewness to 5.3, and '
                r'$355 \times 5.3^{2} \approx 10{,}000$, which you clear three times over. The '
                r'cost is bias &mdash; you are no longer estimating the true mean &mdash; so fix '
                r'the percentile before launch and report capped and uncapped lifts side by '
                r'side. Choosing the cap afterwards is a researcher degree of freedom and it '
                r'will be found.'),
             a_simple=('<b>You are four times short, so cap the metric and announce the rule '
                       'before you look.</b> The lopsidedness you have demands roughly 115,000 '
                       'users in each arm and you have 30,000. Running four times longer is the '
                       'honest alternative and usually is not available. Capping the metric at a '
                       'high level brings the requirement down to around 10,000, which you '
                       'comfortably clear. The price is that you are no longer measuring the '
                       'true average, so fix the cap before the test starts and show both the '
                       'capped and the uncapped result.')),
    ],
    anchor=dict(
        formula=r'$n \gtrsim 355\,s^{2}$ &nbsp;&middot;&nbsp; $s = 17.9 \Rightarrow n \approx '
                r'114{,}000$ &nbsp;&middot;&nbsp; $s = 5.3 \Rightarrow n \approx 10{,}000$',
        formula_simple='Multiply the squared lopsidedness of your metric by 355. That is how '
                       'many users you need in each arm before the ordinary test is safe.',
        bullets=[
            'The theorem is about the average, not the data, and its speed is set by skewness',
            'Capping buys precision with bias &mdash; declare the rule before launch, never after',
            'A rank test answers a different question from the one revenue is asking',
        ]),
    chips=['winsorising', 'bootstrap interval', 'A/A test', 'power and MDE',
           'bounded proxy metric'],
    followup='Bookings per user is heavily right-skewed with a big spike at zero and the team wants a t-test. What do you do?',
),

# ============================================================ F3
dict(
    id='independence',
    tier='foundation',
    title='Independence is the assumption that silently breaks',
    kicker='Your sample size is not the number of rows &mdash; it is the number of independent things you randomised',
    simple=[
        'Every interval and every test you run rests on one quiet assumption: that each row you '
        'counted is a fresh, unrelated piece of information. Real data almost never is. One '
        'user generates forty sessions. Two hundred evaluation questions come from twenty '
        'source documents. Comments sit inside threads and requests sit inside customer '
        'accounts. Rows from the same group resemble each other, so the second row from a user '
        'tells you much less than the first did.',
        'When that happens your uncertainty comes out too small, which makes your result look '
        'too impressive, which means you ship noise. The nasty part is that nothing looks '
        'wrong. There is no error, no warning, just a confident number arriving on time. The '
        'habit that saves you is to ask out loud what actually got randomised. If you '
        'randomised users, your sample size is users, no matter how many rows the query '
        'returned.',
    ],
    analogy=('<b>Like asking households what they had for dinner.</b> Interview four households '
             'and you have four dinners. Interview one household of four and you have one '
             'dinner described four times. The transcript is the same length either way, and '
             'only one of them is worth four.'),
    simple_extra=(
        'You can put a price on it. If each user hands you fifty events and events within a '
        'user resemble each other even mildly &mdash; a correlation of about a fifth &mdash; '
        'then two million rows carry roughly as much information as two hundred thousand '
        'independent ones, and the uncertainty you should be quoting is about three times what '
        'the naive calculation prints. Every fix says the same thing in a different dialect: '
        'work at the level you randomised. Roll the data up to one number per user, or use a '
        'method that knows which rows belong together when it draws the error bars.'),
    trap_simple=(
        '"We have two million rows, so we have plenty of power." You have forty thousand users. '
        'The subtler version of the same mistake is resampling rows when you bootstrap: '
        'shuffling individual rows quietly re-imposes independence at the exact step where you '
        'were trying to measure the dependence, so the interval comes out just as narrow and '
        'just as wrong. Resample whole users.'),
    tech=[
        r'Every t-test, interval and p-value assumes $\mathrm{Var}(\sum X_i) = \sum '
        r'\mathrm{Var}(X_i)$, which holds only under independence. When observations cluster '
        r'the covariance terms are positive and your variance estimate is missing them, so the '
        r'standard errors come out too small &mdash; in production analytics typically by a '
        r'factor of 2 to 5. The scale factor is the design effect $1 + (m-1)\rho$, with $m$ the '
        r'cluster size and $\rho$ the intraclass correlation. At $m = 50$ events per user and '
        r'$\rho = 0.2$ the design effect is 10.8, so two million rows behave like about 185,000 '
        r'and every SE is $\sqrt{10.8} = 3.3$ times what you printed.',
        r'Four fixes, all the same idea in different clothes. Cluster-robust standard errors. '
        r'The delta method for ratio metrics such as clicks per impression, with all moments '
        r'computed at the user level &mdash; provably equivalent to the cluster-robust '
        r'estimator for clustered randomised experiments. Bootstrap at the cluster level rather '
        r'than the row level. Or aggregate to the randomisation unit first and test the '
        r'per-unit values, which changes the estimand from a ratio of averages to an average of '
        r'ratios, so say which one the business is asking for before you pick it.',
    ],
    tech_note=(
        'The same failure has a different name on every team. Session metrics under user '
        'randomisation. Per-query metrics under per-user assignment. Tenant randomisation in '
        'B2B, where you have hundreds of clusters instead of millions of users. Eval questions '
        'drawn from shared source passages. The diagnostic is identical in all four: count the '
        'clusters rather than the rows, and treat an A/A test that fires far more than 5% of '
        'the time as evidence you have found one.'),
    fig=dict(
        kind='blocks', h=212,
        boxes=[
            dict(x=30, y=42, w=198, h=54, t='2,000,000 clicks', sub='rows in the query',
                 tone='sig'),
            dict(x=274, y=42, w=180, h=54, t='40,000 users', sub='what you randomised',
                 tone='mem'),
            dict(x=30, y=128, w=198, h=54, t='200 eval questions', sub='rows in the score',
                 tone='sig'),
            dict(x=274, y=128, w=180, h=54, t='20 source documents', sub='what varies freely',
                 tone='mem'),
            dict(x=500, y=85, w=192, h=54, t='error bars x 3.3', sub='at 50 rows per cluster',
                 tone='sig'),
        ],
        links=[dict(a=0, b=1), dict(a=2, b=3), dict(a=1, b=4, tone='sig'),
               dict(a=3, b=4, tone='sig')],
        labels=[dict(x=34, y=16, t='WHAT YOU COUNTED', a='start'),
                dict(x=686, y=16, t='WHAT THE MISMATCH COSTS', a='end')],
        foot='divide by the design effect, not by the row count',
        alt='Two datasets each collapsing from a large row count to a much smaller number of '
            'independent clusters, and the resulting threefold widening of the error bars'),
    caption=('Two setups that look nothing alike and have exactly the same shape. The left '
             'column is what the query returns; the middle column is what actually varies '
             'independently. The right-hand box is the price: at fifty rows per cluster and a '
             'within-cluster correlation of 0.2, every standard error you print is under a third '
             'of what it should be.'),
    caption_simple=('Two setups that look different and are the same shape underneath. The left '
                    'column is what the query returned; the middle is what genuinely varies on '
                    'its own. The box on the right is the price: with fifty rows per group, the '
                    'uncertainty you print is about a third of the truth, so every result looks '
                    'three times more convincing than it is.'),
    when=[
        'You randomised users and the analysis is per event, per session or per impression',
        'An eval set draws several questions from each source document',
        'Your A/A test comes back significant far more often than one time in twenty',
        'A B2B experiment randomises accounts and then reports per-seat numbers',
    ],
    trap=('"I have 2 million rows, so I have tons of power." You have 40,000 users. The subtler '
          'version, which gets past more interviewers: bootstrapping rows in clustered data. '
          'Resampling individual rows re-imposes independence at exactly the step where you were '
          'trying to measure the dependence, so the bootstrap interval comes out just as narrow '
          'as the wrong analytic one and looks like it was earned. Resample clusters.'),
    math=dict(
        tex=r'\mathrm{DEFF} = 1 + (m-1)\rho \qquad n_{\text{eff}} = \frac{n}{\mathrm{DEFF}} '
            r'\qquad \mathrm{SE}_{\text{true}} = \sqrt{\mathrm{DEFF}}\;\mathrm{SE}_{\text{naive}}',
        note='$\\rho$ is the correlation between two rows from the same cluster, and it only '
             'has to be small. At 50 rows per user, $\\rho = 0.2$ already costs you a factor of '
             'eleven in effective sample size.',
        cost='needs a cluster id on every row'),
    code=dict(
        label='The same data, two standard errors',
        cost='statsmodels',
        src=('<span class="k">import</span> statsmodels.api <span class="k">as</span> sm\n\n'
             '<span class="c"># 40,000 users x 50 impressions = 2,000,000 rows, one binary click</span>\n'
             'X = sm.add_constant(df[<span class="s">"treated"</span>])\n\n'
             'naive = sm.OLS(df[<span class="s">"click"</span>], X).fit()\n'
             'clust = sm.OLS(df[<span class="s">"click"</span>], X).fit(\n'
             '    cov_type=<span class="s">"cluster"</span>,\n'
             '    cov_kwds={<span class="s">"groups"</span>: df[<span class="s">"user_id"</span>]})\n\n'
             '<span class="k">print</span>(naive.bse[<span class="s">1</span>], clust.bse[<span class="s">1</span>])  '
             '<span class="c"># the second is 2-5x the first</span>\n'
             '<span class="k">print</span>(df[<span class="s">"user_id"</span>].nunique())      '
             '<span class="c"># this, not len(df), is your n</span>')),
    real=('Anthropic&rsquo;s <i>Adding Error Bars to Evals</i> (arXiv:2411.00640, November 2024) '
          'makes clustered standard errors recommendation number two of five, and prints the '
          'explicit formula, because eval suites draw several questions from the same source '
          'passage and naive standard errors understate the uncertainty on published model '
          'comparisons. The production version is the same arithmetic: naive standard errors run '
          '2 to 5 times too small whenever the randomisation unit and the analysis unit differ, '
          'the case Microsoft&rsquo;s experimentation group published on for tenant-randomised '
          'B2B tests.'),
    drills=[
        dict(q='You randomised by user but you are analysing click-through rate per impression. What is wrong, and how do you fix it?',
             a=(r'<b>Your denominator is impressions and your unit of randomisation is users, so '
                r'the standard error is fiction.</b> Impressions within a user are correlated, so '
                r'a two-proportion z-test with $n$ set to impressions understates the SE, '
                r'typically by 2 to 5 times, and your A/A tests will fire constantly. Two correct '
                r'fixes: the delta method for the ratio $\bar{X}/\bar{Y}$ with every moment '
                r'computed at the user level, or cluster-robust standard errors, which are '
                r'provably equivalent here. Averaging each user&rsquo;s own ratio and t-testing '
                r'those is also valid but estimates the average of ratios, not the ratio of '
                r'averages. Say which one the OEC is.'),
             a_simple=('<b>You counted impressions but you randomised people, so the error bars '
                       'are fiction.</b> Every impression from one person moves with the others, '
                       'so treating each as fresh evidence makes the result look two to five '
                       'times more certain than it is, and your sanity checks will fire '
                       'constantly. Fix it by computing at the person level: either use a method '
                       'that knows which rows share a person, or work out each person&rsquo;s own '
                       'rate first and compare those. The second choice quietly changes what you '
                       'are measuring &mdash; the average person&rsquo;s rate rather than the '
                       'overall rate &mdash; so decide which the business is asking about.')),
        dict(q='Two million rows, forty thousand users, fifty events each. How much power do you actually have?',
             a=(r'<b>Far less than the row count suggests &mdash; compute the design effect '
                r'before you answer.</b> $1 + (m-1)\rho$ with $m = 50$; even a mild $\rho = 0.2$ '
                r'gives 10.8. Effective sample size is $2{,}000{,}000 / 10.8 \approx 185{,}000$, '
                r'and every SE is $\sqrt{10.8} = 3.3$ times the naive one, so an MDE computed off '
                r'the row count is wrong by the same factor. Report the number of clusters '
                r'alongside the number of rows, and estimate $\rho$ from your own data rather '
                r'than guessing it &mdash; it falls out of a one-line variance-components fit.'),
             a_simple=('<b>Nothing like two million observations&rsquo; worth.</b> With fifty '
                       'events per person, rows inside a person repeat each other. Even a mild '
                       'resemblance between them &mdash; a correlation of about a fifth &mdash; '
                       'shrinks two million rows to the equivalent of roughly two hundred '
                       'thousand and triples every error bar, so the smallest effect you can '
                       'detect is three times bigger than you planned for. Report how many '
                       'people, not just how many rows, and measure the resemblance from your own '
                       'data rather than assuming it away.')),
        dict(q='Your eval suite is 200 questions drawn from 20 source passages, and model A beats model B by 3 points. What do you check first?',
             a=('<b>That your n is 20, not 200.</b> Questions from one passage share its topic, '
                'its difficulty and any label noise in it, so the effective sample size sits near '
                'the number of passages rather than the number of questions. Compute clustered '
                'standard errors with the passage as the cluster, which is Anthropic&rsquo;s '
                'recommendation number two, or bootstrap passages rather than questions. Then buy '
                'the power back: run both models on identical items and test the paired '
                'per-question difference, which removes item-difficulty variance entirely and is '
                'usually worth more than any of the corrections.'),
             a_simple=('<b>That your real sample is twenty passages, not two hundred '
                       'questions.</b> Questions drawn from one passage share its topic, its '
                       'difficulty and any mistakes buried in it, so they are not twenty times '
                       'more informative than the passage itself. Redraw the error bars grouping '
                       'by passage, or resample whole passages rather than single questions. Then '
                       'win the power back the cheap way: score both models on exactly the same '
                       'items and compare them question by question, which cancels out how hard '
                       'each question was.')),
    ],
    anchor=dict(
        formula=r'$\mathrm{DEFF} = 1 + (m-1)\rho$ &nbsp;&middot;&nbsp; $m = 50,\ \rho = 0.2 '
                r'\Rightarrow \mathrm{DEFF} = 10.8$ &nbsp;&middot;&nbsp; $\mathrm{SE} \times 3.3$',
        formula_simple='Count the things you randomised, not the rows. Fifty rows per person at '
                       'a mild within-person correlation costs you a factor of eleven.',
        bullets=[
            'The randomisation unit is the sample size, whatever the query returns',
            'Naive standard errors run 2 to 5 times too small when rows cluster',
            'Bootstrap clusters, never rows &mdash; row resampling repeats the same lie',
        ]),
    chips=['clustered standard errors', 'delta method', 'design effect', 'A/A test',
           'paired comparison'],
    followup='You randomised by user but you are analysing click-through rate per impression. What is wrong and how do you fix it?',
),

# ============================================================ F4
dict(
    id='count-distributions',
    tier='foundation',
    title='Picking the right count distribution',
    kicker='Your variance is three times your mean &mdash; that one fact already rules out the model most people reach for',
    simple=[
        'Counting things looks like the simplest measurement there is, and it is where the most '
        'avoidable modelling errors live. A count comes from one of a small number of physical '
        'stories, and each story implies a different amount of natural variation. A fixed '
        'number of chances with the same chance each time gives one shape. Events arriving over '
        'a window at a steady rate gives another. Drawing a handful of items from a small pool '
        'without putting them back gives a third, because the pool changes as you draw.',
        'The useful diagnostic takes one line of code and no theory at all. Compute the average '
        'of your counts, then compute the variance &mdash; how spread out they are. For the '
        'steady-arrivals story those two should come out roughly equal. That is a defining '
        'property of the story, not a coincidence. If the spread is three times the average, '
        'the story is wrong, and the usual reason is that you are not looking at one population: '
        'some users do the thing far more than others. Choosing on that comparison rather than '
        'on habit is the whole skill.',
    ],
    analogy=('<b>Like counting buses.</b> If they turn up at random at six an hour, the number '
             'in any given hour clusters tightly around six. If half the routes are hourly and '
             'half run every ten minutes, you get quiet hours and swamped hours, and the count '
             'swings far wider than the average predicts. Same average, different spread, '
             'because there is more than one kind of route.'),
    simple_extra=(
        'Four stories are worth being able to name on demand. A fixed number of tries at the '
        'same chance. Events arriving over a window at a steady rate. Drawing without '
        'replacement from a pool small enough that removing items matters. And the '
        'wider-spread version of the arrivals story, for when the rate itself differs from one '
        'person to the next. Interviewers pick the case where the obvious answer is wrong, and '
        'the two features that make it wrong are a small pool and a natural ceiling. Read the '
        'setup for those two before you name anything.'),
    trap_simple=(
        'Two specific ones. Treating a draw from a small pool as though each pick were '
        'independent, when taking an item out changes the odds for the next pick. And using the '
        'steady-arrivals model for something with a natural ceiling &mdash; clicks cannot '
        'exceed the number of times the thing was shown, and a model with no upper limit will '
        'cheerfully put probability on counts that could never happen.'),
    tech=[
        r'Four physical stories, four distributions. <b>Binomial</b>: $n$ fixed and known, '
        r'constant $p$, independent trials, and $\mathrm{Var} = np(1-p) < \mu$. '
        r'<b>Poisson</b>: events in continuous time at rate $\lambda$, use $\lambda t$ for a '
        r'window, and $\mathrm{Var} = \mu$ exactly. <b>Hypergeometric</b>: sampling without '
        r'replacement from a finite pool, so the trials are dependent by construction. '
        r'<b>Negative binomial</b>: a Gamma-mixed Poisson, for counts with $\mathrm{Var} > \mu$. '
        r'Binomial(200, 0.02) is well approximated by Poisson(4) &mdash; that is the rare-event '
        r'limit, and it is the Netflix form of the question.',
        r'Overdispersion is the tell you are being tested on. $\mathrm{Var}/\mu = 3$ rules out '
        r'Poisson by definition, not by goodness of fit. It nearly always means unmodelled '
        r'heterogeneity &mdash; users carry different underlying rates &mdash; or clustering, '
        r'which is the same problem wearing the other card&rsquo;s clothes. Fit a Poisson GLM '
        r'anyway and the standard errors come out deflated by roughly $\sqrt{\phi} \approx 1.7$, '
        r'which is enough to manufacture significance across half your coefficients. Reach for '
        r'negative binomial or a mixed model; if the count also has a ceiling, the bounded '
        r'analogue is beta-binomial. Underdispersion, $\mathrm{Var} < \mu$, is the binomial '
        r'signature and is worth naming when you see it.',
    ],
    tech_note=(
        'Before you accept overdispersion as real, rule out the boring causes: a duplicated '
        'event stream, a mixture of two populations you could simply split, zero inflation from '
        'users who could never have generated the event, and time-varying exposure you have not '
        'entered as an offset. A quasi-Poisson fit is the cheap diagnostic &mdash; it estimates '
        'the dispersion parameter directly and hands you the exact factor your naive standard '
        'errors were missing.'),
    fig=dict(
        kind='tree', h=282, nw=150, nh=44,
        head=['WHAT YOU OBSERVE', 'WHICH DISTRIBUTION'],
        nodes=[
            dict(id='r', x=360, y=58, w=204, t='fixed number of trials?',
                 sub='is the count capped by something'),
            dict(id='a', x=160, y=142, w=190, t='without replacement?',
                 sub='does the pool shrink as you draw'),
            dict(id='b', x=556, y=142, w=196, t='variance against the mean',
                 sub='the overdispersion tell'),
            dict(id='hg', x=70, y=226, w=134, t='hypergeometric', sub='5 drawn from 100',
                 tone='mem'),
            dict(id='bi', x=252, y=226, w=180, t='binomial', sub='clicks per 200 impressions',
                 tone='mem'),
            dict(id='po', x=452, y=226, w=140, t='Poisson', sub='12 requests an hour',
                 tone='mem'),
            dict(id='nb', x=636, y=226, w=152, t='negative binomial', sub='variance 3x the mean',
                 tone='sig'),
        ],
        edges=[dict(a='r', b='a', label='yes', dx=-16), dict(a='r', b='b', label='no', dx=16),
               dict(a='a', b='hg', label='yes', dx=-14), dict(a='a', b='bi', label='no', dx=14),
               dict(a='b', b='po', label='equal', dx=-18), dict(a='b', b='nb', label='bigger', dx=18)],
        foot='the bottom-right branch is the one people skip: compare the variance with the mean before you fit',
        alt='A decision tree running from whether the count has a fixed number of trials, '
            'through whether sampling is without replacement and whether the variance exceeds '
            'the mean, to hypergeometric, binomial, Poisson or negative binomial'),
    caption=('The tree reads the setup, not the name of the metric. Two features decide almost '
             'every case: whether the count is capped by something else you also measure, and '
             'whether the variance sits on the mean or well above it. Answer those and the '
             'distribution follows. Guess the distribution first and you will spend the rest of '
             'the interview defending it.'),
    caption_simple=('The tree reads the setup rather than the name of the metric. Two things '
                    'decide nearly every case: whether the count has an upper limit it cannot '
                    'pass, and whether the counts vary about as much as their average or far '
                    'more. Answer those two and the choice makes itself.'),
    when=[
        'You are asked for the probability of at least so many events in a window',
        'Your count model fits and the standard errors look implausibly tight',
        'Somebody samples a handful of users from a small pool and reaches for the binomial',
        'A metric is bounded by another quantity you also measure, like clicks by impressions',
    ],
    trap=(r'"It is counts, so Poisson." The two specific ways that fails: sampling without '
          r'replacement from a small pool, where removing a unit changes the next draw &mdash; '
          r'Meta&rsquo;s five-from-a-hundred question exists to catch it &mdash; and any count '
          r'with a natural ceiling, where Poisson puts probability on impossible values. And the '
          r'one that costs the offer: seeing $\mathrm{Var}/\mu = 3$, fitting Poisson anyway, and '
          r'reporting the p-values it prints.'),
    real_label='Where these get asked, and the number that decides each one',
    real=('These are documented 2026 loop questions and each turns on one number. Uber: twelve '
          'ride requests an hour, chance of at least three in ten minutes &mdash; Poisson with a '
          'rate of 2 for that window. Meta: five users drawn from a pool of 100 that is 20 '
          'treatment and 80 control, chance of exactly two treatment &mdash; hypergeometric at '
          '20.7%, against the binomial&rsquo;s 20.5%. Netflix: why 200 trials at 2% behaves like '
          'Poisson with a mean of 4. Google: why Poisson is wrong for click-through rate, since '
          'clicks are capped by impressions and vary far more across users than Poisson allows.'),
    math=dict(
        tex=r'\text{binomial } \mathrm{Var} = np(1-p) < \mu \;\;\big|\;\; '
            r'\text{Poisson } \mathrm{Var} = \mu \;\;\big|\;\; '
            r'\text{neg. binomial } \mathrm{Var} = \mu + \tfrac{\mu^{2}}{r} > \mu',
        note='The variance-to-mean ratio is a model-selection statistic, not an afterthought. '
             'Compute it first and it eliminates two of the four candidates before you fit '
             'anything at all.',
        cost='one pass over the counts'),
    code=dict(
        label='The variance-to-mean check, then the model',
        cost='statsmodels',
        src=('<span class="k">import</span> statsmodels.api <span class="k">as</span> sm\n\n'
             '<span class="k">print</span>(counts.mean(), counts.var())\n'
             '<span class="c"># ratio near 1 means Poisson is plausible; 3 means it is not</span>\n\n'
             'pois = sm.GLM(counts, X, family=sm.families.Poisson()).fit()\n'
             '<span class="k">print</span>(pois.pearson_chi2 / pois.df_resid)\n'
             '<span class="c"># the dispersion parameter, estimated. 1.0 is the Poisson claim</span>\n\n'
             'nb = sm.GLM(counts, X, family=sm.families.NegativeBinomial()).fit()\n'
             '<span class="k">print</span>(pois.bse[<span class="s">1</span>], nb.bse[<span class="s">1</span>])\n'
             '<span class="c"># at dispersion 3 the Poisson SE is about 1.7x too small</span>')),
    drills=[
        dict(q='Your event counts have variance three times the mean. What does that tell you, and what model do you use?',
             a=(r'<b>It rules out Poisson outright, because Poisson forces the variance to equal '
                r'the mean.</b> Overdispersion at that scale almost always means heterogeneity: '
                r'your users carry different underlying rates, so the population is a mixture '
                r'rather than one process. Negative binomial is the standard answer &mdash; a '
                r'Gamma-mixed Poisson with an explicit dispersion parameter &mdash; or a mixed '
                r'model if you want the per-user rates themselves. Name the consequence too: a '
                r'Poisson GLM fitted anyway deflates standard errors by roughly '
                r'$\sqrt{\phi} \approx 1.7$. And if the count has a ceiling, use beta-binomial '
                r'rather than negative binomial.'),
             a_simple=('<b>It rules out the steady-arrivals model, because that model forces the '
                       'spread and the average to match.</b> Counts that vary three times as much '
                       'as their average nearly always mean your users are not one population: '
                       'some do the thing far more often than others. Use the version of the '
                       'model that carries an extra knob for the extra spread, or model the '
                       'per-user rates directly. Then name the consequence: fitting the '
                       'steady-arrivals model anyway prints error bars roughly half as wide as '
                       'the truth, which turns ordinary noise into findings.')),
        dict(q='Five users are drawn from a pool of 100 that is 20 treatment and 80 control. What is the probability exactly two are treatment?',
             a=(r'<b>Hypergeometric, not binomial &mdash; the pool shrinks as you draw.</b> '
                r'$\binom{20}{2}\binom{80}{3}/\binom{100}{5} = 20.7\%$. The binomial answer at '
                r'$p = 0.2$ gives 20.5%, so numerically it hardly matters here, and that is '
                r'exactly the trap: the interviewer is checking whether you noticed the sampling '
                r'was without replacement, not whether you can carry two decimal places. Give the '
                r'rule that generalises &mdash; when the sample is a small fraction of the pool '
                r'the two agree, and when it is a large fraction they diverge fast, which is the '
                r'finite-population correction.'),
             a_simple=('<b>Use the without-replacement model, because taking a user out changes '
                       'the odds for the next pick.</b> The answer is just under twenty-one per '
                       'cent. The simpler calculation that ignores the shrinking pool gives just '
                       'over twenty and a half, so the two barely differ here &mdash; which is '
                       'the point of the question. The interviewer is checking whether you '
                       'noticed the pool was finite, not your arithmetic. Carry away the rule: '
                       'take a small slice of the pool and the two agree, take a large slice and '
                       'they do not.')),
        dict(q='Why is Poisson the wrong model for click-through rate?',
             a=(r'<b>Two independent reasons, and a strong answer gives both.</b> First the '
                r'support is wrong: clicks are bounded above by impressions and Poisson has no '
                r'ceiling, so it assigns probability to counts that cannot occur. Second, clicks '
                r'are overdispersed across users because propensity varies from person to person, '
                r'so the variance is wrong well before you reach the boundary. Binomial or '
                r'beta-binomial is the right family, beta-binomial being the bounded analogue of '
                r'the negative binomial. It is also why $\sum \text{clicks} / \sum '
                r'\text{impressions}$ cannot be z-tested with $n$ set to impressions &mdash; that '
                r'is the clustering problem again.'),
             a_simple=('<b>Two separate reasons, and the strong answer names both.</b> Clicks '
                       'cannot exceed the number of times something was shown, so a model with no '
                       'upper limit is describing a world that does not exist. And people differ '
                       'in how likely they are to click, so the counts vary far more than that '
                       'model allows even inside the range it can reach. The right family is the '
                       'one built on a fixed number of chances, in the version that carries an '
                       'extra knob for the spread between people.')),
    ],
    anchor=dict(
        formula=r'$\mathrm{Var} < \mu$ binomial &nbsp;&middot;&nbsp; $\mathrm{Var} = \mu$ '
                r'Poisson &nbsp;&middot;&nbsp; $\mathrm{Var} > \mu$ negative binomial '
                r'&nbsp;&middot;&nbsp; no replacement: hypergeometric',
        formula_simple='Compare the spread with the average. Below it means a fixed number of '
                       'tries, level with it means steady arrivals, above it means your '
                       'population is a mixture.',
        bullets=[
            'Read the setup for two features: a ceiling on the count, and a pool small enough to shrink',
            'Variance over mean is a model-selection statistic &mdash; compute it before you fit',
            'A Poisson fit on overdispersed counts roughly halves your standard errors and manufactures significance',
        ]),
    chips=['overdispersion', 'negative binomial', 'beta-binomial', 'zero inflation',
           'offset term'],
    followup='Your event counts have variance three times the mean. What does that tell you, and what model do you use?',
),

# ============================================================ F5
dict(
    id='regression-to-mean',
    tier='foundation',
    title='Regression to the mean is not a treatment effect',
    kicker='If you picked the group because it was extreme, it improves whether or not you touch it',
    simple=[
        'Every measurement is part real and part luck. When you pick out the worst performers '
        'you pick up two kinds of people: those who are genuinely struggling, and those who '
        'happened to have a bad week. Measure them again and the bad luck does not repeat, so '
        'the group as a whole drifts back toward the middle. Nobody did anything to them. The '
        'improvement is arithmetic, and selecting on an extreme is what guarantees it.',
        'This is why "we coached the bottom decile and they improved twelve per cent" is not '
        'evidence that coaching works. It is not evidence that it fails either, and that is the '
        'point: the number you are holding cannot tell you which. The only thing that separates '
        'a real effect from the rebound is a comparison group picked by the same rule and left '
        'alone. If you did not keep one, the honest answer is that you cannot say, and the fix '
        'is to run it again holding back a random slice of that same decile.',
    ],
    analogy=('<b>Like going back to a restaurant you loved.</b> You return because that first '
             'meal was extraordinary, and this time it is merely very good. The kitchen has not '
             'slipped. The first visit caught them on a night when everything landed and the '
             'second caught an ordinary night. Choose any experience because it was extreme and '
             'the repeat will be tamer.'),
    simple_extra=(
        'The same mechanism has a business name. When you ship the experiment that measured the '
        'biggest win, you have selected partly on a lucky measurement, so what you get in '
        'production is reliably smaller than what you reported. Measured across whole '
        'portfolios the shrinkage runs twenty to fifty per cent, which is why adding up the '
        'lifts of thirty shipped experiments never matches the movement in the annual metric. '
        'Same arithmetic, different costume, and it is the second half of this card that '
        'interviewers actually push on.'),
    trap_simple=(
        '"We controlled for the starting point by only including users who started low." That '
        'is not a control, it is the mechanism. Filtering on a low first measurement is '
        'precisely what guarantees the second one looks better. The other version is a '
        'before-and-after chart for the selected group with no comparison group anywhere on it, '
        'and the gap labelled as the effect.'),
    tech=[
        r'Write the observed score as $X = \tau + \varepsilon$. Selecting on $X$ being extreme '
        r'selects jointly on $\tau$ and on $\varepsilon$, and $\varepsilon$ does not persist, so '
        r'the conditional expectation of the second measurement is pulled toward the population '
        r'mean by the reliability: $E[X_2 \mid X_1] = \mu + \rho(X_1 - \mu)$ with $\rho < 1$. '
        r'The expected rebound is $(1-\rho)(\mu - X_1)$, entirely mechanical, and it is largest '
        r'exactly where the selection was most extreme and the metric noisiest &mdash; which is '
        r'to say, exactly where the intervention was most likely to be aimed.',
        r'The clean diagnostic is a control group selected by the same rule and left alone. '
        r'Without one, a pre-post comparison on a selected group is uninterpretable, and no '
        r'covariate adjustment rescues it: conditioning on the baseline <i>is</i> the selection, '
        r'not a correction for it. The same structure produces the winner&rsquo;s curse in '
        r'experimentation &mdash; Gelman and Carlin&rsquo;s Type M error is the exaggeration '
        r'ratio of an estimate conditional on significance, worst when the study was '
        r'underpowered &mdash; and the decline effect in science. The fixes on the '
        r'experimentation side are empirical-Bayes shrinkage of the reported lift, a post-launch '
        r'holdback, or discounting the roadmap forecast by a measured shrinkage factor.',
    ],
    tech_note=(
        'How to separate this from a genuine novelty effect, because interviewers push on '
        'exactly that seam: novelty shows a time trend inside the experiment window as users '
        'habituate, whereas regression to the mean does not &mdash; it is a one-off gap between '
        'the selected estimate and the truth, visible only on re-measurement. Both can be '
        'present at once, and naming only one of them is the answer that loses the point.'),
    fig=dict(
        kind='scatter',
        head=['MEASURED TWICE', 'NOTHING DONE IN BETWEEN'],
        xr=(0, 10), yr=(0, 10), ph=206,
        xlab='week 1 score', ylab='week 2 score',
        xticks=[(2, '2'), (4, '4'), (6, '6'), (8, '8')],
        yticks=[(2, '2'), (4, '4'), (6, '6'), (8, '8')],
        regions=[dict(x0=0, x1=3.0, y0=0, y1=10, tone='sig', op=0.09)],
        groups=[dict(pts=_REST, tone='mute', r=3.0, label='everyone else', lx=7.4, ly=2.0),
                dict(pts=_SEL, tone='sig', r=4.0,
                     label='the bottom tenth, picked on week 1', lx=0.25, ly=9.4)],
        curves=[dict(pts=[(0.6, 0.6), (9.4, 9.4)], tone='mute', dash='5 4', sw=1.4,
                     label='if nothing moved', lat=-1, dx=-6, dy=22, la='end'),
                dict(pts=[(0.15, 3.96), (3.0, 3.96)], tone='mem', sw=1.8,
                     label='week 2 average: 4.0', lat=0, dx=6, dy=-9, la='start'),
                dict(pts=[(2.23, 2.23), (2.23, 3.96)], tone='sig', sw=2.4,
                     label='up 1.7, untouched', lat=0, dx=8, dy=17, la='start')],
        foot='nobody was coached: this is the same noise, measured twice',
        alt='A scatter of the same users scored in two weeks. The shaded bottom tenth selected '
            'in week one averages 2.2 then 4.0 in week two, rising toward the middle with no '
            'intervention at all'),
    caption=('Every point is one user scored twice, with nothing done to anyone in between. The '
             'shaded band is the bottom decile as selected on week one. Their average climbs '
             'from 2.2 to 4.0 &mdash; a 78% improvement you could write up and present &mdash; '
             'purely because the noise that put them in the band did not repeat. The diagonal is '
             'where they would sit if nothing moved.'),
    caption_simple=('Each dot is one user scored in two different weeks, with nothing done to '
                    'them in between. The shaded strip is the bottom tenth as picked in week one. '
                    'Their average goes from 2.2 to 4.0, an improvement of nearly eighty per '
                    'cent, and the only cause is that the bad luck which put them there did not '
                    'come back. The diagonal is where they would sit if nothing had moved.'),
    when=[
        'An intervention was aimed at the worst-performing users, accounts or regions',
        'Someone reports a before-and-after number for a group that was selected on the before',
        'A shipped experiment&rsquo;s lift is visibly smaller in production than it was in the test',
        'The best of many candidates &mdash; a prompt, a model, a sweep &mdash; is quoted at its winning score',
    ],
    trap=('"We controlled for baseline by only including low-baseline users." That is the '
          'mechanism presented as its own remedy: conditioning on an extreme first measurement '
          'is exactly what manufactures the rebound. The second trap arrives once someone '
          'concedes the first &mdash; attributing the entire shrinkage to novelty. Novelty is a '
          'different mechanism with a different signature, and the answer that scores names both '
          'and says how to tell them apart.'),
    math=dict(
        tex=r'E[X_2 \mid X_1] = \mu + \rho\,(X_1 - \mu), \qquad '
            r'\rho = \frac{\sigma^{2}_{\tau}}{\sigma^{2}_{\tau} + \sigma^{2}_{\varepsilon}} < 1',
        note='$\\rho$ is the reliability of the measurement. The noisier the metric and the more '
             'extreme the selection, the larger the rebound &mdash; and none of it is an effect '
             'of anything.',
        cost='no treatment required'),
    code=dict(
        label='The effect you can measure with no treatment at all',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
             'tau = rng.normal(<span class="s">50</span>, <span class="s">10</span>, <span class="s">200_000</span>)   '
             '<span class="c"># true ability, fixed for each user</span>\n'
             'w1  = tau + rng.normal(<span class="s">0</span>, <span class="s">10</span>, <span class="s">200_000</span>)  '
             '<span class="c"># week 1: ability plus noise</span>\n'
             'w2  = tau + rng.normal(<span class="s">0</span>, <span class="s">10</span>, <span class="s">200_000</span>)  '
             '<span class="c"># week 2: ability plus FRESH noise</span>\n\n'
             'worst = w1 &lt; np.quantile(w1, <span class="s">0.10</span>)  '
             '<span class="c"># bottom decile, selected on week 1</span>\n'
             '<span class="k">print</span>(w1[worst].mean(), w2[worst].mean())  '
             '<span class="c"># 25.2 then 37.7</span>\n'
             '<span class="k">print</span>(w2[worst].mean() / w1[worst].mean() - <span class="s">1</span>)\n'
             '<span class="c"># 0.497 -- a "+50% improvement" from an intervention that does not exist</span>')),
    real=('The Open Science Collaboration&rsquo;s 2015 replication project: 97% of the original '
          'studies were statistically significant, 36% of the replications were, and the average '
          'effect size roughly halved, from 0.403 to 0.197. In experimentation the same '
          'arithmetic is priced &mdash; Airbnb&rsquo;s Experiment Reporting Framework documents '
          '20 to 50% portfolio-level overstatement, and Facebook shrank estimates across 226 News '
          'Feed tests to cut mean squared error by 44%. Palmer and Pe&rsquo;er (PLOS Genetics '
          '2017) show the identical inflation in the top hits of quantitative-trait GWAS.'),
    drills=[
        dict(q='We targeted the bottom decile of users with a re-engagement campaign and their engagement went up 12%. Ship it?',
             a=(r'<b>No &mdash; you have measured a campaign and a guaranteed rebound added '
                r'together, and you cannot separate them.</b> Selecting the bottom decile selects '
                r'partly on transient noise, and $E[X_2 \mid X_1] = \mu + \rho(X_1 - \mu)$ with '
                r'$\rho < 1$ means the group rises whether or not you act. The fix is one '
                r'sentence: randomise a holdout inside the bottom decile and compare treated '
                r'against untreated within it. If the campaign has already gone out to everyone, '
                r'the salvage is to check whether the ninth decile drifted upward over the same '
                r'window, and to say plainly that this is weaker than a randomised comparison.'),
             a_simple=('<b>No &mdash; the campaign and a guaranteed rebound are tangled together '
                       'in that single number.</b> Picking the bottom tenth picks people who were '
                       'genuinely disengaged and people who happened to have a quiet week, and '
                       'quiet weeks do not repeat, so the group climbs on its own. Run it again '
                       'holding back a random slice of that same bottom tenth and compare the '
                       'two. If it has already gone out to everyone, the best you can do is check '
                       'whether the next tenth up also drifted, and say plainly that this is '
                       'weaker evidence.')),
        dict(q='A colleague says we controlled for baseline by restricting to low-baseline users. Is that a valid control?',
             a=('<b>No &mdash; that restriction is the thing that creates the artefact.</b> '
                'Conditioning on an extreme value of a noisy first measurement is the definition '
                'of selecting on noise; it does not remove the rebound, it guarantees it. Putting '
                'the baseline into a regression has the same problem when the group itself was '
                'formed from the baseline, and there is a second failure mode lurking: adjusting '
                'for anything measured after treatment is a bad control. What works is '
                'randomisation inside the selected stratum &mdash; select on baseline if you '
                'want, then randomise within the selection.'),
             a_simple=('<b>No &mdash; that restriction is what creates the illusion in the first '
                       'place.</b> Choosing only people whose first score was low means choosing '
                       'people who were partly unlucky, and unluckiness does not repeat. Putting '
                       'the starting score into a model afterwards does not undo it, because the '
                       'group was built out of that score. The move that works is to select on '
                       'the starting score if you want to, and then split that selected group at '
                       'random so half get the treatment and half do not.')),
        dict(q='Your test measured a 1% lift. Should you forecast 1% after launch?',
             a=('<b>No &mdash; forecast less, and be specific about how much less.</b> You are '
                'shipping this one because it won, which means you selected on a measurement that '
                'contains noise, so the estimate is biased upward. That is Gelman and '
                'Carlin&rsquo;s Type M error, the exaggeration ratio conditional on significance, '
                'and it is worst on underpowered tests. Empirically, shipped-win effects shrink 20 '
                'to 50%, so the defensible forecast is a shrunk estimate &mdash; empirical-Bayes '
                'shrinkage toward the portfolio mean is the standard tool &mdash; plus a '
                'post-launch holdback so you measure what you actually got.'),
             a_simple=('<b>No &mdash; forecast less than one per cent, and say how much less.</b> '
                       'You are shipping this test because it came out best, and coming out best '
                       'means it caught a favourable run of luck as well as a real effect. '
                       'Measured across whole portfolios, shipped winners deliver twenty to fifty '
                       'per cent less than they measured. So discount the forecast, and keep a '
                       'small randomly held-back group after launch so you can measure what you '
                       'really got rather than argue about it a quarter later.')),
    ],
    anchor=dict(
        formula=r'$E[X_2 \mid X_1] = \mu + \rho\,(X_1 - \mu),\ \rho < 1$ &nbsp;&middot;&nbsp; '
                r'rebound $= (1-\rho)(\mu - X_1)$',
        formula_simple='Extreme first, ordinary second. The further out you selected and the '
                       'noisier the metric, the bigger the free improvement you are about to '
                       'take credit for.',
        bullets=[
            'Selecting on an extreme selects on noise, and noise does not repeat',
            'A comparison group chosen by the same rule is the only clean diagnostic',
            'Same mechanism as the winner&rsquo;s curse: shipped lifts shrink 20 to 50%',
        ]),
    chips=['winner&rsquo;s curse', 'Type M error', 'empirical-Bayes shrinkage', 'holdback',
           'novelty effect'],
    followup='We targeted the bottom decile of users with a re-engagement campaign and their engagement went up 12%. Ship it?',
),

]
