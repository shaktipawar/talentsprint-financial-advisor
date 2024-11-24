import json
from agents.agent import Agent
from prompt_templates import output_template
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class Output_Agent(Agent):

    def invoke(self, question, reviewer_response = None):

        agent_name = "OUTPUT AGENT"

        value = reviewer_response() if callable(reviewer_response) else reviewer_response
        r_next_agent, r_message, r_response  = self.check_for_content(value)

        p_agents_message = self.state["previous_agents_response"][-1].content


        # Setting message in templates
        template = output_template.template
        prompt = template.format(Placeholder1 = p_agents_message)
        #message = [SystemMessage(content = prompt),HumanMessage(content = question)]
        message = [
            {"role" : "system", "content" : str(prompt)},
            {"role" : "user", "content" : str(question)},
        ]


        # Extends as message is a list.
        self.messages.extend(message)

        # Talk to OpenAI.
        response = self.chatllm.invoke(message)
        json_object = self.convert_to_json(response.content)

        # Append as AIMessage is an object.
        #aimessage_object = AIMessage(content = json.dumps(json_object))
        aimessage_object = {"role" : "assistant", "content" : str(json_object["response"])}
        self.messages.append(aimessage_object)
        
        # Update state object.
        self.update_state("next_agent", "")
        self.update_state("previous_agents_response", json_object["response"])
        self.update_state("output_response", aimessage_object)

        self.print_agents_output(agent_name, json_object, "light_yellow")
        self.updateflow(agent_name)
        
        return self.state