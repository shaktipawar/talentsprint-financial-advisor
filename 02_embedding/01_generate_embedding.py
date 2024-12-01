import json
import os,yaml
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from helper.utility import Utitlity

config_path = os.path.join(os.path.dirname(__file__), '', '', 'config.yaml')

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)
    for key, value in config.items():
        os.environ[key] = value


# HERE WE ARE NOT USING 
# DATALOADING.
# SPLITTING STRATEGIES FOR CHUNKING
# AS THE DATA IS ALREADY PREPROCESSED AND KEPT IN THE JSON FORMAT.
# WE JUST NEED TO FETCH THE JSON OBJECT AND GET THE REQUIRED ATTRIBUTES EMBEDDING USING RESPECTIVE EMBEDDING MODEL
# AND SAVE THE DOCUMENT IN VECTORDB.
class Generate_Embeddings():

    def __init__(self, name_of_colletion):
        # Define path for persistent storage outside the root folder
        persistent_directory = os.path.join('..', '03_chromadb')

        self.embedding_model = Utitlity.get_embedding_model()

        # Initialize ChromaDB vector store
        self.vector_db = Chroma(
            persist_directory = persistent_directory, 
            collection_name = name_of_colletion, 
            embedding_function = self.embedding_model)

    def load_json_data(self, filepath):
        # Load the JSON data from a file (replace with your actual file path)
        with open(filepath, 'r') as file: #filepath
            self.json_data = json.load(file)
    
    def add_documents(self):
        
        documents = []
        
        for item in self.json_data:

            # Prepare metadata and Document object
            metadata = {
                "Question": item["Question"],
                "Financial Instrument": "Mutual Fund"
            }

            # Create Document object with content and metadata
            document = Document(
                page_content=item["Answer"], 
                metadata=metadata)

            documents.append(document)

            # Add documents to vector store
        self.vector_db.add_documents(documents)

# Usage Example
if __name__ == "__main__":

    ge = Generate_Embeddings("mutual_fund_faq") # pass name of the collection where you want to create embeddings.

    # Get the current working directory
    cwd = os.getcwd()

    # Create the 'assets' folder path
    data_folder = os.path.join(cwd, '02_embedding','data')

    # Create the full path for the CSV file
    file_path = os.path.join(data_folder, "01_mutual_funds.json")

    ge.load_json_data(file_path)

    ge.add_documents()
