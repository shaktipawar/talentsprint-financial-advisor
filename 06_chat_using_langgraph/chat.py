import os
import chainlit as cl
from graph import create_graph, compile_workflow
import json
from termcolor import colored

# Import the financial advisor module directly
from importlib import import_module
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Set the working directory to the project root
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the graph and workflow
print("Creating Graph and compiling workflow")
graph = create_graph()
workflow = compile_workflow(graph)
print("Graph and workflow created")

# Import financial advisor functions
from chainlit_financial_advisor import (
    QUESTIONS, 
    user_responses, 
    get_recommendation
)

# Global variable to track financial advisor state
financial_advisor_active = False
current_question_key = None

@cl.on_chat_start
async def start():
    global financial_advisor_active
    
    # Add a button to launch financial advisor
    await cl.Message(
        content="Our product is currently in its Alpha phase, and while we are diligently working towards launching the full version, we are pleased to offer you two options for assistance:\n\n"
        "1. You may share your investment requirements via our selection menu, and we will provide you with a concise overview of financial advice. To access this feature, please click on the Snapshot Financial Advice button.\n\n"
        "2. Alternatively, you may initiate a direct chat with us, during which we will furnish you with a comprehensive analysis and guidance on Mutual Funds ONLY.\n\n"
        "We appreciate your understanding and patience as we enhance our product to better serve your needs.",
        actions=[
            cl.Action(
                name="launch_financial_advisor", 
                value="launch", 
                label="Snapshot Financial Advice"
            )
        ]
    ).send()

@cl.action_callback("launch_financial_advisor")
async def launch_financial_advisor(action):
    global financial_advisor_active, current_question_key, user_responses
    
    # Reset the state
    financial_advisor_active = True
    current_question_key = "income_range"
    user_responses.clear()
    
    # Welcome message
    await cl.Message(
        content="Welcome to your personal financial planning session! 🌟\n\n"
        "I'll ask you a series of questions to understand your financial situation "
        "and provide personalized recommendations. Let's begin!"
    ).send()
    
    # Ask first question
    await ask_financial_advisor_question()

async def ask_financial_advisor_question():
    global current_question_key
    
    if current_question_key is None:
        return
    
    question_data = QUESTIONS[current_question_key]
    
    # Create a message with the question and options
    await cl.Message(content=question_data["question"]).send()
    
    # Add options as clickable elements
    actions = [
        cl.Action(name="financial_advisor_select", value=option, label=option)
        for option in question_data["options"]
    ]
    
    await cl.Message(
        content="Please select an option:", 
        actions=actions
    ).send()

@cl.action_callback("financial_advisor_select")
async def handle_financial_advisor_selection(action):
    global current_question_key, user_responses
    
    # Store the response
    user_responses[current_question_key] = action.value
    
    # Show acknowledgment
    await cl.Message(f"Got it! You selected: {action.value}").send()
    
    # Get next question
    questions = list(QUESTIONS.keys())
    current_index = questions.index(current_question_key)
    
    if current_index < len(questions) - 1:
        # Move to next question
        current_question_key = questions[current_index + 1]
        
        await cl.Message("Let's move on to the next question...").send()
        await ask_financial_advisor_question()
    else:
        # Generate final recommendation
        recommendation = get_recommendation(user_responses)
        
        await cl.Message(
            "Thank you for providing all the information! "
            "I've analyzed your responses and prepared a personalized recommendation."
        ).send()
        
        await cl.Message(recommendation).send()
        
        # Reset the state
        current_question_key = None
        
        # Add restart option
        await cl.Message(
            content="Would you like to start over with a new assessment?",
            actions=[
                cl.Action(name="launch_financial_advisor", value="restart", label="Restart Assessment")
            ]
        ).send()

@cl.on_message
async def respond(message: cl.Message):
    global financial_advisor_active
    
    # If financial advisor is active, ignore workflow processing
    if financial_advisor_active and current_question_key is not None:
        return
    
    # Reset financial advisor state if a normal message is sent
    financial_advisor_active = False
    print('#########################')
    print(user_responses)
    # Original workflow processing
    iteration = 40
    dict_inputs = {"question": message.content+' '+json.dumps(user_responses)}
    limit = {"recursion_limit": iteration}

    # Stream through the workflow
    response_text = ""
    elements = []
    for event in workflow.stream(dict_inputs, limit):
        if "output" in event:
            string_obj = event['output']["output_response"]["content"]
            json_obj = json.loads(string_obj)
            response = json_obj["response"]
            response_text += response

            if json_obj["attachment"]:
                elements = [
                    cl.File(
                        name= json_obj["filename"],
                        url = json_obj["attachment"],
                        display="inline",
                    ),
                ]
    
    await cl.Message(content=response_text, elements=elements).send()

if __name__ == "__main__":
    cl.run()