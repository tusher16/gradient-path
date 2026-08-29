CARDS = [

# ============================================================================
dict(
    id='bayesian-inference',
    tier='advanced',
    title='Bayesian inference',
    kicker='It gives you the probability statement everyone wants, at the price of defending a prior in public',
    simple=[
        'You start with what you already believed about a number &mdash; a conversion rate, a '
        'failure rate, a click-through. Then the data arrives and tells you, for every value that '
        'number could take, how well that value explains what you saw. Multiply the two together '
        'and you get where you end up. That is the whole machine: what you believed, weighted by '
        'how well each answer explains the evidence.',
        'The part worth arguing about is the starting point, because it is worth a specific '
        'number of imaginary observations. A starting point worth forty observations, meeting '
        'forty real ones, lands you exactly halfway between the two. Meeting four hundred real '
        'ones, it barely registers. So the starting point matters most in precisely the '
        'situations people reach for it &mdash; a new market, a thin eval set, a segment with '
        'nine users. And there is no way to opt out of having one. Refusing to choose is itself '
        'a choice, and a surprisingly strong one.',
    ],
    analogy=('<b>Like hiring for a role you have already filled forty times.</b> You do not start '
             'each candidate from nothing; you start from what forty hires taught you, and the '
             'interview moves you off that starting point. Someone who insists they start from '
             'nothing has really started from &ldquo;every candidate is equally likely to be '
             'brilliant&rdquo; &mdash; which is not neutrality, it is a strong claim about the '
             'world, stated quietly.'),
    simple_extra=('The other thing you buy is the sentence people wrongly say about ordinary '
                  'ranges of plausible values. Here you really are allowed to say there is a '
                  'ninety-five percent chance the true rate sits inside this range &mdash; given '
                  'your model and your starting point. That caveat is not a formality. It is the '
                  'thing a stakeholder is entitled to reject, and you should be ready to show '
                  'them how much the answer moves if they do.'),
    trap_simple=('Saying &ldquo;we used a flat starting point, so the result is objective&rdquo;. '
                 'Flat over the rate is not flat over the odds, and it has consequences you can '
                 'check by hand: with zero conversions in three sessions, the flat starting point '
                 'hands you twenty percent. That is not nothing. That is an opinion.'),
    tech=[
        'The posterior is proportional to the likelihood times the prior, and every argument you '
        'will have is about the second factor. A credible interval genuinely licenses the '
        'sentence &ldquo;95% probability the parameter is in here&rdquo; &mdash; conditional on '
        'the model and the prior &mdash; which is the sentence candidates wrongly attach to a '
        'confidence interval. That conditioning clause is the whole trade.',
        'Know three conjugate pairs and stop: Beta&ndash;Binomial for rates, Gamma&ndash;Poisson '
        'for counts, Normal&ndash;Normal for means. Conjugacy is a computational convenience, not '
        'a principle &mdash; it exists so the update is arithmetic instead of MCMC, and the '
        'moment your model stops being conjugate you sample and nothing about the logic changes. '
        'What conjugacy does buy you is an honest unit for the prior: $\\text{Beta}(\\alpha, '
        '\\beta)$ is $\\alpha - 1$ prior successes and $\\beta - 1$ prior failures, so you can '
        'state the strength of your belief in observations and let someone argue with the number.',
        'Which is why $\\text{Beta}(1,1)$ is not &ldquo;no prior&rdquo;. It is flat on $p$, and '
        'flat on $p$ is not flat on $p/(1-p)$ &mdash; a different parameterisation of the same '
        'claimed ignorance gives a different posterior, so you have to say which scale you were '
        'flat on. Check it with arithmetic: 0 successes in 3 trials under $\\text{Beta}(1,1)$ '
        'gives a posterior mean of $1/5$. Twenty percent, from a prior that supposedly said '
        'nothing.',
    ],
    tech_note=('With a lot of data the prior washes out and Bayesian and frequentist intervals '
               'converge, so the argument is loudest exactly where the data are thinnest. The '
               'defence is not to claim your prior is right, it is to show a sensitivity analysis '
               'across priors &mdash; a flat one, yours, and a deliberately hostile one &mdash; '
               'and then say which decisions actually change. If none of them change, the prior '
               'was never the issue and you have said so with evidence.'),
    fig=dict(
        kind='plot',
        head=['WHAT YOU BROUGHT', 'WHAT YOU LEAVE WITH'],
        xr=(0.0, 0.55), yr=(0, 9.2), ph=210,
        xlab='conversion rate',
        ylab='plausibility',
        xticks=[(0.10, '10%'), (0.20, '20%'), (0.25, '25%'), (0.30, '30%'),
                (0.40, '40%'), (0.50, '50%')],
        curves=[
            dict(tone='plain', label='prior  20%', la='middle', dx=0, dy=-10, lat=9,
                 pts=[(0.045, 0.04), (0.060, 0.20), (0.075, 0.59), (0.090, 1.27), (0.105, 2.22),
                      (0.120, 3.35), (0.135, 4.49), (0.150, 5.45), (0.165, 6.12), (0.180, 6.42),
                      (0.195, 6.34), (0.210, 5.94), (0.225, 5.32), (0.240, 4.56), (0.255, 3.76),
                      (0.270, 2.98), (0.285, 2.29), (0.300, 1.70), (0.315, 1.22), (0.330, 0.85),
                      (0.345, 0.58), (0.360, 0.38), (0.375, 0.24), (0.390, 0.15), (0.405, 0.09),
                      (0.420, 0.05), (0.435, 0.03), (0.450, 0.02), (0.465, 0.01), (0.480, 0.00),
                      (0.495, 0.00)]),
            dict(tone='sig', label='data  30%', la='middle', dx=0, dy=-10, lat=17,
                 pts=[(0.045, 0.00), (0.060, 0.00), (0.075, 0.00), (0.090, 0.00), (0.105, 0.02),
                      (0.120, 0.06), (0.135, 0.14), (0.150, 0.31), (0.165, 0.60), (0.180, 1.02),
                      (0.195, 1.59), (0.210, 2.29), (0.225, 3.07), (0.240, 3.85), (0.255, 4.56),
                      (0.270, 5.12), (0.285, 5.48), (0.300, 5.60), (0.315, 5.48), (0.330, 5.15),
                      (0.345, 4.66), (0.360, 4.06), (0.375, 3.41), (0.390, 2.77), (0.405, 2.17),
                      (0.420, 1.64), (0.435, 1.20), (0.450, 0.85), (0.465, 0.58), (0.480, 0.38),
                      (0.495, 0.24)]),
            dict(tone='mem', fill=True, label='posterior  25%', la='middle', dx=0, dy=-11, lat=13,
                 pts=[(0.045, 0.00), (0.060, 0.00), (0.075, 0.00), (0.090, 0.00), (0.105, 0.02),
                      (0.120, 0.09), (0.135, 0.31), (0.150, 0.81), (0.165, 1.72), (0.180, 3.09),
                      (0.195, 4.75), (0.210, 6.41), (0.225, 7.67), (0.240, 8.25), (0.255, 8.05),
                      (0.270, 7.19), (0.285, 5.90), (0.300, 4.47), (0.315, 3.15), (0.330, 2.06),
                      (0.345, 1.26), (0.360, 0.72), (0.375, 0.39), (0.390, 0.19), (0.405, 0.09),
                      (0.420, 0.04), (0.435, 0.02), (0.450, 0.01), (0.465, 0.00), (0.480, 0.00),
                      (0.495, 0.00)]),
        ],
        foot='the prior is worth 38 imaginary trials and the data is worth 40, so the answer '
             'lands halfway and narrower than either',
        alt='Three curves on one axis. A prior peaking at twenty percent, a likelihood from the '
            'data peaking at thirty percent, and the posterior peaking between them at twenty-five '
            'percent and taller and narrower than both, because it is built from the two of them '
            'together.'),
    caption=('Two inputs of roughly equal weight, so the posterior lands midway and is narrower '
             'than either. Halve the data and the peak slides left towards the prior; multiply it '
             'by ten and the prior curve stops mattering entirely. The interview question is which '
             'of those three pictures you are actually in.'),
    caption_simple=('Two inputs of roughly equal weight, so the answer lands midway and is '
                    'narrower than either one alone. With ten times the data the starting point '
                    'would barely shift the peak. Knowing which of those situations you are in is '
                    'the whole skill.'),
    when=[
        'You are launching in a market with 40 sessions of data and a PM wants a conversion number',
        'An eval set has fewer than 100 paired comparisons and the bootstrap is wobbling',
        'A segment shows a 60% conversion rate on nine users and someone wants to act on it',
        'Someone reports a range and says there is a 95% chance the value is inside it',
    ],
    trap=('Presenting a Bayesian result as assumption-free. The sentence is &ldquo;we used a flat '
          'prior, so this is just what the data says&rdquo;, and both halves are wrong. '
          '$\\text{Beta}(1,1)$ is uniform on the rate and therefore not uniform on the odds, so '
          'it is a specific opinion about the odds scale wearing a neutral costume; and 0 '
          'conversions in 3 sessions comes back as a posterior mean of 20%, which is a strong '
          'claim that no data supports. Say instead: &ldquo;here is my prior, here is what it is '
          'worth in observations, and here is the answer under three different ones.&rdquo;'),
    math=dict(
        tex=r'p(\theta \mid y) \;\propto\; \underbrace{p(y \mid \theta)}_{\text{likelihood}}\;\underbrace{p(\theta)}_{\text{the argument}} \qquad \text{Beta}(\alpha,\beta) + (s, f) \;\to\; \text{Beta}(\alpha + s,\ \beta + f)',
        note='The update is addition, which is why conjugacy feels like magic and why it is only '
             'convenience. The prior enters as counts you made up, so quote it in counts and let '
             'someone argue with the number.',
        cost='one prior you have to say out loud'),
    code=dict(
        label='The same data under three priors',
        cost='scipy',
        src=('<span class="k">from</span> scipy.stats <span class="k">import</span> beta\n\n'
             's, f = <span class="s">12</span>, <span class="s">28</span>'
             '            <span class="c"># 12 conversions in 40 sessions</span>\n'
             '<span class="k">for</span> a, b <span class="k">in</span> '
             '[(<span class="s">1</span>, <span class="s">1</span>), '
             '(<span class="s">8</span>, <span class="s">32</span>), '
             '(<span class="s">40</span>, <span class="s">160</span>)]:\n'
             '    post = beta(a + s, b + f)\n'
             '    <span class="k">print</span>(a, b, '
             '<span class="k">round</span>(post.mean(), <span class="s">3</span>), '
             'post.interval(<span class="s">0.95</span>))\n\n'
             '<span class="c"># 1   1    0.310   [0.181, 0.455]   &lt;- the "uninformative" one</span>\n'
             '<span class="c"># 8   32   0.250   [0.162, 0.350]</span>\n'
             '<span class="c"># 40  160  0.217   [0.167, 0.271]</span>\n'
             '<span class="c"># same 12 of 40. the answer moves 9 points of conversion on the prior alone</span>')),
    real=('statsforevals.com recommends Bayesian paired methods for pairwise binary comparisons '
          'below about 100 items and the bootstrap above that &mdash; a defensible boundary for '
          'where Bayes earns its keep in LLM eval work. The sharper case is Bing&rsquo;s own '
          'prior: perhaps 1 in 500 experiments clears a high-ROI bar, and at 80% power and 5% '
          'alpha that prior drags the chance a significant win is real down to 3.1%. Move the '
          'prior to 1 idea in 3 being real and the identical result is 89% likely to be true. '
          'Same data, same p-value, two different worlds.'),
    drills=[
        dict(q='You are launching in a new city with almost no data. Construct a prior.',
             a=('<b>Pool across the cities you already have, then let the data pull.</b> Fit a '
                'hierarchical model: the new city&rsquo;s prior is centred on the population mean '
                'across existing cities, with a variance set by the observed between-city '
                'variance &mdash; so cities that historically differ a lot give you a wide prior '
                'and cities that cluster give you a tight one. That is a prior you can defend '
                'with a table rather than a hunch. Then finish the answer properly: show how far '
                'the posterior moves under a flat prior versus yours, and name the decision that '
                'would have to flip before the choice of prior mattered.'),
             a_simple=('<b>Borrow from the cities you already run in.</b> Start the new city at '
                       'the average of the existing ones, and set how confident you are by how '
                       'much those cities differ from each other. If they are all alike you start '
                       'confident; if they are all over the place you start loose. Then do the '
                       'honest second half: show what the answer would have been from a blank '
                       'start, and say whether the decision changes. Usually it does not, and '
                       'saying so ends the argument.')),
        dict(q='A colleague says a flat prior means "no prior, so the result is objective". Is that right?',
             a=('<b>No &mdash; flat is a choice, and you can catch it doing work.</b> '
                '$\\text{Beta}(1,1)$ is uniform on the rate, which makes it non-uniform on the '
                'odds, so &ldquo;uniform&rdquo; only means something once you say which '
                'parameterisation you were uniform over. The arithmetic makes it concrete: 0 '
                'successes in 3 trials returns a posterior mean of $1/5$, and 1 in 3 returns '
                '$2/5$ rather than the observed $1/3$. A prior that says nothing does not shift '
                'your estimate by 7 points. Report yours in prior successes and failures instead, '
                'so the assumption is visible and arguable.'),
             a_simple=('<b>No. Flat is an opinion, and you can watch it change the answer.</b> '
                       'Flat means every rate from zero to certainty is equally believable, which '
                       'is a strong claim, not the absence of one. Watch it work: with zero '
                       'conversions in three sessions, the flat start hands you twenty percent, '
                       'and with one in three it hands you forty rather than the thirty-three you '
                       'actually saw. State your starting point as a count of imaginary trials '
                       'instead. Then everyone can see it and argue with it.')),
        dict(q='Your credible interval is [1.6%, 3.5%]. A colleague says that is just the confidence interval. Are they the same?',
             a=('<b>Numerically close with enough data, and a different sentence.</b> The credible '
                'interval is a statement about the parameter given the data, the model and the '
                'prior: 95% of the posterior mass sits in there. The confidence interval is a '
                'statement about the procedure &mdash; intervals built this way cover the truth '
                '95% of the time. With a lot of data and a mild prior they converge to nearly the '
                'same numbers, which is exactly why people confuse them. The difference is what '
                'you are entitled to say out loud, and only one of them licenses the sentence the '
                'PM wants.'),
             a_simple=('<b>Nearly the same numbers, and a genuinely different sentence.</b> One of '
                       'them lets you say there is a ninety-five percent chance the true value '
                       'sits in this range, as long as you add "given my model and my starting '
                       'point". The other one is a statement about the method rather than about '
                       'this particular range: build ranges this way and they contain the truth '
                       'ninety-five percent of the time. With plenty of data the two land on '
                       'almost identical numbers, which is why people swap them by accident.')),
    ],
    anchor=dict(
        formula=r'$p(\theta \mid y) \propto p(y \mid \theta)\,p(\theta)$ &nbsp;&middot;&nbsp; $\text{Beta}(\alpha,\beta)$ is $\alpha-1$ prior successes, $\beta-1$ prior failures',
        formula_simple='What you believed, weighted by how well each answer explains the data. '
                       'The more data, the less your starting point survives.',
        bullets=[
            'A credible interval is the sentence people wrongly attach to a confidence interval',
            'A prior is worth a specific number of imaginary observations &mdash; quote the number',
            'Flat is not neutral, and priors wash out with data, so the argument is loudest where the data are thinnest',
        ]),
    chips=['conjugate prior', 'credible interval', 'hierarchical shrinkage', 'prior sensitivity',
           'Beta-Binomial'],
    followup='You are launching in a new city with almost no data. Construct a prior.',
),

# ============================================================================
dict(
    id='bayesian-ab',
    tier='advanced',
    title='Bayesian A/B testing and expected loss',
    kicker='&ldquo;96% chance B beats A&rdquo; sounds like the end of the conversation, and it hides how much you lose if you are wrong',
    simple=[
        'A Bayesian test gives you a whole distribution of plausible lifts, and the dashboard '
        'squeezes it into one headline: the chance that B is better than A. That number is real, '
        'but it is the wrong one to decide on. It tells you how often you would be wrong and says '
        'nothing at all about how badly.',
        'The number that decides is the one nobody puts on the dashboard: if you ship B and you '
        'turn out to be wrong, how much do you expect to give up? Add up every scenario where B '
        'is worse, weighted by how much worse it is. That is your expected loss. Ship when it '
        'falls below a threshold you wrote down before the test started &mdash; a level of harm '
        'you have decided you can live with. Two tests can carry the identical headline and land '
        'on opposite sides of that line, because one of them has a long ugly tail and the other '
        'does not.',
    ],
    analogy=('<b>Like taking a bet you are ninety-six percent sure of.</b> Being told you will '
             'probably win tells you nothing about the stake. Ninety-six percent on the price of a '
             'coffee is a fine bet; the same ninety-six percent on your house is not. What '
             'separates them is what happens in the four percent of worlds where you were wrong '
             '&mdash; and that is the number the dashboard never shows you.'),
    trap_simple=('Saying &ldquo;it is Bayesian, so we can look whenever we like&rdquo;. The first '
                 'half is true: the running answer is honest after every single visitor. The '
                 'second half is not. If your rule is to stop the moment the headline crosses '
                 'ninety-five percent, then you have built a rule that goes looking for a good '
                 'moment, and it finds one far more often than it should.'),
    tech=[
        'Bayesian A/B gives you $P(\\theta_B > \\theta_A)$ and the full posterior of the lift. The '
        'posterior is valid at any sample size &mdash; no fixed horizon, no peeking correction for '
        'the posterior itself. But $P(\\theta_B > \\theta_A) = 0.96$ on a lift of $+0.01\\%$ is a '
        'terrible reason to ship, because that probability is just the area of the posterior above '
        'zero and area is blind to distance.',
        'The decision quantity is expected loss, $E[\\max(0,\\ \\theta_A - \\theta_B)]$: the same '
        'region, weighted by how far short you fell. Ship when it drops below a pre-set threshold '
        'of caring &mdash; a common default is 0.1% of the metric. Two posteriors with the same '
        '96% headline can differ by 3x on expected loss, and the wide one is almost always the '
        'test somebody stopped early.',
        'Which is the honest answer to &ldquo;so Bayesian means we can peek freely&rdquo;: no. '
        'Bayes removes the multiple-testing <i>interpretation</i> problem, not the operating '
        'characteristics of your stopping rule. Stop as soon as $P(\\theta_B > \\theta_A) > 0.95$ '
        'under a flat prior and your long-run error behaviour lands close to frequentist peeking. '
        'The posterior is coherent; the procedure wrapped around it still has a false positive '
        'rate, and the only way to know it is to simulate the rule.',
    ],
    tech_note=('The industry is genuinely split, so know both sides: VWO and GrowthBook ship '
               'Bayesian engines with expected loss as the documented default, while Optimizely, '
               'Statsig, Eppo and Spotify are frequentist-sequential. When the Bayesian engine '
               'says 96% and the frequentist p-value on the same data says 0.09, nobody is '
               'broken &mdash; they are answering different questions under different priors. '
               'Show the interval and the expected loss; do not adjudicate between two headline '
               'numbers.'),
    fig=dict(
        kind='plot',
        head=['SAME 96% HEADLINE', 'DIFFERENT DECISION'],
        xr=(-1.0, 2.4), yr=(0, 3.2), ph=200,
        xlab='lift in conversion, percentage points',
        ylab='posterior density',
        xticks=[(-1.0, '-1.0'), (-0.5, '-0.5'), (0, '0'), (0.5, '+0.5'), (1.0, '+1.0'),
                (1.5, '+1.5'), (2.0, '+2.0')],
        vlines=[dict(x=0.0, tone='plain', label='B and A are equal')],
        bands=[dict(x0=-1.0, x1=0.0, tone='sig', op=0.13, label='B loses in here')],
        curves=[
            dict(tone='mem', fill=True, lat=14, la='middle', dx=0, dy=-11,
                 label='n = 50k/arm   loss 0.0022pp',
                 pts=[(-0.32, 0.00), (-0.28, 0.00), (-0.24, 0.01), (-0.20, 0.02), (-0.16, 0.04),
                      (-0.12, 0.09), (-0.08, 0.19), (-0.04, 0.36), (0.00, 0.63), (0.04, 1.00),
                      (0.08, 1.47), (0.12, 1.98), (0.16, 2.45), (0.20, 2.79), (0.24, 2.91),
                      (0.28, 2.79), (0.32, 2.45), (0.36, 1.98), (0.40, 1.47), (0.44, 1.01),
                      (0.48, 0.63), (0.52, 0.36), (0.56, 0.19), (0.60, 0.09), (0.64, 0.04),
                      (0.68, 0.02), (0.72, 0.01), (0.76, 0.00), (0.80, 0.00)]),
            dict(tone='sig', lat=13, la='middle', dx=0, dy=-11,
                 label='stopped at 5k/arm   loss 0.0071pp',
                 pts=[(-0.85, 0.00), (-0.72, 0.00), (-0.59, 0.01), (-0.46, 0.02), (-0.33, 0.04),
                      (-0.20, 0.08), (-0.07, 0.14), (0.06, 0.24), (0.19, 0.37), (0.32, 0.53),
                      (0.45, 0.68), (0.58, 0.81), (0.71, 0.89), (0.84, 0.89), (0.97, 0.82),
                      (1.10, 0.69), (1.23, 0.54), (1.36, 0.38), (1.49, 0.25), (1.62, 0.15),
                      (1.75, 0.08), (1.88, 0.04), (2.01, 0.02), (2.14, 0.01), (2.27, 0.00),
                      (2.40, 0.00)]),
        ],
        foot='the threshold of caring is 0.1% of the metric, or 0.0048pp here. only the narrow '
             'one clears it',
        alt='Two posterior distributions for the lift of B over A. Both put 96 percent of their '
            'mass above zero, but the wide one from the test that was stopped early spills much '
            'further into the region where B loses, giving it three times the expected loss on an '
            'identical headline number.'),
    caption=('Both posteriors put 96% of their mass to the right of zero. The headline cannot tell '
             'them apart because it only counts area; expected loss weights that area by depth, '
             'and the early-stopped test is 3x worse on it. This is why the decision rule is the '
             'loss, not the probability.'),
    caption_simple=('Both curves have the same amount of themselves on the winning side of zero, '
                    'so both report the same headline. The wide one reaches much further into the '
                    'losing region, which is what costs you when you are wrong. That difference is '
                    'the whole reason for the second number.'),
    when=[
        'The dashboard reads "96% chance to beat control" and someone treats it as a launch signal',
        'A PM wants "the probability this is better" and will not accept a range',
        'You are choosing a stopping rule for a Bayesian test and nobody has written one down',
        'The Bayesian engine says 96% and the frequentist p-value on the same data is 0.09',
    ],
    trap=('Claiming Bayesian A/B &ldquo;solves peeking&rdquo;. The exact sentence is &ldquo;it is '
          'Bayesian, so the numbers are valid whenever we look&rdquo; &mdash; and the first half '
          'is genuinely true, which is what makes the trap effective. The posterior is coherent '
          'after every observation. What is not exempt is the rule you wrapped around it: stop as '
          'soon as the headline clears 95% and the distribution of decisions that rule produces '
          'inflates just like frequentist peeking. The second trap is quieter: shipping on '
          '$P(\\theta_B > \\theta_A)$ alone, so a 96% chance of a $+0.01\\%$ lift reads as a win.'),
    math=dict(
        tex=r'\text{ship if}\quad E\bigl[\max(0,\ \theta_A - \theta_B)\bigr] < \tau \qquad \text{not}\qquad P(\theta_B > \theta_A) > 0.95',
        note='The right-hand side is an area. The left-hand side is that same area weighted by how '
             'far short you fell, which is why the two rank experiments differently. The only '
             'part that is not arithmetic is $\\tau$, and it has to be set before you look.',
        cost='one threshold of caring, pre-registered'),
    code=dict(
        label='Both numbers from the same posterior draws',
        cost='numpy, scipy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             '<span class="k">from</span> scipy.stats <span class="k">import</span> beta\n\n'
             'rng = np.random.default_rng(<span class="s">11</span>)\n'
             'a = beta(<span class="s">1</span>+<span class="s">2412</span>, '
             '<span class="s">1</span>+<span class="s">47588</span>).rvs('
             '<span class="s">500_000</span>, random_state=rng)   '
             '<span class="c"># control 2412/50000</span>\n'
             'b = beta(<span class="s">1</span>+<span class="s">2532</span>, '
             '<span class="s">1</span>+<span class="s">47468</span>).rvs('
             '<span class="s">500_000</span>, random_state=rng)   '
             '<span class="c"># variant 2532/50000</span>\n\n'
             '<span class="k">print</span>((b &gt; a).mean())                 '
             '<span class="c"># ~0.960 -- the dashboard number</span>\n'
             '<span class="k">print</span>(np.maximum(<span class="s">0</span>, a - b).mean())    '
             '<span class="c"># ~2.2e-05 -- the decision number</span>\n\n'
             '<span class="c"># stop the same experiment at 5k/arm (241 vs 280) and the headline is</span>\n'
             '<span class="c"># still ~0.960, but expected loss is ~7.1e-05 -- over the 4.8e-05</span>\n'
             '<span class="c"># threshold. identical headline, opposite decision.</span>')),
    real=('GrowthBook and VWO ship Bayesian engines with expected loss as the documented default '
          'decision rule; Optimizely, Statsig, Eppo and Spotify are frequentist-sequential. The '
          'number that keeps the argument honest belongs to Optimizely: their own platform ran at '
          'a false positive rate of over 20%, brought under 5% only after they shipped mSPRT '
          '(Johari, Koomen, Pekelis &amp; Walsh, KDD 2017). That 20% came from a stopping rule, '
          'not from a p-value &mdash; which is exactly why a Bayesian engine wired to '
          '&ldquo;stop at 95%&rdquo; inherits it.'),
    drills=[
        dict(q='Your Bayesian engine says 96% chance B wins. The frequentist p-value is 0.09. Which do you believe, and what do you tell the PM?',
             a=('<b>Both, because they answer different questions &mdash; and then you stop '
                'quoting either one.</b> The 96% is posterior mass above zero under your prior; '
                'the 0.09 is tail probability under the null. Nothing is broken, and with a flat '
                'prior on a two-sided test those two are roughly the same statement wearing '
                'different clothes. What you tell the PM is the interval and the expected loss: '
                'does the credible interval exclude the MDE you pre-registered, and is the '
                'expected loss under the threshold? If the interval runs from below the MDE to '
                'well above it, the honest answer is that the test has not finished.'),
             a_simple=('<b>Believe both, then stop arguing about which headline is right.</b> They '
                       'answer different questions, and on this data they are close to the same '
                       'statement said two ways. What the PM needs is neither: give the range of '
                       'plausible lifts, and how much you expect to lose if you ship and you are '
                       'wrong. If the range still includes lifts too small to be worth having, '
                       'the test is not finished, and no headline number changes that.')),
        dict(q='So Bayesian testing means we can peek freely?',
             a=('<b>No &mdash; the posterior is exempt, your stopping rule is not.</b> The '
                'posterior is a valid summary of the evidence after every single observation, '
                'which is the true part of the claim. But &ldquo;stop as soon as '
                '$P(\\theta_B > \\theta_A) > 0.95$&rdquo; is a decision procedure, and procedures '
                'have operating characteristics. Under a flat prior that rule behaves close to '
                'frequentist peeking, because it keeps sampling until noise happens to be '
                'favourable and then halts. Fix it the same way either camp does: simulate the '
                'rule under the null, see the actual false positive rate, and add a minimum '
                'runtime or an alpha-spending style boundary.'),
             a_simple=('<b>No. The running answer is fine; the rule for when to stop is not.</b> '
                       'You can look at a Bayesian result whenever you want and it will be an '
                       'honest summary of what you have seen so far. The problem is a rule that '
                       'stops the moment the number looks good, because that rule waits for a '
                       'lucky stretch and then calls it. Test the rule itself: run it on data '
                       'where you know there is no difference and count how often it declares a '
                       'winner.')),
        dict(q='Expected loss is 0.0004pp, well under the threshold, and the lift is +0.01%. Ship?',
             a=('<b>No &mdash; a low expected loss says B is safe, not that B is worth it.</b> '
                'Expected loss is a floor test: it tells you the downside is small. On a '
                '$+0.01\\%$ lift the upside is equally small, and you are about to buy permanent '
                'code, a permanent config branch and a permanent maintenance cost for an effect '
                'nobody will ever detect again. The second half of the rule is the pre-registered '
                'MDE: check whether the credible interval sits mostly above it. Here it will not, '
                'so the decision is do not ship, and say why in one line &mdash; the effect is '
                'probably real and definitely not worth owning.'),
             a_simple=('<b>No. A small expected loss means it is safe, not that it is worth '
                       'doing.</b> That number only tells you the downside is tiny. So is the '
                       'upside. You would be taking on code you have to keep working forever in '
                       'exchange for a gain nobody will ever measure again. The other half of the '
                       'decision is the smallest lift you agreed in advance was worth having, and '
                       'this one is nowhere near it. Say that out loud rather than shipping '
                       'because the safety check passed.')),
    ],
    anchor=dict(
        formula=r'$E\bigl[\max(0,\ \theta_A - \theta_B)\bigr] < \tau$ &nbsp;&middot;&nbsp; not &nbsp;&middot;&nbsp; $P(\theta_B > \theta_A) > 0.95$',
        formula_simple='How much you expect to give up if you are wrong, not how likely you are to '
                       'be wrong.',
        bullets=[
            'The headline is an area; the expected loss is that area weighted by how far short you fell',
            'Set the threshold of caring before you look &mdash; it is the only part that is not arithmetic',
            'Bayes fixes the interpretation of peeking, never the operating characteristics of your stopping rule',
        ]),
    chips=['expected loss', 'credible interval', 'stopping rules', 'sequential testing', 'MDE'],
    followup='Your Bayesian engine says 96% chance B wins and the frequentist p-value is 0.09. Which do you believe, and what do you tell the PM?',
),

