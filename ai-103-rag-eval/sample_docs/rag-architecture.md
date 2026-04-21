# Why Summitline Support Uses Retrieval-Augmented Generation

Summitline Outfitters built its support concierge on **Retrieval-Augmented
Generation (RAG)** so the model's answers are always grounded in Summitline's
own knowledge base — return policy, shipping, warranty, product data — rather
than guessed from the model's training data.

## The pipeline

1. **Index.** Summitline's policies, FAQs, and product copy are chunked into
   ~800-character windows and stored in an Azure AI Search index with both a
   vector embedding (1536-dim `text-embedding-3-small`) and the raw text.
2. **Retrieve.** Every customer question is embedded and sent to AI Search as
   a **hybrid** query — keyword (BM25) catches exact SKU strings and product
   names, while vector similarity catches paraphrased intent. Reciprocal Rank
   Fusion merges the two candidate lists.
3. **Rerank.** Azure AI Search's **semantic ranker** then re-scores the fused
   pool with a cross-encoder transformer and returns the top-k chunks.
4. **Ground.** The top chunks are injected into the model prompt with a
   system message that requires every fact in the answer to come from the
   context, cited with a `[filename]` tag.
5. **Evaluate.** Every release is scored with `GroundednessEvaluator` and
   `RelevanceEvaluator` from `azure-ai-evaluation`. Summitline legal requires
   aggregate scores of **3.5 or higher** on both metrics before the concierge
   goes to production.

## Why hybrid plus semantic?

Keyword search alone misses paraphrased questions (a customer asking "can I
send this back?" will never hit the word "return"). Vector search alone misses
exact identifiers (a SKU or a binding-compatibility code). Hybrid search gets
both. The semantic ranker on top then uses a transformer to pick the chunk
that actually answers the question, not just the chunk that is closest in
embedding space.

## Why RAG instead of just prompting?

Without retrieval, the model has no Summitline-specific context and will
either refuse to answer policy questions or make up plausible-sounding
policies. RAG gives the model **citable sources**, which is both a
correctness guarantee and the reason groundedness scores can rise above 4.
Hallucinations drop sharply once the prompt explicitly says "answer only from
the Context block and cite sources in square brackets".
