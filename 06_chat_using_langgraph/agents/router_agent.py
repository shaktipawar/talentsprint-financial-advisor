import json
from agents.agent import Agent
from prompt_templates import router_template
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from helper import Helper, MessageType
class Router_Agent(Agent):

    def invoke(self, question):

        agent_name = "ROUTER AGENT"
        Helper.print(MessageType.AGENT_MESSAGE, "AGENT NAME", agent_name)

        r_response = "EMPTY"
        if(len(self.state["reviewer_response"]) > 0):
            r_response = self.state["reviewer_response"][-1].content

        # Setting message in templates
        template = router_template.template
        prompt = template.format(Placeholder1 = r_response)

        #message = [SystemMessage(content = prompt),HumanMessage(content = question)]
        message = [
            {"role" : "system", "content" : str(prompt)},
            {"role" : "user", "content" : str(question)},
        ]

        Helper.print(MessageType.PROMPT_MESSAGE, "PROMPT", message)

        # Extends as message is a list.
        self.messages.extend(message)

        # Talk to OpenAI.
        response = self.chatllm.invoke(message)
        json_object = self.convert_to_json(response.content)

        Helper.print(MessageType.LLM_RESPONSE, "LLM RESPONSE", json_object)

        # Append as AIMessage is an object.
        #aimessage_object = AIMessage(content = json.dumps(json_object))
        aimessage_object = {"role" : "assistant", "content" : str(json_object["response"])}
        self.messages.append(aimessage_object)
        
        # Update state object.
        self.update_state("next_agent", json_object["next_agent"])
        self.update_state("previous_agents_response", json_object["response"])
        self.update_state("router_response", aimessage_object)

        Helper.print(MessageType.AI_MESSAGE, "AI RESPONSE", aimessage_object)

        self.updateflow(agent_name)
        
        return self.state