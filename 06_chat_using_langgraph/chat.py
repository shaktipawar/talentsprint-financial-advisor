import os
import chainlit as cl
from graph import create_graph, compile_workflow
import json
from termcolor import colored

# Set the working directory to the project root
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the graph and workflow
print("Creating Graph and compiling workflow")
graph = create_graph()
workflow = compile_workflow(graph)
print("Graph and workflow created")

# Chainlit Chat Functionality
@cl.on_message
async def respond(query: str):
    iteration = 40
    dict_inputs = {"question": query.content}
    limit = {"recursion_limit": iteration}

    # Stream through the workflow
    response_text = ""
    for event in workflow.stream(dict_inputs, limit):
        if "output" in event:
            response = event['output']["output_response"]["content"]
            response_text += response

    # Send the AI response back to the user
    await cl.Message(content=response_text).send()
    #await cl.Message(content=response).send()
