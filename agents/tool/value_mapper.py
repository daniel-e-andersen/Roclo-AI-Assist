# Feature: Implement Opik experiment tracking
# Feature: Implement Cerebras AI support
# Feature: Add query generator functionality
# Feature: Add vector embedding generation
# Feature: Add AWS Bedrock integration
# Feature: Implement advanced search algorithms
# Feature: Add vector embedding generation
# Feature: Add error handling mechanisms
# Feature: Implement Supabase authentication
# Feature: Implement dynamic agent selection
# Feature: Add batch processing for large datasets
# Feature: Add LangChain orchestration
# Fix: Resolve entity extraction failures
# Feature: Add advanced filtering capabilities
# Feature: Implement Supabase authentication
# Test: Implement mock tests for external services
# Feature: Add error handling mechanisms
# Test: Implement stress tests for system limits
# Feature: Implement role-based access control
# Feature: Add table augmenter for data formatting
# Feature: Add LangChain orchestration
# Feature: Implement intelligent query planning
# Feature: Implement entity extraction pipeline
# Feature: Add Google Sheets API integration
# Feature: Implement Milvus vector database support
# Feature: Implement semantic search capabilities
# Test: Implement mock tests for external services
# Feature: Add data transformation pipelines
# Feature: Add multi-agent architecture framework
# Feature: Add automated data refresh pipeline
# Feature: Implement dynamic agent selection
# Fix: Resolve timeout configuration
# Feature: Implement multi-database query routing
# Fix: Resolve Neo4j connection pooling issues
# Feature: Implement custom embedding models
# Feature: Add error handling mechanisms
# Fix: Resolve memory optimization
# Feature: Add result augmenter capabilities
# Refactor: Restructure configuration management
# Feature: Add data transformation pipelines
# Fix: Resolve LangChain callback errors
# Feature: Implement chat history persistence
# Feature: Implement semantic search capabilities
# Fix: Resolve PostgreSQL deadlock issues
# Feature: Add AWS Bedrock integration
# Feature: Add result augmenter capabilities
import re
from typing import Dict, Any, List
from agents.tool.fulltext_field import (
    fulltext_name_to_label
)
from langchain_core.messages import HumanMessage
from agents.tool.patterns import (
    match_pattern,
    where_pattern,
    fulltext_pattern,
    value_pattern
)
from agents.tool.utils import RocloEntity
import logging
from opik.api_objects.span import Span


async def value_mapper(state: Dict[str, Any]) -> Dict[str, Any]:  
    """
    Maps values in a Cypher query to the most relevant values in a graph database.

    This function parses a Cypher query, identifies nodes, relationships, and properties,
    and attempts to map their values to the most relevant ones in the graph database.
    If no similar value is found, it returns an error message.

    Args:
        state (Dict[str, Any]): Contains the Cypher query and other contextual information.

    Returns:
        Dict[str, Any]: Updated state with the mapped Cypher query or an error message.
    """
    cypher_query, user_id, session_id = state['messages'][-1].content, state.get('user_id'), state.get('session_id')

    # Mapping variables to their labels and types (node or relationship)
    variable_to_label = {}

    # Start the span.
    span = state['trace'].span(
        name = "Value_Mapper",
        type = 'tool',
        input = "Roclo"
    )

    try:
        # Step 1: Parse nodes and relationships from the Cypher query
        cypher_query = await _map_value_in_match_pattern(cypher_query, user_id, session_id, variable_to_label, span)

        # Step 2: Extract values from fulltext patterns.
        _extract_variable_in_fulltext_pattern(cypher_query, variable_to_label)
        
        # Step 3: Extract values from WHERE clause  
        cypher_query = await _map_value_in_where_pattern(cypher_query, user_id, session_id, variable_to_label, span)
        
        # Update the span.
        logging.getLogger(f"{user_id}-{session_id}").info("Invoked Value Mapper")
        span.update(output = cypher_query)
        span.end()

        return {
            "messages":HumanMessage(content = cypher_query),
            "sender":"value_mapper"
        }
    
    except Exception as e:
        logging.getLogger(f"{user_id}-{session_id}").error(f"Error while invoking Value Mapper: {e}")
        span.update(output = str(e))
        span.end()

        raise


