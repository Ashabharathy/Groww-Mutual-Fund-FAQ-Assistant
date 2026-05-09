import os
from rag_logic import RAGEngine

def main():
    print("=== Mutual Fund FAQ Assistant (Phase 3: RAG Engine) ===")
    print("Type 'exit' to quit.\n")
    
    # Initialize engine
    # It will look for GROQ_API_KEY in .env or environment variables
    engine = RAGEngine()
    
    if not engine.api_key:
        print("ALERT: No GROQ_API_KEY found. Please set it in your environment or a .env file.")
        print("Example: set GROQ_API_KEY=gsk_...")
        print("-" * 50)

    test_queries = [
        "What is the expense ratio of Tata Small Cap Fund?",
        "Should I invest in Tata Digital India Fund?",
        "What is my PAN ABCDE1234F balance?",
        "Who is the fund manager of Tata Ethical Fund?",
        "What is the weather in Mumbai?"
    ]
    
    print("Running sample test queries...\n")
    for q in test_queries:
        print(f"User: {q}")
        response = engine.process_query(q)
        print(f"Assistant: {response}")
        print("-" * 50)

    while True:
        user_input = input("\nAsk a question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        response = engine.process_query(user_input)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main()
