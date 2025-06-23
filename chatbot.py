import os
import streamlit as st
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models.model import Model

load_dotenv()

# Load IBM credentials
api_key = os.getenv("IBM_GRANITE_API_KEY")
project_id = os.getenv("IBM_GRANITE_PROJECT_ID")
base_url = os.getenv("IBM_GRANITE_URL")  # should be for text generation
model_id = os.getenv("MODEL_ID")  # e.g., granite-3b-instruct


def run_chatbot():
    st.title("🤖 Smart City Chatbot (IBM Granite)")

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous chat
    for i in range(0, len(st.session_state.chat_history), 2):
        with st.chat_message("user"):
            st.write(st.session_state.chat_history[i])
        if i + 1 < len(st.session_state.chat_history):
            with st.chat_message("assistant"):
                st.markdown(st.session_state.chat_history[i + 1])

    # Chat input
    user_input = st.chat_input("Type your question here...")

    if user_input:
        st.session_state.chat_history.append(user_input)
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Initialize model
                    model = Model(
                        model_id=model_id,
                        credentials={"apikey": api_key, "url": base_url},
                        project_id=project_id,
                    )

                    prompt = f"""You are a helpful smart city assistant focused on sustainability and policy advice.
Provide responses as bullet points where helpful, using a friendly tone.

Input: {user_input}
Response:"""

                    response = model.generate_text(
                        prompt=prompt,
                        params={
                            "max_new_tokens": 512,
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "decoding_method": "sample",
                            "stop_sequences": ["<|endoftext|>", "User:"],
                        },
                    )

                    output = (
                        response["generated_text"]
                        if isinstance(response, dict) and "generated_text" in response
                        else str(response)
                    )

                    st.markdown(output)
                    st.session_state.chat_history.append(output)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.chat_history.append(
                        "Sorry, I encountered an issue."
                    )
