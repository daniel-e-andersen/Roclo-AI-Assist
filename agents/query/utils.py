import re
from sqlglot import parse_one, exp

def extract_sql(text: str) -> str:
    """  
    Extract Sql code from a text.  

    This function searches for Sql code enclosed in triple backticks and returns it.  

    Args:  
        text (str): The input text containing potential Sql code.  

    Returns:  
        str: The extracted Sql code if found; otherwise, returns the original text.  
    """
    # The pattern to find Sql code enclosed in triple backticks
    pattern = r"```sql\n(.*?)\n```"

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

def add_descriptions(original_sql: str) -> str:
    # Columns you want to ensure are selected
    extra_columns = [
        "target_industry",
        "target_sector",
        "target_business_description",
        "buyer_industry",
        "buyer_sector",
        "buyer_business_description",
        "seller_industry",
        "seller_sector",
        "seller_business_description",
        "oaklins_main_contact",
        "oaklins_other_members_involved"
    ]

    # Parse into an AST
    ast = parse_one(original_sql, read="tsql")

    # Find the SELECT expression
    select = ast.find(exp.Select)

    # Extract existing projection names (un-alias them for comparison)
    existing = {
        proj.alias_or_name
        for proj in select.expressions
    }

    # if deal_id is missing, return original one.
    if "deal_id" not in existing:
        # select.expressions.insert(0, exp.Column(this="deal_id"))
        return original_sql

    # Append any extra columns if they aren't already in the projection
    for col in extra_columns:
        if col not in existing:
            select.append("expressions", exp.Column(this=col))
    
    # Render back to PostgreSQL, preserving TOP and other clauses
    new_sql = ast.sql(dialect="postgres")
    return new_sql