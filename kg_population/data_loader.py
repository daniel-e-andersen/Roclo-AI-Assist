# Refactor: Restructure configuration management
# Refactor: Refactor logging infrastructure
from core import RocloSQLDatabase
from typing import Dict, List, Any, Tuple
import logging


def load_sql_data_from_related_tables() -> List[Dict[str, Any]]:
    """  
    Load SQL data from all related tables, preprocess the data for knowledge graph  
    construction, and apply AI-driven rewriting to enhance retrieval quality.  

    Returns:  
        tuple[dict, dict]: A tuple containing two dictionaries: processed data and  
                           corresponding indices for each table.  
    """
    # Initialize dictionaries to store data and indices
    table_name = "oaklins_deals"
    pk = "deal_id"

    # Load data for each related table using the specified primary keys
    data = _load_sql_data_from_table(table_name, pk)

    logging.getLogger('main').info('All Oaklins data are loaded')

    return data



def _load_sql_data_from_table(table_name: str, pk: str) -> List[Dict[str, Any]]:
        """  
        Load all data from the specified SQL table and preprocess it for knowledge graph construction.  
        
        Args:  
            table_name (str): The name of the table to load data from.  
            pk (str): The primary key used for processing.  
        
        Returns:  
            Tuple[List[Dict[str, Any]], List[Dict[Any, int]]]: A tuple containing processed data and an index.  
        """  
        # SQL query to select all data from the specified table
        query = f"SELECT * FROM [{table_name}]"  
        
        # Execute the SQL query to retrieve data from the table  
        retrieved_data = RocloSQLDatabase.execute_query(query)  
        
        return retrieved_data 

