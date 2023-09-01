# Refactor: Refactor error handling mechanisms
# Refactor: Refactor query generation logic
# Refactor: Refactor agent communication protocols
# Refactor: Optimize resource allocation
# Test: Add security tests for authentication
# Refactor: Refactor agent architecture for better modularity
# Refactor: Optimize memory usage patterns
# Refactor: Refactor agent communication protocols
# Refactor: Optimize database query performance
# Test: Implement mock tests for external services
# Refactor: Refactor UI components for reusability
# Optimize vector database performance
# Add advanced data synchronization
# Implement intelligent system scaling
# Add advanced user session management
# Add intelligent database optimization
from chain import RocloChatbotChain
from core import RocloSupabaseDatabase
import chainlit as cl
from chainlit.types import ThreadDict
from config import Credentials
from logger import setup_logger
import opik
from typing import Dict, Optional, Any
from starters import starters, starters_index
from core import RocloOpikTracker
import logging
from utils import get_user_message
from chainlit.input_widget import TextInput


try:
    # Build the workflow of the RocloChatbotChain
    RocloChatbotChain.build_workflow()
except Exception as e:
    print(e)
    exit()


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    """
    Authenticate the user by email and password
    """
    if (username, password) == ("valerii@roclo.com", "P@ssw0rdRoclo"):
        return cl.User(
            identifier="valerii", metadata={"role": "admin", "provider": "credentials"}
        )
    if username and password:
        user_id = RocloSupabaseDatabase.authenticate_user(username, password)

        if user_id:
            logging.getLogger('main').info("User %s signed in", user_id)
            return cl.User(
                identifier=username, metadata={"role": "user", "provider": "credentials"}
            )
        else:
            return None
    return None


# @cl.oauth_callback
# def oauth_callback(
#   provider_id: str,
#   token: str,
#   raw_user_data: Dict[str, str],
#   default_user: cl.User,
# ) -> Optional[cl.User]:
#     if provider_id == 'google':
#         # if default_user.identifier == 'valerii@roclo.com':
#         #     return cl.User(
#         #         identifier="valerii", metadata={"role": "admin", "provider": "credentials"}
#         #     )
#         return cl.User(
#             identifier="valerii", metadata={"role": "admin", "provider": "credentials"}
#         )
#     return None


# @cl.set_starters
# async def set_starters():
#     return [
#         cl.Starter(
#             label= starter['label'],
#             message= starter['message'],
#             icon= starter['icon'],
#         ) for starter in starters
#     ]


@cl.on_chat_start
async def on_chat_start():
    pass


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    pass

# @cl.on_chat_start
# async def start():
#     settings = await cl.ChatSettings(
#         [
#             TextInput(id="AgentName", label="Agent Name", initial="AI", placeholder="Ask a question..."),
#         ]
#     ).send()
#     value = settings["AgentName"]

@cl.on_message
async def on_message(message: cl.Message):
    """
    Receive the user message and process it
    """
    # Create Task, and Add task to task list
    task = cl.Task(title = "Processing your question", status = cl.TaskStatus.RUNNING)
    task_list = cl.TaskList()
    task_list.status = "Running..."
    await task_list.add_task(task)
    await task_list.send()
    cl.user_session.set("task", task)
    cl.user_session.set("task_list", task_list)

    # Get the session details
    user_id = cl.user_session.get('user').identifier
    thread_id = cl.context.session.thread_id

    # Setup the logger.
    setup_logger(
        user_id = user_id,
        session_id = thread_id
    )

    try:
        input_msg = message.content

        # If it's starter message, ask the user specific entity name and replace the message
        if message.content in [starter['message'] for starter in starters]:
            # Get the starter.
            starter = starters[starters_index[message.content]]
            # Ask to user about specific entity name, and replace the user message.
            entity_name = await get_user_message(content = starter['ask_message'])
            input_msg = starter['content'] % entity_name

        # Start the tracking to Comet Opik cloud.
        trace = opik.Opik(project_name = 'Oaklins').trace(
            name = user_id,
            input = input_msg,
            metadata= {
                "user_id": user_id,
                "session_id": thread_id
            }
        )

        # Invoke the Roclo chatbot chain
        result = await RocloChatbotChain.ainvoke(
            user_id = user_id,
            session_id = thread_id,
            message = input_msg,
            trace = trace
        )

        # Update the task list
        task_list.status = "Done"
        await task_list.send()

        # If the agent invoke calls larger than 3, it means data retrieval is processed, so ask user feedback, and add this to dataset.
        if len(result['messages']) > 3:
            # If the agent graph invokation stopped due to too many invokation, add this result with error database.
            if result['sender'] == 'data_retriever':
                await _add_items_to_dataset_with_feedback_score(result, -1)
            # else:
            #     feedback_score = await _get_user_feedback()
            #     if feedback_score != "Ignore":
            #         await _add_items_to_dataset_with_feedback_score(result, feedback_score)
        
    except Exception as e:
        await cl.Message(content = "Something went wrong. Please try again").send()
        cl.user_session.get('task').status = cl.TaskStatus.FAILED
        task_list.status = "Failed"
        await task_list.send()

@cl.action_callback("action_button")
async def on_action(action: cl.Action):
    user_question = action.payload['user_question']
    print(user_question)
    print(action.forId)

    msg = cl.Message(id=action.forId)
    print(msg.elements)
    # file = cl.File(
    #     name=user_question,
    #     path="./config.py",
    #     display="inline",
    # )

    #     # 4. Update the message to replace button with download link
    # message = action.message
    # # message.actions = []  # Remove action buttons
    # message.elements.append(file)  # Add download element
    
    # await message.update()

async def _get_user_feedback() -> Optional[int]:
    """
    Get user feedback with score from 1 to 10.
    """
    res = await cl.AskActionMessage(
        content = "Was this response helpful?\n" +\
        "Please rate your experience from 1 (least helpful) to 5 (most helpful).\n" +\
        "Thank you!",
        actions = [
            cl.Action(name = "feedback", payload = {"value": x}, label = f"{x}") for x in [1, 2, 3, 4, 5, 'Ignore']
        ],
        timeout = 3600
    ).send()

    if res:
        return res.get("payload").get('value')
    

async def _add_items_to_dataset_with_feedback_score(result: Dict[str, Any], feedback_score: int) -> None:
    """
    Add items (Rational_planner, Cypher_generator, and Graph_augmenter) to dataset based on the feedback score.
    """
    try:
        user_question = result['messages'][0].content
        rational_plan = result['messages'][1].content

        if feedback_score == -1:
            cypher_generator = result['messages'][-3].content
        else:
            cypher_generator = result['messages'][-4].content
            graph_augmenter = result['messages'][-1].content
        
        RocloOpikTracker.add_item_to_dataset(
            item = {'input': user_question, 'output': rational_plan}, dataset_name=f"Rational_Planner_score_{feedback_score}"
        )
        RocloOpikTracker.add_item_to_dataset(
            item = {'input': user_question, 'output': cypher_generator, 'retry': (len(result['messages'])-3) / 3}, dataset_name=f"Cypher_Generator_score_{feedback_score}"
        )

        if feedback_score != -1:
            RocloOpikTracker.add_item_to_dataset(
                item = {'input': user_question, 'output': graph_augmenter}, dataset_name=f"Graph_Augmenter_score_{feedback_score}"
            )
    except Exception as e:
        logging.getLogger(f"{result['user_id']}-{result['session_id']}").error(f"Error while adding items to dataset: {str(e)}", )