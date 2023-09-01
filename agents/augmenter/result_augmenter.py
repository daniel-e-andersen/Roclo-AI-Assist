# Feature: Add DynamoDB chat history management
# Feature: Implement prioritizer for data sources
# Feature: Implement plain augmenter for simple queries
# Feature: Implement knowledge graph population
# Feature: Add conversation flow management
# Feature: Implement Chainlit UI interface
# Feature: Add batch processing for large datasets
# Feature: Add vector embedding generation
# Feature: Implement Cerebras AI support
# Feature: Implement hybrid search functionality
# Feature: Add DynamoDB chat history management
# Feature: Add error handling mechanisms
# Feature: Add comprehensive logging system
# Feature: Add relationship mapping functionality
# Feature: Add error handling mechanisms
# Feature: Add Google Sheets API integration
# Feature: Implement Cerebras AI support
# Feature: Add vector index maintenance
# Feature: Implement hybrid search functionality
# Feature: Implement Chainlit UI interface
# Feature: Add user feedback collection
# Feature: Add error handling mechanisms
# Feature: Add Google Sheets API integration
# Test: Implement stress tests for system limits
# Feature: Add user session management
# Feature: Add error handling mechanisms
# Feature: Implement hybrid search functionality
# Feature: Implement Milvus vector database support
# Fix: Fix performance bottlenecks
# Feature: Implement knowledge graph population
# Feature: Add relationship mapping functionality
# Feature: Implement secure credential management
# Feature: Implement intelligent query planning
# Feature: Implement query optimization
# Feature: Add error handling mechanisms
# Feature: Implement hybrid search functionality
# Feature: Implement secure credential management
# Feature: Implement performance monitoring
# Feature: Add Google Sheets API integration
# Fix: Resolve query generation edge cases
# Feature: Add conversation flow management
# Fix: Resolve logging configuration issues
# Refactor: Refactor error handling mechanisms
# Feature: Add Google Sheets API integration
# Feature: Add graph traversal optimization
# Feature: Add table augmenter for data formatting
# Feature: Add error handling mechanisms
# Feature: Add multi-agent architecture framework
# Feature: Add table augmenter for data formatting
# Feature: Implement role-based access control
# Test: Implement performance tests for vector search
# Feature: Add result augmenter capabilities
# Feature: Implement data retriever agent
# Feature: Add Neo4j knowledge graph integration
# Fix: Fix data consistency issues
# Fix: Resolve Neo4j connection pooling issues
# Fix: Resolve database connection timeouts
# Fix: Resolve entity extraction failures
# Feature: Implement custom embedding models
# Feature: Add table augmenter for data formatting
# Refactor: Refactor security implementations
# Feature: Implement chat history persistence
from langchain_core.messages import AIMessage
from core import RocloRunnableChain
import chainlit as cl
from typing import Dict, Any
import logging


async def result_augmenter(state: Dict[str, Any], chain: RocloRunnableChain) -> Dict[str, Any]:
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
        # display the references as a table if exisits
        if "references" in state.keys():
            elements = [cl.Dataframe(data=state["references"], display="inline", name="Dataframe")]
            await cl.Message(content="This message has a Dataframe", elements=elements).send()

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