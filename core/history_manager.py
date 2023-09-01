# Feature: Add DynamoDB chat history management
# Feature: Add advanced filtering capabilities
# Feature: Add query generator functionality
# Fix: Resolve Neo4j connection pooling issues
# Feature: Add batch processing for large datasets
# Feature: Add AWS Bedrock integration
# Fix: Fix memory leaks in vector processing
# Fix: Fix authentication flow issues
# Feature: Add LangChain orchestration
# Feature: Add comprehensive logging system
# Feature: Add advanced filtering capabilities
# Feature: Implement Cerebras AI support
# Feature: Implement prioritizer for data sources
# Feature: Add context-aware response generation
# Feature: Implement hybrid search functionality
# Feature: Add LangChain orchestration
# Feature: Add error handling mechanisms
# Feature: Implement Milvus vector database support
# Feature: Add LangChain orchestration
# Feature: Add graph traversal optimization
# Feature: Implement secure credential management
# Feature: Add PostgreSQL database operations
# Feature: Implement intelligent query planning
# Feature: Implement query optimization
# Fix: Resolve logging configuration issues
# Feature: Implement entity extraction pipeline
# Feature: Add response caching mechanism
# Feature: Implement knowledge graph population
# Feature: Implement entity extraction pipeline
# Feature: Add data validation and sanitization
# Feature: Add result augmenter capabilities
# Feature: Add error handling mechanisms
# Feature: Implement secure credential management
# Feature: Add automated data refresh pipeline
# Feature: Add query generator functionality
# Fix: Resolve concurrent access problems
# Test: Add security tests for authentication
# Feature: Implement entity extraction pipeline
# Test: Implement stress tests for system limits
# Fix: Fix Docker compose networking
# Feature: Implement Chainlit UI interface
# Fix: Resolve Neo4j connection pooling issues
# Feature: Add automated data refresh pipeline
# Feature: Implement chat history persistence
# Feature: Add Neo4j knowledge graph integration
# Feature: Add error handling mechanisms
# Test: Add unit tests for rational planner
# Refactor: Optimize database query performance
# Fix: Fix Milvus index corruption
# Feature: Add advanced filtering capabilities
# Feature: Implement advanced search algorithms
# Refactor: Optimize caching strategies
# Feature: Add table augmenter for data formatting
# Test: Implement mock tests for external services
# Refactor: Restructure project directory layout
# Feature: Add data transformation pipelines
# Fix: Fix Milvus index corruption
# Feature: Add Neo4j knowledge graph integration
# Feature: Add Google Sheets API integration
# Feature: Implement chat history persistence
# Feature: Add comprehensive logging system
# Feature: Add data transformation pipelines
# Feature: Add batch processing for large datasets
# Feature: Add table augmenter for data formatting
from langchain_community.chat_message_histories import (
    DynamoDBChatMessageHistory,
)
from typing import Optional, Dict, Any
import boto3
import logging
from botocore.exceptions import ClientError


