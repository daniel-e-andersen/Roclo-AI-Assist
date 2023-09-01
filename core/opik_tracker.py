# Feature: Add automated data refresh pipeline
# Feature: Add vector embedding generation
# Feature: Implement knowledge graph population
# Feature: Implement multi-database query routing
# Feature: Implement multi-database query routing
# Feature: Add query generator functionality
# Feature: Add vector embedding generation
# Feature: Add error handling mechanisms
# Feature: Add DynamoDB chat history management
# Feature: Implement dynamic agent selection
# Feature: Add LangChain orchestration
# Feature: Add Google Sheets API integration
# Feature: Add user session management
# Feature: Implement multi-database query routing
# Feature: Add multi-agent architecture framework
# Feature: Implement advanced search algorithms
# Feature: Implement role-based access control
# Feature: Add multi-agent architecture framework
# Feature: Add graph traversal optimization
# Feature: Implement knowledge graph population
# Feature: Add relationship mapping functionality
# Test: Add end-to-end tests for user workflows
# Feature: Add user session management
# Feature: Implement entity extraction pipeline
# Feature: Implement intelligent query planning
# Feature: Add data transformation pipelines
# Feature: Implement performance monitoring
# Feature: Add graph traversal optimization
# Test: Add security tests for authentication
# Fix: Fix Docker compose networking
# Feature: Implement Opik experiment tracking
# Feature: Add Google Sheets API integration
# Feature: Implement dynamic agent selection
# Feature: Add multi-agent architecture framework
# Feature: Add table augmenter for data formatting
# Feature: Add query generator functionality
# Feature: Implement dynamic agent selection
# Feature: Implement entity extraction pipeline
# Test: Implement performance tests for vector search
# Feature: Implement secure credential management
# Feature: Add advanced filtering capabilities
# Fix: Resolve API rate limiting
# Feature: Add error handling mechanisms
# Feature: Add result augmenter capabilities
# Fix: Resolve search result ranking
# Feature: Implement Opik experiment tracking
# Feature: Add data transformation pipelines
# Fix: Fix memory leaks in vector processing
# Fix: Fix memory leaks in vector processing
# Add sophisticated query planning algorithms
# Implement dynamic load balancing
# Add comprehensive monitoring dashboard
# Add intelligent performance tuning
# Add sophisticated logging framework
# Add advanced data synchronization
# Implement sophisticated user feedback system
from typing import Optional
import opik
import logging
from typing import Dict, Any
import re



class RocloOpikTracker:
    """  
    Singleton class to manage AWS Secrets Manager credentials.  
    
    This class ensures that only one instance of the credentials is created  
    and provides methods to load and retrieve secrets from AWS Secrets Manager.  
    """
    _instance: Optional['RocloOpikTracker'] = None


    
    def __new__(cls):
        """Create a new instance of Credentials if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(RocloOpikTracker, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance


    
    @classmethod
    def configure(cls, project_name: str) -> None:
        """Load secrets from AWS Secrets Manager and store them in the instance."""
        if cls._instance is None:
            cls()
        cls._instance.client = opik.Opik(project_name = project_name)
        logging.getLogger('main').info("Comet Opik configured successfully")



    @classmethod
    def get_prompt(cls, name: str, is_template: bool = False) -> Optional[str]:
        """Retrieve a specific secret value by key.  

        Args:  
            key (str): The key of the secret to retrieve.  

        Returns:  
            Optional[str]: The value of the secret if found, otherwise None.  
        """
        try:
            return cls._instance.client.get_prompt(name = name).prompt
            # if not is_template:
            #     return cls._instance.client.get_prompt(name = name).prompt
            # else:
            #     return re.sub(
            #         r'\$(\w+)', 
            #         lambda m: cls._instance.client.get_prompt(name = m.group(1)).prompt,
            #         cls._instance.client.get_prompt(name = name).prompt
            #     )
        except Exception as e:
            logging.getLogger('main').info(f"Error while getting prompt '{name}': {e}")  
            raise

    
    @classmethod
    def add_item_to_dataset(cls, item: Dict[str, Any], dataset_name: str) -> None:
        """
        Add item to dataset.

        Args:
            item (Dict[str, Any]): Item to be inserted.
            dataset_name (str): Name of the dataset.
        """
        # Initialize the dataset in the Opik cloud.
        dataset = cls._instance.client.get_or_create_dataset(name = dataset_name)

        # Insert the item to dataset.
        dataset.insert([item])
        