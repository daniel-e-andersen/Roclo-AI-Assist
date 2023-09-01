import chainlit as cl
from typing import Dict, Any
import json
import logging

async def routing_from_rational_planner(state: Dict[str, Any]) -> str:
    """  
    Define the routing target based on the output of the rational planner.  

    Args:  
        state (Dict[str, Any]): The current state containing message and routing information.  

    Returns:  
        str: The routing target indicating the next action to take.  
    """
    message = state['messages'][-1]

    if "no rational plan is required" in message.content.lower():
        task_2 = cl.Task(title = "Answering your question", status = cl.TaskStatus.RUNNING)
        cl.user_session.set("task", task_2)
        await cl.user_session.get("task_list").add_task(task_2)
        await cl.user_session.get("task_list").send()
        return "__end__"
    
    else:
        task_2 = cl.Task(title = "Retrieving data from Oaklins", status = cl.TaskStatus.RUNNING)
        cl.user_session.set("task", task_2)
        await cl.user_session.get("task_list").add_task(task_2)
        await cl.user_session.get("task_list").send()
        return "__continue__"

        


async def routing_from_db_retriever(state: Dict[str, Any]) -> str:
    """  
    Determine the next step based on the graph retrieval result.  

    Args:  
        state (Dict[str, Any]): The state containing the retrieval message.  

    Returns:  
        str: The next action to take.  
    """
    message = state['messages'][-1].content

    # If number of agent invoke calls larger than 12 (>=13), stop the agent graph invokation.
    if len(state['messages']) > 12:
        if message.startswith("No data was retrieved"):
            content = "I apologize, but I'm unable to find the relevant information to answer your question. " +\
            "Could you please provide additional details or rephrase your question? This will help me give you a more accurate and helpful response. Thank you for your understanding."
        elif message.startswith("The data retrieval process has exceeded the expected volume"):
            content = "I apologize, but your question involves a larger amount of data than I can effectively process within my current limitations. " +\
            "To provide you with an accurate and helpful response, would you mind breaking down your question into smaller parts or asking a more specific question? " +\
            "This will help me better assist you. Thank you for your patience."
        elif message.startswith("I encountered an issue"):
            content = "I apologize, but I wasn't able to properly process your question. " +\
            "It seems there might have been an issue retrieving the necessary information. " +\
            "Would you mind starting a new chat session and rephrasing your question with additional context? " +\
            "This will help me provide you with a more accurate and helpful response. Thank you for your understanding."

        # Send message to user about the error case.
        await cl.Message(content = content).send()
        return "__end__"

    if message.startswith("No data was retrieved") or message.startswith("The data retrieval process has exceeded the expected volume") or message.startswith("I encountered an issue"):
        return "query_generator"
    
    # If the retrieved data is correct, update the task list.
    cl.user_session.get("task").status = cl.TaskStatus.DONE
    task_3 = cl.Task(title = "Answering your question", status = cl.TaskStatus.RUNNING)
    cl.user_session.set("task", task_3)
    await cl.user_session.get("task_list").add_task(task_3)
    await cl.user_session.get("task_list").send()

    # route augments
    try:
        retrieved_data = json.loads(message)
        
        if len(retrieved_data) >=2 and len(retrieved_data[0]) >= 3:
            logging.getLogger(f"{state['user_id']}-{state['session_id']}").info("Route to prioritizer")
            return "prioritizer"
        else:
            logging.getLogger(f"{state['user_id']}-{state['session_id']}").info("Route to plain_augmenter")
            return "plain_augmenter"
    except Exception as e:
        logging.getLogger('main').error(f"Error while result routing: {e}")
        raise

