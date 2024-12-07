import chainlit as cl
from typing import Dict
import time

# Store user responses
user_responses = {}

# Define questions and their options
QUESTIONS = {
    "income_range": {
        "question": "What is your annual income range?",
        "options": [
            "Less than ₹50,000", 
            "₹50,000 - ₹1000,000", 
            "₹100,000 - ₹500,000", 
            "₹500,000 - ₹2,500,000", 
            "More than ₹2,500,000"
        ]
    },
    "investment_experience": {
        "question": "How would you rate your investment experience?",
        "options": [
            "Beginner",
            "Intermediate",
            "Advanced",
            "Expert"
        ]
    },
    "risk_tolerance": {
        "question": "What is your risk tolerance level?",
        "options": [
            "Conservative",
            "Moderately Conservative",
            "Moderate",
            "Moderately Aggressive",
            "Aggressive"
        ]
    },
    "financial_goals": {
        "question": "What are your primary financial goals?",
        "options": [
            "Retirement Planning",
            "Wealth Accumulation",
            "Child Education Funding",
            "Home Purchase",
            "Income Generation"
        ]
    },
    "investment_horizon": {
        "question": "What is your investment time horizon?",
        "options": [
            "Less than 5 years",
            "5-10 years",
            "10-20 years",
            "20+ years"
        ]
    }
}

def get_recommendation(responses: Dict[str, str]) -> str:
    """
    Generate a personalized recommendation based on user responses.
    """
    recommendation = "Based on your responses, here's a personalized financial recommendation:\n\n"
    
    # Risk profile based on experience and tolerance
    if responses["risk_tolerance"].startswith("Conservative"):
        risk_profile = "conservative"
    elif responses["risk_tolerance"].startswith("Moderate"):
        risk_profile = "moderate"
    else:
        risk_profile = "aggressive"
    
    # Investment horizon consideration
    long_term = responses["investment_horizon"] in ["10-20 years", "20+ years"]
    
    # Generate recommendation based on risk profile and horizon
    if risk_profile == "conservative":
        recommendation += "• Consider a portfolio heavily weighted in bonds and debt based mutual funds\n"
        recommendation += "• Focus on large-cap dividend-paying stocks\n"
        recommendation += "• Maintain a larger emergency fund (6-12 months of expenses)\n"
    elif risk_profile == "moderate":
        recommendation += "• Consider a balanced portfolio of stocks, mutual funds and bonds\n"
        recommendation += "• Include both mid caps and value stocks\n"
        recommendation += "• Include both index based and mid cap based mutual funds\n"
        recommendation += "• Maintain a moderate emergency fund (4-6 months of expenses)\n"
    else:
        recommendation += "• Consider a portfolio heavily weighted in stocks\n"
        recommendation += "• Include exposure to emerging markets and small-cap stocks and kutual funds\n"
        recommendation += "• Maintain a standard emergency fund (3-4 months of expenses)\n"
    
    # Add goal-specific recommendations
    if responses["financial_goals"] == "Retirement Planning":
        recommendation += "\nFor Retirement Planning:\n"
        recommendation += "• Maximize contributions to retirement accounts like PPF, NSC and KVP\n"
        recommendation += "• Include explosure to dbet and income based Mutual funds\n"
        recommendation += "• Include details on Annuities for regular income\n"
    elif responses["financial_goals"] == "Child Education Funding":
        recommendation += "\nFor Child Education Funding:\n"
        recommendation += "• Look into Child savings plans\n"
        recommendation += "• Consider NPS Vatsalya and Sukanya Samriddhi Yojana\n"
    
    # Add income-based recommendations
    if responses["income_range"].startswith("Less than"):
        recommendation += "\nBudgeting Priorities:\n"
        recommendation += "• Focus on building emergency savings\n"
        recommendation += "• Prioritize debt reduction if applicable\n"
    elif responses["income_range"].endswith("200,000"):
        recommendation += "\nTax Strategy:\n"
        recommendation += "• Consider tax-advantaged investment vehicles\n"
        recommendation += "• Look into charitable giving strategies\n"
    
    return recommendation

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    cl.user_session.set("current_question", "income_range")
    
    await cl.Message(
        content="Welcome to your personal financial planning session! 🌟\n\n"
                "I'll ask you a series of questions to understand your financial situation "
                "and provide personalized recommendations. Let's begin!"
    ).send()
    
    # Ask first question
    await ask_next_question()

async def ask_next_question():
    """Ask the current question"""
    current_question = cl.user_session.get("current_question")
    if current_question is None:
        return
    
    question_data = QUESTIONS[current_question]
    
    # Create a message with the question and options
    msg = cl.Message(content=question_data["question"])
    
    # Add options as clickable elements
    for option in question_data["options"]:
        await msg.send()
        await cl.Message(content=f"- {option}", actions=[
            cl.Action(name="select", value=option, collapsed=False)
        ]).send()

@cl.action_callback("select")
async def handle_option_selection(action):
    """Handle option selection"""
    current_question = cl.user_session.get("current_question")
    if current_question is None:
        return
    
    # Store the response
    user_responses[current_question] = action.value
    
    # Show acknowledgment
    await cl.Message(f"Got it! You selected: {action.value}").send()
    
    # Get next question
    questions = list(QUESTIONS.keys())
    current_index = questions.index(current_question)
    
    if current_index < len(questions) - 1:
        # Move to next question
        next_question = questions[current_index + 1]
        cl.user_session.set("current_question", next_question)
        
        await cl.Message("Let's move on to the next question...").send()
        await ask_next_question()
    else:
        # Generate final recommendation
        cl.user_session.set("current_question", None)
        recommendation = get_recommendation(user_responses)
        
        await cl.Message(
            "Thank you for providing all the information! "
            "I've analyzed your responses and prepared a personalized recommendation."
        ).send()
        
        await cl.Message(recommendation).send()
        
        # Add restart option
        await cl.Message(
            content="Would you like to start over with a new assessment?",
            actions=[cl.Action(name="restart", value="restart")]
        ).send()

@cl.action_callback("restart")
async def handle_restart(action):
    """Handle restart request"""
    user_responses.clear()
    cl.user_session.set("current_question", "income_range")
    await cl.Message("Let's start a new assessment!").send()
    await ask_next_question()

@cl.on_stop
def on_stop():
    """Clean up when the chat stops"""
    user_responses.clear()

#if __name__ == "__main__":
#    cl.run()
