import streamlit as st
import requests
from typing import Optional

# Base URL and credentials
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "0fe13348-39ca-4cf7-9c36-5aed5597f4a1"
FLOW_ID = "9af597b9-c435-411d-8e64-6d1382f827d5"
APPLICATION_TOKEN = "AstraCS:AonHETebNgrhCYFjyAxlHBmU:9a9cdf1d368612b43a6f78d813a695bd1ce777d0ba8b40b3d796a3c2e655e4d5"  # Replace with your token

# Default tweaks dictionary
TWEAKS = {}

def run_flow(message: str, endpoint: str, tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks

    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call API. Status code: {response.status_code}"}

# Custom CSS for styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f6;
            color: #333;
        }
        .main-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            color: #1e88e5;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .sub-header {
            font-size: 1.2rem;
            color: #757575;
            text-align: center;
            margin-bottom: 2rem;
        }
        .input-section {
            background-color: #f5f7fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .stTextInput>div>div>input {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }
        .stButton>button {
            background-color: #1e88e5;
            color: white;
            font-weight: 500;
            padding: 0.6rem 1.2rem;
            border-radius: 25px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:hover {
            background-color: #1565c0;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        .response-container {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-top: 2rem;
            border-left: 5px solid #1e88e5;
        }
        .sidebar .sidebar-content {
            background-color: #e8eaf6;
            padding: 1rem;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main App Layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">SWIEZ</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-powered assistant. Ask me anything!</p>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
user_query = st.text_input(
    "Ask :",
    "",
    placeholder="Type your question here...",
    help="Your query will be processed by our advanced AI model.",
)
st.markdown('</div>', unsafe_allow_html=True)

# Submit Button
if st.button("Get Answer"):
    if not user_query.strip():
        st.warning("Please enter a question for Bot.")
    else:
        # Run the flow
        with st.spinner("Bot is thinking..."):
            response = run_flow(user_query, FLOW_ID, TWEAKS)

        # Display results
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        if "error" in response:
            st.error(response["error"])
        else:
            st.success("Bot has an answer for you!")
            outputs = response.get("outputs", [])
            if outputs:
                results = outputs[0].get("outputs", [{}])[0].get("results", {})
                message = results.get("message", {}).get("data", {}).get("text", "I couldn't generate a response. Please try asking another question.")
                st.markdown(f"**Bot:** {message}")
            else:
                st.info("Bot is having trouble processing your request. Please try again.")

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🤖 About Bot")
st.sidebar.info(
    """
    **Bot - Your AI Assistant**
    - Powered by advanced language models
    - Seamlessly answers your questions on various topics
    - Continuously learning and improving
    
    Got feedback? Let us know how we can make Bot even better!
    """
)

