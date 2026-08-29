CFG = dict(
    key='gp-stats-status-v1',
    num='05',
    title='Statistics &amp; Probability, Decision by Decision',
    h1='Statistics &amp; Probability',
    deck=('40 ideas, explained twice. Every card opens in <b>plain English</b> with a picture and '
          'an everyday analogy &mdash; flip one switch and the same card becomes the '
          '<b>precise, interview-grade</b> version, formula and all. Statistics is where '
          'candidates lose offers quietly: not by failing to define a p-value, but by failing '
          'the question that comes after it. So every card here ends in a decision you have to '
          'make with the numbers in front of you.'),
    howto=[
        'Leave it on <b>Simple</b> the first night. Read the picture before the words.',
        'Cover the answer. Say the trap out loud before you scroll to it.',
        'Flip to <b>Technical</b> and check you can say the same thing with the symbols.',
        'Mark yourself honestly at the bottom of the card. Fuzzy is a useful answer.',
        'Away from this page? Copy a card&rsquo;s <b>prompt</b> into ChatGPT or Gemini and let it quiz you.',
    ],
    legend_sig=('where the <i>error</i> comes from &mdash; the estimate that moves, the false '
                'positive you bought, the conclusion that does not survive a second look.'),
    legend_mem=('what <i>survives</i> &mdash; the honest interval, the effect that is really '
                'there, the decision you can defend a quarter later.'),
    role='AI/ML interview tutor',
    subject='statistics and probability, for AI / ML / data engineering interviews',
    subject_short='statistics and probability',
    ex2=('Where it shows up in a real system (an experimentation platform, an offline '
         'evaluation, a model actually serving traffic, an LLM eval set) &mdash; name a real '
         'system or a real failure, not "used in data analysis"'),
    stack='Prefer scipy, statsmodels, numpy and pandas when you show code.',
    tiers=dict(
        foundation=dict(name='Foundation', title='Probability, and the four ways it misleads you',
                        blurb=('Before any test: what a probability is, what an average hides, and '
                               'the assumption that quietly breaks in every real dataset. Almost '
                               'every senior-level trap further down this page is a violation of '
                               'something in this block &mdash; a dependent sample, a long tail, '
                               'a base rate nobody mentioned.')),
        core=dict(name='Core', title='Inference: the numbers you are asked to defend',
                  blurb=('p-values, intervals, power and the tests themselves &mdash; but as '
                         'decisions, not definitions. This is the block that gets asked in every '
                         'loop, and the block where the follow-up question does all the '
                         'filtering.')),
        advanced=dict(name='Advanced', title='Bayes, causality and the model&rsquo;s own uncertainty',
                      blurb=('Priors that carry the whole argument, confounders that survive a '
                             'regression, fairness definitions that cannot all hold at once, and '
                             'the difference between not knowing the answer and not knowing how '
                             'sure you are.')),
        production=dict(name='In Production', title='Experiments, and evaluating things that talk back',
                        blurb=('The statistics of a system that is actually serving traffic: '
                               'sample ratio mismatch, interference, novelty, and the whole new '
                               'problem of putting an honest number on an LLM. This is the block '
                               'that separates a candidate who has run an experiment from one who '
                               'has read about them.')),
    ),
    footer=('The order is deliberate: nothing on this page leans on an idea below it. Foundation '
            'is probability and the shape of data; Core is inference as a set of decisions; '
            'Advanced is Bayes, causality and uncertainty about the model itself; '
            'In&nbsp;Production is everything that only breaks once real traffic is hitting it. '
            'Marks and your Simple/Technical choice are saved in this browser only.'),
)
