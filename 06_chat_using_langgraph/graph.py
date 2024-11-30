import json
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from termcolor import colored
from agents.agent import Agent
from agents.router_agent import Router_Agent
from agents.mf_faq_agent import MF_FAQ_Agent
from agents.mf_product_agent import MF_Products_Agent
from agents.reviewer_agent import Reviewer_Agent
from agents.output_agent import Output_Agent
from agents.endnode_agent import EndNodeAgent
from state import AgentGraphState, state


def create_graph():

    # INITIALIZE GRAPH
    graph = StateGraph(AgentGraphState)

    # ROUTER
    graph.add_node(
        "router",
        lambda state: Router_Agent(state = state).invoke(
            question = state["question"]
        ))

    # MF FAQ
    graph.add_node(
        "mf_faq",
        lambda state: MF_FAQ_Agent(state = state).invoke(
            question = state["question"]
        ))
    
    # MF PRODUCTS
    graph.add_node(
        "mf_products",
        lambda state: MF_Products_Agent(state = state).invoke(
            question = state["question"]
        ))
    
    # REVIEWER
    graph.add_node(
        "reviewer",
        lambda state: Reviewer_Agent(state = state).invoke(
            question = state["question"]
        ))
    
    # OUTPUT
    graph.add_node(
        "output",
        lambda state: Output_Agent(state = state).invoke(
            question = state["question"]
        ))

    # END
    # graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    # EDGES
    graph.set_entry_point("router")

    # graph.add_edge("router", "mf_faq")
    # graph.add_edge("router", "mf_products")
    # graph.add_edge("router", "reviewer")

    graph.add_edge("mf_faq", "reviewer")
    graph.add_edge("mf_products", "reviewer")

    # graph.add_edge("reviewer", "output")
    # graph.add_edge("reviewer", "router")

    # CONDITIONAL EDGES
    graph.add_conditional_edges(
        "reviewer",
        # pass_review method can be made obsolete.
        # incase we are able to store next_agent in State object.
        lambda state : state["next_agent"][-1].content #get_agent(state=state) # router / output
    )

    graph.add_conditional_edges(
        "router",
        lambda state : state["next_agent"][-1].content #get_agent(state=state) # mf_faq / mf_products / output
    )

    graph.set_finish_point("output")
    
    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow

def get_agent(state: AgentGraphState):
    return state["next_agent"][-1].content




# Define the edges in the agent graph
def pass_review(state: AgentGraphState, state_key : str, current_agent = None):

    if state_key == "router_response":
        review_list = state["router_response"]
    elif state_key == "reviewer_response":
        review_list = state["reviewer_response"]
    else:
        review_list = None

    if review_list:
        review = review_list[-1]
    else:
        review = "No review"

    if review != "No review":
        if isinstance(review, HumanMessage):
            review_content = review.content
        else:
            review_content = review
        
        review_data = json.loads(review_content)
        next_agent = review_data["next_agent"]
    else:
        next_agent = "end"
    
    print(colored(f"NEXT AGENT : {next_agent}", "blue"))
    print(colored("------", "blue"))
    
    return next_agent
