import json
from model import get_open_ai, get_open_ai_json
from state import AgentGraphState 
class Agent:

    def __init__(self, state : AgentGraphState):
        self.state = state
        self.model = "gpt-4o-mini"
        self.server = "openai"
        self.temperature = 0
        self.agentflow = ""
        self.messages = []
        self.chatllm = self.get_llm()

    def get_llm(self, json_model= True):
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
        
    def update_state(self, key, value):
        self.state = {**self.state, key:value}

    def check_for_content(self, var):

        next_agent = ""
        message = ""
        response = ""

        if var is None:
            return "EMPTY", "EMPTY", "EMPTY"
        
        if isinstance(var, list):
            if len(var) > 0:
                for item in var:
                    if hasattr(item, "next_agent"):  # Ensure the object has the 'content' attribute
                        next_agent = item.next_agent
                    if hasattr(item, "message"):
                        message = item.message
                    if hasattr(item, "reponse"):
                        message = item.response

        
        return next_agent, message, response

    def updateflow(self, agent_name):
        if self.agentflow == "": 
            self.agentflow += f"{agent_name} " 
        else: 
            self.agentflow += f"--> {agent_name}"

    def convert_to_json(self, content):
        json_obj = json.loads(content)
        return json_obj
    

    
