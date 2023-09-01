# Feature: Add LangChain orchestration
# Feature: Add AWS Bedrock integration
# Feature: Add advanced filtering capabilities
# Feature: Implement plain augmenter for simple queries
# Feature: Add conversation flow management
# Feature: Add vector embedding generation
# Feature: Implement Cerebras AI support
# Feature: Add error handling mechanisms
# Feature: Add response caching mechanism
# Feature: Add vector embedding generation
# Feature: Implement entity extraction pipeline
# Feature: Add PostgreSQL database operations
# Feature: Add vector index maintenance
# Feature: Implement Supabase authentication
# Feature: Implement hybrid search functionality
# Feature: Implement Chainlit UI interface
# Feature: Add error handling mechanisms
# Feature: Add Google Sheets API integration
# Feature: Add AWS Bedrock integration
# Feature: Implement advanced search algorithms
# Fix: Resolve query generation edge cases
# Feature: Implement real-time data synchronization
# Feature: Add multi-agent architecture framework
# Feature: Add advanced filtering capabilities
# Feature: Implement secure credential management
# Feature: Implement chat history persistence
# Feature: Add error handling mechanisms
# Fix: Resolve Neo4j connection pooling issues
# Fix: Resolve AWS credentials rotation
# Test: Add regression tests for critical paths
# Fix: Fix relationship mapping errors
# Fix: Fix memory leaks in vector processing
# Feature: Add Google Sheets API integration
# Feature: Implement hybrid search functionality
# Feature: Add graph traversal optimization
# Feature: Add data transformation pipelines
# Fix: Resolve search result ranking
# Feature: Add automated data refresh pipeline
# Fix: Fix query parsing errors
# Feature: Implement prioritizer for data sources
# Feature: Implement multi-database query routing
# Feature: Implement prioritizer for data sources
# Feature: Add multi-agent architecture framework
# Test: Implement mock tests for external services
# Feature: Add automated data refresh pipeline
# Feature: Add vector embedding generation
# Feature: Add batch processing for large datasets
# Feature: Add AWS Bedrock integration
# Feature: Implement advanced search algorithms
# Fix: Resolve query generation edge cases
# Refactor: Refactor security implementations
from typing import Optional
from config import Credentials
from typing import Dict, Any, List
from pymilvus import MilvusClient
from kg_population.vector_calculator.vector_schmea import vector_schema
from kg_population.vector_calculator.embedding_function import JinaEmbeddingFunction
import logging

class RocloMilvusVectorDB:
    """  
    Singleton class to manage Roclo SQL database.  
    
    This class ensures that only one instance of the sql database is created  
    and provides methods to excute the cypher query and returns the result.  
    """
    _instance: Optional['RocloMilvusVectorDB'] = None

    def __new__(cls):
        """Create a new instance of RocloGraphDatabase if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloMilvusVectorDB, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance
    

    @classmethod
    def connect(cls):
        """Initialize the connection to the Neo4j GraphDB."""
        if cls._instance is None:
            cls()

        try:
            cls._instance.client = MilvusClient(
                uri = Credentials.get_secret("MILVUS_URI")
            )
            # Define the Jina embedding function.
            cls._instance.ef = JinaEmbeddingFunction(
                vector_schema['values']['model'],
                Credentials.get_secret("JINAAI_API_KEY"),
                task = vector_schema['values']['task'],
                dimensions = vector_schema['values']['dimensions']
            )
            collection_name = vector_schema['collection_name']
            if cls._instance.client.has_collection(collection_name):
                RocloMilvusVectorDB.load_collection(collection_name)
                logging.getLogger('main').info(f"Loaded Milvus {collection_name} collection.")
            logging.getLogger('main').info("Milvus Vector Database connected.")
        except Exception as e:
            logging.getLogger('main').info("Failed to connect to Milvus Vector database: %s", e)
            raise

            
    
    @classmethod
    def create_collection(cls, collection: Dict[str, Any]) -> None:
        """
        Create the collection.

        Args:
            collection_name (str): Name of the collection.
        """
        collection_name = collection['collection_name']

        if cls._instance.client.has_collection(collection_name):
            cls._instance.client.drop_collection(collection_name=collection_name)
            logging.getLogger('main').info(f"Dropped existing collection: {collection_name}")

        # Create schema.
        schema = cls._create_schema(collection["schema"])
        # Create index params.   
        index_params = cls._create_index_params(collection["index_params"])
        print(index_params)

        # Create collection
        cls._instance.client.create_collection(
            collection_name=collection_name,
            schema=schema
        )
        logging.getLogger('main').info(f"Created collection: {collection_name}")

        # Create indexes separately
        cls._instance.client.create_index(
            collection_name=collection_name,
            index_params=index_params,
            sync=False
        )
        logging.getLogger('main').info(f"Index {collection['collection_name']} created.")


    @classmethod
    def _create_schema(cls, schema: Dict[str, Any]) -> Any:
        """
        Create the schema.
        """
        milvus_schema = MilvusClient.create_schema(
            auto_id = schema['auto_id'],
            enable_dynamic_field = schema['enable_dynamic_field']
        )
        for field in schema['schema']:
            milvus_schema.add_field(**field)

        return milvus_schema


    @classmethod
    def _create_index_params(cls, index_params: List[Dict[str, str]]) -> Any:
        """
        Create Milvus index params.
        """
        milvus_index_params = MilvusClient.prepare_index_params()
        for param in index_params:
            milvus_index_params.add_index(**param)

        return milvus_index_params


    @classmethod
    def insert_data(cls, collection_name: str, data: List[Dict[str, Any]]) -> None:
        """
        Insert data into Milvus

        Args:
            collection_name (str): Name of the collection
            vector_data (Dict[str, Any]): Data to be inserted.
        """
        cls._instance.client.insert(
            collection_name = collection_name,
            data = data
        )

    
    @classmethod
    def release_collection(cls, collection_name: str) -> None:
        """Release the collection"""
        cls._instance.client.release_collection(
            collection_name= collection_name
        )

    @classmethod
    def load_collection(cls, collection_name: str) -> None:
        """Load the collection"""
        cls._instance.client.load_collection(
            collection_name= collection_name
        )

    @classmethod
    def search_data(cls, query_str:str, collection_name: str, filter_deals: List, selction_list: List = ["id", "deal_id", "text", "title"], distance_threshold: float = 0) -> List:
        """Similarity Search"""
        # embedding
        query_vector = cls._instance.ef.encode_documents([query_str])

        # search
        results = cls._instance.client.search(
            collection_name=collection_name,
            data=query_vector,
            limit=100,
            filter=f"deal_id in {filter_deals}",
            # search_params={
            #     "metric_type": "COSINE",
            #     "params": {"ef": 64}  # or other params depending on index type
            # },
            output_fields=selction_list
        )[0]

        print(results)

        # Filter if threshold
        if distance_threshold:
            filtered_results = [hit for hit in results if hit['distance'] >= distance_threshold]
            logging.getLogger('main').info("filtered by threshold at %s", distance_threshold)
            if len(filtered_results) > 3:
                results = filtered_results
        
        return results