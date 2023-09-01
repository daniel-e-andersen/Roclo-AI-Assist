from kg_population.graph_transformer.node.node_schema import node_schema
from kg_population.graph_transformer.relation.relation_schema import relation_schema
from utils import write_cypher_queries
from typing import Dict, List, Any
import logging

# List of the index cypher queries.
index_queries = []


def extract_indexes() -> None:
    """
    Extract the indexes(Search-performance, full-text) to enhance the retrieval capabilities.
    """
    global index_queries

    # Create indexes on node properties.
    for node in node_schema:
        label = node['label']
        # Index of the key property.
        _create_index(node['key_property'], 'node', label, node['key_property']['name'], None, None)

        if 'properties' in node.keys():
            for node_prop in node['properties'].keys():
                _create_index(node['properties'][node_prop], 'node', label, node_prop, None, None)

    # Create indexes on relationship properties.
    for relation in relation_schema:
        for relation_type in relation['relations'].keys():
            relation_one = relation['relations'][relation_type]
            reverse_type = relation_one['reverse']

            start_node = relation_one['start']['label']
            end_node = relation_one['end']['label']
            
            if 'properties' in relation_one.keys():
                for relation_prop in relation_one['properties']:
                    _create_index(relation_prop, 'relation', relation_type, relation_prop['prop'], start_node, end_node)
                    _create_index(relation_prop, 'relation', reverse_type, relation_prop['prop'], start_node, end_node)

    # Write the cypher queries to file.
    write_cypher_queries(index_queries)

    logging.getLogger('main').info("All indexes are extracted.")



def _create_index(schema: List[Dict[str, Any]], type: str, label: str, property: str, start: str, end: str) -> None:
    """
    Make the cypher query to create the index.

    Args:
        schema (List[Dict[str, Any]]): Schema of the KG construction.
        type (str): Specify the entity types. Can be 'node' or 'relation'.
        label (str): Label of the entity.
        property (str): Property of the entity.
        start (str): Start node of the relationship. None for the node entity.
        end (str): End node of the relationship. None for node entity.
    """
    global index_queries

    # Initialize the eneity and properties string on cypher query.
    if type == 'node':
        entity = f"(n:{label})"
        prop_1 = f"(n.{property})"
        prop_2 = f"[n.{property}]"
    else:
        entity = f"()-[r:{label}]-()"
        prop_1 = f"(r.{property})"
        prop_2 = f"[r.{property}]"

    # Name of the index.
    index_name = f"{label}_{property}".lower()
    if start is not None and end is not None:
        index_name = f"from_{start}_to_{end}_{label}_{property}".lower()

    # Search performance indexes.
    if schema['index'] == 'range':
        query = f"CREATE INDEX {index_name} IF NOT EXISTS FOR {entity} ON {prop_1};"
        index_queries.append(query)
    elif schema['index'] == 'text':
        query = f"CREATE TEXT INDEX {index_name} IF NOT EXISTS FOR {entity} ON {prop_1};"
        index_queries.append(query)

    # Full-text indexes.
    if "full_text_index" in schema.keys() and schema['full_text_index'] == True:
        full_query = f"CREATE FULLTEXT INDEX fulltext_{index_name} IF NOT EXISTS FOR {entity} ON EACH {prop_2};"
        index_queries.append(full_query)