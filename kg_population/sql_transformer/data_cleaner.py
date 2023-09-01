from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents import Document
import re
import unicodedata
from utils import check_item
import tiktoken
from typing import List, Dict, Any, Optional
import logging


def clean_data(data: List[Dict[str, Any]], table_name: str) -> None:
    """  
    Cleans and processes the given data based on the specified table name.  
    
    Args:  
        data (List[Dict[str, Any]]): A list of dictionaries containing data to be cleaned.  
        table_name (str): The name of the table that determines the cleaning process.  
    """
    match table_name:
        case 'project_buyer_comments':
            for row in data:
                row['cleaned_content'] = _clean_text(row['comment'])
            logging.getLogger('main').info(f"Max token length of {table_name} = {_get_max_token_length(data, 'cleaned_content')}")

        case 'crm_opportunity_notes' | 'crm_opportunity_schedules':
            for row in data:
                row['cleaned_content'] = _clean_text(_extract_text_from_html(row['text']))
            logging.getLogger('main').info(f"Max token length of {table_name} = {_get_max_token_length(data, 'cleaned_content')}")

        case 'descriptions':
            logging.getLogger('main').info(f"Max token length of {table_name} = {_get_max_token_length(data, 'text')}")




def _extract_text_from_html(html_content: str) -> Optional[str]:  
        """  
        Extracts plain text from HTML content using Html2TextTransformer.  
        
        Args:  
            html_content (str): The HTML content to extract text from.  
        
        Returns:  
            str or None: Extracted text or None if input is invalid.  
        """  
        if not check_item(html_content):  
            return None  
        
        document = Document(page_content=html_content)  
        html2text = Html2TextTransformer()  
        docs_transformed = html2text.transform_documents([document])  

        return docs_transformed[0].page_content if docs_transformed else None


def _get_max_token_length(data: List[Dict[str, Any]], key) -> int:  
        """  
        Calculates the maximum token length of a specified key in the data.  
        
        Args:  
            data (list): The list of dictionaries to evaluate.  
            key (str): The key whose token length needs to be evaluated.  
        
        Returns:  
            int: The maximum token length found for the specified key.  
        """  
        encoding = tiktoken.get_encoding('cl100k_base')  
        return max([len(encoding.encode(row[key])) for row in data if check_item(row[key])], default=0)


def _clean_text(text: str, 
                remove_non_ascii=True,
                remove_extra_whitespace=True,
                normalize_unicode=True,
                custom_replacements=None) -> str:
        """
        Clean text by removing unnecessary characters and normalizing content.
        
        Args:
            text (str): Input text to clean
            remove_non_ascii (bool): Whether to remove non-ASCII characters
            remove_extra_whitespace (bool): Whether to normalize whitespace
            normalize_unicode (bool): Whether to normalize Unicode characters
            custom_replacements (dict): Additional custom replacements to apply
            
        Returns:
            str: Cleaned text
        """

        if not check_item(text):
            return None
        
        text = text.lower()

        # Default replacements
        replacements = {
            '_x000d_': '',
            '\r\n': ' ',
            '\r': ' ',
            '\n': ' ',
            '\t': ' ',
            '\xa0': ' ',
            '\u200b': '',
            '\u2028': ' ',
            '\u2029': ' ',
            '&nbsp;': '',
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&quot;': '"',
            '&apos;': "'",
            '&#x27;': "'",
            '&#x2F;': '/',
            '&#39;': "'",
            '&#47;': '/',
            '\ufeff': '',
            '\u200e': '',
            '\u200f': '',
        }
        # Add custom replacements if provided
        if custom_replacements:
            replacements.update(custom_replacements)
        
        # Apply all replacements
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Normalize Unicode characters
        if normalize_unicode:
            text = unicodedata.normalize('NFKD', text)
        
        # Remove control characters
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
        
        # Remove non-ASCII characters
        if remove_non_ascii:
            text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Remove extra whitespace
        if remove_extra_whitespace:
            text = re.sub(r'\s+', ' ', text)

        return text.strip()