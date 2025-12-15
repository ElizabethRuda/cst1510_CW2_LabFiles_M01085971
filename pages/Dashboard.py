"""
Dashboard page for Multi-Domain Intelligence Platform
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from multi_domain_platform.services.database_manager import DatabaseManager
from multi_domain_platform.services.ai_assistant import AIAssistant

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

# Initialize database manager
db_manager = DatabaseManager()

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
st.caption("📈 Data loaded from Multi-Domain Intelligence Platform database")

# Load data
try:
    incidents = db_manager.execute_query("SELECT * FROM cyber_incidents")
    datasets = db_manager.execute_query("SELECT * FROM datasets_metadata")
    tickets = db_manager.execute_query("SELECT * FROM it_tickets")
except Exception as e:
    st.error(f"❌ Database error: {e}")
    st.info("💡 Make sure the database exists and contains data.")
    st.stop()

# Convert to DataFrames
inc_df = pd.DataFrame(incidents) if incidents else pd.DataFrame(columns=["id", "title", "severity", "status", "date"])
dat_df = pd.DataFrame(datasets) if datasets else pd.DataFrame(columns=["id", "name", "source", "category", "size"])
tic_df = pd.DataFrame(tickets) if tickets else pd.DataFrame(columns=["id", "title", "priority", "status", "created_date"])

# Key Metrics
st.markdown("---")
st.subheader("🎯 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Incidents", len(inc_df))

with col2:
    if not inc_df.empty and 'status' in inc_df.columns:
        open_incidents = len(inc_df[inc_df['status'].isin(['open', 'in_progress'])])
        st.metric("Active Incidents", open_incidents)
    else:
        st.metric("Active Incidents", 0)

with col3:
    if not inc_df.empty and 'severity' in inc_df.columns:
        critical_incidents = len(inc_df[inc_df['severity'] == 'Critical'])
        st.metric("Critical", critical_incidents, delta=None)
    else:
        st.metric("Critical", 0)

with col4:
    st.metric("Datasets", len(dat_df))

with col5:
    if not tic_df.empty and 'status' in tic_df.columns:
        open_tickets = len(tic_df[tic_df['status'].isin(['open', 'in_progress'])])
        st.metric("Open Tickets", open_tickets)
    else:
        st.metric("Open Tickets", 0)

st.markdown("---")

# Main content with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🛡️ Cyber Incidents", "📚 Datasets", "🎫 IT Tickets", "📈 Analytics", "🤖 AI Assistant"]
)

# -------------------------
# TAB 1: CYBER INCIDENTS
# -------------------------
with tab1:
    st.subheader("🛡️ Cyber Incidents Analysis")
    
    if not inc_df.empty and len(inc_df) > 0:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'severity' in inc_df.columns:
                severities = inc_df['severity'].unique().tolist()
                selected_severity = st.multiselect(
                    "Filter by Severity",
                    severities,
                    default=severities
                )
            else:
                selected_severity = []
        
        with col2:
            if 'status' in inc_df.columns:
                statuses = inc_df['status'].unique().tolist()
                selected_status = st.multiselect(
                    "Filter by Status",
                    statuses,
                    default=statuses
                )
            else:
                selected_status = []
        
        with col3:
            date_range = None
            if 'date' in inc_df.columns and inc_df['date'].notna().any():
                try:
                    inc_df['date'] = pd.to_datetime(inc_df['date'], errors='coerce')
                    if inc_df['date'].notna().any():
                        date_range = st.date_input(
                            "Date Range",
                            value=(inc_df['date'].min(), inc_df['date'].max()),
                            min_value=inc_df['date'].min(),
                            max_value=inc_df['date'].max()
                        )
                except Exception:
                    pass
        
        # Filter data
        filtered_inc = inc_df.copy()
        if 'severity' in inc_df.columns and selected_severity:
            filtered_inc = filtered_inc[filtered_inc['severity'].isin(selected_severity)]
        if 'status' in inc_df.columns and selected_status:
            filtered_inc = filtered_inc[filtered_inc['status'].isin(selected_status)]
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'severity' in filtered_inc.columns:
                st.markdown("**Incidents by Severity**")
                severity_counts = filtered_inc['severity'].value_counts()
                if len(severity_counts) > 0:
                    fig = px.pie(
                        values=severity_counts.values,
                        names=severity_counts.index,
                        color_discrete_sequence=px.colors.sequential.Reds_r
                    )
                    st.plotly_chart(fig, use_container_width=True, key="incidents_severity_pie")
        
        with col2:
            if 'status' in filtered_inc.columns:
                st.markdown("**Incidents by Status**")
                status_counts = filtered_inc['status'].value_counts()
                if len(status_counts) > 0:
                    fig = px.bar(
                        x=status_counts.index,
                        y=status_counts.values,
                        labels={'x': 'Status', 'y': 'Count'},
                        color=status_counts.values,
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True, key="incidents_status_bar")
        
        # Data table
        st.markdown("**📋 Incident Details**")
        display_cols = [col for col in ['id', 'title', 'severity', 'status', 'date'] if col in filtered_inc.columns]
        st.dataframe(
            filtered_inc[display_cols],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No incidents data available. Add incidents from the Cybersecurity page.")

# -------------------------
# TAB 2: DATASETS
# -------------------------
with tab2:
    st.subheader("📚 Datasets Metadata")
    
    if not dat_df.empty and len(dat_df) > 0:
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Datasets", len(dat_df))
        with col2:
            if 'size' in dat_df.columns:
                total_size = dat_df['size'].sum()
                size_gb = total_size / (1024 * 1024 * 1024)
                st.metric("Total Size", f"{size_gb:.2f} GB" if size_gb > 0 else "0 B")
            else:
                st.metric("Total Size", "N/A")
        with col3:
            if 'size' in dat_df.columns and dat_df['size'].notna().any():
                avg_size = dat_df['size'].mean()
                avg_mb = avg_size / (1024 * 1024)
                st.metric("Avg Size", f"{avg_mb:.0f} MB" if avg_size > 0 else "0 B")
            else:
                st.metric("Avg Size", "N/A")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'category' in dat_df.columns and dat_df['category'].notna().any():
                st.markdown("**Datasets by Category**")
                category_counts = dat_df['category'].value_counts()
                if len(category_counts) > 0:
                    fig = px.pie(
                        values=category_counts.values,
                        names=category_counts.index,
                        color_discrete_sequence=px.colors.sequential.Greens_r
                    )
                    st.plotly_chart(fig, use_container_width=True, key="datasets_category_pie")
        
        with col2:
            if 'source' in dat_df.columns and dat_df['source'].notna().any():
                st.markdown("**Datasets by Source**")
                source_counts = dat_df['source'].value_counts()
                if len(source_counts) > 0:
                    fig = px.bar(
                        x=source_counts.index,
                        y=source_counts.values,
                        labels={'x': 'Source', 'y': 'Count'},
                        color=source_counts.values,
                        color_continuous_scale='Purples'
                    )
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True, key="datasets_source_bar")
        
        # Data table
        st.markdown("**📋 Dataset Details**")
        st.dataframe(dat_df, use_container_width=True, hide_index=True)
    else:
        st.info("No datasets data available. Add datasets from the Data Science page.")

# -------------------------
# TAB 3: IT TICKETS
# -------------------------
with tab3:
    st.subheader("🎫 IT Tickets")
    
    if not tic_df.empty and len(tic_df) > 0:
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            if 'priority' in tic_df.columns:
                priorities = tic_df['priority'].unique().tolist()
                selected_priority = st.multiselect(
                    "Filter by Priority",
                    priorities,
                    default=priorities
                )
            else:
                selected_priority = []
        
        with col2:
            if 'status' in tic_df.columns:
                statuses = tic_df['status'].unique().tolist()
                selected_status = st.multiselect(
                    "Filter by Status",
                    statuses,
                    default=statuses
                )
            else:
                selected_status = []
        
        # Filter data
        filtered_tic = tic_df.copy()
        if 'priority' in tic_df.columns and selected_priority:
            filtered_tic = filtered_tic[filtered_tic['priority'].isin(selected_priority)]
        if 'status' in tic_df.columns and selected_status:
            filtered_tic = filtered_tic[filtered_tic['status'].isin(selected_status)]
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'status' in filtered_tic.columns:
                st.markdown("**Tickets by Status**")
                status_counts = filtered_tic['status'].value_counts()
                if len(status_counts) > 0:
                    fig = px.pie(
                        values=status_counts.values,
                        names=status_counts.index,
                        color_discrete_sequence=px.colors.sequential.Oranges_r
                    )
                    st.plotly_chart(fig, use_container_width=True, key="tickets_status_pie")
        
        with col2:
            if 'priority' in filtered_tic.columns:
                st.markdown("**Tickets by Priority**")
                priority_counts = filtered_tic['priority'].value_counts()
                if len(priority_counts) > 0:
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
        st.info("No tickets data available. Add tickets from the IT Operations page.")

# -------------------------
# TAB 4: ANALYTICS
# -------------------------
with tab4:
    st.subheader("📈 Comprehensive Analytics")
    
    # Overall statistics
    st.markdown("**📊 Overall Statistics**")
    
    active_incidents = len(inc_df[inc_df['status'].isin(['open', 'in_progress'])]) if not inc_df.empty and 'status' in inc_df.columns else 0
    active_tickets = len(tic_df[tic_df['status'].isin(['open', 'in_progress'])]) if not tic_df.empty and 'status' in tic_df.columns else 0
    
    stats_data = {
        'Module': ['Cyber Incidents', 'Datasets', 'IT Tickets'],
        'Total Records': [len(inc_df), len(dat_df), len(tic_df)],
        'Active/Open': [active_incidents, len(dat_df), active_tickets]
    }
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    # Comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Incident Severity Distribution**")
        if not inc_df.empty and 'severity' in inc_df.columns:
            severity_counts = inc_df['severity'].value_counts()
            if len(severity_counts) > 0:
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
        if not tic_df.empty and 'priority' in tic_df.columns:
            priority_counts = tic_df['priority'].value_counts()
            if len(priority_counts) > 0:
                fig = px.bar(
                    x=priority_counts.index,
                    y=priority_counts.values,
                    labels={'x': 'Priority', 'y': 'Count'},
                    color=priority_counts.values,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True, key="analytics_tickets_priority")

# -------------------------
# TAB 5: AI ASSISTANT
# -------------------------
with tab5:
    st.subheader("🤖 AI Assistant")
    
    ai_assistant = AIAssistant()
    
    if not ai_assistant.is_available():
        st.warning("⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY in secrets.toml.")
        st.info("💡 Add your API key to `.streamlit/secrets.toml` or `secrets.toml` file.")
    else:
        st.success("✅ AI Assistant is ready!")
        
        # Chat interface
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = []
        
        # Display chat history
        for msg in st.session_state.ai_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Chat input
        user_input = st.chat_input("Ask me anything about cybersecurity, IT operations, or data science...")
        
        if user_input:
            # Add user message
            st.session_state.ai_messages.append({"role": "user", "content": user_input})
            
            # Build detailed context from loaded data
            context_parts = []
            
            # Cybersecurity incidents context
            if not inc_df.empty and len(inc_df) > 0:
                context_parts.append(
                    f"Cybersecurity Incidents: Total {len(inc_df)} incidents."
                )
                if 'severity' in inc_df.columns:
                    severity_counts = inc_df['severity'].value_counts().to_dict()
                    if severity_counts:
                        context_parts.append(
                            f"Severity breakdown: "
                            f"{', '.join([f'{k}: {v}' for k, v in severity_counts.items()])}"
                        )
                if 'status' in inc_df.columns:
                    status_counts = inc_df['status'].value_counts().to_dict()
                    if status_counts:
                        context_parts.append(
                            f"Status breakdown: "
                            f"{', '.join([f'{k}: {v}' for k, v in status_counts.items()])}"
                        )
            else:
                context_parts.append(
                    "Cybersecurity Incidents: No incidents recorded."
                )
            
            # Datasets context
            if not dat_df.empty and len(dat_df) > 0:
                total_size = dat_df['size'].sum() if 'size' in dat_df.columns else 0
                size_gb = total_size / (1024 * 1024 * 1024)
                context_parts.append(
                    f"Datasets: Total {len(dat_df)} datasets, "
                    f"total size {size_gb:.2f} GB."
                )
                if 'category' in dat_df.columns:
                    categories = dat_df['category'].value_counts().to_dict()
                    if categories:
                        context_parts.append(
                            f"Categories: "
                            f"{', '.join([f'{k}: {v}' for k, v in categories.items()])}"
                        )
            else:
                context_parts.append("Datasets: No datasets recorded.")
            
            # IT Tickets context
            if not tic_df.empty and len(tic_df) > 0:
                context_parts.append(f"IT Tickets: Total {len(tic_df)} tickets.")
                if 'priority' in tic_df.columns:
                    priority_counts = tic_df['priority'].value_counts().to_dict()
                    if priority_counts:
                        context_parts.append(
                            f"Priority breakdown: "
                            f"{', '.join([f'{k}: {v}' for k, v in priority_counts.items()])}"
                        )
                if 'status' in tic_df.columns:
                    status_counts = tic_df['status'].value_counts().to_dict()
                    if status_counts:
                        context_parts.append(
                            f"Status breakdown: "
                            f"{', '.join([f'{k}: {v}' for k, v in status_counts.items()])}"
                        )
            else:
                context_parts.append("IT Tickets: No tickets recorded.")
            
            platform_context = " ".join(context_parts)
            
            # Get AI response with detailed context
            with st.spinner("Thinking..."):
                response = ai_assistant.generate_response(
                    user_input, platform_context
                )
            
            # Add AI response
            st.session_state.ai_messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 🔧 Navigation")
    st.markdown("---")
    
    st.markdown("### 📄 Pages")
    if st.button("🔑 Login Page"):
        st.switch_page("pages/1_🔑_Login.py")
    if st.button("🚨 Cybersecurity"):
        st.switch_page("pages/2_🚨_Cybersecurity.py")
    if st.button("📊 Data Science"):
        st.switch_page("pages/3_📊_Data_Science.py")
    if st.button("💻 IT Operations"):
        st.switch_page("pages/4_💻_IT_Operations.py")
    if st.button("🤖 AI Assistant"):
        st.switch_page("pages/5_🤖_AI_Assistant.py")
    
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
