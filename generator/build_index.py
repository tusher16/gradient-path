#!/usr/bin/env python3
"""Rebuild the hub.

The study path is recovered from each built page's OWN rail, so it can never
drift from the content: add a card to a module and the hub's counts follow on
the next rebuild.
"""
import re, json, os
import os as _os
ROOT = _os.path.dirname(_os.path.abspath(__file__))

# the built pages live one level up, in the repo root
SITE = _os.path.dirname(ROOT)

MODULES = [
    dict(id='la',    n='01', key='gp-la-status-v2',        file='01-linear-algebra.html',
         title='Linear Algebra, Slowly'),
    dict(id='b75',   n='02', key='b75-status-v1',          file='blind75nightlyreview.html',
         title='Blind 75 in 18 Moves'),
    dict(id='ml',    n='03', key='gp-ml-status-v1',        file='03-machine-learning.html',
         title='Machine Learning, Model by Model'),
    dict(id='llm',   n='04', key='gp-llm-status-v1',       file='04-llms.html',
         title='LLMs, End to End'),
    dict(id='stats', n='05', key='gp-stats-status-v1',     file='05-statistics.html',
         title='Statistics &amp; Probability'),
    dict(id='sd',    n='06', key='gp-sysdesign-status-v1', file='06-system-design.html',
         title='ML &amp; GenAI System Design'),
]

TIER_ANCHOR = {'Foundation': 'tier-foundation', 'Core': 'tier-core',
               'Advanced': 'tier-advanced', 'In Production': 'tier-production'}

# (module id, tier name, why). Nothing on the path leans on a stop below it.
PATH_ORDER = [
    ('la',    'Foundation',    'The objects and the four moves. Nothing else stands up without these.'),
    ('ml',    'Foundation',    'What learning actually is &mdash; the loss, the fit, and the honest measurement.'),
    ('stats', 'Foundation',    'Probability, and the four ways it misleads you. Read it before you trust any number below.'),
    ('la',    'Core',          'Span, rank and the null space. This is where the geometry starts paying.'),
    ('ml',    'Core',          'The model zoo, linear through gradient boosting and clustering.'),
    ('stats', 'Core',          'Inference as a set of decisions. The block asked in every loop.'),
    ('b75',   'Patterns',      'Eighteen coding patterns. Runs alongside the rest &mdash; do one a night.'),
    ('la',    'Advanced',      'Eigenvectors, SVD and PCA. Half the interview questions live here.'),
    ('ml',    'Advanced',      'Calibration, imbalance, and a neural network built from the perceptron up.'),
    ('stats', 'Advanced',      'Bayes, causality, and knowing how sure you are rather than just what you predict.'),
    ('llm',   'Foundation',    'How a language model works at all: tokens, probabilities, sampling.'),
    ('llm',   'Core',          'Inside the transformer. Attention, masking, RoPE, the KV cache.'),
    ('la',    'In Production', 'The linear algebra that only shows up in a served model.'),
    ('llm',   'Advanced',      'Training it, and bending it to your task without retraining it.'),
    ('ml',    'In Production', 'Drift, skew, late labels, A/B tests that lie for four days.'),
    ('llm',   'In Production', 'The AI engineer stack. If you only have one evening, spend it here.'),
    ('stats', 'In Production', 'Experiments, and putting an honest number on something that talks back.'),
    ('sd',    'Foundation',    'The method: turn a vague prompt into numbers before you draw a single box.'),
    ('sd',    'Core',          'The components every design reuses, and the binding constraint inside each.'),
    ('sd',    'Advanced',      'Five designs worked end to end. Cover the estimate and do the arithmetic yourself.'),
    ('sd',    'In Production', 'Five more, where latency, cost and blast radius decide and the model is the easy part.'),
]


def rail_tiers(path):
    s = open(path).read()
    nav = re.search(r'<nav class="rail".*?</nav>', s, re.S).group(0)
    out = []
    for m in re.finditer(r'<li class="rail-tier">(.*?)</li>|data-rail="([^"]+)"', nav):
        if m.group(1):
            out.append((m.group(1), []))
        elif out:
            out[-1][1].append(m.group(2))
    return dict(out)


