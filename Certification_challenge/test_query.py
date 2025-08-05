#!/usr/bin/env python3
"""
Test script to check if the Tesla Investment Tracker can answer questions.
"""

from agentic_rag_bm25 import AgenticRAGBM25

def test_query():
    """Test if the app can answer a simple query."""
    
    print("🧪 Testing Tesla Investment Tracker Query Response...\n")
    
    # Initialize agent
    agent = AgenticRAGBM25()
    agent.load_tesla_data()
    agent.create_bm25_retriever()
    
    # Test query
    test_query = "What was Tesla's revenue in Q4 2023?"
    print(f"📝 Test Query: {test_query}")
    
    # Run analysis
    result = agent.run_comprehensive_analysis(test_query)
    
    print(f"\n📊 Analysis Result:")
    print(f"Query: {result['query']}")
    print(f"Response: {result['response']}")
    print(f"Context Used: {result['context_used']} documents")
    print(f"Sources: {result['context_sources']}")
    print(f"Fallback Mode: {result.get('fallback_mode', False)}")
    
    if result.get('fallback_mode'):
        print("\n⚠️ Running in fallback mode (no OpenAI API key)")
        print("To enable full LLM features, set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-openai-api-key'")
    else:
        print("\n✅ Full LLM analysis completed successfully!")

if __name__ == "__main__":
    test_query() 