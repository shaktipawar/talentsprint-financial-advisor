# Prerequisites
* Create vitual environment on your system (for Windows)
    ```
    cd 06_chat_using_langgraph
    python -m venv venv
    cd venv
    cd scripts
    activate
    cd..
    cd..

    pip install -r requirements.txt
    ```
* Inside 06_chat_using_langgraph, create config.yaml and update your OPENAI_API_KEY.
    ```
    OPENAI_API_KEY: "<<ADD YOUR OPEN_AI_KEY>>"
    ```


# Folder and File Details.

## 03_chromadb (folder)
* ChromaDB as vector database. 
* Folder acts a location to store vector embeddings.

## 06_chat_using_langgraph (folder)

* Holds code for Muti-Agent workflow using Langgraph

### agents (folder)

* Lists all Agents

### prompt_templates (folder)

* Lists all Prompt Templates

### app.py

* Executes Graph without Frontend (for Developers)

### chat.py

* Frontend for Chat messaging.

* Implemented using Chainlit.

### graph.py

* Implements Graph Workflow

### model.py

* Returns Chat and Embedding model.

### requirements.txt

* Represents all Installed Packages.

### state.py

* Schema for State of Graph