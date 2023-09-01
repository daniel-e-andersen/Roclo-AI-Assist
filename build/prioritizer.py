from core import RocloRunnableChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from operator import itemgetter
from core import RocloOpikTracker
import logging
from config import Credentials
from utils import replace_prompt


def create_prioritizer_chain() -> RocloRunnableChain:
    """  
    Create a Oaklins Prioritizer chain.  

    This function initializes a RocloRunnableChain configured for Prioritization
    based on user messages and chat history.  

    Returns:  
        RocloRunnableChain: An instance of the RocloRunnableChain configured for Oaklins Prioritizer.  
    """
    try:
        # Create the chat prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", replace_prompt(RocloOpikTracker.get_prompt('oaklins_business_description_prompt', True))),
                MessagesPlaceholder(variable_name='chat_history'),
                ("user", "{user_question}{rational_plan}"),
            ]
        )

        # Initialize the language model with specified parameters
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key = Credentials.get_secret("OPENAI_API_KEY"),
            temperature=0,
            streaming = True
        )
        
        # Return the configured RocloRunnableChain
        return RocloRunnableChain(
            data = {
                "user_question": itemgetter("user_question"),
                "rational_plan": itemgetter('rational_plan'),
                "chat_history": itemgetter("chat_history"),
            },
            prompt = prompt,
            llm = llm,
            input_key = "user_question",
            history_key = "chat_history",
            name = "priortizer"
        )
    
    except Exception as e:
        logging.getLogger('main').error(f"Error while creating oaklins priortizer chain: {e}")
        raise