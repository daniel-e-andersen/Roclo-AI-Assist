# Test: Implement stress tests for system limits
# Refactor: Optimize caching strategies
# Refactor: Refactor utility functions
# Refactor: Optimize caching strategies
# Test: Add end-to-end tests for user workflows
# Refactor: Optimize vector search algorithms
import collections
from typing import List, Dict, Any, Tuple
from utils import (
    check_item,
    delete_uniques
)
import logging


def process_data(data: List[Dict[str, Any]], table_name: str, pk: str) -> Tuple[List[Dict[str, Any]], Dict[Any, int]]:
    """  
    Preprocess data loaded from MSSQL based on specified table names.  
    
    The function handles specific transformations for different tables:  
    - Normalizes financial records in 'company_financials'.  
    - Combines address fields in 'office_addresses'.  
    - Merges name fields in 'contacts', 'company_shareholders', and 'user_profile'.  
    - Groups related records for certain detail tables.  
    - Adjusts specific values in 'crm_opportunity_notes'.  
    - Filters unique values based on the specified primary key for most tables.  
    
    Parameters:  
        data (List[Dict[str, Any]]): A list of dictionaries representing rows of data.  
        table_name (str): The name of the table from which the data is sourced.  
        pk (str): The primary key field used for indexing.  

    Returns:  
        Tuple[List[Dict[str, Any]], Dict[Any, int]]: A tuple containing the processed data and an index mapping.  
    """
    match table_name:
        case 'company_financials':
            data = _process_company_financials(data)

        case 'office_addresses':
            _combine_name_fields(data, "street_line_one", "street_line_two", "street_address")

        case 'contacts' | 'company_shareholders' | 'user_profile':
            _combine_name_fields(data, "first_name", "last_name", "name")

        case "company_details_company_subtypes" | "company_details_sectors" | "company_details_sub_sectors":
            data = _group_company_details(data)

        case "crm_opportunity_notes":
            _adjust_crm_opportunity_notes(data)
    

    # Delete entries with unique primary key values unless the table is 'descriptions'
    origin_size = len(data)
    if table_name != 'descriptions':
        data = delete_uniques(data, pk)
    
    # Log filtered data size if changes were made
    if len(data) != origin_size:
        logging.getLogger('main').info(f"'{table_name}' filtered from {origin_size} to {len(data)} while loading")

    # Calculate the index based on the primary key
    index = {d[pk]:i for i, d in enumerate(data)}

    return data, index


def _process_company_financials(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """  
    Process the company financials to group data by company ID and type.  
    
    Parameters:  
        data (List[Dict[str, Any]]): Financial data records.  

    Returns:  
        List[Dict[str, Any]]: Processed financial data grouped by company ID.  
    """
    grouped_data = collections.defaultdict(lambda: {  
        'company_id': None,  
        'profit_and_loss': [],  
        'balance_sheet': []  
    })  
    financial_data = {}

    for row in data:
        # Normalize key names
        if row['key'] == 'stock_&_work_in_progress':
            row['key'] = 'stock_and_work_in_progress'
        
        # Store company ID
        grouped_data[row['company_id']]['company_id'] = row['company_id']

        # Store financial records by type
        financial_data[row['key']] = float(row['value']) 
        if row['key'] == 'ebitda' and row['types'] == "p_and_l":
            grouped_data[row['company_id']]['profit_and_loss'].append(financial_data.copy())
            financial_data.clear()
        if row['key'] == 'net_assets' and row['types'] == "balance_sheet":
            grouped_data[row['company_id']]['balance_sheet'].append(financial_data.copy())
            financial_data.clear()

    return [
        {k: str(v).replace("'", '"') if k in ["profit_and_loss", "balance_sheet"] else v for k,v in d.items()}
        for d in grouped_data.values()
    ]



def _combine_name_fields(data: List[Dict[str, Any]], first_name_field: str, last_name_field: str, combined_name_field: str) -> None:  
    """  
    Combine first name and last name into a single name field.  
    
    Parameters:  
        data (List[Dict[str, Any]]): Contact data records.
    """  
    for row in data:  
        first_name = row.get(first_name_field)  
        last_name = row.get(last_name_field)
        if check_item(first_name):
                row[combined_name_field] = f"{first_name} {last_name}" if check_item(last_name) else first_name
        else:
            row[combined_name_field] = None

        # Remove obsolete fields
        del row[first_name_field]
        del row[last_name_field]


def _group_company_details(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:  
    """  
    Group company detail records by companydetails_id.  
    
    Parameters:  
        data (List[Dict[str, Any]]): Company detail records.  

    Returns:  
        List[Dict[str, Any]]: Grouped company detail records.  
    """  
    grouped_data = collections.defaultdict(lambda: {'companydetails_id': None})  
    
    # Assuming all records share the same additional keys other than 'companydetails_id' and 'id.'  
    secondary_key = next(key for key in data[0] if key not in {"companydetails_id", "id"})  
    
    for row in data:  
        company_id = row['companydetails_id']  
        value = row[secondary_key]  

        if company_id in grouped_data:  
            grouped_data[company_id][secondary_key].append(value)  
        else:  
            grouped_data[company_id]['companydetails_id'] = company_id  
            grouped_data[company_id][secondary_key] = [value]  

    return list(grouped_data.values())



def _adjust_crm_opportunity_notes(data: List[Dict[str, Any]]) -> None:  
    """  
    Adjust specific fields in CRM opportunity notes.  
    
    Parameters:  
        data (List[Dict[str, Any]]): CRM opportunity note records.  

    Returns:  
        List[Dict[str, Any]]: Updated CRM opportunity note records.  
    """  
    for row in data:  
        if row['id'] == 6002:  
            row['text'] = None