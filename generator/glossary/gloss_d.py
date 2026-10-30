G = {}
G["retrieval"] = [
 ("BM25","Keyword scoring that rewards rare words and discounts long documents.","The baseline a vector search must beat. Often it does not, on exact terms and product codes."),
 ("Hybrid retrieval","Running keyword and vector search together and merging the results.","The standard answer to 'semantic search missed an exact product name'."),
 ("HNSW","A navigable graph index that finds near neighbours fast by skipping across layers.","The default index in most vector databases. Trade-off: memory, and rebuild cost on updates."),
 ("Two-tower retrieval","Encoding query and item separately so item vectors can be precomputed.","How retrieval stays fast at scale — the cost of ranking millions is moved offline."),
 ("Contextual retrieval","Prepending document context to each chunk before embedding it.","The fix for chunks that are meaningless alone — 'it rose 3%' with no subject."),
 ("Cold start","No history yet for a new user or item, so personalisation has nothing to work with.","Every recommender design. The answer is content features or popularity until signal arrives."),
 ("PII redaction","Stripping personal data before text reaches a model or a log.","Any pipeline sending user content to a third-party API."),
 ("ACL pre-filter","Applying permissions before search, not after.","Filtering after retrieval returns a short or empty list and leaks existence; pre-filtering is the correct design."),
]
G["serving"] = [
 ("Prompt caching","Reusing the computed attention state for a prompt prefix you have already seen.","Long system prompts repeated every call — cuts both latency and cost substantially."),
 ("Prefix caching","The same idea at the serving layer: share KV cache across requests with a common prefix.","Why batching requests that share a system prompt is cheaper than it looks."),
 ("Prefix-aware routing","Sending requests with the same prefix to the same replica so the cache hits.","The follow-up to prefix caching — a cache only helps if routing cooperates."),
 ("PagedAttention","Storing the KV cache in fixed pages instead of one contiguous block.","vLLM's core trick. It removes the memory fragmentation that wasted most of the cache."),
 ("Continuous batching","Letting finished sequences leave the batch and new ones join mid-flight.","Why throughput jumps versus static batching — no waiting for the slowest sequence."),
 ("Chunked prefill","Splitting a long prompt's prefill into pieces so decoding is not starved.","How one long request stops blocking everyone else's tokens."),
 ("Speculative decoding","A small model drafts several tokens; the big one verifies them in a single pass.","Latency reduction with identical output. The follow-up: acceptance rate decides the gain."),
 ("Arithmetic intensity","Flops performed per byte moved from memory.","Why decoding is memory-bound and prefill is compute-bound — the key to any serving question."),
 ("Peak-to-average ratio","How much your busiest minute exceeds your average.","Capacity planning. Provision for the average and you fail every launch."),
 ("Admission control","Rejecting requests at the door when the system is saturated.","Better than accepting everything and timing out — fail fast and keep the queue honest."),
 ("Circuit breaker","Stopping calls to a failing dependency instead of retrying into it.","How a slow downstream service takes down everything upstream, and the standard prevention."),
 ("Cost per request","Total spend divided by requests served, broken down by token type.","The number that makes an architecture argument concrete instead of aesthetic."),
 ("Max input tokens","The hard ceiling on prompt length for a given model.","Chunking and context-packing decisions; the constraint that forces retrieval over stuffing."),
 ("Compaction","Merging accumulated writes or segments into a clean compacted form.","LSM-tree storage and vector-index maintenance — the background work that reclaims space."),
 ("Point-in-time correctness","Building features using only data that existed at prediction time.","The definition of no leakage in a feature store. The single most common training-serving bug."),
 ("Prompt versioning","Treating prompts as versioned artefacts with a changelog.","How you answer 'the model got worse last Tuesday' — without it, you cannot."),
 ("YaRN","A method for extending a model's context window beyond its trained length.","Long-context questions, alongside position interpolation."),
 ("Position interpolation","Squeezing position indices into the trained range so longer contexts still work.","The simpler long-context extension, usually needing a short fine-tune."),
 ("Attention scores","The softmaxed query-key products that decide where each token looks.","Reading an attention implementation, and any question about what the mask does."),
]
G["quant"] = [
 ("GPTQ","Post-training quantisation that compensates for error layer by layer, using sample data.","4-bit weights with small quality loss and no retraining."),
 ("AWQ","Quantisation that protects the small fraction of weights that matter most.","Named next to GPTQ. Often better at low bit widths; the trade-off question is quality versus speed."),
 ("NF4","A 4-bit number format spaced for normally distributed weights.","QLoRA's format — it fits the actual distribution of weights rather than spacing values evenly."),
 ("FP8 quantisation","An 8-bit floating format with real exponent bits, unlike int8.","Modern inference on recent hardware. It handles outlier activations that int8 cannot."),
]
