# Feature: Implement knowledge graph population
# Fix: Resolve memory optimization
# Fix: Fix memory leaks in vector processing
# Feature: Add AWS Bedrock integration
# Feature: Add comprehensive logging system
# Feature: Add relationship mapping functionality
# Feature: Add error handling mechanisms
# Feature: Add Google Sheets API integration
# Fix: Fix data consistency issues
# Feature: Implement Cerebras AI support
# Feature: Implement rational planner agent
# Fix: Resolve AWS credentials rotation
# Feature: Add context-aware response generation
# Feature: Implement Chainlit UI interface
# Feature: Implement retry logic for failed operations
# Feature: Add LangChain orchestration
# Feature: Add error handling mechanisms
# Fix: Resolve LangChain callback errors
# Feature: Implement real-time data synchronization
# Feature: Implement Milvus vector database support
# Feature: Implement knowledge graph population
# Feature: Implement query optimization
# Feature: Add error handling mechanisms
# Feature: Add Google Sheets API integration
# Fix: Resolve database connection timeouts
# Fix: Resolve entity extraction failures
# Test: Add regression tests for critical paths
# Feature: Add conversation flow management
# Feature: Implement semantic search capabilities
# Fix: Resolve API rate limiting
# Feature: Implement Milvus vector database support
# Feature: Implement retry logic for failed operations
# Feature: Implement entity extraction pipeline
# Refactor: Restructure database connection management
# Test: Implement stress tests for system limits
# Feature: Implement custom embedding models
# Feature: Implement query optimization
# Feature: Add graph traversal optimization
# Feature: Add vector index maintenance
# Feature: Add table augmenter for data formatting
# Feature: Add multi-agent architecture framework
# Feature: Add data validation and sanitization
# Refactor: Refactor agent architecture for better modularity
# Fix: Resolve query generation edge cases
# Feature: Implement Opik experiment tracking
# Feature: Add table augmenter for data formatting
# Fix: Resolve vector similarity calculation
# Feature: Add result augmenter capabilities
# Feature: Implement data retriever agent
# Feature: Implement chat history persistence
# Fix: Resolve API rate limiting
# Fix: Resolve query generation edge cases
# Fix: Resolve PostgreSQL deadlock issues
# Feature: Implement semantic search capabilities
# Feature: Add result augmenter capabilities
# Feature: Add table augmenter for data formatting
# Refactor: Optimize resource allocation
# Fix: Resolve entity extraction failures
# Feature: Implement chat history persistence
# Refactor: Refactor security implementations
from typing import Optional
from neo4j import AsyncGraphDatabase
from config import Credentials
from contextlib import asynccontextmanager
from typing import Dict
import logging
from utils import convert_neo4j_datetime
import tiktoken
# from langchain_neo4j import Neo4jGraph
# from langchain_neo4j.chains.graph_qa.cypher_utils import (
#     CypherQueryCorrector,
#     Schema,
# )


class RocloGraphDatabase:
    """  
    Singleton class to manage Roclo graph database.  
    
    This class ensures that only one instance of the graph database is created  
    and provides methods to excute the cypher query and returns the result.  
    """
    _instance: Optional['RocloGraphDatabase'] = None

    def __new__(cls):
        """Create a new instance of RocloGraphDatabase if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloGraphDatabase, cls).__new__(cls)
            cls._instance.driver = None
            cls._instance.session = None
        return cls._instance
    

    @classmethod
    def connect(cls, database = None):
        """Initialize the connection to the Neo4j GraphDB."""
        if cls._instance is None:
            cls()

        try:
            cls._instance.driver = AsyncGraphDatabase.driver(
                Credentials.get_secret("NEO4J_URI"),
                auth = (
                    Credentials.get_secret("NEO4J_USERNAME"),
                    Credentials.get_secret("NEO4J_PASSWORD")
                )
            )

            # Initialize the LangChain's Cypher query corrector.
            # graph = Neo4jGraph(
            #     url = Credentials.get_secret("NEO4J_URI"),
            #     database = Credentials.get_secret("NEO4J_DATABASE"), 
            #     username = Credentials.get_secret("NEO4J_USERNAME"), 
            #     password= Credentials.get_secret("NEO4J_PASSWORD"),
            #     enhanced_schema=True
            # )
            # corrector_schema = [
            #     Schema(el["start"], el["type"], el["end"])
            #     for el in graph.structured_schema.get("relationships")
            # ]
            # cls._instance.cypher_query_corrector = CypherQueryCorrector(corrector_schema)
            
            # Initialize the session.
            if database == None:
                cls._instance.session = cls._instance.driver.session(
                    database = Credentials.get_secret("NEO4J_DATABASE")
                )
            else:
                cls._instance.session = cls._instance.driver.session(
                    database = database
                )

            logging.getLogger('main').info("Neo4j Graph Database connected.")
        except Exception as e:
            logging.getLogger('main').info("Failed to connect to Neo4j database: %s", e)
            raise
    

    @classmethod
    async def correct_query(cls, query: str) -> str:
        """
        Correct the Cypher query's relationship mismatches.

        Args:
            query (str): Cypher query need to fix.
        
        Returns:
            str: Corrected cypher query.
        """
        return cls._instance.cypher_query_corrector(query)



    @classmethod
    async def _close_connection(cls):
        """Close the Neo4j GraphDatabase connection"""
        if cls._instance.driver:
            await cls._instance.driver.close()

    
    @classmethod
    @asynccontextmanager
    async def _transaction(cls):
        """Transaction context manager with proper handling."""
        if not cls._instance.session:
            raise RuntimeError("Session not initialized. Call init() first.")
        
        tx = await cls._instance.session.begin_transaction(timeout=300)
        try:  
            yield tx
        except Exception as e:  
            await tx.rollback()  
            raise  
        finally:  
            await tx.close()

            
    
    @classmethod
    async def execute_query(cls, query: str, query_type: str = 'match') -> Optional[Dict]:
        """
        Execute the cypher query and returns the records as dict.
        """
        async with cls._transaction() as tx:
            result = await tx.run(query)

            # If the query type is 'match', retrieve the data and format it.
            if query_type == 'match':
                result_df = await result.to_df()
                result_data = result_df.to_dict(orient='records')
                convert_neo4j_datetime(result_data)
                return  result_data
            
            # For data modification queries like CREATE, UPDATE, and DELETE, commite the transaction after executing the query.
            else: 
                await tx.commit()
                return None
