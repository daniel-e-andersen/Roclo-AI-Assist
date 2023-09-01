from typing import List
from langchain_core.messages import HumanMessage

import sqlglot
from sqlglot.expressions import Like

async def result_refactor(sql_query: str, retrieved_data: List) -> List:
    """
    This function parses a SQL query, and refactors
    """
    
    