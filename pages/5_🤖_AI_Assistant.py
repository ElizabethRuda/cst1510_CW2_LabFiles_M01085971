"""
AI Assistant page for Multi-Domain Intelligence Platform
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from multi_domain_platform.services.ai_assistant import AIAssistant

st.set_page_config(
    page_title="AI Assistant - Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Assistant")
st.markdown("### AI-Powered Intelligence Assistant")

# Check authentication
if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please log in to access this page.")
    st.stop()

# Initialize AI Assistant
ai_assistant = AIAssistant()

# Check availability
if not ai_assistant.is_available():
    st.warning("⚠️ AI Assistant is not available. Please configure OPENAI_API_KEY in secrets.toml or environment variables.")
    st.info("💡 To enable AI Assistant, add your OpenAI API key to `.streamlit/secrets.toml` file.")
    st.code("""
[secrets]
OPENAI_API_KEY = "your-api-key-here"
    """)
    st.stop()

# Chat interface
st.subheader("Chat with AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about the platform..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ai_assistant.generate_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