async def _map_value_in_match_pattern(cypher_query: str, user_id: str, session_id: str, variable_to_label: Dict[str, List[str]], span: Span) -> str:
    """
    Map the values in the cypher query with match pattern

    Example:
        MATCH (c:Company {name: "BambooHR"}) -> Company, name, "BambooHR" -> "BambooHR LLC"
        MATCH ()-[r:located_in {country:"UK"}] -> located_in, country, "UK" -> "GB"

    Args:
        cypher_query (str): Cypher query need to map the value.
        user_id (str): ID of the user.
        table_id (str): Table ID of the Postgres that mapped values are stored.
        session_id (str): Current session id of the Chatbot UI.
        variable_to_label (Dict[str, List[str]]): Dict of the entity variable and type. e.g: {"c": ["Company", "node]}
        span (Span): Current Span of Opik Tacker.
    
    Returns:
        str: Value mapped cypher query.
    """
    # Collect matches before iterating  
    matches = list(match_pattern.finditer(cypher_query))

    for node_match in matches: 
        if node_match.group('node_var') and node_match.group('node_label'): # Node pattern 
            # Find the node variable, label, and properties string.
            node_var, label, properties_str = node_match.group('node_var'), node_match.group('node_label'), node_match.group(3)
            variable_to_label[node_var] = [label, 'node']
            # If properties string exsits, map the value.
            if properties_str:  
                properties = re.findall(value_pattern, properties_str)
                for prop, value in properties:  
                    # Create the dataclass and map the value with graph database.
                    node_match_entity = RocloEntity(node_var, label, prop, value, 'node', user_id, session_id, 'match')
                    await node_match_entity.map_graph_value()
                    # If the mapped value is different from origin value, start the span and update the cypher query.
                    if node_match_entity.mapped_value != value:
                        # Create the sub span.
                        sub_span = span.span(
                            name = "Sub_Mapper",
                            type = 'tool',
                            input = f"From {label} {prop} - {value}",
                            output = f"To {node_match_entity.mapped_value} - {node_match_entity.map_type}"
                        )
                        sub_span.end()
                        # Update the cypher query.
                        cypher_query =  node_match_entity.update_query(cypher_query)
    
        elif node_match.group('rel_var') and node_match.group('rel_label'):  # Relationship pattern.   
            # Find the relationship variable, label, and properties string.
            rel_var, label, properties_str = node_match.group('rel_var'), node_match.group('rel_label'), node_match.group(6)
            variable_to_label[rel_var] = [label, 'relationship']
            # If properties string exsits, map the value.
            if properties_str:  
                properties = re.findall(value_pattern, properties_str)
                for prop, value in properties:  
                    # Create the dataclass and map the value with graph database.
                    relation_match_entity = RocloEntity(rel_var, label, prop, value, 'relationship', user_id, session_id, 'match')
                    await relation_match_entity.map_graph_value()
                    # If the mapped value is different from origin value, start the span and update the cypher query.
                    if relation_match_entity.mapped_value != value:
                        # Create the sub span.
                        sub_span = span.span(
                            name = "Sub_Mapper",
                            type = 'tool',
                            input = f"From {label} {prop} - {value}",
                            output = f"To {relation_match_entity.mapped_value} - {relation_match_entity.map_type}"
                        )
                        sub_span.end()
                        # Update the cypher query.
                        cypher_query = relation_match_entity.update_query(cypher_query)

    return cypher_query



def _extract_variable_in_fulltext_pattern(cypher_query: str, variable_to_label: Dict[str, List[str]]) -> None:
    """
    Extract the variable in fulltext pattern.

    Example:
        CALL db.index.fulltext.queryNodes("fulltext_company_descriptions", "Saas") YIELD node as c, score -> {"c":["Company", "node]}
    """
    for fulltext_match in fulltext_pattern.finditer(cypher_query):
        if fulltext_match.group(1) and fulltext_match.group(2):
            fulltext_index, fulltext_var = fulltext_match.group(1), fulltext_match.group(2)
            # Get the label from the full text name.
            fulltext_label = fulltext_name_to_label[fulltext_index]
            variable_to_label[fulltext_var] = [fulltext_label, 'node']




async def _map_value_in_where_pattern(cypher_query: str, user_id: str, session_id: str, variable_to_label: Dict[str, List[str]], span: Span) -> str:
    """
    Map the values in the cypher query with where pattern

    Example:
        WHERE c.type = 'Private Equity'

    Args:
        cypher_query (str): Cypher query need to map the value.
        user_id (str): ID of the user.
        table_id (str): Table ID of the Postgres that mapped values are stored.
        session_id (str): Current session id of the Chatbot UI.
        variable_to_label (Dict[str, List[str]]): Dict of the entity variable and type. e.g: {"c": ["Company", "node]}
        span (Span): Current Span of Opik Tacker.
    
    Returns:
        str: Value mapped cypher query.
    """
    # Collect matches before iterating  
    matches = list(where_pattern.finditer(cypher_query))

    for where_match in matches:  
        if where_match.group(1) and where_match.group(2) and where_match.group(3):  # Handle 'node.property = "value"'  
            # Find the entity variable, label, and properties string.
            var, prop, value = where_match.group(1), where_match.group(2), where_match.group(3)
            # Get the label and entity type from var.
            if variable_to_label.get(var):
                [label, entity_type] = variable_to_label.get(var)  
                # Create the dataclass and map the value with graph database.
                where_match_entity = RocloEntity(var, label, prop, value, entity_type, user_id, session_id, 'where')
                await where_match_entity.map_graph_value()
                # If the mapped value is different from origin value, start the span and update the cypher query.
                if where_match_entity.mapped_value != value: 
                    # Create the sub span.
                    sub_span = span.span(
                        name = "Sub_Mapper",
                        type = 'tool',
                        input = f"{label} {prop} - {value}",
                        output = f"{where_match_entity.mapped_value} - {where_match_entity.map_type}"
                    )
                    sub_span.end()
                    # Update the cypher query.
                    cypher_query = where_match_entity.update_query(cypher_query)

    return cypher_query