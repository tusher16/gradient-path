CARDS = [

# ----------------------------------------------------------------- 1
dict(
    id='which-test',
    tier='core',
    title='Which test, and when the standard choice is wrong',
    kicker='Naming the test is table stakes &mdash; naming the assumption that is about to break is the answer',
    simple=[
        'Choosing a test is not a lookup. Three questions get you there, in this order. First: what '
        'is a single row? If one person can generate fifty rows, you do not have fifty independent '
        'pieces of evidence, and any test that counts rows will hand you a range far too narrow. '
        'Second: are you comparing two averages, two rates, or two whole shapes? Third: is the same '
        'unit measured in both arms &mdash; the same eval questions put to both models, the same '
        'users seen before and after? If so, pair them. Pairing takes the differences between units '
        'out of the noise and is usually the largest free win available.',
        'Only after those three does the name of the test matter. And when a standard choice does go '
        'wrong it is almost never because the data are not bell-shaped. It is because the test '
        'quietly answers a different question from the one the business asked, or because at '
        'production scale it fires every single day.',
    ],
    analogy=('<b>Like a drawer of measuring instruments.</b> A kitchen scale, a tape measure and a '
             'thermometer all give you a confident number, and only one of them answers the question '
             'you asked. Swapping to the fashionable instrument because the last one looked '
             'unfamiliar is how you end up weighing a room and reporting it in degrees.'),
    trap_simple=('Saying you will use the rank-based test because the data are not bell-shaped, and '
                 'then reporting the change in the average. The rank test asks whether one group '
                 'tends to come out ahead of the other, which is not a question about averages at '
                 'all. You have answered something else and put it in the revenue slide.'),
    tech=[
        'Welch is the default two-sample test, not Student&rsquo;s. Welch drops the equal-variance '
        'assumption and costs a fraction of a degree of freedom when variances really are equal, so '
        'the pooled $t$ is the choice that needs defending. Use a two-proportion $z$-test only when '
        'every user contributes exactly one observation; the moment users generate many events you '
        'need clustered standard errors or the delta method, or your $n$ is impressions when it '
        'should be users. Chi-square for contingency tables and for SRM checks, Fisher&rsquo;s exact '
        'once expected cell counts drop below about 5. Pair wherever the design is paired.',
        'Two standard choices go wrong in ways interviewers probe. Mann&ndash;Whitney tests '
        'stochastic dominance &mdash; whether one draw tends to beat the other &mdash; not a '
        'difference in means, so the lift you report from it is not the lift finance will book. And '
        'the KS test as a production drift alarm collapses at scale: the p-value of any '
        'goodness-of-fit test goes to zero as $n$ grows for <i>any</i> non-zero difference, so at 10 '
        'million rows every trivial shift is $p &lt; 0.001$. Swap to an effect size &mdash; PSI with '
        'the usual bands, under 0.1 stable, 0.1&ndash;0.25 moderate, above 0.25 a real shift &mdash; '
        'or subsample to a fixed $n$ before testing so the alarm keeps a constant sensitivity.',
    ],
    tech_note=('Normality is the question candidates over-index on. It is the sampling distribution '
               'of the mean that needs to be roughly normal, not the data, and how quickly that '
               'happens depends on skewness &mdash; Kohavi&rsquo;s rule of thumb is about $355 s^2$ '
               'users per arm, where $s$ is the skewness coefficient. Running Shapiro&ndash;Wilk on '
               '100k rows to decide is worse than useless: at that $n$ it always rejects.'),
    fig=dict(
        kind='tree', h=406, nw=150,
        head=['WHAT YOU OBSERVE', 'WHAT YOU RUN'],
        nodes=[
            dict(id='r',  x=360, y=34,  w=210, t='what are you comparing?'),
            dict(id='A',  x=120, y=108, w=150, t='two means'),
            dict(id='B',  x=360, y=108, w=140, t='two rates'),
            dict(id='C',  x=600, y=108, w=170, t='two distributions'),
            dict(id='A1', x=120, y=186, w=185, t='same units in both arms?'),
            dict(id='B1', x=360, y=186, w=170, t='one row per user?'),
            dict(id='C1', x=600, y=186, w=175, t='millions of rows?'),
            dict(id='a1', x=48,  y=268, w=92,  t='paired t',     sub='same eval items',    tone='mem'),
            dict(id='a2', x=178, y=268, w=112, t='Welch',        sub='cap first if skewed', tone='mem'),
            dict(id='b1', x=300, y=268, w=104, t='two-prop z',   sub='one event each',     tone='mem'),
            dict(id='b2', x=422, y=268, w=116, t='delta method', sub='or bootstrap users', tone='mem'),
            dict(id='c1', x=545, y=268, w=108, t='PSI bands',    sub='not a p-value',      tone='mem'),
            dict(id='c2', x=662, y=268, w=104, t='KS is fine',   sub='moderate n only',    tone='mem'),
            dict(id='x',  x=178, y=346, w=170, t='Mann-Whitney',
                 sub='answers a different question', tone='sig'),
        ],
        edges=[
            dict(a='r', b='A'), dict(a='r', b='B'), dict(a='r', b='C'),
            dict(a='A', b='A1'), dict(a='B', b='B1'), dict(a='C', b='C1'),
            dict(a='A1', b='a1', label='yes'), dict(a='A1', b='a2', label='no'),
            dict(a='B1', b='b1', label='yes'), dict(a='B1', b='b2', label='no'),
            dict(a='C1', b='c1', label='yes'), dict(a='C1', b='c2', label='no'),
            dict(a='a2', b='x', label='the trap', tone='sig', dash='4 4'),
        ],
        foot='the first question is not whether the data are normal; it is what a single row actually is',
        alt=('A decision tree running from what you observe to the test you run: two means, two rates '
             'or two distributions at the top, then a question about pairing, about one row per user, '
             'and about scale, ending in six tests, with Mann-Whitney hanging off Welch as the wrong turn.')),
    caption=('Read it top down and it takes four seconds. The two right-hand columns are where '
             'candidates lose the round: users contributing many events turn a two-proportion z-test '
             'into a delta-method problem, and a KS test pointed at production traffic is an alarm '
             'that can only ever be on.'),
    caption_simple=('Read it from the top and you land on the test in four seconds. The two branches '
                    'on the right are where people go wrong: counting events instead of people, and '
                    'using a significance test as a monitoring alarm when it will fire every day.'),
    when=[
        'A PM asks which test you would run and expects a one-word answer',
        'Revenue per user is zero-inflated and heavy-tailed and the team wants a t-test',
        'The drift monitor fires on eight of forty features every morning',
        'Users contribute dozens of events each and someone is about to z-test conversion on impressions',
    ],
    trap=('&ldquo;The data aren&rsquo;t normal, so I&rsquo;ll use Mann&ndash;Whitney&rdquo; &mdash; '
          'followed two sentences later by &ldquo;the treatment lifted revenue per user by 3%&rdquo;. '
          'Mann&ndash;Whitney never estimated that. Two more get said in the same breath: '
          '&ldquo;I used Student&rsquo;s t-test&rdquo;, when Welch is the default and pooling '
          'variances is an assumption you did not have to make; and &ldquo;Shapiro&ndash;Wilk says '
          'non-normal so the t-test is invalid&rdquo; on 100k rows, where the test always rejects and '
          'normality of the raw data was never the requirement in the first place.'),
    math=dict(
        tex=r't_{\text{Welch}}=\frac{\bar{x}_A-\bar{x}_B}{\sqrt{s_A^2/n_A+s_B^2/n_B}}'
            r'\qquad\text{Student pools into one }s^2',
        note='Welch estimates the degrees of freedom from the two variances instead of assuming they '
             'match. When they do match you give up a fraction of a degree of freedom; when they do '
             'not, the pooled version is simply wrong, and unequal arm sizes make it worse.',
        cost='two variances, not one'),
    code=dict(
        label='The same shift, three sample sizes',
        cost='scipy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             '<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n'
             '<span class="k">for</span> n <span class="k">in</span> '
             '(<span class="s">1_000</span>, <span class="s">100_000</span>, <span class="s">10_000_000</span>):\n'
             '    a, b = rng.normal(<span class="s">0</span>, <span class="s">1</span>, n), '
             'rng.normal(<span class="s">0.01</span>, <span class="s">1</span>, n)\n'
             '    <span class="k">print</span>(n, stats.ks_2samp(a, b).pvalue)\n\n'
             '<span class="c"># a shift of 0.01 sd. the same shift every time. nobody would ever care</span>\n'
             '<span class="c">#      1,000  -&gt;  p = 0.11     quiet</span>\n'
             '<span class="c">#    100,000  -&gt;  p = 0.010    fires</span>\n'
             '<span class="c"># 10,000,000  -&gt;  p = 5e-91    screams -- at nothing</span>')),
    real=('Microsoft&rsquo;s Seven Rules of Thumb (Kohavi et al., exp-platform, 2014) exists because '
          'Bing teams kept shipping and killing features on a metric the t-test could not carry. '
          'Revenue per user there has a skewness coefficient of 17.9, and the rule of 355 times '
          'skewness squared puts the normal approximation out of reach until roughly 114,000 users '
          'per arm for 4.4% sensitivity. Capping the metric cut skewness from 18 to 5.3, about an '
          'elevenfold cut in the users required. At 30,000 per arm the fix is not a different test; '
          'it is a capping rule you wrote down first.'),
    drills=[
        dict(q='Your metric is revenue per user, it is zero-inflated and heavy-tailed, and you have '
               '30,000 users per arm. Walk me through the test you would actually run.',
             a=('<b>Welch on a capped metric, and I would say the cap rule out loud before looking at '
                'the data.</b> At Bing-like skewness the raw mean needs six figures per arm, so at '
                '30k the normal approximation is the thing that is broken, not the test. Options in '
                'order: winsorise at a pre-declared percentile and run Welch; or bootstrap the '
                'difference in means at the user level, which needs no distributional assumption; or '
                'decompose into the purchase rate and the mean spend among purchasers and test both, '
                'which also tells you <i>why</i> it moved. Run CUPED on a pre-period covariate first '
                'either way &mdash; halving the variance is worth more than any choice of test.'),
             a_simple=('<b>Cap the extreme values first, then run the ordinary two-group test.</b> '
                       'With a metric where one customer in ten thousand spends a hundred times the '
                       'average, thirty thousand people per arm is not enough for the usual '
                       'arithmetic to behave, so the fix is the metric rather than the test. Decide '
                       'the cap before you look at the results, or you are choosing it to get the '
                       'answer you want. Two alternatives worth naming: resample the users to get a '
                       'range directly, or split the metric into how many people bought and how much '
                       'buyers spent, and test both.')),
        dict(q='Your drift monitor fires on 8 of 40 features every single day. What do you change?',
             a=('<b>Stop alarming on a p-value and alarm on an effect size.</b> Any goodness-of-fit '
                'p-value goes to zero as $n$ grows for any non-zero difference, so at production '
                'volume the KS test is a detector of having lots of rows. Four changes: switch to PSI '
                'with the conventional bands, or Wasserstein, or a quantile-shift check; correct '
                'across the 40 features with Benjamini&ndash;Hochberg rather than testing each at '
                '0.05; move the alarm from input drift towards prediction or performance drift, which '
                'is what you actually care about; and set the threshold from a backtest of historical '
                'days rather than a textbook default.'),
             a_simple=('<b>Alarm on how big the shift is, not on whether it is detectable.</b> With '
                       'millions of rows a day, a difference far too small to matter is still easy to '
                       'detect, so the alarm is really telling you the traffic is large. Replace it '
                       'with a stability score that has agreed bands for small, moderate and real '
                       'shifts, and set the band from a replay of the last few months rather than a '
                       'default. Then check forty features at once means forty chances to be wrong '
                       'each morning, so correct for that too.')),
        dict(q='You ran Shapiro&ndash;Wilk on 100k rows, it rejected, so you switched to '
               'Mann&ndash;Whitney and reported a 3% revenue lift. Two problems.',
             a=('<b>The normality test was the wrong question, and the replacement answers a '
                'different one.</b> Shapiro&ndash;Wilk at $n$ = 100,000 rejects on any real data, and '
                'what the t-test needs is approximate normality of the <i>sampling distribution of '
                'the mean</i>, which large $n$ helps with rather than hurts. Then Mann&ndash;Whitney '
                'tests stochastic dominance, so a 3% mean lift is not what it estimated &mdash; you '
                'have silently changed the estimand from a mean to a ranking, and revenue is a mean. '
                'Welch on a capped metric, or a bootstrap of the difference in means, keeps the '
                'question the business asked.'),
             a_simple=('<b>The normality check was pointless, and the test you swapped to answers a '
                       'different question.</b> With a hundred thousand rows that check rejects on '
                       'any real data, and what the ordinary test actually needs is that the '
                       '<i>average</i> behaves predictably, which more data helps. The rank test then '
                       'asks whether one group tends to beat the other, which is not the same as '
                       'asking how much more money came in &mdash; and money is an average. Cap the '
                       'extremes and use the ordinary test, or resample to get the range.')),
    ],
    anchor=dict(
        formula=r'$t_{\text{Welch}}=\dfrac{\bar{x}_A-\bar{x}_B}{\sqrt{s_A^2/n_A+s_B^2/n_B}}$'
                r' &nbsp;&middot;&nbsp; pool nothing you do not have to',
        formula_simple='Let each group keep its own spread, pair whatever can be paired, and count '
                       'the things you randomised rather than the rows they produced.',
        bullets=[
            'Welch by default; pooled Student&rsquo;s t is the choice that needs an argument',
            'Mann&ndash;Whitney swaps the mean for a ranking &mdash; never report a mean lift from it',
            'At production scale a KS p-value always fires; alarm on PSI or another effect size',
            'One row per user, or clustered errors &mdash; your sample size is what you randomised',
        ]),
    chips=['Welch', 'delta method', 'PSI bands', 'paired designs', 'winsorising'],
    followup='Your metric is revenue per user, it is zero-inflated and heavy-tailed, and you have 30,000 users per arm. Walk me through the test you would actually run.',
),

