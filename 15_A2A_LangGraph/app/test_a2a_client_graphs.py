"""
Test script for A2A Client Graphs.

This script demonstrates how to use both the basic and advanced A2A client graphs
to communicate with the A2A agent server.
"""
import asyncio
import logging
from langchain_core.messages import HumanMessage

from app.a2a_client_graph import create_a2a_client_graph
from app.advanced_a2a_client_graph import create_advanced_a2a_client_graph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_basic_a2a_client_graph():
    """Test the basic A2A client graph."""
    print("\n" + "="*60)
    print("🧪 Testing Basic A2A Client Graph")
    print("="*60)
    
    try:
        # Create the basic graph
        graph_instance, graph = await create_a2a_client_graph()
        
        # Test queries
        test_queries = [
            "What are the latest developments in artificial intelligence?",
            "Find me recent papers on transformer architectures"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- Test Query {i} ---")
            print(f"Query: {query}")
            
            # Initialize state
            initial_state = {
                "messages": [HumanMessage(content=query)],
                "a2a_response": "",
                "task_id": "",
                "context_id": "",
                "is_complete": False
            }
            
            # Run the graph
            result = await graph.ainvoke(initial_state)
            print("✅ Response received successfully!")
            print(f"Response preview: {result['messages'][-1].content[:200]}...")
        
        print("\n✅ Basic A2A Client Graph test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in basic A2A client graph test: {e}")
        logger.error(f"Basic A2A client graph test failed: {e}", exc_info=True)


async def test_advanced_a2a_client_graph():
    """Test the advanced A2A client graph with multi-turn conversation."""
    print("\n" + "="*60)
    print("🚀 Testing Advanced A2A Client Graph")
    print("="*60)
    
    try:
        # Create the advanced graph
        graph_instance, graph = await create_advanced_a2a_client_graph()
        
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
        
        for i, query in enumerate(conversation_queries, 1):
            print(f"\n--- Turn {i} ---")
            print(f"Query: {query}")
            
            # Add the new query to messages
            current_state["messages"] = [HumanMessage(content=query)]
            
            # Run the graph
            result = await graph.ainvoke(current_state)
            
            # Update state for next turn
            current_state.update({
                "task_id": result.get("task_id", ""),
                "context_id": result.get("context_id", ""),
                "conversation_history": result.get("conversation_history", [])
            })
            
            print("✅ Response received successfully!")
            print(f"Response preview: {result['messages'][-1].content[:200]}...")
            print(f"Task ID: {result.get('task_id', 'N/A')}")
            print(f"Context ID: {result.get('context_id', 'N/A')}")
        
        # Close the client
        await graph_instance.close()
        print("\n✅ Advanced A2A Client Graph test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in advanced A2A client graph test: {e}")
        logger.error(f"Advanced A2A client graph test failed: {e}", exc_info=True)


async def test_error_handling():
    """Test error handling with invalid server URL."""
    print("\n" + "="*60)
    print("🛡️ Testing Error Handling")
    print("="*60)
    
    try:
        # Try to connect to a non-existent server
        graph_instance, graph = await create_a2a_client_graph("http://localhost:9999")
        
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content="Test query")],
            "a2a_response": "",
            "task_id": "",
            "context_id": "",
            "is_complete": False
        }
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        print("Response:", result['messages'][-1].content)
        
    except Exception as e:
        print(f"✅ Error handling test passed - expected error: {e}")


async def main():
    """Run all tests."""
    print("🧪 Starting A2A Client Graph Tests")
    print("Make sure your A2A agent server is running on http://localhost:10000")
    
    # Test basic graph
    await test_basic_a2a_client_graph()
    
    # Test advanced graph
    await test_advanced_a2a_client_graph()
    
    # Test error handling
    await test_error_handling()
    
    print("\n" + "="*60)
    print("🎉 All tests completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
