CARDS = [

    # ------------------------------------------------------------------ F6
    dict(
        id='correlation-causation',
        tier='foundation',
        title='Correlation, causation and the third thing',
        kicker='Everyone can recite the slogan. The interview asks which of three structures you are looking at, and only one of them is fixed by adding the variable to your regression',
        simple=[
            'Two things move together. There are only a handful of explanations, and the whole '
            'skill is telling them apart in about thirty seconds. The first caused the second. '
            'The second caused the first. Or some third thing is responsible &mdash; and that '
            'third thing comes in three quite different shapes, which is the part nobody '
            'rehearses.',
            'A <b>common cause</b> sits behind both: heavy users try more features and also stick '
            'around, so the feature looks like it keeps them. A <b>stepping stone</b> sits on the '
            'path between them: the change works <i>through</i> it, so holding it fixed deletes '
            'the very effect you were measuring. A <b>shared consequence</b> sits downstream of '
            'both: two unrelated causes feed into it, and if you look only at the cases where it '
            'happened, you invent a link that was never there. Hold the first one fixed. Never '
            'touch the other two. The quick test is timing: did this variable already exist '
            'before you made your change, or did it appear afterwards? Before is fair game. '
            'After is a trap.',
        ],
        analogy=('<b>Like counting fire engines.</b> More engines turn up, more damage &mdash; and '
                 'nobody blames the engines, because the size of the fire drives both. Now survey '
                 'only the buildings that burned down. Inside that group, damp weather and a slow '
                 'alarm can look unrelated, or even helpful, because every building that survived '
                 'has been thrown away.'),
        trap_simple=('Saying the slogan out loud and then, two minutes later, reading a regression '
                     'coefficient as if it were an effect. The quieter version is adding more '
                     'controls because more feels safer. Two of the three shapes get worse the '
                     'more you control for them, and nothing in the output tells you which shape '
                     'you are in.'),
        tech=[
            'Draw the arrows before you touch the data. A <b>confounder</b> is a common cause, '
            '$X \\leftarrow C \\rightarrow Y$: it opens a backdoor path and you must block it, by '
            'adjustment, stratification or randomisation. A <b>mediator</b> lies on the causal '
            'path, $X \\rightarrow M \\rightarrow Y$: conditioning on it removes exactly the '
            'effect you were trying to estimate, which is why controlling for enquiries when you '
            'measure Instant Book is Airbnb&rsquo;s favourite trap. A <b>collider</b> is a common '
            'effect, $X \\rightarrow K \\leftarrow Y$: the path through it is already blocked, and '
            'conditioning on it <i>opens</i> it, manufacturing a correlation between two variables '
            'that were independent. That is Berkson&rsquo;s paradox, and it is the one that '
            'separates candidates.',
            'So "I controlled for it" is not an argument, it is a claim about a graph. The backdoor '
            'criterion names the minimal sufficient adjustment set; the sloppy version &mdash; put '
            'everything in and let the regression sort it out &mdash; guarantees you condition on '
            'mediators and colliders too, and can flip the sign of the estimate. The heuristic '
            'that gets you most of the way in an interview is one phrase: <b>pre-treatment '
            'covariates only</b>. Anything measured after the treatment is downstream of it, and '
            'downstream variables are either mediators or colliders. Neither belongs in a causal '
            'regression.',
        ],
        tech_note=('Selection into the sample is a collider you did not choose. Restricting to '
                   'users who converted, sessions that completed or accounts that survived is '
                   'conditioning on a common effect, and it distorts every association you then '
                   'measure inside that group. The only clean fixes are randomisation or a design '
                   'that makes the confounder irrelevant &mdash; instrumental variables, '
                   'difference-in-differences, regression discontinuity. A control variable is not '
                   'a design.'),
        fig=dict(
            kind='blocks',
            h=236,
            boxes=[
                dict(x=92, y=44, w=84, h=38, t='heavy user', sub='common cause', tone='mem'),
                dict(x=34, y=140, w=84, h=38, t='uses feature'),
                dict(x=150, y=140, w=84, h=38, t='retains'),
                dict(x=318, y=44, w=84, h=38, t='enquiries', sub='on the path', tone='sig'),
                dict(x=260, y=140, w=84, h=38, t='Instant Book'),
                dict(x=376, y=140, w=84, h=38, t='bookings'),
                dict(x=544, y=44, w=84, h=38, t='converted', sub='common effect', tone='sig'),
                dict(x=486, y=140, w=84, h=38, t='ad quality'),
                dict(x=602, y=140, w=84, h=38, t='discount'),
            ],
            links=[
                dict(a=0, b=1, side='down'), dict(a=0, b=2, side='down'),
                dict(a=4, b=3, side='up'), dict(a=3, b=5, side='down'),
                dict(a=7, b=6, side='up'), dict(a=8, b=6, side='up'),
            ],
            labels=[
                dict(x=34, y=26, t='confounder', a='start', tone='mem'),
                dict(x=260, y=26, t='mediator', a='start', tone='sig'),
                dict(x=486, y=26, t='collider', a='start', tone='sig'),
                dict(x=34, y=202, t='adjust for it', a='start', tone='mem'),
                dict(x=260, y=202, t='adjusting deletes it', a='start', tone='sig'),
                dict(x=486, y=202, t='adjusting invents it', a='start', tone='sig'),
            ],
            foot='only the left-hand shape is fixed by putting the variable in your regression',
            alt='Three small causal diagrams side by side with the same three boxes each. On the '
                'left both arrows point out of the top box down to the two lower boxes, a '
                'confounder, marked adjust for it. In the middle the arrows run from the left box '
                'up through the top box and down to the right box, a mediator, marked adjusting '
                'deletes it. On the right both arrows point up into the top box, a collider, '
                'marked adjusting invents it.'),
        caption=('The boxes never change; only the arrowheads do, and the arrowheads reverse the '
                 'instruction. Nothing in a regression output distinguishes these three, which is '
                 'why the answer has to come from knowing what happened before what.'),
        caption_simple=('Same three boxes in all three pictures. The only difference is which way '
                        'the arrows point, and that difference is the entire answer to whether you '
                        'should hold the middle thing fixed.'),
        when=[
            'A dashboard says users of a feature retain far better and someone wants to build more of it',
            'You are about to add a control variable "to be safe"',
            'An analysis is restricted to users who converted, sessions that completed, or accounts still active',
            'A promo, a notification or an email was targeted rather than randomised',
        ],
        trap=('Saying "correlation is not causation" and then, two minutes later, reading a '
              'regression coefficient as a causal effect. The sharper version is a sentence '
              'candidates volunteer unprompted: <i>"I controlled for it, so it is causal."</i> Ask '
              'which of the three structures the control is. If it was measured after the '
              'treatment it is a mediator or a collider, and adding it made the estimate worse, '
              'not better.'),
        math=dict(
            tex=r'X \leftarrow C \rightarrow Y \quad \text{adjust} \qquad X \rightarrow M \rightarrow Y \quad \text{do not} \qquad X \rightarrow K \leftarrow Y \quad \text{never}',
            note='Same three variables, three different graphs, three opposite instructions. The '
                 'data cannot tell you which graph you are in. Only knowing what happened before '
                 'what can.',
            cost='a graph you have to defend, not a p-value'),
        code=dict(
            label='Collider bias in six lines: nothing changes but who you look at',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
                 'skill = rng.normal(size=<span class="s">200_000</span>)\n'
                 'luck  = rng.normal(size=<span class="s">200_000</span>)  '
                 '<span class="c"># independent by construction</span>\n'
                 '<span class="k">print</span>(np.corrcoef(skill, luck)[<span class="s">0</span>,<span class="s">1</span>])  '
                 '<span class="c"># -0.003. nothing there</span>\n\n'
                 'hired = skill + luck &gt; <span class="s">2.0</span>   '
                 '<span class="c"># a common effect of both: 7.9% get in</span>\n'
                 '<span class="k">print</span>(np.corrcoef(skill[hired], luck[hired])[<span class="s">0</span>,<span class="s">1</span>])  '
                 '<span class="c"># -0.72 among the hired</span>\n'
                 '<span class="c"># inside the company, talent and luck now look like substitutes.</span>\n'
                 '<span class="c"># they are not. you conditioned on a collider.</span>')),
        real=('Google Flu Trends. The model fitted <b>45 search terms chosen from 50 million '
              'candidates</b> against 1,152 data points, so it learned winter rather than '
              'influenza &mdash; high-school basketball season correlates beautifully with flu '
              'season. It missed the non-seasonal 2009 H1N1 pandemic entirely, then overestimated '
              'CDC influenza-like-illness in <b>100 of 108 weeks</b> from August 2011, at one '
              'point predicting more than double the true share of doctor visits. A lagged '
              'autoregression on CDC data alone beat it: mean absolute error 0.311 against 0.486. '
              '(Lazer et al., <i>Science</i> 343, 2014.)'),
        drills=[
            dict(q='You regress churn on promo exposure and find promos reduce churn. What is wrong?',
                 a=('<b>The coefficient is a selection artefact, and you cannot sign the bias.</b> '
                    'Promos are targeted, not randomised: if the targeting model picked users '
                    'predicted to churn, exposure is downstream of a churn risk score you may not '
                    'even have as a column; if it picked engaged users, exposure is downstream of '
                    'engagement. Either way there is an open backdoor path $\\text{promo} '
                    '\\leftarrow \\text{targeting score} \\rightarrow \\text{churn}$. Propose a '
                    'randomised holdout inside the targeted population, or an encouragement design '
                    'that randomises the nudge rather than the promo.'),
                 a_simple=('<b>The promos were aimed, not tossed at random, so the comparison is '
                           'rigged.</b> Whoever chose who got a promo chose using something '
                           '&mdash; a predicted risk of leaving, or how engaged someone already '
                           'was &mdash; and that same something drives churn on its own. You are '
                           'comparing two groups that were different before the promo arrived. '
                           'The fix is to hold back a slice of the targeted users at random and '
                           'send them nothing.')),
            dict(q='Estimating the effect of Instant Book on host bookings, you control for the number of enquiries. Is that OK?',
                 a=('<b>No &mdash; enquiries are downstream of Instant Book.</b> They are a '
                    'mediator: part of how the feature produces bookings is by changing the '
                    'enquiry flow, so conditioning on them strips out the effect you were hired to '
                    'measure and leaves a direct effect nobody asked for. Worse, enquiries are '
                    'also caused by unobserved host quality, so conditioning on them opens a '
                    'collider path and biases what is left. Pre-treatment covariates only: '
                    'listing age, market, price band.'),
                 a_simple=('<b>No &mdash; enquiries happen because of the feature, so holding them '
                           'fixed throws the answer away.</b> Part of how Instant Book creates '
                           'bookings is by changing how many enquiries come in. Freeze that and '
                           'you have measured the feature with its main route to the outcome '
                           'switched off. Control only for things that were already true before '
                           'the feature was switched on: how old the listing is, which city, what '
                           'price band.')),
            dict(q='Among users who converted, ad relevance and discount size are negatively correlated. Is a good ad a substitute for a discount?',
                 a=('<b>No &mdash; you conditioned on a collider and manufactured that '
                    'correlation.</b> Conversion is a common effect of both, '
                    '$\\text{relevance} \\rightarrow \\text{convert} \\leftarrow \\text{discount}$. '
                    'Inside the converted group, a weak ad has to be paired with a big discount to '
                    'have got there at all, so the two look like substitutes even if they were '
                    'independent in the population. Recompute on everyone who saw an ad. If you '
                    'want the substitution question answered, you need a design that varies one '
                    'while holding the other.'),
                 a_simple=('<b>No &mdash; the pattern is made by looking only at the winners.</b> '
                           'To end up in the converted group you needed either a good ad or a big '
                           'discount, so within that group the people with weak ads are exactly '
                           'the ones who got large discounts. The trade-off is an artefact of who '
                           'you kept. Look at everyone who saw an ad and it disappears.')),
        ],
        anchor=dict(
            formula=r'$X \leftarrow C \rightarrow Y$ &nbsp;&middot;&nbsp; $X \rightarrow M \rightarrow Y$ &nbsp;&middot;&nbsp; $X \rightarrow K \leftarrow Y$',
            formula_simple='Both arrows point out of it: hold it fixed. The arrows run through it: '
                           'leave it alone. Both arrows point into it: touching it invents the link.',
            bullets=[
                'A pre-treatment common cause is the only one of the three you fix by adding it to the regression',
                'Anything measured after the treatment is a mediator or a collider, and both make the estimate worse',
                'Conditioning on a shared consequence creates correlation between things that were independent',
            ]),
        chips=['confounding', 'backdoor criterion', 'bad controls', 'Berkson&rsquo;s paradox',
               'difference-in-differences'],
        followup='You regress churn on promo exposure and find promos reduce churn. What&rsquo;s wrong?',
    ),

    # ------------------------------------------------------------------ F7
    dict(
        id='expected-value',
        tier='foundation',
        title='Expected value and the linearity trick',
        kicker='Linearity holds whether or not the pieces are independent &mdash; that one fact solves most of the brainteasers, and the follow-up is always "now the variance"',
        simple=[
            'The average of a total is the total of the averages. Always. It does not matter '
            'whether the pieces are related, whether they nudge each other, whether one makes the '
            'next more likely. Work out the average of each piece and add them up. That single '
            'fact answers most of the puzzles interviewers use to find out whether you can think '
            'in probability rather than recite it.',
            'The standard move is to chop the thing you were asked about into a pile of tiny '
            'yes-or-no events, find the chance of each, and add those chances. Ten letters '
            'shuffled into ten addressed envelopes: how many arrive correctly? Each letter has '
            'one chance in ten and there are ten letters, so on average exactly one arrives. '
            'That is true for a hundred letters and for a million. The letters are very much not '
            'independent &mdash; if nine are right the tenth must be &mdash; and it changes '
            'nothing. Where relatedness bites is the <i>spread</i> of outcomes, and the spread is '
            'what you get asked about next.',
        ],
        analogy=('<b>Like a relay team.</b> The expected total time is the four expected leg times '
                 'added together, even though the runners feed off each other and a bad handover '
                 'in leg two drags leg three with it. Ask instead how <i>unpredictable</i> the '
                 'total is, and suddenly you do have to know whether those legs move together.'),
        trap_simple=('Getting the average right, then working out the spread as though the pieces '
                     'were unrelated, without saying so out loud. The interviewer is not checking '
                     'your arithmetic. They are listening for whether you noticed you had made an '
                     'assumption.'),
        tech=[
            'Two facts, and the interview lives in the gap between them. '
            '$E\\bigl[\\sum_i X_i\\bigr] = \\sum_i E[X_i]$ holds under any dependence at all. '
            '$\\mathrm{Var}\\bigl(\\sum_i X_i\\bigr) = \\sum_i \\mathrm{Var}(X_i) + '
            '\\sum_{i \\neq j} \\mathrm{Cov}(X_i, X_j)$ does not. So the move on nearly every '
            'brainteaser is the same: write the quantity as a sum of indicator variables, take '
            'expectations term by term, add. Dependence between the indicators is irrelevant, and '
            'you should say that out loud rather than quietly assuming it away.',
            'The canonical setup: $n$ letters dropped at random into $n$ addressed envelopes, with '
            '$I_i$ equal to 1 when letter $i$ lands correctly. $E[I_i] = 1/n$, so the expected '
            'number of matches is $n \\cdot 1/n = 1$ &mdash; for every $n$, forever. The '
            'indicators are heavily dependent, since if $n-1$ match the last one must. Now the '
            'follow-up. $\\mathrm{Var}(I_i) = \\tfrac{1}{n}\\bigl(1-\\tfrac{1}{n}\\bigr)$ and '
            '$\\mathrm{Cov}(I_i,I_j) = \\tfrac{1}{n(n-1)} - \\tfrac{1}{n^2}$, and those covariance '
            'terms sum to exactly $1/n$, so the variance is exactly 1 as well. Assume independence '
            'and you report $1 - 1/n$: 0.9 at $n = 10$. Close enough to pass unnoticed, wrong for '
            'a reason you should be able to name on the spot.',
        ],
        tech_note=('Two more tools finish the family. The law of total expectation, '
                   '$E[X] = E\\bigl[E[X \\mid Y]\\bigr]$, handles anything with a random stopping '
                   'rule: condition on the first step and recurse. And the standard means and '
                   'variances should be instant &mdash; Bernoulli $p$ and $p(1-p)$, Poisson '
                   '$\\lambda$ and $\\lambda$, exponential $1/\\lambda$ and $1/\\lambda^2$, '
                   'geometric $1/p$. Coupon collector falls straight out of the same decomposition: '
                   'collecting all ten takes $10\\bigl(1 + \\tfrac12 + \\dots + \\tfrac{1}{10}\\bigr) '
                   '\\approx 29.3$ draws, a sum of ten independent geometric waits.'),
        fig=dict(
            kind='blocks',
            h=224,
            boxes=[
                dict(x=34, y=52, w=132, h=50, t='10 letters', sub='10 envelopes, shuffled'),
                dict(x=206, y=52, w=140, h=50, t='one flag per letter', sub='1 if it lands right'),
                dict(x=386, y=52, w=132, h=50, t='each flag: 1 in 10', sub='chance of a match'),
                dict(x=558, y=52, w=128, h=50, t='expectation: 1', sub='for every n', tone='mem'),
                dict(x=34, y=142, w=200, h=50, t='now the variance', sub='the flags are dependent'),
                dict(x=274, y=142, w=190, h=50, t='assume independence', sub='you get 0.9', tone='sig'),
                dict(x=504, y=142, w=182, h=50, t='add the covariances', sub='you get exactly 1.0', tone='mem'),
            ],
            links=[
                dict(a=0, b=1, label='split'), dict(a=1, b=2, label='each'),
                dict(a=2, b=3, label='add', tone='mem'),
                dict(a=4, b=5, label='skip', tone='sig'), dict(a=5, b=6, label='fix', tone='mem'),
            ],
            labels=[
                dict(x=34, y=40, t='expectation: no independence needed', a='start', tone='mem'),
                dict(x=34, y=130, t='variance: the covariance terms do not vanish', a='start', tone='sig'),
            ],
            foot='the same ten flags in both rows; only the bottom row needs to know they interact',
            alt='Two rows of boxes. The top row decomposes ten letters into ten yes-or-no flags, '
                'each with a one in ten chance, adding to an expectation of exactly one. The '
                'bottom row shows the same flags feeding a variance calculation: assuming '
                'independence gives 0.9, adding the covariance terms gives exactly 1.0.'),
        caption=('The top row never asks whether the flags interact, because it does not need to. '
                 'The bottom row does, and skipping that question costs you a tenth of the answer '
                 'here and a factor of ten on a real clustered metric.'),
        caption_simple=('Both rows use the same ten yes-or-no flags. Only the bottom row &mdash; '
                        'the spread &mdash; has to care that the flags push each other around.'),
        when=[
            'A brainteaser starts "what is the expected number of..."',
            'You have produced an expectation and the interviewer says "now the variance"',
            'A metric is a sum over events that are obviously not independent: sessions per user, tokens per request',
            'You are about to multiply two probabilities that came from the same people',
        ],
        trap=('Computing a variance as if the pieces were independent when the problem never said '
              'they were, and not flagging it. The damaging version is silent: you write down the '
              'sum of the variances and move on. In the envelope problem that hands you 0.9 '
              'instead of 1.0. On a real metric &mdash; forty sessions from the same user &mdash; '
              'it hands you a standard error that is far too small, a p-value that is far too '
              'small, and a launch decision built on noise.'),
        math=dict(
            tex=r'E\Bigl[\sum_i X_i\Bigr] = \sum_i E[X_i] \qquad \mathrm{Var}\Bigl(\sum_i X_i\Bigr) = \sum_i \mathrm{Var}(X_i) + \sum_{i \neq j} \mathrm{Cov}(X_i, X_j)',
            note='The left equation has no assumptions attached to it. The right one has exactly '
                 'one, and it is hiding in the second term: drop it and you are claiming '
                 'independence you were never given.',
            cost='one sum is free, the other costs you every pair'),
        code=dict(
            label='Ten letters, ten envelopes: check the expectation and the variance',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
                 'n, trials = <span class="s">10</span>, <span class="s">200_000</span>\n'
                 'matches = np.array([(rng.permutation(n) == np.arange(n)).sum()\n'
                 '                    <span class="k">for</span> _ <span class="k">in</span> '
                 '<span class="k">range</span>(trials)])\n\n'
                 '<span class="k">print</span>(matches.mean())        '
                 '<span class="c"># 1.00 -- and it is 1.00 for every n</span>\n'
                 '<span class="k">print</span>(matches.var(ddof=<span class="s">1</span>))  '
                 '<span class="c"># 1.00 -- the covariance terms put the missing 1/n back</span>\n'
                 '<span class="k">print</span>(<span class="s">1</span> - <span class="s">1</span>/n)          '
                 '<span class="c"># 0.90 -- what independence would have told you</span>')),
        real=('Airbnb&rsquo;s experimentation platform. Their own writeup opens with a price-filter '
              'test that was a significant <b>+4% at day seven</b> and null by the time it '
              'finished. The fix they built was a dynamic p-value threshold obtained by '
              '<i>simulating</i> varying real effect sizes, variances and certainty levels, rather '
              'than deriving a closed form &mdash; the honest response when the expectation you '
              'need has no clean formula behind it. (Airbnb Engineering, <i>Experiments at '
              'Airbnb</i>.)'),
        drills=[
            dict(q='Ten letters are dropped at random into ten addressed envelopes. How many arrive correctly on average, and does your answer need them to be independent?',
                 a=('<b>Exactly 1, and no.</b> Define $I_i = 1$ when letter $i$ lands correctly. '
                    'Each envelope is equally likely to receive any letter, so $E[I_i] = 1/10$, '
                    'and $E\\bigl[\\sum_i I_i\\bigr] = \\sum_i E[I_i] = 10 \\cdot 1/10 = 1$ by '
                    'linearity alone. The indicators are strongly dependent &mdash; nine matches '
                    'force the tenth &mdash; and linearity never asked. The same argument gives 1 '
                    'for any $n$, which is the part that surprises people.'),
                 a_simple=('<b>Exactly one, and no.</b> Give every letter a flag that is on when it '
                           'lands in the right envelope. Each flag has one chance in ten of being '
                           'on, and there are ten of them, so on average one flag is on. Adding '
                           'averages never requires the flags to be unrelated &mdash; and here '
                           'they are wildly related, since nine correct letters force the tenth. '
                           'The answer is one for a million letters too.')),
            dict(q='Now compute the variance.',
                 a=('<b>Also exactly 1 &mdash; not the 0.9 you get by assuming independence.</b> '
                    '$\\sum_i \\mathrm{Var}(I_i) = 10 \\cdot \\tfrac{1}{10}\\bigl(1 - '
                    '\\tfrac{1}{10}\\bigr) = 0.9$. But $\\mathrm{Cov}(I_i, I_j) = '
                    '\\tfrac{1}{n(n-1)} - \\tfrac{1}{n^2}$, and there are $n(n-1)$ such pairs, so '
                    'they contribute exactly $1/n = 0.1$. Total: 1.0. The point is not the tenth '
                    'of a unit &mdash; it is that you were asked for the assumption, and the '
                    'covariance term is where it lived.'),
                 a_simple=('<b>Also exactly one, not the nine tenths independence would give '
                           'you.</b> Add up how much each flag wobbles on its own and you get nine '
                           'tenths. But the flags push each other: one letter landing right makes '
                           'the others slightly more likely to land right too. Adding those '
                           'interactions back contributes exactly the missing tenth. The number '
                           'matters less than noticing the interactions exist.')),
            dict(q='Your metric is total sessions per user over a week, and you need a standard error. Where does linearity stop helping?',
                 a=('<b>At the variance, immediately.</b> The expected weekly total is still the '
                    'sum of the expected daily totals, dependence and all. The standard error is '
                    'not: sessions from one user are positively correlated across days, so the '
                    'covariance terms are large and positive and dropping them understates the '
                    'variance badly. Aggregate to the randomisation unit first, or use '
                    'cluster-robust errors, or bootstrap users rather than rows. The design effect '
                    'is $1 + (m-1)\\rho$.'),
                 a_simple=('<b>At the spread, immediately.</b> The weekly average is still just the '
                           'daily averages added up, and nothing goes wrong there. The uncertainty '
                           'is another matter: one heavy user contributes seven days that all look '
                           'alike, so those days are not seven independent pieces of evidence. '
                           'Roll the data up to one row per user before you compute uncertainty, '
                           'or your error bars will be far too narrow.')),
        ],
        anchor=dict(
            formula=r'$E[X+Y] = E[X] + E[Y]$ &nbsp;always&nbsp;&middot;&nbsp; $\mathrm{Var}(X+Y) = \mathrm{Var}(X) + \mathrm{Var}(Y) + 2\,\mathrm{Cov}(X,Y)$',
            formula_simple='Averages of a total always add up. Spreads only add up when the pieces '
                           'do not move together.',
            bullets=[
                'Chop the quantity into yes-or-no indicators, take each average, add &mdash; dependence never enters',
                'The moment you want a variance you owe the room a covariance term or an explicit independence assumption',
                'Ten letters in ten envelopes: expectation 1 for every n, and the variance is 1 too, not 0.9',
            ]),
        chips=['linearity of expectation', 'indicator variables', 'law of total expectation',
               'covariance', 'clustered standard errors'],
        followup='Now compute the variance.',
    ),

    # ------------------------------------------------------------------ F8
    dict(
        id='long-tails',
        tier='foundation',
        title='Long tails break averages and break models',
        kicker='The mean sits in a gap where nobody lives, the median is not the business metric, and the loss you trained on quietly picked one of them for you',
        simple=[
            'Some quantities are lopsided. Most requests are fast and a few are enormously slow; '
            'most customers spend a little and a few spend thousands. When a quantity looks like '
            'that, the average stops describing anybody. Half your requests can finish inside a '
            'tenth of a second while the average sits about two thirds higher, dragged up by the '
            'slow ones &mdash; and one request in a hundred takes six times the average.',
            'Two things break as a result. First, a promise written as "the average response is '
            'under two hundred milliseconds" is comfortably true while one customer in a hundred '
            'waits nearly a second and writes in about it. What people actually feel is the '
            'slowest few percent, so that is the number that belongs in the target. Second, a '
            'model trained to minimise squared error is trying to get the average right, and in a '
            'lopsided world the average is decided by a handful of extreme rows. If the decision '
            'you care about is the typical case, or the slow tail, train something that aims at '
            'that instead.',
        ],
        analogy=('<b>Like the average salary in a small bar.</b> Nine people on thirty thousand '
                 'and one billionaire walk in, and the average salary in the room is now over a '
                 'hundred million. Every number is correct and the average describes nobody '
                 'present. Ask what the person in the middle earns, and what the top earner '
                 'earns, and you have actually described the bar.'),
        trap_simple=('Squashing a lopsided quantity onto a compressed scale, fitting the model '
                     'there, and reporting the improvement as if it were a percentage change in '
                     'money. It is not. Squashing and un-squashing does not hand back the average '
                     '&mdash; it hands back a different, smaller number, and finance will notice '
                     'when the revenue fails to appear.'),
        tech=[
            'Heavy tails attack the estimate before they attack the model. The central limit '
            'theorem is about the sampling distribution of the mean, and how fast it gets there '
            'depends on skewness: Kohavi&rsquo;s rule of thumb is that you need at least '
            '$355 s^2$ users per arm, where $s$ is the skewness coefficient. Bing&rsquo;s '
            'revenue-per-user has $s = 17.9$, which is roughly <b>114,000 users per arm</b> just '
            'to reach 4.4% sensitivity. Capping the metric cut skewness from 18 to 5.3 &mdash; '
            'about an elevenfold cut in the sample size needed, bought with a bias you must '
            'declare before you look at the data, not after.',
            'Then the two production consequences. An SLO on <i>mean</i> latency is satisfiable '
            'while the slowest 1% of requests are an order of magnitude worse, which is why p95 or '
            'p99 latency, never the mean, is the guardrail teams actually write down. And squared '
            'error estimates a conditional mean, so on a heavy-tailed target the loss is dominated '
            'by a handful of rows and the fit chases them: if the decision is about a typical case '
            'or a specific quantile, use absolute error or quantile (pinball) loss, or model the '
            'tail explicitly. $\\log(1+x)$ is not a free lunch either &mdash; you are then '
            'estimating the mean of the logs, which exponentiates back to a geometric mean, not to '
            'revenue.',
        ],
        tech_note=('Reporting is where this costs money. You cannot exponentiate the mean of the '
                   'logs and call it a revenue lift; use Duan&rsquo;s smearing estimator or fit on '
                   'the raw scale. And do not reach for Mann-Whitney "because the data are not '
                   'normal": it tests stochastic dominance, while the business metric is a mean, '
                   'so you have quietly answered a different question and nobody in the room will '
                   'catch it except the interviewer.'),
        fig=dict(
            kind='plot',
            head=['WHAT THE AVERAGE HIDES', 'WHAT THE USER FEELS'],
            xr=(0, 1100), yr=(0, 0.19), ph=190,
            xlab='request latency, ms', ylab='share of requests',
            xticks=[(0, '0'), (95, '95'), (157, '157'), (500, '500'), (970, '970')],
            yticks=[(0.05, '5%'), (0.10, '10%'), (0.15, '15%')],
            bands=[dict(x0=492, x1=1100, tone='sig', label='the slowest 5%', op=0.09)],
            vlines=[dict(x=95, tone='mem', label='p50'),
                    dict(x=157, tone='sig', label='mean'),
                    dict(x=970, tone='sig', label='p99')],
            curves=[dict(pts=[(0, 0.0), (10, 0.079), (20, 0.148), (30, 0.171), (40, 0.172),
                              (50, 0.162), (60, 0.150), (70, 0.136), (85, 0.117), (95, 0.105),
                              (110, 0.090), (130, 0.073), (157, 0.056), (180, 0.045),
                              (220, 0.032), (260, 0.023), (320, 0.015), (400, 0.009),
                              (500, 0.005), (600, 0.003), (700, 0.002), (800, 0.0013),
                              (970, 0.0007), (1100, 0.0005)],
                        tone='plain', fill=True)],
            marks=[dict(x=95, y=0.105, label='95 ms', tone='mem', dx=-8, dy=-2, la='end'),
                   dict(x=157, y=0.056, label='157 ms', tone='sig', dx=8, dy=-8),
                   dict(x=970, y=0.0007, label='970 ms', tone='sig', dx=6, dy=-10)],
            foot='half the requests finish by 95 ms, the average is 157 ms, and one in a hundred waits 970 ms',
            alt='A right-skewed latency distribution with a tall early peak and a long thin tail. '
                'Dashed lines mark the median at 95 milliseconds, the mean at 157 milliseconds and '
                'the 99th percentile at 970 milliseconds, with the slowest five percent shaded.'),
        caption=('The mean is not in the middle of anything. It sits between the bulk and the tail, '
                 'about 65% above the median and about a sixth of the way to the p99 &mdash; which '
                 'is why an SLO written on it is satisfied by a system that is failing for one user '
                 'in a hundred.'),
        caption_simple=('The average sits in the gap between the crowd on the left and the stragglers '
                        'on the right. It describes neither group, and a promise written on it is '
                        'satisfied by a system that is already failing for one user in a hundred.'),
        when=[
            'Someone proposes an average as a service level target',
            'The metric is revenue per user, session length, items per order or tokens per request',
            'A model looks excellent on validation and the money never appears',
            'A team wants a t-test on bookings per user, which is zero-inflated and heavily skewed',
        ],
        trap=('Reporting a mean lift computed on log-transformed data as if it were a percentage '
              'lift in revenue. The sentence is usually <i>"revenue is up 6% in the model"</i> '
              '&mdash; it is not; the model moved the mean of the logs, which is a geometric mean '
              'and a smaller number on the raw scale. Its close cousin is "n is over thirty so the '
              'central limit theorem applies", said about a metric with a skewness of 18 and 30,000 '
              'users per arm.'),
        math=dict(
            tex=r'n_{\text{per arm}} \geq 355\,s^2 \qquad s_{\text{Bing revenue/user}} = 17.9 \;\Rightarrow\; n \approx 114{,}000',
            note='Skewness enters squared, so the metric definition is a sample-size decision. '
                 'Capping took Bing from 18 to 5.3 and cut the requirement by about elevenfold '
                 'without touching traffic.',
            cost='a bias you declare in advance, in exchange for an order of magnitude'),
        code=dict(
            label='The three numbers to quote instead of the mean',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
                 '<span class="c"># latency in ms: median 95, lognormal with sigma = 1</span>\n'
                 'ms = rng.lognormal(mean=np.log(<span class="s">95</span>), sigma=<span class="s">1.0</span>, size=<span class="s">2_000_000</span>)\n\n'
                 '<span class="k">for</span> q <span class="k">in</span> (<span class="s">50</span>, <span class="s">95</span>, <span class="s">99</span>):\n'
                 '    <span class="k">print</span>(q, <span class="k">round</span>(np.percentile(ms, q)))  '
                 '<span class="c"># 95, 492, 973</span>\n'
                 '<span class="k">print</span>(<span class="k">round</span>(ms.mean()))            '
                 '<span class="c"># 157 -- above 65% of your traffic</span>\n'
                 '<span class="k">print</span>(<span class="k">round</span>(np.exp(np.log(ms).mean())))  '
                 '<span class="c"># 95 -- the geometric mean is the MEDIAN, not the mean</span>')),
        real=('Long Term Capital Management, 1998. Models calibrated on normal-tailed volatility '
              'gave near-zero probability to a joint Russian default and flight to quality; LTCM '
              'lost <b>4.6 billion dollars in under four months</b> and was recapitalised that '
              'September in a 3.6 billion dollar Fed-brokered rescue. The lesson is that tails and '
              'correlations are not stable across regimes. The everyday version is '
              'Microsoft&rsquo;s: Bing&rsquo;s revenue per user has a skewness of <b>17.9</b>, so '
              'a t-test on it needs about 114,000 users per arm before the normal approximation is '
              'worth anything.'),
        drills=[
            dict(q='You transformed revenue with log1p and the model looks great. How do you report the business impact?',
                 a=('<b>Not by exponentiating the coefficient.</b> Fitting on $\\log(1+y)$ '
                    'estimates $E[\\log(1+Y)]$, and $\\exp$ of that is a geometric mean &mdash; '
                    'systematically below the arithmetic mean that revenue actually is, by roughly '
                    'a factor of $\\exp(\\sigma^2/2)$ on a lognormal. Either apply Duan&rsquo;s '
                    'smearing estimator to retransform, or fit on the raw scale with a heavy-tail-'
                    'aware model. Then report the lift as a difference in mean revenue per user '
                    'with a bootstrap interval, because that is the number finance will book.'),
                 a_simple=('<b>Not by undoing the squash and calling it money.</b> Fitting on the '
                           'compressed scale gets you the average of the compressed numbers, and '
                           'un-compressing that gives you something closer to the middle customer '
                           'than to the average customer &mdash; always smaller, sometimes far '
                           'smaller. Either correct for that with a known adjustment, or fit on '
                           'the money itself and quote the change in revenue per user with an '
                           'honest range around it.')),
            dict(q='Your p50 latency is 95 ms, your mean is 157 ms and your p99 is 970 ms. The SLO says "average under 200 ms". What do you do?',
                 a=('<b>Change the SLO before you change the system.</b> You are passing a target '
                    'that is blind to the failure: the mean is 157 ms with 43 ms of headroom while '
                    'one request in a hundred is 970 ms, and no amount of tail improvement or tail '
                    'degradation will move that headroom much. Rewrite the objective on p95 and '
                    'p99, set the threshold from a backtest of historical days rather than a round '
                    'number, and keep the mean as a cost proxy, not a promise.'),
                 a_simple=('<b>Change the promise before you change the system.</b> The target is '
                           'measuring the wrong thing: the average has plenty of room to spare '
                           'while one request in a hundred takes ten times the typical wait, and '
                           'fixing those slow requests barely moves the average at all. Write the '
                           'promise on the slowest few percent, and pick the threshold from what '
                           'your system has actually done on past days.')),
            dict(q='Bookings per user is heavily right-skewed with a big spike at zero and the team wants a t-test. Your approach?',
                 a=('<b>The t-test is not automatically wrong &mdash; it is wrong at your sample '
                    'size.</b> Compute the skewness and compare with $355 s^2$ per arm. If you '
                    'clear it, Welch is fine and it is a mean, which is what the business wants. '
                    'If you do not, in order: cap or winsorise at a pre-declared percentile, or '
                    'bootstrap the difference in means at the user level, or decompose into '
                    '$P(\\text{book}) \\times E[\\text{bookings} \\mid \\text{book}]$ and test '
                    'both. Do not switch to Mann-Whitney and then report a mean lift.'),
                 a_simple=('<b>It depends on one number, and you can go and get it.</b> Measure how '
                           'lopsided the metric is and work out how many users per arm that '
                           'lopsidedness demands. Clear that bar and the ordinary test is fine. '
                           'Miss it and your options are to trim the extreme values at a limit you '
                           'set in advance, to resample users to get an honest range, or to split '
                           'the question into who books at all and how much bookers book.')),
        ],
        anchor=dict(
            formula=r'$n \geq 355\,s^2$ &nbsp;&middot;&nbsp; $\exp\bigl(E[\log Y]\bigr) \neq E[Y]$',
            formula_simple='Lopsidedness enters the sample size squared. And un-squashing an '
                           'average never gives you back the average you started with.',
            bullets=[
                'The mean of a heavy-tailed metric is set by a handful of rows, so it converges slowly and moves for the wrong reasons',
                'Put the SLO on p95 or p99; the mean is a cost proxy, not a promise anyone feels',
                'Squared error targets a conditional mean &mdash; if you want the middle or the tail, change the loss, not the data',
            ]),
        chips=['skewness and the CLT', 'capping and winsorising', 'quantile regression',
               'bootstrap intervals', 'Duan smearing'],
        followup='You transformed revenue with log1p and the model looks great. How do you report the business impact?',
    ),

    # ------------------------------------------------------------------ F9
    dict(
        id='sampling-bias',
        tier='foundation',
        title='Sampling: which bias are you buying',
        kicker='Every dataset was collected by a process, and the process &mdash; not the row count &mdash; decides what you are allowed to conclude',
        simple=[
            'Every dataset was gathered somehow, and the gathering is what limits what you can '
            'say. Three ways it goes wrong, and you should be able to name which one you are '
            'holding within a sentence. <b>Selection</b>: the list you drew from was never the '
            'group you care about. <b>Survivorship</b>: the things that failed are not in the '
            'file, so you are studying the winners and calling it a study of everyone. '
            '<b>Non-response</b>: you asked everybody but only a certain kind of person answered, '
            'and whether they answered is related to the very thing you were asking about.',
            'Here is the part that matters. None of these gets better with more rows. Collect ten '
            'times as much data and your uncertainty gets narrower around a number that is still '
            'tilted, which is worse than being loudly unsure. The production version is the one '
            'that catches people in interviews: your labelled examples are whatever somebody '
            'reviewed, and what somebody reviewed is whatever the old model flagged. So the first '
            'question about any dataset is not how big it is. It is who is missing.',
        ],
        analogy=('<b>Like judging a restaurant from its reviews.</b> The people who bothered to '
                 'write either loved it or were furious; everyone who had an unremarkable dinner '
                 'went home and said nothing. Read a thousand reviews instead of ten and you learn '
                 'the split between delighted and outraged very precisely. You still learn nothing '
                 'about the average dinner.'),
        trap_simple=('Saying the dataset is far too large for this to be a problem. Size and tilt '
                     'are different things: more rows shrink the wobble in your estimate and do '
                     'nothing whatsoever to the tilt. The largest election poll ever run at the '
                     'time got 1936 spectacularly wrong, and a survey one forty-eighth its size '
                     'got it right.'),
        tech=[
            'Learn the names so you can classify out loud in one sentence: <b>selection</b> (the '
            'sampling frame is not the target population), <b>survivorship</b> (units that failed '
            'left the dataset), <b>non-response</b> (responding is correlated with the outcome), '
            '<b>under-coverage</b>, <b>length-biased sampling</b> (sample moments rather than '
            'sessions and long sessions are over-represented), and <b>collider or Berkson</b> bias '
            '(you conditioned on a common effect). None of them is a variance problem. Bias does '
            'not shrink with $n$ &mdash; the standard error goes as $n^{-1/2}$ and the bias goes '
            'as $n^{0}$ &mdash; so more data buys a tighter interval around the wrong number. '
            'Lazer calls this big data hubris.',
            'Then the design vocabulary, because the follow-up asks what you would do instead. '
            '<b>Stratified</b> sampling lowers variance when the strata genuinely differ and lets '
            'you guarantee coverage of a small group you care about. <b>Cluster</b> sampling is '
            'cheaper per unit, raises variance, and forces clustered standard errors downstream. '
            'In an ML system the training set is a survey nobody designed: ask who is missing '
            'before you ask what your AUC is. The production form is a loop &mdash; your labels '
            'are whatever got reviewed, and what got reviewed is whatever the previous model '
            'flagged.',
        ],
        tech_note=('The fix for the label loop is boring and it is the answer they want: hold out '
                   'a small randomly chosen slice of traffic that bypasses the model entirely and '
                   'gets reviewed anyway. It costs you a known and budgetable amount of fraud, and '
                   'it is the only source of an unbiased prevalence estimate you will ever have. '
                   'Without it, the model&rsquo;s estimate of the fraud it already blocks decays '
                   'towards zero and it stops blocking it.'),
        fig=dict(
            kind='blocks',
            h=292,
            boxes=[
                dict(x=34, y=52, w=140, h=46, t='all US voters', sub='the 1936 electorate'),
                dict(x=204, y=52, w=160, h=46, t='phone books, car lists', sub='the sampling frame'),
                dict(x=394, y=52, w=140, h=46, t='10M ballots sent', sub='2.4M came back'),
                dict(x=564, y=52, w=122, h=46, t='Landon 57-43', sub='the answer', tone='sig'),
                dict(x=204, y=142, w=160, h=46, t='no phone, no car', sub='most 1936 voters', tone='sig'),
                dict(x=394, y=142, w=140, h=46, t='the 76% silent', sub='who never replied', tone='sig'),
                dict(x=34, y=216, w=652, h=46, t='Roosevelt: 61% and 46 of the 48 states',
                     sub='Gallup called it with about 50,000 people', tone='mem'),
            ],
            links=[
                dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3, tone='sig'),
                dict(a=1, b=4, side='down', tone='sig'),
                dict(a=2, b=5, side='down', tone='sig'),
            ],
            labels=[
                dict(x=34, y=26, t='2.4 million replies, and the wrong answer', a='start', tone='sig'),
                dict(x=34, y=130, t='who never entered the sample', a='start', tone='sig'),
            ],
            foot='the tilt came from the frame and the non-reply, and 2.4 million rows did nothing about either',
            alt='A pipeline from all US voters, through a sampling frame of telephone books and '
                'car registrations, to ten million ballots of which 2.4 million returned, ending '
                'in the prediction Landon 57 to 43. Two boxes drop below it showing who was '
                'excluded: people with no phone and no car, and the 76% who never replied. A wide '
                'box underneath gives the truth, Roosevelt on 61% and 46 of 48 states, called by '
                'Gallup from about 50,000 people.'),
        caption=('Two exclusions, stacked. The frame removed most of the 1936 electorate before a '
                 'single ballot went out, and the response rate removed three quarters of what was '
                 'left &mdash; and both exclusions correlate with how people voted. No sample size '
                 'repairs either.'),
        caption_simple=('Two groups were dropped before anyone counted anything: people with no '
                        'telephone and no car, and the three quarters who never posted the ballot '
                        'back. Both groups voted differently from the ones who stayed in, so the '
                        'answer was wrong before it was tallied.'),
        when=[
            'Someone justifies a conclusion with the size of the dataset',
            'Your labelled data came out of a review queue',
            'A survey, a feedback widget or a thumbs-up rate is being read as the population',
            'You are retraining on outcomes that only exist for the cases the last model let through',
        ],
        trap=('<i>"We have 500 million rows, so sampling bias is not an issue."</i> Row count is a '
              'statement about variance and this is a statement about bias; the two do not trade. '
              'The ML mirror image is just as common: "the test set is held out, so it is '
              'unbiased" &mdash; held out from a training set that was itself drawn from whoever '
              'the old system happened to serve, and reviewed by whoever the old system happened '
              'to flag.'),
        math=dict(
            tex=r'\mathrm{SE} \propto n^{-1/2} \qquad \text{bias} \propto n^{0} \qquad \mathrm{MSE} = \text{bias}^2 + \text{variance}',
            note='Only one of the two terms responds to more data. Past a certain n the whole error '
                 'is the term your sampling process put there, and the confidence interval is a '
                 'precise statement about the wrong quantity.',
            cost='a design question, never an estimator question'),
        code=dict(
            label='The label loop, in one retraining cycle',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
                 'fraud = rng.random(<span class="s">200_000</span>) &lt; <span class="s">0.01</span>  '
                 '<span class="c"># the truth: 1% of traffic</span>\n'
                 'score = rng.normal(<span class="s">2.5</span> * fraud, <span class="s">1.0</span>)   '
                 '<span class="c"># the model you already run</span>\n'
                 'passed = score &lt; np.quantile(score, <span class="s">0.98</span>)  '
                 '<span class="c"># you block the top 2%</span>\n\n'
                 '<span class="k">print</span>(fraud.mean())          '
                 '<span class="c"># 0.0102 -- the world</span>\n'
                 '<span class="k">print</span>(fraud[passed].mean())  '
                 '<span class="c"># 0.0041 -- what your next training set sees</span>\n'
                 '<span class="c"># retrain on `passed` and the model learns fraud is rare.</span>\n'
                 '<span class="c"># do it three times and it learns fraud is gone.</span>')),
        real=('The <i>Literary Digest</i> poll of the 1936 US presidential election. It collected '
              '<b>2.4 million replies</b>, the largest poll ever run at that point, and predicted '
              'Landon over Roosevelt 57&ndash;43. Roosevelt took <b>61% of the popular vote and 46 '
              'of the 48 states</b>. The frame was telephone books and car registrations &mdash; '
              'wealthy, in 1936 &mdash; and only about 24% of ballots came back. Gallup called the '
              'same election correctly with roughly 50,000 people, one forty-eighth of the sample.'),
        drills=[
            dict(q='You retrain a fraud model on the transactions your current model let through. What happens over three retraining cycles?',
                 a=('<b>The measured prevalence of the fraud you already block collapses towards '
                    'zero, and then you stop blocking it.</b> The training set is conditioned on '
                    '"not blocked", which removes exactly the positives the model is good at '
                    'catching. Each cycle the estimated base rate for that pattern falls, the '
                    'decision threshold drifts, more of it gets through, and the loop closes. Fix '
                    'it with a randomised holdout that bypasses the model and is labelled anyway, '
                    'plus delayed chargeback labels on the blocked stream where you can get them.'),
                 a_simple=('<b>The model stops believing in the fraud it is best at catching, and '
                           'then it lets it through.</b> You only ever see what got past the '
                           'current model, so the kinds of fraud it catches well are missing from '
                           'the next training set. Each round the model concludes that pattern is '
                           'rarer than it is, relaxes, and lets a bit more through. The fix is to '
                           'let a small random slice of traffic past unchecked on purpose and '
                           'review it anyway.')),
            dict(q='A colleague says "we have 500 million rows, so sampling bias is not an issue". Respond.',
                 a=('<b>Row count controls variance; it does nothing to bias.</b> The standard '
                    'error falls as $n^{-1/2}$ while the bias is $O(1)$ in $n$, so at 500 million '
                    'rows your confidence interval is a very precise statement about the wrong '
                    'quantity &mdash; and precision makes the error harder to argue with, not '
                    'easier to spot. The right questions are what the sampling frame was, who '
                    'never entered it, and whether entry correlates with the outcome. If it does, '
                    'the size is aggravating, not reassuring.'),
                 a_simple=('<b>More rows fix the wobble, never the tilt.</b> Collecting more data '
                           'makes your answer more precise; it does not move it towards the truth '
                           'if the way you collected it was skewed. At five hundred million rows '
                           'you get a very narrow, very confident, very wrong number that nobody '
                           'can argue with. Ask instead who could never have shown up in this data '
                           'at all.')),
            dict(q='A satisfaction survey has a 6% response rate and averages 4.6 out of 5. Name the bias and say what you can conclude.',
                 a=('<b>Non-response bias, and you can conclude almost nothing about the '
                    'population.</b> The 94% are missing not at random: people answer support '
                    'surveys when the experience was memorable, which is bimodal, so the 4.6 is a '
                    'statement about respondents only. Two moves. Bound it: assume the worst '
                    'plausible value for non-responders and see whether the conclusion survives. '
                    'Then chase a small random subsample of non-responders hard, and use that '
                    'subsample to reweight &mdash; that is the only version of this that produces '
                    'a defensible number.'),
                 a_simple=('<b>It is non-response bias, and the honest answer is that you know very '
                           'little.</b> People fill in support surveys when the experience stuck in '
                           'their mind, which usually means it was very good or very bad, so the '
                           'score describes the answerers and nobody else. Two things you can do: '
                           'work out what the number would look like if the silent ninety-four '
                           'percent were as unhappy as is plausible, and go and chase a small '
                           'random handful of them until they reply.')),
        ],
        anchor=dict(
            formula=r'$\mathrm{SE} \propto n^{-1/2}$ &nbsp;&middot;&nbsp; $\text{bias} \propto n^{0}$',
            formula_simple='The wobble shrinks as you collect more. The tilt does not shrink at all.',
            bullets=[
                'Name the mechanism &mdash; selection, survivorship or non-response &mdash; before you propose any fix',
                'More rows narrow the interval around the wrong number and never move it',
                'Your labels are whatever got reviewed, and what got reviewed is whatever the last model flagged',
            ]),
        chips=['selection bias', 'survivorship bias', 'non-response', 'stratified sampling',
               'feedback loops'],
        followup='You retrain a fraud model on the transactions your current model let through. What happens over three retraining cycles?',
    ),

    # ------------------------------------------------------------------ F10
    dict(
        id='simulation',
        tier='foundation',
        title='Simulation beats recall',
        kicker='"I would simulate the null and look" outranks a half-remembered formula &mdash; as long as you can say what it is you would generate',
        simple=[
            'You do not have to remember the formula. Nearly every question of the form "how '
            'likely is this" can be answered by building the situation in eight lines of code, '
            'running it a few thousand times and counting how often the thing happened. Shuffle '
            'the labels to see what pure chance produces. Draw your own rows again with '
            'replacement to see how much your answer wobbles. Generate fake data from the process '
            'you think you have, to find out how big an effect you could detect. Three questions, '
            'one move.',
            'It is a real answer, not a dodge, whenever there is no clean formula &mdash; a ratio, '
            'a median, grouped data, a rule that stops early &mdash; and whenever you want to '
            'check a formula you do half remember. It becomes a dodge the moment you cannot say '
            'what you would generate, because choosing how the fake data is made <i>is</i> the '
            'assumption being tested. The production version is worth saying out loud in any '
            'experiment question: split your control group in two at random, run the whole '
            'pipeline on it, and count how often it declares a winner. It should be about one time '
            'in twenty.',
        ],
        analogy=('<b>Like testing a pub dice game by playing it.</b> You could work out the odds of '
                 'a house rule nobody can quite explain, or you could roll it ten thousand times '
                 'and count. The second way is not cheating. It is only cheating if you cannot say '
                 'how many dice there are and what the rule is, which was the actual question.'),
        trap_simple=('Treating the split-your-control-group check as a formality you run once and '
                     'tick off. It is the only audit you have of whether your uncertainty numbers '
                     'are honest. When it comes back declaring winners far more often than one '
                     'time in twenty, something in the pipeline is lying, and you have to find it '
                     'before you run a single real test.'),
        tech=[
            'Three simulations cover almost everything. Shuffle the treatment labels and recompute '
            'the statistic for an exact permutation null. Resample with replacement &mdash; '
            'clusters, not rows, if the data are grouped &mdash; for a bootstrap interval around a '
            'median, a ratio, an AUC or a win rate that has no clean standard error. Generate data '
            'from the process you believe in for a power analysis. That last one is strictly more '
            'general than $n \\approx 16\\sigma^2/\\delta^2$: a simulated power analysis handles a '
            'ratio metric, clustering, a sequential stopping rule, skew and a capping rule in the '
            'same twenty lines, and the closed form handles none of them.',
            'The audit version is the <b>A/A test</b>. Split control at random, push both halves '
            'through the entire pipeline including the metric definition, and count how often you '
            'declare a winner. It should be 5%. If it is 12%, your variance estimator is wrong and '
            'the shortlist is short: clustered data analysed as if rows were independent, a ratio '
            'metric with a naive variance instead of the delta method, an assignment or '
            'sample-ratio bug, an outlier problem, or a peeking rule baked into the dashboard. Say '
            '"I would start with an A/A test" in any experiment design question &mdash; it is the '
            'cheapest credibility on offer, and it is the one thing that catches errors no formula '
            'check will.',
        ],
        tech_note=('Simulation has its own standard error and you should quote it unprompted. An '
                   'estimated rate from $B$ replications carries $\\sqrt{p(1-p)/B}$: at a true 5%, '
                   'a thousand runs give about 0.7 percentage points, so you can separate 5% from '
                   '12% comfortably and 5% from 6% not at all. Ten thousand runs takes that to '
                   'about 0.2 points. A thousand is the floor; use ten thousand when the quantity '
                   'you want lives in a tail.'),
        fig=dict(
            kind='plot',
            head=['WHAT ONE RUN TELLS YOU', 'WHAT A THOUSAND DO'],
            xr=(0, 5000), yr=(0, 0.26), ph=190,
            xlab='simulated A/A runs', ylab='share declared significant',
            xticks=[(0, '0'), (1000, '1,000'), (2000, '2,000'), (3000, '3,000'), (5000, '5,000')],
            yticks=[(0.05, '5%'), (0.12, '12%'), (0.20, '20%')],
            bands=[dict(x0=0, x1=500, tone='sig', label='noise', op=0.08)],
            vlines=[dict(x=1000, tone='plain', label='1,000 runs')],
            curves=[
                dict(pts=[(25, 0.240), (50, 0.180), (100, 0.160), (200, 0.155), (300, 0.127),
                          (500, 0.136), (750, 0.128), (1000, 0.130), (1500, 0.125), (2000, 0.128),
                          (3000, 0.125), (4000, 0.124), (5000, 0.123)],
                     tone='sig', label='clustered rows, naive variance', lat=8, dx=8, dy=-12),
                dict(pts=[(25, 0.040), (50, 0.100), (100, 0.070), (200, 0.050), (300, 0.047),
                          (500, 0.048), (750, 0.048), (1000, 0.048), (1500, 0.050), (2000, 0.048),
                          (3000, 0.051), (4000, 0.051), (5000, 0.051)],
                     tone='mem', label='the same pipeline, fixed', lat=8, dx=8, dy=16),
            ],
            marks=[dict(x=100, y=0.160, label='16% after 100 runs', tone='sig', dx=8, dy=-10)],
            foot='a thousand runs separates 5% from 12% comfortably; a hundred runs separates nothing',
            alt='Two running estimates of an A/A false positive rate against the number of '
                'simulated runs. Both swing wildly below a few hundred runs; by a thousand runs '
                'the broken pipeline has settled near 12% and the fixed one near 5%.'),
        caption=('The left-hand third of this plot is why "we ran an A/A and it looked fine" is not '
                 'evidence. At 100 runs the broken pipeline read 16% and the fixed one read 7%; '
                 'both were noise. The answer only exists after about a thousand runs, and you can '
                 'compute in advance how many you need.'),
        caption_simple=('Early on, both lines jump around and neither is telling you anything. Only '
                        'after about a thousand repeats do they settle into their real answers '
                        '&mdash; one at roughly one in eight, one at roughly one in twenty. You can '
                        'work out how many repeats you need before you start.'),
        when=[
            'You cannot remember the closed form and the clock is running',
            'The estimator is a median, a ratio, a quantile or a win rate',
            'The design has clustering, capping or a stopping rule that no formula covers',
            'You are asked to design an experiment and want one sentence that buys credibility',
        ],
        trap=('Treating an A/A test as a box to tick rather than an audit of your variance '
              'estimator. The giveaway sentence is <i>"we ran an A/A and it was fine"</i> with no '
              'rate attached and no count of runs. The mirror failure is offering to simulate '
              'without being able to state the data-generating process &mdash; that tells the '
              'interviewer you are avoiding the assumption rather than making it explicit, and it '
              'is the one case where "I would simulate it" scores badly.'),
        math=dict(
            tex=r'\mathrm{SE}_{\text{MC}} = \sqrt{\frac{p(1-p)}{B}} \qquad p = 0.05,\; B = 1{,}000 \;\Rightarrow\; \pm 0.7\text{pp}',
            note='Your simulated answer is itself an estimate. Quote its error bar and the '
                 'interviewer stops wondering whether you understand what you just did.',
            cost='B is a dial you set, not a constraint you inherit'),
        code=dict(
            label='An A/A test that fails, in eight lines',
            cost='numpy + scipy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n'
                 '<span class="k">from</span> scipy <span class="k">import</span> stats\n\n'
                 'rng = np.random.default_rng(<span class="s">0</span>)\n\n'
                 '<span class="k">def</span> aa(users=<span class="s">2000</span>, per_user=<span class="s">20</span>):\n'
                 '    u = rng.normal(size=users)[:, <span class="k">None</span>]      '
                 '<span class="c"># a per-user effect</span>\n'
                 '    rows = u + rng.normal(size=(users, per_user))\n'
                 '    a, b = rows[:users//<span class="s">2</span>].ravel(), rows[users//<span class="s">2</span>:].ravel()\n'
                 '    <span class="k">return</span> stats.ttest_ind(a, b).pvalue   '
                 '<span class="c"># 40,000 rows, treated as iid</span>\n\n'
                 '<span class="k">print</span>(np.mean([aa() &lt; <span class="s">0.05</span> '
                 '<span class="k">for</span> _ <span class="k">in</span> <span class="k">range</span>(<span class="s">1000</span>)]))\n'
                 '<span class="c"># 0.55. not 0.05. there are 2,000 users, not 40,000 rows,</span>\n'
                 '<span class="c"># and no formula in your head was going to tell you that.</span>')),
        real=('Spotify picked its sequential testing framework by simulation rather than by '
              'argument. At 500 users per arm and a true effect of 0.2 standard deviations, their '
              'simulations put a group sequential test at about <b>90% power</b> against roughly '
              '<b>72&ndash;77%</b> for always-valid methods and about 75% for Bonferroni across '
              'fourteen looks &mdash; a measured price for unlimited peeking rather than a guessed '
              'one. Twitch published simulated bootstrapped A/A tests in November 2021 for the '
              'same reason: to check their variance estimators survived heavy-tailed metrics.'),
        drills=[
            dict(q='Your A/A tests come back significant 12% of the time. Name three causes.',
                 a=('<b>Your variance estimator is wrong, and there are five usual suspects.</b> '
                    'Clustered data analysed as if rows were independent &mdash; the commonest, and '
                    'the design effect is $1 + (m-1)\\rho$. A ratio metric such as '
                    '$\\sum\\text{clicks}/\\sum\\text{impressions}$ with a naive variance instead '
                    'of the delta method. An assignment or sample-ratio bug making the two halves '
                    'genuinely different. An outlier-driven metric where the t-test approximation '
                    'has not kicked in. Or a stopping rule baked into the dashboard, which is '
                    'peeking. Diagnose by simulating each in turn.'),
                 a_simple=('<b>Your uncertainty numbers are too small, and there is a short list of '
                           'reasons.</b> Rows that belong to the same user counted as independent '
                           'evidence, so the error bars come out far too narrow. A rate built by '
                           'dividing one total by another and given the wrong uncertainty. A bug '
                           'making the two halves genuinely different people. A metric ruled by a '
                           'few extreme values. Or a dashboard someone watches until it goes '
                           'green.')),
            dict(q='You offer to simulate rather than derive. When does that count against you?',
                 a=('<b>When you cannot state the data-generating process.</b> Simulation does not '
                    'remove an assumption, it makes you write it down: the distribution, the '
                    'dependence structure, the effect size, the stopping rule. If you can say "I '
                    'would generate clustered Bernoulli outcomes with intra-cluster correlation '
                    'around 0.1, twenty rows per user, and sweep the true lift", that is a design. '
                    'If you say "I would just simulate it" and stop, you have swapped a formula '
                    'you did not know for an assumption you have not made.'),
                 a_simple=('<b>When you cannot say what you would generate.</b> Simulating does not '
                           'get rid of the assumptions, it forces you to write them down: how the '
                           'numbers are spread, how they clump together, how big an effect you are '
                           'looking for, when you stop. Name those and you have designed something. '
                           'Say only that you would simulate it, and you have traded a formula you '
                           'forgot for a decision you dodged.')),
            dict(q='How many simulation runs before you trust the answer?',
                 a=('<b>Enough that the Monte Carlo error is small next to the difference you care '
                    'about.</b> A simulated rate has $\\mathrm{SE} = \\sqrt{p(1-p)/B}$. At a true '
                    '5%, a thousand runs gives 0.7 percentage points, so 5% against 12% is settled '
                    'and 5% against 6% is not. Ten thousand takes you to 0.2 points. Use a thousand '
                    'as the floor, ten thousand for anything that depends on a tail quantile, and '
                    'quote the interval alongside the number.'),
                 a_simple=('<b>Enough that the leftover randomness is small compared with the gap '
                           'you are trying to see.</b> For a one-in-twenty rate, a thousand repeats '
                           'pins it to within about seven tenths of a percentage point &mdash; '
                           'plenty to tell one in twenty from one in eight, useless for telling one '
                           'in twenty from one in seventeen. Ten thousand repeats cuts that to '
                           'about two tenths. A thousand is the floor.')),
        ],
        anchor=dict(
            formula=r'$\sqrt{p(1-p)/B}$ &nbsp;&middot;&nbsp; 1,000 runs &rarr; &plusmn;0.7 points at 5%',
            formula_simple='A thousand runs pins a one-in-twenty rate to within about seven tenths '
                           'of a point. A hundred runs pins nothing.',
            bullets=[
                'Permutation for a null, resampling for an interval, generated data for power &mdash; three questions, one move',
                'An A/A test that declares winners more than one time in twenty is a broken variance estimator, not bad luck',
                'A thousand runs is the floor and ten thousand is what a tail quantile needs',
            ]),
        chips=['bootstrap', 'permutation test', 'A/A test', 'power analysis', 'sequential testing'],
        followup='Your A/A tests come back significant 12% of the time. Name three causes.',
    ),
]
