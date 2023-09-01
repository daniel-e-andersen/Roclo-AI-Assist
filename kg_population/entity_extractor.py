# Test: Add validation tests for data integrity
# Test: Implement performance tests for vector search
# Test: Implement stress tests for system limits
# Refactor: Refactor utility functions
# Refactor: Optimize caching strategies
from utils import (
    clear_graph_outputs,
    write_shell_command
)
from typing import Dict, List, Any
from kg_population.graph_transformer.node.node_extractor import extract_nodes
from kg_population.graph_transformer.relation.relation_extractor import extract_relations
from kg_population.graph_transformer.index.index_extractor import extract_indexes
from collections import defaultdict
from utils import description_sections

def extract_entities(data: Dict[str, List[Dict[str, Any]]], data_index: Dict[str, Dict[Any, int]]) -> None:
    """
    Extract the knowledge graph from loaded SQL data by CSV format.

    Args:
        data (Dict[str, List[Dict[str, Any]]]): Loaded data from SQL database.
        data_index (Dict[str, Dict[Any, int]]): Index of the data. Match the primary key to its position(index) on the list.
    """

    def _group_company_descriptions() -> None:
        """
        Group the company descriptions by company id.
        """
        # Group dicts by primary key - company_id.
        grouped_dicts = defaultdict(list)
        _ = [grouped_dicts[d['company_id']].append(d) for d in data['descriptions']]  
        grouped_dicts = dict(grouped_dicts) 

        # Join rows have same company id.
        joined_data = []
        for company_id in grouped_dicts.keys():
            grouped_dict = grouped_dicts[company_id]

            # Change the last row(as is the indexed for specific company id) based on the descriptions sections.
            last_row = grouped_dict[-1]
            last_row['text'] = description_sections[last_row['type']] + ":\n" + last_row['text'].replace('\n\n', '\n')

            # Append the other rows to last row's text.
            for row in reversed(grouped_dict[:-1]):
                last_row['text'] = description_sections[row['type']] + ":\n" + row['text'].replace('\n\n', '\n') + '\n\n' + last_row['text']

            joined_data.append(last_row)

        # Update the data and data index.
        data['descriptions'] = joined_data
        data_index['descriptions'] = {d['company_id']:i for i, d in enumerate(data['descriptions'])}


    # Clear the graph output files.
    clear_graph_outputs()

    # Group the company descriptions by company_id.
    _group_company_descriptions()

    # Extract nodes.
    extract_nodes(data, data_index)

    # Extract relationships.
    extract_relations(data, data_index)

    # Extract indexes.
    extract_indexes()

    # Write shell command for neo4j-admin database import full.
    write_shell_command()