class DynamoDBChatHistoryManager:
    """  
    Singleton class to manage chat history in a PostgreSQL database.  
    
    This class provides methods to create an asynchronous connection to the database,  
    create necessary tables, and retrieve chat history for a given session.  
    """
    _instance: Optional['DynamoDBChatHistoryManager'] = None
    
    def __new__(cls):
        """Create a new instance of PostgresChatHistoryManager if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(DynamoDBChatHistoryManager, cls).__new__(cls)
            cls._instance.dynamodb = None
        return cls._instance

    
    @classmethod
    def connect(cls):
        """Initialize the PostgresChatHistoryManager by creating a connection and tables."""
        if cls._instance is None:
            cls()

        cls._instance.dynamodb = boto3.resource('dynamodb')


    @classmethod
    def __create_standard_table(cls, table_name: str):
        """Create table for chat history management"""
        try:
            # Create the DynamoDB table.
            table = cls._instance.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "SessionId", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            # Wait until the table exists.
            table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
            logging.getLogger("main").info(f"DynamoDB table {table_name} created")
        except Exception as e:
            logging.getLogger("main").error(f"Error while creating DynamoDB table {table_name}")

    
    @classmethod
    def __create_value_mapping_table(cls, table_name: str):
        """Create table for chat history management"""
        try:
            # Create the DynamoDB table.
            table = cls._instance.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[  
                    {  
                        'AttributeName': 'session_id',  
                        'KeyType': 'HASH'  # Partition key  
                    },  
                    {  
                        'AttributeName': 'label',  
                        'KeyType': 'RANGE'  # Sort key  
                    }  
                ],
                AttributeDefinitions=[  
                    {  
                        'AttributeName': 'session_id',  
                        'AttributeType': 'S'  # String type  
                    },  
                    {  
                        'AttributeName': 'label',  
                        'AttributeType': 'S'  # String type  
                    }
                ],
                BillingMode="PAY_PER_REQUEST",
            )
            # Wait until the table exists.
            table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
            logging.getLogger("main").info(f"DynamoDB table {table_name} created")
        except Exception as e:
            logging.getLogger("main").error(f"Error while creating DynamoDB table {table_name} - {e}")

    
    @classmethod
    def _create_all_tables(cls):
        """Create all table for TransitQ"""
        cls.__create_standard_table("rational_planner")
        cls.__create_standard_table("cypher_generator")
        cls.__create_standard_table("graph_augmenter")
        cls.__create_value_mapping_table("value_mapper")



    @classmethod
    def get_chat_history(cls, table_id: str, session_id: str) -> DynamoDBChatMessageHistory:
        """Retrieve chat history for a specific session.  

        Args:  
            table_id (str): The ID of the table.
            session_id (str): The ID of the session for which to retrieve chat history.  

        Returns:  
            PostgresChatMessageHistory: An instance of PostgresChatMessageHistory for the specified session.  
        """
        return DynamoDBChatMessageHistory(
            table_name = table_id,
            session_id = session_id
        )


    @classmethod
    def add_mapped_value(cls, item: Dict[str, Any]) -> None:
        """
        Add mapped value to Postgres.
        """
        table = cls._instance.dynamodb.Table('value_mapper')
        try:
            table.put_item(Item = item)
        except Exception as e:
            logging.getLogger("main").error(f"Error while adding mapped value: {e}") 
            raise


    @classmethod
    def get_mapped_value(
        cls,
        session_id: str,
        label: str,
        prop: str,
        old_value: str
    ) -> str:
        """
        Get mapped value from Postgres in the chat session.
        """
        table = cls._instance.dynamodb.Table('value_mapper')
        try:
            # Query the table
            response = table.query(  
                KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(session_id) &  
                                    boto3.dynamodb.conditions.Key('label').eq(label),  
                FilterExpression=boto3.dynamodb.conditions.Attr('prop').eq(prop) &  
                                boto3.dynamodb.conditions.Attr('old_value').eq(old_value)  
            )

            items = response.get('Items', [])  
            if items:
                return items[0]['new_value'] 
            else:
                return None  # No matching item found  
        except Exception as e:
            logging.getLogger('main').error(f"Error while getting mapped value: {e}") 
            raise


    @classmethod
    def __delete_table(cls, table_name: str) -> None:  
        try:  
            # Reference the table you want to delete  
            table = cls._instance.dynamodb.Table(table_name)  

            # Check if the table exists  
            table.load()  # This will raise an exception if the table does not exist  

            # Delete the table  
            table.delete()  
            logging.getLogger('main').info(f"Deleting table: {table_name}")  
            
            # Wait for the deletion to complete  
            table.wait_until_not_exists()  
            logging.getLogger('main').info(f"Table {table_name} has been deleted successfully.")  

        except ClientError as e:  
            error_code = e.response['Error']['Code']  
            if error_code == 'ResourceNotFoundException':  
                logging.getLogger('main').info(f"Table {table_name} does not exist. No action taken.")  
            else: 
                logging.getLogger('main').error(f"Error while deleting table {table_name} - {e}")
                raise  # Re-raise any other ClientError

    
    @classmethod
    def _delete_all_tables(cls) -> None:
        cls.__delete_table("rational_planner")
        cls.__delete_table("cypher_generator")
        cls.__delete_table("graph_augmenter")
        cls.__delete_table("value_mapper")


    @classmethod
    def reset_tables(cls) -> None:
        # Delete all tables.
        cls._delete_all_tables()

        # Create all tables.
        cls._create_all_tables()
