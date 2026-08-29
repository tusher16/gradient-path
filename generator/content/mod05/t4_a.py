CARDS = [

    # ------------------------------------------------------------------ 1
    dict(
        id='srm',
        tier='production',
        title='Sample ratio mismatch',
        kicker='The first thing you check, and the only finding that voids an experiment rather than qualifying it',
        simple=[
            'You asked for an even split. Before you look at a single metric, count how many '
            'users actually landed in each arm. If the counts differ by more than chance can '
            'explain, something in the pipeline is deciding who gets assigned or who gets '
            'counted, and that something is tangled up with the treatment.',
            'This is not a caveat you put at the bottom of the readout. Random assignment is the '
            'only reason the two groups are comparable at all &mdash; it is the entire basis for '
            'calling the difference an effect. Break it and your number is contaminated by an '
            'unknown amount in an unknown direction. You cannot correct for it, because you '
            'would have to know which users went missing and why. You cannot drop them either: '
            'whatever removed them was correlated with the treatment, so removing them yourself '
            'just repeats the bug by hand. You bin the result, find the cause, and rerun.',
            'And the imbalance that matters is far smaller than it looks. On 1.2 million users, '
            'a split of 50.4 against 49.6 means nearly five thousand people are unaccounted for.',
        ],
        analogy=('<b>Like weighing two bags of shopping when one bag has a hole in it.</b> The '
                 'scales are accurate and the reading is repeatable, and it is still measuring '
                 'the wrong thing. You cannot guess a correction either, because what fell '
                 'through the hole was not a random handful &mdash; it was the tins and the '
                 'bottles.'),
        trap_simple=('Two sentences cost the loop. The first is <i>"it is only four tenths of a '
                     'percent off, that is fine"</i> &mdash; at over a million users that gap is '
                     'thousands of people and nowhere near chance. The second is <i>"we found '
                     'the mismatch, dropped the affected users and carried on"</i> &mdash; the '
                     'thing that removed them was correlated with the treatment, so dropping '
                     'them by hand keeps the bias and adds a story about why it is fine.'),
        tech=[
            'An SRM check is a chi-square goodness-of-fit test on the per-arm user counts against '
            'the configured allocation. Run it on every experiment, every day, before the metric. '
            'Alarm at $p &lt; 0.0005$, not $0.05$ &mdash; you are running this check thousands of '
            'times a year and you want almost no false alarms, and a genuine SRM is gross rather '
            'than marginal. The 50.4 / 49.6 split on 1.2 million users gives $\\chi^2 = 76.8$ and '
            '$p \\approx 2 \\times 10^{-18}$; at that sample size anything past roughly '
            '50.16 / 49.84 already trips the threshold.',
            'Then localise it against the five-bucket taxonomy from Fabijan et al. '
            '<b>Assignment</b>: a randomisation bug, unstable IDs, assignment correlated across '
            'concurrent experiments. <b>Execution</b>: a redirect that costs treatment a page '
            'load, a delivery delay, a client bundle that fails to load. <b>Log processing</b>: a '
            'bot filter or a bad join applied after assignment. <b>Analysis</b>: the wrong trigger '
            'condition, incomplete counterfactual logging. <b>Interference</b>: force-assignment '
            'through URL parameters. The diagnostic is one query &mdash; recompute the ratio at '
            'assignment, at exposure, and after every filter. Clean at assignment and broken '
            'after filtering means the treatment is changing who gets counted, and your metric is '
            'measuring that change rather than the feature.',
        ],
        tech_note=('Two things get called an SRM and are not. A ratio that drifts on the first '
                   'day of a ramp is a ramp &mdash; recompute once allocation is stable. And a '
                   'triggered analysis legitimately counts fewer users than were assigned, so '
                   'the check belongs on the triggered population against its own expected '
                   'ratio, not against the assignment ratio. What is never acceptable is an SRM '
                   'you have explained but not fixed: an explanation is not a correction, and '
                   'the estimate stays void either way.'),
        math=dict(
            tex=r'\chi^2 = \sum_i \frac{(O_i - E_i)^2}{E_i} \;\Rightarrow\; 2\cdot\frac{4800^2}{600000} = 76.8, \quad p \approx 2 \times 10^{-18}',
            note='The test says the split is not chance. It says nothing about which users are '
                 'missing or which way the estimate is pushed &mdash; which is exactly why there '
                 'is no adjustment available to you, only a rerun.',
            cost='one degree of freedom, and a threshold of 0.0005'),
        code=dict(
            label='Where the ratio breaks, in one query',
            cost='scipy',
            src=('<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
                 '<span class="c"># run the check at every stage, not just on the final table</span>\n'
                 '<span class="k">for</span> stage, (c, t) <span class="k">in</span> counts.items():\n'
                 '    chi2, p = stats.chisquare([c, t], f_exp=[(c + t) / <span class="s">2</span>] * <span class="s">2</span>)\n'
                 '    <span class="k">print</span>(stage, c, t, <span class="s">f"p={p:.2g}"</span>)\n\n'
                 '<span class="c"># assigned      600102  599898   p=0.79   &lt;- the coin was fair</span>\n'
                 '<span class="c"># exposed       600102  599898   p=0.79   &lt;- delivery was fair</span>\n'
                 '<span class="c"># bot-filtered  604800  595200   p=1.9e-18 &lt;- it broke HERE</span>\n'
                 '<span class="c"># the filter is the bug. the metric was never the story</span>')),
        fig=dict(
            kind='blocks', h=282,
            boxes=[
                dict(x=34, y=42, w=150, h=52, t='control', sub='expected 600,000', tone='mem'),
                dict(x=34, y=112, w=150, h=52, t='treatment', sub='expected 600,000', tone='mem'),
                dict(x=240, y=42, w=160, h=52, t='604,800 counted', sub='4,800 too many', tone='sig'),
                dict(x=240, y=112, w=160, h=52, t='595,200 counted', sub='4,800 missing', tone='sig'),
                dict(x=452, y=77, w=234, h=52, t='chi-square 76.8',
                     sub='about 2 in a billion billion', tone='sig'),
                dict(x=34, y=196, w=196, h=52, t='clean at assignment',
                     sub='the coin was fair', tone='mem'),
                dict(x=262, y=196, w=190, h=52, t='broken after the bot filter',
                     sub='engaged users dropped', tone='sig'),
                dict(x=484, y=196, w=202, h=52, t='treatment changed who is counted',
                     sub='not a metric bug', tone='sig'),
            ],
            links=[dict(a=0, b=2), dict(a=1, b=3), dict(a=2, b=4, tone='sig'),
                   dict(a=3, b=4, tone='sig'), dict(a=5, b=6), dict(a=6, b=7)],
            labels=[dict(x=34, y=20, t='what you configured', a='start', tone='mem', op=0.85),
                    dict(x=686, y=20, t='what the logs counted', a='end', tone='sig', op=0.85),
                    dict(x=34, y=184, t='then localise it', a='start', op=0.55)],
            foot='the gap you can ignore by eye is a one-in-a-billion-billion event by chi-square',
            alt='A configured fifty-fifty split of 1.2 million users set against the counts '
                'actually logged, 604,800 versus 595,200, giving a chi-square of 76.8, and a '
                'second row locating the break after the bot filter rather than at assignment'),
        caption=('The check is one line of arithmetic; the value is in the second row. '
                 'Recomputing the ratio at each stage turns "the experiment is broken" into "the '
                 'bot filter is eating engaged treatment users", which is a bug someone can fix '
                 'this afternoon.'),
        caption_simple=('The top row is the check: the split you asked for against the split the '
                        'system actually recorded. The bottom row is the useful part &mdash; '
                        'asking at which step the two numbers stopped agreeing, because that '
                        'step is the bug.'),
        when=[
            'Every experiment readout, before you look at the metric',
            'The split is 50.4% / 49.6% on 1.2 million users and the PM calls it close enough',
            'Treatment ships behind a redirect, a new bundle, or an extra permission prompt',
            'Your bot filter, trigger condition or telemetry join changed since the last experiment',
        ],
        trap=('Two sentences, both common. <i>"The split is 0.4% off from 50/50, that is '
              'fine"</i> &mdash; at 1.2 million users the chi-square p-value is about two in a '
              'billion billion, so it is neither fine nor close. And the worse one: <i>"we found '
              'the SRM, excluded the users the bot filter flagged, and reran"</i> &mdash; the '
              'exclusion is itself correlated with treatment, so you have not removed the bias, '
              'you have hidden it. The third, rarer and just as fatal, is <i>"we will adjust for '
              'it"</i>. You cannot. The direction is unknown.'),
        real=('Microsoft&rsquo;s experimentation platform found a sample ratio mismatch in '
              'roughly <b>6% of experiments</b> &mdash; at about 10,000 experiments a year, one '
              'a day (Fabijan et al., KDD 2019). The named cases are worth memorising because '
              'each is a different bucket: <b>MSN Carousel</b>, where the bot detector flagged '
              'genuinely engaged treatment users as bots and masked a real win; <b>Skype '
              'Audio</b>, where a mid-session configuration refresh corrupted variant-ID logging '
              'and lost <b>30% of treatment sessions</b>; and <b>Microsoft Teams</b>, where '
              'first-run-experience filtering quietly excluded eligible users from the triggered '
              'analysis.'),
        drills=[
            dict(q='You see a 50.4% / 49.6% split on 1.2 million users. Is that a problem, and where do you look first?',
                 a=('<b>Yes, and it is not close.</b> Chi-square against a 600,000 / 600,000 '
                    'expectation gives $\\chi^2 = 76.8$ and $p \\approx 2 \\times 10^{-18}$ '
                    '&mdash; about 4,800 users on each side of the line. At this $n$ even '
                    '50.16 / 49.84 clears a 0.0005 threshold. Then localise: recompute the ratio '
                    'at assignment, at exposure, and after each filter. Clean at assignment and '
                    'broken after filtering points at the bot filter or the trigger condition, '
                    'which means the treatment is changing who gets counted.'),
                 a_simple=('<b>Yes, and it is not marginal.</b> Four tenths of a percent on 1.2 '
                           'million users is about 4,800 people on each side of the line, which '
                           'a fair coin produces roughly never &mdash; a couple of times in a '
                           'billion billion runs. Then find where it broke: count the users at '
                           'assignment, at the moment they saw the change, and after each filter '
                           'in the pipeline. If the counts are even at assignment and uneven '
                           'afterwards, a filter is removing people, and it is removing them '
                           'because of the treatment.')),
            dict(q='You confirm an SRM. Can you exclude the users your bot filter flagged and analyse the rest?',
                 a=('<b>No &mdash; the exclusion is the bug, not the fix.</b> The filter removed '
                    'users as a function of their behaviour, and behaviour is exactly what the '
                    'treatment changed, so the surviving population is no longer a random split. '
                    'Excluding them by hand reproduces the same selection and adds a false sense '
                    'of having handled it. There is no adjustment either: an SRM tells you the '
                    'estimate is wrong, not by how much or in which direction. Fix the filter, '
                    'rerun, and treat the earlier readout as absent rather than negative.'),
                 a_simple=('<b>No &mdash; throwing them out is the same mistake, done '
                           'deliberately.</b> The filter did not pick people at random. It '
                           'picked them for how they behaved, and how they behaved is the thing '
                           'your change was supposed to affect, so the group left behind is no '
                           'longer an even, fair split. There is nothing to adjust either: the '
                           'check tells you the answer is wrong, not how wrong or in which '
                           'direction. Fix the filter, run it again, and treat the first result '
                           'as one you never got.')),
            dict(q='Treatment is served through a redirect and control is not. What does that do to your experiment?',
                 a=('<b>It manufactures an SRM, and biases the metric in the same move.</b> The '
                    'redirect costs an extra round trip, so a slice of treatment users abandon '
                    'before the page renders and never reach the logs &mdash; and those users '
                    'are disproportionately the slow-connection, low-patience ones. Treatment '
                    'quietly loses its worst users, which flatters the treatment mean, so the '
                    'p-value on your metric is partly measuring the redirect. The fix is '
                    'symmetry: redirect both arms, or assign server-side so the split is decided '
                    'before anything renders.'),
                 a_simple=('<b>It breaks the experiment before the feature has done '
                           'anything.</b> The extra hop costs time, so some people on the '
                           'treated side give up before the page appears and are never counted. '
                           'They are not a random sample of that group &mdash; they are the ones '
                           'on slow connections with the least patience. The treated group loses '
                           'its least engaged users and looks better for a reason that has '
                           'nothing to do with the change. Send both sides through the same hop, '
                           'or decide the split on the server before anything loads.')),
        ],
        anchor=dict(
            formula=r'$\chi^2 = \sum_i (O_i - E_i)^2 / E_i$ &nbsp;&middot;&nbsp; alarm at $p < 0.0005$, never $0.05$',
            formula_simple='Count the users in each arm first. If the gap is bigger than chance, '
                           'stop &mdash; do not adjust it, do not drop anyone, rerun it.',
            bullets=[
                'Run it on every experiment before you read the metric, at a one-in-two-thousand threshold',
                'An SRM voids the estimate in an unknown direction, so there is no adjustment and no partial credit',
                'Localise it by recomputing the ratio at assignment, at exposure, and after every filter',
            ]),
        chips=['chi-square goodness-of-fit', 'A/A test', 'bot filtering', 'trigger conditions',
               'guardrail metrics'],
        followup='You see 50.4% / 49.6% on 1.2 million users. Is that a problem &mdash; and where would you look first?',
    ),

    # ------------------------------------------------------------------ 2
    dict(
        id='cuped',
        tier='production',
        title='CUPED and variance reduction',
        kicker='The fastest way to shorten an experiment is not more traffic &mdash; it is subtracting the noise you could have predicted before it started',
        simple=[
            'You already know a great deal about each user before the experiment starts. Someone '
            'who spent a lot last month will probably spend a lot this month, whichever arm they '
            'land in. That predictable part of their behaviour is pure noise as far as your '
            'experiment is concerned: it is variation between people, not variation caused by '
            'your change. So subtract it. Take each user&rsquo;s pre-period value, work out how '
            'much of this period it predicts, and remove that much before you compare the arms.',
            'The average difference between the arms does not move, and that is the point &mdash; '
            'it stays an honest estimate of the same quantity. What collapses is the spread '
            'around it. The noise left over is one minus the squared correlation between the '
            'pre-period and the experiment period, so a correlation of 0.7 removes about half the '
            'variance. That buys you roughly half the users, or half the calendar, for exactly '
            'the same answer.',
        ],
        analogy=('<b>Like weighing yourself on the same scales every morning.</b> Your weight '
                 'swings a kilo either way from what you ate yesterday, and none of that swing '
                 'has anything to do with the diet you started on Monday. Subtract each '
                 'person&rsquo;s usual and look only at the change. The diet does exactly what '
                 'it did before; you can just see it through far less noise.'),
        simple_extra=('The covariate has to come from before the coin was flipped. Adjust for '
                      'something measured during the experiment &mdash; sessions this week, '
                      'pages viewed, whether they clicked &mdash; and the treatment has already '
                      'had a chance to move it, so you are subtracting part of the effect you '
                      'are trying to measure. That does not make the estimate quieter, it makes '
                      'it wrong. The other limit is structural: new users have no pre-period at '
                      'all, so this helps least on exactly the population a growth team most '
                      'wants to read.'),
        trap_simple=('Calling it a way to correct an uneven split between the arms. It is not a '
                     'correction and was never meant to be one &mdash; random assignment already '
                     'balances the arms on average, and this adjustment leaves the average '
                     'difference exactly where it was. All it does is remove noise you could '
                     'have predicted, so the same number of users buys a sharper answer.'),
        tech=[
            'CUPED replaces $Y$ with $Y_{\\text{adj}} = Y - \\theta(X - \\mathbb{E}[X])$, where '
            '$X$ is a pre-experiment covariate and $\\theta = \\operatorname{Cov}(Y,X) / '
            '\\operatorname{Var}(X)$. Because $\\mathbb{E}[X]$ is subtracted back, the adjusted '
            'metric has the same expectation as $Y$: the point estimate is unchanged and still '
            'unbiased. The variance is multiplied by $(1 - \\rho^2)$, and since $n \\propto '
            '\\sigma^2$ the sample-size saving is the same factor. $\\rho = 0.7$ removes 51% of '
            'the variance and therefore about half the users or half the runtime; $\\rho = 0.5$ '
            'removes only 25%.',
            'The natural $X$ is the same metric in the pre-period, but name the extensions: '
            'post-stratification on at-assignment attributes, control variates built from an ML '
            'prediction of $Y$, and 2024-onward methods combining pre- and in-experiment data. '
            'The hard rule is that $X$ must be measured before assignment. An in-experiment '
            'covariate is a bad control &mdash; it is partly an outcome, so $\\theta$ absorbs '
            'part of the treatment effect and the adjusted estimate is pulled towards zero. And '
            'CUPED does nothing for users with no pre-period, which is why the complete answer '
            'segments: CUPED for returners, at-assignment covariates such as device, geography '
            'and acquisition channel for new users, reported as two segments or combined in a '
            'stratified estimator.',
        ],
        tech_note=('Estimating $\\theta$ from the experiment data is fine and creates no '
                   'meaningful bias at realistic sample sizes, because $X$ is fixed before '
                   'assignment &mdash; estimate it on the pooled arms, not per arm. The failure '
                   'mode worth watching is a covariate that correlates well in aggregate but not '
                   'inside your key segments: you get a headline variance reduction and no extra '
                   'sensitivity where the decision actually lives.'),
        math=dict(
            tex=r'Y_{\text{adj}} = Y - \theta\,(X - \mathbb{E}[X]), \quad \theta = \frac{\operatorname{Cov}(Y,X)}{\operatorname{Var}(X)} \qquad \operatorname{Var}(Y_{\text{adj}}) = (1-\rho^2)\operatorname{Var}(Y)',
            note='Nothing here touches the expectation, which is precisely why it cannot fix an '
                 'imbalance &mdash; and why $X$ must be pre-assignment, or $\\theta$ quietly '
                 'absorbs part of the effect you came to measure.',
            cost='one pre-experiment covariate, and the correlation you actually have'),
        code=dict(
            label='What the correlation is really worth',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
                 '<span class="c"># x = the SAME metric, measured in the two weeks BEFORE assignment</span>\n'
                 'theta = np.cov(y, x)[<span class="s">0</span>, <span class="s">1</span>] / np.var(x, ddof=<span class="s">1</span>)\n'
                 'y_adj = y - theta * (x - x.mean())\n\n'
                 'rho = np.corrcoef(y, x)[<span class="s">0</span>, <span class="s">1</span>]\n'
                 '<span class="k">print</span>(y_adj.var(ddof=<span class="s">1</span>) / y.var(ddof=<span class="s">1</span>), <span class="s">1</span> - rho**<span class="s">2</span>)\n'
                 '<span class="c"># 0.489   0.490    -- the variance ratio IS one minus rho squared</span>\n'
                 '<span class="c"># the mean difference between arms is unchanged. that is the test</span>\n\n'
                 '<span class="c"># swap in an in-experiment x and the estimated lift SHRINKS while</span>\n'
                 '<span class="c"># the interval tightens. that is bias, and no variance trick does it</span>')),
        fig=dict(
            kind='plot', xr=(0, 28), yr=(0, 1.0), ph=190,
            head=['THE SAME EXPERIMENT', 'WITH THE PRE-PERIOD SUBTRACTED'],
            xlab='days running', ylab='half-width of the interval',
            xticks=[(0, '0'), (7, '7'), (14, '14'), (21, '21'), (28, '28')],
            yticks=[(0.3, '0.30 pp'), (0.6, '0.60 pp'), (0.9, '0.90 pp')],
            hlines=[dict(y=0.30, tone='plain', label='the width you need to decide')],
            vlines=[dict(x=14, tone='mem', label='same width, day 14'),
                    dict(x=28, tone='sig', label='day 28')],
            curves=[
                dict(pts=[(3, 0.917), (5, 0.710), (7, 0.600), (10, 0.502), (14, 0.424),
                          (21, 0.346), (28, 0.300)],
                     tone='sig', label='no adjustment', lat=2, dx=10, dy=-12),
                dict(pts=[(3, 0.655), (5, 0.507), (7, 0.428), (10, 0.359), (14, 0.303),
                          (21, 0.247), (28, 0.214)],
                     tone='mem', label='CUPED, correlation 0.7', lat=2, dx=10, dy=18),
            ],
            marks=[dict(x=14, y=0.303, label='half the calendar', tone='mem', dx=10, dy=-10)],
            foot='same traffic, same effect, half the runtime -- that is what a pre-period correlation of 0.7 buys',
            alt='Two curves of confidence-interval half-width against days running for the same '
                'experiment; the CUPED-adjusted curve reaches the decision width on day 14 while '
                'the unadjusted one needs day 28'),
        caption=('Both curves are the same experiment on the same traffic. The only difference is '
                 'whether the pre-period covariate was subtracted first, and the interval you '
                 'need to decide arrives on day 14 instead of day 28. Nothing about the effect '
                 'changed &mdash; only how much noise you had to see through.'),
        caption_simple=('Both lines are the same experiment with the same users. The lower one '
                        'has last month&rsquo;s behaviour subtracted out first. It reaches a '
                        'usable answer in half the time, and it is answering the same question.'),
        when=[
            'The power calculation says six weeks and the roadmap says two',
            'Your metric is revenue or sessions per user &mdash; heavy tailed and stubbornly noisy',
            'Most users in the experiment have a stable pre-period you already log',
            'Someone proposes adjusting for a metric measured inside the experiment window',
        ],
        trap=('The sentence is <i>"we used CUPED to control for the pre-experiment differences '
              'between the two arms"</i>. That is a bias story, and CUPED is not a bias story '
              '&mdash; the adjustment leaves the expectation untouched, and randomisation already '
              'handles imbalance on average. The second version is worse and harder to catch: '
              '<i>"we regressed out sessions during the experiment because it correlated '
              'better"</i>. An in-experiment covariate is partly an outcome, so you subtract part '
              'of your own treatment effect and report a shrunken lift with a suspiciously tight '
              'interval.'),
        real=('CUPED comes from Deng, Xu, Kohavi and Walker at Bing, <i>Improving the Sensitivity '
              'of Online Controlled Experiments by Utilizing Pre-Experiment Data</i> (WSDM 2013), '
              'and it is now a default feature in Optimizely, Statsig and Eppo rather than a '
              'research idea. The number that made it standard is just the arithmetic: a '
              'pre-period covariate correlated at <b>0.7</b> with the experiment metric removes '
              '<b>51% of the variance</b>, which is <b>half the sample size or half the '
              'runtime</b> for an identical point estimate.'),
        drills=[
            dict(q='CUPED cut your variance by 40% on returning users and did nothing at all for new users. What now?',
                 a=('<b>Segment, and use covariates that exist at assignment time.</b> New users '
                    'have no pre-period, so there is no $X$ to regress out &mdash; that is '
                    'structural, not a tuning problem. What you do have at the moment of '
                    'assignment is device, geography, acquisition channel and campaign, so apply '
                    'post-stratification or regression adjustment on those: smaller reduction, '
                    'still real. Report the two segments separately or combine them in a '
                    'stratified estimator with segment-specific $\\theta$. Then ask whether new '
                    'users belong in the decision at all &mdash; if the feature is for returners, '
                    'power on returners and stop paying for the rest.'),
                 a_simple=('<b>Split the population and use what you know at the moment of '
                           'assignment.</b> New users have no history to subtract, and no amount '
                           'of tuning creates one. But you do know their device, their country '
                           'and how they arrived, so group them by those and compare within '
                           'groups &mdash; weaker than a full history, much better than nothing. '
                           'Report the two groups separately, or combine them with the right '
                           'weight for each. And ask whether new users belong in the decision at '
                           'all: if the feature is for people who come back, power the test on '
                           'people who come back.')),
            dict(q='A teammate wants to use sessions during the experiment window as the covariate, because it correlates with revenue better than the pre-period does.',
                 a=('<b>No &mdash; that stronger correlation is exactly the problem.</b> Sessions '
                    'in the window are downstream of the treatment, so the covariate is partly an '
                    'outcome. Subtracting it removes part of the effect you came to measure and '
                    'pulls the estimate towards zero; it is the bad-control problem wearing a '
                    'variance-reduction hat. The tell is that the lift shrinks while the interval '
                    'tightens, which no legitimate variance reduction does &mdash; CUPED must '
                    'leave the point estimate alone. If they want more correlation, build a '
                    'predicted-$Y$ control variate out of pre-assignment features instead.'),
                 a_simple=('<b>No, and the strong correlation is the reason why.</b> Anything '
                           'measured during the experiment could have been changed by the '
                           'experiment. Subtract it and you subtract part of your own result, so '
                           'the measured effect shrinks towards nothing while the error bars get '
                           'tighter &mdash; and that combination is the giveaway. A legitimate '
                           'noise reduction never moves the headline number, only the '
                           'uncertainty around it. If they want a better predictor, build one '
                           'out of things known before anyone was assigned.')),
            dict(q='Your pre-period metric correlates with the experiment metric at 0.5. How much runtime does that buy you?',
                 a=('<b>25%, not half.</b> The variance multiplier is $1 - \\rho^2 = 0.75$, and '
                    'since $n \\propto \\sigma^2$ you need three quarters of the users &mdash; a '
                    'two-week test becomes about ten and a half days. The relationship is '
                    'quadratic and unforgiving at the bottom: $\\rho = 0.3$ saves 9%, $\\rho = '
                    '0.7$ saves 51%, $\\rho = 0.9$ saves 81%. So the honest answer to "should we '
                    'build CUPED" is to measure $\\rho$ on last quarter&rsquo;s data first; below '
                    'roughly 0.4 it does not pay for the pipeline.'),
                 a_simple=('<b>A quarter of it, not half.</b> The noise that survives is one '
                           'minus the correlation squared, and half of a half is a quarter, so '
                           'three quarters of the noise remains and you still need about three '
                           'quarters of the users. A fortnight becomes ten and a half days. The '
                           'saving climbs steeply though: seven tenths halves the test, nine '
                           'tenths cuts it to a fifth. So measure the correlation on last '
                           'quarter&rsquo;s data before you build anything &mdash; under about '
                           'four tenths it does not pay for the pipeline.')),
        ],
        anchor=dict(
            formula=r'$Y_{\text{adj}} = Y - \theta(X - \mathbb{E}[X])$ &nbsp;&middot;&nbsp; variance $\times\,(1 - \rho^2)$, and the mean is untouched',
            formula_simple='Subtract what last month already predicted, then compare what is '
                           'left. Same answer, much less noise.',
            bullets=[
                'The covariate must be measured before assignment &mdash; no exceptions, however well it correlates',
                'Variance falls by one minus the squared correlation: seven tenths halves your runtime, a half only trims a quarter',
                'It reduces variance, it does not correct bias, and it does nothing for users with no history',
            ]),
        chips=['variance reduction', 'post-stratification', 'control variates', 'bad controls',
               'statistical power'],
        followup='CUPED cut your variance by 40% on returning users and did nothing for new users. What now?',
    ),

    # ------------------------------------------------------------------ 3
    dict(
        id='randomisation-unit',
        tier='production',
        title='Randomisation unit is not analysis unit',
        kicker='You randomised users and you are analysing clicks per impression, so your standard error is a work of fiction',
        simple=[
            'You flipped the coin once per user. Then you built a table with one row per session, '
            'or per click, or per search, and ran a test as though every row were its own coin '
            'flip. They are not. Every row belonging to one person moves together: a heavy user '
            'contributes fifty rows that all look alike, and the test counts them as fifty '
            'independent pieces of evidence when they are closer to one.',
            'So the test believes it has far more information than it has. The standard errors '
            'come out too small &mdash; often by a factor of two to five &mdash; and almost '
            'everything looks significant. The tell is an experiment run against itself with no '
            'change in it at all, which should look significant about one time in twenty and '
            'instead fires constantly. The fix keeps the coin flip as the unit: either collapse '
            'each person down to one number and compare those, or use a method that knows the '
            'rows arrive in clumps. Your sample size is the number of people, not the number of '
            'rows.',
        ],
        analogy=('<b>Like a survey where one household posts back fifty forms.</b> You send out '
                 'two thousand questionnaires and one enthusiastic street returns half of them. '
                 'You now hold a thousand pieces of paper and you do not hold a thousand '
                 'opinions. Counting the paper instead of the households is precisely what a '
                 'per-event test does, and it leaves you certain about something you barely '
                 'measured.'),
        simple_extra=('There is a decision hiding inside the fix. Collapsing each person to a '
                      'single number is not the same as pooling everybody&rsquo;s events '
                      'together: the average of everyone&rsquo;s personal click rate is a '
                      'different quantity from the overall click rate, because the second one '
                      'lets your heaviest users vote fifty times. Both are defensible. Only one '
                      'of them is what the business means when it asks whether the feature '
                      'worked, and you have to say which before you run the test, not after you '
                      'have seen both.'),
        trap_simple=('Adding up every click, adding up every impression, dividing one by the '
                     'other, and testing that with the number of impressions as the sample size. '
                     'The sentence that gives it away is <i>"we have two million rows, so we have '
                     'plenty of power"</i> &mdash; you have forty thousand users, and forty '
                     'thousand is your sample size no matter how many rows they generated.'),
        tech=[
            'Randomise by user and analyse per event and the events inside a user are correlated, '
            'so the naive standard error omits the within-user covariance and comes out too small '
            '&mdash; often by a factor of two to five. Your A/A tests then fire far above nominal, '
            'which is the cheapest diagnostic you own. The general form is the cluster design '
            'effect, $1 + (m-1)\\rho_{\\text{ICC}}$ for average cluster size $m$: the effective '
            'sample size is $n$ divided by that, and with fifty sessions per user even a modest '
            'intra-user correlation destroys most of your apparent $n$.',
            'Two correct fixes, and they are provably equivalent for clustered randomised '
            'experiments: the <b>delta method</b> for ratio metrics, and <b>cluster-robust '
            'standard errors</b> clustered on the randomisation unit. The delta method for '
            '$R = \\bar{X} / \\bar{Y}$ computes every moment at the user level, not the event '
            'level. The third option is to aggregate first &mdash; one ratio per user, then a '
            't-test on those &mdash; which is valid but changes the estimand from a ratio of '
            'averages to an average of ratios, so say which one the business is asking for. The '
            'same problem wears other names: session metrics under user randomisation, per-query '
            'metrics under per-user assignment, per-seat metrics under account randomisation in '
            'B2B.',
        ],
        tech_note=('The same rule governs the bootstrap: resample <i>users</i>, not rows. '
                   'Bootstrapping rows in clustered data reproduces the naive standard error '
                   'exactly, with a computational ritual on top that makes it look careful. And '
                   'fixing the standard error does not fix the metric choice &mdash; a ratio of '
                   'averages and an average of ratios can move in opposite directions when the '
                   'treatment changes how much each user does.'),
        math=dict(
            tex=r'\operatorname{Var}\!\left(\frac{\bar{X}}{\bar{Y}}\right) \approx \frac{\operatorname{Var}(X)}{\mu_Y^2} - \frac{2\mu_X \operatorname{Cov}(X,Y)}{\mu_Y^3} + \frac{\mu_X^2 \operatorname{Var}(Y)}{\mu_Y^4}',
            note='Every moment on the right is computed over users, not over events. Compute them '
                 'over events and you have simply rewritten the naive standard error in heavier '
                 'notation.',
            cost='ratio metrics, first-order approximation, moments at the cluster level'),
        code=dict(
            label='The same data, two standard errors',
            cost='statsmodels',
            src=('<span class="k">import</span> statsmodels.api <span class="k">as</span> sm\n\n'
                 '<span class="c"># df has one row per impression; user_id is the randomisation unit</span>\n'
                 'naive = sm.OLS(df.click, sm.add_constant(df.treated)).fit()\n'
                 'clust = naive.get_robustcov_results(cov_type=<span class="s">"cluster"</span>,\n'
                 '                                    groups=df.user_id)\n\n'
                 '<span class="k">print</span>(naive.bse[<span class="s">1</span>], clust.bse[<span class="s">1</span>])\n'
                 '<span class="c"># 0.00041   0.00147    -- 3.6x wider once you cluster on the user</span>\n'
                 '<span class="c"># p 0.004 -&gt; p 0.31. same rows, same estimate, opposite decision</span>')),
        fig=dict(
            kind='blocks', h=246,
            boxes=[
                dict(x=34, y=94, w=140, h=56, t='user 8812', sub='one coin flip', tone='mem'),
                dict(x=232, y=24, w=132, h=32, t='session 1'),
                dict(x=232, y=62, w=132, h=32, t='session 2'),
                dict(x=232, y=100, w=132, h=32, t='session 3'),
                dict(x=232, y=138, w=132, h=32, t='and so on'),
                dict(x=232, y=176, w=132, h=32, t='session 50'),
                dict(x=418, y=56, w=124, h=54, t='n = 50', sub='the naive test', tone='sig'),
                dict(x=418, y=150, w=124, h=54, t='n = 1', sub='the honest count', tone='mem'),
                dict(x=568, y=56, w=118, h=54, t='SE too small', sub='by 2 to 5 times', tone='sig'),
                dict(x=568, y=150, w=118, h=54, t='delta method', sub='or cluster SE', tone='mem'),
            ],
            links=[dict(a=0, b=1), dict(a=0, b=2), dict(a=0, b=3), dict(a=0, b=4), dict(a=0, b=5),
                   dict(a=1, b=6, tone='sig'), dict(a=5, b=7, tone='mem'),
                   dict(a=6, b=8, tone='sig'), dict(a=7, b=9, tone='mem')],
            labels=[dict(x=34, y=18, t='randomisation unit', a='start', tone='mem', op=0.85),
                    dict(x=686, y=18, t='analysis unit', a='end', tone='sig', op=0.85)],
            foot='the rows multiply, the evidence does not',
            alt='One randomised user fanning out into fifty session rows, with the naive test '
                'reading fifty independent observations while the honest count is one user, and '
                'the resulting standard error too small by two to five times'),
        caption=('One coin flip on the left, fifty rows on the right. The naive test reads that '
                 'right-hand column as fifty independent observations; the delta method and '
                 'cluster-robust errors read it as one user with fifty correlated draws. Between '
                 'those two readings sits a standard error wrong by two to five times, and every '
                 'A/A failure you could not explain.'),
        caption_simple=('The person on the left was assigned once. On the right that same person '
                        'becomes fifty rows in the table. A test that counts rows thinks it has '
                        'fifty times more evidence than it really has, and that is where the '
                        'false wins come from.'),
        when=[
            'You randomised by user and the analysis table has one row per session, query or impression',
            'Your A/A tests come back significant far more often than one time in twenty',
            'A B2B experiment randomised by account and scored per seat',
            'Someone reports clicks per impression and calls the sample size the number of impressions',
        ],
        trap=('Computing total clicks divided by total impressions and running a two-proportion '
              'test with the number of impressions as $n$. It is the single most common invalid '
              'test in production analytics. The sentence that carries it is <i>"we have 2 '
              'million rows, so we have plenty of power"</i> &mdash; you have 40,000 users. The '
              'near-miss version is worth knowing too: candidates who sense the standard error is '
              'wrong often reach for the bootstrap and then resample rows, which reproduces '
              'exactly the same understatement with more machinery on top.'),
        real=('Microsoft&rsquo;s experimentation group published specifically on why '
              'tenant-randomised A/B tests are hard and why tenant pairing often fails &mdash; '
              'the B2B version of this problem, where you hold <b>hundreds</b> of clusters '
              'instead of millions of users and the design effect eats the experiment alive. On '
              'the fix side, the delta method and the cluster-robust variance estimator have been '
              'shown to be formally equivalent for clustered randomised experiments, so there is '
              'no argument to have about which one to use. The magnitude to quote is the naive '
              'standard error understated by a factor of <b>two to five</b>.'),
        drills=[
            dict(q='Would clicks-per-user and clicks-per-impression give you the same conclusion?',
                 a=('<b>Not necessarily, and when they disagree that is the finding.</b> They are '
                    'different estimands. A treatment that shows fewer, better-targeted results '
                    'can raise clicks per impression while cutting impressions enough that clicks '
                    'per user falls: the rate improves and the total drops. Clicks per user is an '
                    'average over the randomisation unit, so its standard error is '
                    'straightforward. Clicks per impression is a ratio of averages over a unit '
                    'you did not randomise and needs the delta method. The follow-up is always '
                    '"which is the OEC", and the answer is whichever matches what the business is '
                    'buying &mdash; usually the per-user total, with the rate as a diagnostic.'),
                 a_simple=('<b>Not necessarily, and when they disagree that is the finding.</b> '
                           'They answer different questions. A change that shows fewer but better '
                           'results can lift the click rate while cutting the number of chances '
                           'to click, so the rate goes up and the clicks per person go down. '
                           'Clicks per person is measured on the same unit you randomised, so it '
                           'is the safer number. The rate is measured on a unit you did not '
                           'randomise, so it needs the careful method. Then pick whichever one '
                           'the business is actually paying for.')),
            dict(q='Your A/A tests are significant far more often than they should be. What do you check first?',
                 a=('<b>The analysis unit, before anything else.</b> An A/A test is a pure test '
                    'of your variance estimate, and the commonest way to break it is to randomise '
                    'on one unit and compute standard errors on another. Confirm the ratio is '
                    'clean first, then recompute the same metric with cluster-robust errors on '
                    'the randomisation unit; if the false positive rate falls back to nominal, '
                    'that was it. Only afterwards would I look at peeking, a shared cache, or a '
                    'leaky assignment service, which produce the same symptom for different '
                    'reasons.'),
                 a_simple=('<b>The unit you counted, before anything else.</b> A test of a change '
                           'against itself is a direct check on your error bars, and the usual '
                           'way they break is that you assigned by person and then counted rows. '
                           'Redo the same number with a method that groups the rows by person; if '
                           'the false alarms fall back to about one in twenty, that was the '
                           'cause. Only then look at repeated peeking, a shared cache, or a '
                           'broken assignment service, which cause the same symptom for '
                           'different reasons.')),
            dict(q='Give me the two valid ways to get a standard error here, and say which estimand each one gives you.',
                 a=('<b>Delta method or cluster-robust errors for the ratio of averages; a '
                    'per-user t-test for the average of ratios.</b> Delta method and clustering '
                    'on the randomisation unit are provably equivalent for clustered randomised '
                    'experiments, and both estimate $\\mathbb{E}[X] / \\mathbb{E}[Y]$ &mdash; '
                    'total clicks over total impressions, where a heavy user carries more weight. '
                    'Collapsing to one ratio per user and running a t-test estimates '
                    '$\\mathbb{E}[X/Y]$ &mdash; every user counted once, whatever their volume. '
                    'Neither is more correct. They answer different questions, and a treatment '
                    'that changes activity levels can move them in opposite directions, so choose '
                    'before you look.'),
                 a_simple=('<b>Either group the rows by person when you compute the error bars, '
                           'or collapse each person to one number and compare those.</b> The '
                           'first keeps the overall rate, in which your heaviest users count for '
                           'more because they generated more rows. The second gives every person '
                           'one vote regardless of how much they did. Both are legitimate, and '
                           'they can point in different directions when a change alters how '
                           'active people are. Pick the one that matches the business question, '
                           'and pick it before you see the result.')),
        ],
        anchor=dict(
            formula=r'$\operatorname{Var}(\bar{X}/\bar{Y})$ by the delta method &nbsp;&middot;&nbsp; every moment computed over users, never over events',
            formula_simple='Your sample size is the number of coin flips, not the number of rows '
                           'in the table.',
            bullets=[
                'Correlated rows inside one user shrink the standard error, often by a factor of two to five',
                'Delta method and cluster-robust errors are equivalent here &mdash; use either, and cluster on the randomisation unit',
                'Aggregating per user is also valid but changes the estimand, so say which one the business wants',
            ]),
        chips=['delta method', 'cluster-robust standard errors', 'design effect', 'A/A test',
               'OEC'],
        followup='Would clicks-per-user and clicks-per-impression give you the same conclusion?',
    ),

    # ------------------------------------------------------------------ 4
    dict(
        id='interference',
        tier='production',
        title='Interference: when SUTVA breaks',
        kicker='A/B testing assumes my treatment does not touch you &mdash; which is false in every marketplace and every social product',
        simple=[
            'The whole logic of an A/B test is that control shows you what would have happened '
            'without the change. That holds only if treating me leaves you exactly as you were, '
            'and in a marketplace it does not. If the treatment makes its users book faster, the '
            'rooms they take are rooms control can no longer take. Control gets worse because '
            'treatment got better, and the gap between them is wider than anything you could '
            'ship.',
            'The same happens wherever something is shared: a social product where treated users '
            'message untreated ones, a shared advertising budget, shared stock, a model retrained '
            'on treated traffic. The direction is predictable, which is the useful part &mdash; '
            'in a marketplace the measured lift overstates the global effect, because part of it '
            'was moved rather than made.',
            'The fix is to randomise something bigger than a person: whole cities, whole social '
            'neighbourhoods, whole slices of time, so the leakage happens inside a unit instead '
            'of between units. The bill arrives as power &mdash; your effective sample size '
            'becomes the number of clusters, not the number of people in them, so millions of '
            'users become a few dozen cities.',
        ],
        analogy=('<b>Like testing a shortcut on half the traffic.</b> The new route looks superb '
                 '&mdash; partly because it is, and partly because everyone using it has stopped '
                 'queueing on the old road. Open it to everybody and the queue returns. To '
                 'measure it honestly you switch the whole city on alternate days: a handful of '
                 'days instead of thousands of cars.'),
        trap_simple=('Saying "network effects" and stopping there. The interviewer already knows '
                     'there are network effects &mdash; that is why they asked. They want three '
                     'specific things: which design you would switch to, which way the bias runs '
                     'if you do not, and how much power the switch costs you. Naming the '
                     'phenomenon without naming the design is the clearest signal in the whole '
                     'loop that you have read about experiments rather than run them.'),
        tech=[
            'SUTVA requires no interference between units: my potential outcome must not depend '
            'on your assignment. It is violated by two-sided marketplaces (treatment consumes '
            'shared supply), social graphs (treated users expose untreated ones), shared budgets '
            'and inventory, and any shared model retrained on treated traffic. In a marketplace '
            'the bias is signed rather than random &mdash; treatment takes supply from control, '
            'so the contrast is inflated at both ends and the estimate overstates the global '
            'effect. On a social graph the sign depends on the mechanism, and the design question '
            'is whether the value of the feature depends on your contacts having it too.',
            'Name the designs. <b>Cluster randomisation</b> over geographies or markets. '
            '<b>Ego-cluster randomisation</b>, LinkedIn&rsquo;s answer, which assigns a user '
            'together with their immediate neighbourhood so a treated user&rsquo;s contacts are '
            'treated too. <b>Switchback</b> or time-split designs, where the whole market flips '
            'between arms on a schedule &mdash; DoorDash, Uber and Lyft. <b>Budget-split</b> for '
            'ad auctions. Then quantify in the same breath, because that is what separates the '
            'answers: the effective sample size is the number of clusters, so the MDE grows by '
            'roughly $\\sqrt{\\text{users}/\\text{clusters}}$ times the design effect. Four '
            'million users spread over forty cities gives you forty independent observations, and '
            'every sizing conversation has to start from forty.',
        ],
        tech_note=('Switchback has a parameter of its own, and it is the one that gets asked '
                   'about: the length of the time slot. Too short and treatment carries over into '
                   'the slot that follows, contaminating the next arm; too long and you have very '
                   'few slots and no power left. Bojinov and Simchi-Levi treat this as an optimal '
                   'design problem rather than a rule of thumb. Note also that none of these '
                   'designs is retrofittable &mdash; you cannot cluster an experiment after it '
                   'has already run at the user level.'),
        math=dict(
            tex=r'n_{\text{eff}} = \frac{n}{1 + (m-1)\rho_{\text{ICC}}} \qquad \text{MDE} \;\propto\; \sqrt{\frac{\text{users}}{\text{clusters}}} \times \text{design effect}',
            note='The first term is why cluster randomisation is expensive; the second is the '
                 'sentence to say out loud when you propose it. Both assume the clusters '
                 'themselves are exchangeable, which for cities is a claim you have to defend.',
            cost='you trade a biased estimate of the wrong thing for a noisy estimate of the right one'),
        code=dict(
            label='What forty cities cost you',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
                 'users, clusters, icc = <span class="s">4_000_000</span>, <span class="s">40</span>, <span class="s">0.02</span>\n'
                 'm = users / clusters                <span class="c"># 100,000 users per city</span>\n'
                 'deff = <span class="s">1</span> + (m - <span class="s">1</span>) * icc   <span class="c"># design effect ~ 2001</span>\n\n'
                 '<span class="k">print</span>(users / deff)                <span class="c"># effective n ~ 2,000</span>\n'
                 '<span class="k">print</span>(np.sqrt(deff))               <span class="c"># MDE inflated ~45x</span>\n\n'
                 '<span class="c"># icc is an assumption, so say it out loud and sanity-check it</span>\n'
                 '<span class="c"># against last quarter. the number to quote is 40, not 4,000,000</span>')),
        fig=dict(
            kind='blocks', h=256,
            boxes=[
                dict(x=34, y=40, w=160, h=56, t='treatment 50%', sub='converts faster', tone='sig'),
                dict(x=252, y=100, w=170, h=58, t='shared supply',
                     sub='one pool of inventory', tone='plain'),
                dict(x=34, y=164, w=160, h=56, t='control 50%',
                     sub='your counterfactual', tone='mem'),
                dict(x=478, y=40, w=208, h=56, t='measured lift +6%',
                     sub='part of it was transferred', tone='sig'),
                dict(x=478, y=164, w=208, h=56, t='effect at 100% rollout',
                     sub='nobody left to take from', tone='mem'),
            ],
            links=[dict(a=0, b=1, tone='sig', label='takes supply'),
                   dict(a=1, b=2, side='left', tone='sig', label='starves control'),
                   dict(a=1, b=3, tone='sig'),
                   dict(a=1, b=4, tone='mem')],
            labels=[dict(x=34, y=18, t='SUTVA assumes these are independent', a='start',
                         tone='mem', op=0.8),
                    dict(x=686, y=18, t='they share one pool', a='end', tone='sig', op=0.85)],
            foot='randomise cities, ego-networks or time slots, and the transfer happens inside a unit',
            alt='Treatment and control both drawing on a single shared supply pool, so treatment '
                'consumes what control would have had, producing an overstated measured lift on '
                'one side and a much smaller effect at full rollout on the other'),
        caption=('Treatment and control are not two separate experiments; they are two halves of '
                 'one system drawing on the same pool. Whatever treatment consumes, control does '
                 'not get, so part of the measured gap is a transfer between arms rather than '
                 'value created. At full rollout there is nobody left to take it from.'),
        caption_simple=('The two groups are not independent &mdash; they are drawing from the '
                        'same pot. Anything the treated half takes is something the control half '
                        'does not get, so part of the difference you measured is a transfer '
                        'rather than a gain. Ship it to everyone and there is nobody left to '
                        'take from.'),
        when=[
            'A two-sided marketplace: riders and drivers, guests and hosts, buyers and sellers',
            'A social or messaging feature that treated users can put in front of untreated ones',
            'Shared inventory, a shared ads budget, or a model retrained on treated traffic',
            'The A/B result was strong and the full launch delivered a fraction of it',
        ],
        trap=('Saying "there are network effects here" and stopping. It names the phenomenon and '
              'answers none of the question. The interviewer is waiting for three things and will '
              'not prompt you for them: the design (cluster, ego-cluster, switchback, '
              'budget-split), the direction of the bias (in a marketplace treatment steals '
              'supply, so the lift is overstated), and the power cost (effective sample size is '
              'the number of clusters). The second-order trap is proposing a switchback for a '
              'social product &mdash; time-splitting works because the market state resets '
              'between slots, and a social graph does not reset.'),
        real=('LinkedIn built <b>ego-cluster randomisation</b> for exactly this: assign a user '
              'and their immediate network together so spillover lands inside a cluster '
              '(Saint-Jacques et al., arXiv:1903.08755, 2019, with a 2023 rebuild of the cluster '
              'construction in arXiv:2308.05945). DoorDash runs a production <b>switchback</b> '
              'framework for marketplace tests, and Lyft published a marginal-values approach to '
              'correcting interference bias directly. The number that decides whether you can '
              'afford any of it: your effective sample size falls from <b>millions of users to '
              'tens of clusters</b>, or a few hundred time slots.'),
        drills=[
            dict(q='Independence between units is violated because of the social graph. Walk me through the design you would use and what it costs you.',
                 a=('<b>Ego-cluster randomisation, and it costs me almost all of my effective '
                    'sample size.</b> Partition the graph so each unit is a user plus their '
                    'immediate neighbourhood, assign whole ego-clusters rather than individuals, '
                    'and analyse at the cluster level with cluster-robust errors. That is '
                    'LinkedIn&rsquo;s design, and the point is that a treated user&rsquo;s '
                    'contacts are treated too, so spillover stays inside the unit. The cost is '
                    'that $n$ becomes the number of clusters and the MDE scales with '
                    '$\\sqrt{\\text{users}/\\text{clusters}}$ times the design effect. If the '
                    'effect turns out not to be graph-mediated at all, user randomisation with a '
                    'guardrail on cross-arm contact is far cheaper.'),
                 a_simple=('<b>Randomise whole friendship neighbourhoods instead of individual '
                           'people, and accept that it costs almost all of my statistical '
                           'power.</b> Each unit becomes a person plus the people they interact '
                           'with, assigned together, so the spillover happens inside a unit '
                           'rather than crossing between the two groups. That is what LinkedIn '
                           'does. The bill is that my sample size becomes the number of '
                           'neighbourhoods rather than the number of people, so the smallest '
                           'effect I can detect gets much bigger. Before paying that, I would '
                           'check whether the effect actually travels along the graph at all.')),
            dict(q='Bookings were up 6% in the experiment and up 1% after full launch. Which explanation is the marketplace-specific one, and how would you have caught it beforehand?',
                 a=('<b>Supply cannibalisation &mdash; treatment was taking inventory from '
                    'control, and at 100% there is nobody left to take it from.</b> The signature '
                    'is that the arms move as mirror images on the shared resource: control got '
                    'worse in absolute terms during the test, not merely worse relative to '
                    'treatment. That is how you separate it from the winner&rsquo;s curse, '
                    'novelty decay and a shifted launch population, which do not touch '
                    'control&rsquo;s own level. You catch it beforehand with a geo-cluster or '
                    'switchback design &mdash; a decision you make before the experiment, not '
                    'after the launch disappoints.'),
                 a_simple=('<b>The treated half was taking inventory from the untreated half, and '
                           'once everyone has the feature there is nobody left to take from.</b> '
                           'The giveaway is that the control side got worse in absolute terms '
                           'during the test, not just worse compared with treatment &mdash; the '
                           'two sides move as mirror images. It is not the only candidate &mdash; '
                           'a winning result is overstated anyway, novelty fades, and the launch '
                           'audience is not the test audience &mdash; but it is the one specific '
                           'to a marketplace, and you rule it out by randomising cities or time '
                           'slots rather than people.')),
            dict(q='You propose cluster randomisation over 40 cities instead of 4 million users. What happens to your minimum detectable effect?',
                 a=('<b>It is set by 40 now, not by 4 million.</b> The effective sample size is '
                    'the number of clusters, so the MDE grows by roughly '
                    '$\\sqrt{\\text{users}/\\text{clusters}}$ times the design effect &mdash; and '
                    'with 100,000 users per city even a small intra-cluster correlation makes '
                    'that design effect enormous. You are not detecting a 0.5% lift this way. So '
                    'either the effect is large, or you move to a switchback and buy hundreds of '
                    'time slots instead of dozens of cities, or you pair similar cities and '
                    'analyse within pairs.'),
                 a_simple=('<b>It is decided by 40, not by 4 million.</b> Once you assign whole '
                           'cities, a city is your unit of evidence, so you have forty '
                           'observations however many people live in them &mdash; and cities '
                           'differ from each other for a hundred reasons that have nothing to do '
                           'with your change. The smallest effect you can detect gets much '
                           'larger. So either the effect is big, or you switch to time slots and '
                           'get hundreds of units instead of dozens, or you pair similar cities '
                           'and compare within pairs.')),
        ],
        anchor=dict(
            formula=r'effective $n$ = number of clusters &nbsp;&middot;&nbsp; $\text{MDE} \propto \sqrt{\text{users}/\text{clusters}} \times \text{design effect}$',
            formula_simple='Randomise something big enough that the spillover happens inside it '
                           '&mdash; then count your clusters, not your people.',
            bullets=[
                'In a marketplace, treatment takes supply from control, so the measured lift overstates the global effect',
                'Name the design &mdash; cluster, ego-cluster, switchback, budget-split &mdash; not the phenomenon',
                'The bill is power: your effective sample size is the number of clusters, not the people inside them',
            ]),
        chips=['SUTVA', 'switchback design', 'ego-cluster randomisation', 'design effect',
               'geo experiments'],
        followup='Independence between units is violated because of the social graph. Walk me through the design you would use and what it costs you.',
    ),

    # ------------------------------------------------------------------ 5
    dict(
        id='novelty-effects',
        tier='production',
        title='Novelty, primacy and long-term effects',
        kicker='The two-week experiment measures the two-week effect, and for anything users have to learn that is not what you are shipping',
        simple=[
            'The first four days of an experiment lie, and they lie in both directions. Some '
            'changes get a burst of attention purely because they are new: people poke the new '
            'button, the numbers spike, and the spike decays to nothing over a fortnight. That is '
            'novelty. Other changes make things briefly worse because people knew where '
            'everything used to be; the deficit fades as they relearn, so the real effect is '
            'bigger than what you measured. That is primacy. One problem underneath both: the '
            'effect is moving, and you averaged over the steepest part of the curve.',
            'You diagnose it by plotting the effect against days since a user first saw the '
            'change &mdash; not calendar day, because new users keep arriving and blur it &mdash; '
            'and by splitting new users from returning ones. A line that decays or climbs is your '
            'answer; a flat line is permission to trust the average. What you cannot do is simply '
            'run it longer. Google measured a learning half-life of about sixty days, so even a '
            'ninety-day study captures around two thirds of the effect, and eight weeks instead '
            'of two costs four times the calendar without getting there. Keep a slice of users '
            'out of the launch for a quarter instead.',
        ],
        analogy=('<b>Like judging a restaurant on its opening week.</b> Half the queue is there '
                 'because it is new, the kitchen is still finding its rhythm, and neither of '
                 'those tells you what dinner will be like in March. The honest read comes from '
                 'going back in three months, or from keeping a few regulars who never went in '
                 'week one and asking them instead.'),
        trap_simple=('Blaming the whole shortfall on novelty. It is the flattering explanation '
                     'and usually only part of the story. A winning result is overstated on '
                     'average simply because you picked it for winning; the population at full '
                     'launch is not the population in the experiment; spillover between the two '
                     'groups disappears once everyone has the feature; and the season changed. '
                     'All five produce the same shape. Naming one of five candidates without '
                     'saying how you would tell them apart is exactly the answer the interviewer '
                     'is listening for.'),
        tech=[
            'Novelty and primacy are one phenomenon with opposite signs: a treatment effect that '
            'varies with time since exposure. Novelty decays a lift towards zero; primacy hides '
            'an effect that is really there. Diagnose by plotting the effect against days since '
            'first exposure rather than calendar day &mdash; calendar day mixes cohorts, since a '
            'user who joined on day 12 has had two days of exposure while a day-1 user has had '
            'thirteen &mdash; and by splitting new from returning users, because novelty is '
            'largely a returning-user phenomenon.',
            'The long-run designs, by name: a <b>long-term holdback</b>, keeping 1% of users in '
            'control for a quarter after launch; <b>cookie-cookie-day randomisation</b>, '
            're-randomising cookies daily so no cookie ever accumulates learning and you get an '
            'unlearned baseline to difference against; staged rollouts; and post-launch holdouts. '
            'Google&rsquo;s ads-blindness work put the learning half-life at about <b>60 days</b>, '
            'so a 90-day study captures roughly <b>65%</b> of the total effect and a two-week test '
            'captures almost none of it. The headline result is the one to quote: a <b>50%</b> cut '
            'in mobile search ad load produced significant short-term revenue-per-mille losses '
            'with long-term effects settling near zero &mdash; the two-week readout would have '
            'killed a change that was long-run neutral and clearly better for users.',
        ],
        tech_note=('Cookie-cookie-day is the design worth understanding rather than just naming. '
                   'Re-randomising cookies every day means no cookie ever accumulates experience '
                   'with the treatment, so that arm measures the effect on a permanently '
                   'unlearned user. Differencing it against a stably assigned arm isolates the '
                   'learned component directly, instead of inferring it from the slope of a decay '
                   'curve you may not have run long enough to see. It also tells you whether a '
                   'flat two-week curve was flat because there was nothing to learn, or because '
                   'you stopped watching too soon.'),
        math=dict(
            tex=r'\tau(t)\ \ \text{not}\ \ \tau \qquad t_{1/2} \approx 60\ \text{days} \;\Rightarrow\; 1 - e^{-\ln 2 \cdot 90/60} \approx 65\%\ \text{captured in 90 days}',
            note='What you ship is the limit of $\\tau(t)$ as $t$ grows; what a fixed-horizon '
                 'experiment estimates is the average of $\\tau$ over its window. Those coincide '
                 'only when $\\tau$ is flat, which is the thing you were supposed to check.',
            cost='assumes exponential learning and a stable population'),
        code=dict(
            label='Effect by day since first exposure, not calendar day',
            cost='pandas',
            src=('<span class="c"># calendar day mixes cohorts: someone who joined on day 12 has had</span>\n'
                 '<span class="c"># 2 days of exposure while a day-1 user has had 13</span>\n'
                 'df[<span class="s">"exposure_day"</span>] = (df.date - df.first_seen).dt.days\n\n'
                 'curve = (df.groupby([<span class="s">"exposure_day"</span>, <span class="s">"arm"</span>])\n'
                 '           .metric.mean().unstack())\n'
                 '<span class="k">print</span>((curve.treatment - curve.control).head(<span class="s">14</span>))\n\n'
                 '<span class="c"># day 0  +0.031     day 6  +0.021     day 13  +0.013</span>\n'
                 '<span class="c"># still falling on day 13 -&gt; the two-week mean is not the effect</span>\n'
                 '<span class="c"># split by cohort too: novelty lives with the returning users</span>')),
        fig=dict(
            kind='plot', xr=(0, 90), yr=(-0.2, 3.4), ph=190,
            head=['WHAT YOU MEASURED', 'WHAT YOU SHIP'],
            xlab='days since a user first saw the change', ylab='measured treatment effect',
            xticks=[(0, '0'), (14, '14'), (30, '30'), (60, '60'), (90, '90')],
            yticks=[(0, '0'), (1, '+1%'), (2, '+2%'), (3, '+3%')],
            bands=[dict(x0=0, x1=14, tone='sig', label='you measured here', op=0.12)],
            hlines=[dict(y=2.05, tone='sig', label='the two-week readout'),
                    dict(y=0.16, tone='mem', label='the long-run effect')],
            curves=[dict(pts=[(0, 3.00), (3, 2.51), (7, 1.99), (14, 1.34), (21, 0.92),
                              (30, 0.59), (45, 0.32), (60, 0.22), (90, 0.16)],
                         tone='sig', label='effect by day since first exposure',
                         lat=3, dx=12, dy=-12)],
            marks=[dict(x=0, y=3.00, label='+3.0% on day 1', tone='sig', dx=10, dy=-8),
                   dict(x=90, y=0.16, label='+0.2%', tone='mem', la='end', dx=-8, dy=-12)],
            foot='every point on the curve is honest -- and a fortnight averages over the steepest part of it',
            alt='A treatment effect plotted against days since first exposure, starting at three '
                'per cent on day one and decaying to roughly nothing by day ninety, with the '
                'first fourteen days shaded to show the window a two-week test averages over'),
        caption=('One experiment, plotted honestly. Every point is a correct measurement of the '
                 'effect on a user who has had that many days with the change, and the two-week '
                 'readout is the average over the steepest part of it. The number you ship is the '
                 'right-hand end, not the shaded box.'),
        caption_simple=('This is one experiment, measured properly. Each point is the real effect '
                        'on someone who has had the change for that many days. The two-week '
                        'result is an average taken over the part where the line is falling '
                        'fastest, so it reports something far larger than what you will actually '
                        'get.'),
        when=[
            'A launch decision on anything users have to learn: a redesign, new navigation, a changed default',
            'The lift was strong in week one and half of it was gone by week three',
            'A PM asks whether two weeks is long enough',
            'The experiment won and the full launch delivered a fraction of it',
        ],
        trap=('Two of them. The first is <i>"the effect declined after launch because of '
              'novelty"</i> offered as a complete answer &mdash; it is one of five candidates, '
              'alongside the winner&rsquo;s curse, a launch population that differs from the '
              'experiment population, interference that vanishes at 100% allocation, and '
              'seasonality, and you are being graded on whether you can separate them. The second '
              'is <i>"fine, we will run it for eight weeks"</i>: four times the calendar for a '
              'study that still sits well inside a 60-day half-life. A 1% holdback held for a '
              'quarter costs almost nothing and answers the question properly.'),
        real=('Hohnhold, O&rsquo;Brien and Tang, <i>Focusing on the Long-term: It&rsquo;s Good '
              'for Users and Business</i> (Google, KDD 2015). They measured ads-blindness '
              'learning with a half-life of about <b>60 days</b>, meaning a 90-day study captures '
              'roughly <b>65%</b> of the effect and a two-week test captures almost none. The '
              'result that justified the whole programme: cutting mobile search ad load by '
              '<b>50%</b> produced significant short-term revenue-per-mille losses and long-term '
              'effects that settled near zero. A fixed two-week experiment would have killed a '
              'change that turned out to be long-run neutral and clearly better for users.'),
        drills=[
            dict(q='Why did the effect decline after full launch?',
                 a=('<b>Five candidates, and novelty is only one of them.</b> The winner&rsquo;s '
                    'curse first, because you selected this experiment for winning and selected '
                    'estimates run <b>20&ndash;50%</b> high. Then novelty decay. Then a launch '
                    'population that differs from the experiment population, especially if the '
                    'test was triggered on a narrower set of users. Then interference that '
                    'disappears at 100% allocation. Then seasonality or an instrumentation change '
                    'made at launch. You separate them with evidence, not argument: plot the '
                    'effect by day since exposure for novelty, compare the two populations on '
                    'their pre-period metrics, check whether control moved in absolute terms '
                    'during the test, and hold back 1% to measure the remainder honestly.'),
                 a_simple=('<b>Five explanations, and novelty is only one of them.</b> First, you '
                           'chose this experiment because it won, and winners are overstated on '
                           'average &mdash; shipped effects typically shrink by a fifth to a '
                           'half. Then novelty wearing off. Then a launch audience that is not '
                           'the test audience. Then spillover between the groups that disappears '
                           'once everyone has the feature. Then the season changing, or the '
                           'tracking changing at launch. You tell them apart with evidence: plot '
                           'the effect against how long each person has had the change, compare '
                           'the two audiences on what they did beforehand, and keep a small group '
                           'out of the launch to measure against.')),
            dict(q='The lift is +3% in week one and +0.6% in week three. Do you ship?',
                 a=('<b>Not on that evidence &mdash; you do not yet have a number to ship.</b> '
                    'The curve is still falling, so neither week is the long-run effect and the '
                    'two-week average is certainly not. Replot by days since first exposure and '
                    'split new from returning: if the decay is confined to returning users it is '
                    'novelty, and if new users sit flat near 0.6% that is closer to your '
                    'estimate. The decision is not ship or kill. Launch with a 1% holdback and '
                    'read the honest effect off the holdback in a quarter &mdash; if the change '
                    'is cheap to reverse that beats both extending the test and guessing at the '
                    'asymptote.'),
                 a_simple=('<b>Not yet &mdash; you do not have the number you would be '
                           'shipping.</b> The line is still falling, so neither week is the true '
                           'effect and the average of the two is not either. Redraw it against '
                           'how many days each person has had the change, and separate people who '
                           'were already users from people who arrived during the test. If only '
                           'the existing users are fading, that is novelty; if the newcomers sit '
                           'steady at the lower figure, that is closer to the truth. The real '
                           'decision is neither ship nor kill: launch it, keep one user in a '
                           'hundred out of the launch, and read the honest answer off them in '
                           'three months.')),
            dict(q='Your PM says run it for eight weeks instead of two, to be safe. Respond.',
                 a=('<b>Eight weeks buys four times the calendar and still does not reach the '
                    'timescale.</b> Against a 60-day half-life you are barely one half-life in, '
                    'so you capture a minority of the learning and pay a whole quarter of roadmap '
                    'for it. The cheaper design does the job properly: launch to 99%, hold 1% in '
                    'control for a quarter, and read the long-run effect off the holdback while '
                    'the feature is already earning. If the worry is specifically learning rather '
                    'than duration, cookie-cookie-day randomisation gives you a permanently '
                    'unlearned arm to difference against, which measures the learning instead of '
                    'waiting it out.'),
                 a_simple=('<b>Eight weeks costs four times the calendar and still does not get '
                           'there.</b> The learning it is meant to capture takes about sixty days '
                           'to half-fade, so two months of testing catches a minority of it and '
                           'you have spent a quarter of the year finding that out. The cheap '
                           'version does the job better: ship it to nearly everyone, keep one '
                           'user in a hundred out of the launch for three months, and measure '
                           'against them. The feature earns money the whole time, and you get an '
                           'honest long-run answer instead of a longer short-run one.')),
        ],
        anchor=dict(
            formula=r'$\tau(t)$, not $\tau$ &nbsp;&middot;&nbsp; half-life $\approx 60$ days, so 90 days captures $\sim$65%',
            formula_simple='Plot the effect against days since a person first saw the change. If '
                           'the line is still moving, you do not have your number yet.',
            bullets=[
                'Novelty decays a lift towards nothing; primacy hides one that is really there',
                'Plot by day since first exposure, not calendar day, and split new users from returning ones',
                'Running longer is the expensive answer &mdash; a 1% holdback held for a quarter is the cheap one',
            ]),
        chips=['long-term holdback', 'cookie-cookie-day randomisation', 'winner&rsquo;s curse',
               'regression to the mean', 'staged rollout'],
        followup='Why did the effect decline after full launch?',
    ),
]
