import os, json


from agents.agent import Agent
from prompt_templates import mf_faq_template
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_chroma import Chroma
from model import get_embedding_model
from termcolor import colored

class MF_FAQ_Agent(Agent):

    def invoke(self, question, reviewer_response = None):

        agent_name = "MF FAQ AGENT"
        print(f"Current working directory: {os.getcwd()}")

        value = reviewer_response() if callable(reviewer_response) else reviewer_response
        r_next_agent, r_message, r_response = self.check_for_content(value)

        if(len(self.state["reviewer_response"]) > 0):
            r_response = self.state["reviewer_response"][-1].content

        # Similarity Search
        persistent_directory = os.path.join('..','03_chromadb')
        collection_name = "mutual_fund_faq"
        embedding_model = get_embedding_model()
        vector_db = Chroma(persist_directory=persistent_directory, collection_name=collection_name, embedding_function=embedding_model)
        results = vector_db.similarity_search_with_score(question, k=1)

        # Setting default value, 
        # incase search operation does not find any result
        vectorsearch_result = "EMPTY"

        for result, score in results:
            vectorsearch_result = result.page_content
            
        # Setting message in templates
        template = mf_faq_template.template
        prompt = template.format(Placeholder1 = vectorsearch_result,
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
        self.update_state("mf_faq_response", aimessage_object)

        self.print_agents_output(agent_name, json_object, "light_yellow")
        self.updateflow(agent_name)
        
        return self.state