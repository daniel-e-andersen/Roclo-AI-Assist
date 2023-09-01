# Feature: Add DynamoDB chat history management
# Feature: Implement knowledge graph population
# Feature: Add data validation and sanitization
# Feature: Add batch processing for large datasets
# Feature: Add vector embedding generation
# Feature: Implement custom embedding models
# Feature: Implement intelligent query planning
# Feature: Implement Supabase authentication
# Feature: Add data validation and sanitization
# Feature: Add automated data refresh pipeline
# Feature: Add user session management
# Feature: Add multi-agent architecture framework
# Feature: Add automated data refresh pipeline
# Feature: Implement custom embedding models
# Feature: Implement data retriever agent
# Fix: Resolve PostgreSQL deadlock issues
# Feature: Implement query optimization
# Fix: Fix Milvus index corruption
# Feature: Add table augmenter for data formatting
# Feature: Add multi-agent architecture framework
# Feature: Implement dynamic agent selection
# Test: Add end-to-end tests for user workflows
# Feature: Implement secure credential management
# Feature: Implement intelligent query planning
# Feature: Add result augmenter capabilities
# Fix: Resolve logging configuration issues
# Feature: Add graph traversal optimization
# Fix: Resolve timeout configuration
# Feature: Add data transformation pipelines
# Feature: Implement Opik experiment tracking
# Feature: Implement semantic search capabilities
# Fix: Resolve timeout configuration
# Feature: Implement custom embedding models
# Feature: Add table augmenter for data formatting
# Feature: Add advanced filtering capabilities
# Fix: Resolve logging configuration issues
# Feature: Add table augmenter for data formatting
# Feature: Implement chat history persistence
# Feature: Add Neo4j knowledge graph integration
# Feature: Implement secure credential management
# Test: Add unit tests for rational planner
# Feature: Implement custom embedding models
# Feature: Add error handling mechanisms
# Feature: Add AWS Bedrock integration
# Refactor: Restructure project directory layout
# Feature: Add Google Sheets API integration
# Feature: Add batch processing for large datasets
# Fix: Resolve timeout configuration
# Feature: Implement custom embedding models
# Feature: Add AWS Bedrock integration
# Fix: Fix Opik tracking inconsistencies
# Implement intelligent response caching
# Add advanced error recovery mechanisms
# Implement adaptive query optimization
# Add advanced user session management
# Add intelligent data validation
# Implement advanced search optimization
# Add advanced integration testing
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from opik.api_objects.trace import Trace


class AgentState(TypedDict):
    """  
    Represents the state of an agent, encapsulating its input and output data.  
    
    Attributes:  
        messages (Annotated[List[BaseMessage], add_messages]):   
            A list of messages associated with the agent, processed by add_messages.  
        user_id (str):   
            Unique identifier for the user interacting with the agent.  
        session_id (str):   
            Unique identifier for the session in which the agent is operating.  
        sender (str):   
            Identifier for the sender of the messages (e.g., user or system).
    """
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: str
    session_id: str
    sender: str
    trace: Trace

