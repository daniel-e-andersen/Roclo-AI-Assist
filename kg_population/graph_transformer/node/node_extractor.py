# Refactor: Restructure configuration management
# Refactor: Restructure project directory layout
# Test: Add security tests for authentication
from utils import (
    add_item,
    write_csv_file,
    delete_uniques,
    check_item
)
from kg_population.graph_transformer.node.node_schema import node_schema
from typing import Dict, List, Any
import logging


def extract_nodes(data: Dict[str, List[Dict[str, Any]]], data_index: Dict[str, Dict[Any, int]]) -> None:
    """
    Extract nodes from the SQL database using schema.

    Args:
        data (Dict[str, List[Dict[str, Any]]]): Loaded data from SQL database.
        data_index (Dict[str, Dict[Any, int]]): Index of the data.
    """
    for node in node_schema:
        # Header and data of csv file.
        header, docs = [], []

        # Extract each node through main table.
        for i, row in enumerate(data[node['main_table']]):
            # Store the each row of the CSV file.
            doc = []

            # Add ID property for relationship creation.  
            if i == 0:
                header.append(f"{node['key_property']['name']}:ID({node['label']}){{id-type:{node['key_property']['type']}}}")
            doc.append(row[node['key_property']['col']])

            # Create property field if exists.
            if 'properties' in node.keys():
                for prop in node['properties'].keys():
                    # Add property to header with data type.
                    if i == 0:
                        header.append(f"{prop}:{node['properties'][prop]['type']}")

                    # If node's property is in main table, create value from row.
                    if node['properties'][prop]['table'] == 'main_table':
                        add_item(doc, row[node['properties'][prop]['col']])

                    # If node's property is not in main table, reference other table by FK, create through match values.
                    else:
                        matches = node['properties'][prop]['match']

                        # Initial matching doc from main_table that reference other tables.
                        match_doc, flag = row, True

                        for match in matches:
                            # Foreign key value of original table.
                            fks = match_doc[match[0][1]]

                            if len(match[0]) == 2:
                                if not check_item(fks):
                                    flag = False
                                    break
                                # Index of the reference table that match the FK.
                                try:
                                    ids = data_index[match[1][0]][fks]
                                except Exception:
                                    flag = False
                                    break
                                # New matching doc.
                                match_doc = data[match[1][0]][ids]
                            
                            # If the value is the list.
                            else:
                                ids = [data_index[match[1][0]][fk] for fk in fks if check_item(fk)]
                                if len(ids) == 0:
                                    flag = False
                                    break

                                match_doc = [data[match[1][0]][id] for id in ids]

                        # Add value to doc.
                        if flag == True:
                            if isinstance(match_doc, dict):
                                add_item(doc, match_doc[node['properties'][prop]['col']])
                            else:
                                my_list = [match_docs[node['properties'][prop]['col']] for match_docs in match_doc]
                                result_string = ';'.join(my_list)
                                doc.append(result_string)                                
                        else:
                            doc.append('')

            # Add labels.
            if "extra_labels" in node.keys():
                doc.append(node['label']+";"+";".join(node['extra_labels']))
            else:
                doc.append(node['label'])

            docs.append(doc)
        
        # Delete duplicate IDs if the key property is not id (e.g Country, Investor).
        if node['key_property']['name'] != 'id':
            docs = delete_uniques(docs, 0)

        header.append(":LABEL")
        write_csv_file(f"{node['label']}", docs, header, 'node')

    logging.getLogger('main').info("All nodes are extracted.")