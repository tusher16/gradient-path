CARDS = [

# =====================================================================
dict(
    id='requirements',
    tier='foundation',
    title='Turning the prompt into numbers',
    kicker='Five minutes of questions with a hard stop, and you leave holding a scale sheet instead of a topic',
    simple=[
        'The prompt you are handed is underspecified on purpose. &ldquo;Design a system that '
        'answers questions over ten million internal documents&rdquo; is a topic, not a '
        'specification, and if you start drawing boxes you are guessing at every choice that '
        'actually decides the design.',
        'So you ask. But ask for numbers, not categories. &ldquo;Is this high scale?&rdquo; wastes '
        'your turn, because the answer is yes and yes cannot be multiplied by anything. '
        '&ldquo;Roughly how many documents: a hundred thousand, ten million, or a '
        'billion?&rdquo; hands you something you can work with. The interviewer usually has the '
        'number ready and is waiting to see whether you ask for it.',
        'Six questions cover almost any prompt: who uses this and what do they do with the answer; '
        'how fast, and measured how; how big the corpus is and how often it changes; what good '
        'means and who decides; what it may cost; and what happens when it is wrong. Then stop. '
        'Five minutes, not fifteen. What you carry out of this phase is a short list of numbers '
        'you will design against for the rest of the hour.',
    ],
    analogy=('<b>Like a builder quoting on a kitchen.</b> They ask how many people cook in it, '
             'whether you are living in the house during the work, and what you have to spend. '
             'Three questions, five minutes, and then they start sketching. A builder still '
             'asking questions an hour later is not being thorough, they are stalling, and you '
             'can hear it.'),
    trap_simple=('Asking whether it is &ldquo;high scale&rdquo;, or interrogating for twelve '
                 'minutes because asking feels safer than committing. Saying &ldquo;it '
                 'depends&rdquo; more than twice reads as indecision, not rigour. Ask for a '
                 'number, write it down, and if nobody gives you one, pick one out loud and say '
                 'what would change if you picked wrong.'),
    tech=[
        'Three independent 2026 frameworks allocate 5 minutes, 5-10 minutes and 5 minutes of a '
        '40-60 minute slot to clarification. Call it 10-15% of the interview, with a hard stop. '
        'Spend it on the six questions that always pay in a GenAI prompt: user and action; latency '
        'SLO with a percentile <i>and</i> an end point; corpus size, format, update rate and '
        'whether it holds PII; what &ldquo;good&rdquo; means and who owns the golden set; the cost '
        'ceiling per request or per month; and the blast radius of a wrong answer &mdash; '
        'embarrassing, expensive, or regulated.',
        'Then name the axis the prompt is secretly about, out loud, around minute four. '
        '&ldquo;Design a RAG system over 10M internal documents&rdquo; is a retrieval-quality and '
        'permissions problem, not a vector database problem. &ldquo;Design an inference serving '
        'layer for a 70B model&rdquo; is a GPU memory problem. &ldquo;Design real-time fraud '
        'detection&rdquo; is a latency and label-delay problem. That one sentence is a strong-hire '
        'signal, because it says you found the constraint before you drew anything.',
        'Every qualitative requirement leaves this phase as a number. &ldquo;Fast&rdquo; becomes '
        'p95 under 2 seconds to first token, streaming. &ldquo;Accurate&rdquo; becomes '
        'faithfulness at least 0.90 on a named golden set, measured weekly. Anything still '
        'qualitative when you start drawing is un-designable later, and the first row of every '
        'reconstructed rubric scores exactly this: does the candidate state that it is a '
        'probabilistic system and pin down latency, data sensitivity and scale first.',
    ],
    ask=[
        dict(q='Who are the users, and how many queries?',
             a='Usually: ~20,000 employees at ~10 queries a day. That is 200K/day, 2.3 QPS average and ~23 at peak.'),
        dict(q='p50 or p95, and to first token or to the last byte?',
             a='Usually: p95 under 2 s to first token, streaming. If the consumer is an API parsing JSON, only total time exists.'),
        dict(q='How big is the corpus, how fast does it change, does it hold PII?',
             a='Usually: 10M documents at ~1,500 tokens; minutes of freshness for hot sources, hours for the tail.'),
        dict(q='Do documents carry per-user permissions?',
             a='Usually yes &mdash; and that single answer reshapes retrieval, caching and evaluation all at once.'),
        dict(q='What does &ldquo;good&rdquo; mean, and who owns the judgement?',
             a='Usually: grounded answers with correct citations, scored on a golden set someone is named as owning.'),
        dict(q='What is the cost ceiling, per request or per month?',
             a='Often unstated. Propose one: under 5 cents per conversation is a defensible published anchor.'),
        dict(q='When it is wrong, is that embarrassing, expensive, or regulated?',
             a='This is the question that picks your degradation ladder. Ask it in the first five minutes, not the last five.'),
    ],
    fig=dict(
        kind='blocks', h=300,
        boxes=[
            dict(x=24, y=118, w=156, h=76, t='answer questions over 10M internal docs',
                 tone='sig', sub='the prompt, as given'),
            dict(x=214, y=30, w=176, h=44, t='how many users, how often?'),
            dict(x=214, y=94, w=176, h=44, t='p95 to first token, or total?'),
            dict(x=214, y=158, w=176, h=44, t='per-user permissions?'),
            dict(x=214, y=222, w=176, h=44, t='what happens when it is wrong?'),
            dict(x=430, y=30, w=256, h=44, t='2.3 QPS average, 23 at peak', tone='mem'),
            dict(x=430, y=94, w=256, h=44, t='2 s p95, streaming', tone='mem'),
            dict(x=430, y=158, w=256, h=44, t='filter before you rank', tone='mem'),
            dict(x=430, y=222, w=256, h=44, t='degrade, never guess', tone='mem'),
        ],
        links=[dict(a=0, b=1), dict(a=0, b=2), dict(a=0, b=3), dict(a=0, b=4),
               dict(a=1, b=5, tone='mem'), dict(a=2, b=6, tone='mem'),
               dict(a=3, b=7, tone='mem'), dict(a=4, b=8, tone='mem')],
        labels=[dict(x=102, y=16, t='the prompt', tone='sig'),
                dict(x=302, y=16, t='what you ask'),
                dict(x=558, y=16, t='what you design against', tone='mem')],
        foot='a question whose answer you cannot multiply is a question you should not have asked',
        alt='A vague one-line prompt on the left fanning into four clarifying questions, each '
            'resolving on the right into a number or a design constraint'),
    caption=('The right-hand column is the deliverable. Four of those five boxes are numbers you '
             'will multiply within the next ten minutes; the fifth, permissions, is the constraint '
             'that decides whether your retrieval design is legal. Nothing on the left column is '
             'worth asking unless it lands in the right one.'),
    caption_simple=('The column on the right is what you are actually collecting. Each answer is '
                    'either a number you will multiply in a moment, or a hard constraint that '
                    'rules out whole designs. A question that lands in neither column was not '
                    'worth the minute it cost.'),
    when=[
        'The prompt is one sentence long and the interviewer has stopped talking',
        'You are four minutes in with no number on the board',
        'Someone says the system should be fast, or accurate, and means neither precisely',
        'A requirement arrives with no percentile and no owner attached',
    ],
    trap=('&ldquo;Is this high scale?&rdquo; &mdash; the answer is yes, and yes is not a number '
          'you can multiply. The mirror-image failure is interrogating for twelve minutes because '
          'asking feels safer than committing: Design Gurus names indecision, &ldquo;it '
          'depends&rdquo; more than twice, as a mistake that sinks otherwise strong candidates. '
          'Clarification is a data-gathering step with a hard stop, not a personality.'),
    real=('Uber&rsquo;s GenAI Gateway (engineering blog, 2024-07-11) is requirements-driven design '
          'in public. They counted <b>60+ internal LLM use cases across roughly 30 teams</b> and '
          'built one Go proxy mirroring OpenAI&rsquo;s HTTP interface so LangChain and LlamaIndex '
          'kept working unchanged. It serves about <b>16M queries a month at ~25 QPS peak</b> '
          '&mdash; and 25 QPS is a small number. The requirement that actually shaped the '
          'architecture was governance and PII redaction, not throughput. A candidate who had only '
          'asked about scale would have designed the wrong system.'),
    drills=[
        dict(q='You have assumed 10 million documents. What changes at 1 billion?',
             a=('<b>The index stops fitting on one node, which turns a tuning problem into a '
                'routing problem.</b> At 10M documents, 512-token chunks give ~34M vectors, about '
                '58 GB at int8 once you count the HNSW graph and ID overhead &mdash; one '
                'large-memory node, two for HA. At 1B you are 100 times that, so you shard, and '
                'the recall-versus-latency tradeoff moves from &ldquo;tune HNSW&rdquo; to '
                '&ldquo;route the query to the right shard&rdquo;. Re-embedding crosses a line too: '
                'a weekend job becomes a capacity-planning exercise with a schedule and a budget.'),
             a_simple=('<b>The search index stops fitting on one machine, and that changes the '
                       'whole problem.</b> At ten million documents the index is tens of gigabytes: '
                       'one big machine, two if you want a spare. Multiply by a hundred and it has '
                       'to be split across many machines, so the hard question stops being how to '
                       'tune one index and becomes which machine to send each question to. '
                       'Rebuilding it also stops being a weekend job and becomes something you '
                       'plan capacity and budget for.')),
        dict(q='The interviewer says it should be fast and accurate. What do you write on the board?',
             a=('<b>Two numbers, each with a percentile and an owner, or you have been told '
                'nothing.</b> &ldquo;Fast&rdquo; becomes p95 under 2 s to first token, streaming '
                '&mdash; and you ask whether the consumer is a chat UI, where TTFT is the SLO, or '
                'an API client parsing JSON, where only total time counts, because that answer '
                'decides whether a 90-200 ms reranker is affordable at all. &ldquo;Accurate&rdquo; '
                'becomes faithfulness at least 0.90 on a named golden set, measured weekly, with a '
                'person who owns the set. Write both down and design against them.'),
             a_simple=('<b>Two numbers, each with a promise about how often it holds.</b> '
                       '&ldquo;Fast&rdquo; means nothing until you say the slowest request in '
                       'twenty must start answering within two seconds, and until you know whether '
                       'the user is a person watching words appear, where the first word is what '
                       'counts, or a program waiting for a complete reply, where only the finish '
                       'line counts. &ldquo;Accurate&rdquo; means nothing until you name a set of '
                       'test questions, a score to beat on them, a person who owns that set, and '
                       'how often it is re-run.')),
        dict(q='Four questions in, the interviewer is being vague on purpose. What do you do?',
             a=('<b>Pick the numbers yourself, say them out loud as assumptions, and move.</b> '
                '&ldquo;I will assume 20,000 employees at 10 queries a day, so 200K queries a day, '
                '2.3 QPS average and ~23 at peak on a 10x factor &mdash; stop me if that is off by '
                'an order of magnitude.&rdquo; Then design against it. The rubric rewards stating '
                'assumptions as assumptions and penalises stalling. The vagueness is usually the '
                'test: they want to see you commit to a number and then name which parts of the '
                'design would change if it were wrong.'),
             a_simple=('<b>Choose the numbers yourself, say them out loud as guesses, and start '
                       'designing.</b> Twenty thousand staff asking ten questions a day is two '
                       'hundred thousand questions a day, a couple a second on average and perhaps '
                       'twenty a second in the busiest minute. Say that, invite them to correct '
                       'it, and carry on. The vagueness is often deliberate: they are checking '
                       'whether you can commit to a number and then say which parts of your design '
                       'would change if that number were wrong.')),
    ],
    verdict=dict(
        no=('Starts drawing boxes in minute one. Or the opposite: twelve minutes of &ldquo;is this '
            'high scale?&rdquo; and &ldquo;does it need to be reliable?&rdquo;, arriving at the '
            'architecture with nothing on the board but adjectives. Both fail the same way &mdash; '
            'no numbers to design against, so every later choice is taste.'),
        yes=('Five minutes, six questions, every answer a number, then one sentence naming the axis '
             'the prompt is really about &mdash; permissions, GPU memory, or the label delay '
             '&mdash; and a written scale sheet defended for the rest of the hour. That sentence '
             'is the ladder step: a mid-level candidate asks what to build, a senior one tells you '
             'what the binding constraint will be before drawing it.')),
    anchor=dict(
        formula='&ldquo;fast&rdquo; &rarr; p95 &lt; 2 s to first token &nbsp;&middot;&nbsp; '
                '&ldquo;accurate&rdquo; &rarr; faithfulness &ge; 0.90, weekly, owned',
        formula_simple='Every adjective leaves this step as a number, a promise about how often it '
                       'holds, and a person who owns it.',
        bullets=[
            'Ask for a number, not a category &mdash; the interviewer has it ready',
            'Name the axis the prompt is secretly about, out loud, by minute four',
            'Five minutes and a hard stop; stated assumptions beat more questions',
        ]),
    chips=['scale sheet', 'latency SLO', 'golden set', 'permissions and PII', 'peak-to-average ratio'],
    followup='You&rsquo;ve assumed 10 million documents. What changes at 1 billion?',
),

# =====================================================================
dict(
    id='back-of-envelope',
    tier='foundation',
    title='The arithmetic you do out loud',
    kicker='Order of magnitude wins, four significant figures lose, and the setup is what is being scored',
    simple=[
        'Every design prompt has three or four multiplications hiding in it, and the reason to do '
        'them on the board is that they kill options before you get attached to them.',
        'Start from people. Twenty thousand staff asking ten questions a day is two hundred '
        'thousand questions a day, about two a second on average &mdash; and say out loud that '
        'the busy hour runs three to ten times higher, because sizing for the average is how '
        'systems fall over at nine in the morning.',
        'Then turn questions into tokens, tokens into money, and bytes into machines. Round hard '
        'while you do it: a day is roughly a hundred thousand seconds, and &ldquo;call it two '
        'hundred gigabytes&rdquo; is a better answer than two hundred and fourteen point seven, '
        'because precision here signals you are computing rather than reasoning.',
        'Then check the answer against something you already know. If an internal tool for five '
        'thousand people has come out needing ten thousand of the most expensive chips made, you '
        'have an arithmetic error &mdash; and catching it yourself scores better than never '
        'erring at all.',
    ],
    analogy=('<b>Like pricing a wedding on a napkin.</b> A hundred and twenty guests, three '
             'courses, forty pounds a head: within a minute you know whether this is a five '
             'thousand pound evening or a fifteen thousand pound one, and the answer changes the '
             'venue rather than the menu. Nobody cares that it came out at four thousand eight '
             'hundred and seventy.'),
    trap_simple=('Answering to four decimal places. Two hundred and fourteen point seven gigabytes '
                 'tells the room you are computing rather than reasoning; &ldquo;call it two '
                 'hundred&rdquo; tells them you know which digits are load-bearing. The other half '
                 'of the trap is quoting a price per million words and never once multiplying it '
                 'by the number of words you actually send.'),
    tech=[
        'Do it in five numbers, on the board, unprompted: QPS average and peak; tokens in and out '
        'per request; bytes of index or state; GPUs or dollars per hour; and the cost per request '
        'that falls out of the first four. The 2026 guidance is explicit that hand-waving about '
        'infrastructure no longer passes and that choices must be justified through '
        'cost-per-request analysis. Two multiplications win most GenAI prompts: tokens times '
        'price-per-token gives cost, and bytes-per-token times context times concurrency gives '
        'KV cache.',
        'Two rules turn a model into hardware. Forward compute is about two floating-point '
        'operations per parameter per token, and each decode step drags the entire weight matrix '
        'out of memory once &mdash; so the floor on time per output token is weight bytes divided '
        'by memory bandwidth, before any software exists. Llama-3.1-70B at BF16 is 140 GB of '
        'weights; across two H100s at 3.35 TB/s each, that floor is <b>20.9 ms per token</b> and '
        'a ceiling near <b>48 tokens/s at batch 1</b>, while the GPU sits at roughly <b>0.3% of '
        'its 989 TFLOP/s peak</b>. Prefill is the opposite regime: a 2,048-token prompt takes '
        'about 290 ms and is compute-bound. Same chip, two behaviours, and batching is the only '
        'thing that reconciles them.',
        'Finally, say which regime you sized for. In the published 70B walkthrough, sizing from '
        'peak concurrency gives ~62 H100s and sizing from average throughput gives ~3. Both '
        'arithmetics are correct; they answer different questions. Naming the gap out loud &mdash; '
        '&ldquo;I am sizing for concurrency because the SLO is time-to-first-token&rdquo; &mdash; '
        'is the clearest seniority signal available in an estimation round.',
    ],
    tech_note=('Round aggressively and announce that you are rounding. A day is 86,400 seconds, '
               'which is ten to the fifth for whiteboard purposes; a year is three times ten to '
               'the seventh; a million seconds is 11.6 days. Peak is 3-10x average and you should '
               'say which you used &mdash; the published moderation example takes 50M posts a day '
               'to ~578/s and then applies a 3-5x peak factor on top of that.'),
    math=dict(
        tex=r'\text{FLOPs per token} \approx 2P \qquad\qquad t^{\min}_{\text{token}} = '
            r'\frac{P \times \text{bytes per parameter}}{\text{HBM bandwidth}}',
        note='The first says a 70B forward pass is about 140 GFLOPs. The second says that at batch '
             '1 you will never beat 20.9 ms per token on two H100s, whatever you install. Batching '
             'is what lifts you off the floor; nothing else does.',
        cost='two rules, one whiteboard'),
    estimate=dict(
        label='Sizing a 70B out loud', cost='order of magnitude',
        rows=[
            dict(l='weights, 70B at BF16', w='70 billion x 2 bytes', r='140 GB'),
            dict(l='bytes moved per output token', w='one full pass over the weights', r='140 GB'),
            dict(l='decode floor, 2 x H100', w='140 GB / 6.7 TB per second', r='20.9 ms/token'),
            dict(l='single-user ceiling', w='1 second / 20.9 ms', r='~48 tokens/s'),
            dict(l='compute used doing it', w='140 GFLOPs/token vs 989 TFLOP/s', r='~0.3% of peak'),
            dict(l='KV cache per token', w='2 x 80 layers x 8 KV heads x 128 dim x 2 B', r='0.327 MB'),
            dict(l='concurrency, 2-GPU shard at BF16', w='(160 - 140 - 10) GB / 0.49 GB per request', r='~20'),
            dict(l='concurrency, same shard at FP8', w='(160 - 70 - 10) GB / 0.25 GB per request', r='~325', tot=True),
        ],
        note='Every row is a multiplication you can do standing up, and the last two rows are the '
             'whole design. The model did not get faster when you quantised it; it got smaller, '
             'and sixteen times as many people now fit on the same two cards. That is the sentence '
             'to say out loud.'),
    fig=dict(
        kind='pipeline',
        head=['WHAT YOU ASKED FOR', 'WHAT IT COSTS'],
        steps=[
            dict(t='20K users', sub='10 queries a day'),
            dict(t='200K/day', sub='2.3 QPS average'),
            dict(t='6,000 in', sub='10 chunks x 500', tone='sig'),
            dict(t='1.2B in/day', sub='80M out', tone='sig'),
            dict(t='2,400 a day', sub='dollars, mid tier', tone='mem'),
        ],
        foot='headcount to a daily bill in four multiplications; input is 15x output, which is where the money is',
        alt='A five-box chain: twenty thousand users becomes two hundred thousand queries a day, '
            'becomes six thousand input tokens each, becomes 1.2 billion tokens a day, becomes a '
            'daily bill'),
    caption=('Four multiplications from a headcount to a daily bill, and the picture carries a '
             'ratio the prose does not: 6,000 input tokens against 400 output. Input dominates a '
             'retrieval bill, which is why shrinking retrieved context beats every clever trick '
             'you can play on the generation side.'),
    caption_simple=('Five boxes and four multiplications take you from a headcount to a daily '
                    'bill. The picture also shows where the money goes: the material you feed in '
                    'is fifteen times the answer that comes back, so trimming what you send is '
                    'cheaper than anything you do to the reply.'),
    when=[
        'Anyone says the words &ldquo;at scale&rdquo; without a number attached',
        'You are choosing between two architectures and both sound reasonable',
        'The design implies buying GPUs and nobody has said how many',
        'A number on the board is off by a factor you cannot account for',
    ],
    trap=('Producing a number with four significant figures. &ldquo;214.7 GB&rdquo; signals you '
          'are computing rather than reasoning; &ldquo;call it 200 gigabytes&rdquo; signals you '
          'know which digits are load-bearing. The other half: quoting a per-token price and never '
          'multiplying it by tokens. Two dollars per million sounds free until you note that a '
          '10-chunk RAG prompt is ~6,000 input tokens and 200K requests a day is 1.2 billion input '
          'tokens a day.'),
    real=('Anthropic&rsquo;s Contextual Retrieval writeup (2024-09-19) prices the offline '
          'enrichment step at <b>1.02 dollars per million document tokens</b> with prompt caching '
          '&mdash; one number that converts any corpus straight into an ingestion bill. Ten '
          'million documents at ~1,500 tokens each is 15 billion tokens, so roughly <b>15,300 '
          'dollars, one time</b>. What it buys is published in the same place: top-20 retrieval '
          'failure falling <b>5.7% to 2.9%</b> with contextual BM25 and to <b>1.9%</b> with '
          'reranking. An estimate you can defend and a benefit you can quote, in one breath.'),
    drills=[
        dict(q='Where is that number most likely to be wrong?',
             a=('<b>Name the input with the widest uncertainty and give its range &mdash; not the '
                'arithmetic.</b> In a GenAI estimate it is almost always average output tokens or '
                'the peak-to-average ratio. Output length swings 3x between a terse answer and a '
                'chatty one, and peak runs 3-10x average depending on whether your users sit in '
                'one time zone or five. That pair alone moves a fleet by an order of magnitude. '
                'Then say what you would instrument on day one: a token histogram per endpoint and '
                'a per-minute request count, both shipped with the first deploy.'),
             a_simple=('<b>Point at the input you are least sure of and say how wide it could '
                       'be.</b> Usually two things: how long the answers turn out to be, which '
                       'easily varies threefold, and how much busier the busiest hour is than the '
                       'average one, which runs from three to ten times. Together those two can '
                       'change the size of the fleet tenfold. Then say how you would find out for '
                       'real &mdash; measure the length of every answer and the traffic per '
                       'minute, from the first day it is live.')),
        dict(q='One colleague sizes the 70B fleet at 62 GPUs, another at 3. Who is right?',
             a=('<b>Both, and the SLO decides which question you were being asked.</b> 62 comes '
                'from peak concurrency: 10,000 in-flight requests at ~325 per FP8 two-GPU shard is '
                '31 shards, so 62 H100s. 3 comes from average throughput: 1M requests a day at 500 '
                'output tokens is 500M tokens a day, ~5,800 tokens/s, and one H100 does '
                '2,400-2,780 tok/s at concurrency 100. The gap is queueing and burstiness. If the '
                'SLO is p95 TTFT you must size for concurrency; if the workload is an offline batch '
                'job that may queue, you size for throughput and save 20x.'),
             a_simple=('<b>Both are right, and the promise you made decides which one you use.</b> '
                       'The big number answers how many people can be mid-request at the same '
                       'instant. The small one answers how much text the fleet must produce across '
                       'a whole day. If people are watching words appear and you promised them a '
                       'fast start, you have to pay for the crowd. If the work is a batch job that '
                       'can wait in a queue overnight, you pay for the daily total instead, and '
                       'that is roughly twenty times cheaper.')),
        dict(q='Estimate the index for 10 million documents, out loud, in under a minute.',
             a=('<b>Chunks, then bytes, then compression &mdash; three multiplications.</b> 10M '
                'documents at ~1,500 tokens is 15B tokens; 512-token chunks with 15% overlap is '
                '~34M chunks. At 1,536 dimensions in fp32 that is 34M x 1,536 x 4 bytes, roughly '
                '<b>209 GB</b>. Scalar int8 quantisation cuts it 4x to ~52 GB for under 1% recall '
                'loss; add ~4.4 GB of HNSW graph and ~1.4 GB of ID tracking and you land at '
                '<b>~58 GB</b> &mdash; one large-memory node, two for HA. The 209 GB to 58 GB step '
                'is the most valuable thing to say out loud in that prompt.'),
             a_simple=('<b>Cut the documents into pieces, count the bytes, then squeeze.</b> Ten '
                       'million documents of a few pages each become roughly thirty-four million '
                       'searchable pieces. Each piece is stored as a long list of numbers, and at '
                       'four bytes a number that is a bit over two hundred gigabytes. Store each '
                       'number in one byte instead of four and you are near fifty, losing under '
                       'one percent of search quality; add the index structure and you land at '
                       'sixty. One large machine, two for a spare &mdash; and the '
                       'two-hundred-to-sixty step is the whole answer.')),
    ],
    verdict=dict(
        no=('&ldquo;We would need a few GPUs and a vector database.&rdquo; Or the mirror failure: '
            'a calculator answer to four significant figures with no visible chain, so nobody in '
            'the room can tell which assumption to argue with.'),
        yes=('Five numbers on the board with every multiplication visible, aggressive rounding '
             'announced as rounding, and one sanity check against a known anchor. The senior move '
             'is stating which regime you sized for &mdash; peak concurrency or average throughput '
             '&mdash; because on the same design those two arithmetics differ by 20x and only one '
             'of them matches the SLO you were given.')),
    anchor=dict(
        formula='FLOPs/token &asymp; 2P &nbsp;&middot;&nbsp; decode floor = weight bytes / HBM '
                'bandwidth &nbsp;&middot;&nbsp; cost per million = (per hour / tokens per hour) '
                '&times; 10<sup>6</sup>',
        formula_simple='Five numbers: how many requests, how many words each way, how many bytes '
                       'of index, what the hardware costs an hour, and what all that makes one '
                       'request cost.',
        bullets=[
            'Show the multiplication &mdash; the setup is what is being scored',
            'Round hard and say you are rounding; four significant figures is a tell',
            'Peak is 3-10x average, and sizing from the wrong one is a 20x error',
        ]),
    chips=['KV cache arithmetic', 'peak-to-average ratio', 'decode floor', 'index sizing', 'cost per request'],
    followup='Where is that number most likely to be wrong?',
),

# =====================================================================
dict(
    id='latency-budget',
    tier='foundation',
    title='Spending the milliseconds first',
    kicker='Write the budget as a subtraction before you have components, and let it delete the ones you like',
    simple=[
        'A budget is what stops you designing something four seconds slow and only finding out at '
        'the end. Write the promise down first, then spend it.',
        'Say the promise is that the slowest request in twenty starts answering within two '
        'seconds. A published breakdown for a retrieval chatbot spends it like this: understanding '
        'and routing the question, up to 120 milliseconds; finding the fifty most relevant '
        'passages, up to 220; re-ranking those down to ten with a slower and more accurate model, '
        'up to 200; assembling the prompt and running safety checks, up to 80; and the model '
        'beginning to speak, up to 450. Roughly a second, before it has said a useful word.',
        'Now every component has to buy its slot from another one. That is the point. A budget '
        'turns &ldquo;should we add a re-ranker&rdquo; from a matter of taste into a matter of '
        'arithmetic, and you will usually find that two or three architectures are already dead '
        'before you have drawn any of them.',
    ],
    analogy=('<b>Like a connecting flight.</b> You do not decide what to do in the airport and '
             'then hope the plane waits. You start from the departure time, subtract security, '
             'subtract the walk to the gate, and whatever is left is the time you actually have '
             'for coffee. If the arithmetic leaves eleven minutes, the coffee stops being a '
             'preference.'),
    trap_simple=('Budgeting only for the day when nothing goes wrong. The retry, the safety check '
                 'and the cache miss all happen inside the same promise you made about the slow '
                 'request in twenty. The giveaway sentence is &ldquo;search takes about ten '
                 'milliseconds, so we are fine&rdquo; &mdash; true only on an idle machine, with a '
                 'warm index, and one user.'),
    tech=[
        'Write it as a subtraction, top-down, and state the percentile and the end point in the '
        'same breath: p95 to first token is a different system from p95 to last byte. On a chat '
        'surface you are budgeting time-to-first-token and streaming hides everything after it; '
        'for an API consumer parsing JSON only total time exists. That one answer decides whether '
        'a 90-200 ms cross-encoder reranker is affordable at all, which is why you ask it in the '
        'requirements phase rather than discovering it in the deep dive.',
        'The component numbers are stable enough to memorise: vector search over 1M vectors p50 '
        '4-18 ms and p99 25-90 ms depending on engine; cross-encoder reranking 50-150 ms on GPU, '
        '200-400 ms on CPU; a dedicated safety classifier under 90 ms; a semantic cache hit under '
        '5 ms against 2-5 s live. The one that moves is generation. TTFT for a 70B on one H100 is '
        '~120 ms p50 at concurrency 10 and ~740 ms at concurrency 100, with p95 running 195 ms to '
        '1,450 ms. Vector search barely notices the load; the LLM is the load-dependent term, so '
        'budget it at peak concurrency and not at your desk.',
        'Two regimes break the template. Agent budgets multiply rather than add: four tool calls '
        'means five LLM turns at ~3.4 s each plus ~300 ms per tool, so ~18 s p50 and 35-45 s p95 '
        '&mdash; which is why agents stream intermediate status instead of trying to be fast. And '
        'inside a card authorisation the entire window is ~100 ms, of which fraud scoring gets '
        '10-50 ms. Nothing that calls an LLM fits, so precomputed features and a small model are '
        'chosen by the budget rather than by preference.',
    ],
    nums=[
        dict(k='RAG, TO FIRST USEFUL TOKEN', v='~1.2 s p95',
             s='the published five-stage budget; streaming hides everything after it'),
        dict(k='FRAUD, INSIDE THE AUTHORISATION', v='10-50 ms',
             s='of a ~100 ms window &mdash; a late score is the same as no score'),
        dict(k='TTFT, 70B ON ONE H100', v='195 ms &rarr; 1,450 ms p95',
             s='concurrency 10 to 100: this is the load-dependent term'),
        dict(k='VECTOR SEARCH, 1M VECTORS', v='4-18 ms p50',
             s='barely moves under load; do not spend your worry here'),
        dict(k='CROSS-ENCODER RERANK', v='50-150 ms on GPU',
             s='200-400 ms on CPU &mdash; and the first rung you drop'),
        dict(k='AGENT WITH 4 TOOL CALLS', v='~18 s p50',
             s='derived: five model turns plus tools &mdash; budgets multiply'),
    ],
    fig=dict(
        kind='stack',
        head=['WHERE THE p95 GOES', 'THE TWO YOU CAN CUT'],
        segs=[
            dict(t='parse + route', v=120, sub='60-120 ms'),
            dict(t='retrieve top-50', v=220, sub='120-220 ms', tone='mem'),
            dict(t='rerank to 10', v=200, sub='90-200 ms', tone='sig'),
            dict(t='assemble + check, 40-80 ms', v=80),
            dict(t='model + first token', v=450, sub='250-450 ms', tone='sig'),
        ],
        foot='top of every published band at once is 1.07 s; only two of the five have a cheaper rung underneath',
        alt='A one-second budget bar split into five segments: parse and route, retrieve, rerank, '
            'assemble and check, and model start, with model start much the largest'),
    caption=('The top of every published band at once comes to 1.07 s, which is the ~1.2 s p95 '
             'figure once the tail is allowed for. Two segments have a cheaper rung underneath '
             '&mdash; skip the reranker, start streaming earlier &mdash; and the other three are '
             'fixed costs paid on every single request, which is what you are really committing to.'),
    caption_simple=('Add the slowest version of each step and you land near a second, before the '
                    'answer has begun. Only two of the five can be shortened or dropped when you '
                    'are running late; the other three you pay every time, so they are the real '
                    'commitment.'),
    when=[
        'Someone proposes adding a reranker, a guardrail, or a second retrieval pass',
        'The design works on your laptop and the SLO was written for peak hour',
        'You are asked whether a chat feature can share the fraud model&rsquo;s path',
        'A p95 is quoted and nobody has said what the p99 does',
    ],
    trap=('Budgeting only the happy path. The retry, the guardrail and the cache miss all live '
          'inside the same p95, and so does the reranker queue you forgot about at concurrency '
          '100. The sentence that sinks candidates is &ldquo;retrieval is about 10 milliseconds, '
          'so latency is fine&rdquo; &mdash; measured alone, at concurrency 1, on a warm index, '
          'which is the only condition under which it is true.'),
    math=dict(
        tex=r'\text{budget left} = \text{SLO} - \sum_i \text{(already spent)}_i '
            r'\qquad \text{evaluated at peak concurrency}',
        note='The subtraction is the whole method. A component joins the design only if the '
             'remaining budget can pay for it at peak, with the retry and the guardrail already '
             'deducted &mdash; not at concurrency 1 on a warm cache.',
        cost='top-down, always'),
    real=('The 2025 latency-budget writeup documents a production p95 falling from <b>2.1 s to '
          '1.0 s</b> with no change of base model: the wins came from candidate-set discipline, '
          'conditional routing and streaming. The serving layer shows the same shape &mdash; '
          'Baseten reported prefill/decode disaggregation on Qwen3 Coder 480B at ~50K-token '
          'prompts giving <b>+61% requests/s and 50% lower TTFT</b>, and MLPerf v6.0 in April 2026 '
          'recorded <b>2.7x from software alone on identical 288-GPU hardware</b>. Latency is '
          'architecture, not procurement.'),
    drills=[
        dict(q='Your p95 is 1.2 seconds. What is your p99, and why is it different?',
             a=('<b>Worse, for reasons the mean structurally hides.</b> p99 is tail effects: a cold '
                'shard, a reranker queue that only forms above some concurrency, a retry after a '
                'provider 429, a GPU preemption. Name a concrete one and cap it &mdash; hedged '
                'requests to a second replica after a deadline, a deadline that degrades to '
                'skipping the reranker rather than waiting, a timeout that returns retrieved '
                'passages with no generation. The benchmark shows p95 TTFT going 68 ms to 1,450 ms '
                'from concurrency 1 to 100; that is queueing, not compute, and queueing is what '
                'your p99 is made of.'),
             a_simple=('<b>Noticeably worse, and for reasons that only appear when the system is '
                       'busy.</b> The slowest request in a hundred is usually waiting in a queue, '
                       'retrying after the model provider refused it, or hitting a piece of the '
                       'index that has gone cold. Name one and say how you would cap it: send a '
                       'duplicate request to a second machine when the first is late, or set a '
                       'deadline that skips the optional re-ranking step rather than letting the '
                       'whole request run over.')),
        dict(q='You have 90 ms of budget left and the team wants a cross-encoder reranker. Do they get it?',
             a=('<b>Not unconditionally &mdash; on GPU it is 50-150 ms, so at p95 it does not '
                'fit.</b> Three ways out, in order: make it conditional, running only when the top '
                'retrieval scores are close, which is where it earns its keep; buy the slot from '
                'generation by streaming earlier; or take it and renegotiate the SLO with the '
                'number in hand. Say what dropping it costs, because reranking is the largest '
                'single retrieval-quality lever available &mdash; reported P@10 going 0.62 to '
                '0.84. Make it the first rung of the degradation ladder, not a permanent yes or '
                'no.'),
             a_simple=('<b>Not as a permanent fixture: on a good graphics card it takes fifty to a '
                       'hundred and fifty milliseconds and you have ninety.</b> Run it only when '
                       'the top results score close together, or buy the time from somewhere else '
                       'and say what you gave up. And be honest about the cost of dropping it: '
                       're-ranking is the strongest single quality lever in retrieval, with '
                       'reported precision in the top ten going from about six in ten to more than '
                       'eight in ten. So make it the first thing you switch off under load, not '
                       'the first thing you delete.')),
        dict(q='Same retrieval design, but it is a fraud check inside a card authorisation. What survives?',
             a=('<b>Nothing that makes a network call to an LLM.</b> The whole authorisation window '
                'is ~100 ms and fraud scoring is budgeted 10-50 ms of it, so the budget picks the '
                'architecture for you: features precomputed and served from an in-memory store '
                '(Redis reports 100M ops/s across 20 nodes, sub-millisecond), a small model scoring '
                'in single-digit milliseconds (card networks are reported at 500 attributes in '
                '~1 ms), and rules as the fallback when the model is late. Everything else &mdash; '
                'graph features, an LLM explanation, a case file &mdash; runs after the decision '
                'and improves the next one.'),
             a_simple=('<b>Nothing that has to ask a large language model anything.</b> The whole '
                       'approval takes about a tenth of a second and the fraud check gets between '
                       'ten and fifty milliseconds of that. So the features must be computed in '
                       'advance and held in memory, the model must be small enough to answer in a '
                       'few milliseconds, and if it is late the decision falls back to plain '
                       'rules. Anything slower runs after the payment has been approved or '
                       'declined, and only improves the next decision.')),
    ],
    verdict=dict(
        no=('Adds components and measures at the end, then is surprised. Quotes a p50, budgets the '
            'happy path, and tests at concurrency 1 with a warm cache.'),
        yes=('States the SLO with its percentile and its end point by minute five, subtracts '
             'top-down, budgets the model at peak concurrency rather than at the desk, and names '
             'in advance which component gets dropped when the budget blows. The staff-level '
             'version adds one sentence more: at what traffic does this budget stop closing, and '
             'what do we do the day before that happens.')),
    anchor=dict(
        formula='p95 to first token = 120 + 220 + 200 + 80 + 450 ms &nbsp;&middot;&nbsp; measured '
                'at peak, with the retry counted inside',
        formula_simple='Write the promise down first, then subtract each step from it. A component '
                       'joins the design only if what is left can pay for it when the system is '
                       'busy.',
        bullets=[
            'Say the percentile and the end point: first token and last byte are different systems',
            'Vector search barely moves with load; generation is the load-dependent term',
            'Agent budgets multiply &mdash; five model turns and four tools is 18 seconds, not two',
        ]),
    chips=['time to first token', 'streaming', 'tail latency', 'admission control', 'degradation ladder'],
    followup='Your p95 is 1.2 s. What is your p99, and why is it different?',
),

# =====================================================================
dict(
    id='cost-model',
    tier='foundation',
    title='Dollars per request, unprompted',
    kicker='Cost is a scored row now, and the answer is a chain of multiplications you volunteer before anyone asks',
    simple=[
        'Say what one request costs before the interviewer asks. It is one of the rows they score, '
        'and it is the row candidates skip.',
        'The arithmetic is small. A retrieval answer sends about six thousand words of context and '
        'gets back about four hundred. Two hundred thousand questions a day is a bit over a '
        'billion words in and eighty million out. At mid-tier hosted prices that is a few thousand '
        'a day, close to a hundred thousand a month; on the cheapest fast tier the same design '
        'runs under thirteen thousand a month. Same architecture, roughly eight times the bill, '
        'and the only difference is which model answers.',
        'The second thing to know is that owning hardware is cheap only while it is busy. The same '
        'rented graphics card costs about thirty-five cents per million words produced when it is '
        'fully loaded, and about seven dollars per million when it runs at a twentieth of '
        'capacity. Utilisation, not the purchase order, is the number that decides.',
    ],
    analogy=('<b>Like a taxi meter you cannot see.</b> Every prompt is a fare and the fare is '
             'charged by the word, both ways. A tenth of a penny a ride sounds like nothing until '
             'you notice the meter runs two hundred thousand times a day, and that most of the '
             'fare is the material you handed the driver rather than the answer you got back.'),
    trap_simple=('Quoting a price per million words and never multiplying it by the words you '
                 'actually send. Two dollars per million sounds like nothing until you notice each '
                 'answer ships six thousand words of retrieved material and there are two hundred '
                 'thousand of them a day. The other half is proposing to buy your own hardware to '
                 'save money without saying how busy you will keep it.'),
    tech=[
        'Quote bands with a date; never pair a model name with a price as fact. Mid-2026 prices per '
        'million tokens, input then output, checked 2026-08-20: a nano or flash tier around '
        '0.20-0.25 and 1.25-1.50; a small tier around 0.75-1.00 and 4.50-5.00; a mid tier around '
        '2.00-2.50 and 10-15; a frontier tier around 5.00 and 25-30; hosted open-weight models at '
        '0.14-0.28 and 0.28-0.42. Two independent price indexes disagree about which model sits in '
        'which row and agree about the rows, so the band is the fact and the name is not. Three '
        'multipliers move designs: cached input reads at about 10% of the input rate, batch or '
        'async at 50% off, and a long-context surcharge of 2x input and 1.5x output above ~272K '
        'tokens &mdash; which turns &ldquo;just use a bigger context window instead of '
        'retrieval&rdquo; into a costed decision rather than a free one.',
        'Self-hosting is roughly an order of magnitude cheaper per token, and only if the GPU stays '
        'busy, which is a scheduling problem rather than a procurement one. One H100 at 2.99 an '
        'hour serving a 70B at FP8 and concurrency 100 produces ~2,400 tokens/s, or 8.64M tokens '
        'an hour: about <b>0.35 per million output tokens at full utilisation, 1.73 at 20%, and '
        '6.92 at 5%</b>. Against a mid-tier hosted output rate near 10 per million, full '
        'utilisation is ~28x cheaper and the 5% case is not cheap at all &mdash; and you have also '
        'taken on an on-call rota.',
        'The highest-leverage cost decision in a serving design is neither the model nor the '
        'vendor: it is whether you can quantise. In the published 70B walkthrough a two-GPU shard '
        'at BF16 holds ~20 concurrent requests, because 140 GB of weights leaves almost nothing '
        'for KV cache; at FP8 the weights halve, the cache per token halves, and the same shard '
        'holds ~325. Serving 10,000 concurrent requests is therefore <b>666 H100s or 62</b>, which '
        'at 2.99 per GPU-hour is about <b>1.43M a month against about 133K</b>. Quantisation is a '
        'concurrency decision that arrives as a ten-fold cost difference, not a speed tweak '
        '&mdash; and because it is a model change, it goes through the eval gates like one.',
    ],
    tech_note=('When the business asks you to cut cost per request, the order of return is fixed: '
               'cache prefixes first, near-free and correctness-neutral; route easy traffic to a '
               'small model, which is where the multiple actually comes from; shrink retrieved '
               'context, since input tokens dominate in RAG; batch anything not user-facing at '
               'half price; and only then consider self-hosting, with a utilisation number '
               'already in hand.'),
    estimate=dict(
        label='Pricing the RAG answer', cost='hosted bands, checked 2026-08-20',
        rows=[
            dict(l='input tokens per query', w='10 chunks x 500, plus the prompt', r='~6,000'),
            dict(l='queries per day', w='20K users x 10 each', r='200K'),
            dict(l='input tokens per day', w='200K x 6,000', r='1.2 billion'),
            dict(l='input bill, mid tier', w='1,200 million x 2 dollars', r='2,400 a day'),
            dict(l='output bill, mid tier', w='80 million x 10 dollars', r='800 a day'),
            dict(l='monthly, mid tier', w='3,200 a day x 30', r='~96K a month', tot=True),
            dict(l='same design, flash tier', w='0.25 in / 1.50 out', r='~12.6K a month', tot=True),
            dict(l='cost per query', w='96K / 6M queries a month', r='1.6 cents vs 0.2'),
        ],
        note='That 8x gap is larger than any infrastructure saving available anywhere else in the '
             'design, and it needs no new components &mdash; only a router and an eval set proving '
             'the small model is good enough on the easy 70%. Quote it both ways: in dollars per '
             'month, which is what finance asks, and in cents per query, which is what the PM asks.'),
    fig=dict(
        kind='bars',
        head=['WHAT YOU PAY', 'WHAT ACTUALLY MOVES IT'],
        lw=176, vmax=30,
        bars=[
            dict(label='self-host, fully busy', v=0.35, tone='mem', note='0.35'),
            dict(label='open-weight hosted', v=0.42, tone='mem', note='0.28-0.42'),
            dict(label='nano / flash tier', v=1.50, note='1.25-1.50'),
            dict(label='self-host, 20% busy', v=1.73, tone='sig', note='1.73'),
            dict(label='small tier', v=5.00, note='4.50-5.00'),
            dict(label='self-host, 5% busy', v=6.92, tone='sig', note='6.92'),
            dict(label='mid tier', v=15, note='10-15'),
            dict(label='frontier tier', v=30, note='25-30'),
        ],
        xlab='dollars per million output tokens, 2026 bands',
        foot='the same H100 appears three times; utilisation moves it further than any purchase decision',
        alt='Horizontal bars of dollars per million output tokens, with one self-hosted H100 '
            'appearing at full, twenty percent and five percent utilisation, straddling four '
            'hosted price tiers'),
    caption=('Every bar is dollars per million output tokens on one axis. Three of them are the '
             'same H100 at three utilisations, and they straddle four hosted tiers &mdash; which '
             'is why &ldquo;we will self-host to save money&rdquo; is an incomplete sentence until '
             'you say what fraction of the hour the card is busy.'),
    caption_simple=('The same rented graphics card appears three times: at full load, at a fifth '
                    'of it, and at a twentieth. It moves from cheaper than anything you can rent '
                    'to dearer than most of it without the hardware changing at all. The question '
                    'is never what you buy, it is how busy you keep it.'),
    when=[
        'You have named a model and not yet named a price',
        'Someone proposes a bigger context window instead of retrieval',
        'The design self-hosts and nobody has said what utilisation it assumes',
        'The business hands you a target cost per request',
    ],
    trap=('Quoting a per-token price and never multiplying it by tokens. &ldquo;It is about two '
          'dollars per million, so it is basically free&rdquo; &mdash; then the 10-chunk RAG prompt '
          'turns out to be 6,000 input tokens, 200K requests a day is 1.2 billion input tokens a '
          'day, and the input alone is 2,400 dollars a day. The second half is proposing '
          'self-hosting for cost with no utilisation figure: the same H100 is 0.35 or 6.92 per '
          'million output tokens depending only on how busy you keep it.'),
    real=('DoorDash&rsquo;s LLM content embeddings (engineering blog, 2026-04-14) is a cost '
          'decision that reported as a quality result. They truncated Gemini-embedding-001 to '
          '<b>256 dimensions</b> using Matryoshka representations and re-embedded only entities '
          'that had actually changed rather than the whole catalogue &mdash; storage and search '
          'cost fall directly with dimension count. Quality went up anyway: offline <b>P@10 from '
          '68% to 85%</b>, search null rate <b>down 3.65%</b>, session conversion <b>up 0.66%</b>, '
          'homepage order rate <b>up 2.4%</b>. The cheap version won on the metric as well as the '
          'invoice.'),
    drills=[
        dict(q='Your cost per request is 0.4 cents. The business wants 0.1. What do you cut?',
             a=('<b>In this order, and item two gets you there on its own.</b> One, cache '
                'prefixes: cached input reads at ~10% of the input rate, near-free and '
                'correctness-neutral. Two, route easy traffic to a small model &mdash; the '
                'mid-to-flash gap on this same design is ~8x, more than the 4x you need. Three, '
                'shrink retrieved context, since input runs 15x output in RAG. Four, batch '
                'anything not user-facing at 50% off. Five, and only then, self-host &mdash; and '
                'only with sustained utilisation, because at 5% busy it is dearer than the hosted '
                'mid tier.'),
             a_simple=('<b>In order of return, and the second one alone gets you there.</b> First, '
                       'reuse the identical opening of every prompt, which most providers bill at '
                       'about a tenth of the normal rate. Second, send easy questions to a small '
                       'cheap model and keep the expensive one for the hard ones: on this design '
                       'that gap is about eightfold. Third, send less retrieved text, because what '
                       'you feed in is fifteen times the answer you get back. Fourth, run anything '
                       'nobody is waiting for overnight at half price. Only then buy hardware, and '
                       'only if you can prove you will keep it busy.')),
        dict(q='Finance asks whether to self-host the 70B. What do you need to know first?',
             a=('<b>Sustained utilisation, and whether you can quantise &mdash; nothing else moves '
                'the answer as far.</b> At full load one H100 at 2.99 an hour is ~0.35 per million '
                'output tokens, roughly 28x cheaper than a mid-tier hosted output rate; at 20% it '
                'is 1.73 and at 5% it is 6.92, at which point you are paying more than hosted and '
                'carrying the pager as well. Then the bigger lever: BF16 gives ~20 concurrent '
                'requests per two-GPU shard and FP8 gives ~325, so the same SLO is 666 H100s or '
                '62, about 1.43M a month against 133K. Decide quantisation before you decide '
                'vendor.'),
             a_simple=('<b>How busy the machines will really be, and whether the model can be '
                       'shrunk without losing quality.</b> Kept fully loaded, your own hardware is '
                       'roughly thirty times cheaper per word than a mid-tier service. Running at '
                       'a twentieth of capacity it is dearer than renting, and you have also taken '
                       'on the pager. Then the bigger lever: storing the model in half the space '
                       'lets about sixteen times as many people share one machine, which turns a '
                       'fleet of six hundred and sixty-six cards into sixty-two. That decision is '
                       'worth more than any negotiation with a vendor.')),
        dict(q='A colleague suggests skipping retrieval and pasting everything into a long context window. Price it.',
             a=('<b>It is a costed decision, and the published surcharge is the small part.</b> '
                'Above ~272K tokens the surcharge is 2x input and 1.5x output; but long before '
                'that, replacing a 6,000-token retrieved prompt with a 200,000-token stuffed one '
                'is a 33x input bill on every request, and input already dominates &mdash; 2,400 '
                'dollars a day becomes tens of thousands. Retrieval is a compression step you are '
                'paid to run. The defensible version of the suggestion is prefix caching for a '
                'shared system prompt at ~10% of the input rate, which is a different and much '
                'better idea.'),
             a_simple=('<b>It is a decision with a price tag, and the published surcharge is the '
                       'least of it.</b> Providers charge double for input beyond very long '
                       'contexts, but the real cost is that you have replaced six thousand words '
                       'of selected material with two hundred thousand words of everything, on '
                       'every single request, and what you send in is already the bigger half of '
                       'the bill. Retrieval is the step that decides what is worth paying to send. '
                       'The good version of the idea is reusing one identical shared opening '
                       'across requests, which most providers bill at about a tenth of the rate.')),
    ],
    verdict=dict(
        no=('Names a model, never a number. Says cost can be optimised later, or proposes '
            'self-hosting as a saving with no utilisation figure and no quantisation plan.'),
        yes=('Volunteers cost per request with the chain visible, quotes price bands with a date '
             'and refuses to attach them to a model name, and reaches for routing and caching '
             'before hardware. The senior version names the binding constraint behind the bill '
             '&mdash; KV cache memory, which is why quantisation is a ten-fold cost decision '
             '&mdash; and the staff version asks at what volume the hosted-versus-self-host answer '
             'flips, and how we would notice in time.')),
    anchor=dict(
        formula='cost per million = (price per hour / tokens per hour) &times; 10<sup>6</sup> '
                '&nbsp;&middot;&nbsp; utilisation is the variable, not the hardware',
        formula_simple='Work out what one request costs, in cents, and say it before you are '
                       'asked. Then remember that hardware you own is cheap only while it is busy.',
        bullets=[
            'Quote bands with a date; never pair a model name and a price as fact',
            'Input tokens dominate a retrieval bill &mdash; context length is the cost lever',
            'Quantisation is a concurrency decision: 666 GPUs or 62 for the same SLO',
        ]),
    chips=['model routing', 'prompt caching', 'batch pricing', 'utilisation', 'quantisation'],
    followup='Your cost per request is 0.4 cents and the business wants 0.1. What do you cut?',
),

# =====================================================================
dict(
    id='degradation',
    tier='foundation',
    title='What the system does when it is wrong',
    kicker='Every component here fails by returning something plausible, so &ldquo;retry and alert&rdquo; is not a strategy',
    simple=[
        'Most systems fail by stopping. This one fails by carrying on, confidently. Retrieval '
        'returns a passage from the wrong document and the model answers from it anyway; a tool '
        'call times out and the agent invents what it would have said. Nothing throws an error, so '
        'nothing wakes anybody up.',
        'Which makes the interesting question not what you do when it breaks, but what the user '
        'sees. Write the ladder down before you need it. Full answer with citations. Running late: '
        'the same answer without the slow re-ranking step. Model unavailable: the passages you '
        'found, with no answer written on top. Retrieval down: a recent similar answer, labelled '
        'as possibly stale. And at the bottom, an honest &ldquo;I do not know&rdquo; with a route '
        'to a human.',
        'Every rung still answers. A timeout is the only option that spends the whole budget and '
        'returns nothing at all. The last decision is which way to fail: if being late is the same '
        'as being absent, fail open and let simpler rules decide; if a wrong answer is regulated '
        'or dangerous, fail closed and say so.',
    ],
    analogy=('<b>Like a kitchen on a Saturday night.</b> When the orders back up, a good kitchen '
             'does not stop cooking &mdash; it drops the garnish, then simplifies the sauce, then '
             'tells the table the special is off. Each of those was decided on a quiet Tuesday and '
             'written on the wall. A kitchen improvising that ladder at eight in the evening sends '
             'out food nobody ordered.'),
    trap_simple=('Listing everything that can go wrong and never saying what the user sees. The '
                 'giveaway is offering retries and an alert to whoever is on call: retrying a '
                 'confident wrong answer just gets you a second confident wrong answer, because '
                 'nothing actually failed.'),
    tech=[
        'Enumerate failures by layer rather than by severity, because that is how they cluster. '
        'Retrieval: returns nothing, returns the wrong section, returns stale content, returns '
        'content this user is not allowed to see. Generation: hallucinates, ignores the context you '
        'gave it, exceeds the budget, gets rate-limited. Tools: time out, return malformed data, '
        'succeed with the wrong side effect. Infrastructure: GPU OOM, cold start, provider outage. '
        'Everything on that list except the last two returns HTTP 200.',
        'Then attach a rung to each class. The RAG ladder is: full answer with citations, answer '
        'without reranking, retrieved passages with no generation, cached similar answer with a '
        'staleness banner, honest failure with a path to a human. Each rung is cheaper than the one '
        'above and every rung beats a timeout. Serving-layer failures have their own fixes: on GPU '
        'OOM, preempt the longest-running request by swapping its KV cache to host memory or '
        'recomputing it, with admission control refusing new work before the pool is exhausted; on '
        'client disconnect, propagate cancellation, because without it a malicious client can DDoS '
        'you by opening and immediately closing connections while workers keep generating.',
        'Agents need mechanical limits, and the numbers are published: a hard step limit around 15 '
        'tool calls, repetition detection when the same tool is called twice with identical '
        'parameters, a context budget alert at 80%, a per-task dollar cap, and a circuit breaker '
        'when hourly spend passes 3x the rolling average. Reported runaway loops cost <b>50-500 '
        'dollars per incident before anyone notices</b>, and one code-review agent charged '
        '<b>12 dollars against a 40-cent average</b>. Anything with a side effect gets an '
        'idempotency key: an agent retrying a create-refund tool must not create two refunds, and '
        'that boring answer is the correct one.',
    ],
    tradeoffs=[
        dict(k='Fail open vs fail closed',
             v='<b>The product decides this, not the system.</b> Inside a payment authorisation a '
               'late fraud score is the same as no fraud score, so you fail open to rules and '
               'accept the fraud that slips through that window. For a regulated or clinical '
               'answer you fail closed and say you cannot answer, because a confident wrong answer '
               'is the expensive outcome. Say which one this product is, in a sentence, before you '
               'design the fallback.'),
        dict(k='Timeout vs deadline',
             v='<b>A timeout spends the entire budget and returns nothing.</b> A deadline '
               'propagated through the call chain lets each stage decide to skip itself: at 400 ms '
               'drop the reranker, at 900 ms return passages without generation. Same budget, an '
               'answer instead of a spinner.'),
        dict(k='Degrade everyone vs shed some',
             v='<b>Under real overload, shedding beats degrading.</b> Quietly serving a smaller '
               'model to everybody hides the incident; refusing the lowest-priority class &mdash; '
               'batch jobs, background summarisation &mdash; keeps the interactive SLO honest and '
               'keeps the incident visible. Per-tenant rate limits are the mechanism, and '
               'fair-share scheduling is what stops one team&rsquo;s retry loop starving '
               'everyone&rsquo;s chat.'),
        dict(k='Retry vs idempotency',
             v='<b>Retries are safe for reads and nothing else.</b> Any tool with a side effect '
               'takes an idempotency key and the retry carries the same key. Retrying a '
               'hallucination gets you a second hallucination; retrying a refund gets you a second '
               'refund, which is worse.'),
        dict(k='Silent fallback vs visible one',
             v='<b>Tell the user which rung they are on.</b> A staleness banner, a citation that '
               'links to its source, and an easy route to a human are product features that exist '
               'precisely because the failure mode is silent. A fallback nobody can see is '
               'indistinguishable from a bug, and it will be reported as one.'),
    ],
    fig=dict(
        kind='tree', h=382, nw=140,
        nodes=[
            dict(id='r1', x=100, y=38, t='full answer, cited', tone='mem', sub='the rung you want'),
            dict(id='r2', x=228, y=110, t='no reranking', tone='mem', sub='budget nearly spent'),
            dict(id='r3', x=356, y=182, t='passages, no answer', tone='mem', sub='citations still work'),
            dict(id='r4', x=484, y=254, w=162, t='cached + stale banner', sub='hit rates 20-45%'),
            dict(id='r5', x=612, y=326, t='honest failure', tone='sig', sub='and a route to a human'),
        ],
        edges=[
            dict(a='r1', b='r2', label='over 400 ms', dx=-64),
            dict(a='r2', b='r3', label='model down', dx=-64),
            dict(a='r3', b='r4', label='retrieval down', dx=-64),
            dict(a='r4', b='r5', label='nothing to serve', tone='sig', dx=-64),
        ],
        foot='each arrow is a failure class and every box still returns something; the missing box is the timeout',
        alt='A staircase of five rungs descending left to right: full cited answer, answer without '
            'reranking, passages with no generation, a cached answer with a staleness banner, and '
            'an honest failure with a route to a human'),
    caption=('Each step down is a rung you defined in advance, and each arrow is the failure class '
             'that pushes you there. The list of failure modes is table stakes; what is being '
             'scored is that every rung still returns something, and that you can say which rung '
             'this particular product stops at and why.'),
    caption_simple=('Read it as a staircase you walk down as things go wrong, one step per kind of '
                    'failure. Every step still gives the user something. The only real failure is '
                    'the step that is not drawn: a request that runs out of time and returns '
                    'nothing.'),
    when=[
        'The interviewer asks what the user sees when the provider is down',
        'You have finished listing failure modes and the room has gone quiet',
        'An agent in your design can call a tool that has a side effect',
        'The product is regulated, and a wrong answer is not merely embarrassing',
    ],
    trap=('Listing failure modes without ever saying what the user sees. The list is table stakes; '
          'the ladder is the differentiator. The sentence that gives it away is &ldquo;we would '
          'retry with exponential backoff and alert on-call&rdquo; &mdash; against a hallucination '
          'that buys you a second hallucination and a page nobody can action, because the '
          'component did not fail. It succeeded at returning something wrong.'),
    real=('Stripe Radar makes the point sharply: the fraud decision must land in <b>under 100 '
          'ms</b> inside the authorisation window, over <b>1,000+ characteristics</b> per '
          'transaction, so a model that answers late is exactly equivalent to no model at all and '
          'the fallback to rules is part of the design rather than an afterthought. The tuning '
          'target is public too &mdash; about <b>0.1% of legitimate payments blocked</b> against a '
          'base fraud rate near <b>1 in 1,000</b> &mdash; which is what a fail-open decision is '
          'really trading against.'),
    drills=[
        dict(q='Your LLM provider has a regional outage. What does the user see?',
             a=('<b>The rung you chose in advance, and it depends on what they were doing.</b> For '
                'interactive traffic, a router fails over to a second provider or a self-hosted '
                'fallback for the same task class, with a visible quality note; if neither exists, '
                'the retrieval-only rung &mdash; passages with citations and no synthesis, which '
                'for a search product is most of the value. For anything non-interactive, a queue '
                'that drains when service returns. Then say how it trips: per-provider error-rate '
                'and latency SLOs feeding a circuit breaker, or you will be failing over by hand '
                'at 3 a.m.'),
             a_simple=('<b>Whatever you decided in advance they should see.</b> For someone '
                       'waiting on a screen: switch to a second supplier or your own smaller '
                       'model, and tell them the answer is coming from the backup. If there is no '
                       'second supplier, show the passages you found with links and no written '
                       'answer &mdash; for a search product that is most of the value anyway. For '
                       'work nobody is waiting on, queue it and run it when service returns. And '
                       'say how you would notice: an automatic switch that trips on the error '
                       'rate, not a person reading a dashboard.')),
        dict(q='Your agent has been looping for forty minutes. What should have stopped it, and what did it cost?',
             a=('<b>Five mechanical limits, and not one of them is a better prompt.</b> A hard step '
                'limit around 15 tool calls; repetition detection when the same tool is called '
                'twice with identical parameters; a context budget alert at 80%; a per-task dollar '
                'cap; and a circuit breaker when hourly spend passes 3x the rolling average. '
                'Published figures: runaway loops cost 50-500 dollars before anyone notices, and '
                'one code-review agent charged 12 dollars against a 40-cent average. Quality '
                'degrades structurally too &mdash; agents are reported holding up for about five '
                'steps, then deteriorating as context accumulates &mdash; so the step limit '
                'protects the answer, not just the bill.'),
             a_simple=('<b>Five hard limits, and not one of them is a better prompt.</b> Stop after '
                       'about fifteen tool calls. Notice when the same tool is called twice with '
                       'exactly the same arguments. Warn when the conversation has filled four '
                       'fifths of the model&rsquo;s working memory. Cap what one task may spend. '
                       'Trip a breaker when this hour&rsquo;s spending is three times the usual. '
                       'Reported incidents run from fifty to five hundred dollars before anyone '
                       'notices; one code-review agent spent twelve dollars on a job that normally '
                       'costs forty cents. Quality also falls away after about five steps, so the '
                       'limit protects the answer too.')),
        dict(q='Fraud scoring took 120 ms. Do you block the transaction?',
             a=('<b>No &mdash; you fail open to rules and record the miss.</b> The authorisation '
                'window is ~100 ms and scoring is budgeted 10-50 ms of it, so a 120 ms answer '
                'arrived after the decision was needed. Treating late as &ldquo;decline&rdquo; '
                'declines good customers at whatever rate your model is slow &mdash; far more '
                'people than the fraud inside that window. Stripe deliberately blocks about 0.1% '
                'of legitimate payments against a base fraud rate near 1 in 1,000; a '
                'timeout-blocks policy would swamp both inside a day. Alert on the timeout rate '
                'instead, and fail closed only where a wrong answer is regulated.'),
             a_simple=('<b>No. Let it through on the simple rules and record that the model was '
                       'late.</b> The approval takes about a tenth of a second and the score '
                       'arrived after the decision was due. If late means decline, you turn away '
                       'honest customers every time the system is slow, and there are far more of '
                       'them than fraudsters. Roughly one payment in a thousand is fraudulent, and '
                       'a large processor deliberately refuses about one in a thousand good ones; '
                       'blocking on slowness would dwarf both. Fail the customer-safe way here, '
                       'and the other way only where a wrong answer is a legal problem.')),
    ],
    verdict=dict(
        no=('Lists failure modes and never says what the user sees, then offers retries and '
            'alerting. Treats a hallucination as an error to be retried rather than as a component '
            'succeeding at returning something wrong.'),
        yes=('Names the ladder rung by rung, attaches each rung to a failure class, and says which '
             'rung this product stops at and why. The senior signal is framing fail-open versus '
             'fail-closed as a product decision with a number attached &mdash; false declines '
             'against the fraud rate. The staff signal is asking when the ladder itself breaks: '
             'what share of traffic can sit on the bottom rung before the product is no longer '
             'worth shipping.')),
    anchor=dict(
        formula='full answer &rarr; no rerank &rarr; passages only &rarr; cached + banner &rarr; '
                'honest failure',
        formula_simple='Write the ladder down before you need it: full answer, faster answer, '
                       'passages with no answer, a recent answer marked as old, and finally an '
                       'honest admission with a way to reach a person.',
        bullets=[
            'Every rung still answers; a timeout spends the budget and returns nothing',
            'Fail open where late equals absent; fail closed where wrong is regulated',
            'Anything with a side effect takes an idempotency key, retries included',
        ]),
    chips=['degradation ladder', 'circuit breaker', 'idempotency keys', 'load shedding', 'admission control'],
    followup='Your LLM provider has a regional outage. What does the user see?',
),

]
