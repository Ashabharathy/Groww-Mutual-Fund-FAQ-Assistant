# 🏗️ Phase-wise Architecture: Mutual Fund FAQ Assistant (RAG)

## 📌 Architectural Overview
The system relies on a lightweight **Retrieval-Augmented Generation (RAG)** pipeline. It operates under a strict "facts-only" constraint, fetching data exclusively from a curated set of official Mutual Fund documents (AMCs, AMFI, SEBI).

The architecture is divided into 5 clear phases, ensuring data integrity, strict compliance (no investment advice), and a minimal, verifiable user experience.

---

## 🚀 Phase 1: Data Acquisition & Preparation (Corpus Building)
**Goal:** Gather and pre-process the ground truth data.

### Subphase 1.1: Source Identification & Loading Setup
- Define a strict, fixed list of exactly these 15 official URLs for Tata Mutual Funds (no other URLs will be used):
  - https://groww.in/mutual-funds/tata-small-cap-fund-direct-growth
  - https://groww.in/mutual-funds/tata-gold-etf-fof-direct-growth
  - https://groww.in/mutual-funds/tata-digital-india-fund-direct-growth
  - https://groww.in/mutual-funds/tata-silver-etf-fof-direct-growth
  - https://groww.in/mutual-funds/tata-ethical-fund-direct-growth
  - https://groww.in/mutual-funds/tata-nifty-capital-markets-index-fund-direct-growth
  - https://groww.in/mutual-funds/tata-arbitrage-fund-direct-growth
  - https://groww.in/mutual-funds/tata-nifty-midcap-150-momentum-50-index-fund-direct-growth
  - https://groww.in/mutual-funds/tata-resources-energy-fund-direct-growth
  - https://groww.in/mutual-funds/tata-india-pharma-and-healthcare-fund-direct-growth
  - https://groww.in/mutual-funds/tata-index-fund-nifty-plan-direct
  - https://groww.in/mutual-funds/tata-elss-fund-direct-growth
  - https://groww.in/mutual-funds/titanium-hybrid-long-short-fund-direct-growth
  - https://groww.in/mutual-funds/tata-money-market-fund-direct-growth
  - https://groww.in/mutual-funds/tata-nifty500-multicap-india-manufacturing-50%3A30%3A20-index-fund-direct-growth

### Subphase 1.2: Raw Data Extraction
- Use an asynchronous headless browser (`Playwright`) to navigate to each URL and wait for the dynamic React DOM to fully render, ensuring facts like Expense Ratios and NAV are captured.
- Extract the raw HTML content and the scheme name from the page `<title>`.
- Save the raw HTML files and a corresponding `_meta.json` (containing the source URL and scheme name) to a local `data/raw/` directory.

### Subphase 1.3: Data Cleaning & Chunking
- Read the raw HTML files from `data/raw/` and use `BeautifulSoup` to strip out noisy boilerplate tags (`header`, `footer`, `nav`, `aside`, `script`, `style`, `svg`).
- Isolate the main body/content and use `html2text` to convert the HTML into clean Markdown.
- **Advanced Noise Filtering:** Truncate the massive footer navigational link blocks (e.g., stopping at "Looking to invest in mutual funds?") and dynamically discard irrelevant sections (e.g., "Recently viewed", "Compare similar funds").
- **Semantic Split:** Use LangChain's `MarkdownHeaderTextSplitter` (splitting on `##` and `###`) to ensure that FAQs and entire sections stay together.
- **Custom Table Preservation:** For massive tables (like "Holdings"), programmatically split the table by rows (e.g., batches of 15) and *prepend the markdown header row* to each batch. This ensures isolated table chunks retain column context for accurate vector retrieval.
- **Fallback Chunking:** If any non-table semantic section still exceeds 1000 characters, use a `RecursiveCharacterTextSplitter` to gracefully sub-divide it while maintaining context.
- Save the highly localized semantic chunk arrays into a `data/cleaned/` directory.

### Subphase 1.4: Metadata Tagging & Export
- Tag each chunk with critical metadata: `source_url`, `amc_name`, `scheme_name`.
- Add a `last_updated_date` tag to satisfy the transparency footer requirement.
- Export to a final output format (e.g. `corpus_chunks.json`) for downstream use.

### Subphase 1.5: Automated Ingestion Pipeline (Scheduler)
- **GitHub Actions Integration:** Implement a workflow to automate the end-to-end data pipeline (Phases 1 & 2).
- **Scheduled Triggers:** Configure a `cron` schedule (e.g., daily) to pull the latest scheme data (NAV, expense ratios) from Groww.
- **Continuous Update:** Automate the process of re-scraping, re-cleaning, and re-indexing to ensure the assistant always provides the most recent factual data.

