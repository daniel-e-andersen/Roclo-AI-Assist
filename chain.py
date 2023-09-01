# Test: Add validation tests for data integrity
# Test: Add validation tests for data integrity
# Refactor: Refactor query generation logic
# Refactor: Restructure test frameworks
# Refactor: Refactor UI components for reusability
# Test: Implement performance tests for vector search
# Refactor: Refactor authentication system
# Refactor: Refactor UI components for reusability
# Implement advanced security protocols
# Implement intelligent resource allocation
# Implement intelligent backup systems
# Add sophisticated deployment automation
# Add advanced data encryption
# Implement advanced AI agent orchestration
import functools
from typing import Optional
from config import Credentials
from core import (
    AgentState,
    RocloPostgresDatabase,
    RocloSupabaseDatabase,
    RocloMilvusVectorDB,
    DynamoDBChatHistoryManager,
    RocloOpikTracker
)
from agents import (
    rational_planner,
    query_generator,
    value_mapper,
    result_augmenter,
    plain_augmenter,
    table_augmenter,
    db_retriever,
    routing_from_rational_planner,
    routing_from_db_retriever,
    prioritizer
)
from build import (
    create_query_generator_chain,
    create_result_augmenter_chain,
    create_rational_planner_chain,
    create_plain_augmenter_chain,
    create_table_augmenter_chain,
    create_prioritizer_chain
)
from logger import setup_logger
import asyncio
from langgraph.graph import END, StateGraph
import logging
from langchain_core.messages import HumanMessage
from opik.api_objects.trace import Trace
from typing import Dict, Any


class RocloChatbotChain:
    """  
    Main chain of the Roclo Chatbot, responsible for building and managing the workflow.  
    """
    _instance: Optional['RocloChatbotChain'] = None

    def __new__(cls):
        """Create a new instance of RocloChatbotChain if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloChatbotChain, cls).__new__(cls)
        return cls._instance
    

    @classmethod
    def build_workflow(cls) -> None:
        """
        Build the multi-agent workflow for the chatbot.
        """
        if cls._instance is None:
            cls()

        try:
            # Setup main logger
            setup_logger()
            
            # Build the Credentials.
            Credentials.set_secrets()

            # Build the chat history manager.
            DynamoDBChatHistoryManager.connect()

            # Initialize the Roclo Postgres Database.
            RocloPostgresDatabase.connect()

            # Initialize the Roclo Supabase Database.
            RocloSupabaseDatabase.connect()

            # Initialize the Roclo Milvus Database.
            RocloMilvusVectorDB.connect()

            # initialize the Opik Tacer.
            RocloOpikTracker.configure(project_name = 'Oaklins')

            # Define the agents nodes.
            cls._define_nodes()
            cls._instance.workflow = StateGraph(AgentState)

            # Add nodes to worflow.
            cls._add_workflow_nodes()

            # Define edges between nodes.
            cls._define_workflow_edges()

            # Build the agent graph.
            cls._instance.agent_graph = cls._instance.workflow.compile()

            logging.getLogger('main').info("Agent Graph builded. Let's start chat!")

        except Exception as e:
            logging.getLogger('main').error(f"Error while building the agents workflow: {e}")
            raise
        
    
    @classmethod
    def _define_nodes(cls) -> None:
        """Define the agent nodes"""
        try:
            cls._instance.rational_planner = functools.partial(
                rational_planner,
                chain = create_rational_planner_chain()
            )
            cls._instance.query_generator = functools.partial(
                query_generator,
                chain = create_query_generator_chain()
            )
            cls._instance.result_augmenter = functools.partial(
                result_augmenter,
                chain = create_result_augmenter_chain()
            )
            cls._instance.plain_augmenter = functools.partial(
                plain_augmenter,
                chain = create_plain_augmenter_chain()
            )
            cls._instance.table_augmenter = functools.partial(
                table_augmenter,
                chain = create_table_augmenter_chain()
            )
            cls._instance.db_retriever = db_retriever
            cls._instance.prioritizer = functools.partial(
                prioritizer,
                chain = create_prioritizer_chain()
            )

        except Exception as e:
            logging.getLogger('main').error(f"Error while creating agent nodes: {e}")
            raise



    @classmethod
    def _add_workflow_nodes(cls) -> None:
        """  
        Add nodes to the workflow.  
        """ 
        try:
            cls._instance.workflow.add_node("rational_planner", cls._instance.rational_planner)
            cls._instance.workflow.add_node("query_generator", cls._instance.query_generator)
            cls._instance.workflow.add_node("result_augmenter", cls._instance.result_augmenter)
            cls._instance.workflow.add_node("plain_augmenter", cls._instance.plain_augmenter)
            cls._instance.workflow.add_node("table_augmenter", cls._instance.table_augmenter)
            cls._instance.workflow.add_node("db_retriever", cls._instance.db_retriever)
            cls._instance.workflow.add_node("prioritizer", cls._instance.prioritizer)
        except Exception as e:
            logging.getLogger('main').error(f"Error while adding nodes to workflow: {e}")
            raise

    @classmethod
    def _define_workflow_edges(cls) -> None:
        """  
        Define edges between nodes in the workflow.  
        """
        try:
            cls._instance.workflow.set_entry_point("rational_planner")
            cls._instance.workflow.add_conditional_edges(
                "rational_planner",
                routing_from_rational_planner,
                {
                    "__continue__":"query_generator",
                    "__end__":"plain_augmenter"
                }
            )
            cls._instance.workflow.add_edge("query_generator", "db_retriever")
            cls._instance.workflow.add_conditional_edges(
                "db_retriever",
                routing_from_db_retriever,
                {
                    "query_generator":"query_generator",
                    "plain_augmenter":"plain_augmenter",
                    "prioritizer": "prioritizer",
                    "__end__": END
                }
            )
            cls._instance.workflow.add_edge("plain_augmenter", END)
            cls._instance.workflow.add_edge("prioritizer", "table_augmenter")
            cls._instance.workflow.add_edge("table_augmenter", END)
        except Exception as e:
            logging.getLogger('main').error(f"Error while defining edges between nodes: {e}")
            raise


    @classmethod
    async def ainvoke(
        cls,
        user_id: str,
        session_id: str,
        message: str,
        trace: Trace
    ) -> Dict[str, Any]:
        """
        Invoke the agent workflow.

        Args:
            user_id (str): User identifier.
            session_id (str): Session identifier.
            message (str): User question.
            logger (logging.Logger): logger.
        """
        return await cls._instance.agent_graph.ainvoke(
            {
                "messages": HumanMessage(content = message),
                "user_id": user_id,
                "session_id": session_id,
                "sender": "human",
                "trace":trace
            }
        )


        