# ============================================================================
dict(
    id='confounding-dags',
    tier='advanced',
    title='Confounding, DAGs and the backdoor criterion',
    kicker='&ldquo;I threw everything into the regression&rdquo; is the most common way to make a causal estimate worse',
    simple=[
        'A third variable can sit in three different places, and where it sits decides whether '
        'you control for it or leave it alone. If it causes both the treatment and the outcome, '
        'it is faking the relationship and you must adjust for it. If the treatment causes it and '
        'it then causes the outcome, it is a step on the road you were trying to measure &mdash; '
        'adjust for it and you delete the very effect you came for. And if the treatment and the '
        'outcome both cause it, adjusting for it invents a relationship that was never there.',
        'So &ldquo;control for everything you have&rdquo; is not a cautious default. It is a '
        'coin flip that makes the answer better a third of the time. The rule that gets you most '
        'of the way home is boring and reliable: only adjust for things that were already true '
        'before the treatment happened. Anything measured afterwards is downstream of the thing '
        'you are studying, and putting it in the model does damage you cannot see in any summary '
        'statistic.',
    ],
    analogy=('<b>Like the films that actually get made.</b> A studio green-lights a script if it '
             'is either brilliant or cheap. So among the films that got made, budget and script '
             'quality look strongly negatively related &mdash; not because money ruins writing, '
             'but because you are only ever looking at the ones that cleared the bar. Filter on '
             'something two independent causes both feed into, and you manufacture a relationship '
             'out of nothing.'),
    trap_simple=('Saying &ldquo;we controlled for everything we had, so the estimate is '
                 'clean&rdquo;. Adding a variable that happened after the treatment, or one that '
                 'the treatment and the outcome both cause, makes the answer worse rather than '
                 'better &mdash; and in the second case it can flip the sign. The other version '
                 'is quieter: adding a control because it made the model fit better. That is a '
                 'prediction test being used to settle a cause question.'),
    tech=[
        'Draw the graph before you fit anything. A <b>confounder</b> is a common cause of '
        'treatment and outcome: you must adjust, or the backdoor path stays open. A '
        '<b>mediator</b> sits on the path $X \\to M \\to Y$: adjusting removes exactly the effect '
        'you wanted, leaving a direct effect conditional on a post-treatment variable. A '
        '<b>collider</b> is a common effect of two variables: adjusting <i>creates</i> an '
        'association that does not exist. That last one is Berkson&rsquo;s paradox, and in a '
        'sample selected on &ldquo;admitted&rdquo;, &ldquo;hospitalised&rdquo; or '
        '&ldquo;clicked&rdquo;, two independent causes come out negatively correlated.',
        'The backdoor criterion names the minimal sufficient adjustment set: a set $Z$ that blocks '
        'every backdoor path from $X$ to $Y$ and contains no descendant of $X$. Note the second '
        'clause &mdash; it is the one that fails in practice, and it is what makes '
        '&ldquo;bad controls&rdquo; a named failure rather than a rounding error. Conditioning on '
        'a post-treatment variable can bias an estimate and sometimes reverse its sign.',
        'This is a graph question, not a p-value question, and no amount of model fit will tell '
        'you the answer. Say &ldquo;pre-treatment covariates only&rdquo; and you have dodged 80% '
        'of the trap in one sentence. The remaining 20% is remembering that <i>who is in your '
        'sample</i> is adjustment too: analysing only users who clicked, only hosts who listed, '
        'only patients who were admitted is a collider adjustment you never wrote into the '
        'regression.',
    ],
    tech_note=('Two tells that a causal analysis has gone predictive. First, a variable earned its '
               'place because it raised $R^2$ &mdash; a collider will often raise $R^2$ while '
               'destroying the estimate, so fit is evidence of nothing here. Second, nobody can '
               'say what the treatment is supposed to do to each control. If you cannot draw the '
               'arrow, you cannot justify the adjustment, and the honest move is to draw the '
               'graph on a whiteboard and let people disagree with the arrows instead of the '
               'coefficients.'),
    fig=dict(
        kind='blocks',
        h=252,
        head=['THE ONE YOU CUT', 'THE TWO YOU DO NOT'],
        boxes=[
            dict(x=86, y=54, w=100, h=36, t='host tenure', tone='mem'),
            dict(x=34, y=142, w=96, h=36, t='Instant Book'),
            dict(x=154, y=142, w=84, h=36, t='bookings'),
            dict(x=310, y=54, w=100, h=36, t='enquiries', tone='sig'),
            dict(x=258, y=142, w=96, h=36, t='Instant Book'),
            dict(x=378, y=142, w=84, h=36, t='bookings'),
            dict(x=482, y=54, w=96, h=36, t='Instant Book'),
            dict(x=602, y=54, w=84, h=36, t='bookings'),
            dict(x=534, y=142, w=100, h=36, t='ranked top', tone='sig'),
        ],
        links=[
            dict(a=0, b=1, side='down', tone='mem', label='cut this'),
            dict(a=0, b=2, side='down', tone='mem'),
            dict(a=1, b=2),
            dict(a=4, b=3, side='up', tone='sig'),
            dict(a=3, b=5, side='down', tone='sig'),
            dict(a=4, b=5),
            dict(a=6, b=8, side='down', tone='sig'),
            dict(a=7, b=8, side='down', tone='sig'),
        ],
        labels=[
            dict(x=136, y=26, t='1  confounder', tone='mem'),
            dict(x=360, y=26, t='2  mediator', tone='sig'),
            dict(x=584, y=26, t='3  collider', tone='sig'),
            dict(x=136, y=206, t='adjust for it', tone='mem'),
            dict(x=360, y=206, t='adjust and it vanishes', tone='sig'),
            dict(x=584, y=206, t='adjust and you invent it', tone='sig'),
        ],
        foot='the only arrow you may cut is the one pointing into the treatment. the other two '
             'look like diligence and are damage',
        alt='Three small causal graphs. In the first, host tenure causes both Instant Book and '
            'bookings, and the arrow from tenure into Instant Book is marked as the one you cut '
            'by adjusting. In the second, Instant Book causes enquiries which cause bookings, so '
            'adjusting for enquiries deletes the effect. In the third, Instant Book and bookings '
            'both cause a listing being ranked top, so adjusting for ranking invents an '
            'association.'),
    caption=('Same three boxes, three different arrangements, three different verdicts. Adjusting '
             'for the first is the only move that removes bias; the other two add it. Nothing in '
             'the data distinguishes these graphs for you &mdash; you have to know which arrow '
             'points where before you fit.'),
    caption_simple=('The same three boxes arranged three ways, with three opposite answers. Only '
                    'in the first picture does controlling for the extra box help. In the other '
                    'two it hurts, and the numbers coming out of the model look equally '
                    'convincing either way.'),
    when=[
        'Someone says "we controlled for it in the regression, so the relationship is causal"',
        'You are estimating the effect of Instant Book and a reviewer asks you to control for enquiries',
        'The analysis is restricted to users who clicked, hosts who listed, or patients who were admitted',
        'A variable earned its place in the model because it improved R-squared',
    ],
    trap=('&ldquo;More controls means less bias.&rdquo; Two specific versions cost the loop. The '
          'first is adding a control because it improved $R^2$, which applies a predictive '
          'criterion to a causal question &mdash; a collider often raises $R^2$ on the way to '
          'wrecking your estimate. The second is Airbnb&rsquo;s own question: controlling for '
          'number of enquiries while estimating the effect of Instant Book on bookings. Enquiries '
          'are downstream of the treatment. You have not removed bias; you have estimated a direct '
          'effect conditional on a post-treatment variable and induced collider bias while you '
          'were at it.'),
    math=dict(
        tex=r'P\bigl(Y \mid do(X)\bigr) \;=\; \sum_{z} P\bigl(Y \mid X,\, Z=z\bigr)\,P(Z=z)',
        note='Valid only when $Z$ blocks every backdoor path from $X$ to $Y$ <i>and</i> contains '
             'no descendant of $X$. The second condition is the one that fails, and it is the '
             'entire content of "bad controls".',
        cost='a graph you are willing to defend'),
    code=dict(
        label='Manufacturing a correlation out of nothing',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n'
             'n = <span class="s">200_000</span>\n'
             'x = rng.normal(size=n)                     '
             '<span class="c"># headline quality</span>\n'
             'y = rng.normal(size=n)                     '
             '<span class="c"># topic interest -- independent of x</span>\n'
             'c = x + y + rng.normal(size=n)             '
             '<span class="c"># "ranked top": a COMMON EFFECT of both</span>\n\n'
             '<span class="k">print</span>(np.corrcoef(x, y)[<span class="s">0</span>, '
             '<span class="s">1</span>])           '
             '<span class="c"># -0.003 -- they really are independent</span>\n'
             'sel = c &gt; <span class="s">1.5</span>                              '
             '<span class="c"># "we only looked at listings that ranked"</span>\n'
             '<span class="k">print</span>(np.corrcoef(x[sel], y[sel])[<span class="s">0</span>, '
             '<span class="s">1</span>]) '
             '<span class="c"># -0.35 -- you manufactured this</span>')),
    real=('Obermeyer et al., <i>Science</i> 366:447 (October 2019). A commercial risk-prediction '
          'algorithm applied to roughly 200 million people a year in the US used healthcare '
          '<i>cost</i> as the label for health <i>need</i>. Less had historically been spent on '
          'Black patients at the same level of illness, so the label carried the access path '
          'rather than the illness path and Black patients had to be considerably sicker to earn '
          'the same score. Fixing the label raised the share of Black patients flagged for extra '
          'care from 17.7% to 46.5%. No modelling change was required.'),
    drills=[
        dict(q='You are estimating the effect of Instant Book on host bookings and you control for number of enquiries. Is that OK?',
             a=('<b>No &mdash; enquiries are downstream of the treatment.</b> Instant Book changes '
                'how many enquiries a listing gets, and enquiries change bookings, so enquiries '
                'are a mediator. Adjusting for them removes the part of the effect that runs '
                'through enquiries, which is most of the effect you were asked about, and leaves '
                'you reporting a direct effect conditional on a post-treatment variable &mdash; '
                'plus collider bias if anything unobserved drives both enquiries and bookings. '
                'Drop it. Keep pre-treatment covariates only. If somebody genuinely wants the '
                'direct effect, that is a mediation analysis and a different question.'),
             a_simple=('<b>No &mdash; enquiries happen after the treatment.</b> Instant Book '
                       'changes how many enquiries a listing gets, and those enquiries are how it '
                       'turns into bookings. Holding enquiries fixed removes most of the effect '
                       'you were sent to measure, and quietly adds a new distortion on top. Drop '
                       'it and keep only things that were already true before the change went '
                       'live. If someone actually wants the leftover path, say so &mdash; that is '
                       'a different study.')),
        dict(q='Your analysis only uses users who clicked the recommendation. What have you already conditioned on, before writing any code?',
             a=('<b>A collider, and it never appears in the model.</b> Clicking is a common effect '
                'of the recommendation and of the user&rsquo;s underlying interest, so filtering '
                'on it opens a path between those two and makes them negatively associated inside '
                'your sample. This is Berkson&rsquo;s paradox arriving as a WHERE clause. Sample '
                'selection is adjustment, and it is the version nobody reviews because there is no '
                'coefficient attached to it. Fix it by defining the population at randomisation, '
                'not at the point of engagement, and if you cannot, say which direction the bias '
                'runs.'),
             a_simple=('<b>On something both the treatment and the outcome cause, which is the '
                       'worst possible choice.</b> A click happens because the recommendation was '
                       'good and because the person was already interested. Keeping only the '
                       'clickers means that within your sample, one of those explanations '
                       'substitutes for the other, and they come out looking opposed. The filter '
                       'in your query did as much damage as a bad control would have, and nobody '
                       'reviews the query. Define the group at the moment of randomisation '
                       'instead.')),
        dict(q='Adding the variable raised R-squared from 0.31 to 0.44. Is that a reason to keep it?',
             a=('<b>No. $R^2$ is a predictive criterion and this is a causal question.</b> A '
                'collider will frequently raise $R^2$ a great deal precisely because it soaks up '
                'variance in $Y$ that is correlated with $X$ &mdash; the fit improves as the '
                'estimate degrades, so the number you are watching moves the wrong way on purpose. '
                'The decision rule is order of operations: pick the adjustment set from the graph '
                'using the backdoor criterion, fit once, and report $R^2$ as a description of the '
                'fit rather than a defence of the specification.'),
             a_simple=('<b>No. A better fit is a prediction argument, and this is a cause '
                       'question.</b> The worst kind of control &mdash; one that the treatment and '
                       'the outcome both cause &mdash; will often improve the fit a lot, exactly '
                       'while it is ruining your estimate. So the number people quote as '
                       'reassurance moves in the wrong direction here. Choose your controls from '
                       'the picture of what causes what, before you fit anything, and treat fit as '
                       'a description afterwards.')),
    ],
    anchor=dict(
        formula=r'$P(Y \mid do(X)) = \sum_z P(Y \mid X, Z=z)P(Z=z)$ &nbsp;&middot;&nbsp; only if $Z$ blocks every backdoor and contains no descendant of $X$',
        formula_simple='Adjust for what causes both. Never for what the treatment causes, and '
                       'never for what the treatment and the outcome both cause.',
        bullets=[
            'Common cause: adjust. Step on the path: adjusting deletes the effect. Shared consequence: adjusting invents one',
            'Choosing who is in the sample is adjustment you did not write down',
            'Pre-treatment covariates only, and the adjustment set comes from the graph, never from R-squared',
        ]),
    chips=['backdoor criterion', 'collider bias', 'bad controls', 'mediation analysis',
           'Berkson&rsquo;s paradox'],
    followup='You are estimating the effect of Instant Book on host bookings and you control for number of enquiries. Is that OK?',
),

