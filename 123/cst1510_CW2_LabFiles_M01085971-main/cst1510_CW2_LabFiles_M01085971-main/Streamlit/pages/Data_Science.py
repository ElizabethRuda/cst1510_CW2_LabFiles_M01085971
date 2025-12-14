import sys
from pathlib import Path
import streamlit as st

# -------------------------------------------------
# Add project root (CST1510_CW2) to Python path
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(page_title="Data Science", page_icon="📊", layout="centered")

# -------------------------------------------------
# Guard (login required)
# -------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in.")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚙️ Settings")
st.info(f"Logged in as: **{st.session_state.username}**")

st.divider()

# -------------------------------------------------
# Logout
# -------------------------------------------------
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out.")
    st.switch_page("Home.py")