# ----------------------------------------------------------------- 2
dict(
    id='bootstrap',
    tier='core',
    title='The bootstrap',
    kicker='When there is no formula for the standard error, resampling is the formula &mdash; provided you resample the right thing',
    simple=[
        'You have a number you care about &mdash; a median latency, a win rate, a ratio of two '
        'totals &mdash; and no textbook formula for how much it wobbles. The bootstrap gets you one '
        'anyway. Treat the sample you have as if it were the whole population, deal yourself a fresh '
        'sample of the same size from it at random, allowing repeats, recompute your number, and do '
        'that ten thousand times. The spread of those ten thousand numbers is your uncertainty, and '
        'the middle 95% of them is your interval. No formula, no derivation.',
        'The catch is hiding in the words &ldquo;deal yourself a fresh sample&rdquo;. A sample of '
        'what? If two hundred traces came from twenty users, dealing traces treats twenty people as '
        'two hundred and the interval comes out far too narrow. Deal users. The bootstrap is only as '
        'honest as the unit you resample, and it can never invent information the sample did not '
        'contain &mdash; which is why it struggles in the far tail and at very small sizes.',
    ],
    analogy=('<b>Like a straw poll of your own notebook.</b> You cannot rerun the year, so you '
             'shuffle the days you did record, deal yourself a fresh year out of them, and see how '
             'different the answer comes out. Do that ten thousand times and the range you get back '
             'is an honest picture of how much your single answer could have wobbled.'),
    trap_simple=('Resampling rows when the rows come in groups. Two hundred traces from twenty users '
                 'is twenty independent things, not two hundred, and dealing traces gives an interval '
                 'far tighter than the data can support. The other one is putting an interval around '
                 'the best of twelve options: reshuffling cannot see that the number was picked for '
                 'being the highest.'),
    tech=[
        'Resample $n$ rows with replacement $B$ times, recompute the statistic on each resample, and '
        'read the 2.5th and 97.5th percentiles of the resampled statistics. $B \\geq 1{,}000$ is '
        'enough for a central interval and 10,000 if you are anywhere near a tail. It works for '
        'medians, quantiles, ratios, AUC, win rates, F1 and every LLM eval metric &mdash; anything '
        'where the delta method is painful or the sampling distribution is not something you want to '
        'derive at a whiteboard. Percentile is fine most of the time, BCa corrects bias and skew, and '
        'the smooth bootstrap, which jitters each resample with a kernel, is the recommendation for '
        'small-$n$ eval scores.',
        'Three failure modes, and interviewers ask about all of them. <b>Dependence</b>: resample '
        'clusters, not rows &mdash; users, sessions, documents, conversations &mdash; or you have '
        're-imported the independence assumption you were trying to avoid. <b>The extreme tail</b>: a '
        'resample can only ever contain values you already observed, so an interval on a 99.9th '
        'percentile from a few hundred points is decided by two or three rows, and comes out lumpy '
        'and overconfident. <b>Selection</b>: bootstrapping the maximum of a set you chose by its '
        'maximum gives a tight band around a number that was picked for being lucky, and needs a '
        'max-T correction or, better, a fresh held-out set.',
    ],
    tech_note=('The bootstrap estimates sampling variability and nothing else. If the eval set is '
               'contaminated, the judge model silently upgraded, or the traces came from a week that '
               'was not representative, the interval will be beautifully narrow and centred in the '
               'wrong place. Below roughly 300 items plain standard errors are not trustworthy '
               'either: use a Wilson interval for a pass rate and a smooth bootstrap for continuous '
               'scores.'),
    fig=dict(
        kind='pipeline',
        head=['WHAT YOU RESAMPLE', 'WHAT YOU GET'],
        steps=[
            dict(t='200 traces, 20 users', sub='the real n is 20', tone='sig'),
            dict(t='draw 20 users with replacement', sub='clusters, not rows'),
            dict(t='recompute the median', sub='10,000 times'),
            dict(t='take the middle 95%', sub='that is the interval', tone='mem'),
        ],
        foot='the interval is only ever as honest as the unit you deal out',
        alt=('A four-step pipeline: 200 traces from 20 users, draw 20 users with replacement, '
             'recompute the median ten thousand times, take the middle 95 percent as the interval.')),
    caption=('Every step but the second is mechanical. The second is the whole decision: resample the '
             'unit you randomised. Bootstrapping the 200 traces instead of the 20 users on this data '
             'returns an interval 2.3 times too narrow, and nothing in the output tells you so.'),
    caption_simple=('Three of these four steps are mechanical. The second one is the decision: you '
                    'deal out people, not rows. Dealing rows here gives an interval less than half '
                    'the width it should be, and nothing in the answer warns you.'),
    when=[
        'Your metric is a median, a ratio or a win rate and there is no clean standard error',
        'The metric is skewed enough that you do not trust the normal approximation',
        'Two hundred eval traces turn out to have come from twenty users',
        'Someone wants a confidence interval around the best of twelve prompt variants',
    ],
    trap=('&ldquo;I bootstrapped it, so the interval is assumption-free.&rdquo; Two specific '
          'sentences cost the loop. The first is bootstrapping rows in clustered data &mdash; 200 '
          'traces from 20 users resampled as 200 independent traces, which reports a band far tighter '
          'than the data can support and does it silently. The second is &ldquo;we swept 12 prompts, '
          'the best got 88%, and here is its bootstrap interval&rdquo;: the resampling never sees the '
          'selection, so you get a confident interval around the luckiest of twelve numbers.'),
    math=dict(
        tex=r'\hat\theta^{*(1)},\dots,\hat\theta^{*(B)}\;\Rightarrow\;'
            r'\text{CI}_{95}=\bigl[\hat\theta^{*}_{(0.025B)},\;\hat\theta^{*}_{(0.975B)}\bigr]',
        note='The percentiles are taken over the resampled statistics, not over the data. Nothing '
             'here corrects bias, dependence between rows, or a statistic that was selected for being '
             'the largest of a set.',
        cost='B recomputations instead of a derivation'),
    code=dict(
        label='Rows against clusters, on the same data',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
             'user = np.repeat(np.arange(<span class="s">20</span>), <span class="s">10</span>)'
             '        <span class="c"># 200 traces from 20 users</span>\n'
             'lat  = rng.lognormal(np.repeat(rng.normal(<span class="s">0</span>, <span class="s">.6</span>, '
             '<span class="s">20</span>), <span class="s">10</span>), <span class="s">.3</span>)\n\n'
             '<span class="k">def</span> ci(draw, B=<span class="s">10000</span>):\n'
             '    <span class="k">return</span> np.percentile([np.median(lat[draw()]) '
             '<span class="k">for</span> _ <span class="k">in</span> <span class="k">range</span>(B)],\n'
             '                        [<span class="s">2.5</span>, <span class="s">97.5</span>])\n\n'
             'ci(<span class="k">lambda</span>: rng.integers(<span class="s">0</span>, <span class="s">200</span>, '
             '<span class="s">200</span>))          <span class="c"># rows  -&gt; [0.82, 1.01]</span>\n'
             'ci(<span class="k">lambda</span>: np.concatenate([np.where(user == u)[<span class="s">0</span>]  '
             '<span class="c"># users -&gt; [0.73, 1.16]</span>\n'
             '     <span class="k">for</span> u <span class="k">in</span> rng.integers('
             '<span class="s">0</span>, <span class="s">20</span>, <span class="s">20</span>)]))\n\n'
             '<span class="c"># same data, same statistic. the honest interval is 2.3x wider</span>')),
    real=('Anthropic&rsquo;s <i>Adding Error Bars to Evals</i> (Miller, arXiv:2411.00640, November '
          '2024) turned this into standard practice for model evaluation, and two of its five '
          'recommendations are bootstrap hygiene: cluster the standard error when questions arrive in '
          'related groups, and do inference on question-level paired differences rather than on two '
          'marginal intervals. statsforevals.com adds the small-sample floor &mdash; below about 300 '
          'items use a Wilson interval for a pass rate and a smooth bootstrap for continuous scores '
          '&mdash; and states plainly that an interval on the best prompt from a sweep needs a max-T '
          'correction.'),
    drills=[
        dict(q='Your eval metric is a median latency over 200 traces. Give me a 95% interval. Now '
               'those 200 traces turn out to come from 20 users &mdash; does anything change?',
             a=('<b>Yes, and it changes the answer, not just the wording.</b> First pass: resample '
                '200 traces with replacement 10,000 times, take the median of each resample, read the '
                '2.5th and 97.5th percentiles. Once you know the traces come from 20 users the '
                'resampling unit changes: draw 20 users with replacement and take all of that '
                'user&rsquo;s traces each time. Your effective sample size was never 200, it is 20, '
                'and on realistic between-user variance the honest interval comes out roughly twice '
                'as wide. Same statistic, same code, different unit &mdash; and the second one is the '
                'number you report.'),
             a_simple=('<b>Yes &mdash; it roughly doubles the interval.</b> Deal yourself two hundred '
                       'traces from the ones you have, take the middle value, repeat ten thousand '
                       'times, and the middle of that spread is your range. But once you know the '
                       'traces came from twenty people, you have to deal out people instead, taking '
                       'all of a person&rsquo;s traces whenever you draw them. You had twenty '
                       'independent things all along, and the range that admits it is much wider.')),
        dict(q='You swept 12 prompts, the best scored 88% against a baseline of 81%, and you '
               'bootstrapped a confidence interval around the 88%. What is wrong?',
             a=('<b>The bootstrap resamples the data; it cannot see the sweep.</b> 88% is the maximum '
                'of twelve noisy estimates, so it is biased upward by construction &mdash; with 12 '
                'independent comparisons at 5% you find a &ldquo;winner&rdquo; from pure noise about '
                '46% of the time. What you produced is a tight band around a lucky number. Fixes in '
                'order: score the chosen prompt on a fresh held-out set, the only fully honest one; '
                'Holm or Benjamini&ndash;Hochberg across the variants; or a max-T correction so the '
                'interval accounts for the selection. And on 200 items a 7-point gap has a standard '
                'error near 3.5 points even before any of that.'),
             a_simple=('<b>The reshuffling never sees the sweep.</b> You took the highest of twelve '
                       'numbers, and the highest of twelve noisy numbers is too high on average '
                       '&mdash; run twelve prompts that are genuinely identical and one of them still '
                       'looks like a winner about half the time. Reshuffling the same two hundred '
                       'items cannot detect that, so you get a narrow range around a lucky number. '
                       'Score the chosen prompt on a fresh set of items and report that instead.')),
        dict(q='Can you bootstrap a 95% interval for the 99.9th percentile of request latency from '
               '500 traces?',
             a=('<b>No &mdash; not one you should quote.</b> A resample only ever contains values you '
                'already observed, so the 99.9th percentile of every resample is pinned to your top '
                'handful of rows: the bootstrap distribution goes discrete and lumpy, and the '
                'interval is both unstable and too narrow at the top. Three honest moves: report a '
                'quantile the data can support, such as p95; collect more tail data; or fit a tail '
                'model and say out loud that you are modelling rather than measuring. If you must '
                'work near a tail, push $B$ to 10,000, and on small samples use the smooth bootstrap '
                'so resamples are not restricted to the values you happened to see.'),
             a_simple=('<b>No &mdash; not one worth quoting.</b> Reshuffling can only ever deal you '
                       'values you already collected, so the very top of the range is decided by two '
                       'or three requests. The spread you get back looks reassuringly tight precisely '
                       'because every reshuffle keeps hitting the same few rows. Report a level the '
                       'data can support, gather more of the tail, or say plainly that you are '
                       'modelling the tail rather than measuring it.')),
    ],
    anchor=dict(
        formula=r'resample $\to$ recompute $\to$ percentiles &nbsp;&middot;&nbsp; of clusters, not rows',
        formula_simple='Deal yourself a fresh sample from the one you have, recompute, repeat ten '
                       'thousand times, and read off the middle.',
        bullets=[
            'It replaces a formula you do not have with computation you do',
            'Resample the unit you randomised &mdash; users, not rows',
            'It cannot repair bias, selection, or a tail the sample never contained',
        ]),
    chips=['percentile vs BCa', 'clustered standard errors', 'smooth bootstrap', 'max-T correction',
           'Wilson interval'],
    followup='Your eval metric is median latency over 200 traces &mdash; give me a 95% interval. Now those 200 traces come from 20 users: does anything change?',
),

