# Phase 3: The RAG Engine & Core Logic - Edge Cases

This document outlines potential edge cases, risks, and failure modes during the RAG retrieval and generation phase, along with proposed mitigations.

## 1. Mixed Intent Queries (Advisory + Factual)
* **Edge Case:** The user asks a question that mixes factual requests with investment advice: *"What is the expense ratio of Tata Small Cap, and should I invest all my savings in it?"*
* **Mitigation:** The intent classification guardrail must be tuned to be highly conservative. If *any* part of the query is advisory, the system must trigger the refusal handler and decline the entire prompt politely.

## 2. Irrelevant Factual Queries
* **Edge Case:** The user asks a completely unrelated factual question: *"What is the capital of France?"* or *"Who won the cricket match?"*
* **Mitigation:** Add a system prompt constraint: *"If the query is unrelated to the provided mutual fund context, politely state that you can only answer questions related to the Tata Mutual Funds in your database."* 

## 3. Missing Context (Hallucination Risk)
* **Edge Case:** The semantic search fails to retrieve the correct chunk containing the answer, and the LLM guesses the answer based on its pre-trained knowledge, violating the "facts-only" constraint.
* **Mitigation:** The prompt must strictly mandate: *"Answer strictly using ONLY the provided context. If the answer is not contained in the context, reply exactly with: 'I do not have the information to answer that question.'"*

## 4. Aggregation Failures
* **Edge Case:** The user asks a question requiring data from multiple schemes: *"List the exit loads of all 15 Tata funds."* The Vector DB might only retrieve top-K chunks (e.g., K=4), missing the other 11 funds.
* **Mitigation:** Set a higher `K` value if the query intent is broad, or simply allow the LLM to answer based on the top-K chunks it *did* retrieve, while stating: *"Based on the top retrieved documents, here are the exit loads for..."*

## 5. Contradictory Information
* **Edge Case:** Two retrieved chunks contain slightly different factual data (e.g., due to parsing errors or different dates on the page).
* **Mitigation:** Instruct the LLM to either state both facts with their respective context, or prioritize the chunk with the most recent `last_updated_date`.
