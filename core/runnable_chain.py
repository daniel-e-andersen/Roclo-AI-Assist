# Feature: Implement prioritizer for data sources
# Feature: Add AWS Bedrock integration
# Feature: Add vector embedding generation
# Feature: Implement Opik experiment tracking
# Feature: Implement Cerebras AI support
# Feature: Add query generator functionality
# Feature: Add error handling mechanisms
# Feature: Implement advanced search algorithms
# Feature: Add advanced filtering capabilities
# Feature: Implement intelligent query planning
# Feature: Implement dynamic agent selection
# Feature: Add PostgreSQL database operations
# Test: Implement stress tests for system limits
# Feature: Add Google Sheets API integration
# Feature: Add advanced filtering capabilities
# Feature: Add vector index maintenance
# Feature: Implement hybrid search functionality
# Fix: Resolve memory optimization
# Feature: Add user session management
# Feature: Add AWS Bedrock integration
# Feature: Implement entity extraction pipeline
# Feature: Implement role-based access control
# Feature: Add LangChain orchestration
# Feature: Implement Chainlit UI interface
# Feature: Add query generator functionality
# Feature: Implement dynamic agent selection
# Feature: Implement secure credential management
# Feature: Add DynamoDB chat history management
# Feature: Add error handling mechanisms
# Feature: Implement intelligent query planning
# Feature: Implement query optimization
# Feature: Add table augmenter for data formatting
# Feature: Add data transformation pipelines
# Test: Implement stress tests for system limits
# Feature: Implement secure credential management
# Feature: Add context-aware response generation
# Feature: Implement hybrid search functionality
# Feature: Implement Milvus vector database support
# Feature: Implement retry logic for failed operations
# Feature: Implement plain augmenter for simple queries
# Feature: Implement semantic search capabilities
# Test: Add end-to-end tests for user workflows
# Feature: Implement custom embedding models
# Feature: Implement rational planner agent
# Fix: Fix user permission validation
# Fix: Fix data consistency issues
# Feature: Add data transformation pipelines
# Feature: Add multi-agent architecture framework
# Feature: Add vector embedding generation
# Refactor: Optimize database query performance
# Feature: Add error handling mechanisms
# Refactor: Optimize caching strategies
# Fix: Resolve PostgreSQL deadlock issues
# Feature: Implement data retriever agent
# Feature: Add LangChain orchestration
# Fix: Resolve AWS credentials rotation
# Refactor: Optimize memory usage patterns
# Implement advanced AI agent orchestration
# Add intelligent query routing
# Implement sophisticated user feedback system
# Implement advanced memory management
# Implement intelligent backup systems
# Add sophisticated data analytics
# Implement sophisticated CI/CD pipeline
# Add intelligent performance tuning
from typing import Dict, Any, AsyncIterator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.config import RunnableConfig
from .history_manager import DynamoDBChatHistoryManager
from langchain_core.messages import BaseMessage
from langchain_core.runnables import ConfigurableFieldSpec



class RocloRunnableChain:
    """  
    A class to manage the execution of a runnable chain that integrates prompts,  
    language models, and message history management.  
    
    Attributes:  
        runnable_chain (RunnableWithMessageHistory): The runnable chain that combines  
            prompts, language models, and message history.  
    """
    def __init__(
        self,
        data: Dict,
        prompt: ChatPromptTemplate,
        llm: BaseChatModel,
        input_key: str,
        history_key: str,
        name: str
    ) -> RunnableWithMessageHistory:
        """Initialize the RocloRunnableChain with the provided components.  

        Args:  
            data (Dict[str, Any]): The data to be used in the runnable chain.  
            prompt (ChatPromptTemplate): The chat prompt template to be used.  
            llm (BaseChatModel): The language model to be invoked.  
            input_key (str): The key for input messages.  
            history_key (str): The key for history messages.  
            name (str): Name of the agent.
        """
        self.runnable_chain = RunnableWithMessageHistory(
            data | prompt | llm,
            DynamoDBChatHistoryManager.get_chat_history,
            input_messages_key = input_key,
            history_messages_key = history_key,
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="table_id",
                    annotation=str,
                    name="Table ID",
                    description="Unique identifier for the table.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="session_id",
                    annotation=str,
                    name="Session ID",
                    description="Unique identifier for the session.",
                    default="",
                    is_shared=True,
                ),
            ],
        )
        self.name = name



    async def ainvoke(self, input:Dict[str, Any], config:RunnableConfig) -> BaseMessage:
        """Invoke the runnable chain asynchronously with the given input and configuration.  

        Args:  
            input (Dict[str, Any]): The input data for the invocation.  
            config (RunnableConfig): The configuration for the runnable.  

        Returns:  
            BaseMessage: The response from the language model.  

        Raises:  
            Exception: Catches various exceptions that may occur during invocation.  
        """
        try:  
            return await self.runnable_chain.ainvoke(input, config)  
        except Exception as e:
            raise
    


    async def astream(self, input:Dict, config:RunnableConfig) -> AsyncIterator[BaseMessage]:
        """Stream the output of the runnable chain asynchronously.  

        Args:  
            input (Dict[str, Any]): The input data for streaming.  
            config (RunnableConfig): The configuration for the runnable.  

        Returns:  
            Any: The streamed output from the language model.  

        Raises:  
            Exception: Catches various exceptions that may occur during streaming.  
        """
        try:
            async for chunk in self.runnable_chain.astream(input, config):  
                yield chunk # Yield each chunk as it's retrieved.
        except Exception as e:
            raise