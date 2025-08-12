#!/usr/bin/env python3
"""
Test script to demonstrate RAG and LangGraph concepts.

This script tests the RAG system and both agent types to showcase
the differences in behavior and performance.
"""

import os
import sys
from typing import Dict, Any
from langgraph_sdk import get_sync_client

def test_rag_system():
    """Test the RAG system with different queries."""
    print("=" * 60)
    print("TESTING RAG SYSTEM")
    print("=" * 60)
    
    # Test queries that demonstrate chunk overlap and retrieval concepts
    test_queries = [
        "What is the Federal Pell Grant Program?",
        "How does the Direct Loan Program work?",
        "What are the academic calendar requirements?",
        "Explain the cost of attendance and packaging process"
    ]
    
    client = get_sync_client(url="http://localhost:2024")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 40)
        
        try:
            # Test with simple agent first
            result = client.runs.invoke(
                None,  # Threadless run
                "simple_agent",  # Assistant id
                input={
                    "messages": [
                        {
                            "role": "human",
                            "content": f"Use the retrieve_information tool to answer: {query}"
                        }
                    ]
                }
            )
            
            # Extract the response
            if hasattr(result, 'messages') and result.messages:
                response = result.messages[-1].content
                print(f"Response: {response[:200]}...")
            else:
                print("No response received")
                
        except Exception as e:
            print(f"Error: {e}")

def test_agent_comparison():
    """Compare the behavior of simple agent vs helpful agent."""
    print("\n" + "=" * 60)
    print("COMPARING AGENT BEHAVIORS")
    print("=" * 60)
    
    test_query = "What is the MuonClip optimizer and what paper did it first appear in?"
    
    client = get_sync_client(url="http://localhost:2024")
    
    # Test simple agent
    print(f"\n1. Testing Simple Agent")
    print("-" * 40)
    print(f"Query: {test_query}")
    
    try:
        result_simple = client.runs.invoke(
            None,
            "simple_agent",
            input={
                "messages": [
                    {
                        "role": "human",
                        "content": test_query
                    }
                ]
            }
        )
        
        if hasattr(result_simple, 'messages') and result_simple.messages:
            response = result_simple.messages[-1].content
            print(f"Simple Agent Response: {response[:300]}...")
            print(f"Message count: {len(result_simple.messages)}")
        else:
            print("No response from simple agent")
            
    except Exception as e:
        print(f"Error with simple agent: {e}")
    
    # Test helpful agent
    print(f"\n2. Testing Helpful Agent")
    print("-" * 40)
    print(f"Query: {test_query}")
    
    try:
        result_helpful = client.runs.invoke(
            None,
            "agent_helpful",
            input={
                "messages": [
                    {
                        "role": "human",
                        "content": test_query
                    }
                ]
            }
        )
        
        if hasattr(result_helpful, 'messages') and result_helpful.messages:
            response = result_helpful.messages[-1].content
            print(f"Helpful Agent Response: {response[:300]}...")
            print(f"Message count: {len(result_helpful.messages)}")
            
            # Check for helpfulness evaluation messages
            helpfulness_messages = [
                msg.content for msg in result_helpful.messages 
                if "HELPFULNESS:" in getattr(msg, 'content', '')
            ]
            if helpfulness_messages:
                print(f"Helpfulness evaluations: {helpfulness_messages}")
        else:
            print("No response from helpful agent")
            
    except Exception as e:
        print(f"Error with helpful agent: {e}")

def test_chunk_overlap_concept():
    """Demonstrate chunk overlap concept with RAG queries."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING CHUNK OVERLAP CONCEPTS")
    print("=" * 60)
    
    # Queries designed to test chunk boundary issues
    boundary_queries = [
        "What are the eligibility requirements and application process for federal student aid?",
        "Explain the relationship between cost of attendance, packaging, and verification procedures",
        "How do academic calendars affect loan disbursement and grant timing?"
    ]
    
    client = get_sync_client(url="http://localhost:2024")
    
    for i, query in enumerate(boundary_queries, 1):
        print(f"\n{i}. Boundary Test Query: {query}")
        print("-" * 50)
        
        try:
            result = client.runs.invoke(
                None,
                "simple_agent",
                input={
                    "messages": [
                        {
                            "role": "human",
                            "content": f"Use retrieve_information to answer: {query}"
                        }
                    ]
                }
            )
            
            if hasattr(result, 'messages') and result.messages:
                response = result.messages[-1].content
                print(f"Response: {response[:250]}...")
                
                # Analyze response completeness
                if "I don't know" in response or "not contained" in response:
                    print("⚠️  Potential chunk boundary issue detected")
                else:
                    print("✅ Response appears complete")
            else:
                print("No response received")
                
        except Exception as e:
            print(f"Error: {e}")

def test_retriever_k_parameter():
    """Demonstrate the effect of different k values on retrieval."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING RETRIEVER K PARAMETER EFFECTS")
    print("=" * 60)
    
    # Test with a complex query that might benefit from different k values
    complex_query = "What are all the different types of federal student aid available and how do they differ in terms of eligibility, amounts, and repayment requirements?"
    
    print(f"Complex Query: {complex_query}")
    print("-" * 50)
    
    client = get_sync_client(url="http://localhost:2024")
    
    try:
        result = client.runs.invoke(
            None,
            "simple_agent",
            input={
                "messages": [
                    {
                        "role": "human",
                        "content": f"Use retrieve_information to provide a comprehensive answer: {complex_query}"
                    }
                ]
            }
        )
        
        if hasattr(result, 'messages') and result.messages:
            response = result.messages[-1].content
            print(f"Response with k=5: {response[:400]}...")
            
            # Analyze response quality
            if len(response) > 500:
                print("✅ Comprehensive response (good recall)")
            else:
                print("⚠️  Potentially incomplete response (low recall)")
                
            if "federal" in response.lower() and "aid" in response.lower():
                print("✅ Relevant content found (good precision)")
            else:
                print("⚠️  May lack relevant content (low precision)")
        else:
            print("No response received")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests."""
    print("RAG and LangGraph Analysis Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        client = get_sync_client(url="http://localhost:2024")
        # Try a simple ping
        client.runs.invoke(None, "simple_agent", input={"messages": [{"role": "human", "content": "test"}]})
    except Exception as e:
        print("❌ Error: LangGraph server not running or not accessible")
        print("Please start the server with: langgraph dev")
        print(f"Error details: {e}")
        return
    
    print("✅ LangGraph server is running")
    
    # Run tests
    test_rag_system()
    test_agent_comparison()
    test_chunk_overlap_concept()
    test_retriever_k_parameter()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)
    print("\nKey Insights:")
    print("1. Chunk overlap affects context preservation across boundaries")
    print("2. Retriever k parameter balances precision vs recall")
    print("3. Helpful agent adds quality control but increases complexity")
    print("4. RAG performance depends on document chunking strategy")

if __name__ == "__main__":
    main()
