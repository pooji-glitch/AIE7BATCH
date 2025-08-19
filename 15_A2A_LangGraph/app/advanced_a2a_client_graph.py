"""
Advanced LangGraph Graph that uses the A2A application with multi-turn conversations.

This graph provides a more sophisticated client that can handle:
- Multi-turn conversations
- Streaming responses
- Error handling and retry logic
- Conversation state management
"""
from __future__ import annotations

import asyncio
import logging
from typing import Dict, Any, Annotated, TypedDict, List, Optional
from uuid import uuid4

import httpx
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
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


class AdvancedA2AClientState(TypedDict):
    """Advanced state schema for the A2A client graph with conversation management."""
    messages: Annotated[List, add_messages]
    a2a_response: str
    task_id: str
    context_id: str
    is_complete: bool
    conversation_history: List[Dict[str, Any]]
    error_count: int
    max_retries: int


class AdvancedA2AClientGraph:
    """Advanced LangGraph Graph that communicates with A2A agent server with conversation management."""
    
    def __init__(self, a2a_server_url: str = "http://localhost:10000", max_retries: int = 3):
        self.a2a_server_url = a2a_server_url
        self.max_retries = max_retries
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
        logger.info("Advanced A2A client initialized successfully")
    
    def prepare_a2a_request(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the A2A request from the current state with conversation context."""
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
        """Make API call to the A2A agent server with retry logic."""
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
        
        error_count = state.get("error_count", 0)
        
        for attempt in range(self.max_retries):
            try:
                # Send the message to the A2A agent
                logger.info(f"Sending query to A2A agent (attempt {attempt + 1}): {request_data['user_query']}")
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
                
                # Update conversation history
                conversation_entry = {
                    "query": request_data["user_query"],
                    "response": a2a_response,
                    "task_id": task_id,
                    "context_id": context_id,
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                return {
                    "a2a_response": a2a_response,
                    "task_id": task_id,
                    "context_id": context_id,
                    "is_complete": True,
                    "error_count": 0,
                    "conversation_history": state.get("conversation_history", []) + [conversation_entry]
                }
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error calling A2A agent (attempt {attempt + 1}): {e}")
                
                if attempt == self.max_retries - 1:
                    # Final attempt failed
                    return {
                        "a2a_response": f"Error after {self.max_retries} attempts: {str(e)}",
                        "task_id": "",
                        "context_id": "",
                        "is_complete": True,
                        "error_count": error_count,
                        "conversation_history": state.get("conversation_history", [])
                    }
                
                # Wait before retry
                await asyncio.sleep(1 * (attempt + 1))
    
    async def call_a2a_agent_streaming(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Make streaming API call to the A2A agent server."""
        if not self.client:
            await self.initialize_client()
        
        # Prepare the request
        request_data = self.prepare_a2a_request(state)
        send_message_payload = request_data["a2a_request"]
        
        # Create the streaming A2A request
        streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload)
        )
        
        try:
            logger.info(f"Sending streaming query to A2A agent: {request_data['user_query']}")
            
            # Get the streaming response
            stream_response = self.client.send_message_streaming(streaming_request)
            
            # Collect streaming chunks
            full_response = ""
            task_id = ""
            context_id = ""
            
            async for chunk in stream_response:
                # Process each chunk
                if hasattr(chunk, 'root') and chunk.root:
                    if hasattr(chunk.root, 'result'):
                        result = chunk.root.result
                        if hasattr(result, 'id'):
                            task_id = result.id
                        if hasattr(result, 'context_id'):
                            context_id = result.context_id
                        if hasattr(result, 'content'):
                            full_response += result.content
            
            logger.info(f"Completed streaming response from A2A agent. Task ID: {task_id}")
            
            return {
                "a2a_response": full_response or "Streaming response completed",
                "task_id": task_id,
                "context_id": context_id,
                "is_complete": True,
                "error_count": 0
            }
            
        except Exception as e:
            logger.error(f"Error in streaming call to A2A agent: {e}")
            return {
                "a2a_response": f"Streaming error: {str(e)}",
                "task_id": "",
                "context_id": "",
                "is_complete": True,
                "error_count": state.get("error_count", 0) + 1
            }
    
    def format_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Format the A2A response for the user with conversation context."""
        a2a_response = state.get("a2a_response", "No response received")
        conversation_history = state.get("conversation_history", [])
        
        # Create a formatted response message
        formatted_response = f"""
🤖 A2A Agent Response:

{a2a_response}

---
*Response provided by A2A agent at {self.a2a_server_url}*
"""
        
        # Add conversation summary if there's history
        if conversation_history:
            formatted_response += f"\n📝 Conversation History ({len(conversation_history)} exchanges):\n"
            for i, entry in enumerate(conversation_history[-3:], 1):  # Show last 3 exchanges
                formatted_response += f"{i}. Q: {entry['query'][:50]}...\n"
        
        return {
            "messages": [AIMessage(content=formatted_response)]
        }
    
    def decide_response_type(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Decide whether to use regular or streaming response."""
        # For now, always use regular response
        # You could add logic here to decide based on query type or user preference
        return {"response_type": "regular"}
    
    def should_continue(self, state: Dict[str, Any]) -> str:
        """Decide whether to continue or end the graph."""
        if state.get("is_complete", False):
            return "end"
        return "continue"
    
    def build_graph(self):
        """Build the advanced LangGraph for A2A client communication."""
        # Create the graph
        workflow = StateGraph(AdvancedA2AClientState)
        
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


# Convenience function to create and use the advanced A2A client graph
async def create_advanced_a2a_client_graph(server_url: str = "http://localhost:10000", max_retries: int = 3):
    """Create and return an initialized advanced A2A client graph."""
    graph_instance = AdvancedA2AClientGraph(server_url, max_retries)
    graph = graph_instance.build_graph()
    return graph_instance, graph


# Example usage function with multi-turn conversation
async def example_multi_turn_conversation():
    """Example of multi-turn conversation using the advanced A2A client graph."""
    # Create the graph
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
        print(f"\n{'='*60}")
        print(f"Turn {i}: {query}")
        print(f"{'='*60}")
        
        # Add the new query to messages
        current_state["messages"] = [HumanMessage(content=query)]
        
        # Run the graph
        try:
            result = await graph.ainvoke(current_state)
            
            # Update state for next turn
            current_state.update({
                "task_id": result.get("task_id", ""),
                "context_id": result.get("context_id", ""),
                "conversation_history": result.get("conversation_history", [])
            })
            
            print("Response:", result["messages"][-1].content)
            
        except Exception as e:
            print(f"Error in turn {i}: {e}")
    
    # Close the client
    await graph_instance.close()


if __name__ == "__main__":
    # Run the multi-turn conversation example
    asyncio.run(example_multi_turn_conversation())
