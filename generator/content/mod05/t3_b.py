CARDS = [

    # ------------------------------------------------------------------ 1
    dict(
        id='fairness-metrics',
        tier='advanced',
        title='Fairness definitions that cannot both hold',
        kicker='Calibration and equal error rates are a theorem apart, and the follow-up finds out whether you know which one your product owes people',
        simple=[
            'A risk score is fair. Prove it. Two people will now hand you two different '
            'tests, and each will call their own test fairness.',
            'The first test: whoever the model scores at seven out of ten should go on to '
            'reoffend, or default, or churn at the same rate whichever group they belong '
            'to. The score means one thing everywhere. That is calibration. The second '
            'test: among the people who never went on to do the thing, the same share '
            'should get flagged in every group. Equal false alarms. That is equalised '
            'odds.',
            'Both are reasonable, and both were argued in public about the same model. '
            'When the two groups have different underlying rates, arithmetic guarantees '
            'you cannot have both at once. It is a proof, not a tuning problem, and no '
            'library and no constraint in the loss function gets you out of it. So the '
            'useful question is never whether the model is fair. It is which of the two '
            'definitions your product owes the people it scores &mdash; decided before '
            'you look at the numbers, and written down with a name against it.',
        ],
        analogy=('<b>Like a hospital triage badge.</b> One ward insists a red badge must '
                 'mean the same danger whichever door you walked in through. Another '
                 'insists the same share of healthy people get pulled aside for tests, '
                 'whichever door. Both are fair. If the two doors see different illness '
                 'rates, the hospital has to pick one.'),
        simple_extra=('The other half of the job is arithmetic on subgroups, and it is '
                      'where most audits quietly fail. Aggregate accuracy hides subgroup '
                      'catastrophe: in the 2018 Gender Shades audit, commercial gender '
                      'classifiers were wrong about darker-skinned women up to about a '
                      'third of the time, and wrong about lighter-skinned men under one '
                      'time in a hundred. And when you do split the data, the smallest '
                      'subgroups carry the widest error bars &mdash; so a gap that looks '
                      'alarming and a gap that looks absent can both be nothing but too '
                      'few people. Put the interval next to every subgroup number, or you '
                      'are guessing in both directions.'),
        trap_simple=('&ldquo;We ran the fairness library, the parity check passed, so the '
                     'model is fair.&rdquo; One definition clearing its threshold is not '
                     'fairness; it is one definition clearing its threshold, and the '
                     'theorem says another one is failing at that same moment. The mirror '
                     'version costs just as much: saying one side of the COMPAS argument '
                     'was simply wrong. Both sides did their arithmetic correctly, on '
                     'different definitions.'),
        tech=[
            'Two results, reached independently. Kleinberg, Mullainathan &amp; Raghavan '
            '(2016) and Chouldechova (2017) showed that calibration within groups, equal '
            'false positive rates and equal false negative rates cannot hold together '
            'unless prevalence is equal across groups or the classifier is perfect. '
            'Chouldechova gives the identity that makes it obvious: for any binary '
            'classifier, $\\mathrm{FPR} = \\frac{p}{1-p}\\cdot\\frac{1-\\mathrm{PPV}}'
            '{\\mathrm{PPV}}\\cdot(1-\\mathrm{FNR})$. Hold PPV equal across groups '
            '&mdash; that is what calibration buys you &mdash; hold FNR equal too, and '
            'the base rate alone fixes FPR. There is no parameter left to turn.',
            'So the answer to &ldquo;is it biased&rdquo; is that both statements are true '
            'simultaneously, and which one counts is a question about harm rather than '
            'about statistics. Say who bears the cost of a false positive. If it lands on '
            'a person as a detention, a rejection or a screening-out, the error rates are '
            'what you owe and equalised odds is the constraint. If the score is consumed '
            'downstream as a probability &mdash; an expected-value calculation, a queue '
            'ranked by risk &mdash; calibration is what makes it usable, and breaking it '
            'silently corrupts every decision built on top. Pick, write it in the model '
            'card, and report both anyway.',
        ],
        tech_note=('Disaggregated evaluation is the skill actually being tested: the '
                   'metric per group, with an interval, and intersected &mdash; aggregate '
                   'accuracy hides subgroup catastrophe, and the intersection is usually '
                   'where it hides. Small subgroups then bite you from the other side. A '
                   'subgroup of 40 at around 80% accuracy carries a standard error near '
                   '6.3 points, so a 20-point gap has an interval running from roughly 7 '
                   'to 33 points. Say that out loud instead of reporting the point '
                   'estimate as a finding.'),
        math=dict(
            tex=r'\mathrm{FPR} = \frac{p}{1-p}\cdot\frac{1-\mathrm{PPV}}{\mathrm{PPV}}\cdot(1-\mathrm{FNR})',
            note='Calibration fixes PPV across groups. Equal FNR fixes the last term. The '
                 'prevalence $p$ then determines FPR completely, so unequal base rates '
                 'force unequal false positive rates. Nothing here is about the model.',
            cost='holds for every binary classifier, at every threshold'),
        code=dict(
            label='The impossibility, in four lines of arithmetic',
            cost='no model required',
            src=('<span class="c"># Chouldechova (2017): an identity every binary classifier obeys</span>\n'
                 '<span class="k">def</span> fpr(prev, ppv, fnr):\n'
                 '    <span class="k">return</span> (prev / (<span class="s">1</span> - prev)) '
                 '* ((<span class="s">1</span> - ppv) / ppv) * (<span class="s">1</span> - fnr)\n\n'
                 '<span class="c"># ONE model, calibrated to the same PPV in both groups, same FNR in both</span>\n'
                 '<span class="k">print</span>(fpr(<span class="s">0.50</span>, <span class="s">0.65</span>, '
                 '<span class="s">0.30</span>))   <span class="c"># 0.377 -- the higher base rate group</span>\n'
                 '<span class="k">print</span>(fpr(<span class="s">0.30</span>, <span class="s">0.65</span>, '
                 '<span class="s">0.30</span>))   <span class="c"># 0.162 -- same model, other group</span>\n\n'
                 '<span class="c"># nothing was tuned, nothing is broken. the 2.3x gap IS the base rate,</span>\n'
                 '<span class="c"># and the only way to close it is to give up calibration on purpose</span>')),
        fig=dict(
            kind='grid',
            head=['SAME MODEL, SAME DEFENDANTS', 'OPPOSITE VERDICTS'],
            xlab='which definition you audit against',
            ylab='group',
            cols=['calibrated within group', 'equal false positive rate'],
            rows=['white defendants', 'Black defendants'],
            cells=[
                [dict(t='PASSES', sub='same rate at the same score', tone='mem', fill=True),
                 dict(t='23% wrongly flagged', sub='the reference point', tone='plain')],
                [dict(t='PASSES', sub='same rate at the same score', tone='mem', fill=True),
                 dict(t='45% wrongly flagged', sub='FAILS, by roughly 2x', tone='sig', fill=True)],
            ],
            foot='both columns are arithmetically correct; with unequal base rates you cannot have both',
            alt='A two by two table showing one model passing a calibration audit in both '
                'groups while failing an equal-false-positive-rate audit, 45 percent '
                'against 23 percent'),
        caption=('The left column is Northpointe&rsquo;s audit; the right column is '
                 'ProPublica&rsquo;s. Same score, same defendants, same arithmetic, and '
                 'the two audits disagree because they are testing different conditional '
                 'probabilities. Nothing you can do to the model turns both columns '
                 'green.'),
        caption_simple=('Both columns were measured on the same model and the same people. '
                        'One asks whether a score means the same thing in every group; the '
                        'other asks whether the same share of harmless people get flagged. '
                        'There is no version of this model where both come back clean.'),
        when=[
            'A model scores people and the score decides what happens to them &mdash; credit, triage, moderation, hiring',
            'Someone reports one fairness number and treats the audit as finished',
            'Two teams look at the same model and disagree about whether it is biased',
            'You are asked to &ldquo;just make it fair&rdquo; and no definition comes attached to the request',
        ],
        trap=('&ldquo;We ran the fairness library, demographic parity passed, so the model '
              'is fair.&rdquo; One definition clearing its threshold is not fairness, and '
              'if the base rates differ the theorem says some other definition is failing '
              'at that exact moment. The mirror of the trap costs just as much in the '
              'room: saying ProPublica or Northpointe was simply wrong about COMPAS. Both '
              'computed their numbers correctly. They computed different numbers, and the '
              'disagreement was always about which harm the score was allowed to '
              'distribute.'),
        real=('ProPublica&rsquo;s COMPAS analysis (May 2016) found Black defendants were '
              'roughly twice as likely to be wrongly flagged high risk &mdash; about 45% '
              'against about 23% false positive rate. Northpointe replied that the score '
              'was calibrated: equal reoffence rates at equal scores, across race. Both '
              'were arithmetically correct, and Chouldechova (2017) formalised why they '
              'had to be. The intersectional version is Buolamwini &amp; Gebru&rsquo;s '
              'Gender Shades (2018), where commercial gender classifiers erred on '
              'darker-skinned women up to 34.7% of the time against 0.8% for '
              'lighter-skinned men.'),
        drills=[
            dict(q='Your model is calibrated within both groups but has a higher false-positive rate for one. Is it biased?',
                 a=('<b>Both statements are true at once, and that is a theorem rather '
                    'than a bug.</b> With unequal prevalence, $\\mathrm{FPR}=\\frac{p}{1-p}'
                    '\\cdot\\frac{1-\\mathrm{PPV}}{\\mathrm{PPV}}\\cdot(1-\\mathrm{FNR})$ '
                    'forces it: fix PPV and FNR across groups and the base rate alone sets '
                    'FPR. So I would ask back which harm the product is optimising '
                    'against. If a false positive lands on a person as a detention or a '
                    'rejection, equalised odds is the constraint you owe and you accept a '
                    'calibration loss. If a downstream system reads the score as a '
                    'probability, calibration is the constraint and the error-rate gap '
                    'becomes a disclosed, monitored number.'),
                 a_simple=('<b>Both things are true at the same time, and that is a proof '
                           'rather than a bug.</b> When two groups reoffend or default at '
                           'different underlying rates, a score that means the same thing '
                           'in both groups has to produce different false alarm rates in '
                           'them. So the answer is a question back: who pays for a false '
                           'alarm? If a wrongly flagged person is detained or refused, '
                           'equal false alarm rates are what the product owes. If some '
                           'other system reads the score as a probability and does sums '
                           'with it, keeping the meaning of the score is what you owe.')),
            dict(q='A moderation model flags accounts for restriction pending human review, and it is calibrated across groups. Which definition do you owe, and what do you write down?',
                 a=('<b>Equalised odds, and you write it down before you look at the '
                    'results.</b> The cost of a false positive here lands on a person as a '
                    'restriction they did not earn, so the quantity that has to match '
                    'across groups is the rate at which innocent accounts get flagged, not '
                    'the meaning of the score. That means buying a calibration gap on '
                    'purpose and saying so: name the definition in the model card, report '
                    'per-group FPR and FNR with intervals, and state the direction of the '
                    'loss you accepted. Flip the score into a downstream expected-value '
                    'calculation and the answer flips to calibration.'),
                 a_simple=('<b>Equal false alarm rates, and you write it down before you '
                           'see the results.</b> Being wrongly flagged here means a real '
                           'person loses access to their account while someone reviews it, '
                           'so the number that has to match across groups is how often '
                           'innocent people get flagged. Choosing that means giving up the '
                           'other definition on purpose, so record which one you chose, '
                           'publish both sets of numbers with their margins, and say '
                           'plainly what you gave up. If the score were instead feeding a '
                           'cost calculation somewhere else, the choice would go the other '
                           'way.')),
            dict(q='Your smallest subgroup has 40 people in it and shows a 20-point accuracy gap. What do you report?',
                 a=('<b>Report the interval, and say that a 20-point gap on 40 people is '
                    'not yet a finding.</b> At around 80% accuracy, $\\mathrm{SE} = '
                    '\\sqrt{0.8 \\times 0.2 / 40} \\approx 6.3$ points, so a 95% interval '
                    'on that subgroup alone is near &plusmn;12 and the interval on the gap '
                    'runs from roughly 7 to 33 points even against an enormous comparison '
                    'group. You cannot rank harms with that. The decision is a sampling '
                    'one, not a modelling one: oversample that subgroup in the eval set '
                    'until the interval is narrow enough to act on.'),
                 a_simple=('<b>Report the range, and say that a twenty-point gap measured '
                           'on forty people is not yet a finding.</b> With forty people '
                           'and accuracy around eight in ten, the honest margin on that '
                           'one subgroup is about twelve points either side, so the true '
                           'gap could plausibly be seven points or thirty-three. That is '
                           'not enough to rank harms or to promise anyone it has been '
                           'fixed. Go and collect more examples from that subgroup for the '
                           'evaluation set, and until you have them, publish the gap with '
                           'its margin attached.')),
        ],
        anchor=dict(
            formula=r'$\mathrm{FPR} = \frac{p}{1-p}\cdot\frac{1-\mathrm{PPV}}{\mathrm{PPV}}\cdot(1-\mathrm{FNR})$ &nbsp;&middot;&nbsp; fix PPV, and $p$ decides the rest',
            formula_simple='Equal false alarms and one meaning per score are the same knob turned two ways. Different base rates, and you have to choose which one you are turning.',
            bullets=[
                'Calibration, equal false positive rate and equal false negative rate cannot all hold when base rates differ',
                'Which one you owe is a product decision, written down before you look at the numbers',
                'Report per-subgroup metrics with intervals &mdash; a small subgroup is usually just underpowered',
            ]),
        chips=['calibration', 'equalised odds', 'demographic parity',
               'disaggregated evaluation', 'Chouldechova 2017'],
        followup='Your model is calibrated within both groups but has a higher false-positive rate for one. Is it biased?',
    ),

    # ------------------------------------------------------------------ 2
    dict(
        id='quasi-experiments',
        tier='advanced',
        title='When you cannot randomise',
        kicker='&ldquo;We couldn&rsquo;t A/B test it&rdquo; is not a stopping point &mdash; and every design you reach for buys its answer with exactly one assumption',
        simple=[
            'Half the questions that matter cannot be randomised. The feature went to one '
            'country. The price changed for everyone on the same Tuesday. There was never '
            'a control group and there never will be. The answer is not to shrug; it is '
            'to build a stand-in for what would have happened otherwise, and then be '
            'honest that the stand-in is the entire argument.',
            'Three ways to build one. Difference-in-differences: compare the change over '
            'time in the treated group against the change over the same window in an '
            'untreated one, and subtract. Synthetic control: blend several untreated '
            'markets into a weighted mixture that tracked yours closely before the change, '
            'and let the mixture stand in afterwards. Regression discontinuity: when a '
            'threshold decided who got the thing, compare the people who just cleared it '
            'against the people who just missed, on the grounds that nothing else '
            'separates them.',
            'Each buys its answer with one assumption. The two lines would have stayed '
            'parallel. The blend is made of markets your launch never touched. Nobody '
            'could nudge themselves over the line. Say which one you are leaning on '
            'before anyone asks, and say how you would try to break it.',
        ],
        analogy=('<b>Like judging whether the new bypass helped one town.</b> You cannot '
                 'close it to half the residents, so you find towns that have tracked '
                 'yours for years and watch whether yours pulls away after the opening. '
                 'The whole claim rests on those other towns still being a fair stand-in '
                 '&mdash; which is a statement about the towns, not about your data.'),
        trap_simple=('Running the comparison without ever drawing the two lines for the '
                     'months before the change. If they were already drifting apart, '
                     'nothing is holding the method up and the number you produce is the '
                     'drift. The other version: putting a market into your comparison '
                     'group that your own launch spilled into, which quietly subtracts '
                     'part of the effect from itself.'),
        tech=[
            'The estimator is $\\hat{\\tau} = (\\bar{Y}^{T}_{post} - \\bar{Y}^{T}_{pre}) '
            '- (\\bar{Y}^{C}_{post} - \\bar{Y}^{C}_{pre})$, and the second bracket is your '
            'estimate of what the treated unit would have done anyway. Parallel trends is '
            'the claim that this substitution is legitimate. It is not testable in the '
            'post period &mdash; that is the period you are trying to measure. Pre-period '
            'tests are all you get, and they are underpowered, so failing to reject a '
            'pre-trend is weak evidence for the assumption you actually need.',
            'Synthetic control replaces that single control with convex weights over a '
            'donor pool chosen to match the treated unit&rsquo;s pre-period, and does '
            'inference by permutation: rerun the estimator with each donor as the pretend '
            'treated unit and see where yours falls in that distribution. The failure '
            'modes are poor pre-period fit, a donor that was itself treated, and too few '
            'donors for the placebo distribution to mean anything.',
            'Regression discontinuity estimates a local effect at the cutoff and nothing '
            'else. Check the density of the running variable at the threshold for '
            'manipulation, and check that no other policy changes at the same number. '
            'Whichever design you use, cluster the standard errors at the unit you '
            'compared &mdash; market, store, region &mdash; not at the row.',
        ],
        tech_note=('Instrumental variables handle non-compliance and interrupted time '
                   'series handles a single unit with strong seasonality; both are worth '
                   'naming, neither is worth attempting under time pressure without '
                   'saying what identifies them. The sentence that earns credit is the '
                   'same in all four cases: name the identifying assumption, then name '
                   'the two placebos you would run &mdash; a placebo period before the '
                   'change and a placebo unit that was never treated &mdash; and say what '
                   'result would make you abandon the estimate.'),
        math=dict(
            tex=r'\hat{\tau}_{\text{DiD}} = \bigl(\bar{Y}^{T}_{post} - \bar{Y}^{T}_{pre}\bigr) - \bigl(\bar{Y}^{C}_{post} - \bar{Y}^{C}_{pre}\bigr)',
            note='The right-hand bracket is not a measurement, it is a substitution. '
                 'Parallel trends says the control&rsquo;s change is what the treated unit '
                 'would have done anyway, and no amount of post-period data can check '
                 'that.',
            cost='two units, two periods, one untestable assumption'),
        code=dict(
            label='The diff-in-diff line you run before the real one',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
                 '<span class="k">def</span> did(y, treated, post):\n'
                 '    m = <span class="k">lambda</span> t, p: y[(treated == t) &amp; (post == p)].mean()\n'
                 '    <span class="k">return</span> (m(<span class="s">1</span>, <span class="s">1</span>) '
                 '- m(<span class="s">1</span>, <span class="s">0</span>)) - '
                 '(m(<span class="s">0</span>, <span class="s">1</span>) - m(<span class="s">0</span>, '
                 '<span class="s">0</span>))\n\n'
                 '<span class="c"># placebo FIRST: cut the pre-period in half and pretend the launch</span>\n'
                 '<span class="c"># happened at the midpoint. no treatment existed, so there is no effect</span>\n'
                 '<span class="k">print</span>(did(y_pre, treated_pre, fake_post))  '
                 '<span class="c"># want ~0. if not, parallel trends is already dead</span>\n'
                 '<span class="k">print</span>(did(y, treated, post))               '
                 '<span class="c"># only now is this number worth saying out loud</span>')),
        fig=dict(
            kind='plot',
            head=['WHAT YOU MEASURE', 'WHAT YOU ASSUME'],
            xr=(0, 12), yr=(90, 130), ph=200,
            xlab='months relative to launch', ylab='orders per active user',
            xticks=[(0, '-6'), (3, '-3'), (6, '0'), (9, '+3'), (12, '+6')],
            yticks=[(100, '100'), (110, '110'), (120, '120')],
            vlines=[dict(x=6, tone='sig', label='Germany launches')],
            bands=[dict(x0=0, x1=6, tone='mem', op=0.08,
                        label='the only window where the assumption is checkable')],
            curves=[
                dict(pts=[(0, 100), (2, 103), (4, 106), (6, 109), (8, 112), (10, 115), (12, 118)],
                     tone='mem', label='control markets', lat=5, la='end', dx=-10, dy=-14),
                dict(pts=[(0, 95), (2, 98), (4, 101), (6, 104), (8, 111), (10, 115), (12, 119)],
                     tone='sig', label='Germany (treated)', lat=0, dx=6, dy=18),
                dict(pts=[(6, 104), (8, 107), (10, 110), (12, 113)], tone='plain', dash='5 4',
                     label='counterfactual: assumed, not observed', lat=2, la='middle', dx=-14, dy=44),
            ],
            marks=[dict(x=12, y=119, tone='sig', r=4, label='observed', la='end', dx=-6, dy=-10),
                   dict(x=12, y=113, tone='plain', r=4)],
            foot='the estimate is the gap between the two dots, and the lower one is not data',
            alt='A difference-in-differences plot: Germany and the control markets rise in '
                'parallel before launch, Germany pulls ahead afterwards, and a dashed '
                'counterfactual line shows the assumed path the estimate is measured '
                'against'),
        caption=('The pre-period is the only evidence you will ever have for the dashed '
                 'line, and it is evidence about the past. Everything the estimate claims '
                 'lives in the gap between the two right-hand points &mdash; and one of '
                 'those points was never measured.'),
        caption_simple=('Everything before the launch is evidence. Everything after it is '
                        'the claim. The dashed line is the piece nobody ever gets to '
                        'check, which is why the argument you should be having is about '
                        'the left half of the picture.'),
        when=[
            'A feature launched in one country and an exec wants the causal impact',
            'A price or policy changed for every user on the same day',
            'Someone proposes a before-and-after comparison and stops there',
            'A threshold decides who gets the thing &mdash; a score, a spend tier, an age',
        ],
        trap=('&ldquo;There was no control group, so we compared the month before with the '
              'month after.&rdquo; That is a before-and-after, not a '
              'difference-in-differences, and it hands every seasonal move and every '
              'unrelated market shift to your launch. The version that gets caught in more '
              'senior rooms: running diff-in-diff and never plotting the pre-period, or '
              'leaving a market in the donor pool that your own launch spilled into '
              '&mdash; which subtracts part of the effect from itself and reports the '
              'remainder as the answer.'),
        real=('Netflix publishes its quasi-experimentation programme for exactly the cases '
              'randomisation cannot reach &mdash; content launches, marketing spend, '
              'region-level changes &mdash; with a companion post naming the hard parts: '
              'parallel trends, too few units, interference. The reason the assumption '
              'deserves that much attention is the size of what you are chasing. At Bing, '
              'roughly 1 in 500 experiments clears a high-ROI bar and the wins that do '
              'land move key metrics by 0.1% to 1.0%. A control market drifting one point '
              'relative to yours manufactures or erases an effect that size outright.'),
        drills=[
            dict(q='You launched in Germany only and want the causal impact. There is no control group. What do you do, and what would make your answer wrong?',
                 a=('<b>Synthetic control from the other EU markets, and I would name the '
                    'three things that would make it wrong before I said the number.</b> '
                    'Fit convex weights over the untreated markets to match Germany&rsquo;s '
                    'pre-period series, project the composite forward, take the gap. It is '
                    'wrong if Germany had a market-specific shock in the post period, if '
                    'any donor market was itself touched by the launch, or if the '
                    'pre-period fit is poor &mdash; a composite that never tracked Germany '
                    'before is not tracking it now. Inference by placebo: rerun with each '
                    'donor as the pretend treated unit and see where Germany falls.'),
                 a_simple=('<b>Build a stand-in Germany out of the other markets, then say '
                           'what would break it.</b> Find the weighted blend of untreated '
                           'markets that best matches Germany month by month in the year '
                           'before the launch, then carry that blend forward and measure '
                           'the gap. It breaks if something else happened in Germany that '
                           'quarter, if the launch leaked into any of the markets you used '
                           'to build the blend, or if the blend never matched Germany well '
                           'in the first place. Test it by pretending each other market '
                           'was the launched one and checking that they do not show the '
                           'same jump.')),
            dict(q='Your pre-trend test comes back non-significant. Is parallel trends satisfied?',
                 a=('<b>No &mdash; you failed to detect a divergence, which is not the '
                    'same as there not being one.</b> Pre-trend tests run on a handful of '
                    'periods and a handful of units are badly underpowered, so a null '
                    'there is close to uninformative. Say how big a pre-trend you could '
                    'have detected, plot the raw series rather than quoting the test, and '
                    'note the deeper limitation: even a perfectly flat pre-period is a '
                    'statement about the past, and parallel trends is a claim about a '
                    'post period where something changed for your unit and not for the '
                    'controls.'),
                 a_simple=('<b>No. You failed to spot a difference, which is not the same '
                           'as there being none.</b> That test usually runs on a few '
                           'months and a few markets, so it can miss a drift big enough to '
                           'wipe out your whole result. Work out how large a drift you '
                           'could actually have caught, and show the raw lines rather than '
                           'quoting the test. And remember what the test can never cover: '
                           'the lines matching in the past is not a promise they would '
                           'have kept matching afterwards.')),
            dict(q='A score of 700 or above gets the offer. Product tells you customers can see their score before applying. What happens to your regression discontinuity estimate?',
                 a=('<b>It stops identifying the effect of the offer.</b> RDD works only '
                    'if units cannot manipulate the running variable around the cutoff. '
                    'Once applicants can see their score and act on it, the people just '
                    'above 700 are systematically the ones who knew and pushed, so they '
                    'differ from the people just below in more than the offer. The '
                    'diagnostic is a density test on the running variable at the '
                    'threshold: sorting shows up as a pile-up just above the cutoff in the '
                    'histogram. And even clean, the estimate was only ever local &mdash; '
                    'it says nothing about an applicant at 550.'),
                 a_simple=('<b>It stops measuring the offer.</b> The whole design rests on '
                           'people just above and just below the line being alike apart '
                           'from the offer. If applicants can see the score first, the '
                           'ones who land just above it are the ones who knew about the '
                           'line and pushed themselves over, and that difference travels '
                           'with them into your estimate. Check it by drawing a histogram '
                           'of the scores: a bunching just above the cutoff is the sorting '
                           'made visible. And even at its best, this design only tells you '
                           'about people near the line.')),
        ],
        anchor=dict(
            formula=r'$\hat{\tau} = (\bar{Y}^{T}_{post}-\bar{Y}^{T}_{pre}) - (\bar{Y}^{C}_{post}-\bar{Y}^{C}_{pre})$ &nbsp;&middot;&nbsp; the second bracket is the assumption',
            formula_simple='Subtract what the untreated group did anyway from what the treated group did. The bit you subtract is a guess, and defending that guess is the whole job.',
            bullets=[
                'Difference-in-differences rests on parallel trends, and you can only inspect them before the change',
                'Synthetic control rests on a donor pool your launch never touched, plus a pre-period fit good enough to believe',
                'Regression discontinuity rests on nobody moving themselves across the cutoff, and is only ever local to it',
            ]),
        chips=['parallel trends', 'synthetic control', 'regression discontinuity',
               'placebo tests', 'instrumental variables'],
        followup='You launched in Germany only and want the causal impact. There is no control group. What do you do, and what would make your answer wrong?',
    ),

    # ------------------------------------------------------------------ 3
    dict(
        id='leakage-statistics',
        tier='advanced',
        title='Leakage is a statistical failure',
        kicker='Not a coding bug &mdash; a dependence between your split units that every number you report afterwards has already assumed away',
        simple=[
            'A test score is a claim about behaviour on things the model has never seen. '
            'The claim holds only if the test rows are genuinely independent of the '
            'training rows, and rows are almost never the thing that is independent. One '
            'patient contributes forty scans. One user contributes forty sessions. One '
            'document generates twenty evaluation questions.',
            'Split those at random and the same patient lands on both sides of the line. '
            'The model can now score brilliantly by recognising the patient rather than '
            'the disease, and you have measured memorisation and called it '
            'generalisation. The tell is a number that is suspiciously good.',
            'The damage is not confined to the score. Every interval you put around it '
            'counted rows as though they were independent people, so it is far too '
            'narrow, and the regression test you gate releases on is built out of that '
            'interval. Which is why the fix is not care and not a code review. It is the '
            'splitter: split on the group, or split on time, and decide that before you '
            'touch the data.',
        ],
        analogy=('<b>Like sitting your driving test on the three streets you practised '
                 'on.</b> You will pass, and the pass tells nobody whether you can drive '
                 'anywhere else. The fix is not to concentrate harder on the day. It is '
                 'for the examiner to decide which streets are off limits before you '
                 'start practising.'),
        trap_simple=('&ldquo;I used cross-validation, so there is no leakage.&rdquo; '
                     'Cross-validation with the scaling, the imputation or the feature '
                     'selection fitted on the whole dataset leaks in every single fold. '
                     'You have run the same mistake ten times and averaged the answers, '
                     'which makes the number look steadier rather than truer.'),
        tech=[
            'Kapoor &amp; Narayanan name eight types; two of them cover nearly everything '
            'you will be asked. The first is preprocessing or feature selection fitted '
            'outside the fold &mdash; scaling, imputation, target encoding, a filter that '
            'chose features while looking at the full label column. The second is '
            'non-independence between train and test, and that is the statistical one.',
            'State it as an assumption and the fix becomes obvious. Your held-out '
            'estimate assumes the test examples are exchangeable with deployment examples '
            'and independent of the fitting procedure. Clustered rows break the second '
            'half: with $m$ rows per group and within-group correlation $\\rho$, the '
            'effective sample size is $n / (1 + (m-1)\\rho)$, so two million rows at forty '
            'per patient with $\\rho = 0.5$ behave like about a hundred thousand '
            'independent ones. Leakage inflates the point estimate; the clustering '
            'deflates the standard error underneath it. Both errors point the same way.',
            'So the fix is an estimator choice, not a hygiene habit. GroupKFold or '
            'StratifiedGroupKFold when rows nest inside an entity, a forward-chaining '
            'time split when deployment order is temporal, every fitted transform inside '
            'a Pipeline so it is refit per fold, and one final set nobody has touched. '
            'The diagnostic that catches the rest: train a classifier to predict the '
            'group from the features. If it works, that group is sitting there as a '
            'shortcut.',
        ],
        tech_note=('Two corollaries. Illegitimate features are the common industrial case '
                   'and they do not look like a bug &mdash; a column populated by a '
                   'process that only runs after the outcome you are predicting reads as '
                   'a perfectly ordinary feature. And the mirror mistake exists: a split '
                   'stricter than deployment throws away real signal, so if the model '
                   'genuinely will see the same users again, a group split understates '
                   'production performance. Match the split to the deployment question, '
                   'not to a rule you read.'),
        math=dict(
            tex=r'n_{\text{eff}} = \frac{n}{1 + (m-1)\rho} \qquad \text{groups, not rows}',
            note='At 40 rows per patient and a within-patient correlation of 0.5, two '
                 'million rows behave like roughly a hundred thousand independent ones, '
                 'and every standard error computed from $n$ is too small by about '
                 '$\\sqrt{20.5} \\approx 4.5$.',
            cost='the design effect, borrowed from clustered sampling'),
        code=dict(
            label='The same model, two definitions of held out',
            cost='scikit-learn',
            src=('<span class="k">from</span> sklearn.model_selection <span class="k">import</span> '
                 'KFold, GroupKFold, cross_val_score\n'
                 '<span class="k">from</span> sklearn.pipeline <span class="k">import</span> make_pipeline\n'
                 '<span class="k">from</span> sklearn.preprocessing <span class="k">import</span> StandardScaler\n'
                 '<span class="k">from</span> sklearn.linear_model <span class="k">import</span> LogisticRegression\n\n'
                 '<span class="c"># the scaler is refit INSIDE each fold. this is the pipeline, not a habit</span>\n'
                 'pipe = make_pipeline(StandardScaler(), LogisticRegression())\n\n'
                 '<span class="k">print</span>(cross_val_score(pipe, X, y, cv=KFold(<span class="s">5</span>)).mean())\n'
                 '<span class="c">#   0.94 -- the same patients are on both sides of every fold</span>\n'
                 '<span class="k">print</span>(cross_val_score(pipe, X, y, cv=GroupKFold(<span class="s">5</span>), '
                 'groups=patient_id).mean())\n'
                 '<span class="c">#   0.62 -- nothing about the model changed. only what counts as held out</span>')),
        fig=dict(
            kind='blocks',
            h=272,
            boxes=[
                dict(x=34, y=44, w=140, h=38, t='row 1', sub='patient 8812', tone='sig'),
                dict(x=34, y=90, w=140, h=38, t='row 2', sub='patient 8812', tone='sig'),
                dict(x=34, y=136, w=140, h=38, t='row 3', sub='patient 8812', tone='sig'),
                dict(x=34, y=182, w=140, h=38, t='row 4', sub='patient 8812', tone='sig'),
                dict(x=250, y=52, w=170, h=66, t='TRAIN', sub='rows 1 and 3', tone='plain'),
                dict(x=250, y=156, w=170, h=66, t='TEST', sub='rows 2 and 4', tone='plain'),
                dict(x=490, y=104, w=196, h=66, t='the same patient on both sides', sub='0.94 offline, 0.61 live', tone='sig'),
            ],
            links=[dict(a=0, b=4), dict(a=2, b=4), dict(a=1, b=5), dict(a=3, b=5),
                   dict(a=4, b=6, tone='sig'), dict(a=5, b=6, tone='sig')],
            labels=[dict(x=104, y=22, t='one patient, four rows'),
                    dict(x=335, y=22, t='random split'),
                    dict(x=588, y=22, t='what you measured')],
            foot='every row was used exactly once, and nothing here is a coding bug',
            alt='Four rows belonging to one patient are split at random, two into the '
                'training set and two into the test set, so the same patient appears on '
                'both sides and the held-out score measures recognition of the patient'),
        caption=('Nothing in this picture is a bug. Every row appears exactly once, the '
                 'split is a correct uniform random split, and the estimate it produces is '
                 'still meaningless &mdash; because the unit that has to be independent is '
                 'the patient, and the splitter was never told that.'),
        caption_simple=('No row was used twice and no code is wrong. The problem is that '
                        'the same person appears on both sides, so the test is asking '
                        'whether the model recognises that person rather than whether it '
                        'recognises the illness.'),
        when=[
            'Rows nest inside something &mdash; a user, a patient, a document, a store, a day',
            'An offline number is far better than anything you have seen in production',
            'You are about to compare two models on the same held-out set and gate a release on it',
            'The model will be deployed on next month&rsquo;s data, not on a random half of last month&rsquo;s',
        ],
        trap=('&ldquo;I used cross-validation, so there is no leakage.&rdquo; '
              'Cross-validation with preprocessing fitted outside the loop leaks in every '
              'fold, and averaging ten contaminated folds buys you a tighter interval '
              'around an equally wrong number. The second sentence that costs the loop: '
              '&ldquo;we did a random 80/20 split&rdquo; on data where one user supplies '
              'hundreds of rows. Neither is a coding error. Both are the estimator being '
              'handed a definition of independence that the data does not satisfy.'),
        real=('Zech et al. (PLOS Medicine, November 2018) trained a pneumonia CNN that '
              'scored 0.802 AUC internally at Mount Sinai and 0.717 at NIH. Pneumonia '
              'prevalence was 34.2% at one site against 1.2% at the other, a CNN could '
              'identify which hospital a radiograph came from with 99.95% accuracy, and a '
              'model using nothing but hospital prevalence reached 0.861 on the pooled '
              'data. The site was in the image, and it was on both sides of the split. '
              'Kapoor &amp; Narayanan (Patterns, 2023) found the same class of error '
              'across 17 fields and 329 papers.'),
        drills=[
            dict(q='Your churn model gets 0.94 AUC offline and 0.61 in production. Give me your top three hypotheses, ranked.',
                 a=('<b>Temporal or target leakage first, train-serve skew second, '
                    'population shift third &mdash; and each has a cheap test.</b> Leakage '
                    'leads because a 0.33 drop is larger than shift usually delivers: hunt '
                    'for any feature written by a process that runs after the churn event, '
                    'and re-score without it. Then compute the offline and online feature '
                    'vectors for the same entity at the same timestamp and diff them '
                    '&mdash; skew shows up in a handful of columns, not all of them. '
                    'Third, refit on an older window and evaluate forward in time; if the '
                    'honest temporal number is 0.65, the 0.94 never existed.'),
                 a_simple=('<b>Leakage first, then a mismatch between how features are '
                           'built offline and online, then a change in who the users '
                           'are.</b> Leakage leads because that drop is far too big for '
                           'ordinary drift: look for any input that only gets filled in '
                           'after a customer has already left, and rerun without it. Next, '
                           'take one customer, build their inputs both ways at the same '
                           'moment in time, and compare &mdash; a mismatch shows up in a '
                           'few columns. Last, train on an older period and test on a '
                           'later one; if that gives roughly the live number, you have '
                           'your answer.')),
            dict(q='&ldquo;I used cross-validation, so there is no leakage.&rdquo; Respond.',
                 a=('<b>Cross-validation prevents one kind of leakage and none of the '
                    'others.</b> If the scaler, the imputer, the target encoder or the '
                    'feature selector was fitted before the split, every fold saw the '
                    'held-out data through those statistics, and averaging ten '
                    'contaminated folds gives a tighter, more confident, equally wrong '
                    'number. Wrap the lot in a pipeline so each transform is refit inside '
                    'the fold. And cross-validation does nothing whatsoever about grouped '
                    'rows or about time order &mdash; those need GroupKFold and a '
                    'forward-chaining split respectively.'),
                 a_simple=('<b>It rules out one kind of leakage and leaves the rest '
                           'untouched.</b> If you worked out the scaling, the filled-in '
                           'missing values or the feature shortlist using the whole '
                           'dataset before splitting, then every fold has already seen its '
                           'own held-out part through those numbers. Averaging ten such '
                           'rounds gives you a steadier wrong answer. Chain the steps '
                           'together so each one is recomputed inside each fold. And it '
                           'still does nothing about repeated rows from the same person, '
                           'or about testing on the past to predict the future.')),
            dict(q='You have 2 million rows from 40,000 users and you did a random 80/20 split. What is wrong with the interval on your test score?',
                 a=('<b>It is far too narrow, probably by around a factor of four.</b> '
                    'Your $n$ is the number of independent units you could have swapped '
                    '&mdash; 40,000 users, not 2 million rows &mdash; and the same users '
                    'sit on both sides of the split, so the test set is not independent of '
                    'the training set either. At 50 rows per user with a within-user '
                    'correlation of 0.3, the design effect $1 + (m-1)\\rho$ is 15.7, '
                    'giving an effective sample size near 127,000 and standard errors '
                    'understated by $\\sqrt{15.7} \\approx 4$. Split by user, and bootstrap '
                    'users rather than rows.'),
                 a_simple=('<b>It is far too narrow, probably by about a factor of '
                           'four.</b> Your real sample size is the forty thousand people, '
                           'not the two million rows: fifty rows from one person tell you '
                           'nearly the same thing fifty times over. Worse, the same people '
                           'sit on both sides of the split, so the held-out part is not '
                           'really held out. Once you account for the repetition, two '
                           'million rows behave like roughly a hundred and thirty thousand '
                           'independent ones. Split by person, and resample people rather '
                           'than rows when you want an honest margin.')),
        ],
        anchor=dict(
            formula=r'$n_{\text{eff}} = n / \bigl(1 + (m-1)\rho\bigr)$ &nbsp;&middot;&nbsp; split on the unit you are willing to call independent',
            formula_simple='Your sample size is the number of independent things, not the number of rows. Split on the thing, never on the row.',
            bullets=[
                'Leakage inflates the score and voids the interval around it &mdash; the second half is the part people forget',
                'If rows nest inside a user, a patient, a document or a day, that entity is the split unit',
                'Fit every transform inside the fold; the pipeline is the fix, not a resolution to be careful',
            ]),
        chips=['GroupKFold', 'time-ordered split', 'design effect',
               'clustered standard errors', 'pipeline discipline'],
        followup='Your churn model gets 0.94 AUC offline and 0.61 in production. Give me your top three hypotheses, ranked.',
    ),

    # ------------------------------------------------------------------ 4
    dict(
        id='model-uncertainty',
        tier='advanced',
        title='Uncertainty in the model, not the data',
        kicker='Two models with the same accuracy can disagree about which cases they are unsure of, and only one of them is safe to route on',
        simple=[
            'There are two ways a model can fail to know something, and they call for '
            'opposite responses. Some of it is noise in the world: two customers with '
            'identical records, one churns and one does not. No quantity of extra data '
            'removes that. The rest is the model never having seen anything like this '
            'input before &mdash; that part does shrink with more data, and it is the part '
            'that hurts people, because it is invisible in the number the model prints.',
            'The number a classifier prints is not the chance it is right. It is a score '
            'squashed into the range between nothing and one, and on inputs unlike '
            'anything in training it is routinely large and wrong. Putting an automation '
            'threshold on it means trusting it hardest exactly where it has least basis.',
            'The practical answer is to stop asking for one number. Hold out a batch the '
            'model never trained on, measure how wrong it actually was there, and use that '
            'to turn each prediction into a set of answers: wide when the model is out of '
            'its depth, narrow when it is not. That set contains the true answer a stated '
            'fraction of the time, whatever the model happens to be.',
        ],
        analogy=('<b>Like a sommelier who has only ever tasted one valley.</b> Hand them a '
                 'bottle from home and the guess is worth money. Hand them something from '
                 'a country they have never tried and they will still name a grape, in the '
                 'same confident voice, at the same speed. The voice is not the evidence, '
                 'and nothing in it tells you which bottle you handed over.'),
        trap_simple=('Taking the biggest number the classifier prints, calling it '
                     'confidence, and setting an automation threshold on it. A model '
                     'nobody has checked against reality prints large numbers most readily '
                     'on inputs it has never seen &mdash; which are exactly the inputs the '
                     'threshold was built to catch.'),
        tech=[
            'Split the uncertainty. Aleatoric uncertainty is irreducible noise in the '
            'label given the features; epistemic uncertainty is the model&rsquo;s own '
            'ignorance and shrinks with data. Only the second responds to buying labels. '
            'Collapse them into one number and you cannot tell whether the answer is more '
            'data, or a different feature set plus an abstention policy.',
            'A softmax maximum is a normalised margin, not a posterior probability of '
            'correctness. Deep networks are systematically overconfident, and the '
            'calibration fixes &mdash; temperature scaling, Platt, isotonic on a held-out '
            'set, checked with a reliability diagram and a Brier score &mdash; repair the '
            'in-distribution part only. None of them can tell you the input was unlike '
            'anything in training.',
            'Conformal prediction is the one to name in 2026. Under exchangeability it '
            'returns a prediction set $\\hat{C}(x)$ with $P\\bigl(Y \\in \\hat{C}(X)\\bigr) '
            '\\geq 1-\\alpha$: distribution-free, and with no assumption that the model is '
            'well specified &mdash; a bad model simply produces bigger sets. That makes it '
            'directly usable for abstention and human routing, with average set size as '
            'your difficulty measure. Two caveats to raise unprompted: coverage is '
            'marginal, averaged over the population rather than promised per subgroup, and '
            'exchangeability is precisely what distribution shift breaks. Deep ensembles '
            'remain the strongest non-conformal baseline; MC dropout is the cheap one.',
        ],
        tech_note=('For LLM systems the ranking of cheap signals is: token probabilities '
                   'are usable but poorly calibrated, self-reported confidence is worse '
                   'than that, and agreement across sampled generations beats both. And do '
                   'not forget the variance you already own &mdash; Bouthillier et al. '
                   '(2021) showed seed-to-seed variation alone is large enough to threaten '
                   'benchmark conclusions, which means a model comparison run without a '
                   'seed budget is reporting an unknown mixture of method and luck.'),
        math=dict(
            tex=r'\hat{C}(x) = \{\, y : s(x,y) \leq \hat{q}_{1-\alpha} \,\} \qquad P\bigl(Y_{n+1} \in \hat{C}(X_{n+1})\bigr) \geq 1-\alpha',
            note='The quantile is taken over nonconformity scores on a calibration set the '
                 'model never trained on. Nothing in the guarantee mentions the model, '
                 'which is why it survives a badly specified one &mdash; but the coverage '
                 'is marginal, so it is a promise about the population, not about any one '
                 'subgroup.',
            cost='exchangeability, plus a calibration set you never trained on'),
        code=dict(
            label='Split conformal, start to finish',
            cost='numpy',
            src=('<span class="k">import</span> numpy <span class="k">as</span> np\n\n'
                 'alpha = <span class="s">0.10</span>\n'
                 '<span class="c"># nonconformity on a calibration set the model has never seen</span>\n'
                 'cal = <span class="s">1</span> - probs_cal[np.arange(<span class="k">len</span>(y_cal)), y_cal]\n'
                 'n = <span class="k">len</span>(cal)\n'
                 'q = np.quantile(cal, np.ceil((n + <span class="s">1</span>) * '
                 '(<span class="s">1</span> - alpha)) / n, method=<span class="s">"higher"</span>)\n\n'
                 '<span class="c"># a SET per row, not a label. no assumption that the model is any good</span>\n'
                 'sets = probs_test &gt;= <span class="s">1</span> - q\n'
                 '<span class="k">print</span>(sets.sum(<span class="s">1</span>).mean())     '
                 '<span class="c"># average set size = your honest difficulty measure</span>\n'
                 '<span class="k">print</span>(sets[np.arange(<span class="k">len</span>(y_test)), y_test].mean())  '
                 '<span class="c"># ~0.90 coverage, by construction</span>')),
        fig=dict(
            kind='plot',
            head=['WHAT THE MODEL OUTPUTS', 'WHAT IT DOES NOT KNOW'],
            xr=(0, 10), yr=(-3, 3), ph=200,
            xlab='one input feature', ylab='predicted value',
            xticks=[(0, 'rare'), (5, 'typical'), (10, 'rare')],
            yticks=[(0, '0')],
            hlines=[dict(y=1.5, tone='plain', label='act above this line')],
            vlines=[dict(x=9.2, tone='sig', label='a query from out here')],
            bands=[dict(x0=3.5, x1=6.5, tone='plain', op=0.10, label='the training data')],
            curves=[
                dict(pts=[(0, 0), (10, 0)], tone='plain', label='the prediction',
                     lat=0, dx=8, dy=-8),
                dict(pts=[(0, 3.0), (2, 1.2), (3.5, 0.4), (5, 0.3), (6.5, 0.4), (8, 1.2), (10, 3.0)],
                     tone='mem', label='what it could be doing', lat=0, dx=8, dy=14),
                dict(pts=[(0, -3.0), (2, -1.2), (3.5, -0.4), (5, -0.3), (6.5, -0.4), (8, -1.2), (10, -3.0)],
                     tone='mem'),
            ],
            marks=[dict(x=3.6, y=-0.10, tone='mem', r=2.6), dict(x=3.9, y=0.05, tone='mem', r=2.6),
                   dict(x=4.2, y=-0.05, tone='mem', r=2.6), dict(x=4.5, y=0.10, tone='mem', r=2.6),
                   dict(x=4.8, y=-0.08, tone='mem', r=2.6), dict(x=5.1, y=0.06, tone='mem', r=2.6),
                   dict(x=5.4, y=-0.02, tone='mem', r=2.6), dict(x=5.7, y=0.12, tone='mem', r=2.6),
                   dict(x=6.0, y=-0.06, tone='mem', r=2.6), dict(x=6.3, y=0.04, tone='mem', r=2.6),
                   dict(x=9.2, y=0, tone='sig', r=4.5)],
            foot='the point estimate is identical in both places; only the width tells you where to stop',
            alt='A prediction band pinched shut over the region holding the training data '
                'and flaring out on both sides, with a new query far from the data where '
                'the band straddles the decision threshold'),
        caption=('Two queries, one point estimate, and only one of them sits inside '
                 'anything the model has evidence about. The prediction does not move; the '
                 'width does. On the right the band straddles the threshold, which is the '
                 'definition of a case you should not be automating &mdash; and the number '
                 'the softmax prints there is the same either way.'),
        caption_simple=('The line through the middle is the model&rsquo;s answer, and it '
                        'is the same answer in both places. The gap around it is how much '
                        'the model has actually seen. Out on the right that gap is wide '
                        'enough to sit on both sides of the line you act on, which is the '
                        'moment to hand the case to a person.'),
        when=[
            'You are deciding which cases go to a human and need a defensible cut',
            'Someone wants to buy more labels and you have to say whether that will help',
            'A model output triggers an action rather than ranking a list',
            'The model is going somewhere the training data never came from &mdash; a new market, a new language, a new customer',
        ],
        trap=('&ldquo;The model is 98% confident, so we auto-approve anything above '
              '95.&rdquo; That number came out of a softmax, which normalises a margin and '
              'was never constrained to mean anything about correctness &mdash; and it is '
              'at its most confident on the inputs furthest from the training '
              'distribution. The sharper version separates candidates: after temperature '
              'scaling, someone declares the problem solved. Calibration repairs the '
              'in-distribution part and leaves the model exactly as certain about inputs '
              'it has never seen.'),
        real=('Zillow Offers bought homes against a price forecast and was wound down on 2 '
              'November 2021. The Q3 2021 Homes segment took an adjusted loss of 380.1 '
              'million dollars, with a further 240 to 265 million expected on roughly '
              '9,000 homes still to sell; inventory had gone from 3,142 to 9,790 in a '
              'single quarter and about 2,000 people, a quarter of the company, lost their '
              'jobs. Rich Barton&rsquo;s own summary was that &ldquo;the unpredictability '
              'in forecasting home prices far exceeds what we anticipated&rdquo;. The '
              'point forecast was not the problem. Nobody was pricing the width around '
              'it.'),
        drills=[
            dict(q='You want the model to abstain on the hardest 5% of inputs. How do you pick them, and how do you know your abstention policy is working?',
                 a=('<b>Rank by conformal set size or ensemble disagreement, never by '
                    'softmax maximum.</b> Fit split conformal on a calibration set the '
                    'model never saw, abstain on the largest sets until you hit the 5% '
                    'budget, then evaluate the accuracy-versus-coverage curve on the '
                    'retained set with intervals, against a random-abstention baseline '
                    '&mdash; if you are not beating random abstention, the ranking signal '
                    'is worthless. Then audit what you abstained on. A policy that quietly '
                    'abstains on one language or one demographic has not reduced risk, it '
                    'has relocated it somewhere harder to see.'),
                 a_simple=('<b>Rank the cases by how uncertain the model genuinely is, not '
                           'by the number it prints.</b> Two signals work: how many answers '
                           'a proper interval has to include before it is trustworthy, and '
                           'how much a handful of separately trained models disagree. Hand '
                           'over the worst five percent by that ranking. Then prove the '
                           'policy earns its keep: accuracy on the cases you kept has to '
                           'beat what you would get by refusing five percent at random, '
                           'with margins shown. And check who ended up in the refused pile '
                           '&mdash; if it is one language or one group, you moved the risk '
                           'rather than reducing it.')),
            dict(q='Your classifier outputs 0.98 on an input written in a language you have no training data for. What does that number mean?',
                 a=('<b>Close to nothing, and specifically not a 98% chance of being '
                    'right.</b> It is a normalised margin over the classes the model knows '
                    'about, and there is no class for &ldquo;this is nothing like my '
                    'training data&rdquo;, so the mass has to land somewhere. Calibrating '
                    'on in-distribution data will not fix it, because the miscalibration '
                    'is epistemic rather than a temperature problem. What does move: '
                    'disagreement across an ensemble or across sampled generations, and '
                    'conformal set size &mdash; with the honest caveat that if your '
                    'calibration set contains nothing like this input, exchangeability '
                    'fails and the coverage guarantee does not apply either.'),
                 a_simple=('<b>Almost nothing, and certainly not a ninety-eight percent '
                           'chance of being right.</b> The model has to spread its answer '
                           'across the labels it was taught, and none of those labels is '
                           '&ldquo;this is unlike anything I have seen&rdquo;, so the '
                           'weight piles onto whichever one looks least unfamiliar. '
                           'Rechecking its scores against a normal batch of data will not '
                           'help, because the problem is not that its scores are '
                           'mis-scaled, it is that it has never met this input. What helps '
                           'is disagreement between separately trained models &mdash; and '
                           'if none of your reference examples look like this one either, '
                           'no guarantee covers you here.')),
            dict(q='You have budget for ten thousand more labels. Accuracy is 82% and you want 90%. How do you decide whether the labels will get you there?',
                 a=('<b>Find out which kind of uncertainty your errors are made of before '
                    'you spend a penny.</b> Sample the errors and look for near-identical '
                    'inputs carrying different labels: that is aleatoric, and it is a '
                    'ceiling no volume of data crosses. Then measure your annotators '
                    'against each other on the same items &mdash; human-human agreement is '
                    'the practical ceiling, and label noise is not hypothetical, with '
                    '6.49% of MMLU items found to be erroneous. If instead the errors '
                    'concentrate where an ensemble disagrees and where you have few '
                    'training examples, that is epistemic, and labels bought in those '
                    'regions actually move the number.'),
                 a_simple=('<b>Work out which kind of not-knowing the errors are made of '
                           'first.</b> Pull a sample of the mistakes. If you find nearly '
                           'identical cases that were given different answers by the '
                           'labellers, that is noise you cannot buy your way out of, and '
                           'it caps how high accuracy can go. Check it by having two people '
                           'label the same items and seeing how often they agree &mdash; '
                           'that agreement rate is your practical ceiling, and on public '
                           'benchmarks the labels themselves are wrong a few percent of '
                           'the time. If instead the mistakes cluster in places where you '
                           'have almost no examples, more labels there will help.')),
        ],
        anchor=dict(
            formula=r'$\hat{C}(x)$ covers the truth $1-\alpha$ of the time &nbsp;&middot;&nbsp; whatever the model turns out to be',
            formula_simple='Split the not-knowing in two: noise you cannot remove, and gaps you can. Then let the answer be a set, and let the set widen when the model is out of its depth.',
            bullets=[
                'Aleatoric noise does not shrink with data; epistemic gaps do &mdash; decide which one you have before buying labels',
                'A softmax maximum is a normalised margin, not a probability of being right',
                'Conformal coverage is marginal, averaged over the population &mdash; check it per subgroup or it fails exactly where it matters',
            ]),
        chips=['aleatoric vs epistemic', 'conformal prediction', 'deep ensembles',
               'temperature scaling', 'selective prediction'],
        followup='You want the model to abstain on the hardest 5% of inputs. How do you pick them, and how do you know your abstention policy is working?',
    ),
]
