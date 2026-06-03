# Why the SIB OSINT Concierge Uses Retrieval-Augmented Generation

The Sentinel Intelligence Bureau built the OSINT Concierge on
**Retrieval-Augmented Generation (RAG)** so the model's answers are
always grounded in the bureau's own unclassified knowledge base —
handbook, collection policy, attribution policy, publication policy,
public threat feeds — rather than guessed from the model's training
data.

## The pipeline

1. **Index.** The bureau's published policies, handbooks, and approved
   threat-feed entries are chunked into ~800-character windows and
   stored in an Azure AI Search index with both a vector embedding
   (1536-dim `text-embedding-3-small`) and the raw text.
2. **Retrieve.** Every analyst question is embedded and sent to AI
   Search as a **hybrid** query — keyword (BM25) catches exact
   indicator ids and policy section names, while vector similarity
   catches paraphrased intent. Reciprocal Rank Fusion merges the two
   candidate lists.
3. **Rerank.** Azure AI Search's **semantic ranker** then re-scores the
   fused pool with a cross-encoder transformer and returns the top-k
   chunks.
4. **Ground.** The top chunks are injected into the model prompt with
   a system message that requires every fact in the answer to come
   from the context, cited with a `[filename]` tag.
5. **Evaluate.** Every release is scored with `GroundednessEvaluator`
   and `RelevanceEvaluator` from `azure-ai-evaluation`. SIB legal
   requires aggregate scores of **3.5 or higher** on both metrics
   before the Concierge goes to production.

## Why hybrid plus semantic?

Keyword search alone misses paraphrased questions (an analyst asking
"can I quote this on a brief?" will never hit the word "publication").
Vector search alone misses exact identifiers (an indicator id or a
treaty article reference). Hybrid search gets both. The semantic ranker
on top then uses a transformer to pick the chunk that actually answers
the question, not just the chunk that is closest in embedding space.

## Why RAG instead of just prompting?

Without retrieval, the model has no SIB-specific context and will
either refuse to answer policy questions or make up plausible-sounding
policies. RAG gives the model **citable sources**, which is both a
correctness guarantee and the reason groundedness scores can rise above
4. Hallucinations drop sharply once the prompt explicitly says "answer
only from the Context block and cite sources in square brackets".

In the OSINT context this is doubly important: a Concierge answer that
cites a published source can be traced back, audited, and re-reviewed.
A Concierge answer that comes from model training data cannot.
