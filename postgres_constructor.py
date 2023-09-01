from config import Credentials
from core import (
    RocloSQLDatabase,
    RocloPostgresDatabase
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
    RocloPostgresDatabase.connect()
    # RocloMilvusVectorDB.connect()
except Exception as e:
    print(e)
    exit()

from kg_population.data_loader import load_sql_data_from_related_tables
from utils import postgres_table_schema
from kg_population.vector_indexer import index_vector
# from kg_population.vector_indexer import index_vector


def main() -> None:
    """
    Extract the knowledge graph from SQL database, and index it into Neo4j.
    """
    logging.getLogger('main').info("Started Postgres Construction.")

    # Load the data from SQL database.
    data = load_sql_data_from_related_tables()
    
    # Create the table
    RocloPostgresDatabase._create_table(postgres_table_schema)

    # Insert data
    RocloPostgresDatabase._insert_data(postgres_table_schema, data)
    
    logging.getLogger('main').info("Completed Postgres Construction.")



if __name__ == '__main__':
    main()
