# Test: Implement stress tests for system limits
# Refactor: Restructure configuration management
# Refactor: Restructure data processing pipeline
# Refactor: Optimize vector search algorithms
# Refactor: Optimize caching strategies
from tqdm import tqdm
from kg_population.vector_calculator.vector_schmea import vector_schema
from kg_population.vector_calculator.embedding_function import JinaEmbeddingFunction
from typing import List, Dict, Any
from core import RocloMilvusVectorDB
from config import Credentials
from utils import (
    get_business_descriptions_for_oaklins,
    split_dict_with_text_list
)
import logging

def index_vector(data: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Index the vector to Milvus.

    Args:
        data (List[Dict[str, Any]]): Data need to be indexed.
    """
    # Create the collection.
    RocloMilvusVectorDB.create_collection(vector_schema)
    logging.getLogger('main').info(f"Indexing {vector_schema['collection_name']}...")

    # Get descriptions from data
    business_descriptions = get_business_descriptions_for_oaklins(data, vector_schema['values']['target_keys'])
    logging.getLogger('main').info(f"Got descriptions from Oaklins, Size is {len(business_descriptions)}")

    # Define the Jina embedding function.
    ef = JinaEmbeddingFunction(
        vector_schema['values']['model'],
        Credentials.get_secret("JINAAI_API_KEY"),
        task = vector_schema['values']['task'],
        dimensions = vector_schema['values']['dimensions']
    )

    # Calculating jinaai embeddings from input file by send batch request.
    progress_bar = tqdm(
        total = len(business_descriptions)//512 + 1, 
        desc = f"----Indexing {vector_schema['collection_name']}..."
    )
    for i in range(0,len(business_descriptions), 512):
        batch_data = business_descriptions[i:i+512]
        devcs = ef.encode_documents([doc[vector_schema['values']['vector_col']] for doc in batch_data])
        vector_data = [
            {**{k: batch_data[i][k] for k in vector_schema['values']['metadata']}, "vector":devcs[i]}
            for i in range(len(batch_data))
        ]
        RocloMilvusVectorDB.insert_data(
            collection_name=vector_schema['collection_name'],
            data = vector_data
        )
        progress_bar.update(1)

    RocloMilvusVectorDB.release_collection(collection_name= vector_schema['collection_name'])

    logging.getLogger('main').info(f"{vector_schema['collection_name']} indexed.")