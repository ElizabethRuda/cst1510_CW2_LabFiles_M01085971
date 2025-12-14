import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DB_PATH = PROJECT_ROOT / "DATA" / "intelligence_platform.db"

# Import database functions
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets

# Page configuration
st.set_page_config(
    page_title="Dashboard - Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Login guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to access the dashboard.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 Intelligence Platform Dashboard</div>', unsafe_allow_html=True)
st.success(f"👋 Welcome, **{st.session_state.username}**! You are logged in.")
st.caption("📈 Data loaded from your Week 8 SQLite database")

# Load data
try:
    conn = connect_database(DB_PATH)
    incidents = get_all_incidents(conn)
    datasets = get_all_datasets(conn)
    tickets = get_all_tickets(conn)
    conn.close()
except Exception as e:
    st.error(f"❌ Database error: {e}")
    st.info("💡 Make sure the database exists and contains data.")
    st.stop()

# Convert to DataFrames
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

# Key Metrics
st.markdown("---")
st.subheader("🎯 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Incidents", len(inc_df))

with col2:
    open_incidents = len(inc_df[inc_df['status'].isin(['open', 'in_progress'])])
    st.metric("Active Incidents", open_incidents)

with col3:
    critical_incidents = len(inc_df[inc_df['severity'] == 'Critical'])
    st.metric("Critical", critical_incidents, delta=None)

with col4:
    st.metric("Datasets", len(dat_df))

with col5:
    open_tickets = len(tic_df[tic_df['status'].isin(['open', 'in_progress'])])
    st.metric("Open Tickets", open_tickets)

st.markdown("---")

# Main content with tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["🛡️ Cyber Incidents", "📚 Datasets", "🎫 IT Tickets", "📈 Analytics"]
)

