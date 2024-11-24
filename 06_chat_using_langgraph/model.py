import os, yaml
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

config_path = os.path.join(os.path.dirname(__file__), '', '', 'config.yaml')

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)
    for key, value in config.items():
        os.environ[key] = value

def get_open_ai(temperature=0, model='gpt-4o-mini'):

    llm = ChatOpenAI(
        model=model,
        temperature = temperature
    )
    return llm

def get_open_ai_json(temperature=0, model='gpt-4o-mini'):
    
    llm = ChatOpenAI(
        model=model,
        temperature = temperature,
        model_kwargs={"response_format": {"type": "json_object"}}
    )
    return llm

def get_embedding_model(model = "text-embedding-ada-002"):
    
    llm = OpenAIEmbeddings(
        model = model
    )
    return llm