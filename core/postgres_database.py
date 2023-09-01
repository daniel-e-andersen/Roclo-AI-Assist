# Feature: Implement prioritizer for data sources
# Feature: Add LangChain orchestration
# Feature: Implement plain augmenter for simple queries
# Feature: Implement Chainlit UI interface
# Feature: Implement multi-database query routing
# Feature: Add query generator functionality
# Feature: Add response caching mechanism
# Feature: Implement advanced search algorithms
# Feature: Add error handling mechanisms
# Feature: Implement Supabase authentication
# Test: Implement stress tests for system limits
# Feature: Add comprehensive logging system
# Feature: Implement secure credential management
# Feature: Add automated data refresh pipeline
# Fix: Resolve timeout configuration
# Feature: Add user feedback collection
# Feature: Implement data retriever agent
# Feature: Add PostgreSQL database operations
# Feature: Implement hybrid search functionality
# Fix: Resolve memory optimization
# Feature: Add query generator functionality
# Feature: Add relationship mapping functionality
# Feature: Add user session management
# Feature: Implement chat history persistence
# Feature: Implement hybrid search functionality
# Feature: Implement secure credential management
# Feature: Implement performance monitoring
# Feature: Add PostgreSQL database operations
# Feature: Add automated data refresh pipeline
# Feature: Add result augmenter capabilities
# Fix: Fix Milvus index corruption
# Feature: Implement advanced search algorithms
# Test: Add end-to-end tests for user workflows
# Feature: Implement hybrid search functionality
# Feature: Add table augmenter for data formatting
# Feature: Add advanced filtering capabilities
# Feature: Add vector index maintenance
# Feature: Add query generator functionality
# Feature: Add error handling mechanisms
# Feature: Add data validation and sanitization
# Fix: Fix relationship mapping errors
# Fix: Resolve query generation edge cases
# Fix: Fix query parsing errors
# Fix: Resolve timeout configuration
# Fix: Resolve concurrent access problems
# Feature: Implement role-based access control
# Feature: Add Neo4j knowledge graph integration
# Fix: Fix Chainlit UI rendering problems
# Feature: Add comprehensive logging system
# Fix: Resolve memory optimization
# Fix: Resolve query generation edge cases
# Fix: Resolve LangChain callback errors
# Feature: Add data transformation pipelines
# Feature: Implement custom embedding models
# Feature: Add comprehensive logging system
# Feature: Add result augmenter capabilities
# Refactor: Optimize memory usage patterns
import psycopg
from config import Credentials
from typing import Optional, Dict, Any
import logging
from tqdm import tqdm

class RocloPostgresDatabase:
    """
    Singleton class to manage Roclo Postgres database.
    """
    _instance: Optional['RocloPostgresDatabase'] = None

    def __new__(cls):
        """Create a new instance if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloPostgresDatabase, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance
    
    @classmethod
    def connect(cls):
        """Initialize the connection to the Postgres."""
        if cls._instance is None:
            cls()
        
        try:
            cls._instance.connection = psycopg.connect(
                dbname=Credentials.get_secret("POSTGRES_DBNAME"),
                user=Credentials.get_secret("POSTGRES_USER"),
                password=Credentials.get_secret("POSTGRES_PASSWORD"),
                host=Credentials.get_secret("POSTGRES_HOST")
            )
            cls._instance.cursor = cls._instance.connection.cursor()
            logging.getLogger('main').info("Postgres Database connected.")
        except Exception as e:
            logging.getLogger('main').info("Failed to connect to Postgres database: %s", e)
            raise

    @classmethod
    def _close_connection(cls):
        """Close the Postgres connection"""
        if cls._instance.connection:
            cls._instance.connection.close()

    @classmethod
    def _create_table(cls, table_schema: Dict[str, Any]) -> None:
        """
        Create the table
        """
        # Drop the table if it exists
        cls._instance.cursor.execute(f"DROP TABLE IF EXISTS {table_schema['table_name']};")
        logging.getLogger('main').info(f"Dropped table: {table_schema['table_name']}")

        # Create a new table
        cls._instance.cursor.execute(table_schema['creation_sql'])
        logging.getLogger('main').info(f"Created table: {table_schema['table_name']}")

        # Create the Indexes
        cls._instance.cursor.execute(table_schema['index_sql'])
        logging.getLogger('main').info(f"Index {table_schema['table_name']} created.")

    @classmethod
    def _insert_data(cls, table_schema: Dict[str, Any], data):
        """
        Insert data in batches of 20 with upsert (on conflict do update).
        Ensures no duplicate conflict keys in the same batch.
        """

        def chunked(iterable, chunk_size):
            for i in range(0, len(iterable), chunk_size):
                yield iterable[i:i + chunk_size]

        if not data:
            return

        columns = list(data[0].keys())
        col_names = ", ".join(columns)
        row_placeholder = "(" + ", ".join(["%s"] * len(columns)) + ")"
        update_clause = ", ".join([f"{col}=EXCLUDED.{col}" for col in columns if col != 'deal_id'])

        for chunk in tqdm(chunked(data, 20), total=(len(data) + 19) // 20, desc="Inserting"):
            # Deduplicate chunk by 'deal_id'
            seen_ids = set()
            deduped_chunk = []
            for row in reversed(chunk):  # reversed to keep the *last* occurrence
                row_id = row['deal_id']
                if row_id not in seen_ids:
                    seen_ids.add(row_id)
                    deduped_chunk.append(row)
            deduped_chunk.reverse()  # reverse back to preserve order

            if not deduped_chunk:
                continue

            values_flat = [value for row in deduped_chunk for value in [row[col] for col in columns]]
            placeholders = ", ".join([row_placeholder] * len(deduped_chunk))

            sql = f"""
                INSERT INTO {table_schema['table_name']} ({col_names})
                VALUES {placeholders}
                ON CONFLICT (deal_id) DO UPDATE SET {update_clause}
            """

            try:
                cls._instance.cursor.execute(sql, values_flat)
            except Exception as e:
                logging.getLogger('main').info(f"Exception Occurred while execuintg inserting query: {e}")

        cls._instance.connection.commit()
    
    @classmethod
    async def execute_query(cls, query: str) -> Dict:
        """
        Execute the cypher query and returns the records as dict.
        """
        try:
            cls._instance.cursor.execute(query)
            results = cls._instance.cursor.fetchall()

            columns = [desc[0] for desc in cls._instance.cursor.description]

            data = [dict(zip(columns, row)) for row in results]

            return data
        
        except Exception as e:
            logging.getLogger('main').info(f"Exception Occurred: {e}")
            raise
    
    @classmethod
    async def rollback(cls) -> Dict:
        """
        Rollback the transactions
        """
        print("rollbacking")
        cls._instance.connection.rollback()
        logging.getLogger('main').info("Rollback is passed")