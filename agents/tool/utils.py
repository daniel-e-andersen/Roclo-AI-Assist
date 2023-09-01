# Feature: Add query generator functionality
# Feature: Add vector embedding generation
# Feature: Implement multi-database query routing
# Feature: Add AWS Bedrock integration
# Feature: Add vector embedding generation
# Feature: Implement custom embedding models
# Feature: Add query generator functionality
# Feature: Add error handling mechanisms
# Feature: Add response caching mechanism
# Feature: Add error handling mechanisms
# Feature: Implement intelligent query planning
# Feature: Add Google Sheets API integration
# Feature: Add batch processing for large datasets
# Feature: Add PostgreSQL database operations
# Feature: Add comprehensive logging system
# Feature: Add LangChain orchestration
# Feature: Add data validation and sanitization
# Fix: Fix memory leaks in vector processing
# Feature: Implement Chainlit UI interface
# Fix: Resolve concurrent access problems
# Feature: Add query generator functionality
# Test: Implement performance tests for vector search
# Feature: Add multi-agent architecture framework
# Feature: Add advanced filtering capabilities
# Feature: Add PostgreSQL database operations
# Feature: Implement Chainlit UI interface
# Feature: Implement dynamic agent selection
# Feature: Add user session management
# Feature: Implement intelligent query planning
# Feature: Implement chat history persistence
# Feature: Implement entity extraction pipeline
# Feature: Add data validation and sanitization
# Feature: Add table augmenter for data formatting
# Feature: Add data transformation pipelines
# Fix: Fix cache invalidation logic
# Feature: Add data transformation pipelines
# Feature: Implement Milvus vector database support
# Fix: Resolve vector similarity calculation
# Fix: Resolve timeout configuration
# Feature: Implement custom embedding models
# Test: Implement mock tests for external services
# Feature: Implement dynamic agent selection
# Feature: Implement Chainlit UI interface
# Feature: Add table augmenter for data formatting
# Feature: Add advanced filtering capabilities
# Fix: Resolve entity extraction failures
# Feature: Add query generator functionality
# Feature: Implement entity extraction pipeline
# Feature: Implement prioritizer for data sources
# Feature: Implement secure credential management
# Feature: Implement prioritizer for data sources
# Feature: Add multi-agent architecture framework
# Feature: Add Neo4j knowledge graph integration
# Feature: Add LangChain orchestration
# Feature: Implement advanced search algorithms
# Fix: Resolve memory optimization
# Feature: Add user feedback collection
# Fix: Fix relationship mapping errors
import logging
from core.graph_database import RocloGraphDatabase
from agents.tool.fulltext_field import (
    fulltext_node_fields,
    fulltext_relationship_fields
)
import chainlit as cl
from core import DynamoDBChatHistoryManager
from typing import List, Optional
from dataclasses import dataclass
from utils import (
    get_value_list_from_data
)


