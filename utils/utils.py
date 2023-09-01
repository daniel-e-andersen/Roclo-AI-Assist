from collections import OrderedDict
import json
import os
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from datetime import datetime, timezone, timedelta
import subprocess
import re
from datetime import datetime 
import logging
from neo4j.time import DateTime
import chainlit as cl
import pandas as pd
import datetime
import csv

def replace_prompt(prompt: str) -> str:
    """  
    Replace curly braces in the prompt with double curly braces.  

    This function is useful for preparing a prompt string for templating engines  
    that use double curly braces to denote placeholders.  

    Args:  
        prompt (str): The input prompt string containing curly braces.  

    Returns:  
        str: The modified prompt string with single curly braces replaced by double curly braces.  
    """
    return prompt.replace("{", "{{").replace("}", "}}")


def check_item(item: Any) -> bool:
    """
    Check if the item is a non-empty value.

    Args:
        item (Any): The item to check.

    Returns:
        bool: True if the item is non-empty, False otherwise.
    """
    return item not in [None, 'nan', '']


def delete_uniques(lists: List[Dict[str, Any]], pk: str) -> List[Dict[str, Any]]: 
    """  
    Remove sublists to retain only unique entries based on the specified primary key.  

    This function keeps the last occurrence of each unique primary key value.  

    Args:  
        lists (List[Dict[str, Any]]): The list of dictionaries (sublists) to process.  
        pk (str): The key used for determining uniqueness.  

    Returns:  
        List[Dict[str, Any]]: A list of dictionaries with unique entries based on the primary key.  
    """ 
    seen = OrderedDict()  

    for lst in lists:  
        first_element = lst[pk]   
        # Keep last value about same pk.
        seen[first_element] = lst  

    return [v for v in seen.values() if v is not None]


def save_json_to_file(items: List[Dict[str, Any]], file_name: str, file_type: str) -> None:
    """  
    Save a list of items to a JSON Lines file.  

    Args:  
        items (List[Dict[str, Any]]): The list of items to save.  
        file_name (str): The name of the output file (without extension).  
        file_type (str): The subdirectory type where the file will be stored.  

    Returns:  
        None  
    """
    file_path = f'kg_population/sql_transformer/{file_type}/{file_name}.jsonl'
    with open(file_path, 'w') as jsonl_file:  
        for item in items:
            jsonl_file.write(json.dumps(item) +'\n')


def load_json_file(file_name: str, file_type: str) -> Optional[List[Dict[str, Any]]]:
    """  
    Load JSON Lines from a specified file.  

    Args:  
        file_name (str): The name of the file to load (without extension).  
        file_type (str): The subdirectory type where the file is located.  

    Returns:  
        Optional[List[Dict[str, Any]]]: A list of dictionaries loaded from the file,  
                                          or None if the file does not exist.  
    """
    file_path = f'kg_population/sql_transformer/{file_type}/{file_name}.jsonl'
    loaded_data = []

    if os.path.exists(file_path):
        with open(file_path, 'r') as jsonl_file:
            for line in jsonl_file:
                loaded_data.append(json.loads(line))
        return loaded_data

    return None


def compare_lists(list_1: List[Any], list_2: List[Any]) -> Tuple[List[Any]]:
    """  
    Compare two lists and print the elements that are unique to each list.  

    Args:  
        list_1 (List[Any]): The first list to compare.  
        list_2 (List[Any]): The second list to compare.  

    Returns:  
        None  
    """
    set_1, set_2 = set(list_1), set(list_2)
    only_in_1 = list(set_1 - set_2)
    only_in_2 = list(set_2 - set_1)
    
    logging.getLogger('main').info("Elements in A but not in B: %s", only_in_1)
    logging.getLogger('main').info("Elements in B but not in A: %s", only_in_2)

    return only_in_1, only_in_2



def clear_graph_outputs() -> None:
    """
    Delete all output files(CSV) transformed for KG population.
    """
    base_path = 'kg_population/graph_transformer/outputs'
    # Remove the node output files
    for node_file in _list_files(f"{base_path}/nodes"):
        _delete_file(f"{base_path}/nodes/{node_file}")

    # Remove the relationship output files
    for relation_file in _list_files(f"{base_path}/relations"):
        _delete_file(f"{base_path}/relations/{relation_file}")

    logging.getLogger('main').info("All entity files are deleted.")



