from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
import json

class AgentGraphState(TypedDict):
    question : str
    router_response : Annotated[list, add_messages]
    mf_faq_response : Annotated[list, add_messages]
    mf_product_response : Annotated[list, add_messages]
    reviewer_response : Annotated[list, add_messages]
    output_response : Annotated[list, add_messages]
    next_agent : Annotated[str, add_messages]
    previous_agents_response : Annotated[str, add_messages]
          
def get_all(state : AgentGraphState, object_key : Literal["router_response", 
                                                          "mf_faq_response",
                                                          "mf_product_response",
                                                          "reviewer_response",
                                                          "output_response"]):
    if state[object_key]:
        val = state[object_key]
        return val

def get_latest(state : AgentGraphState, object_key : Literal["router_response", 
                                                          "mf_faq_response",
                                                          "mf_product_response",
                                                          "reviewer_response",
                                                          "output_response"]):
    if object_key in state:
        if len(state[object_key]) > 0:
            val = state[object_key][-1]  # Safe access
            if object_key == "output_response":
                val = json.loads(val.content)["response"]
                return val
            else:
                return None
        else:
            return None
    else:
        return None  # Or a default value
    
    


state = {
    "question" : "",
    "router_response" : [],
    "mf_faq_response" : [],
    "mf_product_response" : [],
    "reviewer_response" : [],
    "output_response" : [],
    "next_agent" : "",
    "previous_agents_response" : ""
}