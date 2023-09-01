# Test: Implement stress tests for system limits
# Test: Implement performance tests for vector search
# Refactor: Restructure configuration management
# Refactor: Restructure data processing pipeline
# Refactor: Refactor UI components for reusability
# Refactor: Optimize vector search algorithms
# Refactor: Optimize vector search algorithms
# Refactor: Optimize caching strategies
# Refactor: Refactor logging infrastructure
from core import RocloGraphDatabase
from utils import (
    run_command
)
import logging


async def populate_knowledge_graph() -> None:
    """
    Populate the knowledge graph from the extracted entities (files).
    """
    # Delete the database on the Neo4j if exists
    await RocloGraphDatabase.execute_query("DROP DATABASE cavendish IF EXISTS", 'delete')
    logging.getLogger('main').info("Database deleted")

    # Remove the database installation folder if exists
    run_command("sudo rm -rf /var/lib/neo4j/data/databases/cavendish")
    run_command("sudo rm -rf /var/lib/neo4j/data/transactions/cavendish")

    # Change the permission of index.sh
    run_command("sudo chmod 775 ~/Documents/Roclo/GraphRAG/kg_population/graph_transformer/outputs/index.sh")

    # Index the extracted entities (nodes and relationships)
    run_command("cd ~/Documents/Roclo/GraphRAG/kg_population/graph_transformer/outputs/ && ./index.sh")

    # Modify the ownership of the database folder
    run_command("sudo chown neo4j:neo4j -R /var/lib/neo4j/data/databases/cavendish")
    run_command("sudo chown neo4j:neo4j -R /var/lib/neo4j/data/transactions/cavendish")

    # Create the database on Neo4j
    await RocloGraphDatabase.execute_query("CREATE DATABASE cavendish", 'create')
    logging.getLogger('main').info("Database created")

    # Create the indexes
    await _create_neo4j_indexes()


async def _create_neo4j_indexes() -> None:
    """
    Create the neo4j indexes(Search performance & Full-text) based on the writted cypher query.
    """
    # Connect to created database on Neo4j.
    RocloGraphDatabase.connect()

    # Read the writted cypher queries to create indexes
    with open('kg_population/graph_transformer/outputs/cypher.txt', 'r') as file:  
        content = file.read()  

    # Split the content by double newline and strip whitespace from each query  
    queries = [query.strip() for query in content.split('\n\n') if query.strip()]

    # Execute the queries
    for query in queries:
        await RocloGraphDatabase.execute_query(query, 'create')

    logging.getLogger('main').info("All indexes are created.")