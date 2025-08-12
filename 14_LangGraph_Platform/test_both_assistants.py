#!/usr/bin/env python3
"""
Test script to compare both LangGraph assistants.

This script demonstrates the differences between the simple agent
and the agent with helpfulness evaluation.
"""

import time
from langgraph_sdk import get_sync_client

def test_simple_agent():
    """Test the simple agent with a complex query."""
    print("=" * 60)
    print("TESTING SIMPLE AGENT")
    print("=" * 60)
    
    client = get_sync_client(url="http://localhost:2024")
    
    query = "What is the MuonClip optimizer and what paper did it first appear in?"
    print(f"Query: {query}")
    print("-" * 40)
    
    start_time = time.time()
    
    try:
        result = client.runs.invoke(
            None,  # Threadless run
            "simple_agent",  # Assistant id
            input={
                "messages": [
                    {
                        "role": "human",
                        "content": query
                    }
                ]
            }
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Response time: {duration:.2f} seconds")
        print(f"📊 Message count: {len(result.messages)}")
        
        if result.messages:
            response = result.messages[-1].content
            print(f"💬 Response: {response[:300]}...")
            
            # Analyze response quality
            if "MuonClip" in response and "optimizer" in response:
                print("✅ Response contains key terms")
            else:
                print("⚠️  Response may be incomplete")
                
        else:
            print("❌ No response received")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_helpful_agent():
    """Test the agent with helpfulness evaluation."""
    print("\n" + "=" * 60)
    print("TESTING HELPFUL AGENT")
    print("=" * 60)
    
    client = get_sync_client(url="http://localhost:2024")
    
    query = "What is the MuonClip optimizer and what paper did it first appear in?"
    print(f"Query: {query}")
    print("-" * 40)
    
    start_time = time.time()
    
    try:
        result = client.runs.invoke(
            None,  # Threadless run
            "agent_helpful",  # Assistant id
            input={
                "messages": [
                    {
                        "role": "human",
                        "content": query
                    }
                ]
            }
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Response time: {duration:.2f} seconds")
        print(f"📊 Message count: {len(result.messages)}")
        
        if result.messages:
            response = result.messages[-1].content
            print(f"💬 Final Response: {response[:300]}...")
            
            # Check for helpfulness evaluation
            helpfulness_messages = []
            for msg in result.messages:
                content = getattr(msg, 'content', '')
                if "HELPFULNESS:" in content:
                    helpfulness_messages.append(content)
            
            if helpfulness_messages:
                print(f"🔍 Helpfulness evaluations: {len(helpfulness_messages)}")
                for i, eval_msg in enumerate(helpfulness_messages, 1):
                    print(f"   {i}. {eval_msg}")
            
            # Analyze response quality
            if "MuonClip" in response and "optimizer" in response:
                print("✅ Response contains key terms")
            else:
                print("⚠️  Response may be incomplete")
                
        else:
            print("❌ No response received")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def compare_performance():
    """Compare performance metrics between both agents."""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    client = get_sync_client(url="http://localhost:2024")
    
    test_queries = [
        "What is the MuonClip optimizer?",
        "Explain the Federal Pell Grant Program",
        "How does the Direct Loan Program work?"
    ]
    
    simple_times = []
    helpful_times = []
    simple_messages = []
    helpful_messages = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: {query}")
        print("-" * 30)
        
        # Test simple agent
        start_time = time.time()
        try:
            result_simple = client.runs.invoke(
                None, "simple_agent",
                input={"messages": [{"role": "human", "content": query}]}
            )
            simple_time = time.time() - start_time
            simple_times.append(simple_time)
            simple_messages.append(len(result_simple.messages))
            print(f"   Simple Agent: {simple_time:.2f}s, {len(result_simple.messages)} messages")
        except Exception as e:
            print(f"   Simple Agent Error: {e}")
        
        # Test helpful agent
        start_time = time.time()
        try:
            result_helpful = client.runs.invoke(
                None, "agent_helpful",
                input={"messages": [{"role": "human", "content": query}]}
            )
            helpful_time = time.time() - start_time
            helpful_times.append(helpful_time)
            helpful_messages.append(len(result_helpful.messages))
            print(f"   Helpful Agent: {helpful_time:.2f}s, {len(result_helpful.messages)} messages")
        except Exception as e:
            print(f"   Helpful Agent Error: {e}")
    
    # Calculate averages
    if simple_times:
        avg_simple_time = sum(simple_times) / len(simple_times)
        avg_simple_messages = sum(simple_messages) / len(simple_messages)
        print(f"\n📈 Simple Agent Averages:")
        print(f"   Time: {avg_simple_time:.2f}s")
        print(f"   Messages: {avg_simple_messages:.1f}")
    
    if helpful_times:
        avg_helpful_time = sum(helpful_times) / len(helpful_times)
        avg_helpful_messages = sum(helpful_messages) / len(helpful_messages)
        print(f"\n📈 Helpful Agent Averages:")
        print(f"   Time: {avg_helpful_time:.2f}s")
        print(f"   Messages: {avg_helpful_messages:.1f}")
        
        if simple_times:
            time_ratio = avg_helpful_time / avg_simple_time
            message_ratio = avg_helpful_messages / avg_simple_messages
            print(f"\n📊 Comparison:")
            print(f"   Time ratio: {time_ratio:.2f}x slower")
            print(f"   Message ratio: {message_ratio:.2f}x more messages")

def main():
    """Run all tests."""
    print("LangGraph Assistant Comparison Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        client = get_sync_client(url="http://localhost:2024")
        # Try a simple ping
        client.runs.invoke(None, "simple_agent", input={"messages": [{"role": "human", "content": "test"}]})
        print("✅ LangGraph server is running")
    except Exception as e:
        print("❌ Error: LangGraph server not running or not accessible")
        print("Please start the server with: langgraph dev")
        print(f"Error details: {e}")
        return
    
    # Run tests
    test_simple_agent()
    test_helpful_agent()
    compare_performance()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)
    print("\nKey Findings:")
    print("• Simple agent: Faster, fewer messages, no quality control")
    print("• Helpful agent: Slower, more messages, built-in quality evaluation")
    print("• Helpful agent may iterate multiple times to improve response quality")
    print("• Both agents use the same tools but differ in evaluation strategy")

if __name__ == "__main__":
    main()
