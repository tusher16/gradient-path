CARDS = [dict(
    id='rag-10m',
    tier='advanced',
    title='Design: RAG over 10M internal documents',
    kicker='The index is 58 GB, not 209 &mdash; and permissions decide the architecture before the vector store does',

    # ---------------- SIMPLE LAYER ----------------
    simple=[
        'Ten million documents will never fit in front of a model, so the system does not try. '
        'Offline it splits every document into passages of a few hundred words and files each '
        'passage twice: once by meaning, so that a question about &ldquo;laptop replacement&rdquo; '
        'finds a page titled &ldquo;hardware refresh&rdquo;, and once by exact words, so that a '
        'question about ticket INC-2024-00847 finds the one page containing that string. At '
        'question time it pulls about a hundred candidates from each store, ranks them with a '
        'slower and much more accurate model, keeps the best ten, and hands only those to the '
        'language model with an instruction to answer from them and cite where each claim came '
        'from.',
        'Two stores, because meaning-search quietly averages away the exact token that '
        'discriminates &mdash; and an internal corpus is mostly ticket numbers, error codes and '
        'system names. A second ranking pass, because the first pass was tuned for speed over a '
        'very large pile. Citations, because the product is trust: an answer nobody can check is '
        'worth less than a search box.',
        'The hard part is not the size. Thirty-four million passages fit in fifty-eight gigabytes '
        'of memory on one machine, and the search itself takes a few milliseconds. The hard part '
        'is that every employee is allowed to see a different corpus, so the permission check has '
        'to happen <b>inside</b> the search, before ranking. Do it afterwards and the people with '
        'the least access get a blank page and conclude the system is broken.',
    ],
    analogy=('<b>Like a librarian with a security clearance.</b> She keeps two catalogues, one by '
             'subject and one by exact title, pulls a trolley from both, and skims it herself to '
             'put the best ten on top. What makes her job hard is not the size of the library: it '
             'is knowing which rooms you may enter before she takes anything off a shelf.'),
    trap_simple=('Saying &ldquo;we fetch the best ten and then drop the ones the user is not '
                 'allowed to see&rdquo;. That filter runs too late, and it does not fail loudly: '
                 'it fails as an empty page for exactly the people with the narrowest access, who '
                 'then report that the system is broken. The other one is answering '
                 '&ldquo;we would just re-embed everything&rdquo; when asked about upgrading the '
                 'meaning-search model. You cannot mix two of those models in one index, so the '
                 'real answer is a second index built alongside, compared on a fixed test set, '
                 'ramped, and reversible &mdash; with the re-embedding bill named out loud.'),

    # ---------------- TECHNICAL LAYER ----------------
    tech=[
        'Size it before you draw. 10M documents at ~1,500 tokens is ~15B tokens; at 512-token '
        'chunks with 15% overlap that is <b>~34M chunks</b>. At 1,536 dimensions in fp32 the raw '
        'vectors are $34\\text{M} \\times 1536 \\times 4\\,\\text{B} \\approx 209$ GB &mdash; a '
        'number that scares people into sharding. Then apply int8 scalar quantisation (4&times;, '
        'under 1% recall loss) for ~52 GB, add the HNSW graph at $M=16$ '
        '($N \\times M \\times 2 \\times 4\\,\\text{B} \\approx 4.4$ GB) and ~1.4 GB of ID and '
        'version tracking: <b>~58 GB, one large-memory node, two for HA</b>. The 209&rarr;58 step '
        'is the single most valuable thing you say in this prompt.',
        'The request path, in order: gateway (authn, rate limit) &rarr; query understanding '
        '(rewrite, decompose, route) &rarr; semantic cache keyed on query <i>plus tenant plus ACL '
        'hash</i> &rarr; parallel fan-out to dense top-100 and BM25 top-100 with the <b>ACL '
        'pre-filter applied inside both</b> &rarr; fusion (tiered boosting, +7.5% NDCG, against '
        '+1.3% for plain RRF) &rarr; cross-encoder rerank 100&rarr;10 at 50&ndash;150 ms on GPU '
        '&rarr; context assembly under a token budget &rarr; input guardrail &rarr; streamed '
        'generation with citations &rarr; output guardrail, async and sampled. Offline: '
        'connectors and CDC queue &rarr; parse, preserving tables as markdown &rarr; recursive '
        'chunker at 512/50 &rarr; optional contextual enrichment &rarr; batched embedding &rarr; '
        'two sinks, vector and keyword &rarr; ACL sidecar keyed by chunk ID &rarr; index version '
        'registry. Emit chunk IDs, token counts and index version on every request or you cannot '
        'debug a single complaint.',
        'Capacity is not the interesting constraint. 23 QPS against a store benchmarked at p50 '
        '4 ms / p99 25 ms per million vectors is comfortable inside one shard; the LLM is the '
        'bottleneck. Cost is: ~6,000 input and ~400 output tokens per query, 200K queries/day, is '
        '1.2B input and 80M output tokens a day &mdash; <b>&#36;3,200/day, ~&#36;96K/month</b> at a '
        'mid-tier model and <b>~&#36;12.6K/month</b> at a Flash-class one. That 8&times; gap is larger '
        'than any infrastructure saving available anywhere else in this design, which is why '
        'routing is the first cost lever and sharding is not a cost lever at all.',
        'Failure modes worth naming before you are asked. <b>Right document, wrong section</b> is '
        'a chunk-boundary artefact &mdash; fix with parent-document retrieval and contextual chunk '
        'headers, and measure section-level context recall rather than chunk-level. <b>Embedding '
        'migration invalidates the index</b>: you cannot mix vector spaces, so it is dual-index, '
        'shadow evaluate, ramp, roll back, with the re-embed budgeted as a recurring line item. '
        '<b>Prompt injection via a wiki page</b>: retrieved text is data, never instruction, '
        'delimited as such &mdash; and this system holds no tool authority at all, which is the '
        'cheapest defence on the table and worth saying. <b>Stale semantic cache</b> after an '
        'edit: invalidate by document ID on ingest, not by TTL alone. <b>ACL drift</b>: re-check '
        'permissions at query time against live groups, never the snapshot taken at ingestion. '
        'And the eval trap &mdash; recall@10 of 0.91 with faithfulness 0.6 is a system that '
        'confidently invents answers out of the correct documents.',
    ],
    tech_note=('Be honest about which numbers are which. The 34M chunks, the 209&rarr;58 GB sizing '
               'and the &#36;96K/month are <i>derived arithmetic</i> from published unit prices, '
               'compression ratios and Qdrant&rsquo;s graph formula &mdash; not benchmarks anyone '
               'ran on your corpus. The compression ratios themselves (4&times; at under 1% recall '
               'loss, 32&times; binary at 5&ndash;15%) and the vector-store latencies are '
               'measured. Present arithmetic as arithmetic; an interviewer who catches you '
               'passing off a calculation as a benchmark discounts every other number you gave.'),

    # ---------------- FIGURE ----------------
    fig=dict(
        kind='blocks', h=322,
        boxes=[
            dict(x=20,  y=44,  w=84,  h=48, t='query', sub='23 QPS peak'),
            dict(x=124, y=44,  w=126, h=48, t='ACL pre-filter', sub='live groups', tone='sig'),
            dict(x=274, y=18,  w=116, h=42, t='dense top-100', tone='mem'),
            dict(x=274, y=90,  w=116, h=42, t='BM25 top-100', tone='mem'),
            dict(x=414, y=44,  w=116, h=48, t='fuse + rerank', sub='top-10', tone='mem'),
            dict(x=554, y=44,  w=146, h=48, t='LLM + cites', sub='6K in, 400 out', tone='mem'),
            dict(x=20,  y=140, w=112, h=44, t='semantic cache', sub='hit under 5 ms'),
            dict(x=148, y=140, w=146, h=44, t='ACL sidecar', sub='live, not the snapshot'),
            dict(x=20,  y=232, w=104, h=48, t='connectors', sub='CDC queue'),
            dict(x=148, y=232, w=110, h=48, t='chunk 512/50', sub='34M chunks'),
            dict(x=282, y=232, w=100, h=48, t='embed', sub='345 dollars'),
            dict(x=406, y=232, w=136, h=48, t='dual index', sub='58 GB at int8', tone='mem'),
            dict(x=566, y=232, w=134, h=48, t='index version', sub='dual, ramp, roll back'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=1, b=3),
            dict(a=2, b=4), dict(a=3, b=4), dict(a=4, b=5),
            dict(a=0, b=6, side='down'),
            dict(a=7, b=1, side='up', tone='sig'),
            dict(a=8, b=9), dict(a=9, b=10), dict(a=10, b=11), dict(a=11, b=12),
            dict(a=9, b=7, side='up'),
            dict(a=11, b=3, side='up', dash='4 3', label='minutes to nightly'),
        ],
        labels=[
            dict(x=20, y=18, t='REQUEST PATH', a='start'),
            dict(x=20, y=212, t='INDEXING, OFFLINE', a='start'),
        ],
        foot='the permission filter runs inside both retrievers, never after them',
        alt=('Architecture diagram. Top row, left to right: a query passes a permission '
             'pre-filter, fans out to dense and keyword retrieval, is fused and reranked down to '
             'ten passages, and is answered by the model with citations. A middle row holds the '
             'semantic cache and the per-chunk permission sidecar that the query path reads. A '
             'bottom row, offline, runs connectors to chunking to embedding to a dual index that '
             'feeds retrieval on a minutes-to-nightly schedule.')),
    caption=('The pink box is the binding constraint: permissions are applied inside both '
             'retrievers, so the candidate pool is already legal before fusion sees it. Everything '
             'teal is what carries the answer &mdash; two indexes, one reranker, one grounded '
             'generation. Note that the offline row, not the online one, is where the money and '
             'the cutover risk live.'),
    caption_simple=('The pink box is the hard part: who is allowed to see what, checked inside the '
                    'search rather than after it. The teal boxes are the ones that actually '
                    'produce the answer. The bottom row runs overnight and on a schedule, and it '
                    'is where the cost and the upgrade risk sit.'),

    # ---------------- SHARED ----------------
    when_label='The interviewer is really testing',
    when=[
        'Whether you ask about per-user permissions before you draw a single box',
        'Whether you can size the index in your head and land on one node, not a cluster',
        'Whether &ldquo;we would evaluate it&rdquo; is a sentence or an actual system with gates',
        'Whether you know what upgrading the embedding model costs, and how you cut over',
    ],
    trap=('Saying &ldquo;we retrieve the top ten and then filter out what the user cannot '
          'see&rdquo;. That is post-filtering, and it fails silently as an empty result set for '
          'precisely the users with the narrowest access &mdash; who read it as a broken product, '
          'not as a permission boundary. Pre-filter inside both retrievers instead and pay the '
          'recall-tuning cost. The second version of the trap: &ldquo;we would just re-embed '
          'everything&rdquo; when asked about an embedding upgrade. You cannot mix vector spaces, '
          'so the answer is a dual index, a shadow eval, a ramp and a rollback, priced &mdash; '
          '~&#36;345 at text-embedding-3-small, ~&#36;2,240 at large, plus ~&#36;15,300 if you are keeping '
          'contextual enrichment.'),

    nums_label='The numbers you design against',
    nums=[
        dict(k='CORPUS', v='15B tokens', s='10M documents at ~1,500 tokens each'),
        dict(k='CHUNKS', v='34M', s='512 tokens, 15% overlap'),
        dict(k='PEAK LOAD', v='23 QPS', s='2.3 average, 10&times; peak factor'),
        dict(k='INDEX IN RAM', v='58 GB', s='int8 plus graph, down from 209 GB'),
        dict(k='TTFT SLO', v='2 s p95', s='streamed, so first token is what is measured'),
        dict(k='SERVING BILL', v='~&#36;96K/month', s='~&#36;12.6K on a Flash-class model &mdash; same design'),
    ],

    ask=[
        dict(q='Do documents carry per-user permissions?',
             a='Yes &mdash; and this is the constraint that shapes the whole design. Ask it in the first two minutes.'),
        dict(q='How many users, how many queries?',
             a='~20,000 employees at ~10 queries a day: 200K/day, 2.3 QPS average, ~23 QPS peak.'),
        dict(q='Q&amp;A with citations, or search with snippets?',
             a='Q&amp;A with citations users can click through. That makes grounding a product requirement, not a nicety.'),
        dict(q='What is the latency SLO?',
             a='p95 under 2 s to first token, streaming. Which means you are budgeting TTFT, not total generation time.'),
        dict(q='How fresh must the index be?',
             a='Minutes for high-traffic sources, hours for the tail. Tier it by source rather than promising real time.'),
        dict(q='What is the document mix and average length?',
             a='Wikis, Docs, PDFs, Slack, Jira. Mixed formats, ~3 pages, call it 1,500 tokens.'),
        dict(q='What does &ldquo;good&rdquo; mean, and who judges it?',
             a='Grounded answers with correct citations, against a golden set curated by internal comms and support.'),
        dict(q='Managed vector store or self-hosted?',
             a='Managed unless data residency forbids it. At this scale it is not a scale decision.'),
    ],

    estimate=dict(
        label='The arithmetic, out loud', cost='derived, not benchmarked',
        rows=[
            dict(l='corpus', w='10M docs x 1,500 tokens', r='15B tokens'),
            dict(l='chunks', w='15B x 1.15 / 512', r='34M chunks'),
            dict(l='raw vectors, fp32', w='34M x 1,536 x 4 B', r='209 GB'),
            dict(l='int8, 4x, &lt;1% recall loss', w='209 / 4', r='52 GB'),
            dict(l='HNSW graph, M = 16', w='34M x 16 x 2 x 4 B', r='4.4 GB'),
            dict(l='ids and versions', w='34M x 40 B', r='1.4 GB'),
            dict(l='RAM per replica', w='one node, two for HA', r='58 GB', tot=True),
        ],
        note=('Every row above is arithmetic you perform in the room, not a benchmark: the inputs '
              'are published unit sizes and compression ratios, the results are yours. The one to '
              'say slowly is 209 to 58 &mdash; it converts &ldquo;we will need a cluster&rdquo; '
              'into &ldquo;we will need a machine, and a second one for failover&rdquo;.')),

    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='DENSE VS HYBRID',
             v='<b>Hybrid, and not as a hedge.</b> Argue it with the concrete failure: '
               '&ldquo;a query for INC-2024-00847 will not be answered by cosine similarity.&rdquo; '
               'The fusion step is worth arguing too &mdash; plain RRF buys +1.3% NDCG over BM25, '
               'tiered boosting +7.5%.'),
        dict(k='RERANK VS LATENCY',
             v='<b>Take the reranker, then make it the first rung you drop.</b> A cross-encoder '
               'costs 50&ndash;150 ms on GPU and one report puts P@10 at 0.62 &rarr; 0.84. Under '
               'load, degrade to fusion-only and keep answering rather than shedding requests.'),
        dict(k='CHUNK SIZE',
             v='<b>512 with overlap, plus parent-document retrieval.</b> Small chunks retrieve '
               'better and answer worse: semantic chunking hit 91.9% retrieval recall and still '
               'lost end to end, 54% against 69% for recursive 512. Fix the answer with a bigger '
               'parent, not a smaller chunk.'),
        dict(k='PERMISSIONS IN OR AFTER',
             v='<b>Pre-filter, inside both retrievers.</b> Post-filtering is one line of code and '
               'it produces empty result sets for restricted users, which reads as &ldquo;this is '
               'broken&rdquo; rather than &ldquo;this is not for you&rdquo;. Pre-filtering costs '
               'recall tuning effort; that is the whole price.'),
        dict(k='FRESHNESS VS COST',
             v='<b>Tier by source.</b> Minutes for policy docs and runbooks, nightly for the '
               'archive. Real-time indexing of every Slack message is expensive and nobody has '
               'ever asked for it.'),
        dict(k='MANAGED VS SELF-HOSTED',
             v='<b>Not a scale decision at all.</b> At 34M vectors and 23 QPS both work. It is a '
               'data-residency and operational-headcount decision &mdash; say that instead of '
               'benchmarking, because reaching for a benchmark here is the wrong instinct on '
               'display.'),
    ],

    verdict=dict(
        no='Draws documents &rarr; embeddings &rarr; vector database &rarr; LLM, names a vector '
           'database brand as though that were the design, never computes the index size, never '
           'mentions permissions, treats &ldquo;we would evaluate it&rdquo; as a sentence rather '
           'than a system, and answers the embedding-upgrade question with &ldquo;we would '
           're-embed everything&rdquo; &mdash; no cost, no cutover, no dual index.',
        yes='Asks about permissions in the first two minutes and calls it the hardest part. '
            'Computes 34M chunks and 209 GB &rarr; 58 GB out loud. Picks hybrid retrieval and '
            'justifies it with a ticket ID rather than with &ldquo;best of both worlds&rdquo;. '
            'Names the right-document-wrong-section failure before being asked. Prices the '
            're-index. Separates retrieval metrics from generation metrics and attaches a number '
            'to each.'),

    real_label='Where the retrieval numbers come from',
    real=('Anthropic&rsquo;s contextual retrieval work (September 2024) prepends a short generated '
          'context header to each chunk before embedding. Top-20 retrieval failure fell from 5.7% '
          'to 3.7%; adding contextual BM25 took it to 2.9%, a 49% reduction; adding reranking took '
          'it to 1.9%, a 67% reduction. The header generation costs &#36;1.02 per million document '
          'tokens, which on this 15B-token corpus is ~&#36;15,300 one-off &mdash; a real line item, '
          'and the part people leave out when they quote the 67%.'),

    math=dict(
        tex=r'\text{RAM} = \underbrace{N \times D \times b}_{\text{vectors}} + '
            r'\underbrace{N \times M \times 2 \times 4\,\text{B}}_{\text{HNSW graph}} + '
            r'\underbrace{N \times 40\,\text{B}}_{\text{ids and versions}}',
        note='What it does not say: $b$ is a decision, not a constant. int8 is 4&times; at under '
             '1% recall loss, binary is 32&times; at 5&ndash;15%. Choose the compression against '
             'your recall target first, then read the RAM number off this line.',
        cost='one replica, HNSW'),

    drills=[
        dict(q='A user asks a question whose answer is spread across four documents. What breaks?',
             a=('<b>Top-k breaks, and it breaks quietly.</b> Ranking scores each chunk '
                'independently, so the shortlist fills with four near-duplicates of the single '
                'best-matching passage instead of one passage from each source &mdash; and the '
                'model then answers confidently from a quarter of the evidence, with citations '
                'that all look correct. Three fixes in cost order: diversity-aware selection (MMR) '
                'at the fusion step so near-identical chunks stop crowding each other out; query '
                'decomposition into sub-questions with a union of results; and a multi-hop tag in '
                'the golden set so the regression is visible next time. Skip the third and you '
                'will not notice when it returns.'),
             a_simple=('<b>The shortlist fills up with four copies of the same thing.</b> Each '
                       'passage is scored on its own, so the ten that look most like the question '
                       'are usually ten versions of the same paragraph rather than one from each '
                       'document. The model answers confidently from a quarter of the evidence, '
                       'and every citation it gives you checks out, which is what makes it hard to '
                       'spot. Fix it by forcing the shortlist to be varied rather than merely '
                       'similar, by splitting the question into parts and searching each part, and '
                       'by tagging these cases in your test set so you can see the problem come '
                       'back.')),
        dict(q='Cut serving cost by 5x without a quality drop users notice. Go.',
             a=('<b>Routing does most of it, and you should say so before you list anything '
                'else.</b> A small classifier sends the ~70% of queries that are simple lookups to '
                'a Flash-class model and keeps the frontier model for synthesis &mdash; that alone '
                'is most of the distance between ~&#36;96K and ~&#36;12.6K a month. Then prefix caching on '
                'the system prompt, where cached reads bill at ~10% of the input rate. Then shrink '
                'context from 10 chunks to 5, but only after checking that context precision '
                'supports it. Together these plausibly reach 5&times;; that total is derived '
                'arithmetic rather than a measured result, so quote it as an estimate and name '
                'what would move it.'),
             a_simple=('<b>Send the easy questions to the cheap model.</b> Roughly seven in ten '
                       'queries are simple lookups a small model answers just as well, and that '
                       'single decision is most of the difference between about ninety-six '
                       'thousand dollars a month and about thirteen thousand. Then stop paying '
                       'full price to re-read the same instructions on every request &mdash; '
                       'cached reading costs about a tenth. Then send five passages instead of '
                       'ten, but only once you have checked the answer still sits inside the five. '
                       'Order matters: routing first, because the other two are rounding errors '
                       'beside it.')),
        dict(q='How do you know it got better?',
             a=('<b>Two layers of metric, measured separately, or you are shipping blind.</b> '
                'Build a golden set of 300&ndash;1,000 cases harvested from real failures and '
                'tagged by failure mode. Calibrate the judge against 100 human labels until '
                'Spearman is &ge;0.85 &mdash; 0.70 is only good enough for low-stakes work. Gate '
                'CI at faithfulness 0.85 and context recall 0.80 with a 5% regression tolerance, '
                'then sample 10% of live traffic and alert when rolling faithfulness falls below '
                '0.75. The reason to keep the layers apart: recall@10 of 0.91 alongside '
                'faithfulness of 0.6 is a system confidently inventing answers from the correct '
                'documents, and any single blended score hides exactly that case.'),
             a_simple=('<b>Two scores, never one.</b> Measure separately whether the right '
                       'passages were found, and whether the answer actually followed from them. '
                       'A system can be excellent at the first and poor at the second, which is '
                       'the worst failure you can ship: correct sources, invented answer, and it '
                       'looks convincing. Build a few hundred real failed questions into a fixed '
                       'test set, check that your automatic grader agrees with human graders '
                       'before you trust it, block a release that drops more than five percent on '
                       'either score, and keep grading a tenth of live traffic afterwards.')),
    ],

    anchor=dict(
        formula=r'$34\text{M} \times 1536 \times 4\,\text{B} = 209\ \text{GB}$ '
                r'&nbsp;&middot;&nbsp; int8 + graph &nbsp;&middot;&nbsp; $58\ \text{GB}$',
        formula_simple=('Thirty-four million passages, each a list of 1,536 numbers. At four bytes '
                        'a number that is 209 gigabytes; at one byte a number, plus the search '
                        'graph, it is 58. One machine, two for safety.'),
        bullets=[
            'Permissions decide the architecture; the vector store brand is a detail',
            'Size the index twice &mdash; raw and quantised &mdash; and say both numbers',
            'At this scale the LLM is the bottleneck, so cost work means routing, not sharding',
        ]),
    chips=['hybrid retrieval', 'cross-encoder rerank', 'ACL pre-filter', 'semantic cache',
           'golden set and judge'],
    followup='A user asks a question whose answer is spread across four documents. What breaks?',
),
dict(
    id='inference-serving-70b',
    tier='advanced',
    title='Design: an inference layer for a 70B model',
    kicker='KV cache memory is the binding constraint, and quantisation is a ten-fold cost decision rather than a speed tweak',

    # ---------------- SIMPLE LAYER ----------------
    simple=[
        'A 70-billion-parameter model does not fit on one graphics card, so the first decision is '
        'how many cards hold one copy and how much room is left over. Two cards give you 160 '
        'gigabytes. The model&rsquo;s weights take 140 of that at full precision, and about ten '
        'more disappear into framework overhead, which leaves roughly ten gigabytes for the part '
        'nobody expects to matter: the scratch memory each conversation keeps alive while it is '
        'being answered.',
        'That scratch memory is the whole design. Every token in a request &mdash; prompt and '
        'reply &mdash; leaves behind about a third of a megabyte that has to stay resident until '
        'the request finishes. At fifteen hundred tokens a request, ten gigabytes of headroom '
        'holds about twenty conversations at once. Store the weights and the scratch at half the '
        'precision and the same two cards hold about three hundred and twenty-five. Serving ten '
        'thousand people at once is then either six hundred and sixty-six cards or sixty-two, '
        'which is roughly one and a half million dollars a month against a hundred and thirty '
        'thousand. Same model, same service level, one decision.',
        'Everything else in the design protects that pool of scratch memory. Requests queue in '
        'front of a scheduler that keeps a batch running and slots new work in as old work '
        'finishes, instead of waiting for a whole batch to end. Traffic that shares the same long '
        'instructions is sent to the same machine so the work of reading them is done once. A '
        'small pool of machines is kept warm and idle, because starting one takes about a minute '
        'and most traffic spikes are shorter than that &mdash; and the idle time is paid for by '
        'letting overnight batch jobs run there.',
    ],
    analogy=('<b>Like a restaurant kitchen with a very small pass.</b> The chefs and the recipes '
             'are fixed cost; what actually limits how many tables you serve is the counter space '
             'where half-finished plates wait. Every diner occupies a slice of that counter from '
             'first course to last. Buying more chefs does nothing once the counter is full, and '
             'using smaller plates doubles the covers.'),
    trap_simple=('Two sentences sink this round. The first is &ldquo;we would put the standard '
                 'serving framework behind a load balancer and scale up when the cards get '
                 'busy&rdquo; &mdash; scaling up takes about a minute to load the model, and most '
                 'spikes are over before the new machine is ready. The second is quieter and '
                 'worse: working out that the whole company only needs a few thousand tokens a '
                 'second, dividing by what one card produces, and concluding you need about three '
                 'cards. That sum is correct and the answer is twenty times too small, because it '
                 'sizes for the average rather than for how many conversations are open at once '
                 '&mdash; and it is open conversations that consume the memory.'),

    # ---------------- TECHNICAL LAYER ----------------
    tech=[
        'Start at memory, because memory is the constraint and everything else is downstream of '
        'it. Weights: $70\\text{B} \\times 2\\,\\text{B} = 140$ GB at BF16, 70 GB at FP8, 35 GB at '
        'INT4, plus 15&ndash;20% for activations, framework and CUDA context. KV cache per token '
        'for this architecture (80 layers, 8 KV heads via GQA, head dim 128) is '
        '$2 \\times 80 \\times 8 \\times 128 \\times 2\\,\\text{B} = 0.327$ MB, halving to 0.164 '
        'MB at FP8. On a 2&times;H100 shard: BF16 leaves $160 - 140 - 10 \\approx 10$ GB for KV, '
        'and a 1,500-token request needs 0.49 GB, so <b>~20 concurrent</b>. FP8 leaves ~80 GB '
        'against 0.25 GB per request, so <b>~325 concurrent</b>. For 10,000 in flight that is '
        '<b>~62 H100s</b>, against the <b>~666</b> the published BF16 walkthrough lands on, and at '
        'Lambda&rsquo;s &#36;2.99/GPU-hr that is <b>~&#36;1.43M/month against ~&#36;133K/month</b>. '
        'Quantisation here is a ten-fold cost decision, not a speed tweak.',
        'Now the sizing trap, and say it before they spring it. If those users make 1M requests a '
        'day at 500 output tokens, that is 500M output tokens/day, about 5,800 tokens/s on '
        'average, and one H100 running this model at FP8 and concurrency 100 produces '
        '2,400&ndash;2,780 tokens/s &mdash; so average throughput needs about <b>3 GPUs</b>. '
        'Concurrency sizing said 62. Both sums are correct; they answer different questions, and '
        'the gap is queueing and burstiness. &ldquo;I am sizing on concurrency, because the SLO is '
        'TTFT&rdquo; is the sentence that marks the level.',
        'The path, in order: client &rarr; API gateway (auth, per-tenant rate limits, validation, '
        'SSE for streaming) &rarr; model router doing <b>prefix-aware consistent hashing</b>, so '
        'requests sharing a system prompt land on the same scheduler and hit its prefix cache '
        '&rarr; per-model scheduler owning the active batch and the waiting queue, doing '
        'continuous batching and admission control &rarr; workers owning GPUs, weights and a '
        '<b>paged KV pool in 16-token blocks</b> &rarr; optionally separate prefill and decode '
        'pools with a KV transfer path between them. Off the hot path: a warm standby pool, a '
        'batch queue that backfills idle capacity, and a metering pipeline emitting tokens and '
        'cost per tenant.',
        'Failure modes. <b>OOM under a long-context burst</b>: preempt the longest-running '
        'request, swapping its KV to host memory or recomputing it, and let admission control '
        'refuse before the pool is exhausted rather than after. <b>Client disconnects mid-stream</b>: '
        'without cancellation propagation a client that opens and immediately closes connections '
        'DDoSes you while workers keep generating for nobody. <b>Tenant runaway</b>: one team&rsquo;s '
        'retry loop eats the fleet, so per-tenant token-rate limits and a circuit breaker at '
        '3&times; rolling spend. <b>Cold start</b>: ~62 s for vLLM and ~28 minutes if a TensorRT '
        'engine has to compile, so pre-compile engines in CI and ship artefacts &mdash; never '
        'compile in the serving path. <b>Prefix cache thrash</b>: prefix-blind routing turns one '
        'shared 2,000-token system prompt into a per-replica cost. <b>Silent regression from a '
        'quantisation rollout</b>: FP8 is a model change and goes through the model-change gates, '
        'not the config-change ones.',
    ],
    tech_note=('Which numbers are which matters. The weight sizes, the 0.327 MB/token, the '
               'throughput table and the 62-second cold start are published figures. The ~325 '
               'concurrent, the ~62 GPUs and the ~&#36;133K/month are <i>my arithmetic on top of '
               'them</i>, and they assume every request holds 1,500 tokens of KV for its whole '
               'life &mdash; which overstates memory for short requests and understates it for '
               'long ones. The published walkthrough gets ~30 per BF16 shard where this gets '
               '~20, on a different overhead assumption; the order is what is scored. Quote the '
               'band, not the digit.'),

    # ---------------- FIGURE ----------------
    fig=dict(
        kind='blocks', h=336,
        boxes=[
            dict(x=20,  y=44,  w=88,  h=48, t='client', sub='10K in flight'),
            dict(x=126, y=44,  w=112, h=48, t='API gateway', sub='auth, SSE'),
            dict(x=256, y=44,  w=126, h=48, t='prefix router', sub='hash on prefix'),
            dict(x=400, y=44,  w=132, h=48, t='scheduler', sub='continuous batch', tone='mem'),
            dict(x=556, y=16,  w=144, h=44, t='workers', sub='70 GB FP8 weights', tone='mem'),
            dict(x=556, y=80,  w=144, h=50, t='paged KV pool', sub='325 seqs per shard', tone='sig'),
            dict(x=400, y=158, w=132, h=48, t='admission control', sub='bounds the queue'),
            dict(x=556, y=158, w=144, h=48, t='chunked prefill', sub='TTFT is queueing'),
            dict(x=20,  y=258, w=150, h=48, t='warm standby', sub='62 s cold start'),
            dict(x=196, y=258, w=140, h=48, t='batch queue', sub='backfills idle GPUs'),
            dict(x=362, y=258, w=140, h=48, t='per-tenant meter', sub='tokens and dollars'),
            dict(x=528, y=258, w=172, h=48, t='eval gate', sub='FP8 is a model change'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3),
            dict(a=3, b=4), dict(a=3, b=5, tone='sig'), dict(a=4, b=5, side='down'),
            dict(a=3, b=6, side='down'), dict(a=6, b=7),
            dict(a=9, b=3, side='up', dash='4 3', label='backfill'),
        ],
        labels=[
            dict(x=20, y=18, t='REQUEST PATH', a='start'),
            dict(x=20, y=238, t='OFF THE HOT PATH', a='start'),
        ],
        foot='the KV pool is what runs out: one 2-GPU shard holds ~325 sequences at FP8, ~20 at BF16',
        alt=('Architecture diagram. Top row, left to right: client, API gateway, prefix-aware '
             'router, scheduler, and on the right a worker box above the paged KV cache pool that '
             'the scheduler also feeds. Below the scheduler sit admission control and chunked '
             'prefill. A bottom row off the hot path holds a warm standby pool, a batch queue that '
             'backfills idle GPUs into the scheduler, per-tenant metering and an eval gate on '
             'quantisation.')),
    caption=('The pink box is the binding constraint. Weights are a fixed cost you pay once per '
             'shard; the KV pool is the variable cost that decides how many people fit, so the '
             'scheduler is drawn feeding it directly rather than feeding the worker alone. '
             'Everything on the bottom row exists because the top row cannot be scaled reactively '
             'against a 62-second cold start.'),
    caption_simple=('The pink box is the scratch memory each open conversation holds, and it is '
                    'what runs out first &mdash; not the model itself. The bottom row exists '
                    'because starting a new machine takes about a minute, so you keep some warm '
                    'and pay for them with overnight batch work.'),

    # ---------------- SHARED ----------------
    when_label='The interviewer is really testing',
    when=[
        'Whether you name the binding constraint before you name a serving framework',
        'Whether you size on peak concurrency or on average throughput &mdash; and whether you notice which',
        'Whether quantisation is a first-class decision or a footnote you add when pushed',
        'Whether you have thought about the first sixty seconds after a deploy',
    ],
    trap=('Two sentences sink this round. The first: &ldquo;we would run vLLM behind a load '
          'balancer and autoscale on GPU utilisation.&rdquo; Reactive autoscaling cannot help when '
          'the cold start is ~62 s and the spike is shorter than the scale-up. The second is '
          'quieter and much worse: &ldquo;500M output tokens a day over 2,400 tokens/s is about '
          'three H100s.&rdquo; The arithmetic is correct and the answer is twenty-fold wrong, '
          'because it sizes for average throughput while the SLO is p95 TTFT and the memory is '
          'held by concurrent sequences, not by tokens per second. Name which of the two you are '
          'sizing on, out loud, and the trap disappears.'),

    nums_label='The numbers you design against',
    nums=[
        dict(k='WEIGHTS', v='140 / 70 / 35 GB', s='BF16, FP8, INT4 &mdash; plus 15&ndash;20% overhead'),
        dict(k='KV PER TOKEN', v='0.327 MB', s='80 layers, 8 KV heads, head dim 128; 0.164 at FP8'),
        dict(k='PER 2&times;H100 SHARD', v='~20 vs ~325', s='concurrent 1,500-token requests, BF16 vs FP8'),
        dict(k='FLEET FOR 10K', v='~666 vs ~62 GPUs', s='same SLO, one quantisation decision apart'),
        dict(k='THE BILL', v='&#36;1.43M vs &#36;133K', s='per month at Lambda&rsquo;s &#36;2.99/GPU-hr'),
        dict(k='COLD START', v='62 s', s='vLLM; ~28 min if a TensorRT engine must compile'),
    ],

    ask=[
        dict(q='Can we quantise, if quality holds on the eval set?',
             a='Yes &mdash; and it is the highest-leverage question in the prompt. It is the difference between ~666 GPUs and ~62.'),
        dict(q='How many models, and what sizes?',
             a='One 70B, plus a small model for routing and classification. That second one pays for itself twice.'),
        dict(q='Interactive chat, or batch?',
             a='Both. Which is what lets batch work backfill the idle capacity you are already paying for.'),
        dict(q='What are the SLOs?',
             a='p95 TTFT under 500 ms interactive, inter-token under 50 ms. TTFT is the one that shapes the scheduler.'),
        dict(q='Peak concurrency?',
             a='~10,000 in flight. Ask for concurrency, not QPS &mdash; concurrency is what holds memory.'),
        dict(q='Typical prompt and output length?',
             a='~1,000 in, ~500 out. Call it 1,500 tokens of KV per request and carry that through every sum.'),
        dict(q='Multi-tenant: hard isolation, or accounting?',
             a='Accounting and fair-share. That rules out per-tenant fleets before anyone proposes one.'),
        dict(q='What hardware is available?',
             a='H100 80 GB, tensor-parallel across 2 GPUs. So the unit you are sizing is a 160 GB shard.'),
    ],

    estimate=dict(
        label='The arithmetic, out loud', cost='FP8 column; derived from sourced sizes',
        rows=[
            dict(l='weights, BF16', w='70B x 2 B', r='140 GB'),
            dict(l='weights, FP8', w='70B x 1 B', r='70 GB'),
            dict(l='KV per token, BF16', w='2 x 80 x 8 x 128 x 2 B', r='0.327 MB'),
            dict(l='KV per request, FP8', w='1,500 tokens x 0.164 MB', r='0.25 GB'),
            dict(l='free for KV on a 160 GB shard', w='160 - 70 - 10 overhead', r='~80 GB'),
            dict(l='concurrency per shard', w='80 / 0.25', r='~325 requests'),
            dict(l='fleet for 10,000 in flight', w='10,000 / 325, x 2 GPUs', r='~62 H100s', tot=True),
        ],
        note=('Run the same table at BF16 and you get ~10 GB free and ~20 per shard, so ~500 '
              'shards; the published walkthrough assumes ~30 per shard and lands on ~333 shards, '
              'or ~666 H100s. Either way it is an order of magnitude more hardware than FP8, which '
              'is the point. Both fleet numbers are derived arithmetic on top of sourced memory '
              'figures rather than measured throughput, and both assume every request holds its '
              'full 1,500 tokens for its whole life &mdash; say that out loud, because it is the '
              'first thing a good interviewer pokes.')),

    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='CONTINUOUS VS STATIC BATCHING',
             v='<b>Continuous, and be able to say why in one sentence.</b> Static batching '
               'head-of-line blocks: a 50-token request and a 2,000-token request in the same '
               'batch both wait for the long one. Continuous batching over a paged KV pool gives '
               '3&ndash;5&times; the effective batch size.'),
        dict(k='THROUGHPUT VS LATENCY',
             v='<b>Sit deliberately near the knee, and know where it is.</b> An H100 needs ~300 '
               'concurrent sequences before decode becomes compute-bound. Past that, aggregate '
               'throughput keeps rising while per-user latency degrades. Exactly where you sit is '
               'an SLO decision, not a framework default.'),
        dict(k='QUANTISATION VS QUALITY',
             v='<b>FP8, gated on the eval set.</b> It roughly doubles achievable concurrency and '
               'cuts cost about ten-fold at fixed SLO here. Not free: A100s have no FP8 hardware '
               'acceleration, so on that generation you get the memory saving without the '
               'throughput saving.'),
        dict(k='DISAGGREGATE PREFILL AND DECODE',
             v='<b>Not for a dense 70B at moderate batch.</b> The wins are real elsewhere &mdash; '
               '7&times; on GB200 NVL72 with Dynamo, and +61% req/s with a 50% TTFT cut at Baseten '
               'on ~50K-token prompts &mdash; but here the KV transfer can cost more than it '
               'saves. Say what would flip it: long contexts, MoE, higher concurrency.'),
        dict(k='REACTIVE VS PREDICTIVE SCALING',
             v='<b>Predictive, plus warm standby.</b> A ~62 s cold start is longer than most '
               'spikes, so reactive scaling always arrives after the incident. Pay for the standby '
               'by backfilling batch work onto it rather than by arguing for headroom.'),
        dict(k='FAIRNESS VS UTILISATION',
             v='<b>Fair-share with per-tenant token rates.</b> Strict reservations strand GPUs; '
               'pure first-come-first-served lets one team&rsquo;s batch job starve everyone '
               'else&rsquo;s chat. Separate priority class for interactive traffic, and metering '
               'that makes the bill visible per team.'),
    ],

    verdict=dict(
        no='&ldquo;We would use vLLM behind a load balancer with autoscaling.&rdquo; Never '
           'computes weights or KV cache, sizes the fleet from average throughput without noticing '
           'which question that answers, and treats quantisation as a footnote to add if there is '
           'time at the end.',
        yes='Identifies KV cache memory as the binding constraint inside three minutes. Computes '
            '140 GB, 0.327 MB per token, ~20 against ~325 concurrent per shard, and produces both '
            'the ~666-GPU and the ~62-GPU fleet with the reason they differ. Notes that reactive '
            'autoscaling cannot beat a 62-second cold start. Catches the '
            'throughput-versus-concurrency sizing trap out loud. The published ladder is explicit '
            'here: SDE II names vLLM, SDE III names the KV cache constraint and scopes '
            'quantisation and speculative decoding unprompted, Principal frames the design as a '
            'portfolio of tradeoffs and asks when it breaks.'),

    real_label='Where the latency actually goes',
    real=('On a single H100 running Llama-3.3-70B at FP8, vLLM 0.18 goes from 120 tokens/s at '
          'concurrency 1 to 2,400 tokens/s at concurrency 100 &mdash; twenty times the throughput '
          'on the same card. Over that same range p95 TTFT goes from 68 ms to 1,450 ms. Nothing '
          'got slower; the queue got longer, and almost all of that 1,450 ms is waiting rather '
          'than computing. Baseten&rsquo;s disaggregated prefill/decode rollout attacks exactly '
          'that layer and reports +61% requests/s with a 50% TTFT reduction on ~50K-token prompts.'),

    math=dict(
        tex=r'\text{KV bytes} = 2 \times L \times H_{kv} \times d_{h} \times '
            r'\text{seq} \times \text{batch} \times b',
        note='The 2 is keys and values. $H_{kv}$ is 8 rather than 64 because of grouped-query '
             'attention, and that factor of eight is the only reason serving a 70B model is '
             'affordable at all. What the formula hides: $\\text{seq}$ is the <i>whole</i> '
             'sequence, so a long-context request holds its memory for the entire generation.',
        cost='per token, per request'),

    drills=[
        dict(q='Cut p95 time-to-first-token in half.',
             a=('<b>Attack prefill and queueing &mdash; decode is not where the time is.</b> TTFT '
                'is how long the request waited plus how long its prompt took to prefill, and the '
                'benchmark shows it: the same card goes from 68 ms p95 at concurrency 1 to '
                '1,450 ms at concurrency 100. So: chunked prefill, so one long prompt cannot '
                'block the batch; prefix caching for the shared system prompt, which is '
                'free if the router is prefix-aware; and admission control to bound queue depth, '
                'trading a little throughput for the tail you are measured on. If long contexts '
                'dominate, disaggregate prefill and decode for the 50% TTFT cut Baseten reported. '
                'Adding GPUs works only through queue depth, and it is the most expensive way to '
                'buy it.'),
             a_simple=('<b>Look at the waiting, not the typing.</b> Time to first token is mostly '
                       'how long the request sat in a queue plus how long it took to read the '
                       'prompt, not how fast the model writes. The same card answers in about '
                       'seventy milliseconds with one user and takes almost a second and a half '
                       'with a hundred &mdash; nothing about the hardware changed, the line got '
                       'longer. So break long prompts into pieces that cannot block everyone '
                       'behind them, reuse the work already done on the shared instructions, and '
                       'cap how many requests you let in so the queue stays short. Buying more '
                       'machines also works, and it is the most expensive way to shorten a '
                       'queue.')),
        dict(q='A team wants a fine-tuned variant. Do they get their own fleet?',
             a=('<b>No &mdash; LoRA adapters on a shared base, swapped per request.</b> A full '
                'fine-tune brings its own 70 GB of weights and its own KV pool, so every team that '
                'asks multiplies the fleet; adapters are a few hundred megabytes and ride the base '
                'model&rsquo;s batch. Promote a variant to a dedicated fleet only when its own '
                'traffic would keep a shard busy, which is a utilisation sum you can do in front '
                'of them rather than a policy argument. The exception worth naming: if their '
                'variant changes the architecture or the quantisation, it is a different model and '
                'the adapter route is closed.'),
             a_simple=('<b>No. Give them a small add-on layer that rides on the shared model.</b> '
                       'A separate copy needs its own seventy gigabytes and its own share of the '
                       'machines, so every team that asks multiplies the bill. The add-on layers '
                       'are a few hundred megabytes and can be swapped in per request against one '
                       'shared copy. A team earns its own machines when its own traffic would keep '
                       'those machines busy &mdash; that is a sum you can do with them in the '
                       'room, not a policy you have to defend.')),
        dict(q='Speculative decoding: yes or no?',
             a=('<b>Yes at low concurrency, no at high, and the sign flips at the roofline.</b> '
                'With few sequences in flight the GPU is memory-bound &mdash; it is streaming '
                'weights from HBM every step and the FLOPs are sitting idle &mdash; so a draft '
                'model verifying several tokens per pass buys real latency for free. Past the '
                'batching knee, around 300 concurrent sequences on an H100, decode is '
                'compute-bound and the draft competes for the same FLOPs as traffic that is '
                'already paying. So it is a per-pool decision: on for the interactive pool, off '
                'for the batch pool. &ldquo;It is a knob whose sign depends on where you sit on '
                'the roofline&rdquo; answers the question they actually asked.'),
             a_simple=('<b>Yes when the machine is half idle, no when it is busy.</b> The trick '
                       'has a small fast model guess the next few words and the big model check '
                       'them all in one pass. When only a handful of conversations are running, '
                       'the big model spends most of its time waiting on memory, so the checking '
                       'is nearly free and everyone gets answers sooner. When hundreds are '
                       'running, the machine is already flat out on work that people are paying '
                       'for, and the guesses compete with them. So switch it on for the '
                       'interactive pool and off for the bulk one.')),
    ],

    anchor=dict(
        formula=r'$2 \times 80 \times 8 \times 128 \times 2\,\text{B} = 0.327\ \text{MB/token}$ '
                r'&nbsp;&middot;&nbsp; $\times\,1500 \times N_{\text{concurrent}}$',
        formula_simple=('Every token in flight keeps about a third of a megabyte of scratch memory '
                        'alive until its request finishes, or half that at reduced precision. '
                        'Multiply by tokens per request, then by open requests. That product, not '
                        'the model weights, is what runs out.'),
        bullets=[
            'Weights are the fixed cost; the KV cache is the variable one, and it is what runs out',
            'Size on concurrency when the SLO is time to first token &mdash; size on throughput and you land twenty-fold low',
            'A 62-second cold start rules out reactive autoscaling, so warm standby is not optional',
        ]),
    chips=['paged KV cache', 'continuous batching', 'FP8 quantisation', 'prefix-aware routing',
           'speculative decoding'],
    followup='Cut p95 time-to-first-token in half.',
),
dict(
    id='support-agent',
    tier='advanced',
    title='Design: a customer-support agent',
    kicker='Pin down what &ldquo;resolved&rdquo; means before you draw anything, then put authority in the tool layer rather than the prompt',

    # ---------------- SIMPLE LAYER ----------------
    simple=[
        'A message arrives on chat or email. A fast classifier checks it for abuse and for '
        'attempts to hijack the agent. A small, cheap model then decides which of four things it '
        'is: a question the help centre already answers, an account action, something genuinely '
        'complicated, or something out of scope. Roughly seven in ten are the first kind and never '
        'need the expensive model at all. For the rest a loop runs &mdash; the model proposes a '
        'step, a tool carries it out, the model reads the result &mdash; and it stops when the job '
        'is done or when it hits a hard limit: fifteen steps, a spending cap for that one '
        'conversation, and a check that it has not just called the same tool with the same '
        'arguments twice.',
        'The structural decision is that the model never performs an action. It asks the tool '
        'layer, and a separate piece of ordinary software decides whether the action is allowed: '
        'who the customer is, whether the order qualifies, whether the refund sits under the value '
        'limit that needs a person to approve it. That software never reads the conversation, so '
        'nothing a customer types can argue it round. An invented refund is impossible in the same '
        'way an invalid amount is impossible &mdash; it never reaches the payment system.',
        'The number everyone quotes is the one to distrust. There is no industry definition of '
        '&ldquo;resolved&rdquo;: handing a customer a set of instructions counts for some '
        'vendors, and a chat the customer abandoned in frustration counts for others. Insist on a '
        'written definition &mdash; closed without a human touch and not reopened within seven '
        'days &mdash; before you design, and measure how many customers come back beside it. '
        'Optimise the headline figure alone and you will build an agent that refuses to escalate.',
    ],
    analogy=('<b>Like a new call-centre agent with a locked till.</b> They can look anything up, '
             'say anything reassuring, and start a refund &mdash; but the till only opens for '
             'amounts under the limit printed on their badge, and a supervisor holds the key for '
             'the rest. Training them better changes what they say. It never changes what the till '
             'does.'),
    trap_simple=('Saying &ldquo;we would prompt it carefully so it never promises a refund it '
                 'cannot give&rdquo;. An instruction is a request, not a control: the same message '
                 'box that carries your instruction carries the customer trying to undo it. The '
                 'safeguard has to be structural &mdash; the model asks, and separate software '
                 'that never reads the chat decides. The second trap is quoting a resolution rate '
                 'as though it meant the same thing everywhere. Ask what the number counts before '
                 'you agree to be measured on it.'),

    # ---------------- TECHNICAL LAYER ----------------
    tech=[
        'Pin the metric before the architecture, because everything downstream is scored against '
        'it. Intercom reports Fin averaging a <b>76% resolution rate</b> under its own definition, '
        'which counts procedure handoffs; one FCA-regulated customer reports <b>60% inbound and '
        '90% outbound</b> under a definition it wrote itself. There is no standard &mdash; '
        'deflection is routinely counted as resolution, and so are abandoned chats. So write it '
        'down: closed with no human touch and no reopen within 7 days. Naming this problem '
        'unprompted is one of the strongest signals available in this prompt.',
        'Sizing. 1M conversations/month is ~33K/day, 0.4/s average and ~1.2/s on promo days: not a '
        'throughput problem. Per conversation, 5 turns of (1,500 system + ~1,000 history + 2,000 '
        'retrieved + 800 tool schemas) is <b>~26,000 input tokens</b> and ~1,500 output: &#36;0.067 at '
        'a mid-tier model, <b>~&#36;0.045</b> once you prefix-cache the ~2,300 static tokens per turn '
        'at ~10% of the input rate, <b>~&#36;0.007</b> on a small model. So &#36;45K/month against &#36;7K, '
        'and the routing decision is the entire cost model. Latency: 5 turns at ~400 ms TTFT plus '
        '150 output tokens at 20 ms, plus ~300 ms per tool call, is <b>~18 s p50 and '
        '35&ndash;45 s p95</b> end to end &mdash; which is why the UI narrates &ldquo;checking your '
        'order&hellip;&rdquo; rather than showing a spinner.',
        'The path, in order: channel adapters &rarr; conversation service (session state, history '
        'compaction) &rarr; input guardrail at &lt;90 ms &rarr; intent router on a small model (FAQ '
        '/ account action / complex / out of scope) &rarr; agent loop {plan, select tool, execute, '
        'observe} bounded by ~15 steps, a per-task dollar cap and repetition detection &rarr; '
        '<b>tool layer behind a deterministic policy engine</b>, where every tool carries an ACL, '
        'an idempotency key and a value threshold above which a human approves &rarr; hybrid '
        'retrieval with reranking over ~5,000 articles &rarr; generation with citations &rarr; '
        'output guardrail. Off the path: an escalation queue carrying the transcript, the tool '
        'trace and the agent&rsquo;s stated hypothesis, and an eval pipeline sampling 10% of '
        'conversations plus 100% of escalations. History lives in a session store, long-term '
        'customer memory in the CRM read <i>as a tool</i> rather than stuffed into context, and the '
        'scratchpad outside the context window so long tasks do not degrade.',
        'Failure modes. <b>A loop that never terminates</b> costs a published &#36;50&ndash;500 before '
        'anyone notices: hard step cap, repetition detection at two identical calls, token budget, '
        'circuit breaker at 3&times; rolling hourly spend. <b>Cost blowup from retries</b> &mdash; '
        'one code-review agent charged &#36;12 against a &#36;0.40 average &mdash; so the dollar cap is '
        'per task, not only per tenant. <b>Hallucinated action</b>, an HR agent sending welcome '
        'emails on imagined acceptance status: verify against the source of truth before '
        'executing, and schema-validate every tool result. <b>Prompt injection</b> via the ticket '
        'or a retrieved review: untrusted-data framing, authority at the tool layer. '
        '<b>Wrong-but-confident refund</b>: idempotency keys, an approval threshold, daily '
        'reconciliation of AI-initiated financial actions. <b>Escalation black hole</b>: the '
        'handoff payload is a designed artefact, not a link to a transcript.',
    ],
    tech_note=('Which numbers are which. The resolution benchmarks, the guardrail thresholds and '
               'the incident costs are published. The &#36;0.045 per conversation and the &#36;45K-to-&#36;7K '
               'span are <i>derived</i> from listed per-token prices and an assumed turn '
               'structure, and the 26,000 input tokens is the assumption to argue with, because '
               'moving it moves everything else. The &#36;5&ndash;8 fully loaded cost of a human '
               'ticket is a standard planning estimate rather than a published figure &mdash; use '
               'it to make the point that cost is not the binding constraint here, not as evidence '
               'for anything finer.'),

    # ---------------- FIGURE ----------------
    fig=dict(
        kind='blocks', h=326,
        boxes=[
            dict(x=20,  y=44,  w=96,  h=48, t='channels', sub='chat, email'),
            dict(x=134, y=44,  w=118, h=48, t='input guard', sub='under 90 ms'),
            dict(x=270, y=44,  w=126, h=48, t='intent router', sub='small model, 70%'),
            dict(x=414, y=44,  w=126, h=48, t='agent loop', sub='max 15 steps'),
            dict(x=558, y=44,  w=142, h=48, t='cited reply', sub='output guard', tone='mem'),
            dict(x=200, y=140, w=176, h=52, t='hybrid retrieval', sub='5,000 articles', tone='mem'),
            dict(x=414, y=140, w=180, h=52, t='policy engine', sub='ACL, idempotency, cap', tone='sig'),
            dict(x=20,  y=246, w=150, h=50, t='KB ingest', sub='versioned, rollback'),
            dict(x=196, y=246, w=170, h=50, t='escalation queue', sub='transcript plus trace'),
            dict(x=392, y=246, w=150, h=50, t='human agent', sub='keeps the context'),
            dict(x=568, y=246, w=132, h=50, t='eval sampler', sub='10%, all escalations'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3), dict(a=3, b=4),
            dict(a=3, b=5, side='left'), dict(a=3, b=6, side='down', tone='sig'),
            dict(a=6, b=8, side='down', tone='sig', label='above threshold'),
            dict(a=8, b=9),
            dict(a=7, b=5, dash='4 3'),
            dict(a=4, b=10, side='down', dash='4 3', label='sampled'),
        ],
        labels=[
            dict(x=20, y=18, t='REQUEST PATH', a='start'),
            dict(x=20, y=222, t='KB, EVAL, HANDOFF', a='start'),
        ],
        foot='authority sits in the policy engine, not the prompt: the model proposes, the tool layer disposes',
        alt=('Architecture diagram. Top row, left to right: channel adapters, an input guardrail, '
             'an intent router that sends most traffic to a small model, a bounded agent loop, and '
             'a cited reply behind an output guardrail. Below the loop sit hybrid retrieval over '
             'the help centre and the deterministic policy engine that holds tool authority. A '
             'bottom row, off the main path, holds knowledge-base ingestion feeding retrieval, an '
             'escalation queue that the policy engine fills when a value threshold is crossed, the '
             'human agent it hands off to, and an eval sampler fed from the replies.')),
    caption=('The pink path is the one that matters: the loop can only <i>ask</i>, and the policy '
             'engine decides &mdash; including when to fill the escalation queue instead of '
             'acting. Retrieval and the cited reply are what carry the answer. Note that nothing '
             'in the request path is allowed to reach a payment system directly, which is what '
             'makes a hallucinated refund a design impossibility rather than a prompt-quality '
             'problem.'),
    caption_simple=('The pink path is the important one: the agent can only ask, and a separate '
                    'piece of ordinary software decides whether the action happens or goes to a '
                    'person. The teal boxes are what produce the answer the customer reads. '
                    'Nothing in the top row can touch money on its own.'),

    # ---------------- SHARED ----------------
    when_label='The interviewer is really testing',
    when=[
        'Whether you pin down what &ldquo;resolved&rdquo; means before designing against it',
        'Whether authority lives in the tool layer or in a paragraph of prompt',
        'Whether the loop has hard bounds with actual numbers on them',
        'Whether you price a conversation without being asked to',
    ],
    trap=('Saying &ldquo;we would prompt it carefully so it does not promise a refund it cannot '
          'give&rdquo;. A prompt is a request, not a control: the same channel that carries your '
          'instruction carries the customer writing &ldquo;ignore your previous '
          'instructions&rdquo; into the chat box. The control has to be structural &mdash; the '
          'model proposes, the policy engine disposes, and that engine never reads the '
          'conversation. The second version of the trap is quoting a resolution rate as if it were '
          'a standard measure: Fin&rsquo;s 76% counts procedure handoffs, other vendors count '
          'abandoned chats, and nobody publishes a definition unless asked. Ask what the number '
          'counts.'),

    nums_label='The numbers you design against',
    nums=[
        dict(k='VOLUME', v='1M/month', s='~33K/day, 0.4/s average, ~1.2/s on promo days'),
        dict(k='PER CONVERSATION', v='~26K in, 1.5K out', s='5 turns of system, history, context, schemas'),
        dict(k='COST', v='~&#36;0.045', s='mid-tier with prefix caching; ~&#36;0.007 on a small model'),
        dict(k='MONTHLY', v='&#36;45K vs &#36;7K', s='the routing decision, and essentially nothing else'),
        dict(k='END TO END', v='~18 s p50', s='35&ndash;45 s p95, so the UI narrates the tool steps'),
        dict(k='LOOP BOUNDS', v='15 steps', s='repetition at 2 identical calls, breaker at 3&times; spend'),
    ],

    ask=[
        dict(q='What does &ldquo;resolve&rdquo; mean, precisely?',
             a='Closed with no human touch and no reopen within 7 days. Insist on it in writing &mdash; there is no industry standard.'),
        dict(q='What can the agent do, as opposed to say?',
             a='Order lookup, address change, refunds under a threshold, subscription cancel. Everything else read-only.'),
        dict(q='Where is the human in the loop?',
             a='Refunds above the threshold and anything flagged. The threshold is a business decision &mdash; ask for the number.'),
        dict(q='What volume, and how peaky?',
             a='~1M conversations a month, 3&times; on promo days. Comfortably not a throughput problem.'),
        dict(q='Channel and latency expectation?',
             a='Chat, streaming. First token under 2 s; users tolerate multi-second tool steps if the UI narrates them.'),
        dict(q='What is the knowledge base?',
             a='~5,000 help-centre articles plus policy docs. Small enough that retrieval is solved if you rerank.'),
        dict(q='Regulated?',
             a='Payments and returns policy, so an audit trail is required &mdash; which makes the tool trace a product requirement.'),
        dict(q='What is the cost ceiling?',
             a='Under &#36;0.10 per conversation. Comfortable, which tells you cost is not the binding constraint here.'),
    ],

    estimate=dict(
        label='The arithmetic, out loud', cost='derived from listed token prices',
        rows=[
            dict(l='tokens per turn', w='1,500 system + 1,000 history + 2,000 context + 800 schemas', r='~5,300'),
            dict(l='per conversation', w='5 turns x 5,300', r='~26K in, 1.5K out'),
            dict(l='mid-tier model', w='26K x &#36;2/M + 1.5K x &#36;10/M', r='&#36;0.067'),
            dict(l='with prefix caching', w='2,300 static tokens at ~10% of input rate', r='&#36;0.045'),
            dict(l='small model instead', w='&#36;0.20 / &#36;1.25 per M', r='&#36;0.007'),
            dict(l='1M conversations a month', w='route ~70% to the small model', r='&#36;45K &rarr; &#36;7K', tot=True),
        ],
        note=('A human ticket costs on the order of &#36;5&ndash;8 fully loaded &mdash; a planning '
              'estimate, not a published figure. Against &#36;0.045 the break-even deflection rate is '
              'so small that cost is not the binding constraint in this design. The cost of a '
              '<i>wrong</i> resolution is. Say that sentence out loud; it reframes the entire '
              'round, and it is the reason the policy engine gets the deep dive rather than the '
              'model choice.')),

    tradeoff_label='The tradeoffs, and the sentence you say',
    tradeoffs=[
        dict(k='AGENT LOOP VS WORKFLOW',
             v='<b>Scripted workflow for the top 20 intents, agent loop for the tail.</b> With an '
               'LLM only at the natural-language boundaries the common path is more reliable, '
               'cheaper and auditable. Over-engineering multi-agent systems where a workflow would '
               'do is on every published list of candidate pitfalls, and this is exactly where it '
               'happens.'),
        dict(k='AUTONOMY VS APPROVAL',
             v='<b>Threshold-based approval, and ask for the threshold.</b> Every irreversible '
               'action &mdash; refund, cancellation, address change on a shipped order &mdash; is '
               'a place where a hallucinated action becomes a real loss. The number is a business '
               'decision, and asking for it is part of the answer rather than a delay to it.'),
        dict(k='MODEL ROUTING',
             v='<b>Route ~70% of traffic to a small model.</b> That one decision is the whole gap '
               'between &#36;45K and &#36;7K a month. Every other cost lever in this design is a rounding '
               'error beside it, so raise it before anyone asks about cost.'),
        dict(k='CONTEXT VS QUALITY',
             v='<b>Compact hard, keep durable state outside the window.</b> The published '
               'observation is that agents perform perfectly for about five steps and then degrade '
               'sharply. The scratchpad and the customer record live outside the context; the '
               'context carries what this turn needs and nothing else.'),
        dict(k='RESOLUTION RATE VS CSAT',
             v='<b>Never optimise the headline number alone.</b> Optimise resolution and you get '
               'an agent that will not escalate. Measure reopen rate and post-escalation CSAT '
               'beside it, or the metric will be gamed by the system you just built &mdash; and '
               'you will not find out for a quarter.'),
        dict(k='KB FRESHNESS VS REVIEW',
             v='<b>Minutes to index, one action to roll back.</b> Policy changes have to reach the '
               'index fast, which rules out a human review gate on every edit &mdash; so a wrong '
               'policy document propagates immediately. Version the knowledge base and make '
               'rollback a single action rather than a re-ingest.'),
    ],

    verdict=dict(
        no='Draws an agent with a list of tools, says &ldquo;we would use LangGraph&rdquo;, never '
           'bounds the loop, never prices a conversation, treats resolution rate as a self-evident '
           'metric, and has nothing for the irreversible-action problem beyond &ldquo;we would '
           'prompt it carefully&rdquo;.',
        yes='Insists on a written definition of resolution before designing anything. Puts '
            'authority in the tool layer and says so in one sentence. Bounds the loop with a step '
            'cap, a per-task dollar cap and repetition detection, with the numbers attached. '
            'Routes ~70% of traffic to a small model and shows the &#36;45K &rarr; &#36;7K arithmetic '
            'unprompted. Names the reopen-rate gaming risk before the interviewer gets there.'),

    real_label='Where the headline number hides',
    real=('Intercom reports that Fin averages a <b>76% resolution rate</b> across its customer '
          'base, under Intercom&rsquo;s own definition, which counts procedure handoffs as '
          'resolved. One FCA-regulated customer, Carmoola, reports <b>60% of inbound and 90% of '
          'outbound</b> conversations resolved end to end, under a definition that customer wrote. '
          'The industry has no standard measure: deflection is frequently counted as resolution, '
          'and abandoned chats often count too. Two vendors quoting the same figure can be '
          'measuring different things, so the first question about any of them is what it counts.'),

    math=dict(
        tex=r'\text{cost} = \underbrace{T \times (s + h + c + f)}_{\text{input tokens}} '
            r'\times p_{\text{in}} + \text{out} \times p_{\text{out}}',
        note='The term to attack is $s + f$ &mdash; system prompt plus tool schemas &mdash; '
             'because it is static, repeated on every one of the $T$ turns, and therefore '
             'cacheable at ~10% of the input rate. Shrinking $c$ costs groundedness and shrinking '
             '$h$ costs coherence, so cache the static part before you cut either.',
        cost='per conversation'),

    drills=[
        dict(q='The agent resolves 70% of tickets. Your VP wants 85%. What do you do?',
             a=('<b>Segment the 30% before you change anything.</b> Expect a large share to be '
                'structurally non-resolvable &mdash; fraud claims, regulated disputes, customers '
                'without the entitlement they are asking about &mdash; and no amount of prompt '
                'work moves those. Then, in order: add the missing <i>tools</i>, because most '
                'unresolved tickets fail on capability rather than comprehension; improve '
                'retrieval on the specific intents where context recall is low; and push back on '
                'the target if reopen rate is climbing, because at that point resolution and '
                'deflection are being conflated and you are being asked to game a metric. Bring '
                'the segmentation to the meeting &mdash; &ldquo;85% of what?&rdquo; is a '
                'legitimate answer when the definition was never written down.'),
             a_simple=('<b>Find out what the failing thirty percent actually are before you touch '
                       'the system.</b> A large slice of them are unresolvable on purpose: fraud '
                       'claims, regulated disputes, customers who are not entitled to what they '
                       'are asking for. Of what is left, most fail because the agent cannot '
                       '<i>do</i> the thing rather than because it misunderstood, so the fix is '
                       'new tools, not better wording. Then improve the search for the topics '
                       'where it keeps missing the right article. And if more customers are coming '
                       'back after a supposedly solved conversation, say so out loud &mdash; that '
                       'is the target eating itself.')),
        dict(q='How do you stop it promising a refund it cannot give?',
             a=('<b>The model never promises &mdash; the tool layer does.</b> The '
                'customer-facing sentence is generated <i>after</i> the tool returns, so the agent '
                'is describing an outcome rather than predicting one. Eligibility is decided by a '
                'deterministic policy engine reading the order, the policy version and the value '
                'threshold, and that engine never sees the conversation, so no phrasing in the '
                'chat can move it. Each tool carries an ACL, a strict output schema and an '
                'idempotency key, and anything above the threshold parks in a human approval '
                'queue. A prompt '
                'telling the model to be careful is not a control, because the channel carrying '
                'your instruction also carries the customer&rsquo;s attempt to override it.'),
             a_simple=('<b>It cannot promise, because it does not decide.</b> The reply the '
                       'customer reads is written after the refund system has answered, not '
                       'before, so the agent is reporting what happened rather than predicting it. '
                       'Whether a refund is allowed is settled by a separate piece of ordinary '
                       'software that reads the order and the policy and never reads the chat, so '
                       'nothing the customer types can talk it round. Anything above the value '
                       'limit waits for a person, and a daily check lists every payment the agent '
                       'started. Telling the model to be careful is not a safeguard: the same '
                       'message box carries the customer trying to undo your instruction.')),
        dict(q='How do you evaluate this?',
             a=('<b>Four layers, and the business one is not optional.</b> Task completion '
                'decomposed into sub-goals, so a partial resolution scores as partial rather than '
                'as failure. Tool-usage efficiency: redundant calls, mis-ordered calls, the same '
                'call twice. Reasoning coherence, which catches the right answer reached by wrong '
                'reasoning &mdash; the one that will not generalise to the next ticket. Then the '
                'business layer: resolution under your written definition, reopen rate, escalation '
                'rate, and CSAT <i>after</i> escalation. Build the golden set from real '
                'escalations rather than imagined cases, calibrate the judge against human labels '
                'to Spearman &ge;0.85 before you trust a single score it produces, and sample 10% '
                'of live conversations continuously alongside 100% of escalations.'),
             a_simple=('<b>Score the work, not just the answer.</b> Break each conversation into '
                       'the steps it should have completed and mark them off, so a half-solved '
                       'case scores as half. Check whether the agent used the right tools in the '
                       'right order or called the same one three times. Check whether a right '
                       'answer came from right reasoning, because a lucky one will not repeat. '
                       'Then measure the business outcome: how many were solved under your written '
                       'definition, how many customers came back within a week, how many needed a '
                       'person, and how those people rated it afterwards. Build the test set out '
                       'of real escalations, and confirm your automatic grader agrees with human '
                       'graders before you believe it.')),
    ],

    anchor=dict(
        formula=('&#36;0.045 per AI conversation &nbsp;&middot;&nbsp; &#36;5&ndash;&#36;8 per '
                 'human ticket &nbsp;&middot;&nbsp; cost is not the constraint'),
        formula_simple=('About four and a half cents a conversation, against five to eight dollars '
                        'for a human ticket. Cost is not what limits this design. The price of a '
                        'confidently wrong answer is.'),
        bullets=[
            'Write down what &ldquo;resolved&rdquo; means before you design against it',
            'Authority lives in the tool layer; a prompt is not a control surface',
            'Bound the loop in numbers: 15 steps, a per-task dollar cap, two identical calls',
        ]),
    chips=['tool-layer authority', 'bounded agent loop', 'intent routing', 'escalation payload',
           'reopen rate'],
    followup='The agent resolves 70% of tickets. Your VP wants 85%. What do you do?',
),
]