# ----------------------------------------------------------------- 3
dict(
    id='winners-curse',
    tier='core',
    title='The winner&rsquo;s curse',
    kicker='The lift you ship is smaller than the lift you measured, and the reason is that you picked it for being big',
    simple=[
        'Every measured effect is the real effect plus noise. When you run a hundred experiments and '
        'ship the handful that looked best, you are not selecting only on which changes were good '
        '&mdash; you are also selecting on which ones got lucky. The winners are, on average, the '
        'ones whose noise happened to point upward, so the number in the launch document is too big '
        'before anybody has done anything wrong.',
        'Two consequences worth saying out loud. Effects shrink after launch, typically by a fifth to '
        'a half, which is why thirty experiments worth one percent each never add up to thirty '
        'percent on the annual chart. And the bigger and more surprising the win, the more of it is '
        'likely to be luck: the largest number on a leaderboard is the one most likely to be '
        'overstated, not the one to trust most. Being third on a leaderboard is not a fact about your '
        'model until you know how much the ordering wobbles.',
    ],
    analogy=('<b>Like a darts night where only the best throw counts.</b> Twenty people throw once '
             'and the winner lands the treble twenty. Ask them to do it again and they will not, on '
             'average, because you selected the throw at least as much as the thrower. Their real '
             'standard sits between that throw and the room average, and much closer to the room than '
             'the applause suggested.'),
    trap_simple=('&ldquo;We are third on the leaderboard.&rdquo; A rank is an estimate with a wobble '
                 'like any other, and when the gaps between models are smaller than that wobble, '
                 'third could equally be first or sixth. The in-house version is reporting the best '
                 'of twelve prompt variants as though someone had measured it rather than chosen it.'),
    tech=[
        'Observed effect equals true effect plus noise, so selecting on the observed effect selects '
        'partly on the noise. Gelman &amp; Carlin (2014) give the two error types worth naming: '
        '<b>Type M</b>, the exaggeration ratio of the estimate against the truth conditional on being '
        'selected, and <b>Type S</b>, the probability that a significant effect has the wrong sign. '
        'Both get worse as power falls, because an underpowered test has to get lucky to clear '
        'significance at all &mdash; which is why a significant result from a small test is the least '
        'trustworthy kind, not the most impressive one.',
        'Numbers to carry. Shipped-win effects shrink 20&ndash;50% in production. Facebook News Feed '
        '(Coey &amp; Cunningham, 2019) fitted shrinkage estimators over 226 experiments and cut mean '
        'squared error by 44%; Airbnb&rsquo;s experiment reporting framework (Lee &amp; Shen, 2018) '
        'documented 20&ndash;50% overstatement at portfolio level. The fixes are empirical-Bayes '
        'shrinkage of the reported lift before it reaches a roadmap, a post-launch holdback that '
        'measures the realised effect, or an explicit discount on the forecast. And keep this '
        'separate from novelty: novelty leaves a time trend inside the experiment, so plot the effect '
        'by days since first exposure; the winner&rsquo;s curse has no trend at all, it is a level '
        'shift that was there on day one.',
    ],
    tech_note=('The same mechanism runs the public leaderboards. <i>The Leaderboard Illusion</i> '
               '(arXiv:2504.20879, 2025) documented 27 private Llama-4 variants tested before release '
               'with only the best disclosed &mdash; best-of-N submission with selective reporting is '
               'this card operating at industry scale. Rank intervals over MMLU (arXiv:2607.16259; 15 '
               'models, 57 subjects, 100 prompt variations) routinely put three or more models at the '
               'same rank.'),
    fig=dict(
        kind='scatter',
        head=['WHAT YOU MEASURED', 'WHAT YOU GET'],
        xr=(0, 2), yr=(-0.4, 2.2),
        regions=[dict(x0=0, x1=2, y0=1.0, y1=2.2, tone='sig', op=0.07)],
        groups=[
            dict(pts=[(0.1, 0.45), (0.2, -0.15), (0.3, 0.6), (0.35, 0.05), (0.5, 0.85),
                      (0.55, 0.2), (0.6, 0.95), (0.7, 0.35), (0.75, 0.7), (0.9, 0.55),
                      (1.0, 0.9), (1.1, 0.4), (1.2, 0.75), (1.35, 0.95), (1.5, 0.6), (1.7, 0.8)],
                 tone='plain', hollow=True,
                 label='every experiment you ran', lx=1.95, ly=-0.3, la='end'),
            dict(pts=[(0.5, 1.1), (0.7, 1.3), (0.85, 1.25), (1.0, 1.55), (1.1, 1.45), (1.3, 1.9)],
                 tone='sig', r=4.2,
                 label='the six you shipped', lx=0.05, ly=2.05, la='start'),
        ],
        curves=[
            dict(pts=[(0, 1.0), (2, 1.0)], tone='sig', dash='5 4', sw=1.3,
                 label='ship only from up here', lat=0, la='start', dx=8, dy=-8),
            dict(pts=[(0, 0), (2, 2)], tone='mem', sw=1.6,
                 label='measured = true', lat=-1, la='end', dx=-6, dy=16),
        ],
        xticks=[(0, '0'), (1.0, '+1.0%'), (2.0, '+2.0%')],
        yticks=[(0, '0'), (1.0, '+1.0%'), (2.0, '+2.0%')],
        xlab='the effect that was really there',
        ylab='the effect you measured',
        foot='everything you shipped sits above the diagonal - that gap is the 20 to 50 percent you give back',
        alt=('A scatter of measured effect against true effect. A dashed horizontal line marks the '
             'ship threshold; every point above it also sits above the diagonal, so each shipped '
             'experiment measured larger than it truly was, while several genuinely good experiments '
             'below the line were never shipped.')),
    caption=('The diagonal is honesty. Every point you shipped sits above it, and not because the '
             'experiments were run badly &mdash; the shipped set is defined by having measured high, '
             'and measuring high is partly luck. Note the points on the lower right too: real wins '
             'that missed the bar, which is the same coin&rsquo;s other side.'),
    caption_simple=('The diagonal line is where an honest measurement would land. Everything above '
                    'the dashed line got shipped, and every one of those points sits above the '
                    'diagonal &mdash; each was measured as better than it really was. The points low '
                    'on the right are the opposite error: genuinely good changes that got unlucky and '
                    'were dropped.'),
    when=[
        'A launch review asks how much of the roadmap forecast to believe',
        'The metric moved less after launch than the experiment promised',
        'Someone is about to add up thirty experiment lifts and put the total in a deck',
        'You are reporting the best of twelve prompt variants, or a leaderboard position',
    ],
    trap=('&ldquo;We&rsquo;re #3 on the leaderboard.&rdquo; A rank is a point estimate of an ordering '
          'and it carries an interval: rank intervals built over MMLU with paired tests and Holm '
          'correction (15 models, 57 subjects, 100 prompt variations) routinely put three or more '
          'models at the same rank, so #3 is frequently indistinguishable from #1 or #6. The in-house '
          'twin is &ldquo;the effect declined after launch because of novelty&rdquo;, said without '
          'ruling out the winner&rsquo;s curse, a launch population that differs from the experiment '
          'population, or interference that disappears at 100% rollout.'),
    math=dict(
        tex=r'\hat\theta=\theta+\varepsilon\;\Rightarrow\;E\bigl[\hat\theta\mid\hat\theta\ \text{selected}\bigr]>\theta'
            r'\qquad \text{Type M}=\frac{E[\,|\hat\theta|\mid\text{significant}\,]}{|\theta|}',
        note='The estimator is unbiased. The selection is what is biased, so no amount of care in the '
             'analysis removes it &mdash; only shrinkage, replication or a holdback does.',
        cost='pure selection; nothing was done wrong'),
    code=dict(
        label='Two thousand ideas, ship the ones that measure well',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
             'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
             'true = rng.normal(<span class="s">0.0</span>, <span class="s">0.005</span>, '
             '<span class="s">2000</span>)      <span class="c"># true lifts, sd 0.5pp</span>\n'
             'obs  = true + rng.normal(<span class="s">0</span>, <span class="s">0.004</span>, '
             '<span class="s">2000</span>) <span class="c"># each measured with se 0.4pp</span>\n'
             'ship = obs &gt; <span class="s">0.008</span>                       '
             '<span class="c"># ship anything measuring above +0.8pp</span>\n\n'
             'obs[ship].mean()    <span class="c"># 1.10%  what the launch doc says</span>\n'
             'true[ship].mean()   <span class="c"># 0.65%  what you actually get</span>\n'
             '<span class="c"># 41% of the reported lift was selection. no bug, no novelty, no bad analysis</span>')),
    real_label='Where this has actually broken',
    real=('Facebook News Feed is the cleanest documented case: Coey &amp; Cunningham (2019) fitted '
          'shrinkage estimators across 226 experiments and cut mean squared error by 44%, which only '
          'works if the raw reported lifts were systematically too large. Airbnb&rsquo;s experiment '
          'reporting framework (Lee &amp; Shen, 2018) put portfolio-level overstatement at '
          '20&ndash;50%, and Azevedo et al. (2020) modelled the distribution of true effects across '
          'Bing&rsquo;s portfolio for the same reason. The universal symptom: summed experiment lifts '
          'never match the annual metric movement.'),
    drills=[
        dict(q='Your test showed a 1% improvement. Should you expect the same 1% after launch?',
             a=('<b>No &mdash; expect less, and say so before anyone asks.</b> You selected this '
                'experiment for having a large measured effect, so part of that 1% is noise you '
                'selected on: regression to the mean with a P&amp;L consequence. Published shrinkage '
                'across portfolios runs 20&ndash;50%, so forecast 0.5&ndash;0.8% and quote the range '
                'rather than the point. Then propose the two things that turn this into a measurement '
                'instead of a hope: an empirical-Bayes shrunk estimate for the roadmap number, and a '
                'post-launch holdback of a small slice of traffic that measures the realised effect.'),
             a_simple=('<b>No &mdash; budget for less.</b> You picked this experiment because its '
                       'number looked good, and part of any good-looking number is luck that will not '
                       'repeat. Across published portfolios the shipped effect comes in a fifth to a '
                       'half smaller, so forecast about half to two thirds of what you measured and '
                       'say that out loud. Then hold a small slice of users back from the launch for '
                       'a while, so you can measure what you actually got instead of arguing about '
                       'it a quarter later.')),
        dict(q='The effect faded after full launch. Your PM says it is novelty wearing off. Are they right?',
             a=('<b>Possibly, and they have not shown it &mdash; there are at least three other '
                'candidates.</b> Novelty, the winner&rsquo;s curse, a launch population that differs '
                'from the experiment population, and interference that disappears at 100%. They are '
                'distinguishable, which is the point of the question: novelty leaves a time trend '
                'inside the experiment, so plot the treatment effect by days since first exposure and '
                'split new against returning users. The winner&rsquo;s curse produces a level shift '
                'with no trend, present from day one. Google&rsquo;s ads-blindness work puts the '
                'learning half-life near 60 days, so a two-week test barely sees a novelty curve at '
                'all &mdash; which cuts against the novelty story more often than people expect.'),
             a_simple=('<b>Maybe, and they have not shown it.</b> At least three other things shrink '
                       'an effect at launch: the win was partly luck to start with, the people who '
                       'get it at full launch are not the people who were in the test, and effects '
                       'that depend on being rare vanish once everyone has it. You can tell them '
                       'apart. If people are getting bored, the effect also fades over time inside '
                       'the test, so chart it against how long each person has had the feature. If it '
                       'is flat inside the test and smaller outside, boredom is not the story.')),
        dict(q='&ldquo;We&rsquo;re #3 on the leaderboard.&rdquo; What is wrong with that sentence?',
             a=('<b>A rank is an estimate, and you have not reported its interval.</b> Build '
                'directional pairwise tests, apply Holm, and report the set of ranks the model could '
                'occupy: over MMLU with 15 models, 57 subjects and 100 prompt variations, overlapping '
                'intervals routinely place three or more models at the same rank, and subject-level '
                'variability exceeded prompt-variant variability. Then ask the selection question &mdash; '
                'how many private variants were submitted with only the best disclosed? <i>The '
                'Leaderboard Illusion</i> counted 27 private Llama-4 variants ahead of one public '
                'release, which is best-of-N reporting dressed as a measurement.'),
             a_simple=('<b>Third is not a measurement until you know how much the ordering '
                       'wobbles.</b> Re-run the same benchmark with the questions phrased differently '
                       'and the order shuffles; when the gaps between models are smaller than that '
                       'shuffle, third and first and sixth are the same claim. Report the range of '
                       'positions you could be in. Then ask how many private attempts were made '
                       'before the public one, because a board that shows only a lab&rsquo;s best '
                       'attempt is showing you its luckiest.')),
    ],
    anchor=dict(
        formula=r'$\hat\theta=\theta+\varepsilon$ &nbsp;&middot;&nbsp; $E[\hat\theta\mid\text{shipped}]>\theta$',
        formula_simple='What you measured is what is true plus luck, and picking the biggest number '
                       'picks up the luck along with it.',
        bullets=[
            'Selection on the estimate biases the estimate upward &mdash; no bug required',
            'Expect 20&ndash;50% shrinkage on shipped wins, and shrink the number before it reaches a deck',
            'Novelty leaves a time trend inside the test; the winner&rsquo;s curse does not',
            'A rank, a best-of-twelve prompt and a leaderboard position are all selected maxima',
        ]),
    chips=['Type M and Type S', 'empirical-Bayes shrinkage', 'post-launch holdback',
           'regression to the mean', 'max-T correction'],
    followup='Your test showed a 1% improvement. Should you expect the same 1% after launch?',
),

