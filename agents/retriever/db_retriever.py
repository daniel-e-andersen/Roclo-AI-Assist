# Feature: Implement knowledge graph population
# Feature: Add query generator functionality
# Feature: Implement multi-database query routing
# Feature: Add batch processing for large datasets
# Feature: Add response caching mechanism
# Feature: Add advanced filtering capabilities
# Feature: Add PostgreSQL database operations
# Feature: Add automated data refresh pipeline
# Feature: Implement hybrid search functionality
# Feature: Implement data retriever agent
# Feature: Add error handling mechanisms
# Feature: Implement advanced search algorithms
# Feature: Implement Opik experiment tracking
# Feature: Implement real-time data synchronization
# Feature: Implement Milvus vector database support
# Feature: Add LangChain orchestration
# Feature: Implement Chainlit UI interface
# Feature: Implement intelligent query planning
# Feature: Implement intelligent query planning
# Feature: Implement entity extraction pipeline
# Feature: Implement chat history persistence
# Feature: Add table augmenter for data formatting
# Feature: Implement performance monitoring
# Feature: Implement secure credential management
# Feature: Add automated data refresh pipeline
# Feature: Implement performance monitoring
# Feature: Add graph traversal optimization
# Feature: Add result augmenter capabilities
# Feature: Add data transformation pipelines
# Feature: Implement semantic search capabilities
# Feature: Implement Opik experiment tracking
# Feature: Implement plain augmenter for simple queries
# Fix: Fix Docker compose networking
# Feature: Add automated data refresh pipeline
# Feature: Implement chat history persistence
# Feature: Add multi-agent architecture framework
# Feature: Implement advanced search algorithms
# Feature: Implement custom embedding models
# Feature: Add AWS Bedrock integration
# Feature: Add data transformation pipelines
# Refactor: Restructure database connection management
# Fix: Resolve database connection timeouts
# Feature: Add comprehensive logging system
# Fix: Fix cache invalidation logic
# Feature: Add table augmenter for data formatting
# Fix: Resolve vector similarity calculation
# Implement advanced API rate limiting
# Implement sophisticated data migration
# Implement intelligent failover mechanisms
# Implement adaptive query optimization
# Implement sophisticated data migration
# Implement advanced workflow automation
# Add advanced error recovery mechanisms
from typing import Dict, Any
from core import RocloPostgresDatabase
from langchain_core.messages import HumanMessage
import logging
import tiktoken
import json

encoding = tiktoken.get_encoding('cl100k_base')

async def db_retriever(state: Dict[str, Any]) -> Dict[str, Any]:
    """  
    Execute the generated SQL query and return the result.  

    Args:  
        state (Dict[str, Any]): The state containing the query and other parameters.  

    Returns:  
        Dict[str, Any]: The response including messages and state information.  
    """
    query = state['messages'][-1].content

    # Start the span
    span = state['trace'].span(
        name = "DB_Retriever",
        type = 'tool',
        input = "Roclo"
    )

    try:
        # retrieval_result = await RocloGraphDatabase.execute_query(query)
        retrieval_result = await RocloPostgresDatabase.execute_query(query)
        if not retrieval_result:  
            retrieval_result = "No data was retrieved from the query. The result set is empty." +\
                "The SQL query syntax appears to be correct. However, the lack of results may be due to overly restrictive conditions or incorrect parameters. " +\
                "Please review and provide the exact SQL query for further analysis."
        
        # elif len(encoding.encode(str(retrieval_result))) > 100000:
        elif len(retrieval_result) > 100:
            retrieval_result =  "The data retrieval process has exceeded the expected volume. Please verify that your SQL query is correctly formulated, " +\
                "utilizing precise entity references at each step. Additionally, consider implementing data retrieval limits within your query to optimize performance."
            
        else:
            
            retrieval_result = json.dumps(retrieval_result)

    except Exception as e:
        retrieval_result = "I encountered an issue while attempting to retrieve the data. It appears there is a syntax error in the sql query." +\
            f"The following error was generated when executing the SQL query:\n\n{e}\n" +\
            "Kindly revise the sql query to resolve this issue." 

        await RocloPostgresDatabase.rollback()

    # Log the result and update the span
    logging.getLogger(f"{state['user_id']}-{state['session_id']}").info("Invoked DB Retriever")
    span.update(output = str(retrieval_result))
    span.end()

    return {
        "messages":HumanMessage(content = retrieval_result),
        "sender":"db_retriever"
    }