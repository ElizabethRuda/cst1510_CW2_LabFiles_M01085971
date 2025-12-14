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
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. **Initialize the database:**
   ```bash
   python -c "from app.data.schema import create_all_tables; create_all_tables()"
   ```

5. **Load sample data:**
   ```bash
   python -c "from app.data.db import connect_database; from app.data.incidents import load_incidents_from_csv; from app.data.datasets import load_datasets_from_csv; from app.data.tickets import load_tickets_from_csv; conn = connect_database(); load_incidents_from_csv(conn); load_datasets_from_csv(conn); load_tickets_from_csv(conn); conn.close()"
   ```

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
├── app/
│   ├── data/              # Database access layer
│   │   ├── db.py          # Database connection
│   │   ├── schema.py      # Database schema definitions
│   │   ├── incidents.py   # Cyber incidents CRUD
│   │   ├── datasets.py    # Datasets CRUD
│   │   ├── tickets.py     # IT tickets CRUD
│   │   └── users.py       # User management
│   ├── models/            # OOP model classes
│   │   ├── user.py        # User model
│   │   ├── incident.py    # SecurityIncident model
│   │   ├── dataset.py     # Dataset model
│   │   └── ticket.py      # ITTicket model
│   ├── repositories/      # Repository pattern
│   │   └── incident_repository.py
│   ├── services/          # Business logic layer
│   │   ├── ai_service.py  # OpenAI integration
│   │   ├── incident_service.py
│   │   ├── dataset_service.py
│   │   ├── ticket_service.py
│   │   └── user_service.py
│   └── examples/          # Usage examples
│       └── oop_usage_example.py
├── pages/                 # Streamlit pages
│   └── Dashboard.py       # Main dashboard
├── DATA/                  # Database and data files
│   ├── intelligence_platform.db
│   ├── cyber_incidents.csv
│   ├── datasets_metadata.csv
│   └── it_tickets.csv
├── Home.py                # Main entry point
├── auth.py                # Authentication functions
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
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

### Using OOP Models

```python
from app.models.user import User
from app.models.incident import SecurityIncident

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

### Using Repository Pattern

```python
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

**Note:** Requires OpenAI API key in `.env` file:
```
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

The application follows a layered architecture:

1. **UI Layer** - Streamlit pages and components
2. **Service Layer** - Business logic and AI integration
3. **Repository Layer** - Data access abstraction
4. **Model Layer** - OOP domain models
5. **Data Access Layer** - Database operations

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
# Recreate database
rm DATA/intelligence_platform.db
python -c "from app.data.schema import create_all_tables; create_all_tables()"
```

### Import Errors
```bash
# Ensure you're in the project root directory
cd /path/to/project
streamlit run Home.py
```

### AI Assistant Not Working
- Check that `.env` file exists with `OPENAI_API_KEY`
- Verify API key is valid
- Check internet connection

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
