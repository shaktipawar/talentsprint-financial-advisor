import json
from agents.agent import Agent
from prompt_templates import output_template
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from helper import Helper, MessageType
class Output_Agent(Agent):

    def invoke(self, question):

        agent_name = "OUTPUT AGENT"
        Helper.print(MessageType.AGENT_MESSAGE, "AGENT NAME", agent_name)


        p_agents_message = "EMPTY"
        if(len(self.state["previous_agents_response"]) > 0):
            p_agents_message = self.state["previous_agents_response"][-1].content

        # Setting message in templates
        template = output_template.template
        prompt = template.format(Placeholder1 = p_agents_message)
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
        #aimessage_object = AIMessage(content = json.dumps(json_object)) # We are using the whole object, as it has attachment and filename attributes aswell.
        
        # Here, we need to pass the whole json_object in content so that 
        # the fronend can read other properties from this object like attachment, file_name
        aimessage_object = {"role" : "assistant", "content" : json.dumps(json_object)} 
        self.messages.append(aimessage_object)
        
        # Update state object.
        self.update_state("next_agent", "") #No Next Agent.
        self.update_state("previous_agents_response", json_object["response"])
        self.update_state("output_response", aimessage_object)

        Helper.print(MessageType.AI_MESSAGE, "AI RESPONSE", aimessage_object)

        self.updateflow(agent_name)
        
        return self.state