#!/usr/bin/env python3
"""
Simple test script to check if the Tesla Investment Tracker app components work.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_data_loading():
    """Test if data can be loaded properly."""
    try:
        import pandas as pd
        
        # Test loading each data file
        data_files = [
            "data/tesla_financial_metrics.csv",
            "data/market_sentiment_data.csv", 
            "data/tesla_research_papers.csv",
            "data/competitor_analysis.csv",
            "data/tesla_product_reviews.json"
        ]
        
        for file_path in data_files:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                print(f"✅ Loaded {file_path}: {len(df)} rows")
            elif file_path.endswith('.json'):
                import json
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(f"✅ Loaded {file_path}: {len(data.get('tesla_products', []))} products")
        
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_agent_initialization():
    """Test if the agent can be initialized (without API calls)."""
    try:
        from agentic_rag_bm25 import AgenticRAGBM25
        
        # Create agent without initializing LLM
        agent = AgenticRAGBM25()
        
        # Load data
        documents = agent.load_tesla_data()
        print(f"✅ Agent initialized with {len(documents)} documents")
        
        # Create retriever
        retriever = agent.create_bm25_retriever()
        print("✅ BM25 retriever created")
        
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_api_keys():
    """Test if required API keys are set."""
    required_keys = ['OPENAI_API_KEY']
    optional_keys = ['TAVILY_API_KEY']
    
    print("\n🔑 API Key Status:")
    
    for key in required_keys:
        if os.getenv(key):
            print(f"✅ {key}: Set")
        else:
            print(f"❌ {key}: Not set (REQUIRED)")
    
    for key in optional_keys:
        if os.getenv(key):
            print(f"✅ {key}: Set")
        else:
            print(f"⚠️ {key}: Not set (optional)")
    
    return all(os.getenv(key) for key in required_keys)

def main():
    """Run all tests."""
    print("🧪 Testing Tesla Investment Tracker Components...\n")
    
    # Test 1: Data loading
    print("1. Testing data loading...")
    data_ok = test_data_loading()
    
    # Test 2: Agent initialization
    print("\n2. Testing agent initialization...")
    agent_ok = test_agent_initialization()
    
    # Test 3: API keys
    print("\n3. Testing API keys...")
    keys_ok = test_api_keys()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY:")
    print(f"Data Loading: {'✅ PASS' if data_ok else '❌ FAIL'}")
    print(f"Agent Init: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    print(f"API Keys: {'✅ PASS' if keys_ok else '❌ FAIL'}")
    
    if data_ok and agent_ok and keys_ok:
        print("\n🎉 All tests passed! Your app should work.")
        print("\nTo start the app:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        print("2. Run: python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
        
        if not keys_ok:
            print("\nTo set API keys:")
            print("export OPENAI_API_KEY='your-openai-api-key'")
            print("export TAVILY_API_KEY='your-tavily-api-key' (optional)")

if __name__ == "__main__":
    main() 