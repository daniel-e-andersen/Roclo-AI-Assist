# Test: Add validation tests for data integrity
# Refactor: Restructure configuration management
# Refactor: Restructure configuration management
# Test: Add end-to-end tests for user workflows
# Refactor: Restructure project directory layout
from utils import (
    add_item,
    write_csv_file,
    check_item
)
from kg_population.graph_transformer.relation.relation_schema import relation_schema
from typing import Dict, List, Any
import logging


def extract_relations(data: Dict[str, List[Dict[str, Any]]], data_index: Dict[str, Dict[Any, int]]) -> None:
    """
    Extract relationships from the SQL database using schema.

    Args:
        data (Dict[str, List[Dict[str, Any]]]): Loaded data from SQL database.
        data_index (Dict[str, Dict[Any, int]]): Index of the data.
    """
    for relation in relation_schema:
        for rel in relation['relations'].keys():
            docs, header = [], []
            rel_meta = relation['relations'][rel]

            # Add start and end id for connecting nodes to header.
            header.append(f":START_ID({rel_meta['start']['label']})")
            header.append(f":END_ID({rel_meta['end']['label']})")
            header.append(":TYPE")

            # Add properties to header if exist.
            if 'properties' in rel_meta.keys():
                for prop in rel_meta['properties']:
                    header.append(f"{prop['prop']}:{prop['type']}")

            # Add realtion items to doc.
            for row in data[relation['table']]:
                doc = []

                # Add header id.
                if rel_meta['start']['table'] == 'main_table':
                    start_id = row[rel_meta['start']['id']]
                else:
                    matches = rel_meta['start']['match']
                    match_doc, flag = row, True
                    for match in matches:
                        fks = match_doc[match[0][1]]
                        if not check_item(fks):
                            flag = False
                            break   
                        try:
                            ids = data_index[match[1][0]][fks]
                        except:
                            flag = False
                            break
                        match_doc = data[match[1][0]][ids]
                
                    if flag == True:
                        start_id = match_doc[rel_meta['start']['id']]
                    else:
                        start_id = None

                # Add end id.
                if rel_meta['end']['table'] == 'main_table':
                    end_id = row[rel_meta['end']['id']]
                else:
                    matches = rel_meta['end']['match']
                    match_doc, flag = row, True
                    for match in matches:
                        fks = match_doc[match[0][1]]
                        if not check_item(fks):
                            flag = False
                            break   
                        try:
                            ids = data_index[match[1][0]][fks]
                        except:
                            flag = False
                            break
                        match_doc = data[match[1][0]][ids]
                
                    if flag == True:
                        end_id = match_doc[rel_meta['end']['id']]
                    else:
                        end_id = None
                
                # If the start and end ids are exist, add properties.
                if check_item(start_id) and check_item(end_id):
                    add_item(doc, start_id)
                    add_item(doc, end_id)
                    doc.append(rel)
                
                    # Add properties if exist.
                    if 'properties' in rel_meta.keys():
                        for prop in rel_meta['properties']:
                            
                            if prop['table'] == 'main_table':
                                add_item(doc, row[prop['col']])
                            else:
                                matches = prop['match']
                                match_doc, flag = row, True

                                for match in matches:
                                    fks = match_doc[match[0][1]]
                                    if not check_item(fks):
                                        flag = False
                                        break
                                    
                                    try:
                                        ids = data_index[match[1][0]][fks]
                                    except:
                                        flag = False
                                        break

                                    match_doc = data[match[1][0]][ids]
                                
                                if flag == True:
                                    add_item(doc, match_doc[prop['col']])
                                else:
                                    doc.append('')
                
                    # Add doc to data.
                    docs.append(doc)
            
            write_csv_file(f"{rel_meta['start']['label']}-{rel}-{rel_meta['end']['label']}", docs, header, 'relation')

            # If there is reverse relationships, change the start and end id header and assign reversed type.
            if "reverse" in rel_meta.keys():
                header[0] = f":END_ID({rel_meta['start']['label']})"
                header[1] = f":START_ID({rel_meta['end']['label']})"
                docs = [row[:2] + [rel_meta['reverse']] + row[3:] for row in docs]

                write_csv_file(f"{rel_meta['end']['label']}-{rel_meta['reverse']}-{rel_meta['start']['label']}", docs, header, 'relation')

    logging.getLogger('main').info("All relationships are extracted.")