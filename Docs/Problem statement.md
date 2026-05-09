# Problem Statement: Mutual Fund FAQ Assistant (Facts-Only Q&A)

## 📌 Overview
The objective of this project is to build a **facts-only FAQ assistant** for mutual fund schemes, using **Groww** as the reference product context. The assistant will answer objective, verifiable queries related to mutual funds by retrieving information exclusively from official, public sources such as AMC (Asset Management Company) websites, AMFI, and SEBI.

The system must strictly avoid providing investment advice, opinions, or recommendations. Every response must include a single, clear source link and adhere to defined constraints around clarity, accuracy, and regulatory compliance.

---

## 🎯 Objective
Design and implement a lightweight, **Retrieval-Augmented Generation (RAG)-based assistant** that:
- Answers factual queries about mutual fund schemes.
- Uses a curated corpus of official documents.
- Provides concise, source-backed responses.

---

## 👥 Target Users
- **Retail Investors:** Comparing mutual fund schemes and seeking factual data.
- **Customer Support & Content Teams:** Handling repetitive mutual fund-related queries efficiently.

---

## 🛠️ Scope of Work

### 1. Corpus Definition
- Select **Tata Mutual Fund** as the Asset Management Company (AMC).
- Collect and strictly use **exactly these 15 official URLs** (no other URLs will be used):
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

### 2. FAQ Assistant Requirements
The assistant must answer **facts-only** queries, such as:
- Expense ratio of a scheme
- Exit load details
- Minimum SIP amount
- ELSS lock-in period
- Riskometer classification
- Benchmark index
- Process to download statements or capital gains reports

**Response Formatting Rules:**
- Limited to a **maximum of 3 sentences**.
- Includes **exactly one** citation link.
- Includes a standardized footer: _“Last updated from sources: <date>”_

### 3. Refusal Handling
The assistant must politely **refuse** non-factual or advisory queries, such as:
- _“Should I invest in this fund?”_
- _“Which fund is better?”_

**Refusal Guidelines:**
- Be polite and clearly worded.
- Reinforce the "facts-only" limitation.
- Provide a relevant educational link (e.g., an AMFI or SEBI resource).

### 4. Minimal User Interface
The solution should feature a simple, user-friendly interface containing:
- A welcoming introductory message.
- **Three** clickable example questions to guide the user.
- A highly visible disclaimer: **“Facts-only. No investment advice.”**

---

## ⚠️ Constraints & Guidelines

### Data & Sources
- ✅ **DO:** Use only official public sources (AMC, AMFI, SEBI).
- ❌ **DO NOT:** Use third-party blogs, news articles, or aggregator websites.

### Privacy & Security
The system must **never** collect, store, or process Personally Identifiable Information (PII) such as:
- PAN or Aadhaar numbers
- Account numbers
- OTPs (One-Time Passwords)
- Email addresses or phone numbers

### Content Restrictions
- **No** investment advice, predictions, or recommendations.
- **No** performance comparisons or return calculations.
- _Note: For performance-related queries, provide a direct link to the official scheme factsheet only._

### Transparency
- Responses must be strictly short, factual, and verifiable.
- Every answer must include a definitive source link and a "last updated" date.

---

## 📦 Expected Deliverables
1. **README Document:**
   - Setup and installation instructions.
   - Selected AMC and chosen schemes.
   - Architecture overview explaining the RAG approach.
   - Known limitations of the current implementation.
2. **Disclaimer Snippet:**
   - The required disclaimer: _“Facts-only. No investment advice.”_ embedded clearly in the UI.

---

## 🏆 Success Criteria
- [ ] Accurate retrieval of factual mutual fund information.
- [ ] Strict and flawless adherence to facts-only responses.
- [ ] Consistent inclusion of valid, working source citations.
- [ ] Proper and polite refusal of all advisory or subjective queries.
- [ ] A clean, minimal, and user-friendly interface.
