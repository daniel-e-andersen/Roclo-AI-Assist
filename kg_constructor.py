from config import Credentials
from core import (
    RocloSQLDatabase,
    RocloOpikTracker,
    RocloGraphDatabase,
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
    RocloOpikTracker.configure(project_name = 'Oaklins')
    # RocloMilvusVectorDB.connect()
    RocloGraphDatabase.connect(database = 'neo4j')
except Exception as e:
    print(e)
    exit()

from kg_population.data_loader import load_sql_data_from_related_tables
from kg_population.entity_extractor import extract_entities
from kg_population.kg_populator import populate_knowledge_graph
# from kg_population.vector_indexer import index_vector


def main() -> None:
    """
    Extract the knowledge graph from SQL database, and index it into Neo4j.
    """
    logging.getLogger('main').info("Started Knowledge Graph population.")

    # Load the data from SQL database.
    data, data_index = load_sql_data_from_related_tables()

    # Extract entities from loaded data and save it by CSV file.
    extract_entities(data.copy(), data_index)

    # Populate the knowledge graph from the extracted entities.
    asyncio.run(populate_knowledge_graph())

    # Index the vector to Milvus for company descriptions, project comments, opportunity notes and activities.
    # index_vector(data)

    logging.getLogger('main').info("Completed Knowledge Graph population.")



if __name__ == '__main__':
    main()
