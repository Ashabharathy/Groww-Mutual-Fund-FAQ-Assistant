# Phase 1: Data Acquisition & Preparation - Edge Cases

This document outlines potential edge cases, risks, and failure modes during the Data Acquisition (Corpus Building) phase, along with proposed mitigations.

## 1. Source Unavailability
* **Edge Case:** One or more of the 15 strict Groww URLs return a `404 Not Found`, `500 Internal Server Error`, or timeout during the scraping process.
* **Mitigation:** Implement retry logic with exponential backoff. If a URL is permanently down, the system should log an alert and proceed with the remaining URLs, or gracefully fail the pipeline and notify the admin.

## 2. Anti-Scraping Mechanisms
* **Edge Case:** Groww's servers block the scraping tool by serving a CAPTCHA or blocking the IP due to perceived bot behavior.
* **Mitigation:** Use appropriate headers (e.g., `User-Agent`) to simulate a standard browser. Add delays between requests to avoid rate limits.

## 3. Dynamic Content Rendering
* **Edge Case:** Crucial mutual fund facts (like Expense Ratios or Exit Loads) are rendered dynamically via JavaScript and are not present in the initial static HTML payload, resulting in empty or incomplete chunks.
* **Mitigation:** If using a static scraper like `BeautifulSoup` fails, switch to a headless browser tool like `Playwright` or `Selenium` to wait for the page to fully render before extracting text.

## 4. Table Splitting and Context Loss
* **Edge Case:** A table containing multiple fund statistics is split down the middle by the text chunking algorithm (e.g., `RecursiveCharacterTextSplitter`), separating the row labels from their corresponding values.
* **Mitigation:** Utilize Markdown-aware or HTML-table-aware splitters that ensure tables are kept intact within a single chunk, or use a tool that converts tables to linear text statements prior to chunking.

## 5. Corrupted or Missing Metadata
* **Edge Case:** The scraper fails to parse the scheme name or the `last_updated_date` from the webpage, resulting in chunks with missing metadata.
* **Mitigation:** Hardcode the scheme names and AMC mapping since the 15 URLs are strictly predefined. If a date cannot be scraped, default to the timestamp of the scraping execution.
