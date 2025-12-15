"""
Data Science page for Multi-Domain Intelligence Platform
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
    page_title="Data Science - Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Science")
st.markdown("### Dataset Management and Analytics")

# Check authentication
if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please log in to access this page.")
    st.stop()

# Initialize database manager
db_manager = DatabaseManager()

# Fetch datasets
datasets = db_manager.execute_query("SELECT * FROM datasets_metadata ORDER BY id DESC")

# Display datasets
if datasets:
    df = pd.DataFrame(datasets)
    
    # Format size column
    if 'size' in df.columns:
        df['size_display'] = df['size'].apply(lambda x: f"{x / (1024*1024):.2f} MB" if x > 0 else "0 B")
    
    st.dataframe(df, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Datasets", len(datasets))
    with col2:
        total_size = sum(d['size'] for d in datasets)
        st.metric("Total Size", f"{total_size / (1024*1024*1024):.2f} GB" if total_size > 0 else "0 B")
    with col3:
        categories = len(set(d['category'] for d in datasets if d['category']))
        st.metric("Categories", categories)
else:
    st.info("No datasets found. Add datasets using the form below.")

# Add new dataset
st.markdown("---")
st.subheader("Add New Dataset")

with st.form("add_dataset"):
    name = st.text_input("Dataset Name", key="dataset_name")
    source = st.text_input("Source", key="dataset_source")
    category = st.text_input("Category", key="dataset_category")
    size = st.number_input("Size (bytes)", min_value=0, value=0, key="dataset_size")
    
    submitted = st.form_submit_button("Add Dataset", type="primary")
    if submitted:
        if name:
            db_manager.execute_update(
                "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
                (name, source, category, size)
            )
            st.success("✅ Dataset added successfully!")
            st.rerun()
        else:
            st.error("Dataset name is required")

