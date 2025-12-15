"""
AI Assistant page for Multi-Domain Intelligence Platform
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from multi_domain_platform.services.ai_assistant import AIAssistant
from multi_domain_platform.services.database_manager import DatabaseManager

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

# Initialize database manager and AI Assistant
db_manager = DatabaseManager()
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

# Load data from database for context
try:
    incidents = db_manager.execute_query("SELECT * FROM cyber_incidents")
    datasets = db_manager.execute_query("SELECT * FROM datasets_metadata")
    tickets = db_manager.execute_query("SELECT * FROM it_tickets")
    
    # Build context with detailed information
    context_parts = []
    
    # Cybersecurity incidents context
    if incidents:
        context_parts.append(f"Cybersecurity Incidents: Total {len(incidents)} incidents.")
        severity_counts = {}
        status_counts = {}
        for inc in incidents:
            severity_counts[inc.get('severity', 'Unknown')] = severity_counts.get(inc.get('severity', 'Unknown'), 0) + 1
            status_counts[inc.get('status', 'Unknown')] = status_counts.get(inc.get('status', 'Unknown'), 0) + 1
        if severity_counts:
            context_parts.append(f"Severity breakdown: {', '.join([f'{k}: {v}' for k, v in severity_counts.items()])}")
        if status_counts:
            context_parts.append(f"Status breakdown: {', '.join([f'{k}: {v}' for k, v in status_counts.items()])}")
    else:
        context_parts.append("Cybersecurity Incidents: No incidents recorded.")
    
    # Datasets context
    if datasets:
        total_size = sum(d.get('size', 0) for d in datasets)
        context_parts.append(f"Datasets: Total {len(datasets)} datasets, total size {total_size / (1024*1024*1024):.2f} GB.")
        categories = {}
        for ds in datasets:
            cat = ds.get('category', 'Uncategorized')
            categories[cat] = categories.get(cat, 0) + 1
        if categories:
            context_parts.append(f"Categories: {', '.join([f'{k}: {v}' for k, v in categories.items()])}")
    else:
        context_parts.append("Datasets: No datasets recorded.")
    
    # IT Tickets context
    if tickets:
        context_parts.append(f"IT Tickets: Total {len(tickets)} tickets.")
        priority_counts = {}
        status_counts = {}
        for tic in tickets:
            priority_counts[tic.get('priority', 'Unknown')] = priority_counts.get(tic.get('priority', 'Unknown'), 0) + 1
            status_counts[tic.get('status', 'Unknown')] = status_counts.get(tic.get('status', 'Unknown'), 0) + 1
        if priority_counts:
            context_parts.append(f"Priority breakdown: {', '.join([f'{k}: {v}' for k, v in priority_counts.items()])}")
        if status_counts:
            context_parts.append(f"Status breakdown: {', '.join([f'{k}: {v}' for k, v in status_counts.items()])}")
    else:
        context_parts.append("IT Tickets: No tickets recorded.")
    
    platform_context = " ".join(context_parts)
    
except Exception as e:
    platform_context = f"Database error: {str(e)}"

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
    
    # Get AI response with platform context
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ai_assistant.generate_response(prompt, platform_context)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()


