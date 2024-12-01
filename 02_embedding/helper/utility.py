from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import OllamaEmbeddings

#Load configuration file
import configparser
config = configparser.ConfigParser()
config.read('../.config')

class Utitlity():

    def get_embedding_model():
        return OpenAIEmbeddings(
            model="text-embedding-ada-002",
            api_key="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") #text-embedding-ada-002,  # text-embedding-3-small
    
        # return OllamaEmbeddings(
        #     model="nomic-embed-text")
    
    def get_chat_completion_model():
        return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2 #,
                #api_key=config['OPENAI']['API_KEY']
                )
     