---

## 🧠 Phase 2: Embedding & Vector Storage
**Goal:** Convert text chunks into searchable vector representations.

1. **Embedding Generation:**
   - Pass the cleaned chunks through a text embedding model (e.g., local `sentence-transformers/all-MiniLM-L6-v2`).
2. **Vector Database Setup:**
   - Store the vectors and their associated metadata in a lightweight Vector Database (e.g., ChromaDB, FAISS, or Qdrant).
3. **Index Optimization:**
   - Optimize the index for fast similarity search using Cosine Similarity or Maximum Marginal Relevance (MMR) to fetch precise, factual snippets.

---

## ⚙️ Phase 3: The RAG Engine & Core Logic
**Goal:** Process user queries, retrieve context, and generate constrained answers.

1. **Query Pre-processing & Intent Classification (Guardrails):**
   - **Refusal Layer:** Intercept the query to check for advisory or subjective intent ("Should I buy?", "Which fund is better?").
   - *If advisory:* Trigger the **Refusal Handler** immediately, bypassing the LLM generation. Return a polite refusal + a relevant AMFI/SEBI educational link.
   - *If factual:* Proceed to the retrieval phase.
2. **Advanced Semantic Retrieval:**
   - **Intent-Based Metadata Filtering:** Use the LLM or a keyword-matching layer to identify the specific Mutual Fund scheme from the query and apply a hard metadata filter (`scheme_name`) to the Vector DB search. This prevents cross-fund hallucinations.
   - **Hybrid Search:** Combine Dense Vector Search (semantic similarity) with Sparse Keyword Search (BM25) to capture specific financial terms (e.g., "ELSS," "Exit Load") that embeddings might miss.
   - **Top-K Retrieval & Reranking:** Fetch the top 10 relevant chunks and use a Cross-Encoder reranker to select the most relevant 3-4 snippets for the final prompt context.
   - **Citation Mapping:** Ensure the `source_url` and `last_updated_date` are strictly mapped from the top retrieved chunk to the final response.
3. **Prompt Engineering & Generation (LLM):**
   - Combine the retrieved context with a strictly structured system prompt.
   - Use **Groq** (e.g., `llama-3-70b-versatile`) for extremely low-latency generation.
   - **System Prompt Constraints:**
     - "You are a strictly facts-only assistant."
     - "Answer using a maximum of 3 sentences."
     - "Do not provide investment advice or comparisons."
     - "If the answer is not in the provided context, state that you do not know."
     - **Unknown Answer Rule:** If you state you do not know, do not provide any citation or source URL.
     - **PII Guardrail:** If the query contains Personally Identifiable Information (PII) like PAN, Aadhaar, or email, refuse to process it and inform the user that PII is not allowed.
   - Pass the prompt and context to the LLM.
4. **Post-processing & Formatting:**
   - Extract the `source_url` and `last_updated_date` from the metadata of the top chunk used.
   - **Conditional Citation:** If the LLM successfully answered the question, format the final output as:
     ```text
     <Answer text (max 3 sentences)>
     <Citation Link>
     Last updated from sources: <date>
     ```
   - **Refusal/Unknown Format:** If the answer is unknown or a refusal, return ONLY the text without the citation link or footer.

---

## 💻 Phase 4: User Interface (Minimal UI)
**Goal:** Build the compliant user-facing application.

1. **Frontend Framework:**
   - Use a lightweight framework suited for AI apps like **Streamlit**, **Gradio**, or a simple **React/Vite** frontend.
2. **UI Components:**
   - **Header:** A simple welcome message establishing the assistant's purpose.
   - **Suggested Queries:** Three clickable, example factual questions to guide the user.
   - **Chat Interface:** Input box and chat history display.
   - **Disclaimer (Static & Visible):** A prominent banner stating: **“Facts-only. No investment advice.”**
3. **API Integration:**
   - Connect the frontend to the backend RAG engine via a REST API (e.g., FastAPI) or run it natively if using Streamlit.

---

## 🧪 Phase 5: Testing, Validation & Deployment
**Goal:** Ensure the system meets the "Success Criteria" and is safe for users.

1. **Retrieval Testing:** Validate that factual queries (e.g., minimum SIP amounts, lock-in periods) accurately fetch the correct document chunks.
2. **Guardrail Testing:** Perform adversarial testing to ensure the bot strictly refuses any form of investment advice or subjective comparisons.
3. **Formatting Validation:** Ensure absolutely no response exceeds 3 sentences and every single response includes the citation link and footer.
4. **Deployment:** Host the application on a reliable, lightweight platform (e.g., Vercel, Streamlit Community Cloud, Hugging Face Spaces).
