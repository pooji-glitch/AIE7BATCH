#!/usr/bin/env python3
"""
Debug script to see what the agent is returning.
"""

from agentic_rag_bm25 import AgenticRAGBM25
import json

def debug_agent():
    """Debug what the agent returns."""
    
    # Initialize agent
    agent = AgenticRAGBM25()
    agent.load_tesla_data()
    agent.create_bm25_retriever()
    
    # Test query
    test_query = "What was Tesla's revenue in Q4 2023?"
    print(f"📝 Test Query: {test_query}")
    
    # Run analysis
    result = agent.run_comprehensive_analysis(test_query)
    
    print(f"\n📊 Raw Result:")
    print(json.dumps(result, indent=2, default=str))
    
    print(f"\n📊 Result Keys:")
    for key, value in result.items():
        print(f"  {key}: {type(value)} = {value}")

if __name__ == "__main__":
    debug_agent() 