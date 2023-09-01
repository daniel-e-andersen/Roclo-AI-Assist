from config import Credentials
from core import (
    RocloPostgresDatabase,
    RocloSheetProvider
)
from logger import setup_logger
import logging

import schedule
import time

from typing import List, Dict, Any, Tuple
import datetime

# Initialize the core functionalities.
try:
    # Initialize the logger.
    setup_logger()
    
    Credentials.set_secrets()
    RocloSheetProvider.connect()
    RocloPostgresDatabase.connect()
    # RocloMilvusVectorDB.connect()
except Exception as e:
    print(e)
    exit()

from utils import postgres_table_schema, oaklins_keys_types

# Function to convert individual value to its proper type
def convert_value(val: Any, typ: type) -> Any:
    if val == "-" or val is None:
        return None
    try:
        if typ is bool:
            if isinstance(val, str):
                return val.lower() in ("true", "1", "yes")
            return bool(val)
        elif typ is datetime.date:
            if isinstance(val, datetime.date):
                return val
            return datetime.datetime.strptime(val, "%d/%m/%Y").date()
        else:
            return typ(val)
    except (ValueError, TypeError):
        return None


# Convert list of lists to list of dicts
def convert_to_dicts(data: List[List[Any]], keys_types: List[Tuple[str, type]]) -> List[Dict[str, Any]]:
    result = []
    for row in data:
        if not row:
            continue
        
        # Pad with None
        padded_row = row + [None] * (44 - len(row))
        # Merge the descriptions

        # target business description
        if padded_row[11]:
            padded_row[10] = padded_row[10] + '\n\n' + padded_row[11]
        del padded_row[11]
        # 
        if padded_row[22]:
            padded_row[21] = padded_row[21] + '\n\n' + padded_row[22]
        del padded_row[22]

        converted_row = {
            key: convert_value(val, typ)
            for (key, typ), val in zip(keys_types, padded_row)
        }
        result.append(converted_row)
    return result


def job():
    data = RocloSheetProvider.get_deals()
    converted_dict = convert_to_dicts(data, oaklins_keys_types)
    RocloPostgresDatabase._insert_data(postgres_table_schema, converted_dict)

    logging.getLogger('main').info(f"Executed job: {len(converted_dict)} deals updated.")

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)