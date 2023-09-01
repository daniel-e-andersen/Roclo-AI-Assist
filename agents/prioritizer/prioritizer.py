# Feature: Add LangChain orchestration
# Feature: Implement knowledge graph population
# Feature: Add automated data refresh pipeline
# Feature: Add AWS Bedrock integration
# Feature: Add advanced filtering capabilities
# Feature: Add vector embedding generation
# Feature: Add conversation flow management
# Feature: Add data validation and sanitization
# Feature: Add error handling mechanisms
# Feature: Add comprehensive logging system
# Feature: Add LangChain orchestration
# Fix: Fix cache invalidation logic
# Feature: Add Google Sheets API integration
# Feature: Add data validation and sanitization
# Feature: Implement secure credential management
# Feature: Add automated data refresh pipeline
# Feature: Add context-aware response generation
# Feature: Implement custom embedding models
# Feature: Implement retry logic for failed operations
# Feature: Implement hybrid search functionality
# Feature: Implement query optimization
# Feature: Implement Opik experiment tracking
# Feature: Add table augmenter for data formatting
# Feature: Add advanced filtering capabilities
# Feature: Implement secure credential management
# Feature: Add multi-agent architecture framework
# Feature: Implement dynamic agent selection
# Feature: Implement query optimization
# Fix: Resolve timeout configuration
# Feature: Add error handling mechanisms
# Feature: Implement chat history persistence
# Feature: Add result augmenter capabilities
# Feature: Implement secure credential management
# Feature: Add error handling mechanisms
# Feature: Add query generator functionality
# Feature: Implement advanced search algorithms
# Feature: Implement retry logic for failed operations
# Feature: Implement semantic search capabilities
# Feature: Implement custom embedding models
# Feature: Implement query optimization
# Feature: Implement rational planner agent
# Feature: Implement Chainlit UI interface
# Fix: Fix Docker compose networking
# Fix: Fix Docker compose networking
# Fix: Fix query parsing errors
# Fix: Resolve timeout configuration
# Feature: Implement dynamic agent selection
# Feature: Add Neo4j knowledge graph integration
# Feature: Add data validation and sanitization
# Feature: Add context-aware response generation
# Feature: Implement Cerebras AI support
# Feature: Add result augmenter capabilities
# Feature: Add LangChain orchestration
# Fix: Resolve concurrent access problems
# Fix: Resolve search result ranking
from langchain_core.messages import HumanMessage
from core import (
    RocloRunnableChain,
    RocloMilvusVectorDB
)
from typing import Dict, Any
import logging
import chainlit as cl
from agents.prioritizer.utils import (
    DateTimeEncoder,
    get_deal_ids
)
import json
from kg_population.vector_calculator.vector_schmea import vector_schema

async def prioritizer(state: Dict[str, Any], chain: RocloRunnableChain) -> Dict[str, Any]:
    """  
    You will receive a user query and a list of dictionaries containing retrieved data. Your goal is to sort these entries by relevance to the user's question.
    """
    
    try:
        # Extract the input message
        retrieved_data = json.loads(state['messages'][-1].content)
        user_question = state['messages'][0].content

        # Initialize i/o_msg for Span
        input_msg = {
            "user_question": user_question,
            "rational_plan": state['messages'][1].content
        }
        
        output_msg = {
            "retrieved_data" : retrieved_data
        }

        # Start span.
        span = state['trace'].span(
            name = "Prioritizer",
            type = 'tool',
            input = "Roclo"
        )

        if "deal_id" in retrieved_data[0].keys() and "target_business_description" in retrieved_data[0].keys():
            deal_ids = [deal["deal_id"] for deal in retrieved_data]
            print(deal_ids)

            # Inoke the chain
            result = await chain.ainvoke(
                input_msg, 
                config = {
                    "configurable": {
                        "table_id": "oaklins_prioritizer",
                        "session_id": state['session_id']
                    }
                }
            )
            business_description = result.content
            input_msg["business_description"] = business_description
            span.update(input=input_msg)

            # Prioritize the Deals
            prioritized_lables = RocloMilvusVectorDB.search_data(business_description, vector_schema['collection_name'], deal_ids, ["deal_id", "title"], 0.35)
            prioritized_deal_ids = get_deal_ids(prioritized_lables)

            # If all is filtered out
            if not prioritized_deal_ids:
                prioritized_deal_ids = deal_ids
                logging.getLogger(f"{state['user_id']}-{state['session_id']}").info(f"All deals are filtered out")
            prioritized_data = [retrieved_data[deal_ids.index(x)] for x in prioritized_deal_ids]

            retrieved_data = prioritized_data

            # update output_msg
            output_msg['retrieved_data'] = retrieved_data
            output_msg['prioritized_lables'] = prioritized_lables
            logging.getLogger(f"{state['user_id']}-{state['session_id']}").info(f"Prioritized is passed")

        retrieved_data = json.dumps(retrieved_data, cls=DateTimeEncoder)
        

        # Update the span.
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").info(f"Invoked Prioritizer")
        span.update(output = output_msg)
        span.end()
        
        return {
            "messages":HumanMessage(content = retrieved_data),
            "sender":"prioritizer"
        }
    
    except Exception as e:
        # log the error and update the span
        logging.getLogger(f"{state['user_id']}-{state['session_id']}").error(f"Error while invoking Prioritizer: {e}")
        span.update(output = str(e))
        span.end()

        # Update the task status
        cl.user_session.get('task').status = cl.TaskStatus.FAILED
        await cl.user_session.get("task_list").send()
        
        raise