# ----------------------------------------------------------------- 4
dict(
    id='simpsons-paradox',
    tier='core',
    title='Simpson&rsquo;s paradox and the segment that flips',
    kicker='Every segment can move one way while the total moves the other, and the total is not automatically the truth',
    simple=[
        'Berkeley&rsquo;s 1973 graduate admissions look open and shut: 44% of men admitted against '
        '35% of women. Go department by department and it reverses &mdash; women were admitted at '
        'equal or higher rates almost everywhere. Both numbers are arithmetically correct. The '
        'overall figure is a weighted average, and the weights differ between the two groups, because '
        'women applied disproportionately to the departments that admit hardly anyone.',
        'This is not a curiosity. It happens whenever the mix of who sits in each group differs '
        'across something that also drives the outcome. And the important part is that arithmetic '
        'will never tell you which number to quote. You settle that by asking what the thing you '
        'split on actually is: something fixed before anyone was assigned, which is a genuine common '
        'cause and belongs in the comparison, or something the treatment itself could have changed, '
        'in which case splitting on it can manufacture the reversal and the pooled number is the '
        'honest one.',
    ],
    analogy=('<b>Like a batting average across two seasons.</b> One player can out-average another in '
             'every single season and still finish behind them over the two combined, if the seasons '
             'differed in difficulty and each player took most of their turns in a different one. '
             'Nobody cheated and no number is wrong. The totals simply weight the two seasons '
             'differently for each player.'),
    trap_simple=('Slicing into fifteen segments after a disappointing result and presenting the one '
                 'that came back significant. That is a fishing trip, not a finding. The subtler '
                 'version is splitting on something that happened after the treatment &mdash; who '
                 'engaged, who opened the feature &mdash; which can invent a reversal out of a '
                 'perfectly clean experiment.'),
    tech=[
        'The mechanism is an unequal mix across a confounder: the pooled rate is a weighted average '
        'of segment rates and the weights differ between arms, so the pooled comparison can reverse '
        'every segment comparison at once. Berkeley 1973 is canonical (Bickel, Hammel &amp; '
        'O&rsquo;Connell, <i>Science</i> 187:398, 1975): 44% of men and 35% of women admitted '
        'overall, with department-level rates equal or higher for women, because application volume '
        'was distributed very differently. In experiments the same shape arrives as <b>mix shift</b>: '
        'if the treatment changes who is active, the composition of the analysed population changes '
        'with it and segment and overall results diverge.',
        'The decision rule, because &ldquo;it depends&rdquo; fails the follow-up. <b>Ask when the '
        'splitting variable was determined.</b> Fixed before assignment and plausibly a cause of the '
        'outcome &mdash; country, device, tenure, department &mdash; then condition on it, the '
        'segmented answer is the causal one, and the segment list should have been pre-registered. '
        'Determined during or after treatment &mdash; sessions in the test window, whether the user '
        'opened the feature &mdash; then it is a mediator or a collider, conditioning opens a '
        'non-causal path, and the pooled estimate is the one that answers the question you '
        'randomised. In a clean randomised test with no SRM the pooled estimate is unbiased by '
        'construction, so a flip inside a post-treatment slice is an analysis bug rather than a '
        'finding. The DAG settles it; the table never will.',
    ],
    tech_note=('Two checks before anyone argues about which number is right. First, SRM inside the '
               'segment: differential dropout in one slice reproduces this shape for free, and about '
               '6% of Microsoft experiments carry an SRM. Second, multiplicity: fifteen post-hoc '
               'slices at 5% hand you a significant one roughly half the time, so a post-hoc segment '
               'is a hypothesis and the confirmation is a fresh test powered for that segment alone.'),
    fig=dict(
        kind='scatter',
        head=['WITHIN EACH DEPARTMENT', 'POOLED'],
        xr=(0.4, 6.8), yr=(0, 92),
        regions=[dict(x0=4.4, x1=6.6, y0=0, y1=92, tone='sig', op=0.07)],
        groups=[
            dict(pts=[], label='most women applied here', lx=5.5, ly=86, tone='sig', la='middle'),
            dict(pts=[(1, 60), (2, 55), (3, 42), (4, 33), (5, 24), (6, 12)],
                 tone='plain', hollow=True),
            dict(pts=[(1, 78), (2, 60), (3, 45), (4, 36), (5, 28), (6, 14)],
                 tone='mem', r=4.0),
        ],
        curves=[
            dict(pts=[(1, 78), (2, 60), (3, 45), (4, 36), (5, 28), (6, 14)], tone='mem', sw=1.9,
                 label='women, by department', lat=0, la='start', dx=8, dy=-9),
            dict(pts=[(1, 60), (2, 55), (3, 42), (4, 33), (5, 24), (6, 12)], tone='plain', sw=1.5,
                 label='men, by department', lat=5, la='end', dx=-8, dy=17),
            dict(pts=[(0.5, 44), (6.7, 44)], tone='sig', dash='5 4', sw=1.3,
                 label='men, pooled 44%', lat=-1, la='end', dx=-4, dy=-8),
            dict(pts=[(0.5, 35), (6.7, 35)], tone='sig', dash='5 4', sw=1.3,
                 label='women, pooled 35%', lat=-1, la='end', dx=-4, dy=17),
        ],
        yticks=[(0, '0'), (35, '35%'), (44, '44%'), (80, '80%')],
        xlab='the departments, hardest to get into on the right',
        ylab='admission rate',
        foot='level or ahead in every department, nine points behind overall - the mix does that, not the decisions',
        alt=('Admission rate plotted by department. The line for women sits at or above the line for '
             'men in every department, while two dashed horizontal lines show the pooled rates the '
             'other way round: men at 44 percent and women at 35 percent. Most women applied in the '
             'shaded region on the right, where almost nobody is admitted.')),
    caption=('The two dashed lines are Berkeley&rsquo;s actual aggregate rates; the per-department '
             'points are illustrative, but their shape is the finding. Women are level or ahead in '
             'every department and nine points behind overall, because their applications '
             'concentrate in the shaded band on the right where the admission rate is near the floor.'),
    caption_simple=('The two dashed lines are the real overall rates, men above women. The two solid '
                    'lines are the rates inside each department, and the women&rsquo;s line is level '
                    'or higher the whole way across. The gap comes from which departments each group '
                    'applied to, not from how they were treated once there.'),
    when=[
        'The overall result is positive and one large segment is significantly negative',
        'A dashboard number and a per-country breakdown disagree about the sign',
        'Someone proposes analysing only the users who engaged with the new feature',
        'A treatment changes who shows up at all, not just what they do',
    ],
    trap=('Slicing into fifteen segments after a null result and reporting the one that came back '
          'significant &mdash; that is the multiple-comparisons card in a disguise, and at fifteen '
          'slices you find one about half the time. The more expensive version is segmenting on a '
          'variable measured after treatment: &ldquo;among users who actually used the feature, the '
          'lift is 8%&rdquo;. Usage is an outcome, not a segment. Conditioning on it opens a collider '
          'path and can manufacture a reversal in a perfectly clean randomised experiment.'),
    math=dict(
        tex=r'\frac{a_1}{b_1}<\frac{c_1}{d_1},\quad\frac{a_2}{b_2}<\frac{c_2}{d_2}'
            r'\qquad\text{yet}\qquad\frac{a_1+a_2}{b_1+b_2}>\frac{c_1+c_2}{d_1+d_2}',
        note='Nothing here is broken. A pooled ratio is a weighted average whose weights come from '
             'the denominators, and the two groups do not share them. Which side answers your '
             'question is a causal matter, and this line cannot tell you.',
        cost='arithmetic only; the causal question is separate'),
    code=dict(
        label='Berkeley&rsquo;s headline, rebuilt from a mix',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
             '<span class="c"># synthetic, shaped like Berkeley: women apply mostly where nobody gets in</span>\n'
             'apps = np.array([[<span class="s">600.</span>, <span class="s">400.</span>],   '
             '<span class="c"># men:   easy dept, hard dept</span>\n'
             '                 [<span class="s">300.</span>, <span class="s">700.</span>]])  '
             '<span class="c"># women: easy dept, hard dept</span>\n'
             'rate = np.array([[<span class="s">0.60</span>, <span class="s">0.20</span>],   '
             '<span class="c"># men admitted, by dept</span>\n'
             '                 [<span class="s">0.64</span>, <span class="s">0.22</span>]])  '
             '<span class="c"># women admitted -- HIGHER in both</span>\n\n'
             '(apps * rate).sum(<span class="s">1</span>) / apps.sum(<span class="s">1</span>)\n'
             '<span class="c"># array([0.440, 0.346])  -- men ahead by 9 points, from the mix alone</span>')),
    real=('UC Berkeley&rsquo;s 1973 graduate admissions: 44% of men admitted against 35% of women, a '
          'gap large enough that the university faced a discrimination suit on the aggregate figure. '
          'The reanalysis by Bickel, Hammel &amp; O&rsquo;Connell (<i>Science</i> 187:398, 1975) '
          'found department-level rates equal or higher for women, with the aggregate gap explained '
          'mostly by which departments each group applied to. The honest reading is neither '
          '&ldquo;there was no bias&rdquo; nor &ldquo;the aggregate was right&rdquo; &mdash; it moves '
          'the question to why the departments women applied to were the ones admitting almost '
          'nobody.'),
    drills=[
        dict(q='The overall lift is significantly positive, but for your largest customer segment it '
               'is significantly negative. What do you do?',
             a=('<b>Do not average it away, and do not act on it yet either.</b> Four checks in '
                'order. Is the segment defined by something fixed before assignment, or by behaviour '
                'during the test? If it is post-treatment, the pooled number is the causal one and '
                'the segment view is an artefact. Is there an SRM inside that segment? Differential '
                'dropout reproduces this shape for free. Was the segment pre-registered, or is it one '
                'of fifteen slices? If it survives all three it is genuine heterogeneity, and the '
                'move is a targeted rollout that excludes the segment plus a confirmation test '
                'powered on that segment alone &mdash; with the segment loss stated next to the '
                'overall gain in the launch decision, not buried under it.'),
             a_simple=('<b>Neither number wins on its own.</b> First ask whether that segment is '
                       'defined by something true about people before the test started, or by what '
                       'they did during it &mdash; if it is their behaviour during the test, the '
                       'segment view is an artefact of the analysis and the overall number stands. '
                       'Then check the split into test and control is still clean inside that '
                       'segment. Then ask whether you planned to look at this segment or found it '
                       'afterwards. If it survives all three it is real: launch to everyone else, run '
                       'a proper test on that segment, and put the loss beside the gain when you '
                       'decide.')),
        dict(q='Berkeley admitted 44% of men and 35% of women, yet no department admitted women at a '
               'lower rate. Which number is the answer?',
             a=('<b>The department-level one, because department is chosen before any admissions '
                'decision and drives the admission rate.</b> It is a common cause of both which group '
                'you are looking at and the outcome, so it is a confounder and you condition on it; '
                'the pooled rate is a weighted average whose weights differ by group. But &ldquo;it '
                'is Simpson&rsquo;s paradox&rdquo; is not where the analysis ends. The disparity has '
                'been relocated, not dissolved: the live question becomes why women&rsquo;s '
                'applications concentrated in the low-admission departments, which is a question '
                'about the pipeline rather than about the admissions committees.'),
             a_simple=('<b>The department-by-department one.</b> Which department you apply to is '
                       'settled before any decision is made and it changes your odds enormously, so '
                       'it belongs in the comparison. The overall figure mixes together applicants '
                       'facing wildly different odds and calls the mixture a rate. Note what this '
                       'does and does not settle: it says the committees were not the mechanism, and '
                       'it moves the question to why the two groups applied to such different '
                       'places.')),
        dict(q='What is your rule for deciding whether to trust the pooled number or the segments?',
             a=('<b>Ask when the splitting variable was determined, not which answer you prefer.</b> '
                'Fixed before assignment and a plausible cause of the outcome: condition on it, the '
                'segmented estimate is the causal one, and it should have been on a pre-registered '
                'list. Determined during or after treatment: conditioning opens a mediator or '
                'collider path, and the pooled estimate is the one that answers the question you '
                'randomised. In a randomised test with no SRM, pooled is unbiased by construction, so '
                'a flip in a post-treatment slice is an analysis bug until proven otherwise. The '
                'arithmetic is identical either way &mdash; the causal graph decides, and if you '
                'cannot draw it you cannot answer.'),
             a_simple=('<b>Ask when the thing you are splitting on was decided.</b> Fixed before '
                       'anyone was put into a group &mdash; country, device, how long they have been '
                       'a customer &mdash; and plausibly affecting the outcome: split on it and '
                       'trust the segments. Decided during or after the treatment &mdash; whether '
                       'they engaged, how many sessions they had: splitting on it can invent the '
                       'reversal by itself, and the overall number is the honest one. Same table, '
                       'two answers, and what decides is the story about what caused what.')),
    ],
    anchor=dict(
        formula=r'$\frac{a_1}{b_1}<\frac{c_1}{d_1}$ and $\frac{a_2}{b_2}<\frac{c_2}{d_2}$'
                r' &nbsp;yet&nbsp; $\frac{a_1+a_2}{b_1+b_2}>\frac{c_1+c_2}{d_1+d_2}$',
        formula_simple='Two fractions can each be smaller than their rival and still be larger once '
                       'the tops and the bottoms are added up, because the two get averaged with '
                       'different weights.',
        bullets=[
            'The pooled number is a weighted average, and the two arms do not share the weights',
            'Split on causes fixed before assignment; never on anything the treatment could change',
            'A flipping segment in a clean randomised test is an analysis bug until proven otherwise',
            'Berkeley: 44% against 35% overall, equal or higher for women in every department',
        ]),
    chips=['confounding', 'mix shift', 'collider bias', 'pre-registered segments',
           'sample ratio mismatch'],
    followup='The overall lift is significantly positive, but for your largest customer segment it is significantly negative. What do you do?',
),

