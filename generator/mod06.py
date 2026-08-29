CFG = dict(
    key='gp-sysdesign-status-v1',
    num='06',
    title='ML &amp; GenAI System Design, Worked End to End',
    h1='ML &amp; GenAI System Design',
    deck=('22 designs, explained twice. Every card opens in <b>plain English</b> with an '
          'architecture picture &mdash; flip one switch and the same card becomes the '
          '<b>full technical</b> version: the arithmetic worked out loud, the tradeoffs argued, '
          'and the three follow-ups they grill you with. The design round is not scored on '
          'whether you name vLLM. It is scored on whether you can say <b>which constraint '
          'binds</b>, in numbers, before you draw a single box.'),
    howto=[
        'Leave it on <b>Simple</b> the first night. Read the architecture before the words.',
        'Cover the estimate. Do the arithmetic yourself, out loud, then check it.',
        'Flip to <b>Technical</b> and check you can defend every box you drew.',
        'Mark yourself honestly at the bottom of the card. Fuzzy is a useful answer.',
        'Away from this page? Copy a card&rsquo;s <b>prompt</b> and have a chatbot run the round.',
    ],
    legend_sig=('what <i>breaks</i> &mdash; the binding constraint, the cost blowup, the failure '
                'mode the interviewer is waiting for you to name unprompted.'),
    legend_mem=('what <i>holds</i> &mdash; the component that earns its place, the number that '
                'justifies it, the degradation path that keeps the system answering.'),
    role='ML system design interviewer and tutor',
    subject='ML and GenAI system design, for AI / ML engineering interviews',
    subject_short='ML and GenAI system design',
    ex2=('A real deployed system that solves this, with the numbers its engineering blog '
         'published &mdash; name the company and the figure, not "many companies do this"'),
    stack=('Prefer concrete components (vLLM, pgvector, Qdrant, Kafka, Redis, Ray) and real '
           'numbers over generic boxes when you show a design.'),
    tiers=dict(
        foundation=dict(name='Foundation', title='The method, before any particular system',
                        blurb=('What a strong answer does in the first ten minutes: turn a vague '
                               'prompt into a measurable one, size it in numbers, spend a latency '
                               'budget, price a request, and decide what the system does when it '
                               'is wrong. Every worked design later in this module reuses all '
                               'five, so learn them as moves rather than as topics.')),
        core=dict(name='Core', title='The components every design reuses',
                  blurb=('Retrieval, serving, caching, evaluation, guardrails, observability and '
                         'the loop that keeps offline and online the same system. Know the '
                         'binding constraint inside each one &mdash; that is the difference '
                         'between naming a component and designing with it.')),
        advanced=dict(name='Advanced', title='Five designs, worked end to end',
                      blurb=('The prompts you are most likely to get, done properly: requirements, '
                             'arithmetic, architecture, tradeoffs, failure modes, and the '
                             'follow-ups. Read the estimate before the diagram &mdash; in a real '
                             'round the numbers come first and the boxes follow from them.')),
        production=dict(name='In Production', title='Five more, where the constraint is not the model',
                        blurb=('Fraud inside a payment authorisation, a home feed, an eval harness, '
                               'moderation at fifty million posts a day, and a platform serving '
                               'every team in the company. These are the designs where latency, '
                               'cost and blast radius do the deciding, and the model is the easy '
                               'part.')),
    ),
    footer=('The order is deliberate: Foundation is the method you apply to any prompt; Core is '
            'the components those designs reuse; Advanced and In&nbsp;Production are ten worked '
            'rounds. Read a design card by covering the estimate and doing the arithmetic '
            'yourself first &mdash; that is the part actually being scored. Marks and your '
            'Simple/Technical choice are saved in this browser only.'),
)