def _delete_file(file_path: str) -> None:
    """
    Delete the file on storage.

    Args:
        file_path (str): File path to be deleted.
    """
    try:  
        if os.path.isfile(file_path):  
            os.remove(file_path) 
        else:  
            logging.getLogger('main').info(f"No file found at '{file_path}'.")  
    except Exception as e:  
        logging.getLogger('main').error(f"Error while deleting file - {file_path}: {e}")



def _list_files(directory: str) -> None:
    """
    Get all file names in a directory.

    Args:
        directory (str): Directory path for getting list of file names.
    """
    try:  
        files = os.listdir(directory)  
        return [file for file in files if os.path.isfile(os.path.join(directory, file))]  
    except OSError as e:  
        logging.getLogger('main').error(f"Error while getting list of files on {directory}: {e}")  
        return []


def write_csv_file(file_name: str, data: List[Dict[str, Any]], header: List[str], type: str) -> None:
    """
    Write CSV file for initial KG population.

    Args:
        file_name (str): Name of the CSV file.
        data (List[Dict[str, Any]]): Data to be writted.
        header (List[str]): Header(columns) of the data.
        type (str): Type of the entity file. Can be 'node' or 'relation'.
    """
    try:
        # Create DataFrame  
        df = pd.DataFrame(data, columns=header)  

        # Write DataFrame to CSV  
        df.to_csv(f"kg_population/graph_transformer/outputs/{type}s/{file_name}.csv", mode = 'w', index=False, sep = "^")
    except Exception as e :
        logging.getLogger('main').error(f"Error while writing CSV file {e}")



def add_item(doc: List[Any], item: Any) -> None:
    """
    Add item to doc if it's not empty value.
    """
    if check_item(item):
        doc.append(_normalize_item(item))
    else:
        doc.append('')


def _normalize_item(item: Any) -> None:
    """
    Normalize  the value for Neo4j integration.

    Args:
        item (Any): Item to be added.
    """
    # Normalize the datetime item.
    if isinstance(item, datetime):
        item = item.replace(tzinfo=timezone(timedelta(hours=1))).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        return item[:-2]+item[-2:]
    
    return item



def write_cypher_queries(queries: List[str]) -> None:
    """
    Write the cypher queries to file.

    Args:
        queries (List[str]): List of the cypher queries.
    """
    with open("kg_population/graph_transformer/outputs/cypher.txt", 'w') as f:
        f.write("\n\n".join(queries))



def write_shell_command() -> None:
    """
    Write shell command for Neo4j database import from csv files.
    """
    # Base command.
    command = "sudo neo4j-admin database import full cavendish --multiline-fields=true --normalize-types=true --verbose=true --array-delimiter=';' --delimiter='^'"

    # Add node command.
    for node_file in _list_files("kg_population/graph_transformer/outputs/nodes"):
        command += f" --nodes=nodes/{node_file}"

    # Add relation command.
    for relation_file in _list_files("kg_population/graph_transformer/outputs/relations"):
        command += f" --relationships=relations/{relation_file}"

    with open("kg_population/graph_transformer/outputs/index.sh", 'w') as file:
        file.write("#!/bin/bash\n\n")
        file.write(command)



def run_command(command: str) -> None:  
    """
    Execute the command on the OS (default: Ubuntu 22.0.4).

    Args:
        command (str): Command to be executed.
    """
    try:  
        # Execute the command  
        result = subprocess.run(command, shell=True, check=True,   
                                stdout=subprocess.PIPE,   
                                stderr=subprocess.PIPE,   
                                text=True)  # text=True for string output  
        
        # Get output and return it  
        logging.getLogger('main').info("Command - %s - executed successfully: %s", command, result.stdout.strip())
    except subprocess.CalledProcessError as e:  
        # Handle errors in command execution  
        logging.getLogger('main').error("An error occurred while executing the command: %s: %s", command, e.stderr.strip())


def extract_sections(xml_string: str, extract_type: str, cleaned_content: str) -> List[str]:  
    """
    Extract the sections from rewritted content.
    """
    # Use regex to find all section contents  
    sections = re.findall(r'<section>(.*?)<\/section>', xml_string, re.DOTALL) 

    if len(sections) == 0:

        # If the input content - cleaned content is wrong for LLM processing, return with original input string.
        if xml_string.startswith("I'm sorry"):
            return [cleaned_content]
        
        if extract_type == 'processing':
            return None
        else:
            logging.getLogger('main').error("Wrong format XML string %s", xml_string)

    return sections