# ============================================================================
dict(
    id='regression-diagnostics',
    tier='advanced',
    title='Regression diagnostics that actually matter',
    kicker='Nobody asks you to recite Gauss&ndash;Markov; they hand you a residual plot and ask what is broken',
    simple=[
        'Five assumptions get taught and two of them break in the wild. The first is even spread: '
        'if the errors get bigger as the prediction gets bigger, your coefficients are still '
        'centred in the right place, but your error bars are wrong. The second is independence: '
        'if the same user shows up forty times, or the rows are in time order and neighbours '
        'resemble each other, your error bars are wrong again and far more badly.',
        'Notice what is not on that list. The one everybody checks &mdash; whether the leftovers '
        'are bell-shaped &mdash; almost never matters once you have a decent sample. And two '
        'features that move together do not bias anything either: they make the individual '
        'coefficients unstable and unreadable while the predictions stay perfectly fine. So the '
        'first question is never &ldquo;which assumption is violated&rdquo;. It is &ldquo;do I '
        'need to read the coefficients, or only the predictions?&rdquo; Half the famous problems '
        'evaporate the moment you answer that.',
    ],
    analogy=('<b>Like a bathroom scale that jitters more the heavier you are.</b> Every reading is '
             'still centred on your real weight, so the long-run average is right and the scale is '
             'not lying to you. What is wrong is your confidence in any single reading: you would '
             'quote a tighter range than you have earned at the top of the dial. The fix is not a '
             'new scale, it is an honest error bar.'),
    trap_simple=('Saying &ldquo;the leftovers are not bell-shaped, so the regression is '
                 'invalid&rdquo;. On a hundred thousand rows the standard normality test rejects '
                 'every single time, and it does not matter, because what you needed was the '
                 'coefficient estimates to behave, not the individual errors. Meanwhile the thing '
                 'that is genuinely breaking the answer &mdash; forty sessions from the same user '
                 'counted as forty independent facts &mdash; never gets mentioned.'),
    tech=[
        'The five: linearity, low multicollinearity, normally distributed errors, homoscedasticity, '
        'independent errors. Rank them by how often they change a decision and the last two are '
        'the only ones that pay rent.',
        '<b>Heteroscedasticity</b> does not bias $\\hat\\beta$; it biases $\\widehat{\\text{Var}}'
        '(\\hat\\beta)$. Use robust (HC3) standard errors by default and stop thinking about it '
        '&mdash; the point estimate is untouched, so there is no cost. <b>Non-independent '
        'errors</b> are the expensive one: repeated measures, clusters, time order. Cluster at the '
        'level the data were generated at, which is usually the randomisation unit, and expect '
        'the standard error to move by a factor, not a percentage. <b>Multicollinearity</b> '
        'inflates $\\text{Var}(\\hat\\beta)$ without biasing it: individual coefficients go '
        'unstable and uninterpretable, joint predictions stay fine, and $\\text{VIF} > 5$ to $10$ '
        'is the usual flag. <b>Normality of errors</b> matters only for small-sample inference; '
        'with $n$ large the CLT covers the coefficient estimates.',
        'The diagnostics that actually catch bugs are three plots, not a battery of tests: '
        'residuals against fitted values, residuals against each feature, and residuals against '
        'time. Structure in any of them is a modelling bug. A failed normality test on 100k rows '
        'is a fact about your sample size.',
    ],
    tech_note=('The failure that costs real money is repeated measures being counted as '
               'independent. One row per session with 40 sessions per user is not $n = 40{,}000$; '
               'it is 1,000 users with structure, and the naive standard error can be too small by '
               'a large factor rather than a few percent. It shows up as a model that is '
               'significant on everything, which reads like a great model right up until nothing '
               'replicates.'),
    fig=dict(
        kind='panels',
        head=['WHAT BREAKS THE ANSWER', 'WHAT DOES NOT'],
        panels=[
            dict(t='spread grows with the fit', sub='use robust HC3 errors', tone='sig',
                 fig=dict(kind='scatter', xr=(0, 10), yr=(-4, 4), ph=400,
                          curves=[dict(pts=[(0, 0), (10, 0)], tone='mute', sw=4, dash='16 12')],
                          groups=[dict(tone='sig', r=11, pts=[
                              (0.40, -0.00), (0.64, 0.30), (0.87, 0.26), (1.11, 0.30), (1.34, 0.79),
                              (1.58, -0.67), (1.82, -0.39), (2.05, -0.92), (2.29, -0.08),
                              (2.52, 0.83), (2.76, -0.02), (2.99, 0.48), (3.23, -1.98),
                              (3.47, 0.16), (3.70, -1.06), (3.94, 2.21), (4.17, 1.16),
                              (4.41, 1.31), (4.65, -0.08), (4.88, 0.93), (5.12, 1.04),
                              (5.35, -0.57), (5.59, -0.86), (5.83, -0.21), (6.06, -1.12),
                              (6.30, -1.14), (6.53, -0.57), (6.77, -1.50), (7.01, 1.63),
                              (7.24, -3.51), (7.48, 1.87), (7.71, -1.46), (7.95, -1.31),
                              (8.18, -3.34), (8.42, -0.37), (8.66, -0.65), (8.89, 0.51),
                              (9.13, -1.47), (9.36, 0.26), (9.60, 3.85)])])),
            dict(t='runs along the time axis', sub='cluster on the unit', tone='sig',
                 fig=dict(kind='scatter', xr=(0, 10), yr=(-4, 4), ph=400,
                          curves=[dict(pts=[(0, 0), (10, 0)], tone='mute', sw=4, dash='16 12')],
                          groups=[dict(tone='sig', r=11, pts=[
                              (0.40, 0.26), (0.64, -0.13), (0.87, 0.48), (1.11, 0.35), (1.34, 0.69),
                              (1.58, 1.00), (1.82, 0.66), (2.05, -0.61), (2.29, -0.77),
                              (2.52, -0.35), (2.76, -0.55), (2.99, -0.22), (3.23, 0.41),
                              (3.47, 0.03), (3.70, 0.80), (3.94, 1.73), (4.17, 2.23), (4.41, 2.73),
                              (4.65, 3.14), (4.88, 3.60), (5.12, 3.60), (5.35, 3.54), (5.59, 3.56),
                              (5.83, 2.64), (6.06, 1.40), (6.30, 0.71), (6.53, 0.87), (6.77, 1.08),
                              (7.01, 0.02), (7.24, -1.16), (7.48, -1.24), (7.71, -1.24),
                              (7.95, -1.14), (8.18, -0.61), (8.42, 0.22), (8.66, 0.34),
                              (8.89, 0.69), (9.13, -0.06), (9.36, -0.79), (9.60, -0.56)])])),
            dict(t='lopsided but even', sub='nothing to fix here', tone='mem',
                 fig=dict(kind='scatter', xr=(0, 10), yr=(-4, 4), ph=400,
                          curves=[dict(pts=[(0, 0), (10, 0)], tone='mute', sw=4, dash='16 12')],
                          groups=[dict(tone='mem', r=11, pts=[
                              (0.40, -1.01), (0.64, -0.98), (0.87, -0.87), (1.11, 1.42),
                              (1.34, -0.99), (1.58, 1.47), (1.82, 2.45), (2.05, 0.67),
                              (2.29, -1.22), (2.52, 2.20), (2.76, -1.17), (2.99, 0.33),
                              (3.23, -0.49), (3.47, -0.02), (3.70, -1.03), (3.94, -1.09),
                              (4.17, 0.44), (4.41, 0.07), (4.65, 0.51), (4.88, -0.18),
                              (5.12, -1.13), (5.35, -0.97), (5.59, -0.83), (5.83, -0.78),
                              (6.06, -1.30), (6.30, -1.12), (6.53, 3.60), (6.77, -0.49),
                              (7.01, -1.17), (7.24, -0.11), (7.48, 0.19), (7.71, 1.24),
                              (7.95, -0.79), (8.18, -0.60), (8.42, 1.32), (8.66, -1.19),
                              (8.89, 1.29), (9.13, -0.04), (9.36, -1.14), (9.60, 0.07)])])),
        ],
        foot='the third one is the plot people escalate and the first two are the plots that '
             'change the answer',
        alt='Three residual plots. The first shows residuals fanning out as the fitted value '
            'grows. The second shows residuals drifting in long runs above and then below zero '
            'along the time axis. The third shows residuals with a hard floor and occasional '
            'large positive values, but no pattern and constant spread, which is the harmless '
            'case.'),
    caption=('Left and middle change the answer: the first needs HC3 robust standard errors, the '
             'second needs clustering on the unit that generated the rows. The right-hand panel is '
             'skewed and perfectly fine &mdash; it is the one that gets escalated, and the one '
             'where a normality test will confirm your fears while nothing is wrong.'),
    caption_simple=('The first two pictures change what you should do: uneven spread needs error '
                    'bars that do not assume even spread, and long runs above and below the line '
                    'mean the rows are not independent. The third is lopsided and completely '
                    'harmless, and it is the one people escalate.'),
    when=[
        'Someone says the regression is invalid because the residuals failed a normality test',
        'Two features correlate at 0.95 and their coefficients come out with opposite signs',
        'One row per session, forty sessions per user, and every standard error looks implausibly tight',
        'A stakeholder is about to read a single coefficient as "the effect of this feature"',
    ],
    trap=('&ldquo;The residuals are not normal, so my regression is invalid.&rdquo; Usually '
          'irrelevant: with $n$ large the CLT covers the coefficient estimates, and Shapiro&ndash;'
          'Wilk on 100,000 rows rejects normality every single time regardless of the truth. '
          'Meanwhile the assumption that is actually breaking the answer &mdash; forty sessions '
          'per user, so the errors are nowhere near independent &mdash; goes unmentioned, and it '
          'is the one that turns a null effect into a $t$ of 11. The tell of a good candidate is '
          'ranking the violations by consequence instead of listing all five.'),
    math=dict(
        tex=r'\widehat{\text{Var}}(\hat\beta)_{\text{HC3}} = (X^{\top}X)^{-1}\Bigl(\sum_i \tfrac{e_i^2}{(1-h_{ii})^2}\,x_i x_i^{\top}\Bigr)(X^{\top}X)^{-1}',
        note='Only the middle changes. $\\hat\\beta$ is untouched, which is the whole point: robust '
             'standard errors fix your confidence, never your coefficients. Swap the meat for a '
             'per-cluster sum and you have clustered errors.',
        cost='no bias correction, only honest error bars'),
    code=dict(
        label='What ignoring 40 sessions per user actually costs',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n'
             'g = np.repeat(np.arange(<span class="s">50</span>), <span class="s">40</span>)  '
             '<span class="c"># 50 users, 40 sessions each</span>\n'
             'hits = <span class="s">0</span>\n'
             '<span class="k">for</span> _ <span class="k">in</span> '
             '<span class="k">range</span>(<span class="s">2000</span>):\n'
             '    u = rng.normal(size=<span class="s">50</span>)[g]                    '
             '<span class="c"># a per-user level</span>\n'
             '    x = rng.normal(size=<span class="s">50</span>)[g] + '
             'rng.normal(<span class="s">0</span>, <span class="s">.3</span>, '
             '<span class="s">2000</span>)\n'
             '    y = u + rng.normal(<span class="s">0</span>, <span class="s">.5</span>, '
             '<span class="s">2000</span>)                 '
             '<span class="c"># TRUE slope is exactly zero</span>\n'
             '    X = np.column_stack([np.ones(<span class="s">2000</span>), x])\n'
             '    b = np.linalg.lstsq(X, y, rcond=<span class="k">None</span>)['
             '<span class="s">0</span>]\n'
             '    r = y - X @ b\n'
             '    se = np.sqrt((r @ r / <span class="s">1998</span>) * '
             'np.linalg.inv(X.T @ X)[<span class="s">1</span>, <span class="s">1</span>])\n'
             '    hits += <span class="k">abs</span>(b[<span class="s">1</span>] / se) &gt; '
             '<span class="s">1.96</span>\n\n'
             '<span class="k">print</span>(hits / <span class="s">2000</span>)   '
             '<span class="c"># 0.71 -- a 5% test that fires 71% of the time under the null</span>')),
    real=('Reinhart &amp; Rogoff, <i>Growth in a Time of Debt</i> (2010), claimed growth turns '
          'sharply negative above a 90% debt-to-GDP ratio. Herndon, Ash &amp; Pollin at UMass '
          'Amherst reproduced it in April 2013 and found a spreadsheet range error excluding five '
          'countries, selective exclusions and an unconventional weighting scheme. Corrected, '
          'average growth above 90% debt was +2.2%, not -0.1% &mdash; a sign flip on a result that '
          'had already been cited in austerity policy across Europe and the US. Nobody caught it '
          'with a diagnostic test; somebody caught it by refitting the model.'),
    drills=[
        dict(q='Your ad-conversion model has two features correlated at 0.95. One coefficient is significantly positive, the other significantly negative. What is going on, and does it matter?',
             a=('<b>Multicollinearity &mdash; the coefficients are individually unidentified and '
                'jointly fine.</b> With $r = 0.95$ the data barely distinguish the two features, '
                'so the fit trades a large positive against a large negative and both come out '
                '&ldquo;significant&rdquo; while their sum is what is actually pinned down. '
                'Predictions are unaffected. Whether it matters is entirely about what you need: '
                'if this is a prediction model, ignore it and say so. If somebody is going to read '
                'the coefficients, you must drop one, combine them into a single feature, or '
                'regularise &mdash; and name which one you did, because they answer different '
                'questions.'),
             a_simple=('<b>The two features are nearly the same feature, so the model cannot tell '
                       'them apart.</b> It splits the credit into a big positive and a big '
                       'negative that cancel, and both look convincing on their own. The '
                       'predictions are completely unharmed. If nobody is reading the individual '
                       'numbers, this is not a problem. If somebody is, you have to drop one, '
                       'merge them, or hold them back towards zero &mdash; and say which, because '
                       'they mean different things.')),
        dict(q='Your regression has heteroskedastic residuals. Does that bias the coefficients?',
             a=('<b>No. It biases the standard errors.</b> OLS stays unbiased and consistent under '
                'heteroscedasticity; what it loses is efficiency, and the usual variance formula '
                'stops being the right one. So the point estimate you report is fine and the '
                'confidence interval around it is not. Use HC3 robust standard errors &mdash; '
                'they leave $\\hat\\beta$ byte-identical and only change the middle of the '
                'sandwich, so there is no reason not to make them the default. And check the '
                'direction rather than assuming: robust errors can come out larger or smaller '
                'than naive ones depending on where the variance sits relative to leverage.'),
             a_simple=('<b>No &mdash; it breaks the error bars, not the estimates.</b> The line you '
                       'fit is still centred in the right place. What is wrong is the stated '
                       'precision, because the usual formula assumes the noise is the same size '
                       'everywhere. Switch to error bars that do not make that assumption. They '
                       'leave the fitted line completely unchanged, so there is no reason not to '
                       'use them by default. And check which way they move &mdash; they can go '
                       'either way.')),
        dict(q='The residuals fail a normality test, and there are forty sessions per user. You have time to fix one. Which?',
             a=('<b>The forty sessions per user, and it is not close.</b> Non-normal residuals on a '
                'large sample cost you nothing &mdash; the CLT covers $\\hat\\beta$, and '
                'Shapiro&ndash;Wilk rejects on 100k rows whatever the truth is, so the test '
                'result carries no information. Non-independent errors cost you the entire '
                'inference: a simulation with a true slope of exactly zero, 50 users and 40 '
                'sessions each, rejects at nominal 5% about 71% of the time. Cluster on user, '
                'watch the $t$ statistic collapse, and re-read every conclusion you drew from that '
                'model.'),
             a_simple=('<b>The forty sessions per user, and it is not close.</b> Lopsided leftovers '
                       'cost you nothing on a big sample, and the test that flags them fires on '
                       'every large dataset regardless of whether anything is wrong. Treating '
                       'forty sessions from one person as forty independent facts costs you '
                       'everything: run it on data with no real effect at all and the model still '
                       'declares a winner about seven times in ten. Group the rows by person, and '
                       'watch most of your findings disappear.')),
    ],
    anchor=dict(
        formula=r'heteroscedasticity: wrong $\widehat{\text{Var}}(\hat\beta)$, right $\hat\beta$ &nbsp;&middot;&nbsp; multicollinearity: unstable $\hat\beta$, right $\hat y$',
        formula_simple='Uneven spread breaks your error bars. Features that move together break '
                       'your coefficients. Neither one breaks your predictions.',
        bullets=[
            'Robust HC3 errors by default; clustered errors the moment a unit appears more than once',
            'Multicollinearity leaves predictions intact &mdash; decide whether you need the coefficients before you panic',
            'Non-normal residuals is the assumption everyone tests and almost nobody needs',
        ]),
    chips=['HC3 robust errors', 'clustered standard errors', 'VIF', 'residual plots',
           'repeated measures'],
    followup='Your ad-conversion model has two features correlated at 0.95, one coefficient significantly positive and the other significantly negative. What is going on, and does it matter?',
),

