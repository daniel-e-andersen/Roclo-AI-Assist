from core import RocloRunnableChain
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from operator import itemgetter
from core import RocloOpikTracker
import logging
from config import Credentials
from utils import replace_prompt


def create_rational_planner_chain() -> RocloRunnableChain:
    """  
    Create a rational planner chain.  

    This function initializes a RocloRunnableChain with a specific chat prompt and   
    a language model (LLM) configured for the rational planner functionality.  

    Returns:  
        RocloRunnableChain: An instance of the RocloRunnableChain configured for rational planning.  
    """
    try:
        # Create the chat prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", replace_prompt(RocloOpikTracker.get_prompt('oaklins_rational_planner_prompt', True))),
                MessagesPlaceholder(variable_name='chat_history'),
                ('user', '{user_question}'),
            ]
        )

        # Initialize the language model with specified parameters
        llm = ChatAnthropic(
            model_name = "claude-opus-4-20250514",
            api_key = Credentials.get_secret("ANTHROPIC_API_KEY"),
            temperature=0,
            max_tokens=5120,
            streaming=False
        )

        # Return the configured RocloRunnableChain
        return RocloRunnableChain(
            data = {
                "user_question": itemgetter('user_question'),
                "chat_history": itemgetter("chat_history"),
            },
            prompt = prompt,
            llm = llm,
            input_key = "user_question",
            history_key = "chat_history",
            name = "rational_planner"
        )
    
    except Exception as e:
        logging.getLogger('main').error(f"Error while creating rational planner chain: {e}")
        raise