# -------------------------
# TAB 1: CYBER INCIDENTS
# -------------------------
with tab1:
    st.subheader("🛡️ Cyber Incidents Analysis")
    
    if not inc_df.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            severities = inc_df['severity'].unique().tolist()
            selected_severity = st.multiselect(
                "Filter by Severity",
                severities,
                default=severities
            )
        
        with col2:
            statuses = inc_df['status'].unique().tolist()
            selected_status = st.multiselect(
                "Filter by Status",
                statuses,
                default=statuses
            )
        
        with col3:
            if 'date' in inc_df.columns and inc_df['date'].notna().any():
                inc_df['date'] = pd.to_datetime(inc_df['date'], errors='coerce')
                date_range = st.date_input(
                    "Date Range",
                    value=(inc_df['date'].min(), inc_df['date'].max()),
                    min_value=inc_df['date'].min(),
                    max_value=inc_df['date'].max()
                )
        
        # Filter data
        filtered_inc = inc_df[
            (inc_df['severity'].isin(selected_severity)) &
            (inc_df['status'].isin(selected_status))
        ]
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Incidents by Severity**")
            severity_counts = filtered_inc['severity'].value_counts()
            fig = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            st.plotly_chart(fig, use_container_width=True, key="incidents_severity_pie")
        
        with col2:
            st.markdown("**Incidents by Status**")
            status_counts = filtered_inc['status'].value_counts()
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                labels={'x': 'Status', 'y': 'Count'},
                color=status_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="incidents_status_bar")
        
        # Timeline
        if 'date' in filtered_inc.columns and filtered_inc['date'].notna().any():
            st.markdown("**📅 Incidents Timeline**")
            timeline_df = filtered_inc.groupby(filtered_inc['date'].dt.to_period('M')).size().reset_index(name='count')
            timeline_df['date'] = timeline_df['date'].astype(str)
            fig = px.line(
                timeline_df,
                x='date',
                y='count',
                markers=True,
                labels={'date': 'Month', 'count': 'Number of Incidents'},
                title="Incidents Over Time"
            )
            st.plotly_chart(fig, use_container_width=True, key="incidents_timeline")
        
        # Data table
        st.markdown("**📋 Incident Details**")
        st.dataframe(
            filtered_inc[['id', 'title', 'severity', 'status', 'date']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No incidents data available.")

# -------------------------
# TAB 2: DATASETS
# -------------------------
with tab2:
    st.subheader("📚 Datasets Metadata")
    
    if not dat_df.empty:
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Datasets", len(dat_df))
        with col2:
            total_size = dat_df['size'].sum() if 'size' in dat_df.columns else 0
            st.metric("Total Size", f"{total_size:,} MB" if total_size else "N/A")
        with col3:
            avg_size = dat_df['size'].mean() if 'size' in dat_df.columns else 0
            st.metric("Avg Size", f"{avg_size:.0f} MB" if avg_size else "N/A")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Datasets by Category**")
            if 'category' in dat_df.columns:
                category_counts = dat_df['category'].value_counts()
                fig = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    color_discrete_sequence=px.colors.sequential.Greens_r
                )
                st.plotly_chart(fig, use_container_width=True, key="datasets_category_pie")
        
        with col2:
            st.markdown("**Datasets by Source**")
            if 'source' in dat_df.columns:
                source_counts = dat_df['source'].value_counts()
                fig = px.bar(
                    x=source_counts.index,
                    y=source_counts.values,
                    labels={'x': 'Source', 'y': 'Count'},
                    color=source_counts.values,
                    color_continuous_scale='Purples'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True, key="datasets_source_bar")
        
        # Size distribution
        if 'size' in dat_df.columns and dat_df['size'].notna().any():
            st.markdown("**📊 Size Distribution**")
            fig = px.histogram(
                dat_df,
                x='size',
                nbins=20,
                labels={'size': 'Size (MB)', 'count': 'Number of Datasets'},
                    title="Dataset Size Distribution"
            )
            st.plotly_chart(fig, use_container_width=True, key="datasets_size_hist")
        
        # Data table
        st.markdown("**📋 Dataset Details**")
        st.dataframe(dat_df, use_container_width=True, hide_index=True)
    else:
        st.info("No datasets data available.")

# -------------------------
# TAB 3: IT TICKETS
# -------------------------
with tab3:
    st.subheader("🎫 IT Tickets")
    
    if not tic_df.empty:
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            priorities = tic_df['priority'].unique().tolist()
            selected_priority = st.multiselect(
                "Filter by Priority",
                priorities,
                default=priorities
            )
        
        with col2:
            statuses = tic_df['status'].unique().tolist()
            selected_status = st.multiselect(
                "Filter by Status",
                statuses,
                default=statuses
            )
        
        # Filter data
        filtered_tic = tic_df[
            (tic_df['priority'].isin(selected_priority)) &
            (tic_df['status'].isin(selected_status))
        ]
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Tickets by Status**")
            status_counts = filtered_tic['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            st.plotly_chart(fig, use_container_width=True, key="tickets_status_pie")
        
        with col2:
            st.markdown("**Tickets by Priority**")
            priority_counts = filtered_tic['priority'].value_counts()
            fig = px.bar(
                x=priority_counts.index,
                y=priority_counts.values,
                labels={'x': 'Priority', 'y': 'Count'},
                color=priority_counts.values,
                    color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="tickets_priority_bar")
        
        # Data table
        st.markdown("**📋 Ticket Details**")
        st.dataframe(filtered_tic, use_container_width=True, hide_index=True)
    else:
        st.info("No tickets data available.")

# -------------------------
# TAB 4: ANALYTICS
# -------------------------
with tab4:
    st.subheader("📈 Comprehensive Analytics")
    
    # Overall statistics
    st.markdown("**📊 Overall Statistics**")
    
    stats_data = {
        'Module': ['Cyber Incidents', 'Datasets', 'IT Tickets'],
        'Total Records': [len(inc_df), len(dat_df), len(tic_df)],
        'Active/Open': [
            len(inc_df[inc_df['status'].isin(['open', 'in_progress'])]),
            len(dat_df),
            len(tic_df[tic_df['status'].isin(['open', 'in_progress'])])
        ]
    }
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    # Comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Incident Severity Distribution**")
        if not inc_df.empty:
            severity_counts = inc_df['severity'].value_counts()
            fig = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                labels={'x': 'Severity', 'y': 'Count'},
                color=severity_counts.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="analytics_incidents_severity")
    
    with col2:
        st.markdown("**Ticket Priority Distribution**")
        if not tic_df.empty:
            priority_counts = tic_df['priority'].value_counts()
            fig = px.bar(
                x=priority_counts.index,
                y=priority_counts.values,
                labels={'x': 'Priority', 'y': 'Count'},
                color=priority_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="analytics_tickets_priority")

# Sidebar
with st.sidebar:
    st.markdown("### 🔧 Navigation")
    st.markdown("---")
    
    # Theme switcher
    st.markdown("### 🎨 Theme")
    if st.button("🌙 Switch to Dark Mode"):
        st.session_state.theme = "dark"
        st.switch_page("pages/Dashboard_Dark.py")
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 👤 User Info")
    st.info(f"Logged in as: **{st.session_state.username}**")
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully!")
        st.switch_page("Home.py")

