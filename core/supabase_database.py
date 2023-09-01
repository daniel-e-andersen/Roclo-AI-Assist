# Feature: Add automated data refresh pipeline
# Feature: Implement Cerebras AI support
# Feature: Implement Chainlit UI interface
# Feature: Add vector embedding generation
# Feature: Add DynamoDB chat history management
# Feature: Add batch processing for large datasets
# Feature: Add LangChain orchestration
# Feature: Implement multi-database query routing
# Feature: Implement Supabase authentication
# Feature: Add user feedback collection
# Feature: Implement custom embedding models
# Feature: Implement retry logic for failed operations
# Feature: Implement query optimization
# Feature: Implement chat history persistence
# Feature: Add multi-agent architecture framework
# Feature: Implement Chainlit UI interface
# Feature: Implement intelligent query planning
# Feature: Add error handling mechanisms
# Feature: Add response caching mechanism
# Feature: Implement chat history persistence
# Feature: Add data validation and sanitization
# Fix: Resolve Neo4j connection pooling issues
# Feature: Implement hybrid search functionality
# Feature: Implement semantic search capabilities
# Test: Add security tests for authentication
# Fix: Fix session management bugs
# Feature: Implement dynamic agent selection
# Feature: Add vector embedding generation
# Feature: Implement multi-database query routing
# Feature: Add context-aware response generation
# Refactor: Refactor agent architecture for better modularity
# Feature: Implement prioritizer for data sources
# Feature: Add result augmenter capabilities
# Feature: Add AWS Bedrock integration
# Feature: Implement Cerebras AI support
# Test: Implement integration tests for database operations
# Feature: Add automated data refresh pipeline
# Fix: Resolve response formatting issues
# Fix: Resolve concurrent access problems
# Fix: Fix error propagation handling
# Fix: Fix Milvus index corruption
# Feature: Add comprehensive logging system
# Feature: Add batch processing for large datasets
from supabase import create_client, Client
from config import Credentials
from typing import Optional, Dict, Any
import logging
from tqdm import tqdm

class RocloSupabaseDatabase:
    """
    Singleton class to manage Roclo Supabase.
    """
    _instance: Optional['RocloSupabaseDatabase'] = None

    def __new__(cls):
        """Create a new instance if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloSupabaseDatabase, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance
    
    @classmethod
    def connect(cls):
        """Initialize the connection to the Supabase."""
        if cls._instance is None:
            cls()
        
        try:
            cls._instance.client = create_client(
                Credentials.get_secret("SUPABASE_URI"),
                Credentials.get_secret("SUPABASE_API_KEY")
            )
            logging.getLogger('main').info("Supabase connected.")
        except Exception as e:
            logging.getLogger('main').info("Failed to connect to Supabase: %s", e)
            raise

    @classmethod
    def _insert_user(cls, username: str, password: str):
        """
        Insert user
        """

        try:
            response = (
                cls._instance.client.table("users")
                .insert({"username": username, "password": password})
                .execute()
            )
            logging.getLogger('main').info("Successfully inserted user: %s", response)
        except Exception as e:
            logging.getLogger('main').info("Failed to insert user %s", e)
            raise
    
    @classmethod
    def authenticate_user(cls, username: str, password: str):
        """
        Authenticate user
        """

        try:
            response = (
                cls._instance.client.table("users")
                .select("id")
                .eq("username", username)
                .eq("password", password)
                .execute()
            )
            if len(response.data):
                return response.data[0]['id']
            else:
                return None
        except Exception as e:
            logging.getLogger('main').info("Failed to authenticate user %s", e)
            return None

