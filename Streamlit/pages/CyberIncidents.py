import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# -----------------------------------
# Fix project path (Week 8 app access)
# -----------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DB_PATH = PROJECT_ROOT / "DATA" / "intelligence_platform.db"

from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets

# -----------------------------------
# Page config
# -----------------------------------
st.set_page_config(
    page_title="Cyberincidents",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------------
# Login guard
# -----------------------------------
if not st.session_state.get("logged_in", False):
    st.error("You must be logged in.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

# -----------------------------------
# Header
# -----------------------------------
st.title("📊 Intelligence Platform Dashboard")
st.success(f"Hello, {st.session_state.username}! You are logged in.")
st.caption("Data loaded from your Week 8 SQLite database.")

# -----------------------------------
# Load data
# -----------------------------------
try:
    conn = connect_database(DB_PATH)
    incidents = get_all_incidents(conn)
    datasets = get_all_datasets(conn)
    tickets = get_all_tickets(conn)
    conn.close()
except Exception as e:
    st.error(f"Database error: {e}")
    st.stop()

# -----------------------------------
# Convert to DataFrames (CORRECT)
# -----------------------------------
inc_df = pd.DataFrame(
    incidents,
    columns=["id", "title", "severity", "status", "date"]
)

dat_df = pd.DataFrame(
    datasets,
    columns=["id", "name", "source", "category", "size"]
)

tic_df = pd.DataFrame(
    tickets,
    columns=["id", "title", "priority", "status", "created_date"]
)

# -----------------------------------
# Tabs
# -----------------------------------
tab1, tab2, tab3 = st.tabs(
    ["Cyber Incidents", "Datasets", "IT Tickets"]
)

with tab1:
    st.subheader("Cyber Incidents")
    st.dataframe(inc_df, use_container_width=True)

with tab2:
    st.subheader("Datasets")
    st.dataframe(dat_df, use_container_width=True)

with tab3:
    st.subheader("IT Tickets")
    st.dataframe(tic_df, use_container_width=True)

st.divider()

# -----------------------------------
# DELETE INCIDENT (Week 9 requirement)
# -----------------------------------
st.subheader("🗑 Delete Cyber Incident")

if not inc_df.empty:
    incident_labels = inc_df.apply(
        lambda r: f"{r['id']} – {r['title']}",
        axis=1
    ).tolist()

    selected = st.selectbox(
        "Select incident",
        options=incident_labels
    )

    delete_id = int(selected.split(" – ")[0])
    confirm = st.checkbox("I confirm deletion")

    if st.button("Delete incident"):
        if not confirm:
            st.warning("Please confirm deletion.")
        else:
            try:
                conn = connect_database(DB_PATH)
                conn.execute(
                    "DELETE FROM cyber_incidents WHERE id = ?",
                    (delete_id,)
                )
                conn.commit()
                conn.close()
                st.success("Incident deleted.")
                st.rerun()
            except Exception as e:
                st.error(f"Delete failed: {e}")
else:
    st.info("No incidents available.")
