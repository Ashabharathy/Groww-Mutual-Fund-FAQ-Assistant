import os
import re
import sys
import httpx
from functools import lru_cache
from groq import Groq
from dotenv import load_dotenv

# Add Phase 2 to path to import VectorStore
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase2_embedding"))
from vector_store import VectorStore

load_dotenv()

class RAGEngine:
    def __init__(self, groq_api_key=None, model_name=None):
        self.api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("WARNING: GROQ_API_KEY not found. LLM calls will fail.")
        
        # Use a custom httpx client with SSL verification disabled to handle
        # corporate network certificate issues
        http_client = httpx.Client(verify=False) if self.api_key else None
        self.client = Groq(api_key=self.api_key, http_client=http_client) if self.api_key else None

        # Use a smaller, faster Groq model by default for interactive queries.
        self.model_name = model_name or os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")
        print(f"RAGEngine using Groq model: {self.model_name}")
        
        # Initialize Vector Store from Phase 2
        db_path = os.path.join("data", "phase2_vector_db")
        self.vs = VectorStore(db_path=db_path)
        
        # Fixed list of 15 schemes for intent extraction
        self.schemes = [
            "Tata Small Cap Fund Direct Growth",
            "Tata Gold ETF FoF Direct Growth",
            "Tata Digital India Fund Direct Growth",
            "Tata Silver ETF FoF Direct Growth",
            "Tata Ethical Fund Direct Growth",
            "Tata Nifty Capital Markets Index Fund Direct Growth",
            "Tata Arbitrage Fund Direct Growth",
            "Tata Nifty Midcap 150 Momentum 50 Index Fund Direct Growth",
            "Tata Resources Energy Fund Direct Growth",
            "Tata India Pharma and Healthcare Fund Direct Growth",
            "Tata Index Fund Nifty Plan Direct",
            "Tata ELSS Fund Direct Growth",
            "Titanium Hybrid Long Short Fund Direct Growth",
            "Tata Money Market Fund Direct Growth",
            "Tata Nifty500 Multicap India Manufacturing 50:30:20 Index Fund Direct Growth"
        ]

    def is_pii_detected(self, query):
        """Simple regex to detect common PII patterns."""
        email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_regex = r'\b\d{10}\b'
        pan_regex = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
        aadhaar_regex = r'\b\d{4}\s\d{4}\s\d{4}\b'
        
        if re.search(email_regex, query) or re.search(phone_regex, query) or \
           re.search(pan_regex, query) or re.search(aadhaar_regex, query):
            return True
        return False

    def is_advisory_query(self, query):
        """Checks if the query is seeking investment advice."""
        advisory_keywords = [
            "should i invest", "is it good to buy", "better than", "recommend",
            "best fund", "where to put money", "prediction", "future returns"
        ]
        query_lower = query.lower()
        for kw in advisory_keywords:
            if kw in query_lower:
                return True
        return False

    def extract_scheme_intent(self, query):
        """Identifies which scheme the user is asking about using a weighted match."""
        query_lower = query.lower()
        best_match = None
        max_matches = 0
        
        # Keywords to ignore in the scheme name when matching
        ignore_keywords = {'tata', 'fund', 'direct', 'growth', 'scheme', 'mutual', 'plan', 'growth'}
        
        for scheme in self.schemes:
            # Significant keywords for this scheme
            scheme_keywords = [kw.lower() for kw in scheme.split() if kw.lower() not in ignore_keywords]
            
            # Count matches of significant keywords in the query
            match_count = sum(1 for kw in scheme_keywords if kw in query_lower)
            
            if match_count > max_matches:
                max_matches = match_count
                best_match = scheme
            elif match_count == max_matches and match_count > 0:
                # If tied, pick the one with the more specific name (longer)
                if best_match and len(scheme) > len(best_match):
                    best_match = scheme

        # Require at least one significant keyword match
        if max_matches >= 1:
            return best_match
        return None

    def get_context(self, query, scheme_filter=None):
        """Retrieves relevant chunks from Vector Store."""
        # If a specific scheme is identified, augment the query with the scheme name
        # so the semantic search is biased toward that fund's chunks
        search_query = f"{scheme_filter}: {query}" if scheme_filter else query

        # Retrieve top 30 to ensure we find chunks for the specific scheme and general info
        results = self.vs.query(search_query, n_results=30)
        
        filtered_docs = []
        filtered_metadatas = []
        
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]

            # Skip nav/boilerplate chunks that slipped through chunking
            if 'IndicesTrack markets' in doc or 'TerminalTrack charts' in doc:
                continue
            
            # ALWAYS prioritize/include General Info chunks if they appear in search results
            if meta['scheme_name'] == "General Tata Mutual Fund Information":
                filtered_docs.append(doc)
                filtered_metadatas.append(meta)
                continue

            # If a specific scheme was identified, prioritize its chunks
            if scheme_filter:
                if meta['scheme_name'] == scheme_filter:
                    filtered_docs.append(doc)
                    filtered_metadatas.append(meta)
            else:
                # If no scheme identified, include everything from top results
                filtered_docs.append(doc)
                filtered_metadatas.append(meta)
                
        # Return top 5 filtered chunks to provide sufficient context
        return filtered_docs[:5], filtered_metadatas[:5]

    def _format_response(self, answer, context_metas):
        no_info_phrases = ["i do not have factual information", "i don't know", "no relevant documents"]
        if any(phrase in answer.lower() for phrase in no_info_phrases):
            return answer

        if context_metas:
            top_meta = context_metas[0]
            return f"{answer}\n\nSource: {top_meta['source_url']}\nLast updated from sources: {top_meta['last_updated_date']}"
        return answer

    @lru_cache(maxsize=256)
    def _generate_answer(self, query):
        # 1. PII Check — hard guardrail, no LLM needed
        if self.is_pii_detected(query):
            return "Security Refusal: Your query contains personally identifiable information (PII). For security reasons, I cannot process queries containing PAN, Aadhaar, phone numbers, or email addresses."

        # 2. Advisory Check — hard policy guardrail, no LLM needed
        if self.is_advisory_query(query):
            return "Policy Refusal: I am a facts-only assistant and cannot provide investment advice, predictions, or fund recommendations. For educational resources on mutual funds, please visit the AMFI website: https://www.amfiindia.com/investor-corner"

        if not self.client:
            return "Error: Groq client not initialized. Please provide a GROQ_API_KEY."

        # 3. Intent & Retrieval
        scheme_intent = self.extract_scheme_intent(query)
        context_docs, context_metas = self.get_context(query, scheme_filter=scheme_intent)

        # 4. LLM Generation — always called for every useful query
        context_text = "\n---\n".join(context_docs) if context_docs else "No relevant documents found."

        system_prompt = f"""You are a strictly facts-only Mutual Fund FAQ Assistant for Tata Mutual Fund.
Your goal is to answer queries using ONLY the provided context from official documents.

CONSTRAINTS:
1. Answer in a MAXIMUM of 3 sentences.
2. Provide exact numerical values and details for:
   - NAV, AUM, Expense Ratio, Exit Load, Minimum SIP, Riskometer (Risk Level), Benchmark Index, and Lock-in Period.
3. If the query is about a specific fund, state the fund name in your answer.
4. Preserve all currency symbols (₹) and percentages (%) exactly.
5. Do not provide investment advice, opinions, or predictions.
6. If the context does not contain the specific answer (especially the numerical value requested), strictly state: "I am sorry, but I do not have factual information regarding this in the provided documents."
7. Be concise, professional, and data-driven.

CONTEXT:
{context_text}
"""

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0,
            max_tokens=220
        )
        answer = completion.choices[0].message.content.strip()
        return self._format_response(answer, context_metas)

    def process_query(self, query):
        return self._generate_answer(query.strip())

if __name__ == "__main__":
    # Quick Test
    engine = RAGEngine()
    print("RAG Engine Initialized.")
