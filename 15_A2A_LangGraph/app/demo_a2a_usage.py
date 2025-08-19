"""
Demo: How to Build a LangGraph Graph to "Use" Your A2A Application

This script demonstrates exactly what you need to do to accomplish the task:
"Build a LangGraph Graph to 'use' your application by creating a Simple Agent 
that can make API calls to the 🤖Agent Node above through the A2A protocol."
"""
import asyncio
import logging
from langchain_core.messages import HumanMessage

# Import our A2A client graphs
from app.a2a_client_graph import create_a2a_client_graph
from app.advanced_a2a_client_graph import create_advanced_a2a_client_graph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demonstrate_basic_usage():
    """
    Demonstrate the basic A2A client graph - this is what you need to do!
    """
    print("\n" + "="*80)
    print("🎯 DEMO: Building a LangGraph Graph to 'Use' Your A2A Application")
    print("="*80)
    
    print("\n📋 TASK: Build a LangGraph Graph to 'use' your application")
    print("   by creating a Simple Agent that can make API calls to the 🤖Agent Node")
    print("   through the A2A protocol.")
    
    print("\n✅ SOLUTION: We've created LangGraph graphs that act as clients!")
    
    # Step 1: Create the A2A client graph
    print("\n🔧 Step 1: Create the A2A client graph")
    print("   graph_instance, graph = await create_a2a_client_graph()")
    
    try:
        graph_instance, graph = await create_a2a_client_graph()
        print("   ✅ Graph created successfully!")
        
        # Step 2: Prepare a query
        print("\n🔧 Step 2: Prepare a query")
        query = "What are the latest developments in artificial intelligence?"
        print(f"   Query: '{query}'")
        
        # Step 3: Initialize state
        print("\n🔧 Step 3: Initialize state")
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "a2a_response": "",
            "task_id": "",
            "context_id": "",
            "is_complete": False
        }
        print("   ✅ State initialized with user message")
        
        # Step 4: Run the graph (this makes the API call to your A2A agent!)
        print("\n🔧 Step 4: Run the graph (makes API call to your 🤖Agent Node)")
        print("   result = await graph.ainvoke(initial_state)")
        
        result = await graph.ainvoke(initial_state)
        print("   ✅ API call successful! Response received from your A2A agent.")
        
        # Step 5: Display the result
        print("\n🔧 Step 5: Display the result")
        response_content = result["messages"][-1].content
        print(f"   Response preview: {response_content[:200]}...")
        
        print("\n🎉 SUCCESS! Your LangGraph Graph successfully 'used' your A2A application!")
        print("   The graph made an API call to your 🤖Agent Node through the A2A protocol.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure your A2A agent server is running on http://localhost:10000")


async def demonstrate_advanced_usage():
    """
    Demonstrate the advanced A2A client graph with multi-turn conversations.
    """
    print("\n" + "="*80)
    print("🚀 ADVANCED DEMO: Multi-turn Conversation with A2A Protocol")
    print("="*80)
    
    print("\n📋 ADVANCED FEATURE: Multi-turn conversations with your A2A agent")
    
    try:
        # Create the advanced graph
        graph_instance, graph = await create_advanced_a2a_client_graph()
        print("   ✅ Advanced graph created successfully!")
        
        # Multi-turn conversation
        conversation_queries = [
            "What are the latest developments in artificial intelligence?",
            "Can you find me recent papers on transformer architectures?",
            "Summarize the key findings from those papers"
        ]
        
        # Initialize state for the conversation
        current_state = {
            "messages": [],
            "a2a_response": "",
            "task_id": "",
            "context_id": "",
            "is_complete": False,
            "conversation_history": [],
            "error_count": 0,
            "max_retries": 3
        }
        
        print(f"\n🔄 Starting multi-turn conversation ({len(conversation_queries)} turns)")
        
        for i, query in enumerate(conversation_queries, 1):
            print(f"\n   Turn {i}: '{query}'")
            
            # Add the new query to messages
            current_state["messages"] = [HumanMessage(content=query)]
            
            # Run the graph (API call to your A2A agent)
            result = await graph.ainvoke(current_state)
            
            # Update state for next turn
            current_state.update({
                "task_id": result.get("task_id", ""),
                "context_id": result.get("context_id", ""),
                "conversation_history": result.get("conversation_history", [])
            })
            
            print(f"   ✅ Response received (Task ID: {result.get('task_id', 'N/A')})")
        
        # Close the client
        await graph_instance.close()
        print("\n🎉 Multi-turn conversation completed successfully!")
        print("   Your LangGraph maintained conversation context across multiple API calls.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def show_what_we_accomplished():
    """
    Show a summary of what we accomplished.
    """
    print("\n" + "="*80)
    print("📊 SUMMARY: What We Accomplished")
    print("="*80)
    
    print("\n🎯 ORIGINAL TASK:")
    print("   'Build a LangGraph Graph to \"use\" your application'")
    print("   'by creating a Simple Agent that can make API calls to the 🤖Agent Node'")
    print("   'through the A2A protocol'")
    
    print("\n✅ WHAT WE BUILT:")
    print("   1. Basic A2A Client Graph (a2a_client_graph.py)")
    print("      - Simple LangGraph that communicates with your A2A agent server")
    print("      - Handles basic request/response cycles")
    print("      - Demonstrates A2A protocol integration")
    
    print("\n   2. Advanced A2A Client Graph (advanced_a2a_client_graph.py)")
    print("      - Multi-turn conversation support")
    print("      - Streaming response handling")
    print("      - Error handling and retry logic")
    print("      - Conversation state management")
    
    print("\n   3. Test Script (test_a2a_client_graphs.py)")
    print("      - Comprehensive testing of both graphs")
    print("      - Demonstrates usage patterns")
    print("      - Error handling validation")
    
    print("\n🔧 KEY COMPONENTS:")
    print("   - A2ACardResolver: Discovers your agent's capabilities")
    print("   - A2AClient: Makes API calls to your agent server")
    print("   - LangGraph State Management: Manages conversation flow")
    print("   - Error Handling: Robust retry logic and error recovery")
    
    print("\n🌐 A2A PROTOCOL INTEGRATION:")
    print("   - Agent Card Discovery: Fetches your agent's capabilities")
    print("   - Message Sending: Sends queries through A2A protocol")
    print("   - Response Processing: Handles A2A protocol responses")
    print("   - Multi-turn Support: Maintains conversation context")
    
    print("\n🎉 RESULT:")
    print("   Your LangGraph Graph successfully 'uses' your A2A application!")
    print("   It can make API calls to your 🤖Agent Node through the A2A protocol.")
    print("   It supports both single queries and multi-turn conversations.")


async def main():
    """
    Run the complete demonstration.
    """
    print("🤖 A2A Client Graph Demonstration")
    print("This shows how to build a LangGraph Graph to 'use' your A2A application")
    
    # Show what we accomplished
    await show_what_we_accomplished()
    
    # Demonstrate basic usage
    await demonstrate_basic_usage()
    
    # Demonstrate advanced usage
    await demonstrate_advanced_usage()
    
    print("\n" + "="*80)
    print("🎯 TASK COMPLETED!")
    print("="*80)
    print("You now have LangGraph Graphs that can 'use' your A2A application!")
    print("They make API calls to your 🤖Agent Node through the A2A protocol.")
    print("\nTo run the tests:")
    print("  uv run python app/test_a2a_client_graphs.py")


if __name__ == "__main__":
    asyncio.run(main())
