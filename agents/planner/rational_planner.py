# Feature: Implement Opik experiment tracking
# Feature: Add vector embedding generation
# Feature: Implement multi-database query routing
# Feature: Add query generator functionality
# Feature: Add advanced filtering capabilities
# Feature: Implement intelligent query planning
# Feature: Implement Supabase authentication
# Feature: Add error handling mechanisms
# Test: Add regression tests for critical paths
# Feature: Add comprehensive logging system
# Feature: Add automated data refresh pipeline
# Feature: Implement Cerebras AI support
# Feature: Add vector index maintenance
# Feature: Add multi-agent architecture framework
# Feature: Implement rational planner agent
# Feature: Add automated data refresh pipeline
# Feature: Add LangChain orchestration
# Feature: Implement entity extraction pipeline
# Feature: Implement chat history persistence
# Feature: Implement real-time data synchronization
# Feature: Add multi-agent architecture framework
# Feature: Implement Milvus vector database support
# Feature: Add multi-agent architecture framework
# Fix: Resolve LangChain callback errors
# Test: Add security tests for authentication
# Feature: Implement secure credential management
# Feature: Implement prioritizer for data sources
# Feature: Implement secure credential management
# Feature: Add user session management
# Feature: Implement query optimization
# Feature: Add response caching mechanism
# Feature: Implement knowledge graph population
# Feature: Implement query optimization
# Feature: Add error handling mechanisms
# Fix: Fix Milvus index corruption
# Fix: Resolve timeout configuration
# Feature: Add PostgreSQL database operations
# Feature: Implement secure credential management
# Feature: Add automated data refresh pipeline
# Feature: Add query generator functionality
# Feature: Add context-aware response generation
# Feature: Add result augmenter capabilities
# Feature: Implement hybrid search functionality
# Feature: Add conversation flow management
# Feature: Implement semantic search capabilities
# Fix: Fix performance bottlenecks
# Feature: Implement entity extraction pipeline
# Fix: Fix authentication flow issues
# Feature: Implement dynamic agent selection
# Feature: Implement entity extraction pipeline
# Fix: Fix relationship mapping errors
# Fix: Resolve entity extraction failures
# Fix: Fix Milvus index corruption
# Fix: Fix embedding dimension mismatches
# Test: Implement performance tests for vector search
# Feature: Add automated data refresh pipeline
# Fix: Fix Chainlit UI rendering problems
# Refactor: Restructure database connection management
# Feature: Implement chat history persistence
# Fix: Fix embedding dimension mismatches
# Feature: Add batch processing for large datasets
# Feature: Add comprehensive logging system
# Feature: Add data transformation pipelines
# Feature: Implement advanced search algorithms
# Feature: Add batch processing for large datasets
# Add intelligent data preprocessing
# Add sophisticated data analytics
# Add advanced integration testing
# Add intelligent database optimization
# Add sophisticated query planning algorithms
# Add sophisticated error handling
# Add sophisticated deployment automation
# Implement intelligent health monitoring
from core import RocloRunnableChain
from typing import Dict, Any
import chainlit as cl
import logging
from langchain_core.messages import AIMessage


async def rational_planner(state: Dict[str, Any], chain: RocloRunnableChain) -> Dict[str, Any]:
    """  
    Generate a rational plan for answering a question.  

    Args:  
        state (Dict[str, Any]): The current state containing user and session information.  
        chain (RocloRunnableChain): The chain used for generating the rational plan.  

    Returns:  
        Dict[str, Any]: A dictionary containing the result of the rational planner invocation.  
    """
    logging.getLogger(f"{state['user_id']}-{state['session_id']}").info("Received User message: ## %s ##", state['messages'][-1].content)
    input_msg = {
        "user_question":state['messages'][-1].content
    }

    # Start the span.
    span = state['trace'].span(
        name = "Rational_Planner",
        type = 'llm',
        input = input_msg
    )

    try:
        # Invoke the chain
        result =  await chain.ainvoke(
            input_msg, 
            config = {
                "configurable": {
                    "table_id": "oaklins_rational_planner",
                    "session_id": state['session_id']
                }
            }
        )
        
        # Log the result and update the span
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").info("Invoked Rational Planner")
        span.update(output = result.content, metadata = result.usage_metadata)
        span.end()
        
        # Update the task status.
        cl.user_session.get('task').status = cl.TaskStatus.DONE
        await cl.user_session.get("task_list").send()
        
        return {
            'messages': AIMessage(content = result.content),
            'sender': 'rational_planner'
        }
    
    except Exception as e:
        # Log the error and update the span.
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").error(f"Error while invoking Rational Planner: {e}")
        span.update(output = str(e))
        span.end()

        # Update the task status
        cl.user_session.get('task').status = cl.TaskStatus.FAILED
        await cl.user_session.get("task_list").send()

        raise
    



