import streamlit as st
from typing import Dict
import json
from graph import create_graph, compile_workflow
import tempfile
import os


QUESTIONS = {
    "income_range": {
        "label": "Monthly Income Range",
        "options": ["Below ₹50,000", "₹50,000 - ₹1,00,000", "Above ₹1,00,000"]
    },
    "investment_horizon": {
        "label": "Investment Timeframe",
        "options": ["Short Term (0-3 years)", "Medium Term (3-7 years)", "Long Term (7+ years)"]
    },
    "risk_tolerance": {
        "label": "Risk Tolerance",
        "options": ["Conservative", "Moderate", "Aggressive"]
    },
    "investment_goal": {
        "label": "Investment Goal",
        "options": ["Wealth Creation", "Regular Income", "Tax Saving", "Retirement"]
    }
}

print("Creating Graph and compiling workflow")
graph = create_graph()
workflow = compile_workflow(graph)
print("Graph and workflow created")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "settings" not in st.session_state:
        st.session_state.settings = {}

def get_response(message: str, settings: Dict):
    iteration = 40
    dict_inputs = {"question": message + ' ' + json.dumps(settings)}
    limit = {"recursion_limit": iteration}

    response_text = ""
    attachments = []

    # Process through workflow
    for event in workflow.stream(dict_inputs, limit):
        if "output" in event:
            string_obj = event['output']["output_response"]["content"]
            json_obj = json.loads(string_obj)
            response = json_obj["response"]
            response_text += response

            # Handle attachments
            if json_obj.get("attachment"):
                print(json_obj["attachment"])
                attachments.append({
                    "name": json_obj["filename"],
                    "url": json_obj["attachment"]
                })

    return response_text, attachments

def display_file(file_data, message_index: int=0):
    """Helper function to display files in Streamlit"""
    name = file_data["name"]
    url = file_data["url"]
    
    st.markdown(f'<a href="{url}" target="_blank" download="{name}">📥 Download {name}</a>', unsafe_allow_html=True)

    # # Create a temporary file to store the content
    # with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(name)[1]) as tmp:
    #     # Download and write the file content
    #     # You'll need to implement the actual file download logic here
    #     # For now, assuming the url contains the file content
    #     tmp.write(url.encode())
    #     tmp_path = tmp.name

    # # Display the file based on its type
    # if name.lower().endswith(('.png', '.jpg', '.jpeg')):
    #     st.image(tmp_path, caption=name)
    # elif name.lower().endswith('.pdf'):
    #     st.download_button(
    #         label=f"Download {name}",
    #         data=open(tmp_path, 'rb'),
    #         file_name=name,
    #         mime="application/pdf",
    #         key=f"download_pdf_{message_index}_{name}"
    #     )
    # else:
    #     st.download_button(
    #         label=f"Download {name}",
    #         data=open(tmp_path, 'rb'),
    #         file_name=name,
    #         key=f"download_file_{message_index}_{name}"
    #     )

    # # Clean up the temporary file
    # os.unlink(tmp_path)

def main():
    st.set_page_config(layout="wide")
    initialize_session_state()

    # Create two columns: sidebar (left) and chat (right)
    with st.sidebar:
        st.title("Investment Profile")
        st.markdown("---")
        
        # Create dropdowns in sidebar
        for key, question in QUESTIONS.items():
            st.session_state.settings[key] = st.selectbox(
                question["label"],
                options=[""] + question["options"],
                key=f"select_{key}"
            )

        st.markdown("---")
        st.subheader("Current Settings")
        for key, value in st.session_state.settings.items():
            if value:
                st.write(f"{QUESTIONS[key]['label']}: {value}")

    # Main chat area
    st.title("Financial Advisor Chat")

    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Display any attachments
            if "attachments" in message:
                for attachment in message["attachments"]:
                    display_file(attachment, idx)

    # Chat input
    if prompt := st.chat_input("Ask your question here..."):
        # Validate all fields are filled
        # empty_fields = [QUESTIONS[k]["label"] for k, v in st.session_state.settings.items() if not v]
        
        # if empty_fields:
        #     with st.chat_message("assistant"):
        #         st.error(
        #             "Please fill out all fields in the sidebar first:\n" + 
        #             "\n".join(f"- {field}" for field in empty_fields)
        #         )
        # else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display response
        response, attachments = get_response(prompt, st.session_state.settings)
        message = {
            "role": "assistant",
            "content": response,
            "attachments": attachments
        }
        st.session_state.messages.append(message)
        
        with st.chat_message("assistant"):
            st.markdown(response)
            for attachment in attachments:
                display_file(attachment)

if __name__ == "__main__":
    main()