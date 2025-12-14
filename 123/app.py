import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
import sqlite3
from pathlib import Path
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Intelligence Platform Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def init_database():
    """Initialize database connection and create tables if needed"""
    db_path = Path("DATA/intelligence_platform.db")
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    
    # Create tables if they don't exist
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Cyber incidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Datasets metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            category TEXT,
            source TEXT,
            last_updated TEXT,
            record_count INTEGER,
            file_size_mb REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # IT tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            priority TEXT,
            status TEXT,
            category TEXT,
            subject TEXT NOT NULL,
            description TEXT,
            created_date TEXT,
            resolved_date TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    
    # Generate sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
    if cursor.fetchone()[0] == 0:
        generate_sample_data(conn)
    
    return conn

def generate_sample_data(conn):
    """Generate sample data for visualization"""
    cursor = conn.cursor()
    
    # Sample cyber incidents
    incident_types = ["Phishing", "Malware", "DDoS", "Data Breach", "Ransomware", "SQL Injection"]
    severities = ["Critical", "High", "Medium", "Low"]
    statuses = ["Open", "Investigating", "Resolved", "Closed"]
    
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    for i in range(150):
        date_obj = pd.Timestamp(np.random.choice(dates))
        date = date_obj.strftime('%Y-%m-%d')
        incident_type = np.random.choice(incident_types)
        severity = np.random.choice(severities, p=[0.1, 0.3, 0.4, 0.2])
        status = np.random.choice(statuses, p=[0.2, 0.3, 0.3, 0.2])
        description = f"Sample {incident_type.lower()} incident detected"
        reported_by = np.random.choice(["alice", "bob", "charlie", "diana"])
        
        cursor.execute("""
            INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, incident_type, severity, status, description, reported_by))
    
    # Sample datasets metadata
    categories = ["Threat Intelligence", "Network Logs", "Security Events", "User Activity", "System Metrics"]
    sources = ["Internal", "External API", "SIEM", "Firewall", "IDS/IPS"]
    
    for i in range(25):
        dataset_name = f"Dataset_{i+1}"
        category = np.random.choice(categories)
        source = np.random.choice(sources)
        last_updated_obj = pd.Timestamp(np.random.choice(dates))
        last_updated = last_updated_obj.strftime('%Y-%m-%d')
        record_count = np.random.randint(1000, 100000)
        file_size_mb = round(np.random.uniform(10, 500), 2)
        
        cursor.execute("""
            INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, record_count, file_size_mb)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    
    # Sample IT tickets
    priorities = ["Critical", "High", "Medium", "Low"]
    ticket_statuses = ["Open", "In Progress", "Resolved", "Closed"]
    ticket_categories = ["Hardware", "Software", "Network", "Security", "Email", "Access"]
    assignees = ["alice", "bob", "charlie", "diana", "eve"]
    
    for i in range(80):
        ticket_id = f"TICKET-{1000+i}"
        priority = np.random.choice(priorities, p=[0.1, 0.2, 0.4, 0.3])
        status = np.random.choice(ticket_statuses, p=[0.2, 0.3, 0.3, 0.2])
        category = np.random.choice(ticket_categories)
        subject = f"Issue with {category.lower()}"
        description = f"User reported issue related to {category.lower()}"
        created_date_obj = pd.Timestamp(np.random.choice(dates))
        created_date = created_date_obj.strftime('%Y-%m-%d')
        resolved_date = None
        if status in ["Resolved", "Closed"]:
            resolved_date = (created_date_obj + timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d')
        assigned_to = np.random.choice(assignees)
        
        cursor.execute("""
            INSERT INTO it_tickets (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))
    
    conn.commit()

# Initialize database
conn = init_database()

# Sidebar navigation
st.sidebar.title("📊 Intelligence Platform")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Выберите страницу",
    ["Главная", "Кибер-инциденты", "Метаданные датасетов", "IT-тикеты", "Общая статистика"]
)

# Main content based on selected page
if page == "Главная":
    st.markdown('<div class="main-header">📊 Intelligence Platform Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
        total_incidents = cursor.fetchone()[0]
        st.metric("Всего инцидентов", total_incidents)
    
    with col2:
        cursor.execute("SELECT COUNT(*) FROM cyber_incidents WHERE status = 'Open' OR status = 'Investigating'")
        active_incidents = cursor.fetchone()[0]
        st.metric("Активных инцидентов", active_incidents)
    
    with col3:
        cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
        total_datasets = cursor.fetchone()[0]
        st.metric("Датасетов", total_datasets)
    
    with col4:
        cursor.execute("SELECT COUNT(*) FROM it_tickets WHERE status = 'Open' OR status = 'In Progress'")
        open_tickets = cursor.fetchone()[0]
        st.metric("Открытых тикетов", open_tickets)
    
    st.markdown("---")
    
    # Quick charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Инциденты по типу")
        df_incidents = pd.read_sql_query("SELECT incident_type, COUNT(*) as count FROM cyber_incidents GROUP BY incident_type", conn)
        fig = px.pie(df_incidents, values='count', names='incident_type', 
                     title="Распределение инцидентов")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Статус инцидентов")
        df_status = pd.read_sql_query("SELECT status, COUNT(*) as count FROM cyber_incidents GROUP BY status", conn)
        fig = px.bar(df_status, x='status', y='count', 
                     title="Статус инцидентов",
                     color='count', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.info("💡 Используйте боковое меню для навигации по разделам")

elif page == "Кибер-инциденты":
    st.title("🛡️ Кибер-инциденты")
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT incident_type FROM cyber_incidents")
        types = [row[0] for row in cursor.fetchall()]
        selected_type = st.multiselect("Тип инцидента", types, default=types)
    
    with col2:
        severities = ["Critical", "High", "Medium", "Low"]
        selected_severity = st.multiselect("Уровень серьезности", severities, default=severities)
    
    with col3:
        statuses = ["Open", "Investigating", "Resolved", "Closed"]
        selected_status = st.multiselect("Статус", statuses, default=statuses)
    
    # Build query
    query = "SELECT * FROM cyber_incidents WHERE 1=1"
    params = []
    
    if selected_type:
        placeholders = ','.join(['?'] * len(selected_type))
        query += f" AND incident_type IN ({placeholders})"
        params.extend(selected_type)
    
    if selected_severity:
        placeholders = ','.join(['?'] * len(selected_severity))
        query += f" AND severity IN ({placeholders})"
        params.extend(selected_severity)
    
    if selected_status:
        placeholders = ','.join(['?'] * len(selected_status))
        query += f" AND status IN ({placeholders})"
        params.extend(selected_status)
    
    query += " ORDER BY date DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Всего", len(df))
    with col2:
        critical = len(df[df['severity'] == 'Critical'])
        st.metric("Критичных", critical, delta=None)
    with col3:
        open_count = len(df[df['status'].isin(['Open', 'Investigating'])])
        st.metric("Активных", open_count)
    with col4:
        resolved = len(df[df['status'] == 'Resolved'])
        st.metric("Решено", resolved)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Инциденты по типу")
        type_counts = df['incident_type'].value_counts()
        fig = px.bar(x=type_counts.index, y=type_counts.values,
                     labels={'x': 'Тип инцидента', 'y': 'Количество'},
                     color=type_counts.values,
                     color_continuous_scale='Reds')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Распределение по серьезности")
        severity_counts = df['severity'].value_counts()
        fig = px.pie(values=severity_counts.values, names=severity_counts.index,
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.subheader("📅 Временная линия инцидентов")
    df['date'] = pd.to_datetime(df['date'])
    df_timeline = df.groupby([df['date'].dt.to_period('M'), 'incident_type']).size().reset_index(name='count')
    df_timeline['date'] = df_timeline['date'].astype(str)
    
    fig = px.line(df_timeline, x='date', y='count', color='incident_type',
                  labels={'date': 'Месяц', 'count': 'Количество инцидентов'},
                  title="Динамика инцидентов по месяцам")
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 Таблица данных")
    st.dataframe(df[['date', 'incident_type', 'severity', 'status', 'description', 'reported_by']], 
                 use_container_width=True, hide_index=True)

elif page == "Метаданные датасетов":
    st.title("📚 Метаданные датасетов")
    st.markdown("---")
    
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Всего датасетов", len(df))
    with col2:
        total_records = df['record_count'].sum()
        st.metric("Всего записей", f"{total_records:,}")
    with col3:
        total_size = df['file_size_mb'].sum()
        st.metric("Общий размер", f"{total_size:.2f} MB")
    with col4:
        avg_size = df['file_size_mb'].mean()
        st.metric("Средний размер", f"{avg_size:.2f} MB")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Датасеты по категориям")
        category_counts = df['category'].value_counts()
        fig = px.pie(values=category_counts.values, names=category_counts.index,
                     title="Распределение по категориям")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Датасеты по источникам")
        source_counts = df['source'].value_counts()
        fig = px.bar(x=source_counts.index, y=source_counts.values,
                     labels={'x': 'Источник', 'y': 'Количество'},
                     color=source_counts.values,
                     color_continuous_scale='Greens')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Size distribution
    st.subheader("📊 Распределение размеров датасетов")
    fig = px.histogram(df, x='file_size_mb', nbins=20,
                       labels={'file_size_mb': 'Размер (MB)', 'count': 'Количество'},
                       title="Гистограмма размеров датасетов")
    st.plotly_chart(fig, use_container_width=True)
    
    # Records vs Size scatter
    st.subheader("📈 Записи vs Размер")
    fig = px.scatter(df, x='record_count', y='file_size_mb', 
                     size='file_size_mb', color='category',
                     hover_data=['dataset_name'],
                     labels={'record_count': 'Количество записей', 'file_size_mb': 'Размер (MB)'},
                     title="Корреляция между количеством записей и размером")
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 Таблица данных")
    st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "IT-тикеты":
    st.title("🎫 IT-тикеты")
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT status FROM it_tickets")
        statuses = [row[0] for row in cursor.fetchall()]
        selected_status = st.multiselect("Статус", statuses, default=statuses)
    
    with col2:
        priorities = ["Critical", "High", "Medium", "Low"]
        selected_priority = st.multiselect("Приоритет", priorities, default=priorities)
    
    # Build query
    query = "SELECT * FROM it_tickets WHERE 1=1"
    params = []
    
    if selected_status:
        placeholders = ','.join(['?'] * len(selected_status))
        query += f" AND status IN ({placeholders})"
        params.extend(selected_status)
    
    if selected_priority:
        placeholders = ','.join(['?'] * len(selected_priority))
        query += f" AND priority IN ({placeholders})"
        params.extend(selected_priority)
    
    query += " ORDER BY created_date DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Всего тикетов", len(df))
    with col2:
        open_tickets = len(df[df['status'].isin(['Open', 'In Progress'])])
        st.metric("Открытых", open_tickets)
    with col3:
        critical = len(df[df['priority'] == 'Critical'])
        st.metric("Критичных", critical)
    with col4:
        resolved = len(df[df['status'] == 'Resolved'])
        st.metric("Решено", resolved)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Тикеты по статусу")
        status_counts = df['status'].value_counts()
        fig = px.bar(x=status_counts.index, y=status_counts.values,
                     labels={'x': 'Статус', 'y': 'Количество'},
                     color=status_counts.values,
                     color_continuous_scale='Purples')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Тикеты по приоритету")
        priority_counts = df['priority'].value_counts()
        fig = px.pie(values=priority_counts.values, names=priority_counts.index,
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        st.plotly_chart(fig, use_container_width=True)
    
    # Category distribution
    st.subheader("📊 Распределение по категориям")
    category_counts = df['category'].value_counts()
    fig = px.bar(x=category_counts.index, y=category_counts.values,
                 labels={'x': 'Категория', 'y': 'Количество'},
                 color=category_counts.values,
                 color_continuous_scale='Blues')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Assignment
    st.subheader("👥 Назначение тикетов")
    if 'assigned_to' in df.columns and df['assigned_to'].notna().any():
        assigned_counts = df['assigned_to'].value_counts()
        fig = px.bar(x=assigned_counts.index, y=assigned_counts.values,
                     labels={'x': 'Назначено', 'y': 'Количество тикетов'},
                     color=assigned_counts.values,
                     color_continuous_scale='Oranges')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 Таблица данных")
    display_cols = ['ticket_id', 'priority', 'status', 'category', 'subject', 'created_date', 'assigned_to']
    available_cols = [col for col in display_cols if col in df.columns]
    st.dataframe(df[available_cols], use_container_width=True, hide_index=True)

elif page == "Общая статистика":
    st.title("📊 Общая статистика")
    st.markdown("---")
    
    # Get all data
    df_incidents = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    df_datasets = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    df_tickets = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    
    # Overall metrics
    st.subheader("🎯 Ключевые показатели")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Инцидентов", len(df_incidents))
    with col2:
        st.metric("Датасетов", len(df_datasets))
    with col3:
        st.metric("Тикетов", len(df_tickets))
    with col4:
        total_data = df_datasets['file_size_mb'].sum()
        st.metric("Данных (MB)", f"{total_data:.0f}")
    with col5:
        critical_incidents = len(df_incidents[df_incidents['severity'] == 'Critical'])
        st.metric("Критичных", critical_incidents)
    
    st.markdown("---")
    
    # Trend analysis
    st.subheader("📈 Анализ трендов")
    
    # Incidents over time
    if 'date' in df_incidents.columns:
        df_incidents['date'] = pd.to_datetime(df_incidents['date'])
        df_incidents_monthly = df_incidents.groupby(df_incidents['date'].dt.to_period('M')).size().reset_index(name='count')
        df_incidents_monthly['date'] = df_incidents_monthly['date'].astype(str)
        
        fig = px.line(df_incidents_monthly, x='date', y='count',
                     labels={'date': 'Месяц', 'count': 'Количество инцидентов'},
                     title="Тренд инцидентов по месяцам",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Comparison chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Статус инцидентов")
        status_counts = df_incidents['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                     title="Распределение статусов")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Статус тикетов")
        ticket_status_counts = df_tickets['status'].value_counts()
        fig = px.pie(values=ticket_status_counts.values, names=ticket_status_counts.index,
                     title="Распределение статусов тикетов")
        st.plotly_chart(fig, use_container_width=True)
    
    # Data summary
    st.subheader("📋 Сводка данных")
    
    summary_data = {
        'Модуль': ['Кибер-инциденты', 'Метаданные датасетов', 'IT-тикеты'],
        'Записей': [len(df_incidents), len(df_datasets), len(df_tickets)],
        'Активных': [
            len(df_incidents[df_incidents['status'].isin(['Open', 'Investigating'])]),
            len(df_datasets),
            len(df_tickets[df_tickets['status'].isin(['Open', 'In Progress'])])
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 Intelligence Platform Dashboard\n\nВизуализация данных платформы")

