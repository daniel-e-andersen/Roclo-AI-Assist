# Feature: Implement knowledge graph population
# Feature: Add query generator functionality
# Feature: Implement Opik experiment tracking
# Feature: Add conversation flow management
# Feature: Add data validation and sanitization
# Feature: Add vector embedding generation
# Feature: Add vector embedding generation
# Feature: Add query generator functionality
# Feature: Implement hybrid search functionality
# Feature: Add advanced filtering capabilities
# Fix: Resolve response formatting issues
# Feature: Add error handling mechanisms
# Feature: Add batch processing for large datasets
# Feature: Add LangChain orchestration
# Feature: Add data validation and sanitization
# Fix: Resolve search result ranking
# Feature: Implement secure credential management
# Feature: Implement prioritizer for data sources
# Feature: Add error handling mechanisms
# Feature: Add Google Sheets API integration
# Fix: Fix query parsing errors
# Feature: Implement hybrid search functionality
# Feature: Add query generator functionality
# Feature: Add PostgreSQL database operations
# Feature: Implement hybrid search functionality
# Feature: Implement Opik experiment tracking
# Fix: Resolve PostgreSQL deadlock issues
# Feature: Implement chat history persistence
# Feature: Add multi-agent architecture framework
# Feature: Implement Milvus vector database support
# Feature: Implement knowledge graph population
# Feature: Implement prioritizer for data sources
# Feature: Add multi-agent architecture framework
# Feature: Add relationship mapping functionality
# Feature: Implement query optimization
# Feature: Add DynamoDB chat history management
# Feature: Implement chat history persistence
# Feature: Implement performance monitoring
# Feature: Add error handling mechanisms
# Feature: Add query generator functionality
# Feature: Implement performance monitoring
# Fix: Fix memory leaks in vector processing
# Feature: Add data transformation pipelines
# Test: Add security tests for authentication
# Feature: Implement advanced search algorithms
# Fix: Fix session management bugs
# Fix: Resolve concurrent access problems
# Feature: Implement query optimization
# Feature: Implement rational planner agent
# Feature: Implement dynamic agent selection
# Fix: Fix Docker compose networking
# Feature: Add table augmenter for data formatting
# Fix: Resolve AWS credentials rotation
# Refactor: Refactor UI components for reusability
# Test: Implement performance tests for vector search
# Feature: Implement prioritizer for data sources
# Feature: Implement advanced search algorithms
# Feature: Implement custom embedding models
# Feature: Add error handling mechanisms
# Fix: Resolve database connection timeouts
# Test: Implement integration tests for database operations
# Refactor: Refactor agent communication protocols
# Feature: Add result augmenter capabilities
# Fix: Fix Milvus index corruption
# Fix: Fix error propagation handling
# Feature: Implement semantic search capabilities
# Feature: Add user feedback collection
# Feature: Implement chat history persistence
from typing import Optional
import pymssql
from config import Credentials
from typing import Dict
import logging

class RocloSQLDatabase:
    """  
    Singleton class to manage Roclo SQL database.  
    
    This class ensures that only one instance of the sql database is created  
    and provides methods to excute the cypher query and returns the result.  
    """
    _instance: Optional['RocloSQLDatabase'] = None

    def __new__(cls):
        """Create a new instance of RocloGraphDatabase if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloSQLDatabase, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance
    

    @classmethod
    def connect(cls):
        """Initialize the connection to the SQL."""
        if cls._instance is None:
            cls()

        try:
            cls._instance.connection = pymssql.connect(
                server = Credentials.get_secret("MSSQL_URI"), 
                database=Credentials.get_secret("MSSQL_DATABASE"), 
                user=Credentials.get_secret("MSSQL_USERNAME"), 
                password=Credentials.get_secret("MSSQL_PASSWORD")
            )
            cls._instance.cursor = cls._instance.connection.cursor()
            logging.getLogger('main').info("SQL Database connected.")
        except Exception as e:
            logging.getLogger('main').info("Failed to connect to SQL database: %s", e)
            raise
    

    @classmethod
    def _close_connection(cls):
        """Close the SQL connection"""
        if cls._instance.connection:
            cls._instance.connection.close()

            
    
    @classmethod
    def execute_query(cls, query: str) -> Dict:
        """
        Execute the cypher query and returns the records as dict.
        """
        try:
            cls._instance.cursor.execute(query)
            results = cls._instance.cursor.fetchall()

            columns = [desc[0] for desc in cls._instance.cursor.description]

            data = [dict(zip(columns, row)) for row in results]

            return data
        
        except Exception as e:
            logging.getLogger('main').info(f"Exception Occurred: {e}")
            raise
