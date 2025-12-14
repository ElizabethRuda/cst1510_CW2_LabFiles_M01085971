# Multi-Domain Intelligence Platform

**Student Name:** Yelyzaveta Ruda  
**Student ID:** M01085971  
**Course:** CST1510 - Multi-Domain Intelligence Platform  
**Project Type:** Coursework 2 (CW2)  
**Date:** December 2025

---

## Project Overview

This is a web application built with Python and Streamlit that serves three different user groups:

- Cybersecurity Analysts - for incident response and threat analysis
- Data Scientists - for dataset governance and discovery
- IT Administrators - for service desk performance and ticket management

The platform provides analysis and insights for each domain.

---

## Features

### Core Features
- Secure authentication with bcrypt password hashing
- SQLite database with CRUD operations for all three domains
- Interactive dashboards with Plotly visualizations
- AI integration using OpenAI API
- Object-oriented code structure

### Domain Features

**Cybersecurity Domain:**
- Incident tracking and severity analysis
- Threat trend identification
- Resolution time analysis
- Charts and visualizations

**Data Science Domain:**
- Dataset catalog management
- Resource consumption analysis
- Size distribution visualizations

**IT Operations Domain:**
- Ticket priority and status tracking
- Performance metrics
- Resolution workflow visualization

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ElizabethRuda/cst1510_CW2_LabFiles_M01085971.git
   cd cst1510_CW2_LabFiles_M01085971
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up AI features (optional):
   Create `.streamlit/secrets.toml` file:
   ```toml
   [secrets]
   OPENAI_API_KEY=your_api_key_here
   ```

4. Database initialization:
   The database is automatically created when you first run the application. If you have CSV files in the `DATA/` directory, the database will use `DATA/intelligence_platform.db`. Otherwise, it creates `multi_domain_platform/database/platform.db`.

### Running the Application

```bash
streamlit run Home.py
```

The application will be available at http://localhost:8501

---

## Default Login Credentials

For testing, you can use these accounts:

| Username | Password | Role |
|----------|----------|------|
| admin | Admin123! | Admin |
| test | Test123! | User |
| user | User123! | User |

---

## Project Structure

```
project_root/
├── multi_domain_platform/
│   ├── models/               # OOP model classes
│   │   ├── user.py
│   │   ├── security_incident.py
│   │   ├── dataset.py
│   │   └── it_ticket.py
│   ├── services/             # Business logic
│   │   ├── database_manager.py
│   │   ├── auth_manager.py
│   │   └── ai_assistant.py
│   ├── database/             # Database layer
│   │   ├── db.py
│   │   └── platform.db
│   └── pages/                # Streamlit pages
│       ├── 1_🔑_Login.py
│       ├── 2_🚨_Cybersecurity.py
│       ├── 3_📊_Data_Science.py
│       ├── 4_💻_IT_Operations.py
│       └── 5_🤖_AI_Assistant.py
├── pages/                    # Dashboard page
│   └── Dashboard.py
├── DATA/                     # Data files (not in git)
│   ├── intelligence_platform.db
│   ├── cyber_incidents.csv
│   ├── datasets_metadata.csv
│   └── it_tickets.csv
├── Home.py                   # Main entry point
├── requirements.txt
├── README.md
├── CW2_TECHNICAL_REPORT.md
├── UML_DIAGRAM.txt
├── ER_DIAGRAM.txt
└── DFD_DIAGRAM.txt
```

---

## Technology Stack

- Python 3.x
- Streamlit 1.28.0+
- SQLite3
- Pandas 2.0.0+
- Plotly 5.17.0+
- bcrypt 4.0.0+
- OpenAI API (GPT-3.5-turbo)
- python-dotenv

---

## Database Schema

The application uses SQLite with four main tables:

1. users - User authentication and roles
2. cyber_incidents - Security incident records
3. datasets_metadata - Dataset catalog information
4. it_tickets - IT support ticket records

For detailed schema, see `ER_DIAGRAM.txt`.

---

## Usage Examples

### Using OOP Models

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

### Using Database Manager (CRUD)

```python
from multi_domain_platform.services.database_manager import DatabaseManager

db = DatabaseManager()

# CREATE
db.execute_update(
    "INSERT INTO cyber_incidents (title, severity, status) VALUES (?, ?, ?)",
    ("Malware Detection", "High", "open")
)

# READ
incidents = db.execute_query("SELECT * FROM cyber_incidents WHERE severity = ?", ("Critical",))

# UPDATE
db.execute_update(
    "UPDATE cyber_incidents SET status = ? WHERE id = ?",
    ("resolved", 1)
)

# DELETE
db.execute_update("DELETE FROM cyber_incidents WHERE id = ?", (1,))
```

### Using Authentication

```python
from multi_domain_platform.services.auth_manager import AuthManager
from multi_domain_platform.services.database_manager import DatabaseManager

db = DatabaseManager()
auth = AuthManager(db)

# Register user (password hashed with bcrypt)
auth.register_user("newuser", "SecurePass123!", "user")

# Login
success = auth.login_user("newuser", "SecurePass123!")
```

### Using AI Assistant

```python
from multi_domain_platform.services.ai_assistant import AIAssistant

ai = AIAssistant()
if ai.is_available():
    response = ai.generate_response("What are the top security threats?")
    print(response)
```

---

## AI Assistant

The AI Assistant provides insights for security advice, data analysis, and general questions about cybersecurity, IT operations, and data science.

Requires OpenAI API key in `.streamlit/secrets.toml`:
```toml
[secrets]
OPENAI_API_KEY=your_key_here
```

---

## Visualizations

The Dashboard includes:
- Pie charts for distribution analysis
- Bar charts for count comparisons
- Line charts for timeline trends
- Histograms for size distributions

All visualizations are interactive using Plotly.

---

## Architecture

The application follows MVC architecture:

1. View Layer - Streamlit pages
2. Service Layer - Business logic (database_manager, auth_manager, ai_assistant)
3. Model Layer - OOP domain models (User, SecurityIncident, Dataset, ITTicket)
4. Data Layer - Database persistence

For detailed architecture, see `UML_DIAGRAM.txt` and `CW2_TECHNICAL_REPORT.md`.

---

## Documentation

- Technical Report: `CW2_TECHNICAL_REPORT.md`
- UML Diagram: `UML_DIAGRAM.txt`
- ER Diagram: `ER_DIAGRAM.txt`
- Data Flow Diagram: `DFD_DIAGRAM.txt`

---

## Requirements Compliance

This project implements Tier 3 (High Distinction) level:

- All three domains fully implemented
- Secure authentication with bcrypt
- Complete CRUD operations with parameterized queries
- Comprehensive visualizations
- AI integration
- OOP refactoring
- Technical documentation

---

## Troubleshooting

### Database Issues
The database is automatically created on first run. If you need to reset it, delete the database file and restart the application.

### Import Errors
Make sure you're in the project root directory and all dependencies are installed:
```bash
pip install -r requirements.txt
streamlit run Home.py
```

### AI Assistant Not Working
- Check that `.streamlit/secrets.toml` exists with `OPENAI_API_KEY`
- Verify API key is valid
- Check internet connection

### No Data Showing
- Ensure database file exists in `DATA/intelligence_platform.db` or `multi_domain_platform/database/platform.db`
- Check CSV files are in `DATA/` directory if loading sample data

---

## Author

Yelyzaveta Ruda  
Student ID: M01085971  
Email: M01085971@students.leedsbeckett.ac.uk

---

**Last Updated:** December 2025
