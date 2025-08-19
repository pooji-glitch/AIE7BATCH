"""
LangGraph Graph that uses the A2A application through the A2A protocol.

This graph acts as a client that can communicate with the A2A agent server
by making API calls through the standardized A2A protocol.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Dict, Any, Annotated, TypedDict, List
from uuid import uuid4

import httpx
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
)
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class A2AClientState(TypedDict):
    """State schema for the A2A client graph."""
    messages: Annotated[List, add_messages]
    a2a_response: str
    task_id: str
    context_id: str
    is_complete: bool


class A2AClientGraph:
    """LangGraph Graph that communicates with A2A agent server."""
    
    def __init__(self, a2a_server_url: str = "http://localhost:10000"):
        self.a2a_server_url = a2a_server_url
        self.client = None
        self.agent_card = None
        self.httpx_client = None
        
    async def initialize_client(self):
        """Initialize the A2A client and fetch agent card."""
        if not self.httpx_client:
            self.httpx_client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))
        
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=self.httpx_client,
            base_url=self.a2a_server_url,
        )
        
        # Fetch the agent card
        self.agent_card = await resolver.get_agent_card()
        logger.info(f"Fetched agent card: {self.agent_card.name}")
        
        # Initialize A2A client
        self.client = A2AClient(
            httpx_client=self.httpx_client,
            agent_card=self.agent_card
        )
        logger.info("A2A client initialized successfully")
    
    def prepare_a2a_request(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the A2A request from the current state."""
        # Get the latest user message
        messages = state["messages"]
        latest_message = messages[-1]
        
        if isinstance(latest_message, HumanMessage):
            user_query = latest_message.content
        else:
            user_query = "Please provide a query"
        
        # Prepare the A2A message payload
        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': user_query}
                ],
                'message_id': uuid4().hex,
            },
        }
        
        # Add task_id and context_id if they exist (for multi-turn conversations)
        if state.get("task_id") and state.get("context_id"):
            send_message_payload['message']['task_id'] = state["task_id"]
            send_message_payload['message']['context_id'] = state["context_id"]
        
        return {
            "a2a_request": send_message_payload,
            "user_query": user_query
        }
    
    async def call_a2a_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Make API call to the A2A agent server."""
        if not self.client:
            await self.initialize_client()
        
        # Prepare the request
        request_data = self.prepare_a2a_request(state)
        send_message_payload = request_data["a2a_request"]
        
        # Create the A2A request
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload)
        )
        
        try:
            # Send the message to the A2A agent
            logger.info(f"Sending query to A2A agent: {request_data['user_query']}")
            response = await self.client.send_message(request)
            
            # Extract response data
            result = response.root.result
            task_id = result.id
            context_id = result.context_id
            
            # Initialize response content
            a2a_response = "Response received from A2A agent"
            
            # Get the response content
            if hasattr(result, 'artifacts') and result.artifacts:
                # Extract content from artifacts
                for artifact in result.artifacts:
                    if hasattr(artifact, 'parts') and artifact.parts:
                        for part in artifact.parts:
                            if hasattr(part, 'text'):
                                a2a_response = part.text
                                break
                        if a2a_response and a2a_response != "Response received from A2A agent":
                            break
            
            logger.info(f"Received response from A2A agent. Task ID: {task_id}")
            
            return {
                "a2a_response": a2a_response,
                "task_id": task_id,
                "context_id": context_id,
                "is_complete": True
            }
            
        except Exception as e:
            logger.error(f"Error calling A2A agent: {e}")
            return {
                "a2a_response": f"Error: {str(e)}",
                "task_id": "",
                "context_id": "",
                "is_complete": True
            }
    
    def format_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Format the A2A response for the user."""
        a2a_response = state.get("a2a_response", "No response received")
        
        # Create a formatted response message
        formatted_response = f"""
🤖 A2A Agent Response:

{a2a_response}

---
*Response provided by A2A agent at {self.a2a_server_url}*
"""
        
        return {
            "messages": [AIMessage(content=formatted_response)]
        }
    
    def should_continue(self, state: Dict[str, Any]) -> str:
        """Decide whether to continue or end the graph."""
        if state.get("is_complete", False):
            return "end"
        return "continue"
    
    def build_graph(self):
        """Build the LangGraph for A2A client communication."""
        # Create the graph
        workflow = StateGraph(A2AClientState)
        
        # Add nodes
        workflow.add_node("call_a2a_agent", self.call_a2a_agent)
        workflow.add_node("format_response", self.format_response)
        
        # Add edges
        workflow.add_edge("call_a2a_agent", "format_response")
        workflow.add_edge("format_response", END)
        
        # Set entry point
        workflow.set_entry_point("call_a2a_agent")
        
        return workflow.compile()
    
    async def close(self):
        """Close the HTTP client."""
        if self.httpx_client:
            await self.httpx_client.aclose()


# Convenience function to create and use the A2A client graph
async def create_a2a_client_graph(server_url: str = "http://localhost:10000"):
    """Create and return an initialized A2A client graph."""
    graph_instance = A2AClientGraph(server_url)
    graph = graph_instance.build_graph()
    return graph_instance, graph


# Example usage function
async def example_usage():
    """Example of how to use the A2A client graph."""
    # Create the graph
    graph_instance, graph = await create_a2a_client_graph()
    
    # Example queries to test
    test_queries = [
        "What are the latest developments in artificial intelligence?",
        "Find me recent papers on transformer architectures",
        "Search for information about machine learning trends in 2024"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "a2a_response": "",
            "task_id": "",
            "context_id": "",
            "is_complete": False
        }
        
        # Run the graph
        try:
            result = await graph.ainvoke(initial_state)
            print("Response:", result["messages"][-1].content)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Run the example
    asyncio.run(example_usage())
