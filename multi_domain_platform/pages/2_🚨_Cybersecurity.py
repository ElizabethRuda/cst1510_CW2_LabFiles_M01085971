"""
Cybersecurity page for Multi-Domain Intelligence Platform
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from multi_domain_platform.services.database_manager import DatabaseManager

st.set_page_config(
    page_title="Cybersecurity - Intelligence Platform",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Cybersecurity")
st.markdown("### Security Incident Management")

# Check authentication
if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please log in to access this page.")
    st.stop()

# Initialize database manager
db_manager = DatabaseManager()

# Fetch incidents
incidents = db_manager.execute_query("SELECT * FROM cyber_incidents ORDER BY id DESC")

# Display incidents
if incidents:
    df = pd.DataFrame(incidents)
    st.dataframe(df, use_container_width=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", len(incidents))
    with col2:
        critical = len([i for i in incidents if i['severity'] == 'Critical'])
        st.metric("Critical", critical)
    with col3:
        open_count = len([i for i in incidents if i['status'] == 'open'])
        st.metric("Open", open_count)
    with col4:
        resolved = len([i for i in incidents if i['status'] == 'resolved'])
        st.metric("Resolved", resolved)
else:
    st.info("No security incidents found. Add incidents using the form below.")

# Add new incident
st.markdown("---")
st.subheader("Add New Security Incident")

with st.form("add_incident"):
    title = st.text_input("Title", key="incident_title")
    severity = st.selectbox("Severity", ["Critical", "High", "Medium", "Low"], key="incident_severity")
    status = st.selectbox("Status", ["open", "in_progress", "resolved"], key="incident_status")
    date = st.date_input("Date", key="incident_date")
    
    submitted = st.form_submit_button("Add Incident", type="primary")
    if submitted:
        if title:
            db_manager.execute_update(
                "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
                (title, severity, status, str(date))
            )
            st.success("✅ Incident added successfully!")
            st.rerun()
        else:
            st.error("Title is required")

