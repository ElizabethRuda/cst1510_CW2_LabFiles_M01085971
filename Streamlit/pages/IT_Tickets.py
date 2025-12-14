import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# -------------------------------------------------
# Add project root (CST1510_CW2) to Python path
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DB_PATH = PROJECT_ROOT / "DATA" / "intelligence_platform.db"

from app.data.db import connect_database
from app.data.incidents import get_all_incidents

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="IT Tickets", page_icon="📈", layout="wide")

# -------------------------------------------------
# Guard (login required)
# -------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("📈 Analytics")

# -------------------------------------------------
# Load data
# -------------------------------------------------
conn = connect_database(DB_PATH)
incidents = get_all_incidents(conn)
conn.close()

df = pd.DataFrame(
    incidents,
    columns=["id", "title", "severity", "status", "date"]
)

# -------------------------------------------------
# Simple analytics (Week 9 requirement)
# -------------------------------------------------
st.subheader("Incidents by Severity")
severity_counts = df["severity"].value_counts()
st.bar_chart(severity_counts)

st.subheader("Incidents by Status")
status_counts = df["status"].value_counts()
st.bar_chart(status_counts)
