# Phase 2: Embedding & Vector Storage - Edge Cases

This document outlines potential edge cases, risks, and failure modes during the Embedding and Vector Storage phase, along with proposed mitigations.

## 1. API Rate Limiting and Downtime
* **Edge Case:** The embedding provider (e.g., OpenAI) rate-limits the embedding requests, or the API goes down during the indexing process.
* **Mitigation:** Implement exponential backoff and retry logic for the embedding API calls. Batch chunks appropriately to stay within RPM/TPM (Requests/Tokens Per Minute) limits.

## 2. Token Limit Exceeded
* **Edge Case:** A specific text chunk is exceptionally long and exceeds the maximum context window (token limit) of the embedding model (e.g., >8192 tokens for `text-embedding-3-small`).
* **Mitigation:** Enforce strict chunk size limits in Phase 1 (e.g., 1000 characters) and use a token-aware text splitter (like `tiktoken`) rather than purely character-based splitters.

## 3. Duplicate Vectors
* **Edge Case:** The pipeline is run multiple times, causing duplicate text chunks to be embedded and stored in the Vector DB, which heavily biases the similarity search.
* **Mitigation:** Implement a hashing mechanism (e.g., MD5 hash of the chunk text) as the unique ID for the vector document. Upsert based on this ID so duplicates overwrite rather than append.

## 4. Vector Database Resource Exhaustion
* **Edge Case:** The local Vector DB (e.g., ChromaDB) runs out of memory or disk space while indexing the vectors.
* **Mitigation:** Since the corpus is strictly limited to 15 URLs, the vector count should be very small (e.g., < 1000 vectors). However, ensure the host machine has adequate disk space and RAM, and clear old DB instances before a fresh ingestion.

## 5. Poor Semantic Separation
* **Edge Case:** Embeddings for different schemes look too mathematically similar because the boilerplate text on the Groww pages is identical across the 15 URLs.
* **Mitigation:** Ensure boilerplate headers, footers, and generic UI text are stripped during Phase 1. Prepend the scheme name explicitly to the chunk text before embedding to forcefully differentiate them in the vector space.
