from config import Credentials
from core import (
    RocloSQLDatabase,
    RocloMilvusVectorDB
)
import asyncio
from logger import setup_logger
import logging


# Initialize the core functionalities.
try:
    # Initialize the logger.
    setup_logger()
    
    Credentials.set_secrets()
    RocloSQLDatabase.connect()
    RocloMilvusVectorDB.connect()
    # RocloMilvusVectorDB.connect()
except Exception as e:
    print(e)
    exit()

from kg_population.data_loader import load_sql_data_from_related_tables
from kg_population.vector_indexer import index_vector
# from kg_population.vector_indexer import index_vector


def main() -> None:
    """
    Extract the knowledge graph from SQL database, and index it into Neo4j.
    """
    logging.getLogger('main').info("Started Knowledge Graph population.")

    # Load the data from SQL database.
    data = load_sql_data_from_related_tables()
    print(data[0].keys())

    # Index the vector to Milvus for company descriptions, project comments, opportunity notes and activities.
    # index_vector(data)
    # print(data[0])
    # print(len(data))

    logging.getLogger('main').info("Completed Knowledge Graph population.")



if __name__ == '__main__':
    main()
