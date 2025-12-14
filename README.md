# Multi-Domain Intelligence Platform

**Student Name:** Yelyzaveta Ruda  
**Student ID:** M01085971  
**Course:** CST1510 - Multi-Domain Intelligence Platform  
**Project Type:** Coursework 2 (CW2)

---

## 📋 Project Overview

The **Multi-Domain Intelligence Platform** is a unified web application built with Python and Streamlit that serves three distinct user groups:

- **Cybersecurity Analysts** - Incident response and threat analysis
- **Data Scientists** - Dataset governance and discovery
- **IT Administrators** - Service desk performance and ticket management

The platform provides high-value analysis, insights, and operational capabilities to address critical real-world problems within each domain.

---

## ✨ Features

### Core Features
- ✅ **Secure Authentication** - Password hashing with bcrypt, role-based access
- ✅ **SQLite Database** - Full CRUD operations for all three domains
- ✅ **Interactive Dashboards** - Real-time data visualization with Plotly
- ✅ **AI Integration** - OpenAI-powered assistant for intelligent insights
- ✅ **Object-Oriented Architecture** - Clean, maintainable code structure

### Domain-Specific Features

#### 🛡️ Cybersecurity Domain
- Incident tracking and severity analysis
- Threat trend identification
- Resolution time analysis
- Interactive visualizations (pie charts, bar charts, timelines)

#### 📚 Data Science Domain
- Dataset catalog management
- Resource consumption analysis
- Data governance recommendations
- Size distribution visualizations

#### 🎫 IT Operations Domain
- Ticket priority and status tracking
- Performance metrics
- Process efficiency analysis
- Resolution workflow visualization

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional, for AI features):**
   ```bash
   # Create .streamlit/secrets.toml file
   mkdir -p .streamlit
   echo "[secrets]" > .streamlit/secrets.toml
   echo "OPENAI_API_KEY=your_api_key_here" >> .streamlit/secrets.toml
   ```

4. **Initialize the database:**
   The database is automatically initialized when you first run the application. The `DatabaseManager` class creates all necessary tables on first use.

   If you need to load sample data from CSV files, ensure the CSV files are in the `DATA/` directory and the database will be created at:
   - `DATA/intelligence_platform.db` (if exists) or
   - `multi_domain_platform/database/platform.db` (default)

### Running the Application

```bash
streamlit run Home.py
```

The application will be available at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://<your-ip>:8501

---

## 🔐 Default Login Credentials

For testing purposes, the following accounts are available:

| Username | Password | Role |
|----------|----------|------|
| `admin` | `Admin123!` | Admin |
| `test` | `Test123!` | User |
| `user` | `User123!` | User |

---

## 📁 Project Structure

```
project_root/
├── multi_domain_platform/    # Main application package
│   ├── models/               # OOP model classes (Week 11)
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── security_incident.py  # SecurityIncident model
│   │   ├── dataset.py        # Dataset model
│   │   └── it_ticket.py      # ITTicket model
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── database_manager.py  # Database operations (CRUD)
│   │   ├── auth_manager.py      # Authentication with bcrypt
│   │   └── ai_assistant.py      # OpenAI ChatGPT integration
│   ├── database/             # Database layer
│   │   ├── db.py             # Database initialization
│   │   └── platform.db       # SQLite database (excluded from Git)
│   └── pages/                # Streamlit pages (Week 9)
│       ├── 1_🔑_Login.py
│       ├── 2_🚨_Cybersecurity.py
│       ├── 3_📊_Data_Science.py
│       ├── 4_💻_IT_Operations.py
│       └── 5_🤖_AI_Assistant.py
├── pages/                    # Streamlit pages (for runtime)
│   └── Dashboard.py          # Main dashboard
├── DATA/                     # Database and data files (excluded from Git)
│   ├── intelligence_platform.db
│   ├── cyber_incidents.csv
│   ├── datasets_metadata.csv
│   └── it_tickets.csv
├── Home.py                   # Main entry point (streamlit run Home.py)
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── .cursorrules             # Development rules
├── README.md                # This file
├── CW2_TECHNICAL_REPORT.md  # Technical report
├── UML_DIAGRAM.txt          # UML class diagram
├── ER_DIAGRAM.txt           # Entity-Relationship diagram
└── DFD_DIAGRAM.txt          # Data Flow diagram
```

---

## 🛠️ Technology Stack

- **Backend:** Python 3.x
- **Web Framework:** Streamlit 1.28.0+
- **Database:** SQLite3
- **Data Processing:** Pandas 2.0.0+
- **Visualization:** Plotly 5.17.0+
- **Security:** bcrypt 4.0.0+
- **AI Integration:** OpenAI API (GPT-3.5-turbo)
- **Environment Management:** python-dotenv

---

## 📊 Database Schema

The application uses SQLite with four main tables:

1. **users** - User authentication and roles
2. **cyber_incidents** - Security incident records
3. **datasets_metadata** - Dataset catalog information
4. **it_tickets** - IT support ticket records

For detailed schema information, see `ER_DIAGRAM.txt`.

---

## 🎯 Usage Examples

### Using OOP Models (Week 11)

```python
from multi_domain_platform.models.user import User
from multi_domain_platform.models.security_incident import SecurityIncident

# Create a user
password = "SecurePass123!"
hashed = User.hash_password(password)
user = User("john_doe", hashed, "admin")

# Create an incident
incident = SecurityIncident(
    title="SQL Injection Attempt",
    severity="Critical",
    status="open"
)
```