def get_business_descriptions_for_oaklins(dict_list: List[Dict[str, Any]], target_keys: List[str]) -> List[Dict[str, Any]]:
    result = []

    for item in dict_list:
        for key in target_keys:
            if item[key] and len(item[key]) > 50:
                description = {
                    "deal_id": item["deal_id"],
                    "text": item[key],
                    "title": key,
                }

                result.append(description)
    
    return result
            

def split_dict_with_text_list(dict_list: List[Dict[str, Any]], prop: str):
    """
    Split dictionaries based on their property list while preserving other keys.
    
    Args:
        dict_list (List[Dict[str, Any]]): List of dictionaries containing 'text' property with list of strings
        prop (str): Property of list of string.
        
    Returns:
        list: New list of dictionaries with split text values
    """
    result = []
    
    for item in dict_list:
        if prop not in item or not isinstance(item[prop], list):
            # If 'text' key doesn't exist or is not a list, keep the original dict
            result.append(item.copy())
            continue
            
        # Create new dictionaries for each text item
        for text in item[prop]:
            new_dict = item.copy()  # Create a shallow copy of the original dict
            new_dict[prop] = text  # Replace text list with single string
            result.append(new_dict)
            
    return result


def get_value_list_from_data(data: List[Dict[Any, Any]]):
    """
    Get the list of the value from list of dict.
    """
    return [value for d in data for value in d.values()]


def convert_neo4j_datetime(data: Any) -> None:
    """
    Convert the neo4j datetime object to python datetime string.
    """
    # If the data is list, convert each item in the list.
    if isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = convert_neo4j_datetime(item)

    # If the data is dict, convert each value in the dict.
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_neo4j_datetime(value)

    # If the data is Neo4j's datetime object, convert it.
    elif isinstance(data, DateTime):
        return data.to_native().strftime('%Y-%m-%d %H:%M:%S.%f %z')

    return data


async def get_user_message(content: str) -> str:
    """
    If the all matched value are wrong, so the user select 'Others' in all cases, ask User about the exact entity name, and re-execute the code.

    Args:
        content (str): Content of the ask message.

    Returns:
        str: User inputed message.
    """
    res = await cl.AskUserMessage(content = content, timeout = 36000).send()
    if res:
        return res['output']

async def convert_list_of_dicts_to_df(data: list[dict]) -> pd.DataFrame:
    """
    Converts a list of dictionaries (e.g., SQL result) to a pandas DataFrame.
    Automatically converts any column containing datetime.date objects to pandas datetime.
    
    Parameters:
    -----------
    data : list of dict
        The input data, each dict represents a row with column names as keys.
    
    Returns:
    --------
    pd.DataFrame
        A DataFrame with proper types, including datetime conversion.
    """
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Convert any columns with datetime.date to datetime64
    for col in df.columns:
        if df[col].dropna().apply(lambda x: isinstance(x, datetime.date)).all():
            df[col] = pd.to_datetime(df[col])
    
    return df

async def save_csv(data: list[dict], filename: str):
    with open(f'csv/{filename}.csv', 'w', newline='') as csvfile:
        # Assume all dictionaries have the same keys, so get headers from the first dict
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())

        # Write headers
        writer.writeheader()

        # Write data rows
        for row in data:
            writer.writerow(row)

async def truncate_descriptions(retrieved_data, max_length=300):
    """
    Truncates the '%business_description' field in each deal if it exceeds max_length characters.

    Args:
        retrieved_data (list): List of dictionaries containing deal data.
        key (str): The key to truncate (default is '%business_description').
        max_length (int): The maximum allowed length before truncation.

    Returns:
        list: The modified list of retrieved_data with truncated descriptions where applicable.
    """
    keys = retrieved_data[0].keys()
    description_keys = ["target_business_description", "buyer_business_description", "seller_business_description"]

    # get common key
    keys = list(set(keys) & set(description_keys))

    for raw in retrieved_data:
        for key in keys:
            if raw[key] and len(raw[key]) > max_length:
                raw[key] = raw[key][:max_length].rstrip() + "..."
    return retrieved_data
