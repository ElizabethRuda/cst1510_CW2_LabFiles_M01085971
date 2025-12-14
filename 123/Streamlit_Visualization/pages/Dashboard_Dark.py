import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    page_title="🚀 Intelligence Platform - Dark Mode",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS with cosmic design
st.markdown("""
    <style>
    /* Dark cosmic theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #2d1b4e 100%);
        color: #e0e0e0;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00ff88, #7b2cbf, #ff006e, #8338ec);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        text-shadow: 0 0 30px rgba(123, 44, 191, 0.5);
    }
    
    .cosmic-card {
        background: linear-gradient(135deg, rgba(123, 44, 191, 0.2), rgba(0, 255, 136, 0.1));
        border: 1px solid rgba(123, 44, 191, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(123, 44, 191, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .metric-glow {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(123, 44, 191, 0.15));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    
    .wing-icon {
        font-size: 2rem;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a3e;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #7b2cbf, #00ff88);
        border-radius: 5px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(26, 26, 62, 0.5);
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #7b2cbf, #00ff88);
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Login guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to access the dashboard.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Header with cosmic design
st.markdown("""
    <div class="main-header">
        <span class="wing-icon">🛸</span> Intelligence Platform 
        <span class="wing-icon">🚀</span><br>
        <span style="font-size: 1.5rem; color: #00ff88;">Cosmic Operations Center</span>
    </div>
""", unsafe_allow_html=True)

st.success(f"👋 Welcome, **{st.session_state.username}**! You are logged in.")
st.caption("🌌 Data loaded from your Week 8 SQLite database | Dark Mode Active")

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

# Key Metrics with cosmic design
st.markdown("---")
st.subheader("🌌 Mission Status Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<div class="metric-glow">', unsafe_allow_html=True)
    st.metric("🛡️ Total Incidents", len(inc_df), delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-glow">', unsafe_allow_html=True)
    open_incidents = len(inc_df[inc_df['status'].isin(['open', 'in_progress'])])
    st.metric("⚡ Active Threats", open_incidents)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-glow">', unsafe_allow_html=True)
    critical_incidents = len(inc_df[inc_df['severity'] == 'Critical'])
    st.metric("🔴 Critical", critical_incidents, delta=None)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-glow">', unsafe_allow_html=True)
    st.metric("📊 Datasets", len(dat_df))
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="metric-glow">', unsafe_allow_html=True)
    open_tickets = len(tic_df[tic_df['status'].isin(['open', 'in_progress'])])
    st.metric("🎫 Open Tickets", open_tickets)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Main content with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🛡️ Cyber Operations", "📚 Data Archives", "🎫 Support Tickets", "📈 Analytics", "🌌 About"]
)

# Custom color scheme for dark theme
cosmic_colors = {
    'primary': ['#00ff88', '#7b2cbf', '#ff006e', '#8338ec', '#3a86ff'],
    'gradient': ['#0a0e27', '#1a1a3e', '#2d1b4e'],
    'accent': '#00ff88'
}

# -------------------------
# TAB 1: CYBER INCIDENTS
# -------------------------
with tab1:
    st.subheader("🛡️ Cyber Operations Center")
    
    if not inc_df.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            severities = inc_df['severity'].unique().tolist()
            selected_severity = st.multiselect(
                "🔍 Filter by Severity",
                severities,
                default=severities,
                key="dark_severity_filter"
            )
        
        with col2:
            statuses = inc_df['status'].unique().tolist()
            selected_status = st.multiselect(
                "🔍 Filter by Status",
                statuses,
                default=statuses,
                key="dark_status_filter"
            )
        
        with col3:
            if 'date' in inc_df.columns and inc_df['date'].notna().any():
                inc_df['date'] = pd.to_datetime(inc_df['date'], errors='coerce')
                date_range = st.date_input(
                    "📅 Date Range",
                    value=(inc_df['date'].min(), inc_df['date'].max()),
                    min_value=inc_df['date'].min(),
                    max_value=inc_df['date'].max(),
                    key="dark_date_filter"
                )
        
        # Filter data
        filtered_inc = inc_df[
            (inc_df['severity'].isin(selected_severity)) &
            (inc_df['status'].isin(selected_status))
        ]
        
        # Charts with dark theme
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌌 Incidents by Severity**")
            severity_counts = filtered_inc['severity'].value_counts()
            fig = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                color_discrete_sequence=cosmic_colors['primary'],
                hole=0.4
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_incidents_severity_pie")
        
        with col2:
            st.markdown("**⚡ Incidents by Status**")
            status_counts = filtered_inc['status'].value_counts()
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                labels={'x': 'Status', 'y': 'Count'},
                color=status_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_incidents_status_bar")
        
        # Timeline with cosmic theme
        if 'date' in filtered_inc.columns and filtered_inc['date'].notna().any():
            st.markdown("**🛸 Temporal Analysis - Incident Timeline**")
            timeline_df = filtered_inc.groupby(filtered_inc['date'].dt.to_period('M')).size().reset_index(name='count')
            timeline_df['date'] = timeline_df['date'].astype(str)
            fig = px.line(
                timeline_df,
                x='date',
                y='count',
                markers=True,
                labels={'date': 'Month', 'count': 'Number of Incidents'},
                title="Cosmic Threat Timeline",
                color_discrete_sequence=[cosmic_colors['accent']]
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                xaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)'),
                yaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)')
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_incidents_timeline")
        
        # Data table
        st.markdown("**📋 Incident Details**")
        st.dataframe(
            filtered_inc[['id', 'title', 'severity', 'status', 'date']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("🌌 No incidents data available in the cosmic database.")

# -------------------------
# TAB 2: DATASETS
# -------------------------
with tab2:
    st.subheader("📚 Data Archives - Knowledge Base")
    
    if not dat_df.empty:
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Datasets", len(dat_df))
        with col2:
            total_size = dat_df['size'].sum() if 'size' in dat_df.columns else 0
            st.metric("💾 Total Size", f"{total_size:,} MB" if total_size else "N/A")
        with col3:
            avg_size = dat_df['size'].mean() if 'size' in dat_df.columns else 0
            st.metric("📈 Avg Size", f"{avg_size:.0f} MB" if avg_size else "N/A")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌌 Datasets by Category**")
            if 'category' in dat_df.columns:
                category_counts = dat_df['category'].value_counts()
                fig = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    color_discrete_sequence=cosmic_colors['primary'],
                    hole=0.4
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e0e0e0'
                )
                st.plotly_chart(fig, use_container_width=True, key="dark_datasets_category_pie")
        
        with col2:
            st.markdown("**🚀 Datasets by Source**")
            if 'source' in dat_df.columns:
                source_counts = dat_df['source'].value_counts()
                fig = px.bar(
                    x=source_counts.index,
                    y=source_counts.values,
                    labels={'x': 'Source', 'y': 'Count'},
                    color=source_counts.values,
                    color_continuous_scale='Plasma'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e0e0e0',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, key="dark_datasets_source_bar")
        
        # Size distribution
        if 'size' in dat_df.columns and dat_df['size'].notna().any():
            st.markdown("**📊 Size Distribution Analysis**")
            fig = px.histogram(
                dat_df,
                x='size',
                nbins=20,
                labels={'size': 'Size (MB)', 'count': 'Number of Datasets'},
                title="Cosmic Data Distribution",
                color_discrete_sequence=[cosmic_colors['accent']]
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                xaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)'),
                yaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)')
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_datasets_size_hist")
        
        # Data table
        st.markdown("**📋 Archive Details**")
        st.dataframe(dat_df, use_container_width=True, hide_index=True)
    else:
        st.info("🌌 No datasets available in the cosmic archives.")

# -------------------------
# TAB 3: IT TICKETS
# -------------------------
with tab3:
    st.subheader("🎫 Support Tickets - Mission Control")
    
    if not tic_df.empty:
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            priorities = tic_df['priority'].unique().tolist()
            selected_priority = st.multiselect(
                "🔍 Filter by Priority",
                priorities,
                default=priorities,
                key="dark_ticket_priority"
            )
        
        with col2:
            statuses = tic_df['status'].unique().tolist()
            selected_status = st.multiselect(
                "🔍 Filter by Status",
                statuses,
                default=statuses,
                key="dark_ticket_status"
            )
        
        # Filter data
        filtered_tic = tic_df[
            (tic_df['priority'].isin(selected_priority)) &
            (tic_df['status'].isin(selected_status))
        ]
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌌 Tickets by Status**")
            status_counts = filtered_tic['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color_discrete_sequence=cosmic_colors['primary'],
                hole=0.4
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0'
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_tickets_status_pie")
        
        with col2:
            st.markdown("**⚡ Tickets by Priority**")
            priority_counts = filtered_tic['priority'].value_counts()
            fig = px.bar(
                x=priority_counts.index,
                y=priority_counts.values,
                labels={'x': 'Priority', 'y': 'Count'},
                color=priority_counts.values,
                color_continuous_scale='Cividis'
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_tickets_priority_bar")
        
        # Data table
        st.markdown("**📋 Ticket Details**")
        st.dataframe(filtered_tic, use_container_width=True, hide_index=True)
    else:
        st.info("🌌 No tickets available in mission control.")

# -------------------------
# TAB 4: ANALYTICS
# -------------------------
with tab4:
    st.subheader("📈 Comprehensive Analytics - Cosmic Intelligence")
    
    # Overall statistics
    st.markdown("**🌌 Mission Statistics**")
    
    stats_data = {
        'Module': ['🛡️ Cyber Operations', '📚 Data Archives', '🎫 Support Tickets'],
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
        st.markdown("**🛡️ Incident Severity Distribution**")
        if not inc_df.empty:
            severity_counts = inc_df['severity'].value_counts()
            fig = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                labels={'x': 'Severity', 'y': 'Count'},
                color=severity_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                showlegend=False,
                xaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)'),
                yaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)')
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_analytics_incidents_severity")
    
    with col2:
        st.markdown("**🎫 Ticket Priority Distribution**")
        if not tic_df.empty:
            priority_counts = tic_df['priority'].value_counts()
            fig = px.bar(
                x=priority_counts.index,
                y=priority_counts.values,
                labels={'x': 'Priority', 'y': 'Count'},
                color=priority_counts.values,
                color_continuous_scale='Plasma'
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                showlegend=False,
                xaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)'),
                yaxis=dict(gridcolor='rgba(123, 44, 191, 0.3)')
            )
            st.plotly_chart(fig, use_container_width=True, key="dark_analytics_tickets_priority")

# -------------------------
# TAB 5: ABOUT
# -------------------------
with tab5:
    st.subheader("🌌 About Intelligence Platform")
    
    st.markdown("""
    <div class="cosmic-card">
        <h2>🚀 Mission Statement</h2>
        <p>The Intelligence Platform represents the next generation of multi-domain intelligence 
        operations. Built for cosmic-scale data analysis and threat detection, this platform 
        empowers space rangers and cyber operatives to maintain security across all domains.</p>
        
        <h3>🛸 Key Features</h3>
        <ul>
            <li>Real-time threat detection and analysis</li>
            <li>Multi-domain data integration</li>
            <li>Advanced visualization and analytics</li>
            <li>Cosmic-grade security protocols</li>
        </ul>
        
        <h3>🌌 Technology Stack</h3>
        <p>Built with cutting-edge technologies for maximum performance and reliability:</p>
        <ul>
            <li>Streamlit for interactive dashboards</li>
            <li>Plotly for advanced visualizations</li>
            <li>SQLite for secure data storage</li>
            <li>Python for backend operations</li>
        </ul>
        
        <h3>🛡️ Security</h3>
        <p>Our platform implements quantum-resistant encryption and multi-factor authentication 
        to protect against future threats. We're prepared for tomorrow's challenges today.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**🌌 Designed for Space Rangers | Built for the Future**")

# Sidebar
with st.sidebar:
    st.markdown("### 🚀 Navigation")
    st.markdown("---")
    
    # Theme switcher
    st.markdown("### 🎨 Theme")
    if st.button("🌙 Switch to Light Mode"):
        st.session_state.theme = "light"
        st.switch_page("pages/Dashboard.py")
    
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


