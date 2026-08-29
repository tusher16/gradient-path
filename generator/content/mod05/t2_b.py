CARDS = [

    # ------------------------------------------------------------------ 1
    dict(
        id='confidence-intervals',
        tier='core',
        title='Confidence intervals',
        kicker='The 95% belongs to the procedure, not to the interval on your screen &mdash; and the width is the part that decides anything',
        simple=[
            'The ninety-five per cent is a fact about the method, not about the pair of numbers '
            'in front of you. Run the experiment again and again, building an interval the same '
            'way each time, and about nineteen in twenty of those intervals would contain the '
            'true value. The one you are holding either contains it or it does not, and nothing '
            'on the page tells you which.',
            'That distinction sounds like pedantry and is not, because the sentence people say '
            'instead &mdash; there is a ninety-five per cent chance the truth is in here &mdash; '
            'quietly turns the interval into a probability statement about the world, which is a '
            'different object requiring a prior belief you would then have to defend.',
            'The part that actually decides anything is the width. A narrow interval that rules '
            'out every effect worth having is a finished result. A wide one is a polite way of '
            'saying you did not collect enough data. And narrowing is expensive: uncertainty '
            'falls with the square root of the sample, so an interval half as wide costs four '
            'times the users.',
        ],
        analogy=('<b>Like throwing a hoop over a fencepost.</b> You know from hundreds of throws '
                 'that your style lands the hoop over the post nineteen times in twenty. That is '
                 'a fact about your throwing. This particular throw has already landed: the post '
                 'is either inside the hoop or it is not. There is no ninety-five per cent left '
                 'in it, only a hoop lying on the grass and a fact about how you throw.'),
        trap_simple=('Saying there is a ninety-five per cent chance the true value sits inside '
                     'this particular interval. The method never made a claim about the truth; it '
                     'made a claim about itself. The second half of the trap is looking at two '
                     'intervals, noticing they overlap, and concluding the two things are the '
                     'same. Overlap is not a test. You have to measure the gap directly.'),
        tech=[
            'Coverage is a property of the procedure: $P(L \\leq \\theta \\leq U) = 0.95$ where '
            'the randomness lives in the endpoints $L$ and $U$, not in $\\theta$. Once the data '
            'are in, the interval is fixed and the probability is 0 or 1. "There is a 95% chance '
            '$\\theta$ is in $[a,b]$" is a credible interval, and it needs a prior. Say the '
            'repeated-sampling sentence out loud once and the follow-up moves on.',
            'Three things worth more than the definition. A CI strictly dominates a p-value '
            '&mdash; direction, magnitude and precision in one object, which is why you report it '
            'and not the p-value. Overlapping marginal CIs do <i>not</i> imply a non-significant '
            'difference: you must interval the difference itself, and for paired data the paired '
            'difference, which removes the shared source of variance and routinely rescues a '
            'result the marginal intervals hid. And width scales as $1/\\sqrt{n}$, so halving it '
            'costs $4n$ &mdash; the single most useful back-of-envelope in experiment and eval '
            'planning.',
            'Use Wald only away from the boundaries. Near 0 or 1, or at small $n$, switch to '
            'Wilson or Clopper-Pearson; Wald will hand you a lower bound below zero and, at zero '
            'events, the interval $[0,0]$.',
        ],
        tech_note=('That $[0,0]$ is where the rule of three earns its keep. With 0 events in $n$ '
                   'trials the 95% upper bound on the rate is about $3/n$, from '
                   '$(1-p)^n = 0.05 \\Rightarrow p \\approx \\ln(20)/n$ and $\\ln 20 \\approx 3$. '
                   'Zero policy violations in 500 evaluation prompts bounds the true rate at '
                   'roughly 0.6%, which at 10M requests a day is up to 60,000 violations a day. '
                   'Hanley and Lippman-Hand published it in <i>JAMA</i> in 1983 under the title '
                   '"If nothing goes wrong, is everything all right?" &mdash; written because '
                   'trials were reporting zero adverse events as evidence of safety.'),
        fig=dict(
            kind='plot', xr=(-2.2, 3.6), yr=(0, 21), ph=215,
            xticks=[(-2, '-2%'), (-1, '-1%'), (0, '0'), (1, '+1%'), (2, '+2%'), (3, '+3%')],
            yticks=[],
            vlines=[dict(x=1.0, tone='mem', label='the true effect, which you never see')],
            curves=[
                dict(pts=[(0.15, 1), (2.55, 1)], tone='mem', sw=2.0),
                dict(pts=[(-0.58, 2), (1.82, 2)], tone='mem', sw=2.0),
                dict(pts=[(-0.10, 3), (2.30, 3)], tone='mem', sw=2.0),
                dict(pts=[(-1.15, 4), (1.25, 4)], tone='mem', sw=2.0),
                dict(pts=[(0.52, 5), (2.92, 5)], tone='mem', sw=2.0),
                dict(pts=[(-0.32, 6), (2.08, 6)], tone='mem', sw=2.0),
                dict(pts=[(0.24, 7), (2.64, 7)], tone='mem', sw=2.0),
                dict(pts=[(-1.55, 8), (0.85, 8)], tone='sig', sw=2.4,
                     label='misses', lat=0, la='end', dx=-8, dy=3.5),
                dict(pts=[(0.00, 9), (2.40, 9)], tone='mem', sw=2.0),
                dict(pts=[(-0.50, 10), (1.90, 10)], tone='mem', sw=2.0),
                dict(pts=[(0.38, 11), (2.78, 11)], tone='mem', sw=2.0),
                dict(pts=[(-0.78, 12), (1.62, 12)], tone='mem', sw=2.0),
                dict(pts=[(-0.15, 13), (2.25, 13)], tone='mem', sw=2.0),
                dict(pts=[(0.70, 14), (3.10, 14)], tone='mem', sw=2.0),
                dict(pts=[(-0.65, 15), (1.75, 15)], tone='mem', sw=2.0),
                dict(pts=[(0.08, 16), (2.48, 16)], tone='mem', sw=2.0),
                dict(pts=[(-0.25, 17), (2.15, 17)], tone='mem', sw=2.0),
                dict(pts=[(0.42, 18), (2.82, 18)], tone='mem', sw=2.0),
                dict(pts=[(-0.90, 19), (1.50, 19)], tone='mem', sw=2.0),
                dict(pts=[(-0.05, 20), (2.35, 20)], tone='mem', sw=2.0),
            ],
            xlab='estimated lift', ylab='twenty repeats',
            foot='the 95 per cent is a property of the machine that made these, not of any one of them',
            alt='Twenty confidence intervals from twenty repeats of the same experiment, drawn '
                'against a vertical line at the true effect. Nineteen of them cross the line; one, '
                'drawn in pink, sits entirely below it and misses.'),
        caption=('Every bar is the same experiment, run again. The procedure has 95% coverage; the '
                 'interval you actually got either contains the truth or does not, and you cannot '
                 'tell from the page. What the page does tell you is the width, and the width is '
                 'what separates a finished result from a request for more traffic.'),
        caption_simple=('Every bar here is the same experiment run again. Nineteen of the twenty '
                        'contain the true value and one does not &mdash; that is what the '
                        'ninety-five per cent means. Which kind you got is not something the '
                        'picture can tell you. What it can tell you is how wide your bar is.'),
        when=[
            'A result is significant and someone asks how big the effect actually is',
            'Two models score 82% and 79% on the same eval and their intervals overlap',
            'A flat test is finished and the team is deciding whether to run another week',
            'A safety review reports zero policy violations in 500 evaluation prompts',
        ],
        trap=('"There is a 95% chance the true lift is between 0.1% and 0.9%." That sentence '
              'describes a credible interval and requires a prior; the interval you computed '
              'describes a procedure. The version that costs more money is the second one: '
              '"Model A and Model B have overlapping intervals, so they are the same." Overlap is '
              'not a test, and on paired data it is a badly misleading one &mdash; put the '
              'interval on the per-item difference and the same two models can separate cleanly.'),
        math=dict(
            tex=r'\bar{x} \pm z_{1-\alpha/2}\,\frac{s}{\sqrt{n}} \qquad\text{width} \;\propto\; \frac{1}{\sqrt{n}} \qquad \text{0 events} \Rightarrow \text{upper bound} \approx \frac{3}{n}',
            note='The randomness is in the endpoints, never in the parameter. Halving the width '
                 'costs four times the data, so "can we tighten this a bit?" is a budget question '
                 'with a fixed exchange rate.',
            cost='normal approximation; use Wilson near 0 or 1'),
        code=dict(
            label='The 95% is in the factory, not in the interval',
            cost='numpy + scipy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 '<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n'
                 'TRUE, hits = <span class="s">1.0</span>, <span class="s">0</span>\n\n'
                 '<span class="k">for</span> _ <span class="k">in</span> <span class="k">range</span>(<span class="s">20000</span>):\n'
                 '    x = rng.normal(TRUE, <span class="s">10</span>, size=<span class="s">400</span>)\n'
                 '    lo, hi = stats.t.interval(<span class="s">0.95</span>, <span class="s">399</span>,\n'
                 '                              loc=x.mean(), scale=stats.sem(x))\n'
                 '    hits += lo &lt;= TRUE &lt;= hi\n\n'
                 '<span class="k">print</span>(hits / <span class="s">20000</span>)   '
                 '<span class="c"># 0.95125 -- the PROCEDURE covers 95% of the time</span>\n'
                 '<span class="c"># any single (lo, hi) either contains 1.0 or does not. no 95% lives inside it</span>')),
        real=('<i>Adding Error Bars to Evals</i> (Miller, Anthropic, Nov 2024, arXiv:2411.00640) '
              'exists because the industry had been shipping bare accuracy numbers with no '
              'uncertainty attached at all. Its arithmetic is the thing to carry: 82% on 50 '
              'prompts has a standard error of 5.4 percentage points and a 95% interval of about '
              '[71%, 93%], which is not a result. Recommendation 4 of the paper is explicitly to '
              'run inference on question-level <i>paired</i> differences rather than comparing two '
              'marginal intervals.'),
        drills=[
            dict(q='Model A scores 82% and Model B 79% on the same 500-question eval, and their 95% confidence intervals overlap. Is A better?',
                 a=('<b>You cannot tell from those two intervals, and the overlap is not evidence '
                    'that they are the same.</b> A marginal CI answers "how good is this model", '
                    'and most of its width is question difficulty &mdash; a variance source both '
                    'models share. Score the same 500 items with both, take the per-question '
                    'difference $d_i = s_{A,i} - s_{B,i}$, and put a CI on $\\bar{d}$. Pairing '
                    'cancels the shared difficulty, so the paired standard error is typically well '
                    'under half the marginal one and a 3-point gap that looked invisible comes '
                    'back clearly non-zero. This is recommendation 4 of the Anthropic error-bars '
                    'paper.'),
                 a_simple=('<b>You cannot tell from those two ranges.</b> Each range answers "how '
                           'good is this model on questions like these", not "is one better than '
                           'the other". Both models sat the same 500 questions, and most of the '
                           'wobble in either score is which questions happened to be hard &mdash; '
                           'a wobble they share. So compare them question by question instead: '
                           'where A wins, where B wins, and put a range on that difference. '
                           'Cancelling the shared difficulty usually cuts the uncertainty by more '
                           'than half, and a gap that looked invisible becomes clear.')),
            dict(q='The interval on your lift is [-2%, +6%] and the PM wants to know whether to ship. What do you say?',
                 a=('<b>That interval is a request for more data, not a result.</b> It contains '
                    'zero, so it is not significant &mdash; but it also contains +6%, far above '
                    'anything you would have declared as an MDE, so you have ruled out nothing in '
                    'either direction. Contrast it with $[-0.2\\%, +0.3\\%]$: identical '
                    '"not significant" verdict, opposite conclusion, because that one has excluded '
                    'every effect worth having and the experiment is finished. Re-run the power '
                    'calculation with the <i>observed</i> variance to get the honest cost of '
                    'resolving it, and if that number is unaffordable, reach for CUPED or a '
                    'sharper proxy rather than more weeks.'),
                 a_simple=('<b>That range is a request for more data, not a result.</b> It runs '
                           'from a two per cent loss to a six per cent gain, so it is equally '
                           'consistent with the feature being a quiet disaster and with it being '
                           'the best thing you shipped this year. Now compare it with a range that '
                           'runs from a tiny loss to a tiny gain: same "not significant" label, but '
                           'that one has genuinely ruled out anything worth having and you can '
                           'close the experiment. The width, not the verdict, is what separates the '
                           'two.')),
            dict(q='Safety review says the model produced zero policy violations in 500 evaluation prompts. Can we ship?',
                 a=('<b>Zero out of 500 is not a rate of zero, and the interval that says it is is '
                    'the wrong interval.</b> Wald collapses to $[0,0]$ at zero events, which is the '
                    'tell. The rule of three gives a 95% upper bound of about $3/n = 3/500$, so the '
                    'true violation rate could be 0.6%. At 10M requests a day that is up to 60,000 '
                    'violations a day, which is not a shipping decision anyone would sign. Invert '
                    'the question instead: name the rate you are willing to tolerate and derive the '
                    'clean trials it needs &mdash; bounding below 0.1% takes roughly 3,000.'),
                 a_simple=('<b>Zero out of five hundred is not a rate of zero.</b> There is a rough '
                           'rule for exactly this: with no failures at all, the highest rate still '
                           'consistent with what you saw is about three divided by the number of '
                           'trials. Three in five hundred is six in a thousand, so the true rate '
                           'could still be a bit over half a per cent. At ten million requests a '
                           'day that is up to sixty thousand violations a day. Turn the question '
                           'round: decide what rate you could live with, and that tells you how '
                           'many clean runs you actually need.')),
        ],
        anchor=dict(
            formula=r'$P(L \leq \theta \leq U) = 0.95$ over repeats &nbsp;&middot;&nbsp; not over $\theta$ &nbsp;&middot;&nbsp; width $\propto 1/\sqrt{n}$',
            formula_simple='Nineteen in twenty of the intervals this method builds contain the '
                           'truth. Yours is a hoop already lying on the grass.',
            bullets=[
                'The ninety-five per cent belongs to the procedure; this interval either contains the parameter or it does not',
                'Overlapping intervals are not a test &mdash; interval the paired difference instead',
                'Halving the width costs four times the data, which is the real budget conversation',
                'Zero events in n trials bounds the rate at about three over n, never at zero',
            ]),
        chips=['paired difference', 'Wilson interval', 'rule of three', 'statistical power',
               'bootstrap'],
        followup='Model A scores 82% and Model B 79% on the same 500-question eval and their confidence intervals overlap — is A better?',
    ),

    # ------------------------------------------------------------------ 2
    dict(
        id='power-mde',
        tier='core',
        title='Power, MDE and &ldquo;how long do we run it&rdquo;',
        kicker='A project-management question wearing a power calculation underneath, and the interviewer wants the arithmetic out loud',
        simple=[
            'Four quantities are locked together: how often you are willing to cry wolf, how '
            'often you are willing to miss a real effect, the smallest effect you actually care '
            'about, and the number of users. Fix any three and the fourth is arithmetic. The '
            'first two are conventions &mdash; one in twenty and one in five. The number of users '
            'is what you are solving for. So the only genuine judgement in the whole exercise is '
            'the third one, and it is a product decision, not a statistical one: below what lift '
            'would you not bother shipping this?',
            'Answer that, and the sample size falls out. Divide by the eligible users you get a '
            'day, split across arms, and round up to whole weeks so the test is not comparing a '
            'Tuesday with a Saturday. Now you can answer "how long" with a number and a reason '
            'instead of "two weeks".',
            'The expensive mistake is sizing for the lift you are hoping for. Effects and sample '
            'sizes trade at a punishing rate: halve the effect you want to catch and you need '
            'four times the users.',
        ],
        analogy=('<b>Like choosing a shutter speed before the race, not after.</b> Freezing a '
                 'sprinter needs a fast shutter and a lot of light; seeing whether anyone crossed '
                 'the line at all needs a phone. Deciding how small a movement you must be able to '
                 'see is what sets the equipment and the budget. Nobody photographs a race first '
                 'and then works out what they were trying to see.'),
        simple_extra=('One more habit that separates people who have run experiments from people '
                      'who have read about them: before asking for more traffic, ask whether you '
                      'can make the metric less noisy. Capping a wild revenue metric, or adjusting '
                      'each user by how they behaved the week before the test started, can cut the '
                      'required sample by half or better. Traffic is somebody else&rsquo;s budget. '
                      'Variance is yours.'),
        tech=[
            'Four quantities, pick three. Fix $\\alpha = 0.05$ and power $1-\\beta = 0.80$, decide '
            'the MDE $\\delta$ from the business, solve for $n$. The general form is '
            '$n = 2\\sigma^2(z_{1-\\alpha/2} + z_{1-\\beta})^2/\\delta^2$ per arm, and at those '
            'conventions the constant $2(1.96+0.84)^2 \\approx 15.7$, which is the entire reason '
            'the whiteboard version is $n \\approx 16\\sigma^2/\\delta^2$. For a proportion, '
            '$\\sigma^2 = p(1-p)$.',
            'Do the canonical one out loud. Baseline conversion 5%, catch a 10% relative lift, so '
            '$\\delta = 0.005$ absolute &mdash; and say "absolute", because relative-versus-'
            'absolute is where this arithmetic usually dies. '
            '$n \\approx 16 \\times 0.05 \\times 0.95 / 0.005^2 = 0.76/0.000025 \\approx 30{,}400$ '
            'per arm. At 50,000 eligible users a day split two ways that is 1.2 days &mdash; and '
            'you still run seven, because a test that only sees Monday and Tuesday is not '
            'measuring your product.',
            'Then say the part that makes it a real answer: a 10% relative lift is enormous. Size '
            'the same experiment for a 2% relative lift and $\\delta = 0.001$, so $n$ goes to '
            '760,000 per arm and 30 days, which rounds to five weeks. That factor of 25 came from '
            'one product decision, and it is the decision the interview is about.',
        ],
        tech_note=('$\\sigma$ is the term you can actually move. Kohavi&rsquo;s Rule 7: a skewed '
                   'metric needs at least $355 s^2$ users per arm, where $s$ is the skewness '
                   'coefficient &mdash; Bing&rsquo;s revenue-per-user has $s = 17.9$, so about '
                   '114,000 users per arm just to reach 4.4% sensitivity. Capping that metric cut '
                   'skewness from 18 to 5.3, roughly an 11-fold reduction in required $n$. CUPED '
                   'does the same job from the other side: a pre-period covariate correlated at '
                   '$\\rho = 0.7$ removes about half the variance, which halves the sample.'),
        fig=dict(
            kind='plot', xr=(0, 10.5), yr=(0, 3.25), ph=200,
            xticks=[(1, '1%'), (2, '2%'), (4, '4%'), (6, '6%'), (8, '8%'), (10, '10%')],
            yticks=[(0.0304, '30k'), (0.76, '760k'), (2, '2M'), (3.04, '3.04M')],
            vlines=[dict(x=1, tone='mem', label='where wins at Bing actually land'),
                    dict(x=10, tone='plain', label='the lift teams size for')],
            curves=[dict(pts=[(1, 3.04), (1.25, 1.946), (1.5, 1.351), (1.75, 0.993), (2, 0.76),
                              (2.5, 0.486), (3, 0.338), (4, 0.19), (5, 0.122), (6, 0.084),
                              (8, 0.047), (10, 0.030)],
                         tone='sig', label='users needed per arm', lat=5, dx=12, dy=-14)],
            marks=[dict(x=2, y=0.76, label='760k per arm, five weeks', tone='mem', dx=10, dy=-12),
                   dict(x=10, y=0.030, label='30k, under two days', tone='plain',
                        dx=-10, dy=-12, la='end')],
            xlab='smallest relative lift you can detect, on a 5 per cent baseline',
            ylab='users per arm',
            foot='halve the effect you want to catch and the bill goes up four times',
            alt='A steeply falling curve of users needed per arm against the smallest relative '
                'lift you can detect on a five per cent baseline: about thirty thousand per arm to '
                'catch a ten per cent lift, seven hundred and sixty thousand to catch two per '
                'cent, and over three million to catch one per cent, which is where wins at Bing '
                'actually land.'),
        caption=('The whole card is this curve. Your MDE is not a statistical preference, it is a '
                 'position on the x-axis, and every step left costs quadratically. Teams argue '
                 'about "how long should we run it" when the argument they are actually having is '
                 'about which point on this line they can afford.'),
        caption_simple=('Your choice of the smallest effect worth catching is a position on this '
                        'line, and every step to the left costs four times as much for half the '
                        'gap. The argument about how long to run the test is really an argument '
                        'about which point on this line the team can afford.'),
        when=[
            'A PM asks "how long do we need to run this?" and expects to hear "two weeks"',
            'You are pitting three variants and a control against fixed daily traffic',
            'A test came back flat and somebody wants to run it one more week',
            'The metric is revenue per user and the histogram has a long right tail',
        ],
        trap=('Sizing from the lift you are hoping for rather than the smallest lift that would '
              'change your decision: "we think this will lift conversion 10%, so we powered for '
              '10%." You have just guaranteed that every real effect &mdash; which at Bing scale '
              'means 0.1% to 1.0% &mdash; comes back inconclusive and gets argued about instead of '
              'decided. The second half of the same trap is quoting a sample size without saying '
              '<b>per arm</b>, and without rounding the days up to whole weeks.'),
        math=dict(
            tex=r'n_{\text{per arm}} \;\approx\; \frac{16\,\sigma^{2}}{\delta^{2}} \qquad\text{from}\qquad n \;=\; \frac{2\sigma^{2}\bigl(z_{1-\alpha/2}+z_{1-\beta}\bigr)^{2}}{\delta^{2}}',
            note=r'The 16 is $2(1.96+0.84)^2 \approx 15.7$ at $\alpha = 0.05$ and 80% power. '
                 r'$\delta$ is <i>absolute</i>: a 10% relative lift on a 5% baseline is '
                 r'$\delta = 0.005$, not 0.10. For a proportion $\sigma^2 = p(1-p)$; for anything '
                 r'skewed, use the observed variance and expect a much larger number.',
            cost='per arm, and only valid once you have named the MDE'),
        code=dict(
            label='The napkin and the library agree, then convert to weeks',
            cost='statsmodels',
            src=('<span class="k">import</span> math\n'
                 '<span class="k">from</span> statsmodels.stats.power '
                 '<span class="k">import</span> NormalIndPower\n'
                 '<span class="k">from</span> statsmodels.stats.proportion '
                 '<span class="k">import</span> proportion_effectsize\n\n'
                 'p0, rel = <span class="s">0.05</span>, <span class="s">0.02</span>   '
                 '<span class="c"># 5% baseline, catch a 2% RELATIVE lift</span>\n'
                 'n = NormalIndPower().solve_power(\n'
                 '        proportion_effectsize(p0 * (<span class="s">1</span> + rel), p0),\n'
                 '        power=<span class="s">0.80</span>, alpha=<span class="s">0.05</span>, '
                 'ratio=<span class="s">1</span>)\n\n'
                 '<span class="k">print</span>(<span class="k">round</span>(n))                         '
                 '<span class="c"># 752684 PER ARM</span>\n'
                 '<span class="k">print</span>(<span class="k">round</span>(<span class="s">16</span> * p0 * '
                 '(<span class="s">1</span> - p0) / (p0 * rel) ** <span class="s">2</span>))  '
                 '<span class="c"># 760000 -- the napkin is within 1%</span>\n\n'
                 '<span class="c"># 50k eligible users/day, two arms -> 25k per arm per day</span>\n'
                 '<span class="k">print</span>(math.ceil(n / <span class="s">25_000</span> / '
                 '<span class="s">7</span>) * <span class="s">7</span>)      '
                 '<span class="c"># 35 days. round UP to whole weeks, always</span>')),
        real=('Kohavi&rsquo;s <i>Seven Rules of Thumb</i> (exp-platform, 2014) records that at Bing '
              'the wins that actually land move key metrics by 0.1% to 1.0%, and that perhaps 1 in '
              '500 experiments is a genuine breakthrough. For scale: a 100 ms latency improvement '
              'is worth about 0.6% of revenue there, and that is a celebrated result. A team that '
              'powers for a 5% lift has powered for something that essentially never happens, so '
              'their experiments come back inconclusive and get settled by seniority instead of '
              'data.'),
        drills=[
            dict(q='Baseline conversion is 5%, you want to detect a 10% relative lift, alpha 0.05, 80% power. Roughly how many users per arm, and how many days?',
                 a=('<b>About 30,000 per arm, which is under two days of traffic, so you run a '
                    'week.</b> $\\delta = 0.05 \\times 0.10 = 0.005$ absolute; '
                    '$\\sigma^2 = p(1-p) = 0.0475$; '
                    '$n \\approx 16 \\times 0.0475/0.005^2 = 0.76/0.000025 \\approx 30{,}400$ per '
                    'arm. At 50,000 eligible users a day split two ways that is 25,000 per arm per '
                    'day, so 1.2 days &mdash; and you run seven anyway, for day-of-week effects. '
                    'Then volunteer the uncomfortable half: a 10% relative lift is enormous, and if '
                    'the real effect is 2% you needed 760,000 per arm and five weeks.'),
                 a_simple=('<b>About thirty thousand people per arm, which is under two days of '
                           'traffic, so you run a week.</b> The gap you are trying to catch is half '
                           'of one per cent in absolute terms. The rough rule is sixteen, times the '
                           'variability of the metric, divided by the square of that gap, and it '
                           'lands near thirty thousand people in each group. At fifty thousand '
                           'eligible users a day split two ways, that fills in a day and a bit '
                           '&mdash; and you still run a full week so the test sees a weekend. Then '
                           'say the uncomfortable part: a ten per cent lift is enormous, and if the '
                           'real effect is two per cent you needed three quarters of a million per '
                           'arm and five weeks.')),
            dict(q='The test has been running two weeks and is flat. The PM wants one more week. What do you say?',
                 a=('<b>One more week buys you almost nothing, and here is the arithmetic.</b> '
                    'Width scales as $1/\\sqrt{n}$, so going from two weeks to three shrinks the '
                    'interval by about 18%: an interval of $[-2\\%, +6\\%]$ becomes roughly '
                    '$[-1.6\\%, +4.9\\%]$ and you have the identical argument seven days later. '
                    'The order is: check SRM and instrumentation first, then re-derive the power '
                    'calculation with the <i>observed</i> variance instead of the guess you '
                    'started with. That gives an honest number of extra weeks. If it comes back as '
                    'six, the decision is no longer "one more week" &mdash; it is CUPED, capping '
                    'the metric, a more sensitive proxy, or accepting the null.'),
                 a_simple=('<b>One more week buys you almost nothing, and here is the '
                           'arithmetic.</b> Uncertainty shrinks with the square root of the sample, '
                           'so a third week narrows your range by less than a fifth. A range '
                           'running from a two per cent loss to a six per cent gain still runs from '
                           'about a one and a half per cent loss to a five per cent gain, and you '
                           'have the same meeting again. Redo the sizing using the variability you '
                           'actually measured rather than the one you guessed. If the honest answer '
                           'is six more weeks, the real choice is whether to spend six weeks, cut '
                           'the noise in the metric, or accept the flat result.')),
            dict(q='You want to test four variants against control on the same traffic. What changes in the sample size?',
                 a=('<b>Two things multiply, and only one of them is obvious.</b> The obvious one: '
                    'five arms share the traffic two arms used to share, so each arm fills at a '
                    'fifth rather than a half of the rate and the same per-arm $n$ takes 2.5 times '
                    'as long. The one candidates miss: four comparisons against control is four '
                    'hypothesis tests, so you either correct &mdash; Holm, or Benjamini-Hochberg '
                    'if this is a screen &mdash; or you pre-declare which variant is the '
                    'candidate. Correcting lowers the per-test $\\alpha$, which raises $n$ again. '
                    'The honest recommendation is usually to cut to two arms, because a five-arm '
                    'test is a nine-week test with less power than anyone in the room thinks.'),
                 a_simple=('<b>Two things multiply, and only one of them is obvious.</b> The '
                           'obvious one: five groups now share the traffic that two used to share, '
                           'so every group fills up two and a half times more slowly. The one '
                           'people miss: four comparisons against the control are four separate '
                           'chances to be fooled by noise, so you must either raise the bar on each '
                           'one or name your favourite before you start. Raising the bar needs more '
                           'people again, on top of the slower fill. Usually the right call is to '
                           'cut to two arms and test the survivor properly.')),
        ],
        anchor=dict(
            formula=r'$n \approx \dfrac{16\sigma^{2}}{\delta^{2}}$ per arm &nbsp;&middot;&nbsp; then days $=$ $n$ &divide; daily eligible per arm, rounded up to whole weeks',
            formula_simple='Sixteen, times how variable the metric is, divided by the square of the '
                           'smallest effect you care about. That is the users you need in each '
                           'group.',
            bullets=[
                'The MDE is a product decision &mdash; the smallest lift that would change what you do',
                'Halve the MDE and the sample size goes up four times',
                'Sample size is per arm, and days round up to whole weeks',
                'If the number is unaffordable, cut the variance before you ask for traffic',
            ]),
        chips=['minimum detectable effect', 'CUPED', 'Type M error', 'sequential testing',
               'sample ratio mismatch'],
        followup='Baseline conversion is 5%, you want to detect a 10% relative lift at 80% power — roughly how many users per arm, and how many days?',
    ),

    # ------------------------------------------------------------------ 3
    dict(
        id='peeking',
        tier='core',
        title='Peeking',
        kicker='Looking at the dashboard is free; stopping because of what you saw is what costs you a 26% false positive rate',
        simple=[
            'An ordinary test only makes its promise if you look once, at the end. Every extra '
            'look is another chance for noise to wander over the line, and the rule "stop when it '
            'goes green" turns those chances into decisions. Evan Miller simulated the extreme '
            'case: check after every single observation and the real false positive rate is 26.1 '
            'per cent, five times what you signed up for. Optimizely ran the realistic ones and '
            'got about 26 per cent checking every 500 visitors, about 20 per cent every thousand, '
            'and over 40 per cent for continuous monitoring.',
            'The important word is stopping, not looking. If you genuinely never act on what you '
            'see, peeking costs nothing at all. Nobody can promise that, because the entire reason '
            'the dashboard exists is so somebody can act early, and the day the number looks '
            'beautiful is the day it happens.',
            'So the fix is not to hide the dashboard, which fails immediately because people take '
            'screenshots. The fix is to change the number printed on it.',
        ],
        analogy=('<b>Like a best-of-seven series you are allowed to stop early.</b> Over seven '
                 'games the better team usually wins. Now let one side call the series off the '
                 'moment it is ahead, and the worse team walks away champion far more often than '
                 'it should. Nothing about how the games are played has changed. Only when you are '
                 'allowed to stop has changed, and that alone is the whole effect.'),
        trap_simple=('"We only peeked twice, so it is basically fine." Two looks roughly doubles '
                     'the rate at which you crown a winner that is not there. The other version is '
                     '"we peeked, but only to check for bugs", which is genuinely fine and which '
                     'nobody can commit to &mdash; the peek that turns up a beautiful number is '
                     'exactly the peek somebody acts on.'),
        tech=[
            'A fixed-horizon p-value is valid at the fixed horizon and nowhere else. Under $H_0$ '
            'the p-value is uniform, so its trajectory over time is essentially a random walk that '
            'dips below any threshold eventually; with unbounded looks and a stop-on-significance '
            'rule the false positive rate tends to 1. The measured version: Evan Miller gets 26.1% '
            'at nominal 5% checking after every observation, and to hold a true 5% with $k$ naive '
            'peeks you must report at about 2.9% for one peek, 2.2% for two, 1.0% for ten.',
            'Say the second cost too, because most candidates only know the first. Stopping early '
            'means stopping <i>conditional on the estimate being extreme</i>, so the shipped effect '
            'is systematically inflated &mdash; a Type M error, not just a Type I one. You get both '
            'a false winner more often and an overstated lift when the winner is real.',
            'Four fixes, and you should be able to name the tradeoff of each: fixed horizon plus '
            'pre-registration (free, inflexible); group sequential with Lan-DeMets alpha spending '
            '(planned looks, needs a max-$n$); always-valid inference / mSPRT (unlimited looks, '
            'costs power); a Bayesian decision rule with an explicit loss. Note what is <i>not</i> '
            'on that list: switching to a Bayesian posterior and keeping the same stopping rule.',
        ],
        tech_note=('Not every look spends alpha. Sample ratio mismatch checks, instrumentation '
                   'sanity and guardrail alarms are looks at a different statistic and a different '
                   'decision &mdash; they do not touch the operating characteristics of your '
                   'primary test, and refusing to run them in the name of purity is worse '
                   'statistics, not better. What spends alpha is repeatedly evaluating the primary '
                   'metric against the launch threshold. Write down before launch which numbers you '
                   'are allowed to act on early, and the distinction becomes auditable rather than '
                   'a matter of trust.'),
        fig=dict(
            kind='plot', xr=(0, 22), yr=(0, 0.30), ph=195,
            xticks=[(1, '1'), (2, '2'), (5, '5'), (10, '10'), (20, '20')],
            yticks=[(0.05, '5%'), (0.10, '10%'), (0.20, '20%'), (0.26, '26%')],
            hlines=[dict(y=0.05, tone='mem', label='the 5% you signed up for')],
            vlines=[dict(x=2, tone='sig', label='"we only peeked twice"')],
            curves=[dict(pts=[(1, 0.05), (2, 0.10), (5, 0.142), (10, 0.20), (20, 0.261)],
                         tone='sig', label='what you actually get',
                         lat=-1, la='end', dx=-10, dy=-10)],
            marks=[dict(x=2, y=0.10, label='roughly double', tone='sig', dx=10, dy=16),
                   dict(x=20, y=0.261, label='26.1%', tone='sig', dx=-10, la='end', dy=16)],
            xlab='times you look at the primary metric and could stop',
            ylab='false positive rate',
            foot='the looking is free. the stopping rule is the thing you are buying.',
            alt='A rising curve of the true false positive rate against the number of times you '
                'check the primary metric under a stop-on-significance rule: five per cent at a '
                'single look, roughly double at two looks, and 26.1 per cent under continuous '
                'checking, set against a flat line marking the five per cent you believe you '
                'bought.'),
        caption=('The flat line is the guarantee you think you have; the curve is the guarantee you '
                 'actually have. The gap opens up almost entirely in the first handful of looks, '
                 'which is why "we only peeked twice" is not the mild concession it sounds like.'),
        caption_simple=('The flat line is the error rate you think you bought. The rising line is '
                        'what you actually have once you allow yourself to stop early. Most of the '
                        'damage is done in the first two or three looks.'),
        when=[
            'The experiment dashboard shows a live p-value that refreshes hourly',
            'A director asks on day 4 whether the result can be called early',
            'Someone proposes stopping because the metric "clearly crossed" this morning',
            'You are designing the results page of an experimentation platform people will watch',
        ],
        trap=('"We only peeked twice, so it is basically fine." Two looks already roughly doubles '
              'your alpha, and to hold a true 5% across two peeks you would have to report at about '
              '2.2%. The subtler version is "we peeked, but only to check for bugs" &mdash; which '
              'is correct in principle and which no team can honestly commit to. And the one that '
              'sounds sophisticated and is not: "we use Bayesian A/B testing, so peeking is not a '
              'problem." That changes the interpretation of the number and not one thing about the '
              'operating characteristics of your stopping rule.'),
        math=dict(
            tex=r'\alpha_{\text{true}} \;=\; P\Bigl(\bigcup_{k=1}^{K}\{\,p_k < 0.05\,\}\ \Big|\ H_0\Bigr) \;\gg\; 0.05',
            note=r'The union over looks, not any single look. Because the p-value trajectory under '
                 r'the null is a random walk, letting $K$ grow without a correction drives this '
                 r'towards 1; Evan Miller measured 26.1% for a look after every observation. The '
                 r'symmetric cost is that $\hat\delta$ at an early stop is conditioned on being '
                 r'extreme, so it is biased upward.',
            cost='one look, at the horizon you named before launch'),
        code=dict(
            label='Five looks at a null experiment',
            cost='numpy + scipy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 '<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n'
                 'LOOKS = [<span class="s">200</span>, <span class="s">400</span>, '
                 '<span class="s">600</span>, <span class="s">800</span>, '
                 '<span class="s">1000</span>]   '
                 '<span class="c"># stop at the first p &lt; .05</span>\n'
                 'fp = <span class="s">0</span>\n\n'
                 '<span class="k">for</span> _ <span class="k">in</span> <span class="k">range</span>(<span class="s">4000</span>):\n'
                 '    a, b = rng.normal(size=<span class="s">1000</span>), rng.normal(size=<span class="s">1000</span>)  '
                 '<span class="c"># NULL IS TRUE</span>\n'
                 '    <span class="k">for</span> n <span class="k">in</span> LOOKS:\n'
                 '        <span class="k">if</span> stats.ttest_ind(a[:n], b[:n]).pvalue &lt; <span class="s">0.05</span>:\n'
                 '            fp += <span class="s">1</span>\n'
                 '            <span class="k">break</span>\n\n'
                 '<span class="k">print</span>(fp / <span class="s">4000</span>)   '
                 '<span class="c"># 0.142 -- five looks, and nothing is happening</span>')),
        real=('Airbnb&rsquo;s price-filter experiment crossed p &lt; 0.05 on day 7 showing about a '
              '4% effect; run to its planned completion the effect was practically null. Airbnb '
              'responded by building simulation-derived, time-varying p-value thresholds into their '
              'platform. Optimizely fixed the same class of bug from the other end: after moving to '
              'mSPRT their platform false positive rate went, in their own words, from over 20% to '
              'under 5% (Johari, Koomen, Pekelis &amp; Walsh, KDD 2017).'),
        drills=[
            dict(q='Our dashboard shows a live p-value that refreshes hourly and the team stops when it drops below 0.05. What is wrong, and how do you fix it without banning the dashboard?',
                 a=('<b>The dashboard is fine; the statistic printed on it is wrong.</b> A '
                    'fixed-horizon p-value is only valid at the horizon, so an hourly refresh plus '
                    'a stop-on-significance rule is effectively unbounded peeking &mdash; Evan '
                    'Miller measured 26.1% at nominal 5% for looks after every observation. Banning '
                    'the dashboard is not a fix, because people screenshot it and decide anyway. '
                    'Serve a statistic that is valid at every look instead: an always-valid p-value '
                    'or confidence sequence from mSPRT, or a group sequential boundary with '
                    'Lan-DeMets spending if you can name a max-$n$. Optimizely did exactly this and '
                    'took their platform false positive rate from over 20% to under 5%.'),
                 a_simple=('<b>The dashboard is fine; the number on it is wrong.</b> The ordinary '
                           'test only keeps its promise if you look once, at the end. Refreshing '
                           'hourly and stopping the moment it looks good is looking hundreds of '
                           'times, and Evan Miller showed that habit turns a five per cent error '
                           'rate into about twenty-six. Taking the dashboard away does not work, '
                           'because people screenshot it and decide anyway. Put a different number '
                           'on it &mdash; one built to stay honest however often you look. '
                           'Optimizely made that switch and their platform error rate fell from '
                           'over twenty per cent to under five.')),
            dict(q='You peeked on day 3, saw p = 0.04, and did not stop. On day 14 it is p = 0.06. What do you report?',
                 a=('<b>You report 0.06 at the pre-declared horizon, and you say out loud that you '
                    'looked.</b> The day-3 number is not evidence of anything: under the null a '
                    'p-value trajectory wanders under 0.05 and back all the time, which is exactly '
                    'why continuous peeking gets to 26%. What matters is whether the look changed a '
                    'decision. If you did not stop, did not extend, did not add traffic and did not '
                    'swap the metric, the horizon-14 test is still valid and the peek cost you '
                    'nothing. If it influenced any of those, the analysis is contaminated and no '
                    'correction applied afterwards repairs it. Then report the interval, and refuse '
                    '"but it was significant on Tuesday".'),
                 a_simple=('<b>You report the day fourteen result, and you say out loud that you '
                           'looked.</b> An early good-looking number is not a finding. Even when '
                           'nothing whatsoever is happening these numbers wander over the line and '
                           'back, which is the entire reason stopping early is dangerous. If the '
                           'peek changed nothing you did, the planned end-of-test result still '
                           'stands and the peek cost you nothing. If the peek made you extend the '
                           'test, add traffic or swap the metric, the result is contaminated and no '
                           'amount of arithmetic afterwards repairs it. Report the range of '
                           'plausible effects, and refuse "but it was significant on Tuesday".')),
            dict(q='Is a Bayesian A/B test immune to peeking?',
                 a=('<b>No &mdash; it changes the interpretation, not the operating '
                    'characteristics.</b> A posterior is a correct statement of belief given the '
                    'data and the prior at any stopping time, but "ship when '
                    '$P(\\delta > 0) > 0.95$, evaluated hourly" is still a stopping rule, and that '
                    'rule has a frequentist error rate you can measure by simulation. With a weak '
                    'prior it comes out close to the frequentist one, because the posterior is '
                    'close to the likelihood. Two things genuinely help, and neither is the word '
                    '"Bayesian": an informative prior, which really does damp early noise and which '
                    'you then have to defend; and a loss function, so you stop when expected loss '
                    'from shipping falls below a threshold set in advance.'),
                 a_simple=('<b>No &mdash; it changes what the number means, not how often you are '
                           'wrong.</b> Switching to Bayesian language does not remove the fact that '
                           'you are deciding, over and over, whether to stop. Simulate that rule and '
                           'it crowns false winners at close to the rate the ordinary version does, '
                           'whenever your starting beliefs are vague. Two things do help. A strong, '
                           'defensible starting belief damps the early noise. And deciding in '
                           'advance how much expected damage you will risk from shipping, then '
                           'stopping when estimated damage drops below it, is a rule you can '
                           'actually hold yourself to.')),
        ],
        anchor=dict(
            formula=r'to hold a true 5%: report at $\approx 2.9\%$ (1 peek), $2.2\%$ (2), $1.0\%$ (10) &nbsp;&middot;&nbsp; or change the statistic',
            formula_simple='Looking is free. Stopping because of what you saw is what costs you, '
                           'and at the extreme it costs about five times the error rate you think '
                           'you have.',
            bullets=[
                'A fixed-horizon p-value is valid at the horizon you named before launch, and nowhere else',
                'Two looks roughly doubles alpha; a look after every observation gives 26.1 per cent',
                'Keep the dashboard, change the statistic &mdash; always-valid or group sequential',
                'Early stopping inflates the effect as well as the error rate',
            ]),
        chips=['sequential testing', 'alpha spending', 'mSPRT', 'winner&rsquo;s curse',
               'pre-registration'],
        followup='Our dashboard shows a live p-value hourly and the team stops when it drops below 0.05 — what is wrong, and how do you fix it without banning the dashboard?',
    ),

    # ------------------------------------------------------------------ 4
    dict(
        id='sequential-testing',
        tier='core',
        title='Sequential testing and always-valid inference',
        kicker='The 2026 expectation is not &ldquo;do not peek&rdquo; &mdash; it is which of the three fixes you would deploy, and what it costs you',
        simple=[
            'There are three ways to buy the right to stop early, and each has a price. The first '
            'is to plan your looks &mdash; five of them, one a day &mdash; and split your error '
            'budget across them, spending a little at each. Because it was budgeted in advance the '
            'total still comes to one in twenty. This is the most sensitive option, and the catch '
            'is that you must estimate in advance how big the test will get.',
            'The second gives up the plan entirely and hands you a number that stays honest '
            'whenever you look, however often, forever. You pay for that freedom in sensitivity. '
            'The third is a Bayesian rule with an explicit statement of what a bad launch costs.',
            'The line worth saying out loud is that you only pay for the peeking you make. And the '
            'cost is not theoretical: in Spotify&rsquo;s own published simulation the planned-looks '
            'method caught about ninety per cent of real effects where the look-whenever methods '
            'caught seventy-two to seventy-seven. A candidate who says sequential testing solves '
            'peeking, full stop, has read about it. A candidate who quotes that gap has run it.',
        ],
        analogy=('<b>Like a season ticket versus a day pass.</b> The season ticket is cheaper per '
                 'match but you have to commit to the fixture list up front. Day passes let you '
                 'turn up whenever you feel like it, forever, with no plan at all, and you pay more '
                 'each time. Neither is cleverer in general. It depends entirely on whether you '
                 'know the fixture list &mdash; and for a scheduled two-week test, you do.'),
        trap_simple=('Saying "we use sequential testing" as though it were free. Every one of these '
                     'methods buys the right to stop early with sensitivity, and someone who cannot '
                     'say roughly how much has not configured one. Name the number: in '
                     'Spotify&rsquo;s comparison the planned-looks method held about ninety per cent '
                     'where the peek-whenever methods sat in the low to mid seventies.'),
        tech=[
            '<b>Group sequential (GST) with Lan-DeMets alpha spending.</b> You declare $K$ looks and '
            'a spending function $\\alpha^*(t)$ that allocates $\\alpha$ across them by information '
            'fraction $t = n_k/n_{\\max}$. O&rsquo;Brien-Fleming spends almost nothing early, so an '
            'early stop demands an enormous effect; Pocock spends evenly. Highest power, '
            'batch-friendly, and it needs a max-$n$ estimate. Spotify ships this, because their '
            'data arrives in daily batches.',
            '<b>Always-valid inference / mSPRT.</b> A mixture sequential probability ratio test '
            'gives a p-value and a confidence sequence valid at every $n$ simultaneously &mdash; '
            'Ville&rsquo;s inequality is what makes that work. No max-$n$, streaming-friendly, '
            'unlimited looks. You tune a mixture variance, which is effectively a prior on the '
            'effect size, and the tuning is where the power goes. Optimizely, Uber and Netflix ship '
            'this; GAVI (Eppo) and corrected-alpha (Statsig) are the same family with different '
            'knobs.',
            'The numbers that settle it, from Spotify&rsquo;s simulation at 500 observations per '
            'arm and a $0.2\\sigma$ effect: GST about 90% power, GAVI 72&ndash;76%, mSPRT '
            '72&ndash;77%, Bonferroni over 14 looks about 75%. So the answer to "why not always use '
            'the safest one" is that when you can name the horizon &mdash; and for a scheduled test '
            'you can &mdash; you are handing over roughly 15 points of power for a freedom you are '
            'not using. Pick by how the data arrives, not by dogma.',
        ],
        tech_note=('Say what you get back, or the card sounds like pure cost. Sequential designs buy '
                   'expected duration: a test with a large true effect crosses the boundary in days '
                   'rather than weeks, so you lose power per test and gain tests per quarter, which '
                   'is a portfolio argument rather than a per-experiment one. Two honest caveats. '
                   'The confidence sequence at an early stop is wider than the fixed-horizon '
                   'interval would have been, so the effect you ship is less precisely estimated. '
                   'And an early stop is still selection on an extreme estimate, so the winner&rsquo;s '
                   'curse applies on top.'),
        fig=dict(
            kind='compare', h=200,
            left=dict(t='group sequential + alpha spending', tone='mem',
                      lines=['about 90% power',
                             'you must estimate a max sample size',
                             'looks are planned, batch-friendly',
                             'Lan-DeMets spending function',
                             'shipped by Spotify (daily batches)']),
            right=dict(t='always-valid / mSPRT', tone='sig',
                       lines=['72 to 77% power',
                              'no max sample size needed',
                              'look as often as you like, forever',
                              'you tune a mixture variance',
                              'shipped by Optimizely, Uber, Netflix']),
            foot='Spotify simulation: 500 observations per arm, effect of 0.2 standard deviations',
            alt='A side-by-side comparison of group sequential testing and always-valid inference. '
                'The left column has about ninety per cent power but requires an estimated maximum '
                'sample size and planned looks; the right column has seventy-two to seventy-seven '
                'per cent power but allows unlimited looks with no maximum sample size.'),
        caption=('Both columns hold a true 5% error rate. The difference is entirely what you must '
                 'know in advance and what you pay for not knowing it. An interviewer asking about '
                 'sequential testing is asking you to pick a column and defend it against the shape '
                 'of your data, not to recite that peeking is bad.'),
        caption_simple=('Both of these keep your error rate honest. The difference is what you must '
                        'commit to up front, and what not committing costs you in sensitivity. The '
                        'question is never which one is better, it is which one fits how your data '
                        'arrives.'),
        when=[
            'You are choosing what your experimentation platform prints on the results page',
            'A team wants the right to stop early and you have to price it for them',
            'The test is scheduled for two weeks and someone proposes always-valid inference',
            'A very large win is obvious on day 3 and stopping early is worth real money',
        ],
        trap=('Naming "sequential testing" as a buzzword and going quiet when asked what it costs. '
              'The sentence that fails the loop is "we use sequential testing, so peeking is free" '
              '&mdash; every one of these methods buys the right to stop early with power, and the '
              'number is 12 to 18 points in Spotify&rsquo;s comparison. The mirror-image failure is '
              'the reverse dogma: "always-valid is strictly safer so we always use it", which '
              'throws away that power on a scheduled two-week test where you could simply have '
              'named the horizon.'),
        math=dict(
            tex=r'\sum_{k=1}^{K}\alpha_k \;=\; \alpha, \qquad t \;=\; \frac{n_k}{n_{\max}}, \qquad \alpha^{*}(t) \;=\; 2 - 2\,\Phi\!\left(\frac{z_{1-\alpha/2}}{\sqrt{t}}\right)',
            note='The spending function decides how much of the budget each look costs. The '
                 'O&rsquo;Brien-Fleming form above spends almost nothing early, which is why an '
                 'early stop under it requires a very large effect and why it barely dents your '
                 'final-look power. You only pay for the peeking you make &mdash; but $t$ is '
                 'defined against $n_{\\max}$, and having to name $n_{\\max}$ is exactly what '
                 'always-valid inference frees you from.',
            cost='you must estimate the maximum sample size'),
        code=dict(
            label='An always-valid p-value, checked 20,000 times',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n'
                 'tau2 = <span class="s">0.01</span>              '
                 '<span class="c"># mixture variance: a prior on the effect. THE knob</span>\n'
                 'a = rng.normal(<span class="s">0</span>, <span class="s">1</span>, <span class="s">20_000</span>)\n'
                 'b = rng.normal(<span class="s">0</span>, <span class="s">1</span>, <span class="s">20_000</span>)   '
                 '<span class="c"># NULL IS TRUE</span>\n\n'
                 'n = np.arange(<span class="s">1</span>, <span class="s">20_001</span>)\n'
                 'd = np.cumsum(a - b) / n            '
                 '<span class="c"># running difference of means</span>\n'
                 'v = <span class="s">2.0</span> / n                       '
                 '<span class="c"># and its variance</span>\n\n'
                 'lr = np.sqrt(v / (v + tau2)) * np.exp(d**<span class="s">2</span> * tau2 / '
                 '(<span class="s">2</span> * v * (v + tau2)))\n'
                 'p = np.minimum(<span class="s">1.0</span>, <span class="s">1.0</span> / '
                 'np.maximum.accumulate(lr))\n\n'
                 '<span class="k">print</span>((p &lt; <span class="s">0.05</span>).any())  '
                 '<span class="c"># False ~96.5% of the time -- across ALL 20,000 looks</span>')),
        real=('Spotify published the comparison in March 2023: group sequential, mSPRT, GAVI and '
              'corrected-alpha, simulated at 500 observations per arm against a 0.2 standard '
              'deviation effect. GST came out at about 90% power, GAVI at 72&ndash;76%, mSPRT at '
              '72&ndash;77% and Bonferroni over 14 looks at about 75%. They chose GST with '
              'Lan-DeMets spending because their data arrives in daily batches. The same study '
              'found that underestimating the maximum sample size by 50 times cost GAVI roughly 30 '
              'points of power against a well-configured GST. Booking.com published a comparable '
              'writeup of their own.'),
        drills=[
            dict(q='Why would you not just always use always-valid inference, since it is strictly safer?',
                 a=('<b>Because the safety is bought with power you may not need to spend.</b> '
                    'Always-valid inference is uniformly valid over stopping times, which is worth a '
                    'great deal when you genuinely cannot name a horizon &mdash; a streaming metric, '
                    'or a platform where any team can stop any test at any hour. For a scheduled '
                    'two-week experiment you can name it, and Spotify prices the difference: about '
                    '90% power for a group sequential design against 72&ndash;77% for mSPRT and GAVI '
                    'on identical data at 500 observations per arm. Fifteen points of power is '
                    'roughly another week of traffic on every test you run. Choose by design: batch '
                    'data with a known max-$n$ goes GST, streaming with unbounded looks goes '
                    'always-valid.'),
                 a_simple=('<b>Because the safety is paid for with sensitivity you may not need to '
                           'spend.</b> The look-whenever methods earn their cost when you genuinely '
                           'cannot say in advance how big the test will get &mdash; a live stream, '
                           'or a platform where anyone can stop anything at any hour. For a test '
                           'already scheduled for two weeks, you can say. Spotify measured the gap on '
                           'identical data: about ninety per cent of the real effects caught with '
                           'planned looks, against roughly three quarters with the look-whenever '
                           'ones. That difference is another week of traffic on every experiment you '
                           'run. Choose by how the data arrives, not by which sounds safest.')),
            dict(q='A group sequential test is configured with a max sample size of 100,000 per arm. Two weeks in you realise traffic is far higher and the true max is 5 million. What happens?',
                 a=('<b>Your spending schedule was computed against the wrong clock, and the design '
                    'degrades badly.</b> The spending function allocates by information fraction '
                    '$t = n_k/n_{\\max}$, so if $n_{\\max}$ is wrong by orders of magnitude every '
                    'look believes it is far later in the test than it is, and spends far too much '
                    'alpha early. Spotify measured exactly this: underestimating max-$n$ by 50 times '
                    'cost GAVI about 30 points of power against a well-configured GST. And you '
                    'cannot quietly re-plan mid-flight either &mdash; changing $n_{\\max}$ after '
                    'seeing the data is peeking with extra steps. Either pre-register a re-planning '
                    'rule, or use the method that needs no $n_{\\max}$ at all, which is the argument '
                    'for always-valid inference in one sentence.'),
                 a_simple=('<b>Your error budget was spread against the wrong timeline, and the '
                           'design falls apart.</b> A planned-looks design divides its budget by how '
                           'far through the test it thinks it is. Guess the finishing line badly and '
                           'every check believes it is nearly at the end, so it spends most of the '
                           'budget in the first few days. Spotify measured this: getting the maximum '
                           'size wrong by a factor of fifty cost about thirty points of sensitivity '
                           'against a properly configured design. You also cannot quietly move the '
                           'finishing line after seeing the data &mdash; that is peeking with extra '
                           'steps. Either write the re-planning rule down in advance, or use the '
                           'method that needs no finishing line.')),
            dict(q='The boundary is crossed on day 3 and the estimated lift is +6%. Do you ship, and what do you tell the PM the lift is?',
                 a=('<b>Ship if that boundary is what you pre-registered &mdash; but do not tell '
                    'them +6%.</b> Crossing a boundary means stopping conditional on the estimate '
                    'being extreme, so the point estimate at an early stop is biased upward. That is '
                    'the winner&rsquo;s curse, and Airbnb&rsquo;s Experiment Reporting Framework '
                    'puts the overstatement at 20&ndash;50%. Report the confidence sequence rather '
                    'than a fixed-horizon interval &mdash; it is wider, and that width is the honest '
                    'price of the early look &mdash; and hand forecasting a shrunk estimate. '
                    'Facebook&rsquo;s News Feed team cut mean squared error by 44% across 226 tests '
                    'doing precisely this. Shipping and forecasting are two separate decisions and '
                    'the answer can be yes to one and much lower on the other.'),
                 a_simple=('<b>Ship if that stopping line is what you agreed in advance &mdash; but '
                           'do not promise a six per cent lift.</b> Stopping early means stopping '
                           'precisely because the number looked big, and numbers selected for being '
                           'big are, on average, too big. Airbnb measured shipped effects being '
                           'overstated by twenty to fifty per cent. So report the wider range that '
                           'goes with an early stop, and give the planning team a deliberately '
                           'shrunk figure. Facebook did this across two hundred and twenty-six tests '
                           'and cut their forecasting error by almost half. Whether to ship and what '
                           'to forecast are two different questions.')),
        ],
        anchor=dict(
            formula=r'GST: $\sum_k \alpha_k = \alpha$, needs $n_{\max}$, $\approx$ 90% power &nbsp;&middot;&nbsp; mSPRT: valid at every $n$, no $n_{\max}$, 72&ndash;77%',
            formula_simple='Planned looks with a shared error budget give the most sensitivity but '
                           'need a finishing line. Look-whenever methods need no finishing line and '
                           'cost you about fifteen points of it.',
            bullets=[
                'Every sequential method buys the right to stop early with power &mdash; name the number',
                'Batch data and a known horizon: group sequential. Streaming and unbounded looks: always-valid',
                'You only pay for the peeking you make',
                'An early stop still overstates the effect &mdash; report the sequence, shrink the estimate',
            ]),
        chips=['alpha spending', 'Lan-DeMets', 'confidence sequence', 'winner&rsquo;s curse',
               'expected duration'],
        followup='Why would you not just always use always-valid inference, since it is strictly safer?',
    ),

    # ------------------------------------------------------------------ 5
    dict(
        id='multiple-comparisons',
        tier='core',
        title='Multiple comparisons',
        kicker='The correction is the easy half; deciding what belongs in the family, and what you deliberately leave alone, is the answer',
        simple=[
            'Everyone can name a correction. The decision that actually separates candidates is '
            'which tests belong together in one family, and which ones you deliberately leave '
            'uncorrected.',
            'Three buckets, all declared before launch. One primary metric, which is the launch '
            'decision, tested once at the usual bar and not corrected, because there is only one of '
            'it. Guardrails &mdash; latency, crashes, complaints, revenue &mdash; also uncorrected, '
            'and this one surprises people: correcting a guardrail raises its bar, which makes it '
            'less likely to fire, which is the opposite of what a safety net is for. A false alarm '
            'there costs an engineer five minutes. A miss ships a regression to everybody. '
            'Everything else is exploratory, gets corrected as a group, and anything that survives '
            'becomes the question for the next experiment rather than a finding in this one.',
            'Then count honestly. Twelve metrics is twelve tests. Twelve metrics across five '
            'countries and three time windows is a hundred and eighty, and almost nobody declares '
            'those.',
        ],
        analogy=('<b>Like a metal detector and a jury.</b> The detector at the airport is tuned to '
                 'shriek at belt buckles, because a false alarm costs thirty seconds and a miss '
                 'costs a plane. The jury needs proof beyond reasonable doubt, because a wrong '
                 'conviction is catastrophic and irreversible. Running both at the same threshold '
                 'would be wrong in both directions. Your primary metric is the jury. Your '
                 'guardrails are the metal detector.'),
        trap_simple=('Applying one blanket correction to twelve metrics that all move together and '
                     'calling it handled. Metrics from a single experiment are heavily correlated, '
                     'and the strictest correction assumes they are independent, so on correlated '
                     'metrics it is far harsher than the situation warrants and you end up unable to '
                     'detect anything at all. And it still does nothing about the five countries and '
                     'three time windows you also sliced, which is where most of the undeclared '
                     'testing actually lives.'),
        tech=[
            'Two guarantees, and they are not interchangeable. <b>FWER</b> is the probability of at '
            'least one false positive in the family: Bonferroni ($\\alpha/m$) controls it, and '
            'Holm&rsquo;s step-down ($p_{(i)} \\leq \\alpha/(m-i+1)$) controls it too while being '
            'uniformly more powerful, so plain Bonferroni has no remaining use case. <b>FDR</b> is '
            'the expected proportion of your rejections that are false: Benjamini-Hochberg controls '
            'it by rejecting the largest $i$ with $p_{(i)} \\leq iq/m$.',
            'The choice is a cost question, not a taste one. Control FWER when a single false '
            'positive is expensive and you will act on each rejection individually &mdash; one '
            'launch decision, one safety claim. Control FDR when you are screening and the output '
            'is a shortlist somebody will follow up: 200 features, 40 prompt variants, a metric '
            'sweep. Ten per cent of a shortlist being wrong is fine if the next step is to check '
            'them.',
            'And the part worth more than either: the family is a design decision. Bonferroni over '
            '12 correlated metrics is conservative to the point of uselessness precisely because it '
            'assumes independence. The industry fix is structural &mdash; pre-register one primary '
            'metric, keep guardrails uncorrected and deliberately sensitive, run Benjamini-Hochberg '
            'over the exploratory set, and require a fresh confirmation run for anything found in '
            'the tail.',
        ],
        tech_note=('Two hidden families. The first is slicing: 12 metrics by 5 segments by 3 time '
                   'windows is 180 tests, and correcting the metrics while leaving the segments '
                   'uncounted is the most common half-fix in the industry. The second is selection '
                   'on the maximum &mdash; reporting the best of 12 prompt variants at 88% as though '
                   'it were an unbiased estimate. That needs a max-$T$ or bootstrap correction, or, '
                   'far more simply, a held-out confirmation set that the winner has never touched.'),
        fig=dict(
            kind='grid',
            head=['WHAT YOU DECLARED', 'WHAT YOU CORRECT'],
            xlab='which family is this test in', ylab='the decision',
            cols=['primary metric', 'guardrails', 'exploratory'],
            rows=['correct it?', 'what a hit means'],
            cells=[
                [dict(t='NO', sub='one declared test', tone='mem', fill=True),
                 dict(t='NO', sub='you want it sensitive', tone='mem', fill=True),
                 dict(t='YES', sub='Benjamini-Hochberg', tone='sig', fill=True)],
                [dict(t='ship or do not', sub='this is the decision', tone='mem'),
                 dict(t='five-minute check', sub='cheap to be wrong', tone='plain'),
                 dict(t='next experiment', sub='not a result yet', tone='sig')],
            ],
            foot='the correction is the easy half. deciding which column a test sits in is the answer.',
            alt='A table splitting the tests in one experiment into three families - the single '
                'pre-declared primary metric, the guardrails, and everything exploratory - and '
                'giving for each whether you correct it and what a hit actually means.'),
        caption=('Nothing in this table is a statistical choice; every cell is a cost. Correcting '
                 'the guardrail column makes your experiment look more rigorous and makes your '
                 'product less safe, which is why "did you correct everything?" is a worse answer '
                 'than "here is what I corrected and why".'),
        caption_simple=('Every cell here is a cost decision rather than a statistical one. '
                        'Tightening the bar on the guardrails would make the analysis look more '
                        'careful and make the product less safe &mdash; which is why correcting '
                        'everything is a worse answer than knowing what you left alone.'),
        when=[
            'A results page shows 12 metrics and someone declares a win because one is green',
            'You swept 40 prompt variants and the best scored 88% against a baseline of 81%',
            'The overall result is flat but significant in one country, and someone wants to ship there',
            'A safety review asks you to apply a correction to every guardrail',
        ],
        trap=('"We applied Bonferroni to the twelve metrics, so multiplicity is handled." Two things '
              'are wrong and one is fatal. Bonferroni assumes independence, the twelve metrics of a '
              'single experiment move together, so you have traded a false positive problem for an '
              'inability to detect anything &mdash; and Holm dominates it at the same guarantee '
              'anyway. The fatal one: nobody corrected the five segments and three time windows that '
              'were also sliced, which is 180 tests that were never declared and which no correction '
              'applied to the twelve can reach.'),
        math=dict(
            tex=r'\text{Holm: } p_{(i)} \leq \frac{\alpha}{m-i+1} \qquad\qquad \text{BH: largest } i \text{ with } p_{(i)} \leq \frac{i}{m}\,q',
            note='Holm bounds the probability of <i>any</i> false positive; BH bounds the expected '
                 '<i>fraction</i> of your rejections that are false. Holm is uniformly more powerful '
                 'than Bonferroni at an identical guarantee. Neither of them knows anything about the '
                 'segments you sliced afterwards, which is why $m$ is a design decision made before '
                 'you look and not an argument you have with the results page.',
            cost='you must declare the family before you look'),
        code=dict(
            label='Same twelve p-values, three different guarantees',
            cost='statsmodels',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 '<span class="k">from</span> statsmodels.stats.multitest '
                 '<span class="k">import</span> multipletests\n\n'
                 '<span class="c"># 12 metrics from ONE experiment, sorted</span>\n'
                 'p = np.array([<span class="s">0.0009</span>, <span class="s">0.0045</span>, '
                 '<span class="s">0.011</span>, <span class="s">0.015</span>, '
                 '<span class="s">0.020</span>, <span class="s">0.028</span>,\n'
                 '              <span class="s">0.049</span>, <span class="s">0.14</span>, '
                 '<span class="s">0.33</span>, <span class="s">0.50</span>, '
                 '<span class="s">0.70</span>, <span class="s">0.95</span>])\n\n'
                 '<span class="k">for</span> m <span class="k">in</span> '
                 '(<span class="s">"bonferroni"</span>, <span class="s">"holm"</span>, '
                 '<span class="s">"fdr_bh"</span>):\n'
                 '    rej, *_ = multipletests(p, alpha=<span class="s">0.05</span>, method=m)\n'
                 '    <span class="k">print</span>(m, rej.sum())\n\n'
                 '<span class="c"># bonferroni 1   alpha/12 = 0.0042, and 0.0045 just misses</span>\n'
                 '<span class="c"># holm       2   SAME guarantee, never weaker. never use bonferroni</span>\n'
                 '<span class="c"># fdr_bh     5   DIFFERENT guarantee: 5% of these five may be false</span>')),
        real=('Bennett and colleagues put a dead Atlantic salmon in an fMRI scanner in 2009, showed '
              'it photographs of humans in social situations, and ran the standard voxelwise '
              'analysis over roughly 130,000 voxels with no correction. A cluster of voxels in the '
              'dead fish&rsquo;s brain cavity came out "active" at p &lt; 0.001. The poster won an '
              'Ig Nobel in 2012 and was built explicitly as an argument for mandatory '
              'multiple-comparison correction in neuroimaging. The industry version of the salmon is '
              'a results page with twelve metrics on it and a green tick next to one of them.'),
        drills=[
            dict(q='We ran 10 variants and one won at p < 0.05. Would you ship it?',
                 a=('<b>Not on that evidence.</b> Ten comparisons at 5% is $1 - 0.95^{10} \\approx '
                    '40\\%$ chance of at least one false winner before you have learned anything &mdash; '
                    'and you also selected on the maximum, so the winner&rsquo;s estimated lift is '
                    'biased upward even when the effect is real. Two moves. Statistically: Holm '
                    'across the ten, and report the winner&rsquo;s interval rather than its point '
                    'estimate. Structurally, and this is the one that gets the offer: rerun the '
                    'winner head-to-head against control as a fresh two-arm test. A ten-arm test is a '
                    'hypothesis generator; the confirmation run is the result. Also ask what the ten '
                    'were &mdash; if they are ten settings of one continuous knob, that is a '
                    'dose-response curve, not ten hypotheses.'),
                 a_simple=('<b>Not on that evidence.</b> Ten separate comparisons at the usual bar '
                           'means roughly a two-in-five chance that at least one looks like a winner '
                           'on luck alone. Worse, you picked the biggest of ten numbers, and the '
                           'biggest of ten flatters itself even when all ten are noise, so the '
                           'reported lift is too high as well. Raise the bar across all ten, and '
                           'report the winner as a range rather than a headline number. Then do the '
                           'thing that actually settles it: run the winner against control on its '
                           'own, on fresh traffic. A ten-way test generates a hypothesis. The rerun '
                           'is the result.')),
            dict(q='We track 12 metrics and declare a win if any of them hits p < 0.05. Redesign it.',
                 a=('<b>Three families, declared before launch, and only one of them decides the '
                    'launch.</b> One primary metric &mdash; the OEC &mdash; tested once at 5%, '
                    'uncorrected because it is one test, and it alone decides ship or not. Guardrails '
                    'left uncorrected and deliberately sensitive, because a false alarm costs a '
                    'ten-minute investigation and a miss ships a latency regression to everyone. '
                    'Everything else exploratory, Benjamini-Hochberg at $q = 0.1$, and whatever '
                    'survives is the hypothesis for the next experiment rather than a result in this '
                    'one. Then close the hole nobody mentions: segments and time windows join the '
                    'exploratory family, so 12 metrics over 5 segments is $m = 60$, not 12.'),
                 a_simple=('<b>Three families, declared before launch, and only one of them decides '
                           'the launch.</b> Name a single metric in advance that the launch turns on, '
                           'and judge it once at the usual bar. Keep the safety metrics deliberately '
                           'twitchy and do not tighten them at all, because a false alarm there costs '
                           'somebody ten minutes while a miss ships a slower, more crash-prone '
                           'product to everyone. Everything else is exploration: tighten it as a '
                           'group, and treat whatever survives as the question for the next '
                           'experiment. And count the slices &mdash; twelve metrics looked at across '
                           'five countries is sixty checks, not twelve.')),
            dict(q='Should you apply a multiple-comparisons correction to your guardrail metrics?',
                 a=('<b>No, and being able to say why is the whole point of the question.</b> A '
                    'correction lowers the false positive rate by raising the bar, which necessarily '
                    'lowers power. For a guardrail that is the wrong trade in both directions at '
                    'once: a false alarm costs an engineer ten minutes confirming nothing broke, and '
                    'a miss ships a latency or crash regression to the entire user base. You want '
                    'guardrails over-sensitive on purpose, and you handle the resulting noise with a '
                    'triage process, not with a threshold. Corrections belong where a false positive '
                    'is expensive and acted on &mdash; the launch decision, and the exploratory set '
                    'that might become next quarter&rsquo;s roadmap. Correcting guardrails is how '
                    'teams make an analysis look rigorous while making the product less safe.'),
                 a_simple=('<b>No, and being able to say why is the whole point of the question.</b> '
                           'Tightening the bar makes false alarms rarer and misses more common. For a '
                           'safety metric that is exactly the wrong swap: a false alarm costs an '
                           'engineer ten minutes of checking, and a miss ships a slower, more '
                           'crash-prone product to everybody. You want those alarms twitchy on '
                           'purpose, and you deal with the noise by having someone triage it rather '
                           'than by raising the bar. Save the tightening for the places where being '
                           'wrong is expensive and someone will act on it: the launch decision '
                           'itself, and the exploratory findings that might become next '
                           'quarter&rsquo;s roadmap.')),
        ],
        anchor=dict(
            formula=r'Holm for the decision &nbsp;&middot;&nbsp; BH for the screen &nbsp;&middot;&nbsp; nothing for the guardrails &nbsp;&middot;&nbsp; and $m$ counts the segments',
            formula_simple='Correct the things you will act on one at a time. Leave the safety '
                           'alarms twitchy on purpose. Count the slices, because they are tests too.',
            bullets=[
                'One guarantee is the chance of any false positive; the other is the fraction of your hits that are false',
                'Holm beats Bonferroni at the same guarantee, so plain Bonferroni has no use case left',
                'The family is a design decision, and segments and time windows belong to it',
                'The real fix is one pre-registered primary metric plus a confirmation run for the winner',
            ]),
        chips=['Holm step-down', 'Benjamini-Hochberg', 'false discovery rate', 'OEC',
               'selection on the max'],
        followup='We ran 10 variants and one won at p < 0.05 — would you ship it?',
    ),
]
