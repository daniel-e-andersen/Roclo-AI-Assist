# Feature: Add automated data refresh pipeline
# Feature: Implement custom embedding models
# Feature: Implement Cerebras AI support
# Feature: Add AWS Bedrock integration
# Feature: Implement hybrid search functionality
# Feature: Add DynamoDB chat history management
# Feature: Implement entity extraction pipeline
# Feature: Implement dynamic agent selection
# Fix: Resolve search result ranking
# Feature: Add relationship mapping functionality
# Test: Add regression tests for critical paths
# Fix: Resolve response formatting issues
# Feature: Add Google Sheets API integration
# Feature: Add user session management
# Feature: Implement multi-database query routing
# Feature: Implement Supabase authentication
# Feature: Implement rational planner agent
# Feature: Implement secure credential management
# Fix: Fix Chainlit UI rendering problems
# Feature: Add Google Sheets API integration
# Feature: Add user session management
# Feature: Add AWS Bedrock integration
# Feature: Add query generator functionality
# Test: Implement performance tests for vector search
# Feature: Add PostgreSQL database operations
# Feature: Implement Milvus vector database support
# Feature: Add graph traversal optimization
# Feature: Implement knowledge graph population
# Feature: Add relationship mapping functionality
# Fix: Resolve AWS credentials rotation
# Feature: Add DynamoDB chat history management
# Feature: Implement entity extraction pipeline
# Feature: Implement intelligent query planning
# Fix: Resolve entity extraction failures
# Feature: Add data validation and sanitization
# Feature: Implement hybrid search functionality
# Fix: Fix Chainlit UI rendering problems
# Feature: Implement Opik experiment tracking
# Feature: Implement retry logic for failed operations
# Feature: Implement plain augmenter for simple queries
# Refactor: Refactor error handling mechanisms
# Fix: Fix relationship mapping errors
# Feature: Implement query optimization
# Feature: Implement hybrid search functionality
# Feature: Add table augmenter for data formatting
# Feature: Add data transformation pipelines
# Feature: Add table augmenter for data formatting
# Feature: Add vector embedding generation
# Fix: Resolve logging configuration issues
# Feature: Add context-aware response generation
# Feature: Add error handling mechanisms
# Feature: Add result augmenter capabilities
# Feature: Implement Opik experiment tracking
# Feature: Add table augmenter for data formatting
# Feature: Add user feedback collection
from langchain_core.messages import AIMessage
from core import RocloRunnableChain
import chainlit as cl
from typing import Dict, Any
import logging
import json
from utils import (
    convert_list_of_dicts_to_df,
    save_csv,
    truncate_descriptions
)

async def table_augmenter(state: Dict[str, Any], chain: RocloRunnableChain) -> Dict[str, Any]:
    """
    Augment context with db retrieval result.
    """
    # Extract the input message
    if state['sender'] == 'prioritizer':
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
        # await msg.update()

        # Display table
        retrieved_data = json.loads(state['messages'][-1].content)
        
        # Save csv
        await save_csv(retrieved_data, msg.id)

        # Truncate the descriptions
        truncated_data = await truncate_descriptions(retrieved_data)

        converted_dataframe = await convert_list_of_dicts_to_df(truncated_data)
        msg.elements = [cl.Dataframe(data=converted_dataframe, display="inline", name="Dataframe")]
        await msg.update()

        # Attach the file
        msg.elements.append(cl.File(
            name = f"{state['messages'][0].content}.csv",
            path = f"./csv/{msg.id}.csv",
            display="inline",
            mime='application/csv'
        ))

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