@dataclass
class RocloEntity:
    variable: str
    label: str
    prop: str
    value: str
    entity_type: str
    user_id: str
    session_id: str
    match_type: str

    def __post_init__(self):
        # Intialize the key patterns of match query.
        if self.entity_type == 'node':
            self.match_query = f"(n:{self.label})"
            self.fulltext_index_name = "fulltext_" + f"{self.label}_{self.prop}".lower()
            self.is_fulltext_index = fulltext_node_fields[f"{self.label}_{self.prop}".lower()]
        else:
            self.match_query = f"()-[n:{self.label}]-()"
            self.fulltext_index_name = fulltext_relationship_fields[f"{self.label}_{self.prop}".lower()]['name']
            self.is_fulltext_index = fulltext_relationship_fields[f"{self.label}_{self.prop}".lower()]['fulltext_index']
        
        # Exact match query.
        self.exact_match_query = f"MATCH {self.match_query} WHERE n.{self.prop} = '{self.value}' RETURN n.{self.prop} LIMIT 1"

        # Fulltext query.
        if self.is_fulltext_index:
            if self.entity_type == 'node':
                self.fulltext_query = f"CALL db.index.fulltext.queryNodes('{self.fulltext_index_name}', '{self.value}') YIELD node as n, score RETURN n.{self.prop} LIMIT 4"
            else:
                self.fulltext_query = f"CALL db.index.fulltext.queryRelationships('{self.fulltext_index_name}', '{self.value}') YIELD relationship as n, score RETURN n.{self.prop} LIMIT 4"

        # Levenshtein similarity query which minimum similarity score is 0.3.
        self.similarity_query = f"MATCH {self.match_query} WITH n, apoc.text.levenshteinSimilarity(n.{self.prop}, '{self.value}') as similarity " +\
        f"WHERE similarity > 0.3 AND n.{self.prop} IS NOT NULL " +\
        f"RETURN n.{self.prop} ORDER BY similarity DESC LIMIT 4"

        # levenshtein similarity query without any limitation.
        self.all_similarity_query = f"MATCH {self.match_query} WITH n, apoc.text.levenshteinSimilarity(n.{self.prop}, '{self.value}') as similarity " +\
        f"WHERE n.{self.prop} IS NOT NULL " +\
        f"RETURN n.{self.prop} ORDER BY similarity DESC LIMIT 4"


    async def map_graph_value(self) -> 'RocloEntity':
        """
        Core of the value mapper tool.

        Make the cypher query to map the graph value and returns most relevant value.
        """
        # Step 1: Perform exact match.
        exact_match_result = await RocloGraphDatabase.execute_query(self.exact_match_query)
        if exact_match_result:
            self.mapped_value, self.map_type = self.value, 'exact'
            return
        
        # Step 2: Get the mapped value in the chat session from Postgres.
        cached_mapped_value = self._get_stored_mapped_value()
        if cached_mapped_value:
            self.mapped_value, self.map_type = cached_mapped_value, 'cache'
            return
        
        # Step 3: Perform full-text search.
        if self.is_fulltext_index:
            fulltext_result = await RocloGraphDatabase.execute_query(self.fulltext_query)
            if fulltext_result:
                mapped_value = await self._get_user_action(f"Did you mean ({self.label}'s {self.prop}):", get_value_list_from_data(fulltext_result))
                if mapped_value != 'Others':
                    self.mapped_value, self.map_type = mapped_value, 'fulltext'
                    self._store_mapped_value()
                    return
        
        # Step 4: Perform levenshtein similarity search where the similarity is bigger than 0.3.
        similarity_result = await RocloGraphDatabase.execute_query(self.similarity_query)
        if similarity_result != {}:
            mapped_value = await self._get_user_action(f"Did you mean ({self.label}'s {self.prop}):", get_value_list_from_data(similarity_result))
            if mapped_value != 'Others':
                self.mapped_value, self.map_type = mapped_value, 'leven'
                self._store_mapped_value()
                return


        # Step 5: Perform levenshtein similarity search without any condition.
        all_similarity_result = await RocloGraphDatabase.execute_query(self.all_similarity_query)
        mapped_value = await self._get_user_action(f"Did you mean ({self.label}'s {self.prop}):", get_value_list_from_data(all_similarity_result), False)
        self.mapped_value, self.map_type = mapped_value, 'leven_all'
        self._store_mapped_value()
        return
    
    
    def _get_stored_mapped_value(self) -> Optional[str]:
        """
        Get the mapped value stored on the Postgres. 
        If not exist, returns None.
        """
        return DynamoDBChatHistoryManager.get_mapped_value(self.session_id, self.label, self.prop, self.value)

    
    def _store_mapped_value(self) -> 'RocloEntity':
        """
        Store the mapped value to Postgres.
        """
        DynamoDBChatHistoryManager.add_mapped_value(
            {
                "session_id": self.session_id,
                "label": self.label,
                "prop": self.prop,
                "old_value": self.value,
                "new_value": self.mapped_value
            }
        )
    

    async def _get_user_action(self, content: str, values: List[str], append_to_others: bool=True) -> str:
        """
        If the different mapped value found, ask the user, and returns selected value by the user.

        Args:
            content (str): Content of the ask message.
            values (List[str]): List of the value need to be selected by the user.

        Returns:
            str: User selected value.
        """
        # Append others to values.
        if append_to_others:
            values.append('Others')

        res = await cl.AskActionMessage(
            content = content,
            actions = [cl.Action(name = value, payload = {"value": value}, label = value) for value in values],
            timeout = 120
        ).send()

        # If the user select the value, returns this value.
        if res:
            return res.get("payload").get('value')
        

    def update_query(self, cypher_query: str) -> str:  
        """  
        Updates the Cypher query and state with the mapped value.
        """  
        logging.getLogger(f"{self.user_id}-{self.session_id}").info("Value mapped from '%s' to '%s'. label: %s, prop: %s, map_type: %s", self.value, self.mapped_value, self.label, self.prop, self.map_type)

        if self.match_type == "match":
            return cypher_query.replace(
                f"{self.variable}:{self.label} {{{self.prop}: '{self.value}'}}", f"{self.variable}:{self.label} {{{self.prop}: '{self.mapped_value}'}}"
            ).replace(
                f'{self.variable}:{self.label} {{{self.prop}: "{self.value}"}}', f'{self.variable}:{self.label} {{{self.prop}: "{self.mapped_value}"}}'
            )
        else:
            return cypher_query.replace(
                f"{self.variable}.{self.prop} = '{self.value}'", f"{self.variable}.{self.prop} = '{self.mapped_value}'"
            ).replace(
                f'{self.variable}.{self.prop} = "{self.value}"', f'{self.variable}.{self.prop} = "{self.mapped_value}"'
            )
    