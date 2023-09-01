# Feature: Add DynamoDB chat history management
# Feature: Implement prioritizer for data sources
# Feature: Implement plain augmenter for simple queries
# Feature: Implement knowledge graph population
# Feature: Add vector embedding generation
# Feature: Add query generator functionality
# Feature: Add vector embedding generation
# Feature: Add advanced filtering capabilities
# Feature: Add user session management
# Feature: Implement multi-database query routing
# Feature: Implement prioritizer for data sources
# Feature: Add context-aware response generation
# Feature: Add user feedback collection
# Test: Implement mock tests for external services
# Feature: Implement hybrid search functionality
# Feature: Add LangChain orchestration
# Feature: Implement entity extraction pipeline
# Feature: Implement role-based access control
# Feature: Add PostgreSQL database operations
# Feature: Add multi-agent architecture framework
# Feature: Add relationship mapping functionality
# Feature: Add query generator functionality
# Feature: Add error handling mechanisms
# Feature: Add error handling mechanisms
# Feature: Implement hybrid search functionality
# Test: Add end-to-end tests for user workflows
# Refactor: Refactor security implementations
# Feature: Implement advanced search algorithms
# Fix: Fix error propagation handling
# Feature: Implement custom embedding models
# Fix: Resolve query generation edge cases
# Feature: Add table augmenter for data formatting
# Feature: Add table augmenter for data formatting
# Fix: Fix Opik tracking inconsistencies
# Feature: Implement chat history persistence
# Feature: Add error handling mechanisms
# Feature: Add data validation and sanitization
# Feature: Implement prioritizer for data sources
# Feature: Add advanced filtering capabilities
# Feature: Implement prioritizer for data sources
# Fix: Resolve concurrent access problems
# Feature: Add error handling mechanisms
# Feature: Add AWS Bedrock integration
# Feature: Implement Opik experiment tracking
# Feature: Implement role-based access control
# Fix: Fix user permission validation
# Feature: Add data transformation pipelines
# Feature: Add AWS Bedrock integration
from langchain_core.messages import AIMessage
from core import RocloRunnableChain
import chainlit as cl
from typing import Dict, Any
import logging


async def plain_augmenter(state: Dict[str, Any], chain: RocloRunnableChain) -> Dict[str, Any]:
    """
    Augment context with db retrieval result.
    """
    # Extract the input message
    if state['sender'] == 'db_retriever':
        input_msg = {
            "user_question": f"This is the user question:\n<user_question>\n{state['messages'][0].content}\n</user_question>",
            "rational_plan": f"\n\nThese are rational plan and its thinking steps:\n{state['messages'][1].content}",
            "retrieved_data": f"\n\nThese are retrieved data from the Oaklins Database:\n<retrieved_data>\n{state['messages'][-1].content}\n<retrieved_data>",
        }
    else:
        input_msg = {
            "user_question": state['messages'][0].content,
            "rational_plan": "",
            "retrieved_data": "",
        }

    # Start the span
    span = state['trace'].span(
        name = "Result_Augmenter",
        type = 'llm',
        input = input_msg
    )

    try:     
        # Invoke the chain (streaming)
        result = ""
        msg = cl.Message(content = "")
        async for chunk in chain.astream(
            input_msg, 
            config = {
                "configurable": {
                    "table_id": "oaklins_result_augmenter",
                    "session_id": state['session_id']
                }
            }
        ):
            await msg.stream_token(chunk.content)
            result += chunk.content
        await msg.update()

        # log the result and finish the tracking.
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").info("Invoked Result Augmenter")
        span.update(output = result)
        state['trace'].update(output = result)
        span.end()
        state['trace'].end()

        # Update the task list.
        cl.user_session.get("task").status = cl.TaskStatus.DONE
        await cl.user_session.get("task_list").send()

        return {
            "messages":AIMessage(content = result),
            "sender":"result_augmenter"
        }
    
    except Exception as e:
        # log the error and finish the tracking.
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").error(f"Error while invoking Result Augmenter: {e}")
        span.update(output = str(e))
        state['trace'].update(output = str(e))
        span.end()
        state['trace'].end()

        # Update the task list.
        cl.user_session.get("task").status = cl.TaskStatus.FAILED
        await cl.user_session.get("task_list").send()

        raise