def main():
    tiers = {}
    for m in MODULES:
        p = os.path.join(SITE, m['file'])
        t = rail_tiers(p)
        tiers[m['id']] = t
        m['total'] = sum(len(v) for v in t.values())

    mods_js = [dict(id=m['id'], n=m['n'], key=m['key'], total=m['total'],
                    title=m['title'], href=m['file']) for m in MODULES]
    by_id = {m['id']: m for m in MODULES}

    path_js = []
    for mid, tier, why in PATH_ORDER:
        m = by_id[mid]
        if mid == 'b75':
            # Blind 75 has rail tiers but the hub treats it as one flat stop:
            # it shares nothing with the rest, so it runs alongside rather than
            # sitting at a position in the order. Its stop links to the page root.
            ids = [i for v in tiers[mid].values() for i in v]
        else:
            ids = tiers[mid].get(tier)
        if ids is None:
            raise SystemExit(f'{mid} has no tier {tier!r}: {list(tiers[mid])}')
        path_js.append(dict(m=mid, n=m['n'], mod=m['title'], key=m['key'], href=m['file'],
                            tier=tier, why=why, ids=ids,
                            anchor=TIER_ANCHOR.get(tier, '')))

    total = sum(m['total'] for m in MODULES)

    # rebuilt from a stored template, so re-running is idempotent
    src = open(_os.path.join(ROOT, 'templates', 'index-base.html')).read()

    # --- the live module grid: append cards 05 and 06 -----------------------
    new_cards = '''    <a class="mod" href="05-statistics.html">
      <div class="mod-top"><span class="mod-n">MODULE 05</span><span class="pill live">Live</span>
        <span class="pill">ML foundations</span></div>
      <h2>Statistics &amp; Probability</h2>
      <p>Distributions and Bayes through experimentation and LLM evaluation. This is where offers are lost quietly &mdash; not by failing to define a p-value, but by failing the question after it. Ends on the 2026 problem nobody has an answer for: <b>putting an honest number on a model that talks back</b>.</p>
      <ul class="facts"><li>40 topics</li><li>4 tiers</li><li>120 drill questions</li><li>44 prompts</li></ul>
      <div class="prog"><span>Marked solid</span><b id="p-stats">0 / 40</b></div>
      <div class="bar"><i id="b-stats"></i></div>
      <span class="go">Open module &rarr;</span>
    </a>
    <a class="mod" href="06-system-design.html">
      <div class="mod-top"><span class="mod-n">MODULE 06</span><span class="pill live">Live</span>
        <span class="pill">System design</span></div>
      <h2>ML &amp; GenAI System Design</h2>
      <p>Twelve building blocks, then ten rounds worked end to end: RAG over 10M documents, a 70B serving layer, a support agent, fraud inside a payment authorisation, moderation at 50M posts a day. The round is not scored on naming vLLM &mdash; it is scored on <b>which constraint binds, in numbers</b>, before you draw a box.</p>
      <ul class="facts"><li>22 designs</li><li>4 tiers</li><li>66 drill questions</li><li>26 prompts</li></ul>
      <div class="prog"><span>Marked solid</span><b id="p-sd">0 / 22</b></div>
      <div class="bar"><i id="b-sd"></i></div>
      <span class="go">Open module &rarr;</span>
    </a>
'''
    anchor = '''      <span class="go">Open module &rarr;</span>
    </a>
  </div>
</div>

<div class="shell" style="padding-top:20px">
  <p class="sect">Being built</p>'''
    assert anchor in src
    src = src.replace(anchor, '''      <span class="go">Open module &rarr;</span>
    </a>
''' + new_cards + '''  </div>
</div>

<div class="shell" style="padding-top:20px">
  <p class="sect">Being built</p>''')

    # --- shrink "Being built" to module 07 only ----------------------------
    i = src.index('<p class="sect">Being built</p>')
    j = src.index('</div>\n</div>', src.index('<div class="grid">', i))
    src = src[:src.index('<div class="grid">', i)] + '''<div class="grid">
    <div class="mod placeholder">
      <div class="mod-top"><span class="mod-n">MODULE 07</span><span class="pill soon">Next up</span>
        <span class="pill">Infrastructure</span></div>
      <h2>Data &amp; Serving Infrastructure</h2>
      <p>Docker, Kubernetes, the pipeline that feeds a model, and the parts of a backend an AI
        engineer is still expected to know.</p>
      <span class="go">Not yet</span>
    </div>
  ''' + src[j:]

    # --- the data the hub runs on ------------------------------------------
    src = re.sub(r'var MODULES = \[.*?\];', 'var MODULES = ' + json.dumps(mods_js) + ';', src, flags=re.S)
    src = re.sub(r'var PATH = \[.*?\];', 'var PATH = ' + json.dumps(path_js) + ';', src, flags=re.S)
    src = re.sub(r'var TOTAL = \d+;', f'var TOTAL = {total};', src)

    # the deck mentions the switch, which now does something real
    src = src.replace(
        'holds the precise version one switch away',
        'holds the precise version one switch away &mdash; and in <b>Simple</b> the formulas '
        'and code are genuinely gone, not just moved down the page')

    open(os.path.join(SITE, 'index.html'), 'w').write(src)
    print(f'hub: {len(MODULES)} modules, {len(path_js)} path stops, {total} cards')
    for m in MODULES:
        print(f'   {m["n"]}  {m["total"]:>3}  {m["title"]}')


if __name__ == '__main__':
    main()
