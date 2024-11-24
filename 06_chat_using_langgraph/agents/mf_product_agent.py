import json
from agents.agent import Agent
from prompt_templates import mf_product_template
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class MF_Products_Agent(Agent):

    def invoke(self, question, reviewer_response = None):

        agent_name = "MF PRODUCTS AGENT"

        value = reviewer_response() if callable(reviewer_response) else reviewer_response
        r_next_agent, r_message, r_response = self.check_for_content(value)

        if(len(self.state["reviewer_response"]) > 0):
            r_response = self.state["reviewer_response"][-1].content
            #r_response = json.loads(self.state["reviewer_response"][-1].content)["response"]

        # Dummy product.
        # this needs to be changed with TTS.
        product_name = "HDFC EQUITY MUTUAL FUND, AXIS INFRA MUTUAL FUND, ICICI LOMBARD ENERGY FUND"

        # Setting message in templates
        template = mf_product_template.template
        prompt = template.format(Placeholder1 = product_name,
                                 Placeholder2 = r_response)
        
        #message = [SystemMessage(content = prompt),HumanMessage(content = question)]
        message = [
            {"role" : "system", "content" : prompt},
            {"role" : "user", "content" : question},
        ]

        # Extends as message is a list.
        self.messages.extend(message)

        # Talk to OpenAI.
        response = self.chatllm.invoke(message)
        json_object = self.convert_to_json(response.content)

        # Append as AIMessage is an object.
        #aimessage_object = AIMessage(content = json.dumps(json_object))
        aimessage_object = {"role" : "assistant", "content" : json_object["response"]}
        self.messages.append(aimessage_object)

        # Update state object.
        self.update_state("next_agent", json_object["next_agent"])
        self.update_state("previous_agents_response", json_object["response"])
        self.update_state("mf_product_response", aimessage_object)

        self.print_agents_output(agent_name, json_object, "light_yellow")
        self.updateflow(agent_name)
        
        return self.state