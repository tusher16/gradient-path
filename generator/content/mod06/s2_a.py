CARDS = [

# ============================================================ 1. retrieval
dict(
    id='retrieval-stack',
    tier='core',
    title='The retrieval stack',
    kicker='Hybrid, reranked and permission-aware &mdash; and the permission filter is the box candidates forget to draw',

    simple=[
        'There are two ways to find a document and they fail in opposite places. Matching the '
        'words finds an error code or a ticket number exactly, and misses anyone who asked the '
        'same thing in different words. Matching the meaning handles the paraphrase, and quietly '
        'loses the one token that mattered, because squashing a sentence down to a single point '
        'smears a part number into every other part number. So production systems run both, merge '
        'the two lists, and hand the top hundred to a slower model that reads each candidate '
        'against the actual question and keeps ten. That second pass is where most of the '
        'precision comes from.',

        'The part candidates forget is permissions. You have to cut the search down to what this '
        'person is allowed to see <i>before</i> you pick the top ten, not after. Filter afterwards '
        'and nothing leaks, which is exactly why it survives review &mdash; but a restricted user '
        'gets a short or empty page and concludes the whole system is broken.',
    ],
    analogy=('<b>Like a library with a card catalogue and a librarian.</b> The catalogue finds the '
             'exact call number and nothing else; the librarian understands what you actually '
             'meant and sometimes fetches the wrong edition. You want both. And you want the '
             'reading-room pass checked at the door &mdash; not after ten books are already '
             'stacked on the desk and nine have to be taken away.'),
    trap_simple=('Naming a database and stopping. The database is the least distinctive choice on '
                 'this list. The sharper version is the permissions sentence: <i>we filter the '
                 'results by what the user can see before we show them</i>. That is filtering '
                 'last. Filter first, inside both searches, or the people with the least access '
                 'get a blank page and file a bug about it.'),

    tech=[
        'Two retrievers, one fusion step, one reranker, and an ACL filter that lives inside the '
        'retrievers rather than after them. BM25 carries exact-token matching &mdash; '
        '<code>INC-2024-00847</code>, <code>0x80070005</code>, <code>RTX-4090</code> against '
        '<code>RTX-4070</code> &mdash; where a dense embedding averages the discriminating token '
        'away. Dense carries paraphrase and synonymy. Fusion is a real decision and not a default: '
        'plain reciprocal-rank fusion buys only +1.3% NDCG over a BM25 baseline, while a tiered '
        'scheme (all-term match boosted 100x, any-term 10x, vector fallback 0.1x) bought +7.5% on '
        'the Wands dataset. Convex-combination alpha is domain-specific &mdash; about 0.3 for '
        'technical docs, 0.7-0.8 for conversational, about 0.6 mixed &mdash; and takes only about '
        '40 labelled query-relevance pairs to tune, which is an afternoon of work.',

        'Retrieve wide, rerank narrow: hybrid to top-100, a cross-encoder to top-30-50, top-5-10 '
        'into the prompt. BGE-reranker-v2-m3 costs 50-100 ms on GPU and nothing to self-host; '
        'Cohere Rerank 3.5 is 100-150 ms and about &#36;100 per 100K queries a month. One published '
        'jump: P@10 from 0.62 to 0.84. It is also the first rung you drop under load, so know what '
        'you lose when you drop it.',

        'The largest single win is at index time, not query time. Anthropic&rsquo;s contextual '
        'retrieval prepends a 50-100 token LLM-written situating blurb to each chunk before '
        'embedding: top-20 retrieval failure falls from 5.7% to 3.7% with contextual embeddings, '
        'to 2.9% adding contextual BM25, and to 1.9% adding reranking &mdash; a 67% relative '
        'reduction, at &#36;1.02 per million document tokens. Chunk recursively at 512 tokens with '
        '50-100 overlap: the benchmarks say semantic chunking retrieves better (91.9% recall, '
        'Chroma) and answers worse (54% end-to-end against 69% for recursive 512, FloTorch), '
        'because 43-token fragments give the generator nothing to work with. Production targets '
        'are Recall@10 of 85-91%, MRR above 0.80, Hit Rate@10 above 90%.',

        'Permissions belong in the index. Apply the ACL as a pre-filter inside both retrievers, '
        'and re-check at generation time against live groups, because permissions drift in the '
        'source system after indexing. Post-filtering a top-k that was computed without ACLs leaks '
        'nothing and silently destroys recall for exactly the users who are already most '
        'constrained. That is worse than a leak, because it looks fine.',
    ],
    tech_note=('The failure to name before you are asked is <i>right document, wrong section</i>. '
               'That is a chunk-boundary artefact, not a model problem, and the fixes run cheapest '
               'first: parent-document retrieval (embed the child, return the parent), contextual '
               'chunk headers, larger chunks with more overlap, then a reranker that sees the '
               'query and the full section together. Measure it with context recall at the '
               '<i>section</i> level, not the chunk level, or the metric will keep telling you '
               'everything is fine.'),

    fig=dict(
        kind='blocks', h=286,
        head=['THE QUERY PATH', 'WHERE THE ACL FILTER GOES'],
        boxes=[
            dict(x=24,  y=110, w=88,  h=46, t='query', tone='sig'),
            dict(x=136, y=110, w=120, h=46, t='ACL pre-filter', tone='mem',
                 sub='groups, at query time'),
            dict(x=284, y=56,  w=128, h=44, t='BM25 top-100', sub='error codes, IDs'),
            dict(x=284, y=164, w=128, h=44, t='vector top-100', sub='paraphrase, meaning'),
            dict(x=440, y=110, w=86,  h=46, t='fuse', sub='tiered boost'),
            dict(x=554, y=110, w=118, h=46, t='rerank', tone='mem', sub='top-100 to top-10'),
            dict(x=554, y=214, w=118, h=46, t='post-filter', tone='sig', dash='4 4',
                 sub='recall drops silently'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2, tone='mem'), dict(a=1, b=3, tone='mem'),
            dict(a=2, b=4), dict(a=3, b=4), dict(a=4, b=5),
            dict(a=5, b=6, side='down', tone='sig', dash='4 4',
                 label='skip it and you land here'),
        ],
        labels=[dict(x=34, y=252, t='pre-filter costs recall tuning. post-filter costs the user.',
                     a='start')],
        foot='the filter belongs inside both retrievers, before the top-k is chosen',
        alt='A query path in which the permission filter sits before the BM25 and vector '
            'retrievers, with a dashed alternative showing the same filter applied after '
            'reranking instead'),
    caption=('The ACL box is the only one whose position changes which results exist rather than '
             'what order they come back in. Everything to its right is ranking. Candidates draw '
             'the reranker and forget the filter, and the interviewer is watching for the filter.'),
    caption_simple=('Every box after the permission check only changes the order of the results. '
                    'The permission check is the one that changes which results exist at all '
                    '&mdash; which is why it has to come first.'),

    nums=[
        dict(k='CHUNKS FROM 10M DOCS', v='34M',
             s='15B tokens, recursive 512 with 15% overlap'),
        dict(k='INDEX AT FP32', v='209 GB', s='34M x 1,536 dims x 4 bytes'),
        dict(k='INDEX AT INT8', v='52 GB', s='4x smaller, under 1% recall loss'),
        dict(k='HNSW GRAPH AT M = 16', v='4.4 GB',
             s='34M x 16 x 2 x 4 bytes &mdash; the graph is the cheap half'),
        dict(k='TOTAL RAM, INT8', v='~58 GB',
             s='one large-memory node, two for HA &mdash; say this out loud'),
        dict(k='TOP-20 RETRIEVAL FAILURE', v='5.7% down to 1.9%',
             s='contextual embeddings, then contextual BM25, then reranking'),
    ],
    tradeoffs=[
        dict(k='Hybrid vs dense only',
             v='<b>Hybrid, and argue it with a string, not a benchmark.</b> "A query for '
               'INC-2024-00847 will not be answered by cosine similarity." Plain RRF buys +1.3% '
               'NDCG over BM25; tiered boosting buys +7.5%; alpha needs about 40 labelled pairs. '
               'The second index and the fusion step are the price, and they are cheap.'),
        dict(k='HNSW graph vs the vectors themselves',
             v='<b>Quantise the vectors; the graph is not your problem.</b> At 34M chunks and '
               '1,536 dims the vectors are 209 GB in fp32 and 52 GB at int8 for under 1% recall '
               'loss, while the HNSW graph at M = 16 is 4.4 GB by Qdrant&rsquo;s N x M x 2 x 4 '
               'formula. Binary quantisation reaches 6.5 GB and costs 5-15% recall, which is '
               'almost never the right trade for an internal corpus.'),
        dict(k='Which engine',
             v='Not a scale decision until it is. pgvector is production-ready to about 10M '
               'vectors a node, about 50M with pgvectorscale at p95 under 50 ms; Qdrant '
               'distributed covers 100M-1B; Milvus past 1B. At 34M vectors and 23 QPS peak this '
               'is a data-residency and headcount decision &mdash; say that instead of '
               'benchmarking three vendors at the whiteboard.'),
        dict(k='Pre-filter vs post-filter',
             v='<b>Pre-filter, and take the recall tuning on the chin.</b> Post-filtering is one '
               'line of code, leaks nothing, and hands restricted users an empty result set that '
               'reads as "the system is broken" rather than "you lack access". Re-check ACLs at '
               'generation against live groups, because the snapshot taken at ingest drifts.'),
    ],
    when=[
        'The corpus is full of ticket IDs, error codes or SKUs and someone proposes embeddings alone',
        'Two users ask the same question and must get different documents back',
        'Retrieval recall looks healthy and the answers still cite the wrong section',
        'You are told to cut 200 ms out of retrieval and have to choose which stage dies',
    ],
    trap=('Naming a vector database as if it were the design. The database is the least '
          'differentiated choice in the stack. The sharper trap is the permissions sentence: '
          '"we filter the results by permission before returning them" &mdash; that is '
          'post-filtering a top-k computed without ACLs. It leaks nothing, which is why it passes '
          'review, and it silently drops recall for restricted users until someone files a ticket '
          'saying search is broken for the legal team.'),
    real=('Uber&rsquo;s Enhanced Agentic RAG behind the Genie on-call copilot (2025-05-29) is the '
          'clearest published example of this exact stack: a Google Docs loader that preserves '
          'tables and table of contents structure, tables rewritten to markdown by an LLM, '
          'metadata enrichment with summaries and keywords, then dual retrieval &mdash; vector '
          'plus BM25 over the enriched metadata &mdash; with query-optimizer and post-processor '
          'agents around it. Result: a 27% relative increase in acceptable answers and a 60% '
          'relative reduction in incorrect advice. Anthropic&rsquo;s contextual retrieval reports '
          'the index-time half: top-20 failure from 5.7% to 1.9%.'),
    drills=[
        dict(q='Your retriever returns the right document but the wrong section. What do you do?',
             a=('<b>This is a chunk-boundary problem, not a model problem.</b> Nothing about the '
                'embedding model is failing &mdash; the document ranked first. Fixes in order of '
                'cost: parent-document retrieval, where you embed the child chunk and return the '
                'parent section; contextual chunk headers so each fragment carries where it sits; '
                'larger chunks with 50-100 tokens of overlap; and only then a reranker that sees '
                'the query and the full section together. Then change the metric: measure context '
                'recall at the section level, because chunk-level recall was already telling you '
                'this was fine.'),
             a_simple=('<b>This is a problem with where you cut the documents up, not with the '
                       'search model.</b> The right document came first, so the search worked. '
                       'The cheapest fix is to search on the small piece but hand back the whole '
                       'section around it. After that, put a line at the top of every piece saying '
                       'where it came from, and cut into bigger overlapping pieces. And measure '
                       'success at the section level, because measuring it at the piece level is '
                       'what told you nothing was wrong.')),
        dict(q='Two people run the same query and one of them is in Finance. Where does the permission check go, and what breaks if you put it after retrieval?',
             a=('<b>Inside both retrievers, as a pre-filter, with a re-check at generation.</b> '
                'Post-filtering computes the top-100 over the whole corpus and then removes what '
                'the user cannot see, so a restricted user gets a handful of results or none at '
                'all &mdash; recall collapses for them specifically and nothing in your aggregate '
                'metrics moves, because they are a minority of traffic. It leaks nothing, so it '
                'passes security review. Pre-filtering costs recall tuning and an ACL sidecar '
                'keyed by chunk ID. Re-check at generation against live groups, because '
                'permissions change in the source system after you indexed.'),
             a_simple=('<b>Before the search, inside both searches, and check again at the end.</b> '
                       'If you filter afterwards you searched the whole library first and then '
                       'took away everything they cannot read, so someone with narrow access ends '
                       'up with almost nothing. Your averages will not show it, because those '
                       'users are a small slice of traffic. Nothing leaks, which is why it gets '
                       'approved. And check again just before answering, because access changes '
                       'after you built the index.')),
        dict(q='Dense retrieval already scores 0.88 on our benchmark. Why pay for BM25 as well?',
             a=('<b>Because your benchmark is made of paraphrases and your traffic is not.</b> '
                'Dense retrieval fails on the queries where a single token carries all the '
                'meaning: error codes, SKUs, invoice IDs, fully-qualified function names. '
                'RTX-4090 and RTX-4070 are semantically near-identical and commercially '
                'unrelated. Then be specific about the fusion, because that is the real question: '
                'plain RRF buys only +1.3% NDCG over BM25 alone, while tiered boosting buys +7.5%. '
                'Alpha is domain-specific, about 0.3 for technical docs, and about 40 labelled '
                'pairs are enough to tune it.'),
             a_simple=('<b>Because the test set is written in normal sentences and your users type '
                       'part numbers.</b> Meaning-based search works by squashing a sentence into '
                       'a single point, which throws away exactly the one token that '
                       'distinguishes one product code from the next. Word matching keeps it. '
                       'Also be careful how you merge the two lists: the naive merge adds almost '
                       'nothing, while boosting the results that matched every word adds several '
                       'times more.')),
    ],
    verdict=dict(
        no='Draws documents to embeddings to vector database to LLM, names a vector database brand '
           'as though that were the design, never computes the index size, never mentions '
           'permissions, and treats "we would evaluate it" as a sentence rather than a system.',
        yes='Asks about permissions in the first two minutes and calls it the hardest part; '
            'computes 34M chunks and 209 GB down to 58 GB out loud; picks hybrid with a specific '
            'reason involving ticket IDs; names right-document-wrong-section before being asked; '
            'prices the re-index; and separates retrieval metrics from generation metrics with '
            'numbers attached to each.'),
    anchor=dict(
        formula=r'$\text{ACL pre-filter} \to \text{BM25} \,\|\, \text{vector} \to \text{top-100} \to \text{rerank} \to \text{top-10}$',
        formula_simple='Cut the search down to what this person may see, search twice, merge, then '
                       'let a slower model re-read the shortlist and keep ten.',
        bullets=[
            'Dense retrieval averages away the token that discriminates &mdash; error codes, SKUs, ticket IDs',
            'Retrieve wide and rerank narrow; the cross-encoder is the first rung you drop under load',
            'Pre-filter by ACL inside both retrievers &mdash; post-filtering leaks nothing and destroys recall',
            'The biggest single win is at index time: contextual chunks take top-20 failure from 5.7% to 1.9%',
        ]),
    chips=['BM25', 'cross-encoder reranking', 'contextual retrieval', 'parent-document retrieval',
           'ACL pre-filter', 'reciprocal rank fusion'],
    followup='Your retriever returns the right document but the wrong section. What do you do?',
),

# ============================================================ 2. serving
dict(
    id='serving-stack',
    tier='core',
    title='The serving stack',
    kicker='GPU memory is the binding constraint, and the KV cache is the half of it that moves',

    simple=[
        'A model being served has two kinds of memory sitting on the graphics card, and only one '
        'of them moves. The weights are the model itself: a fixed block, loaded once, which never '
        'gets smaller. Everything left over holds the running notes for each conversation '
        'currently in flight, and those notes grow with every word of context and every extra '
        'user. That leftover space, not the speed of the chip, is what decides how many people '
        'you can serve at the same time.',

        'Which makes the highest-leverage decision a precision one. Store the weights and the '
        'notes at half the size and, on a two-card machine holding a seventy-billion-parameter '
        'model, the number of conversations you can run at once goes from about twenty to about '
        'three hundred and twenty-five. Same hardware, same model, same day. Buying more cards '
        'gets you the same poor ratio at roughly ten times the price, which is exactly why it is '
        'the wrong first answer.',
    ],
    analogy=('<b>Like a removal van with the engine bolted inside the load space.</b> The engine '
             'takes most of the room and never shrinks. What is left is for boxes, and every '
             'customer keeps adding boxes as the journey goes on. How many customers you can '
             'carry has nothing to do with how fast the van drives. It is set by the space the '
             'engine did not take.'),
    trap_simple=('Answering a capacity question with a shopping list. Saying you would use the '
                 'popular serving library behind a load balancer with autoscaling names the tools '
                 'and skips the constraint. The constraint is the space left on the card after '
                 'the weights. And autoscaling cannot rescue you, because a fresh worker takes '
                 'about a minute to come up and most traffic spikes are over before that.'),

    tech=[
        'Two formulas carry the whole design. Forward FLOPs per token is about $2P$; bytes moved '
        'per decode step is the parameter count times the bytes per parameter. An H100 does 989 '
        'TFLOP/s in BF16 against 3.35 TB/s of HBM, a machine balance of about 295 FLOP per byte '
        '&mdash; so decode at batch 1 runs at roughly 0.3% of peak FLOPs. Decode is a '
        'memory-bandwidth job wearing a compute accelerator&rsquo;s clothes. Prefill is the '
        'opposite: a 2,048-token prompt is compute-bound at about 290 ms. Batching is the only '
        'lever that reconciles the two phases, and an H100 needs about 300 concurrent sequences '
        'before decode stops being memory-bound.',

        'The binding constraint is the KV cache. Llama-3.1-70B has 80 layers, 8 KV heads via GQA '
        'and head dim 128, so per token at BF16 it needs $2 \\times 80 \\times 8 \\times 128 '
        '\\times 2 = 327{,}680$ bytes, about 0.327 MB &mdash; 0.164 MB at FP8. Put that on a '
        'two-GPU node. 160 GB total, 140 GB of BF16 weights, about 10 GB of activations and CUDA '
        'context, leaving 10 GB. At 1,500 tokens a request that is 0.49 GB each, so about 20 '
        'concurrent requests. Quantise the weights to FP8 and you free 70 GB: 80 GB of headroom '
        'at 0.25 GB a request, about 325 concurrent. Sixteen times the concurrency on identical '
        'silicon &mdash; and at 10,000 in-flight that is the difference between about 666 H100s '
        'and about 62.',

        'Everything else is scheduling. Continuous batching over paged KV blocks of 16 tokens '
        'gives 3-5x the effective batch size of static batching, which head-of-line blocks: a '
        '50-token request and a 2,000-token request in the same static batch both wait for the '
        'long one. Naive KV pre-allocation wastes 60-80% of reserved cache, which is the entire '
        'reason PagedAttention exists. And you cannot autoscale out of it &mdash; vLLM cold start '
        'is about 62 s and a TensorRT-LLM engine compile is about 28 minutes, both longer than '
        'the spike you are scaling for. Warm standby, predictive scaling, and backfill the idle '
        'capacity with batch jobs.',
    ],
    tech_note=('Size for the right thing and say which. Ten thousand concurrent in-flight requests '
               'at about 325 per FP8 shard is about 31 shards, about 62 H100s. The same product '
               'sized from average throughput &mdash; 1M requests a day at 500 output tokens is '
               'about 5,800 tokens/s, and one H100 running 70B FP8 at concurrency 100 produces '
               '2,400-2,780 &mdash; needs about 3 GPUs. The gap between 62 and 3 is queueing and '
               'burstiness. "I am sizing for concurrency, not throughput, because the SLO is '
               'TTFT" is the sentence that separates the two answers.'),

    fig=dict(
        kind='bars',
        head=['WHAT YOU PAY FOR', 'WHAT YOU CAN SELL'],
        vmax=160, lw=176,
        bars=[
            dict(label='weights, BF16', v=140, tone='sig', note='140 GB'),
            dict(label='framework + activations', v=10, tone='plain', note='10 GB'),
            dict(label='KV cache headroom', v=10, tone='mem', note='10 GB, ~20 reqs'),
            dict(label='weights, FP8', v=70, tone='sig', note='70 GB'),
            dict(label='framework + activations', v=10, tone='plain', note='10 GB'),
            dict(label='KV cache headroom', v=80, tone='mem', note='80 GB, ~325 reqs'),
        ],
        xlab='GB of a 160 GB two-GPU H100 node',
        foot='same node, same model: the only thing that moved is the weight precision',
        alt='Six horizontal bars comparing a 70 billion parameter model at BF16 and at FP8 on a '
            '160 gigabyte two-GPU node. The BF16 weights leave 10 gigabytes of KV cache headroom, '
            'about 20 concurrent requests, while FP8 leaves 80 gigabytes, about 325'),
    caption=('The pink bars are fixed cost and the teal bars are inventory. Halving the weight '
             'precision does not make the model faster &mdash; it moves 70 GB out of the bar you '
             'pay for and into the bar you sell, and concurrency follows the teal bar, never the '
             'clock speed.'),
    caption_simple=('The pink bars are the model itself: paid for, and unusable for anything else. '
                    'The teal bars are the room left over for people. Making the model smaller '
                    'does not make it faster, it makes the teal bar bigger &mdash; and the teal '
                    'bar is the thing you actually sell.'),

    math=dict(
        tex=r'\text{KV bytes} = 2 \cdot L \cdot H_{kv} \cdot D \cdot S \cdot B \cdot b',
        note='The leading 2 is K and V. What it does not say: no real system allocates $S$ at its '
             'maximum, which is exactly why naive pre-allocation wastes 60-80% of reserved cache '
             'and why PagedAttention pages it in 16-token blocks instead.',
        cost='per model, per precision &mdash; memorise this one'),
    estimate=dict(
        label='The arithmetic that decides the fleet', cost='order of magnitude',
        rows=[
            dict(l='the node', w='2 x H100 80GB', r='160 GB'),
            dict(l='weights, BF16', w='70B x 2 bytes', r='140 GB'),
            dict(l='overhead', w='activations, framework, CUDA', r='~10 GB'),
            dict(l='left for KV', w='160 - 140 - 10', r='10 GB'),
            dict(l='per request', w='1,500 tokens x 0.327 MB', r='0.49 GB'),
            dict(l='concurrency, BF16', w='10 / 0.49', r='~20', tot=True),
            dict(l='weights, FP8', w='70B x 1 byte', r='70 GB'),
            dict(l='left for KV', w='160 - 70 - 10', r='80 GB'),
            dict(l='per request', w='1,500 tokens x 0.164 MB', r='0.25 GB'),
            dict(l='concurrency, FP8', w='80 / 0.25', r='~325', tot=True),
        ],
        note='For 10,000 in-flight that is about 666 H100s against about 62. At Lambda&rsquo;s '
             '&#36;2.99 per GPU-hour, roughly &#36;1.43M a month against roughly &#36;133K. Quantisation here '
             'is a ten-fold cost decision, not a speed tweak &mdash; say that sentence.'),
    nums=[
        dict(k='DECODE AT BATCH 1', v='~0.3% of peak FLOPs',
             s='machine balance is about 295 FLOP per byte'),
        dict(k='KV CACHE, 70B AT BF16', v='0.327 MB/token',
             s='0.164 at FP8; 8B is 0.131, 405B is 0.516'),
        dict(k='CONTINUOUS BATCHING', v='3-5x effective batch',
             s='over static, which head-of-line blocks'),
        dict(k='NAIVE PRE-ALLOCATION', v='60-80% wasted',
             s='the whole reason PagedAttention exists'),
        dict(k='H100, 70B FP8, 100 CONCURRENT', v='2,400 tok/s',
             s='vLLM 0.18; TTFT p95 1,450 ms at that concurrency'),
        dict(k='COLD START', v='~62 s for vLLM',
             s='~28 min to compile a TensorRT-LLM engine &mdash; never in the serving path'),
    ],
    tradeoffs=[
        dict(k='Continuous vs static batching',
             v='<b>Continuous, and be able to say why.</b> Static batching head-of-line blocks: a '
               '50-token request and a 2,000-token request in the same batch both wait for the '
               'long one. Continuous batching over paged KV gives 3-5x the effective batch size. '
               'This is the default in 2026 and naming it is table stakes, not insight.'),
        dict(k='Where to sit on the batching knee',
             v='An H100 needs about 300 concurrent sequences before decode stops being '
               'memory-bound. Past the knee aggregate throughput keeps rising and per-user '
               'latency degrades. Production sits deliberately near it; exactly where is an SLO '
               'decision you should make out loud rather than inherit from a config default.'),
        dict(k='FP8 vs BF16',
             v='<b>FP8, gated on the eval set.</b> It roughly doubles concurrency per GB and is a '
               'ten-fold cost decision in this design. It is not free: quantisation is a model '
               'change and goes through the same gates as a model change, and A100s lack FP8 '
               'hardware acceleration, so you get the memory saving without the throughput one.'),
        dict(k='Disaggregating prefill and decode',
             v='Worth it for MoE models, 100K-plus contexts and high concurrency &mdash; 7x '
               'reported on GB200 NVL72, +61% requests/s and 50% lower TTFT at Baseten, 3-5x for '
               'SGLang HiSparse. Not worth it for a dense 70B at moderate batch, where the KV '
               'transfer between pools can cost more than the split saves.'),
        dict(k='Reactive vs predictive autoscaling',
             v='<b>Predictive, plus warm standby.</b> A vLLM cold start is about 62 s, which '
               'exceeds the duration of most traffic spikes, so a reactive policy finishes '
               'scaling after the spike has passed. Pay for the standby capacity by backfilling '
               'it with non-interactive batch work.'),
    ],
    when=[
        'Someone answers a concurrency problem by asking for more GPUs',
        'p95 time to first token is 1.4 seconds and nobody can say whether it is compute or queueing',
        'Finance asks why serving one 70B model costs &#36;1.4M a month',
        'A team wants a fine-tuned variant and therefore a fleet of their own',
    ],
    trap=('"We would use vLLM behind a load balancer with autoscaling." The published seniority '
          'ladder is explicit about that exact sentence: an SDE II names vLLM and draws load '
          'balancers, an SDE III identifies KV cache memory as the binding constraint and '
          'proactively scopes quantisation and speculative decoding. A second trap hides inside '
          'the first &mdash; sizing the fleet from average throughput, which gives about 3 GPUs, '
          'when the SLO is time to first token and peak concurrency gives about 62, and never '
          'noticing that the two numbers disagree twenty-fold.'),
    real=('The 2026 evidence that software, not silicon, is the lever. MLPerf Inference v6.0 '
          '(April 2026) recorded a 2.7x gain from software alone on identical 288-GPU hardware. '
          'Splitting prefill and decode onto separate hardware, Baseten reported +61% requests/s, '
          '+62% tokens/s and 50% lower TTFT on Qwen3 Coder 480B at roughly 50K-token prompts, and '
          'NVIDIA Dynamo 1.0 with TensorRT-LLM reported 7x on GB200 NVL72 for DeepSeek R1-0528 at '
          'FP4. Not one of those was a hardware purchase.'),
    drills=[
        dict(q='You have a fixed GPU budget. Do you serve one big model or three small ones?',
             a=('<b>Three small ones behind a router, unless the quality floor is the product.</b> '
                'The deciding fact is whether traffic is homogeneous. When 70% or more of it is '
                'easy lookups, small models amortise their weights across far more concurrent '
                'requests per GB and the router pays for itself immediately; when every request '
                'needs frontier reasoning, the split just multiplies your weights. Quantify rather '
                'than assert: dropping 70B from BF16 to FP8 frees 70 GB of a 160 GB two-GPU node, '
                'which at 1,500 tokens a request is the difference between about 20 and about 325 '
                'concurrent. That ratio is the argument, not the parameter count.'),
             a_simple=('<b>Three small ones behind a router, unless every request genuinely needs '
                       'the best model.</b> The question is really about your traffic. If most '
                       'requests are easy lookups, small models take up far less of the card and '
                       'you fit far more people on at once. If every request needs the strongest '
                       'reasoning, splitting just means you are storing several models instead of '
                       'one. Settle it with the memory arithmetic, not with a preference &mdash; '
                       'halving the size of the model already takes you from about twenty '
                       'conversations at once to about three hundred.')),
        dict(q='Time to first token is 68 ms at concurrency 1 and 1,450 ms at concurrency 100. Where did the time go?',
             a=('<b>Queueing, not compute.</b> The prefill work per request has not changed; what '
                'changed is how long a request waits before it is admitted to a batch. Attack it '
                'in that order: chunked prefill so one long prompt cannot block the batch; '
                'prefix-aware consistent hashing so requests sharing a system prompt land on the '
                'same scheduler and reuse its cache; admission control to bound queue depth rather '
                'than let it grow. If long contexts dominate, disaggregate prefill and decode '
                '&mdash; Baseten reported 50% lower TTFT on 50K-token prompts. Adding GPUs '
                'shortens the queue too, at ten times the price.'),
             a_simple=('<b>It is waiting, not working.</b> Each request takes the same amount of '
                       'work as before; what grew is the time it spends in the queue before it '
                       'gets picked up. So fix the queue. Break long prompts into pieces so one '
                       'giant request cannot hold up everyone behind it. Send requests that share '
                       'the same opening instructions to the same machine so it can reuse what it '
                       'already computed. Cap how long the queue is allowed to get, and reject '
                       'past that rather than letting everyone wait.')),
        dict(q='Your fleet is 666 H100s. Cut the bill without buying or removing hardware.',
             a=('<b>Quantise to FP8 and re-size the fleet, gated on the eval set.</b> 666 H100s at '
                'Lambda&rsquo;s &#36;2.99 per GPU-hour is about &#36;1,990 an hour, roughly &#36;1.43M a '
                'month. At about 325 concurrent per FP8 shard the same 10,000 in-flight requests '
                'need about 31 shards, about 62 GPUs, about &#36;185 an hour or &#36;133K a month. Then '
                'guard the decision: quantisation is a model change and goes through the same '
                'eval gates as one, and if any of that fleet is A100s they lack FP8 hardware '
                'acceleration, so you get the memory saving without the throughput saving.'),
             a_simple=('<b>Store the model at half the size, then shrink the fleet to match.</b> '
                       'The cards are mostly full of the model itself. Halve how precisely you '
                       'store it and you free up most of each card for actual conversations, so '
                       'the same traffic fits on roughly a tenth of the machines &mdash; about a '
                       'hundred and thirty thousand a month instead of about one and a half '
                       'million. It is not free: storing the model less precisely can change its '
                       'answers, so it has to pass the same quality checks as a new model would.')),
    ],
    verdict=dict(
        no='"We would use vLLM behind a load balancer with autoscaling." Never computes the '
           'weights or the KV cache, sizes the fleet from average throughput without noticing, '
           'and treats quantisation as a footnote at the end rather than the decision the prompt '
           'is about.',
        yes='Identifies KV cache memory as the binding constraint inside the first three minutes; '
            'computes 140 GB, 0.327 MB per token, and about 20 against about 325 concurrent; '
            'produces both the 666-GPU and the 62-GPU number and explains the gap; notes that '
            'reactive autoscaling cannot work against a 62-second cold start; and names the '
            'throughput-versus-concurrency sizing trap before being pushed into it.'),
    anchor=dict(
        formula=r'$\text{KV bytes} = 2 \cdot L \cdot H_{kv} \cdot D \cdot S \cdot B \cdot b$ &nbsp;&middot;&nbsp; $160-140-10 = 10$ GB &nbsp;&middot;&nbsp; $160-70-10 = 80$ GB',
        formula_simple='What is left on the card after the weights, divided by what one '
                       'conversation costs, is how many people you can serve at once.',
        bullets=[
            'Weights are fixed; the KV cache is what scales with concurrency and context, and it is the constraint',
            'Prefill is compute-bound, decode is memory-bound &mdash; batching is the only lever that joins them',
            'FP8 on a 160 GB node moves concurrency from about 20 to about 325, and the fleet from ~666 to ~62 H100s',
            'Reactive autoscaling loses to a 62-second cold start; warm standby backfilled with batch work wins',
        ]),
    chips=['PagedAttention', 'continuous batching', 'FP8 quantisation', 'chunked prefill',
           'prefix-aware routing', 'speculative decoding'],
    followup='You have a fixed GPU budget. Do you serve one big model or three small ones?',
),

# ============================================================ 3. caching
dict(
    id='caching-layers',
    tier='core',
    title='Four caches, four staleness bugs',
    kicker='Exact match, semantic, KV and prefix, retrieval results &mdash; and only one of them can be wrong in a way your dashboards will not show you',

    simple=[
        'Four different things get cached on the path of one request, and people say the word as '
        'if it were one thing. First, the exact-match cache: same request string, same answer '
        'back, nearly free. Second, the answer cache that matches on meaning rather than exact '
        'wording &mdash; if somebody asked something close enough, hand back the old answer. This '
        'is the dangerous one. Third, inside the chip, the model&rsquo;s working notes for the '
        'answer it is writing right now, plus the shared opening of every prompt: the standing '
        'instructions and the passages you just retrieved, kept so you do not pay to read them '
        'twice. Providers charge about a tenth of the normal rate for that one. Fourth, the '
        'intermediate work: which passages came back for a question, and how they were scored.',

        'Each goes stale about a different thing. The first holds an old answer for an edited '
        'document, the second holds an answer that may never have been right, the third holds an '
        'old block of context, the fourth holds an old ranking. If you cannot say which one '
        'served the bad answer, you cannot fix it.',
    ],
    analogy=('<b>Like a restaurant that keeps four things ready.</b> The chef&rsquo;s notes for the '
             'dish being cooked right now. The stock prepared this morning that every dish starts '
             'from. A plate of yesterday&rsquo;s special handed to anyone who orders something '
             'similar. And a note of which supplier delivered what. Only the third one can make '
             'someone ill, and it is the one nobody checks.'),
    trap_simple=('Proposing the meaning-matching cache with a hit rate copied off a marketing page '
                 'and no story for what happens when the document changes. The figure everyone '
                 'quotes is how often a match is correct, not how often there is a match at all '
                 '&mdash; in production between one and two requests in five hit, not nineteen in '
                 'twenty. And the very next question is what happens when the underlying document '
                 'is edited.'),

    tech=[
        'Four caches, four contracts. <b>Exact match</b> keys on the literal request and is nearly '
        'free. <b>Semantic</b> embeds the query and returns a previous answer when cosine '
        'similarity clears a threshold &mdash; the one that trades correctness for money. '
        '<b>KV and prefix</b> are two mechanisms in one family: the KV cache is per-request, '
        'inside the GPU, correctness-neutral pure speed, while the prefix cache reuses a shared '
        'system prompt and retrieved context block across requests, at about 10% of the input rate '
        'for cached reads and 1.25x to 2x for cache writes. <b>Retrieval results</b> &mdash; the '
        'top-k, the fusion output, the reranker scores, the embeddings themselves &mdash; are the '
        'cheapest large win nobody proposes.',

        'The numbers that kill the marketing. Real semantic-cache hit rates are 20-45%, not 95%: '
        'Portkey measured about 20% on a production RAG workload, an EdTech student Q&amp;A '
        'workload about 45%, open-ended chat 10-20%. The 95% figure refers to match <i>accuracy</i>, '
        'not hit rate. On a &#36;5,000 a month bill a 20% hit rate saves &#36;1,000, and hits return in '
        'under 5 ms against 2-5 s for a live call &mdash; a real latency win and a modest cost '
        'one. The threshold is a product decision, not a tuning parameter: 0.85 is aggressive and '
        'acceptable for FAQ-style Q&amp;A, 0.92 is the production sweet spot, and 0.98 is '
        'conservative enough that it barely beats exact-match caching.',

        'Poisoning is the failure nobody names. Cache a hallucinated or incorrect response and '
        'every similar future query gets that same bad answer &mdash; a persistent, repeatable bug '
        'that A/B testing will not surface, because it looks deterministic. Gate cache writes '
        'behind a quality check. Then key by principal: a semantic cache keyed only on query text '
        'will serve one tenant&rsquo;s answer to another, so the key needs tenant, role and an ACL '
        'hash, plus index version and prompt version. Set TTL against the freshness of the '
        'underlying corpus rather than a round number &mdash; one published worked example runs a '
        '1-hour TTL on a support bot targeting a 20-30% hit rate &mdash; but TTL is the bound, not '
        'the fix. Invalidate by document ID on ingest.',
    ],
    tech_note=('Order of operations, because this is a ranked list and not a menu. Prefix caching '
               'first: Anthropic reports it reducing latency by more than 2x and cost by up to '
               '90%, and it is correctness-neutral, so there is no argument against it. '
               'Retrieval-result caching second. Exact match third. The semantic cache last, and '
               'only with an invalidation path and a quality gate on writes &mdash; it is the only '
               'one of the four that can hand a user an answer that was never true of anything.'),

    fig=dict(
        kind='blocks', h=232,
        head=['THE REQUEST PATH', 'WHAT EACH ONE GOES STALE ABOUT'],
        boxes=[
            dict(x=24,  y=56, w=88,  h=46, t='request', tone='sig'),
            dict(x=134, y=56, w=124, h=46, t='exact match', sub='key: the exact string'),
            dict(x=280, y=56, w=124, h=46, t='semantic', tone='sig', sub='key: the embedding'),
            dict(x=426, y=56, w=124, h=46, t='retrieval cache', sub='top-k and scores'),
            dict(x=572, y=56, w=124, h=46, t='KV and prefix', tone='mem', sub='inside the model'),
            dict(x=134, y=150, w=124, h=50, t='corpus edit', dash='4 4',
                 sub='old answer, same key'),
            dict(x=280, y=150, w=124, h=50, t='poisoning', tone='sig', dash='4 4',
                 sub='one bad answer, forever'),
            dict(x=426, y=150, w=124, h=50, t='index version', dash='4 4',
                 sub='new chunks, old top-k'),
            dict(x=572, y=150, w=124, h=50, t='stale context', dash='4 4',
                 sub='old copy, edited doc'),
        ],
        links=[
            dict(a=0, b=1), dict(a=1, b=2), dict(a=2, b=3), dict(a=3, b=4),
            dict(a=1, b=5, side='down', dash='3 3'),
            dict(a=2, b=6, side='down', dash='3 3', tone='sig'),
            dict(a=3, b=7, side='down', dash='3 3'),
            dict(a=4, b=8, side='down', dash='3 3'),
        ],
        foot='only the pink one can be wrong in a way your dashboards will not show you',
        alt='Four caches drawn on one request path, exact match, semantic, retrieval result and '
            'KV or prefix, each with the specific thing it goes stale about underneath it'),
    caption=('Four caches, four keys, four staleness bugs. Only the semantic cache can be wrong '
             'about the answer itself, and it is the only one whose failure survives a redeploy '
             '&mdash; the entry is still there, still matching, still returning the thing that was '
             'never true.'),
    caption_simple=('Each of the four goes stale about something different: an edited document, a '
                    'wrong answer, an out-of-date index, or an old block of context. Only one of '
                    'them can hand back something that was never true, and it is the one people '
                    'add first.'),

    nums=[
        dict(k='SEMANTIC CACHE, REAL HIT RATE', v='20-45%',
             s='production RAG about 20%, EdTech Q&amp;A about 45%, open chat 10-20%'),
        dict(k='THE 95% FIGURE', v='match accuracy',
             s='not hit rate &mdash; it is marketing, not a budget input'),
        dict(k='CACHED INPUT READS', v='~10% of the input rate',
             s='cache writes cost 1.25x to 2x'),
        dict(k='CACHE HIT LATENCY', v='under 5 ms', s='against 2-5 s for a live call'),
        dict(k='PROMPT CACHING, ANTHROPIC', v='2x latency, up to 90% cost',
             s='correctness-neutral, which is why it goes first'),
        dict(k='SAVING AT A 20% HIT RATE', v='&#36;1,000 a month',
             s='on a &#36;5,000 bill &mdash; real, and not what you were sold'),
    ],
    tradeoffs=[
        dict(k='Prefix cache vs semantic cache',
             v='<b>Prefix cache first, every time.</b> It is correctness-neutral &mdash; Anthropic '
               'reports more than 2x lower latency and up to 90% lower cost &mdash; while the '
               'semantic cache trades correctness for money at a real hit rate of 20-45%. Take '
               'the free win before you take the risky one, and say that you are doing so.'),
        dict(k='Threshold 0.85 vs 0.92 vs 0.98',
             v='0.85 is aggressive and fine for FAQ-style Q&amp;A; 0.92 is the production sweet '
               'spot; 0.98 is conservative and barely beats exact-match caching, so it buys risk '
               'without buying hits. This is a product decision about how wrong an answer is '
               'allowed to be, not a number you tune until the dashboard looks good.'),
        dict(k='TTL vs event invalidation',
             v='<b>Both, but the event is the fix.</b> TTL bounds your worst case; invalidation by '
               'document ID on ingest is what actually repairs it. A 1-hour TTL on a support bot '
               'targeting a 20-30% hit rate is a published starting point, not a design, and it '
               'still means an hour of confidently serving last week&rsquo;s policy.'),
        dict(k='Cache everything vs gate the writes',
             v='<b>Gate writes on a quality check.</b> A hallucination written into a semantic '
               'cache becomes a persistent, repeatable bug that looks deterministic, so an A/B '
               'test will not surface it &mdash; the same wrong answer comes back for every '
               'similar query until a human reads one and complains.'),
        dict(k='Key on the query vs key on the principal',
             v='Query text alone serves one tenant&rsquo;s answer to another and it registers as '
               'a cache hit, not as a leak. Tenant, role and an ACL hash belong in the key, and '
               'so do index version and prompt version &mdash; without those, a re-index '
               'invalidates nothing and a prompt rollout silently skips every cached request.'),
    ],
    when=[
        'Cost per request is the problem and someone proposes a semantic cache to halve it',
        'A user reports the assistant quoting a policy that changed last week',
        'Two tenants share a deployment and the cache key is the query text',
        'You have five minutes to say which cache you would add first, and why that one',
    ],
    trap=('"We&rsquo;ll add a semantic cache, they get about a 95% hit rate." Two errors in one '
          'sentence. 95% is match accuracy rather than hit rate &mdash; production hit rates are '
          '20-45%, so the saving is a fifth of what was just promised &mdash; and there is no '
          'invalidation path anywhere in the sentence. The interviewer&rsquo;s next line is "the '
          'underlying document changed, now what?", and there is no good improvised answer. The '
          'structural one is invalidation by document ID on ingest, not TTL alone.'),
    real=('Anthropic reports prompt caching reducing latency by more than 2x and cost by up to 90% '
          '(contextual retrieval, 2024-09-19) &mdash; the cheapest correctness-neutral win '
          'available, and the one to reach for before semantic caching. Against that, '
          'Portkey&rsquo;s production RAG workload measured a real semantic-cache hit rate of '
          'about 20%, an EdTech student Q&amp;A workload about 45%, and open-ended chat 10-20%. On '
          'a &#36;5,000 a month bill the 20% case saves &#36;1,000. The free cache is worth an order of '
          'magnitude more than the risky one, and it is the one candidates skip.'),
    drills=[
        dict(q='A user says the assistant gave them yesterday&rsquo;s policy. Walk me through the debug.',
             a=('<b>Four candidates, and one trace separates them.</b> A semantic cache hit on a '
                'stale entry; a prefix cache holding a stale retrieved context block; the vector '
                'index not yet re-indexed after the document changed; or the document itself '
                'still stale in the source system. The trace needs cache-hit status, chunk IDs '
                'and chunk ingestion timestamps &mdash; the hit flags separate the first two, the '
                'ingestion timestamps separate the last two. Then name the structural fix rather '
                'than the patch: invalidate cache entries by document ID on ingest, so an edit '
                'takes its entries with it instead of waiting out a TTL.'),
             a_simple=('<b>There are four places it could have come from, and one recording tells '
                       'you which.</b> The answer cache held an old reply; the prompt cache held '
                       'an old copy of the passage; the search index had not been rebuilt since '
                       'the document changed; or the document in the source system is itself out '
                       'of date. Record, for every request, whether it was served from a cache, '
                       'which passages were used, and when each of those was last ingested. Then '
                       'fix it properly: when a document is updated, delete the cached answers '
                       'that used it, rather than waiting for them to expire.')),
        dict(q='Finance wants a higher hit rate. Do you drop the similarity threshold from 0.92 to 0.85?',
             a=('<b>Not to chase a hit rate.</b> 0.85 is aggressive but defensible for FAQ-style '
                'Q&amp;A, 0.92 is the production sweet spot and 0.98 barely beats exact match, so '
                'the band being argued over is narrow. It is also the wrong lever: real hit rates '
                'land at 20-45% whatever you set, so on a &#36;5,000 bill you are negotiating a few '
                'hundred dollars while every near-miss becomes a wrong answer that persists. Take '
                'the correctness-neutral saving instead &mdash; prefix caching at more than 2x '
                'lower latency and up to 90% lower cost &mdash; and spend the threshold budget on '
                'a quality gate for cache writes.'),
             a_simple=('<b>Not to chase a hit rate.</b> The looser setting is defensible for '
                       'simple repeated questions and indefensible for anything where a near-miss '
                       'is a wrong answer. But it is the wrong thing to argue about: the share of '
                       'requests that hit lands between a fifth and a half whatever you set, so '
                       'on a five thousand a month bill you are haggling over a few hundred while '
                       'making wrong answers more likely. Take the free saving instead &mdash; '
                       'reusing the shared opening of every prompt cuts cost by up to ninety '
                       'percent and cannot change an answer.')),
        dict(q='What is in your semantic cache key?',
             a=('<b>Not just the query embedding.</b> Tenant, role and an ACL hash, or you serve '
                'one tenant&rsquo;s answer to another and it registers as a cache hit rather than '
                'a leak. Index version, or a re-index invalidates nothing and the cache keeps '
                'serving pre-index answers indefinitely. Prompt version, or a prompt rollout '
                'silently skips every cached request and your A/B test measures a blend of two '
                'systems. Then gate writes on a quality check, so a hallucination never becomes '
                'an entry in the first place &mdash; that is the difference between a cache and a '
                'permanent bug.'),
             a_simple=('<b>Not just the question.</b> Who is asking, and what they are allowed to '
                       'see, or one customer gets another customer&rsquo;s answer and it looks '
                       'like a normal cache hit rather than a leak. Which version of the search '
                       'index it came from, or rebuilding the index changes nothing. Which '
                       'version of the instructions produced it, or a change to those '
                       'instructions quietly skips everyone served from the cache. And check the '
                       'answer is good before you store it, because a bad one stored is a bad one '
                       'forever.')),
    ],
    anchor=dict(
        formula=r'$\text{saving} = \text{hit rate} \times \text{cost per call}$ &nbsp;&middot;&nbsp; hit rate is $0.20$ to $0.45$, never $0.95$',
        formula_simple='What you save is the share of requests that hit, times what a request '
                       'costs. In production that share is between a fifth and a half, not '
                       'nineteen in twenty.',
        bullets=[
            'Prefix caching is correctness-neutral and nearly free &mdash; take it before the semantic cache',
            'Real semantic hit rates are 20-45%; the 95% number is match accuracy, not hit rate',
            'A cached hallucination is a permanent bug an A/B test cannot see &mdash; gate cache writes',
            'Key by tenant, role and ACL hash; invalidate by document ID on ingest, not by TTL alone',
        ]),
    chips=['prompt caching', 'PagedAttention', 'cache invalidation', 'similarity threshold',
           'multi-tenant cache keys', 'cache poisoning'],
    followup='A user says the assistant gave them yesterday&rsquo;s policy. Walk me through the debug.',
),

# ============================================================ 4. eval harness
dict(
    id='eval-harness',
    tier='core',
    title='The eval harness',
    kicker='Three tiers, or you are shipping blind &mdash; and the tier everyone builds is the one that measures the wrong half',

    simple=[
        'Three levels of checking, and each catches a bug the others cannot see. The cheapest is a '
        'set of flat assertions written per case: this phrase must appear, this one must never '
        'appear. They cost nothing, finish in seconds, and catch the disasters. Above that you '
        'measure the two halves separately &mdash; did the search step find the passages that '
        'contain the answer, and did the writing step stay inside what it was handed. Those are '
        'different failures with different fixes, and a system can score beautifully on one while '
        'failing the other. Third, you run whole cases end to end against a curated set of real '
        'past failures, and you sample live traffic, because the failures nobody thought to write '
        'down only ever appear there.',

        'The trap is building the first half of the middle level and calling it evaluation. '
        'Whether the search worked is the easiest thing to measure and the number least connected '
        'to whether the user got a correct answer. A system that answers faithfully from the '
        'wrong part of the right document scores well on it and is wrong every single time.',
    ],
    analogy=('<b>Like checking a translation.</b> First you check the names and the numbers came '
             'across &mdash; free, mechanical, catches the disasters. Then you check the two '
             'halves separately: did the translator open the right source paragraph, and did they '
             'stay faithful to it. Only then do you hand the whole thing to a fluent reader and '
             'ask whether it says what the original said.'),
    trap_simple=('Naming a tool. Saying you would use an evaluation library and track one score is '
                 'a purchase, not a plan. The plan is three things with numbers on them: where '
                 'the test cases came from, how closely the automatic grader agrees with people, '
                 'and what score blocks a change from shipping. The sharper trap is grading only '
                 'the search step &mdash; a system that finds the right document nine times in '
                 'ten and then answers from the wrong part of it passes that test every time.'),

    tech=[
        'Three tiers, because each catches a different class of failure. Offline evaluation '
        'against a versioned golden dataset catches systematic design problems. CI gates on every '
        'PR catch change-specific regressions. Online monitoring with sampling catches '
        'distribution shift &mdash; the failures nobody thought to write a case for. Underneath '
        'all three sit deterministic assertions: <code>must_include</code> and '
        '<code>must_not_include</code> string checks are free, instant, and catch the worst '
        'regressions before a judge is invoked at all.',

        'Six RAG metrics split across two layers, and the split <i>is</i> the design. Retrieval: '
        'context recall (did we get everything needed) and context precision (is what we got '
        'relevant). Generation: faithfulness (are the claims supported by the retrieved context), '
        'answer relevancy, hallucination, groundedness. They are not interchangeable &mdash; a '
        'system can score high on faithfulness while failing on context recall, and the reverse. '
        'Recall@10 of 0.91 with faithfulness of 0.60 is a real and common system: it retrieves '
        'correctly and then answers confidently from the wrong part. Report the two layers '
        'separately, always.',

        'Calibrate the judge or it is decoration. Minimum 50 human-annotated examples, ideally 100 '
        'or more, spanning the quality spectrum &mdash; a published recipe uses 10 excellent, 10 '
        'poor, 30 ambiguous &mdash; scored by Spearman correlation against the human labels. 0.70 '
        'is acceptable for low-stakes, 0.85 is production-ready. Run 3 independent scoring passes '
        'with chain-of-thought and explicit rubric anchors, average them, and flag high variance '
        'for human review. An uncalibrated judge shows position bias, verbosity preference, and a '
        'systematic preference for outputs that look like its own.',

        'The gate thresholds you should be able to quote without notes: regression tolerance 5%; '
        'faithfulness 0.85 general and 0.95 high-stakes; context recall 0.80 and 0.90; context '
        'precision 0.75; answer relevancy 0.80; groundedness 0.80. Any prompt change triggers a '
        'full run. Online, sample 5-10% of production traffic, alert when the rolling faithfulness '
        'average drops below 0.75, and page at threshold times 0.85. Harvest the golden set from '
        'production failures &mdash; explicit negative feedback, automated scores under threshold, '
        'p99 latency outliers &mdash; and tag each case with a failure mode so you can report '
        'regressions by category instead of by one average that hides them.',
    ],
    tech_note=('Agents change the metrics, not the tiers. Output matching does not work when there '
               'is no single right answer, so you decompose the task into sub-goals and verify '
               'each; score tool-usage efficiency, meaning redundant, missing or mis-ordered '
               'calls; and check reasoning coherence separately from correctness, because an agent '
               'that reaches the right answer by the wrong route will fail on the next input and '
               'your output-matching metric will not have seen it coming.'),

    fig=dict(
        kind='tree', h=296, nw=196,
        head=['THE THREE TIERS', 'WHAT EACH ONE CATCHES'],
        nodes=[
            dict(id='r',  x=360, y=40,  w=212, t='a prompt change lands', tone='sig'),
            dict(id='t1', x=124, y=140, t='tier 1: assertions', sub='free, runs in seconds'),
            dict(id='t2', x=360, y=140, t='tier 2: component evals',
                 sub='retrieval and generation, split'),
            dict(id='t3', x=596, y=140, t='tier 3: end to end',
                 sub='golden set, then live traffic'),
            dict(id='c1', x=124, y=234, t='the disaster', tone='mem',
                 sub='a banned phrase came back'),
            dict(id='c2', x=360, y=234, t='which half broke', tone='mem',
                 sub='recall 0.91, faithfulness 0.60'),
            dict(id='c3', x=596, y=234, t='what you never wrote', tone='mem',
                 sub='drift, and the missing case'),
        ],
        edges=[
            dict(a='r', b='t1', label='free', dx=-34),
            dict(a='r', b='t2', label='12 USD a run', dx=46),
            dict(a='r', b='t3', label='1,800 USD a month', dx=76),
            dict(a='t1', b='c1', label='in seconds', dx=42),
            dict(a='t2', b='c2', label='in ~4.5 minutes', tone='sig', dx=50),
            dict(a='t3', b='c3', label='continuously', dx=44),
        ],
        foot='the middle tier splits in two, and measuring only its left half is the classic failure',
        alt='A three-tier evaluation tree. One prompt change fans out to assertions, component '
            'evaluations and end to end plus online sampling, with the cost and wall clock of '
            'each and the specific failure each one catches'),
    caption=('Each tier is a different order of magnitude in cost and a different class of bug. '
             'The middle column is where the trap lives: split it into retrieval and generation, '
             'or a recall of 0.91 will keep telling you the system is healthy while faithfulness '
             'sits at 0.60.'),
    caption_simple=('Each level costs more and catches something the level below cannot. The '
                    'middle one has to be split in two &mdash; did it find the right passages, '
                    'and did it stay inside them &mdash; because a system can pass one half and '
                    'fail the other every time.'),

    nums=[
        dict(k='JUDGE CALIBRATION', v='Spearman 0.85',
             s='production-ready; 0.70 is the low-stakes floor'),
        dict(k='HUMAN LABELS NEEDED', v='50 minimum, 100+ better',
             s='10 excellent, 10 poor, 30 ambiguous &mdash; about 5 hours of expert time'),
        dict(k='FAITHFULNESS GATE', v='0.85', s='0.95 where a wrong answer is expensive'),
        dict(k='CONTEXT RECALL GATE', v='0.80',
             s='0.90 high-stakes &mdash; and it is a separate number, not the same one'),
        dict(k='REGRESSION TOLERANCE', v='5%',
             s='blocking on absolute thresholds, advisory on everything else'),
        dict(k='ONLINE SAMPLING', v='5-10% of traffic',
             s='alert at rolling faithfulness 0.75, page at threshold times 0.85'),
    ],
    estimate=dict(
        label='What gating every PR actually costs', cost='derived',
        rows=[
            dict(l='golden set', w='1,000 cases x 6 metrics', r='6,000 scores'),
            dict(l='judge passes', w='x 3 independent passes', r='18,000 calls'),
            dict(l='tokens', w='~1,500 in, ~300 out each', r='27M in, 5.4M out'),
            dict(l='one full run', w='small model at &#36;0.20 / &#36;1.25 per M', r='~&#36;12', tot=True),
            dict(l='50 PRs a week', w='50 x &#36;12', r='~&#36;600 a week', tot=True),
            dict(l='wall clock', w='18,000 calls, 100-way concurrency', r='~4.5 min'),
        ],
        note='"We cannot afford to gate every PR" is not a real objection at &#36;12 a run, and '
             'neither is "it would slow the team down" at four and a half minutes. The real cost '
             'is the 100 human labels &mdash; about five hours of expert time, once per judge '
             'version &mdash; and the reason teams skip that is not the money.'),
    when=[
        'A team ships prompt changes weekly and nothing blocks a bad one',
        'Retrieval recall is 0.91 and users say the answers are wrong',
        'A base model swap is proposed and nobody has re-baselined the judge',
        'Somebody proposes an LLM judge and nobody asks how it was calibrated',
    ],
    trap=('"We&rsquo;d use RAGAS and track faithfulness." Naming a framework is not an eval '
          'strategy; the strategy is the golden set, the judge calibration number and the gate '
          'threshold. The sharper trap is the one the research names outright: an evaluation that '
          'only measures the retriever. Recall@10 of 0.91 with faithfulness of 0.60 is a system '
          'that confidently answers from correct documents, and every retrieval metric you own '
          'will say it is healthy.'),
    real=('Uber&rsquo;s Enhanced Agentic RAG used an LLM-as-judge framework scoring 0-5 with '
          'written reasoning, which cut evaluation cycles from weeks to minutes and is what made '
          'the +27% acceptable answers and 60% reduction in incorrect advice reachable at all '
          '&mdash; the harness was the enabling component, not the reporting layer. DoorDash '
          '(2026-04-14) built an LLM-as-a-judge harness to construct golden datasets without a '
          'manual annotation bottleneck, measured with Hit@K and nDCG@K, and moved offline P@10 '
          'from 68% to 85%, with a 3.65% lower search null rate and a 2.4% higher homepage order '
          'rate.'),
    drills=[
        dict(q='Your offline eval is green and users are complaining. What happened?',
             a=('<b>Three candidates, and you can tell them apart with one slice.</b> The golden '
                'set no longer reflects the traffic distribution; the judge is miscalibrated in '
                'exactly the region users care about; or the metric measures the retriever while '
                'the failure is in generation or the tool layer. Distinguish by slicing the online '
                'sample by query cluster and comparing that distribution to the golden '
                'set&rsquo;s: if a cluster is 30% of traffic and 2% of your cases, that is drift '
                'and no amount of judge tuning fixes it. The structural repair is a trace '
                'harvester feeding negative feedback and sub-threshold scores back into the case '
                'store.'),
             a_simple=('<b>Three suspects, and one comparison separates them.</b> Either your test '
                       'cases no longer look like real traffic, or the automatic grader is wrong '
                       'in exactly the area users care about, or you are measuring the finding '
                       'step while the failure is in the writing step. To tell which: group real '
                       'requests by topic and compare that mix to the mix in your test set. If a '
                       'topic is a third of real traffic and almost none of your cases, that is '
                       'your answer. Then fix it permanently by feeding complaints back in as new '
                       'test cases.')),
        dict(q='Recall@10 is 0.91 and users say the answers are wrong. Which number do you look at?',
             a=('<b>Faithfulness, and it is a separate number by design.</b> Recall 0.91 with '
                'faithfulness 0.60 is the named failure of this whole domain: the retriever found '
                'the right documents and the generator did not stay inside them. Split the report '
                'permanently &mdash; retrieval gets context recall at 0.80 and context precision '
                'at 0.75, generation gets faithfulness at 0.85 and groundedness at 0.80 &mdash; '
                'and gate on end-to-end while diagnosing with components. If faithfulness is also '
                'high, the failure is in the tool layer or the question was multi-hop and top-k '
                'returned four near-duplicates of the best chunk.'),
             a_simple=('<b>The one that measures whether the answer stayed inside what was '
                       'found.</b> Nine times in ten the search brought back the right pages, so '
                       'the search is not the problem &mdash; the writing step is going beyond '
                       'what those pages support. Those are two different scores and they must be '
                       'reported separately, permanently, because one can look excellent while '
                       'the other is poor. If the writing score is also high, then the question '
                       'needed several documents at once and the search returned four copies of '
                       'the same one.')),
        dict(q='Your judge and your humans disagree on 30% of cases. What do you do?',
             a=('<b>Do not tune the judge first &mdash; read the disagreements.</b> They almost '
                'always cluster, and the cluster tells you which problem you have: either the '
                'rubric is ambiguous for a class of cases, or the humans are inconsistent with '
                'each other. So measure inter-human agreement before blaming the judge. If two '
                'humans agree with each other at 0.6 you have a rubric problem, not a judge '
                'problem, and no recalibration will help. Then recalibrate against 100 labels '
                'split 10 excellent, 10 poor, 30 ambiguous, run 3 passes with rubric anchors, and '
                'require Spearman 0.85 before it gates anything.'),
             a_simple=('<b>Read the disagreements before you touch the grader.</b> They usually '
                       'cluster in one area, and that tells you what is actually broken. First '
                       'check whether two people grading the same cases agree with each other. If '
                       'they do not, your instructions for what counts as good are vague and the '
                       'automatic grader was never the problem. Fix the instructions, then '
                       're-check the grader against a hundred human-scored examples, and do not '
                       'let it block anyone&rsquo;s work until it tracks human scores closely.')),
    ],
    verdict=dict(
        no='"We&rsquo;d use RAGAS and track faithfulness." No account of where the golden set came '
           'from, no judge calibration, no gate, no online sampling, and no distinction anywhere '
           'between retrieval metrics and generation metrics.',
        yes='Three tiers named explicitly; a judge calibration number &mdash; Spearman 0.85 on 100 '
            'human labels &mdash; offered unprompted; concrete gate thresholds with a 5% '
            'regression tolerance; a golden set sourced from production failures and tagged by '
            'failure mode; and the eval&rsquo;s own cost computed at about &#36;12 a run.'),
    anchor=dict(
        formula=r'gate: faithfulness $\geq 0.85$ &nbsp;&middot;&nbsp; context recall $\geq 0.80$ &nbsp;&middot;&nbsp; regression $\leq 5\%$ &nbsp;&middot;&nbsp; judge Spearman $\geq 0.85$',
        formula_simple='Score the finding step and the writing step separately, hold the automatic '
                       'grader to a measured agreement with people, and block the change if '
                       'anything drops by more than a twentieth.',
        bullets=[
            'Three tiers catch three failures: assertions catch disasters, component evals localise, online sampling finds what you never wrote down',
            'Retrieval and generation metrics are not interchangeable &mdash; recall 0.91 with faithfulness 0.60 is a real system',
            'An uncalibrated judge is decoration: 100 labels, 3 passes, Spearman 0.85, or it gates nothing',
            'A full gated run costs about &#36;12 and about 4.5 minutes, so "too expensive" is not an argument',
        ]),
    chips=['golden dataset', 'LLM-as-judge calibration', 'context recall', 'faithfulness',
           'CI gate thresholds', 'trace harvesting'],
    followup='Your offline eval is green and users are complaining. What happened?',
),

]
