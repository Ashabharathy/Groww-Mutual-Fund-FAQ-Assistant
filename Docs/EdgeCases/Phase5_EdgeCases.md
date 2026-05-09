# Phase 5: Testing, Validation & Deployment - Edge Cases

This document outlines potential edge cases, risks, and failure modes during testing and production deployment, along with proposed mitigations.

## 1. LLM Non-Determinism in Testing
* **Edge Case:** Automated integration tests fail because the LLM phrases the correct factual answer slightly differently than the hardcoded expected string in the test suite.
* **Mitigation:** Do not use exact string matching for automated testing of LLM outputs. Instead, use "LLM-as-a-judge" evaluation, semantic similarity scoring, or regex checks to verify key facts (e.g., asserting that the string "1.5%" is present in the response).

## 2. API Key Expiration or Revocation
* **Edge Case:** The deployment fails in production because the OpenAI/LLM API key or Vector DB cloud key expires, runs out of credits, or is accidentally exposed and revoked.
* **Mitigation:** Set up billing alerts for the LLM provider. Keep API keys securely injected via Environment Variables or a Secret Manager (e.g., Vercel Secrets), and never commit them to the repository.

## 3. Cold Starts and Memory Limits
* **Edge Case:** If deployed on a serverless platform (like Vercel or Streamlit Cloud), the application takes too long to wake up ("cold start"), or the environment runs out of RAM when trying to load the Vector DB into memory.
* **Mitigation:** If using a local Vector DB like ChromaDB, ensure the deployment tier has enough RAM. Alternatively, use a cloud-hosted Vector DB (like Pinecone or Qdrant Cloud) to offload the memory footprint from the serverless function.

## 4. Formatting Validation Failures
* **Edge Case:** The LLM occasionally ignores the formatting instruction and returns 4 sentences instead of the maximum of 3, failing the strict success criteria.
* **Mitigation:** Implement a post-processing validation function in the backend before sending the response to the frontend. If the response exceeds 3 sentences, forcefully truncate it or append a strict post-prompt enforcing brevity.

## 5. Missing Citation Link
* **Edge Case:** The LLM forgets to include the citation link, or formats it in a way the UI cannot render.
* **Mitigation:** Do not rely on the LLM to append the link and footer. Instead, the backend Python/JS code should directly extract the `source_url` and `last_updated_date` from the retrieved chunk's metadata and programmatically append it to the LLM's response.