# ----------------------------------------------------------------- 5
dict(
    id='practical-significance',
    tier='core',
    title='Practical vs statistical significance',
    kicker='At ten million users everything is significant; the question is whether the interval clears what the feature costs to keep',
    simple=[
        'Significance and importance are different questions, and only one of them gets easier with '
        'more users. The evidence that an effect exists depends on how much data you have. The size '
        'of the effect does not. Push the sample high enough and a difference nobody could ever '
        'notice comes back significant, because you have measured a tiny thing very precisely.',
        'So the number that decides is not the test result, it is the range of plausible effects '
        '&mdash; and what you compare that range to is not zero. Zero is the wrong bar. The right bar '
        'is what the feature costs to keep: the engineers who maintain it, the extra code path, the '
        'thing that can page someone at three in the morning, the risk to whatever you promised not '
        'to break. If the whole plausible range sits below that bar, you have a real effect you '
        'should not ship, and that is a decision rather than a shrug. The mirror mistake is just as '
        'expensive: waving away a third of a percent when a third of a percent of revenue is tens of '
        'millions a year.',
    ],
    analogy=('<b>Like a kitchen scale that reads to the milligram.</b> Buy a precise enough scale and '
             'you can prove beyond any doubt that today&rsquo;s loaf is two milligrams heavier than '
             'yesterday&rsquo;s. The measurement is real and the difference is real. Nobody eating '
             'the bread will ever tell, and no bakery on earth would change its process for it.'),
    trap_simple=('Using &ldquo;significant&rdquo; as a synonym for &ldquo;worth doing&rdquo;, and its '
                 'cousin: arguing that a result with a far more impressive test number must be a '
                 'bigger effect. It is a more precisely measured one, not a bigger one, and the two '
                 'usually point opposite ways because the precise one simply had more users.'),
    tech=[
        'p-values shrink with $n$; effect sizes do not. Facebook&rsquo;s emotional contagion study '
        'manipulated News Feed for 689,003 users and reported highly significant effects at a '
        'Cohen&rsquo;s $d$ around 0.001 &mdash; roughly one fewer emotional word per thousand. The '
        'arithmetic is the sample-size rule read backwards: with $n \\approx 16\\sigma^2/\\delta^2$ '
        'per arm, the minimum detectable effect falls as $1/\\sqrt{n}$, so every hundredfold increase '
        'in users divides the detectable effect by ten. None of that makes the effect matter more.',
        'Report the estimate with its interval and compare the interval to a threshold you wrote down '
        'before the test, not to zero. Three things belong in that threshold: the value of the lift '
        'at your actual base, in money or in the OEC&rsquo;s own units; the ongoing cost of keeping '
        'the feature alive; and the guardrails, which are tested for non-inferiority rather than '
        'superiority, so the question there is whether the bad end of the interval is inside '
        'tolerance. Then the decision falls out. If the entire interval sits below the threshold you '
        'have precisely measured something not worth having, and the finding is do not ship. If the '
        'interval straddles the threshold you are asking for more data, not for a verdict.',
    ],
    tech_note=('The inverse error costs more, and interviewers use it as the second half of the same '
               'question. Bing measured about 0.6% of revenue for every 100 ms of speedup and Amazon '
               'about 1% of sales for every 100 ms of slowdown, and at Bing a genuine win moves key '
               'metrics by 0.1&ndash;1.0%. Against numbers like those, &ldquo;only 0.3%&rdquo; is not '
               'a small effect &mdash; it is the size real wins actually come in.'),
    fig=dict(
        kind='plot',
        head=['WHAT MORE USERS BUY', 'WHAT THEY DO NOT'],
        xr=(0, 4), yr=(0, 5.4), ph=190,
        xticks=[(0, '10k'), (1, '100k'), (2, '1M'), (3, '10M'), (4, '100M')],
        yticks=[(0.5, '0.5%'), (1.6, '1.6%'), (5, '5%')],
        bands=[dict(x0=2.0, x1=4.0, tone='sig', op=0.07, label='everything here is significant')],
        curves=[
            dict(pts=[(0, 0.5), (4, 0.5)], tone='mem', sw=1.4, fill=True,
                 label='what the feature costs to keep', lat=-1, la='end', dx=-6, dy=-8),
            dict(pts=[(0, 5.0), (1, 1.58), (2, 0.5), (3, 0.158), (4, 0.05)], tone='sig', sw=1.9,
                 label='smallest lift you can detect', lat=0, la='start', dx=8, dy=-10),
        ],
        marks=[dict(x=0.2, y=0.25, r=0, tone='mem', la='start', dx=0, dy=2,
                    label='significant, and not worth keeping')],
        xlab='users per arm',
        ylab='smallest lift you can detect',
        foot='more users move the falling line and never the flat one',
        alt=('A falling curve showing the smallest detectable lift dropping by about a factor of '
             'three for every tenfold increase in users, crossing a flat shaded line at the lift the '
             'feature must clear to pay for itself, below which everything is significant and not '
             'worth keeping.')),
    caption=('The falling line is the minimum detectable effect, dropping as one over the square root '
             'of the sample size. The flat line is the lift that pays for the feature, and it is set '
             'by engineering cost rather than by statistics. Everything below the crossing point is '
             'significant and not worth shipping. Anchored at a 5% detectable lift with 10,000 users '
             'per arm; the shape is what matters.'),
    caption_simple=('The falling line is the smallest lift you could detect, which keeps dropping as '
                    'you collect more users. The flat line is the lift the feature has to beat to be '
                    'worth maintaining, and no amount of data moves it. Everything under the crossing '
                    'point is a real effect that is not worth shipping.'),
    when=[
        'A result is significant at ten million users and the lift is 0.02%',
        'A PM dismisses a 0.3% lift as being in the noise',
        'Someone ranks two results by which p-value is smaller',
        'You are writing the launch criteria and nobody has named a threshold yet',
    ],
    trap=('Two sentences, mirror images of each other. &ldquo;It&rsquo;s statistically significant, '
          'so we should ship it&rdquo; &mdash; significance says the effect is probably not exactly '
          'zero and says nothing whatever about whether it clears the cost of the code path. And '
          '&ldquo;p = 0.0001 here against p = 0.04 there, so the first effect is stronger&rdquo; '
          '&mdash; no, it is more precisely estimated, usually because it had more users, and it is '
          'frequently the smaller of the two effects. The expensive version of the same confusion is '
          'dismissing a 0.3% lift as noise without ever asking 0.3% of what.'),
    math=dict(
        tex=r'\delta_{\min}\approx\frac{4\sigma}{\sqrt{n}}\qquad\text{ship when }\;'
            r'\text{CI}_{\text{low}}>\delta_{\text{cost}}',
        note='The left-hand side keeps falling as you collect users. The right-hand side is set by '
             'what the feature costs to maintain and does not move at all. Compare the interval to '
             'the cost, never the p-value to 0.05.',
        cost='one threshold, declared before the test'),
    code=dict(
        label='The bar you can detect, against the bar that matters',
        cost='numpy',
        src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
             'sigma = <span class="s">1.0</span>\n'
             '<span class="k">for</span> n <span class="k">in</span> '
             '(<span class="s">1e4</span>, <span class="s">1e5</span>, <span class="s">1e6</span>, '
             '<span class="s">1e7</span>):          <span class="c"># users per arm</span>\n'
             '    <span class="k">print</span>(n, <span class="s">4</span>*sigma/np.sqrt(n))  '
             '<span class="c"># n = 16 sigma^2 / delta^2, rearranged</span>\n\n'
             '<span class="c">#   1e+04   0.0400 sd        1e+06   0.0040 sd</span>\n'
             '<span class="c">#   1e+05   0.0126 sd        1e+07   0.0013 sd</span>\n'
             '<span class="c"># thirtyfold more precision, and the cost of the feature has not moved</span>')),
    real=('Facebook&rsquo;s emotional contagion experiment (Kramer, Guillory &amp; Hancock, '
          '<i>PNAS</i> 111(24), June 2014) manipulated News Feed for 689,003 users. The effects were '
          'real and the p-values were tiny; Cohen&rsquo;s d was around 0.001, about one fewer '
          'emotional word per thousand. The paper is famous for its ethics, but the statistical '
          'lesson is the one interviewers use: massive scale plus significance says nothing about '
          'magnitude. Set it against Bing&rsquo;s latency work, where 100 ms is worth roughly 0.6% of '
          'revenue &mdash; there, a fraction of a percent is the entire prize.'),
    drills=[
        dict(q='p is below 0.001 and the lift is 0.02%. Ship?',
             a=('<b>Nothing in those two numbers decides it.</b> Ask for the interval and for the '
                'threshold. Convert 0.02% into the currency the business runs on at your actual base '
                '&mdash; 0.02% of a large enough revenue line is a real number and 0.02% of a metric '
                'nobody tracks is not &mdash; and set it against the ongoing cost: maintenance, the '
                'extra code path, the on-call surface, the guardrails. If the whole interval sits '
                'below that cost line, the finding is do not ship, and it is a finding rather than a '
                'null. And if nobody wrote a threshold down before the test, say so out loud: that is '
                'the real problem, and it is fixable before the next one.'),
             a_simple=('<b>Those two numbers cannot decide it between them.</b> The first only says '
                       'the effect is probably not exactly zero, which at that many users is close to '
                       'guaranteed. Turn the size into money at your real volume, then put it against '
                       'what the feature costs to keep alive each year &mdash; the people maintaining '
                       'it, the extra thing that can break at three in the morning. If the whole '
                       'plausible range sits below that cost, the answer is a confident no. And if '
                       'nobody agreed a bar before the test started, that is the finding worth '
                       'reporting.')),
        dict(q='A colleague says the result with p = 0.0001 is a stronger effect than the one with '
               'p = 0.04. Correct them.',
             a=('<b>It is a more precisely estimated effect, not a bigger one.</b> A p-value is a '
                'function of the effect size and the sample size together, so a 0.01% lift on ten '
                'million users produces a far smaller p than a 5% lift on two hundred. Put the two '
                'confidence intervals side by side instead; that comparison means something and the '
                'p-value comparison does not. It matters in practice because the tiny-effect, '
                'huge-sample result is usually the one attached to the biggest surface, so ranking a '
                'roadmap by p-value systematically funds the least valuable work in the building.'),
             a_simple=('<b>It is a more precisely measured effect, not a larger one.</b> That number '
                       'combines how big the effect is with how much data you had, so a tiny '
                       'difference measured across millions of people beats a large difference '
                       'measured across two hundred. Compare the two ranges of plausible effect sizes '
                       'instead. Ranking projects by whose test result looked most impressive '
                       'reliably funds the least useful work, because the most heavily measured '
                       'surfaces are not the most valuable ones.')),
        dict(q='Your PM dismisses a 0.3% lift as being in the noise. When are they wrong?',
             a=('<b>Whenever the interval excludes zero and 0.3% of the base is a large number.</b> '
                'Ask what it is 0.3% of. Bing&rsquo;s entire latency programme trades in fractions of '
                'a percent &mdash; about 0.6% of revenue per 100 ms of speedup &mdash; and a genuine '
                'win there moves key metrics by 0.1&ndash;1.0%, so a fraction of a percent is the '
                'normal size of a real result rather than a rounding error. The rule is symmetric '
                'with the other error: never argue from the size of the percentage, argue from the '
                'percentage times the base, set against the cost of keeping it.'),
             a_simple=('<b>Whenever a third of a percent of the base is a big number.</b> A '
                       'percentage says nothing on its own; a third of a percent of a large revenue '
                       'line is tens of millions a year, and the cost of maintaining the feature is a '
                       'rounding error beside it. At the scale large companies operate, genuine wins '
                       'mostly arrive in fractions of a percent, and the ones that arrive in double '
                       'digits are usually bugs. Ask what it is a fraction of before deciding it is '
                       'noise.')),
    ],
    anchor=dict(
        formula=r'$\delta_{\min}\approx 4\sigma/\sqrt{n}$ &nbsp;&middot;&nbsp; ship when '
                r'$\text{CI}_{\text{low}}>\delta_{\text{cost}}$',
        formula_simple='The smallest effect you can detect keeps shrinking as you add users. The '
                       'smallest effect worth having does not move at all.',
        bullets=[
            'More users lower the bar you can detect, never the bar that matters',
            'Compare the interval to a threshold declared before the test, not to zero',
            'A whole interval below the cost line is a decision, not a null result',
            'The mirror error is dismissing a fraction of a percent without asking, of what',
        ]),
    chips=['minimum detectable effect', 'OEC', 'guardrails', 'non-inferiority', 'Cohen&rsquo;s d'],
    followup='p is below 0.001 and the lift is 0.02%. Do you ship?',
),
]
