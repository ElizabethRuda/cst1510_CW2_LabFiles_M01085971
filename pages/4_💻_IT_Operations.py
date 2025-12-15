"""
IT Operations page for Multi-Domain Intelligence Platform
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from multi_domain_platform.services.database_manager import DatabaseManager

st.set_page_config(
    page_title="IT Operations - Intelligence Platform",
    page_icon="💻",
    layout="wide"
)

st.title("💻 IT Operations")
st.markdown("### IT Support Ticket Management")

# Check authentication
if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please log in to access this page.")
    st.stop()

# Initialize database manager
db_manager = DatabaseManager()

# Fetch tickets
tickets = db_manager.execute_query("SELECT * FROM it_tickets ORDER BY id DESC")

# Display tickets
if tickets:
    df = pd.DataFrame(tickets)
    st.dataframe(df, use_container_width=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets", len(tickets))
    with col2:
        critical = len([t for t in tickets if t['priority'] == 'critical'])
        st.metric("Critical", critical)
    with col3:
        open_count = len([t for t in tickets if t['status'] == 'open'])
        st.metric("Open", open_count)
    with col4:
        resolved = len([t for t in tickets if t['status'] == 'resolved'])
        st.metric("Resolved", resolved)
else:
    st.info("No IT tickets found. Add tickets using the form below.")

# Add new ticket
st.markdown("---")
st.subheader("Create New IT Ticket")

with st.form("add_ticket"):
    title = st.text_input("Title", key="ticket_title")
    priority = st.selectbox("Priority", ["critical", "high", "medium", "low"], key="ticket_priority")
    status = st.selectbox("Status", ["open", "in_progress", "resolved", "closed"], key="ticket_status")
    created_date = st.date_input("Created Date", key="ticket_date")
    
    submitted = st.form_submit_button("Create Ticket", type="primary")
    if submitted:
        if title:
            db_manager.execute_update(
                "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
                (title, priority, status, str(created_date))
            )
            st.success("✅ Ticket created successfully!")
            st.rerun()
        else:
            st.error("Title is required")

