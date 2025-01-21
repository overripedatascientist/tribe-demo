from platform import platform
from typing import Optional
import streamlit as st
import json
import os
import requests
from dotenv import load_dotenv
from pprint import pprint

from settings import CONF_FILE, LANGFLOW_TWEAKS, COUNTRIES, AGE_GROUPS, PLATFORMS, TRIBES

load_dotenv(".env")

# Load configuration from config.json file
def load_config():
    with open(CONF_FILE, 'r') as file:
        return json.load(file)


# Inject custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&display=swap');

        /* Apply Barlow Condensed to the title */
        .title, h1 {
            font-family: 'Barlow Condensed', sans-serif !important;
            font-size: 36px !important;
            color: #333333 !important;
            text-align: center !important;
        }

        /* Optional: Style other elements */
        body, [class*="css"] {
            font-family: 'Barlow Condensed', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Add custom CSS
add_custom_css()


# Function to update tweaks with user inputs
def update_tweaks_with_user_input(
        tweaks: dict,
        chat_input: str,
        tribe: Optional[int] = None,
        age_group: Optional[str] = None,
        country: Optional[str] = None,
        gender: Optional[str] = None,
        platform: Optional[str] = None,
        rag_query: Optional[str] = None,
        min_follower_count: Optional[str] = None,
        min_likes_count: Optional[str] = None):

    if not 'ChatInput-nM66I' in tweaks:
        tweaks['ChatInput-nM66I'] = {}
    tweaks['ChatInput-nM66I']['input_value'] = chat_input

    if tribe and tribe != "":
        tweaks['TextInput-n0QkP'] = {}
        tweaks['TextInput-n0QkP']['input_value'] = tribe

    if age_group and age_group != "":
        tweaks['TextInput-4wKnt'] = {}
        tweaks['TextInput-4wKnt']['input_value'] = age_group  # Age group filter

    if country and country != "":
        tweaks['TextInput-wg8O0'] = {}
        tweaks['TextInput-wg8O0']['input_value'] = country  # Country filter

    if gender and gender != "":
        tweaks['TextInput-WCBMY'] = {}
        tweaks['TextInput-WCBMY']['input_value'] = gender

    if platform and platform != "":
        tweaks['TextInput-aYfSJ'] = {}
        tweaks['TextInput-aYfSJ']['input_value'] = platform

    if min_follower_count and min_follower_count != "":
        tweaks['TextInput-UhThw']['input_value'] = min_follower_count  # Minimum follower count

    if min_likes_count and min_likes_count:
        tweaks['TextInput-P1BmY'] = {}
        tweaks['TextInput-P1BmY']['input_value'] = min_likes_count  # Minimum likes count

    tweaks['TextInput-JZobh'] = {}
    tweaks['TextInput-JZobh']['input_value'] = rag_query  # RAG query

    return tweaks


# Function to extract message from the response
def extract_message(response: dict):
    try:
        # First try to get chat output
        if 'outputs' in response and response['outputs']:
            for output in response['outputs']:
                if 'message' in output:
                    return output['message']['text']

        # Fallback to your original extraction method
        message_text = response['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        return message_text
    except (KeyError, IndexError, TypeError) as e:
        st.error(f"Error extracting message: {e}")
        st.write("Full Response:", response)
        return f"Error: Unable to extract message from the response."


# Function to run flow with Streamlit inputs
def run_flow(message: str,
             tweaks: dict,
             config: dict,
             output_type: str = "chat",
             input_type: str = "chat"):
    """
    Run a flow with a given message and optional tweaks.
    """
    BASE_API_URL = "https://api.langflow.astra.datastax.com"
    langflow_id = config['langflow_id']
    flow_id = config['flow_id']
    api_url = f"{BASE_API_URL}/lf/{langflow_id}/api/v1/run/{flow_id}"

    payload = {
        "inputs": {
            "ChatInput-nM66I": {
                "input_value": message
            }
        },
        "output_type": output_type,
        "input_type": input_type,
        "tweaks": tweaks
    }

    pprint(tweaks)

    # Get token from environment variable
    application_token = os.getenv('ASTRA_DB_VECTOR_TOKEN')
    if not application_token:
        st.error("ASTRA_DB_VECTOR_TOKEN not found in environment variables")
        return None

    # Ensure proper header format
    headers = {
        "Authorization": f"Bearer {application_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Only try to parse JSON if we have content
        if response.content:
            try:
                result = response.json()
                st.write("API Response:", result)

                if 'error' in result:
                    st.error(f"API Error: {result['error']}")
                    return None
                return result
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse API response as JSON: {str(e)}")
                st.write("Raw response:", response.text)
                return None
        else:
            st.error("Empty response received from API")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None


# Streamlit app setup
# st.markdown('<h1 class="title">LangFlow Chat Application</h1>', unsafe_allow_html=True)
st.title('Welcome to The TRIBE Experiment')
st.subheader('Alpha Release')

# Load configuration file
config = load_config()

# Initialize session state for clearing input box
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Reset clear_input flag after setting the text box value
if st.session_state.clear_input:
    st.session_state.clear_input = False

# Load tweaks but do not display them on the page
tweaks = LANGFLOW_TWEAKS.copy()

# Add configurable parameters for session-level tweaking (optional)
st.sidebar.header("Define Your Audience")

# Gender selection
selected_gender = st.sidebar.selectbox(
    label="Select Gender",
    options=["", "male", "female"],
    index=0,
    help="Select a gender or leave it blank."
)

# Tribe selection dropdown

selected_tribe = st.sidebar.selectbox(
    label="Select Tribe",
    options=list(TRIBES.keys()),
    index=0,
    help="Select a tribe or leave it blank."
)

# Age Group Selection
selected_age_group = st.sidebar.selectbox(
    label="Select Age Group",
    options=list(AGE_GROUPS.keys()),  # Display pretty labels
    index=0,
    help="Select an age group or leave it blank."
)

# Country selection
selected_country = st.sidebar.selectbox(
    label="Select Market",
    options=list(COUNTRIES.keys()),  # Display pretty labels
    index=0,
    help="Select a geographic focus."
)

# Platform selection
selected_platform = st.sidebar.selectbox(
    label="Select Platform",
    options=list(PLATFORMS.keys()),
    index=0,
    help="Select a social media platform."
)

# New free-text input
rag_query = st.sidebar.text_input(
    label="RAG Query",
    value="climate change opinions and sentiment reactions to brands and conversations around global warming and sustainability",
    placeholder="Type any additional info here...",
    help="This will help ensure to inform the prompt with the most relevant conversations"
)

# Input box and Send button at the top
with st.form("chat_input_form"):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_message = st.text_input(
            'Enter your message',
            key='user_input',
            value='' if st.session_state.clear_input else None,
        )
    with col2:
        submitted = st.form_submit_button("Send")

# When the user submits a message, call the API
if submitted and user_message:
    # Add user message to chat history
    st.session_state.chat_history.append({"text": user_message, "is_user": True})

    # Update tweaks to include the user input in ChatInput-nM66I
    tweaks = LANGFLOW_TWEAKS.copy()
    tweaks = update_tweaks_with_user_input(
        tweaks,
        chat_input=user_message,
        tribe=TRIBES[selected_tribe],
        age_group=AGE_GROUPS[selected_age_group],
        country=COUNTRIES[selected_country],
        gender=selected_gender,
        platform=PLATFORMS[selected_platform],
        rag_query=rag_query
    )

    # Call the run_flow function and get the response
    response = run_flow(user_message, tweaks=tweaks, config=config)

    # Extract and display only the message part
    extracted_message = extract_message(response)

    # Add AI response to chat history immediately after receiving it
    st.session_state.chat_history.append({"text": extracted_message, "is_user": False})

    # Clear input box after sending by setting clear_input flag
    st.session_state.clear_input = True

# Display chat history below the input box (most recent first)
st.markdown("### Chat History")
for chat in reversed(st.session_state.chat_history):  # Reverse order for most recent first
    if chat['is_user']:
        st.markdown(f"<div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin-bottom: 5px;'>{chat['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin-bottom: 5px;'>{chat['text']}</div>", unsafe_allow_html=True)


# Clear chat history button
if st.button('Clear Chat History'):
    st.session_state.chat_history = []
    st.experimental_rerun()