# ============================================================================
dict(
    id='roc-pr-calibration',
    tier='advanced',
    title='ROC-AUC, PR-AUC and calibration',
    kicker='A model can rank every case perfectly and still be lying about every probability it prints',
    simple=[
        'There are two completely different questions you can ask a scoring model, and one number '
        'only answers the first. Question one: does it put the right cases at the top? That is '
        'ranking, and it is what the headline score on every dashboard measures. Question two: '
        'when it says seventy percent, does the thing happen seventy percent of the time? That is '
        'calibration, and the headline score cannot see it at all.',
        'A model can ace the first and fail the second completely &mdash; order every case '
        'correctly while squashing every probability into a narrow band around a half. Which one '
        'you need depends entirely on what happens next. If a human works a queue from the top '
        'down until they run out of hours, you need ranking. If the number gets multiplied by a '
        'cost, or compared against a threshold, or added to another number, you need calibration, '
        'and the ranking score will never once warn you that it is broken.',
    ],
    analogy=('<b>Like a thermometer that reads five degrees cold.</b> It still ranks the days '
             'perfectly &mdash; the hottest week of the year is still the hottest week on the '
             'dial &mdash; so if all you do is sort days, it is a fine instrument. The moment you '
             'use it to decide whether to grit the roads tonight, it is worse than useless, and no '
             'amount of checking the ordering will ever reveal that.'),
    trap_simple=('&ldquo;The ranking score is high, so the model is good.&rdquo; The sharper '
                 'version arrives later: &ldquo;we fixed the probabilities and the ranking score '
                 'did not move, so the fix did nothing.&rdquo; The fix could not have moved it. '
                 'Rescaling every score in the same direction leaves the order untouched by '
                 'construction, which is the cleanest proof that the two things are different '
                 'properties.'),
    tech=[
        'AUC is rank-based. It depends only on the ordering of $\\hat{p}$, so any strictly '
        'increasing map of the scores leaves it identical to the last decimal place while moving '
        'the probabilities anywhere you like. That single fact settles the question: ranking '
        'quality and calibration are different properties, and one metric sees only the first. A '
        'model with AUC 0.976 whose scores are squashed into $[0.4, 0.6]$ ranks flawlessly and is '
        'wrong about every individual probability.',
        'Measure calibration separately: a reliability diagram first, because it shows you the '
        'shape of the error, then the <b>Brier score</b> (a proper scoring rule, decomposing into '
        'calibration plus refinement) or <b>ECE</b> (binned, and genuinely sensitive to the '
        'binning, so quote the bin count). Fix on held-out data with Platt scaling or isotonic '
        'regression. Both are monotone, so both are invisible to AUC &mdash; if you expected the '
        'ranking metric to confirm your calibration fix, you have the wrong mental model.',
        'Then pick by the downstream decision, not by habit. A queue worked top-down at fixed '
        'capacity needs ranking and precision at $k$. A number multiplied by a cost, compared '
        'against a threshold, or fed into an expected-value rule needs calibration, and the '
        'ranking metric is silent about the thing that will hurt you.',
    ],
    tech_note=('Prevalence is the other axis and it is easy to conflate with this one. AUC is '
               'prevalence-invariant, which is exactly why it does not move when you deploy into a '
               'population with a different base rate &mdash; while precision does. At 0.1% '
               'positives a model with AUC 0.95 can still sit under 5% precision at any useful '
               'recall (Saito &amp; Rehmsmeier, PLoS ONE 2015). Ranking, calibration and '
               'prevalence are three separate failures and a single headline number hides all '
               'three.'),
    fig=dict(
        kind='panels',
        head=['THE PROBABILITIES ARE FICTION', 'THE RANKING IS FLAWLESS'],
        panels=[
            dict(t='reliability diagram', sub='every prediction bunched into 0.4 to 0.6',
                 tone='sig',
                 fig=dict(kind='plot', xr=(0, 1), yr=(0, 1), ph=340,
                          curves=[
                              dict(pts=[(0, 0), (1, 1)], tone='mute', sw=3, dash='14 10'),
                              dict(tone='sig', sw=4,
                                   pts=[(0.403, 0.013), (0.429, 0.145), (0.449, 0.247),
                                        (0.470, 0.351), (0.490, 0.453), (0.510, 0.541),
                                        (0.530, 0.650), (0.550, 0.741), (0.571, 0.852),
                                        (0.595, 0.974)]),
                          ])),
            dict(t='ROC curve, same model', sub='AUC 0.976 and nothing looks wrong',
                 tone='mem',
                 fig=dict(kind='plot', xr=(0, 1), yr=(0, 1), ph=340,
                          curves=[
                              dict(pts=[(0, 0), (1, 1)], tone='mute', sw=3, dash='14 10'),
                              dict(tone='mem', sw=4, fill=True,
                                   pts=[(0.000, 0.000), (0.004, 0.560), (0.008, 0.651),
                                        (0.012, 0.704), (0.020, 0.770), (0.030, 0.817),
                                        (0.040, 0.850), (0.060, 0.891), (0.080, 0.917),
                                        (0.110, 0.942), (0.150, 0.961), (0.200, 0.975),
                                        (0.260, 0.985), (0.330, 0.991), (0.420, 0.995),
                                        (0.521, 0.998), (0.664, 0.999), (0.804, 1.000),
                                        (1.000, 1.000)]),
                          ])),
        ],
        foot='one model, one set of predictions. the left picture says do not trust the number, '
             'the right one says ship it',
        alt='Two plots of the same model. On the left a reliability diagram where the curve rises '
            'almost vertically between predicted probabilities of 0.4 and 0.6 while the observed '
            'frequency runs from near zero to near one, far from the diagonal. On the right the '
            'ROC curve for the identical model hugs the top-left corner with an area under the '
            'curve of 0.976.'),
    caption=('Left and right are the same predictions. Squashing every score into $[0.4, 0.6]$ is '
             'a strictly increasing map, so the ROC curve is unchanged to six decimal places while '
             'the Brier score goes from 0.044 to 0.176. If your dashboard shows only the right '
             'panel, the left one can be arbitrarily bad and you will never find out.'),
    caption_simple=('Both pictures come from the same model on the same data. Squeezing every '
                    'score into a narrow band keeps the order exactly as it was, so the '
                    'right-hand picture does not change at all, while the left-hand one falls '
                    'apart. A dashboard that shows only the right-hand picture cannot warn you.'),
    when=[
        'The ops team says the fraud queue is full of garbage and the dashboard says AUC 0.97',
        'The score gets multiplied by an expected loss or compared against a cost threshold',
        'Someone reports AUC on a test set that was rebalanced to 50/50',
        'A risk score is about to be handed to a human who will read it as a probability',
    ],
    trap=('&ldquo;AUC is 0.97, so the model is great&rdquo; on 0.1% prevalence data, and its ugly '
          'cousin: reporting AUC on a class-rebalanced <i>test</i> set. Rebalancing the training '
          'set is a modelling choice you can defend; rebalancing the test set makes every '
          'downstream precision estimate a fiction, because precision depends on prevalence and '
          'you just changed prevalence by hand. The subtler trap, and the one that separates '
          'seniority: &ldquo;we ran isotonic regression and AUC did not move, so the calibration '
          'fix did nothing.&rdquo; It could not have moved AUC. Monotone maps preserve rank.'),
    math=dict(
        tex=r'\text{Brier} = \tfrac{1}{n}\sum_i (\hat p_i - y_i)^2 = \text{calibration} + \text{refinement} \qquad \text{AUC} = \text{AUC}\bigl(g(\hat p)\bigr)\ \ \forall\, g \text{ strictly increasing}',
        note='The right-hand statement is the whole card. AUC sees only the ordering of '
             '$\\hat{p}$; Brier sees the values. That is why a calibration fix cannot change AUC, '
             'and why AUC cannot detect a calibration failure.',
        cost='a proper scoring rule needs the probabilities, not the ranks'),
    code=dict(
        label='Identical AUC, four times the Brier score',
        cost='numpy, scikit-learn',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             '<span class="k">from</span> sklearn.metrics <span class="k">import</span> '
             'roc_auc_score, brier_score_loss\n\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n'
             'y = rng.binomial(<span class="s">1</span>, <span class="s">0.2</span>, '
             '<span class="s">40_000</span>)\n'
             'z = rng.normal(<span class="s">2.8</span> * y, <span class="s">1.0</span>)\n'
             'p = <span class="s">1</span> / (<span class="s">1</span> + np.exp(-(np.log('
             '<span class="s">0.25</span>) + <span class="s">2.8</span>*z - '
             '<span class="s">2.8</span>**<span class="s">2</span>/<span class="s">2</span>)))  '
             '<span class="c"># calibrated</span>\n'
             'q = <span class="s">0.4</span> + <span class="s">0.2</span> * p                    '
             '<span class="c"># squash into [0.4, 0.6] -- strictly increasing</span>\n\n'
             '<span class="k">print</span>(roc_auc_score(y, p), roc_auc_score(y, q))\n'
             '<span class="c"># 0.976141 0.976141   -- identical. rank is all AUC can see</span>\n'
             '<span class="k">print</span>(brier_score_loss(y, p), brier_score_loss(y, q))\n'
             '<span class="c"># 0.0439 0.1759       -- and the probabilities are now fiction</span>')),
    real=('The Epic Sepsis Model. Wong et al. (<i>JAMA Internal Medicine</i>, June 2021) validated '
          'it externally on 38,455 hospitalisations across 27,697 patients at Michigan Medicine. '
          'Epic advertised AUC 0.76&ndash;0.83; the measured AUC was 0.63. At the recommended '
          'threshold it ran at 33% sensitivity and 12% PPV &mdash; missing 1,709 of 2,552 sepsis '
          'cases, 67% of them, while alerting on 18% of all hospitalisations. It was live at '
          'hundreds of US hospitals, and the number on the datasheet was a ranking number.'),
    drills=[
        dict(q='Your fraud model has AUC 0.97 but the ops team says the queue is full of garbage. Diagnose it.',
             a=('<b>Compute precision at the operating threshold before you touch the model.</b> '
                'AUC 0.97 and a useless queue are entirely compatible at low prevalence: FPR has '
                'the huge negative class in its denominator, so a flood of false positives barely '
                'moves it, while precision has predicted positives in its denominator and collapses. '
                'At 0.1% prevalence, AUC 0.95 is compatible with precision under 5% at any useful '
                'recall. So: precision at $k$ where $k$ is what the team can actually work, the PR '
                'curve, and a reliability check at the top of the ranking. Then ask whether AUC '
                'was ever the metric this system should have been optimising.'),
             a_simple=('<b>Work out what fraction of the flagged cases are real, at the cutoff the '
                       'team actually uses.</b> When fraud is rare, a model can look excellent on '
                       'the headline score and still send mostly junk to the queue, because the '
                       'headline divides the mistakes by the enormous pile of ordinary cases. '
                       'Measure instead how many of the top hundred alerts are genuine, since that '
                       'is what the team lives with. Then ask whether the headline score was ever '
                       'the right thing to have been chasing.')),
        dict(q='Can a model be perfectly ranked and badly calibrated at the same time? Give me a concrete example.',
             a=('<b>Yes, and it is easy to construct on purpose.</b> Take any calibrated model and '
                'apply $q = 0.4 + 0.2p$. That map is strictly increasing, so it preserves every '
                'pairwise ordering and AUC is unchanged to six decimal places &mdash; 0.976141 '
                'before and after. But every probability now lives in $[0.4, 0.6]$, and the Brier '
                'score goes from 0.044 to 0.176 while ECE goes from 0.003 to 0.353. The decision '
                'that follows: if a human works the queue top-down, ship it unchanged. If anything '
                'downstream multiplies that number by a cost, do not, until you have calibrated on '
                'held-out data.'),
             a_simple=('<b>Yes, and you can build one deliberately in a single line.</b> Take a '
                       'model whose probabilities are honest and squeeze them all into the band '
                       'between forty and sixty percent. The order of the cases never changes, so '
                       'the headline ranking score is identical to the last decimal. But now every '
                       'number it prints is wrong. If a person works the list from the top, it '
                       'still does its job. If anything multiplies that number by a cost, it is '
                       'now dangerous.')),
        dict(q='You ran isotonic regression on a held-out set and AUC did not change. Did the calibration fix work?',
             a=('<b>The AUC not moving is expected and tells you nothing either way.</b> Isotonic '
                'regression is monotone, so it can only merge ties &mdash; it is close to '
                'incapable of changing the ranking, and Platt scaling is strictly monotone so it '
                'cannot change AUC at all. Measure the thing you actually changed: Brier score and '
                'a reliability diagram on a third split, not the split you fitted the calibrator '
                'on, because fitting the calibrator and scoring it on the same data gives you '
                'optimistic calibration for the same reason it gives you optimistic accuracy.'),
             a_simple=('<b>The ranking score not moving is exactly what should happen, so it '
                       'answers nothing.</b> The fix only rescales the numbers without reordering '
                       'them, so it cannot change a score that only looks at the order. Judge it '
                       'on what it was meant to change: does a bucket of cases the model called '
                       'seventy percent now come true about seventy percent of the time? And check '
                       'that on data you did not use to build the fix, or you will flatter '
                       'yourself.')),
    ],
    anchor=dict(
        formula=r'AUC sees only $\text{rank}(\hat p)$ &nbsp;&middot;&nbsp; Brier and ECE see $\hat p$ itself',
        formula_simple='One number asks whether the order is right. The other asks whether the '
                       'numbers are true. Fixing the second cannot move the first.',
        bullets=[
            'Any strictly increasing rescaling leaves the ranking metric identical and the probabilities anywhere you like',
            'Queue worked top-down at fixed capacity: you need ranking. Number multiplied by a cost: you need calibration',
            'Fix calibration on held-out data, then re-measure Brier and the reliability diagram, never AUC',
        ]),
    chips=['reliability diagram', 'Brier score', 'expected calibration error', 'Platt scaling',
           'isotonic regression'],
    followup='Your fraud model has AUC 0.97 but the ops team says the queue is full of garbage. Diagnose it.',
),

]
