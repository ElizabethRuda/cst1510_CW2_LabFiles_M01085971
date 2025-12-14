import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# --------------------------------------------------
# Load .env from Streamlit folder
# --------------------------------------------------
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)
api_key = os.getenv("OPENAI_API_KEY")

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Security Assistant",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Check API key
# --------------------------------------------------
st.write("API key loaded:", bool(api_key))
if not api_key:
    st.error("OPENAI_API_KEY not found. Add it to Streamlit/.env")
    st.stop()

client = OpenAI(api_key=api_key)

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("🤖 AI Security Assistant")
st.caption("Powered by OpenAI API")
st.write("Ask a question about cyber incidents, IT tickets, or data analysis:")


            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        full_response += delta.content
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

