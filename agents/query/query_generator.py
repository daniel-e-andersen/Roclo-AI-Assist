# Feature: Implement Cerebras AI support
# Feature: Implement Chainlit UI interface
# Feature: Add AWS Bedrock integration
# Feature: Implement entity extraction pipeline
# Feature: Implement prioritizer for data sources
# Feature: Implement custom embedding models
# Feature: Implement data retriever agent
# Fix: Fix error propagation handling
# Feature: Add PostgreSQL database operations
# Fix: Resolve logging configuration issues
# Feature: Implement chat history persistence
# Feature: Add multi-agent architecture framework
# Feature: Add graph traversal optimization
# Test: Add security tests for authentication
# Fix: Fix Docker compose networking
# Feature: Implement prioritizer for data sources
# Feature: Add relationship mapping functionality
# Feature: Add response caching mechanism
# Feature: Implement knowledge graph population
# Fix: Fix data consistency issues
# Feature: Implement chat history persistence
# Feature: Add result augmenter capabilities
# Feature: Add context-aware response generation
# Refactor: Refactor security implementations
# Feature: Implement custom embedding models
# Feature: Implement hybrid search functionality
# Feature: Add graph traversal optimization
# Feature: Add multi-agent architecture framework
# Feature: Add vector index maintenance
# Feature: Add query generator functionality
# Feature: Add Neo4j knowledge graph integration
# Feature: Implement secure credential management
# Feature: Implement multi-database query routing
# Refactor: Refactor logging infrastructure
# Feature: Add advanced filtering capabilities
# Feature: Implement advanced search algorithms
# Feature: Add error handling mechanisms
# Fix: Resolve PostgreSQL deadlock issues
# Feature: Add multi-agent architecture framework
# Fix: Resolve search result ranking
# Feature: Implement data retriever agent
# Feature: Add vector embedding generation
# Feature: Add Google Sheets API integration
# Feature: Add batch processing for large datasets
# Feature: Add comprehensive logging system
# Feature: Implement semantic search capabilities
# Feature: Add comprehensive logging system
# Feature: Add result augmenter capabilities
# Refactor: Refactor security implementations
# Feature: Implement chat history persistence
# Implement advanced authentication flows
# Add sophisticated error handling
# Add intelligent content filtering
# Implement sophisticated CI/CD pipeline
# Add comprehensive monitoring dashboard
# Add intelligent data preprocessing
# Add intelligent content filtering
# Implement intelligent system scaling
from langchain_core.messages import AIMessage
from core import RocloRunnableChain
from typing import Dict, Any
from agents.query.utils import (
    extract_sql,
    add_descriptions
)
import logging
import chainlit as cl



async def query_generator(state: Dict[str, Any], chain: RocloRunnableChain) -> Dict[str, Any]:
    """  
    Generate a SQL query for a GraphDB transaction.  

    Args:  
        state (Dict[str, Any]): The current state containing user and session information.  
        chain (RocloRunnableChain): The chain used for generating the SQL query.  

    Returns:  
        Dict[str, Any]: A dictionary containing the generated SQL query and related information.  
    """
    # Determine the input message based on the sender
    if state['sender'] == 'rational_planner':
        input_msg = {
            "user_question": f"This is the user question:\n<user_question>\n{state['messages'][0].content}\n</user_question>",
            "rational_plan": f"\n\nThese are rational plan and its thinking steps:\n{state['messages'][-1].content}"
        }
    else:
        input_msg = {
            "user_question": state['messages'][-1].content,
            "rational_plan": ""
        }

    # Start span.
    span = state['trace'].span(
        name = "Query_Generator",
        type = 'llm',
        input = input_msg
    )

    try:
        # Invoke the chain to generate the SQL query
        result = await chain.ainvoke(
            input_msg,
            config = {
                "configurable": {
                    "table_id": "oaklins_query_generator",
                    "session_id": state['session_id']
                }
            }
        )

        # Extract the generated SQL query from the result.
        generated_sql = extract_sql(result.content)

        # Add descriptions in sql
        modified_sql = add_descriptions(generated_sql)

        # Update the span.
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").info(f"Invoked SQL Generator")
        span.update(output = modified_sql, metadata = result.usage_metadata)
        span.end()
        
        return {
            "messages": AIMessage(content = modified_sql),
            "sender": "query_generator"
        }
    
    except Exception as e:
        # log the error and update the span
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").error(f"Error while invoking SQL Generator: {e}")
        span.update(output = str(e))
        span.end()

        # Update the task status
        cl.user_session.get('task').status = cl.TaskStatus.FAILED
        await cl.user_session.get("task_list").send()
        
        raise



