from config import Credentials
import asyncio
from kg_population.sql_transformer.api_parallel_processor import process_api_requests
from utils import (
    save_json_to_file,
    check_item,
    load_json_file,
    compare_lists,
    extract_sections,
    description_sections
)
from core import RocloOpikTracker
from typing import List, Dict, Any
import logging



# Retrieve the content rewriting system prompt
content_rewriter_system_prompt = RocloOpikTracker.get_prompt("content_rewriter_system_prompt")



def rewrite_data(data: Dict[str, List[Dict[str, Any]]], index: Dict[str, Dict[Any, int]]) -> None:
    """
    Processes and rewrites content data for various table types using   
    API calls to the OpenAI model.  

    Args:  
        data (Dict[str, List[Dict[str, Any]]]): A dictionary containing various data tables to be processed.  
        index (Dict[str, Dict[Any, int]]): A dictionary mapping identifiers for accessing nested data.  
    """

    def _rewrite_content(requests_data: List[Dict[str, Any]], table_name: str, rpm: float, tpm: float, field_name: str) -> None:
        """  
        Sends content rewriting requests to the OpenAI API and updates the data.  

        Args:  
            requests_data (List[Dict[str, Any]]): A list of dictionaries containing API request data.  
            table_name (str): Name of the table being processed.  
            rpm (int): Maximum requests per minute allowed.  
            tpm (int): Maximum tokens per minute allowed.  
        
        Raises:  
            Exception: Indicative of issues during API processing.  
        """
        logging.getLogger('main').info(f"Rewritting {table_name}...")
        # Save the requests data as input.
        save_json_to_file(requests_data, table_name, 'inputs')

        # Load previously rewritten content 
        rewritted_content = load_json_file(table_name, 'outputs')

        # If no rewritten content exists, make API requests
        if rewritted_content == None:
            asyncio.run(
                process_api_requests(
                    requests_filepath=f'kg_population/sql_transformer/inputs/{table_name}.jsonl',
                    save_filepath = f'kg_population/sql_transformer/outputs/{table_name}.jsonl',
                    request_url='https://api.openai.com/v1/chat/completions',
                    api_key=Credentials.get_secret("OPENAI_API_KEY"),
                    max_requests_per_minute=rpm,
                    max_tokens_per_minute=tpm,
                    token_encoding_name='cl100k_base',
                    max_attempts=50,
                    logging_level=40,
                )
            )
            rewritted_content = load_json_file(table_name, 'outputs')

        while True:
        
            # Compare IDs from original requests to the responses
            added_ids, deleted_ids = compare_lists([data['metadata']['id'] for data in requests_data], [data['id'] for data in rewritted_content])

            if added_ids == [] and deleted_ids == []:
                break

            # If some contents are added, so exist on requests data, but don't exist on rewritted_content, reprocess and add it.
            if added_ids:
                added_requests_data = [x for x in requests_data if x['metadata']['id'] in added_ids]
                save_json_to_file(added_requests_data, table_name + "_added", 'inputs')
                asyncio.run(
                    process_api_requests(
                        requests_filepath=f'kg_population/sql_transformer/inputs/{table_name}_added.jsonl',
                        save_filepath = f'kg_population/sql_transformer/outputs/{table_name}.jsonl',
                        request_url='https://api.openai.com/v1/chat/completions',
                        api_key=Credentials.get_secret("OPENAI_API_KEY"),
                        max_requests_per_minute=rpm,
                        max_tokens_per_minute=tpm,
                        token_encoding_name='cl100k_base',
                        max_attempts=50,
                        logging_level=40,
                    )
                )
                rewritted_content = load_json_file(table_name, 'outputs')

            # If some contents are deleted, remove these contents on rewritted content.
            if deleted_ids:
                rewritted_content = [x for x in rewritted_content if x['id'] not in deleted_ids]
                save_json_to_file(rewritted_content, table_name, 'outputs')

        for row in rewritted_content:
            try:
                data[table_name][row['id']]['rewritted_content'] = extract_sections(
                    row['content'], 
                    'extraction', 
                    data[table_name][row['id']]['cleaned_content'] if 'cleaned_content' in data[table_name][row['id']].keys() else data[table_name][row['id']]['text']
                )
                data[table_name][row['id']][field_name] = '\n\n'.join(data[table_name][row['id']]['rewritted_content'])
                data[table_name][row['id']]['summary'] = row['summary']
            except:
                logging.getLogger('main').error(f"Error while loading the rewritted contents {table_name} - {row['id']}")
                raise

    
    # Iterate over the tables in the provided data
    for table_name in data.keys():
        # Prepare requests based on table type
        match table_name:
            case 'descriptions':
                _rewrite_content(
                    requests_data=[
                        {
                            "model":'gpt-4o-mini', 
                            "messages":[
                                {
                                    'role':'system',
                                    'content':content_rewriter_system_prompt
                                },
                                {
                                    'role':'user',
                                    'content':row['text']
                                }
                            ], 
                            'temperature':0.1,
                            'stream':False,
                            "metadata":{
                                "id":i,
                                'summary':f"This is the {description_sections[row['type']]} of the company named '{data['companies'][index['companies'][row['company_id']]]['name']}'."
                            }
                        } 
                        for i, row in enumerate(data[table_name]) if check_item(row['text']) and check_item(row['company_id'])
                    ],
                    table_name = table_name,
                    rpm = 30000.0,
                    tpm = 150000000.0,
                    field_name = 'text'
                )

        
            case 'project_buyer_comments':
                _rewrite_content(
                    requests_data=[
                        {
                            "model":'gpt-4o-mini', 
                            "messages":[
                                {
                                    'role':'system',
                                    'content':content_rewriter_system_prompt
                                },
                                {
                                    'role':'user',
                                    'content':row['cleaned_content']
                                }
                            ], 
                            'temperature':0.1,
                            'stream':False,
                            "metadata":{
                                "id":i,
                                'summary':f"This is the comment about the M&A project named '{data['projects'][index['projects'][row['project_id']]]['name']}'."
                            }
                        } 
                        for i, row in enumerate(data[table_name]) if check_item(row['cleaned_content']) and check_item(row['project_id'])
                    ],
                    table_name=table_name,
                    rpm = 30000.0,
                    tpm = 150000000.0,
                    field_name = 'comment'
                )

            case 'crm_opportunity_notes' | 'crm_opportunity_schedules':
                _rewrite_content(
                    requests_data=[
                        {
                            "model":'gpt-4o', 
                            "messages":[
                                {
                                    'role':'system',
                                    'content':content_rewriter_system_prompt
                                },
                                {
                                    'role':'user',
                                    'content':row['cleaned_content']
                                }
                            ], 
                            'temperature':0.1,
                            'stream':False,
                            "metadata":{
                                "id":i,
                                'summary':f"This is the note about the M&A opportunity named '{data['crm_opportunities'][index['crm_opportunities'][row['opportunity_id']]]['title']}'."
                            }
                        } 
                        for i, row in enumerate(data[table_name]) if check_item(row['cleaned_content']) and check_item(row['opportunity_id'])
                    ],
                    table_name = table_name,
                    rpm = 10000.0,
                    tpm = 3000000.0,
                    field_name = 'text'
                )