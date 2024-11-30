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


# Steps to Execute
* Open File Server Port (Windows)

    Open a new command prompt.
    ```
    cd 06_chat_using_langgraph
    python -m venv venv
    cd venv
    cd scripts
    activate
    cd..
    cd..

    python fileserver.py
    ```

* You can either opt for Developer mode / UI Mode.

    Open a new command prompt.

    * Developer mode (Windows)

        ```
        cd 06_chat_using_langgraph
        python -m venv venv
        cd venv
        cd scripts
        activate
        cd..
        cd..

        python app.py
        ```

    * UI mode (Window)
    
        ```
        cd 06_chat_using_langgraph
        python -m venv venv
        cd venv
        cd scripts
        activate
        cd..
        cd..

        chainlit run chat.py
        ```


# Questions

Following are example questions (but not limited to following). It is noted just to give a perspective.

### Greetings : Messages
* Greetings !
* How are you ?
* Hope you are enjoying this bright sunny day !!
* Hope you are having a great day.
* Greetings ! Who are you ?
* Good evening !
* Good afternoon !

### Out of Scope task : Messages
* Book an appointment with my hair dresser
* Can you book a flight ticket from MUM to DEL
* Connect my call to Drive.
* Paint me a scenic picture.
* Tell me a story 
* Tell me a joke (Need to add fix for this question. DONE)
* Sing a song for me.

### Mutual Fund Domain : General FAQs
* What is Open-ended Fund/Scheme ?
* What is the history of Mutual Funds in India and role of SEBI in mutual funds industry?
* How is a mutual fund set up?
* Growth/Equity Oriented Scheme (This question comes under Domain and Product both.)
* Money Market or Liquid Schemes
* What are Exchange Traded Funds (ETFs)? (This question went to MDF Product Agent, and needs a fix.)
* When will the investor get statement of account after investing in a mutual fund and\nwhat is a consolidated account statement (CAS)?
* What is application supported by blocked amount (ASBA)? (Router is unable to route this question to MFFAQ Agent, and needs a fix. DONE)
* What is Systematic Withdrawal Plan (SWP)?
        

### Mutual Fund Product : Insights based on analysis of Product and multiple parameters
* Suggest Mutual Funds which has given highest returns in year 2024
* Suggest NAV of Grindlays Super Saver Mutual Fund
* Suggest Mutual Fund Products from Standard Chartered

* Which mutual funds have the highest CAGR over a 1-year, 3-year, and 5-year period?
* Which funds exhibit the lowest volatility and the highest Sharpe Ratio, indicating the best risk-adjusted returns?
* What is the average maximum drawdown for funds across different categories, and which category is the least risky?
* How do the returns of funds in different categories (e.g., Equity, Debt, Hybrid) compare over various time frames?
* Which fund houses consistently outperform in terms of CAGR and Sharpe Ratio?
* Are there any categories of funds that tend to perform well in shorter durations (e.g., 1 week or 1 month) compared to long durations (e.g., 3 years or 5 years)?
* Is there a significant relationship between volatility and CAGR returns? (This quesion was considered out of context, Ideally it should have been routed to MF FAQ Agent)
* Based on historical performance and risk metrics, which funds would be suitable for conservative, moderate, and aggressive investors?
* How do the latest NAV values compare across top-performing funds, and do higher NAVs correlate with better returns?
* Are there funds with unusually high Sharpe Ratios but low returns, or vice versa, indicating potential anomalies?


* If investment horizon is long and risk tolerance is Aggressive. Find top 5 Mutual Fund under Small Cap equity category with highest CAGR in past 5 years
* If investment horizon is long and risk tolerance is Moderately Aggressive. Find top 5 Mutual Fund under Multi Cap equity category with highest CAGR in past 5 years
* If investment horizon is medium and risk tolerance is Conservative. Find top 5 Mutual Fund under hybrid category with highest CAGR in past 5 years
* If the financial goal is tax saving and risk tolerance is  Aggressive. Find top 5 Mutual Fund under ELSS category with highest CAGR in past 5 years
* If the financial goal is Income. Find top 5 Mutual Fund under Income category with highest CAGR in past 5 years
* If the investment horizon in short and risk tolerance is Conservative. Find top 5 Mutual Fund under Debt Scheme - Liquid Fund category with highest CAGR in past 5 years
* If the investment horizon in medium and risk tolerance is Moderate. Find top 5 Mutual Fund under Index Fund Scheme category with highest CAGR in past 5 years
* If the investment goal is income(pension). Find top 5 Mutual Fund under Income category with highest CAGR in past 5 years
* If the investment goal is Home Purchase.
Find top 5 Mutual Fund under Large Cap category with highest CAGR in past 5 years
Find top 5 Mutual Fund under Index fund category with highest CAGR in past 5 years
* If the investment goal is Childs education
Find top 5 Mutual Fund under small Cap category with highest CAGR in past 5 years
Find top 5 Mutual Fund under Index Fund category with highest CAGR in past 5 years

<br>
<br>


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

### fileserver.py

* Helps in download File from separate http port.
* Implemented using Flask

### graph.py

* Implements Graph Workflow

### helper.py
* Helper code for Logging using termcolor package.

### model.py

* Returns Chat and Embedding model.

### requirements.txt

* Represents all Installed Packages.

### state.py

* Schema for State of Graph