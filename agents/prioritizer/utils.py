import re
import json
from datetime import date

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def extract_json(text: str) -> str:
    """  
    Extract JSON code from a text.  

    This function searches for JSON code enclosed in triple backticks and returns it.  

    Args:  
        text (str): The input text containing potential JSON code.  

    Returns:  
        str: The extracted JSON code if found; otherwise, returns the original text.  
    """
    # The pattern to find JSON code enclosed in triple backticks
    pattern = r"```json\n(.*?)\n```"

    # Find all matches in the input text
    matches = re.findall(pattern, text, re.DOTALL)

    return matches[0] if matches else text



def check_string_ends_with_limit(input_string: str) -> str:  
    """
    Check the string that it has clear limitation of retrieval result. If the string doesn't have LIMIT statement, add this.

    Args:
        input_string (str): The input string(cypher query).

    Returns:
        str: If the query is incorrect, add LIMIT 10 in the end of the query.
    """
    # Define the regex pattern to match the string ending with "LIMIT {number}"  
    pattern = r"LIMIT \d+$"  
    
    # Use re.search to check if the pattern matches the end of the input_string  
    if re.search(pattern, input_string.strip()):  
        return input_string
    else:  
        return input_string + " LIMIT 10"



def replace_operations(input_string: str) -> str:
    """
    Replace some operators in the cypher query like '=~'.
    """
    return input_string.replace('=~', '=')


def get_deal_ids(data):
    # Loop through the list and add elements only if they haven't appeared before
    deal_ids = []

    for raw in data:
        if raw['entity']['deal_id'] not in deal_ids:
            deal_ids.append(raw['entity']['deal_id'])
    
    return deal_ids