### Using Database Manager (CRUD Operations - Week 8)

```python
from multi_domain_platform.services.database_manager import DatabaseManager

db = DatabaseManager()

# CREATE - Insert new record
db.execute_update(
    "INSERT INTO cyber_incidents (title, severity, status) VALUES (?, ?, ?)",
    ("Malware Detection", "High", "open")
)

# READ - Query data
incidents = db.execute_query("SELECT * FROM cyber_incidents WHERE severity = ?", ("Critical",))

# UPDATE - Modify record
db.execute_update(
    "UPDATE cyber_incidents SET status = ? WHERE id = ?",
    ("resolved", 1)
)

# DELETE - Remove record
db.execute_update("DELETE FROM cyber_incidents WHERE id = ?", (1,))
```

### Using Authentication Manager (Week 7)

```python
from multi_domain_platform.services.auth_manager import AuthManager
from multi_domain_platform.services.database_manager import DatabaseManager

db = DatabaseManager()
auth = AuthManager(db)

# Register new user (password automatically hashed with bcrypt)
auth.register_user("newuser", "SecurePass123!", "user")

# Login user
success = auth.login_user("newuser", "SecurePass123!")
```

### Using AI Assistant (Week 10)

```python
from multi_domain_platform.services.ai_assistant import AIAssistant

ai = AIAssistant()
if ai.is_available():
    response = ai.generate_response("What are the top security threats?")
    print(response)
```
from app.repositories.incident_repository import IncidentRepository

repo = IncidentRepository(db_path="DATA/intelligence_platform.db")
incidents = repo.get_all()
```

See `app/examples/oop_usage_example.py` for more examples.

---

## 🤖 AI Assistant

The AI Assistant feature provides intelligent insights for:
- Security advice based on incident summaries
- Data trend analysis
- General questions about cybersecurity, IT operations, and data science

**Note:** Requires OpenAI API key in `.streamlit/secrets.toml` file:
```toml
[secrets]
OPENAI_API_KEY=your_key_here
```

---

## 📈 Visualizations

The Dashboard includes comprehensive visualizations:

- **Pie Charts** - Distribution analysis (severity, status, category)
- **Bar Charts** - Count comparisons
- **Line Charts** - Timeline trends
- **Histograms** - Size distributions

All visualizations are interactive and powered by Plotly.

---

## 🏗️ Architecture

The application follows a layered architecture (MVC pattern):

1. **View Layer** - Streamlit pages (`pages/`, `multi_domain_platform/pages/`)
2. **Service Layer** - Business logic (`multi_domain_platform/services/`)
   - `database_manager.py` - CRUD operations with parameterized queries
   - `auth_manager.py` - Authentication with bcrypt hashing
   - `ai_assistant.py` - OpenAI ChatGPT integration
3. **Model Layer** - OOP domain models (`multi_domain_platform/models/`)
   - `User`, `SecurityIncident`, `Dataset`, `ITTicket`
4. **Data Layer** - Database persistence (`multi_domain_platform/database/`)

**Note:** The root `pages/` directory is used by Streamlit at runtime. The actual source code pages are in `multi_domain_platform/pages/` as per project requirements.

For detailed architecture information, see `UML_DIAGRAM.txt` and `CW2_TECHNICAL_REPORT.md`.

---

## 📝 Documentation

- **Technical Report:** `CW2_TECHNICAL_REPORT.md` (1,384 words)
- **UML Diagram:** `UML_DIAGRAM.txt`
- **ER Diagram:** `ER_DIAGRAM.txt`
- **Data Flow Diagram:** `DFD_DIAGRAM.txt`
- **Requirements Check:** `REQUIREMENTS_CHECK.md`

---

## ✅ Requirements Compliance

This project implements **Tier 3 (High Distinction)** level:

- ✅ All three domains fully implemented
- ✅ Secure authentication with bcrypt
- ✅ Complete CRUD operations
- ✅ Comprehensive visualizations
- ✅ AI integration
- ✅ OOP refactoring
- ✅ Repository pattern
- ✅ Technical documentation

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Database is automatically created on first run
# If you need to reset, delete the database file:
rm DATA/intelligence_platform.db
# or
rm multi_domain_platform/database/platform.db
# Then restart the application - it will recreate the schema
```

### Import Errors
```bash
# Ensure you're in the project root directory
cd /path/to/project
# Make sure all dependencies are installed
pip install -r requirements.txt
streamlit run Home.py
```

### AI Assistant Not Working
- Check that `.streamlit/secrets.toml` file exists with `OPENAI_API_KEY`
- Verify API key is valid
- Check internet connection
- The AI Assistant will show a warning if the API key is not configured

### No Data Showing in Dashboard
- Ensure the database file exists in `DATA/intelligence_platform.db` or `multi_domain_platform/database/platform.db`
- Check that CSV files are in the `DATA/` directory if you need to load sample data
- The `DatabaseManager` automatically checks for existing database in `DATA/` first

---

## 📄 License

This project is part of CST1510 coursework at Leeds Beckett University.

---

## 👤 Author

**Yelyzaveta Ruda**  
Student ID: M01085971  
Email: M01085971@students.leedsbeckett.ac.uk

---

## 🙏 Acknowledgments

- Streamlit team for the excellent web framework
- OpenAI for AI capabilities
- Plotly for interactive visualizations

---

**Last Updated:** December 2025
