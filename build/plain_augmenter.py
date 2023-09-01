from core import RocloRunnableChain
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from operator import itemgetter
from core import RocloOpikTracker
import logging
from config import Credentials


def create_plain_augmenter_chain():
    """
    Create result augmenter chain.
    """
    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", RocloOpikTracker.get_prompt('oaklins_plain_augmenter_prompt')),
                MessagesPlaceholder(variable_name='chat_history'),
                ("user", "{user_question}{rational_plan}{retrieved_data}"),
            ]
        )
        
        llm = ChatAnthropic(
            model_name = "claude-opus-4-20250514",
            api_key = Credentials.get_secret("ANTHROPIC_API_KEY"),
            temperature=0,
            max_tokens=5120,
            streaming=False
        )

        # llm = ChatOpenAI(
        #     model="gpt-4o",
        #     api_key = Credentials.get_secret("OPENAI_API_KEY"),
        #     temperature=0,
        #     streaming = True
        # )

        return RocloRunnableChain(
            data = {
                "user_question": itemgetter('user_question'),
                "rational_plan": itemgetter('rational_plan'),
                "retrieved_data": itemgetter('retrieved_data'),
                "chat_history":itemgetter("chat_history"),
            },
            prompt = prompt,
            llm = llm,
            input_key = "user_question",
            history_key = "chat_history",
            name = "result_augmenter"
        )
    
    except Exception as e:
        logging.getLogger('main').error(f"Error creating result augmenter chain: {e}")