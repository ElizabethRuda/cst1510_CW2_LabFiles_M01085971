# Multi-Domain Intelligence Platform - Project Structure

## Current Active Structure (multi_domain_platform/)

This is the main project structure that is actively used:

```
/home/stud/
├── Home.py                          # Main entry point (uses auth.py)
├── pages/
│   └── Dashboard.py                 # Main dashboard (uses multi_domain_platform)
├── auth.py                          # Authentication utilities (used by Home.py)
├── requirements.txt                  # Python dependencies
├── README.md                        # Project documentation
├── secrets.toml                     # Configuration file
├── .gitignore                       # Git ignore rules
├── CW2_TECHNICAL_REPORT.md         # Technical report
├── ER_DIAGRAM.txt                   # Entity-Relationship diagram
├── UML_DIAGRAM.txt                  # UML diagram
├── DFD_DIAGRAM.txt                  # Data Flow diagram
├── REQUIREMENTS_CHECK.md            # Requirements compliance check
└── multi_domain_platform/           # Main application package
    ├── models/                      # Data models (OOP)
    │   ├── __init__.py
    │   ├── user.py                  # User model
    │   ├── security_incident.py     # SecurityIncident model
    │   ├── dataset.py               # Dataset model
    │   └── it_ticket.py             # ITTicket model
    ├── services/                    # Business logic services
    │   ├── __init__.py
    │   ├── database_manager.py      # Database operations (CRUD)
    │   ├── auth_manager.py          # Authentication with bcrypt
    │   └── ai_assistant.py          # AI/OpenAI integration
    ├── database/                    # Database files
    │   ├── db.py                    # Database utilities
    │   └── platform.db              # SQLite database
    └── pages/                       # Streamlit pages
        ├── 1_🔑_Login.py            # Login page
        ├── 2_🚨_Cybersecurity.py    # Cybersecurity domain
        ├── 3_📊_Data_Science.py     # Data Science domain
        ├── 4_💻_IT_Operations.py   # IT Operations domain
        └── 5_🤖_AI_Assistant.py     # AI Assistant page
```

## File Usage Map

### Active Files (Currently Used)

**Root Level:**
- `Home.py` - Main entry point, uses `auth.py`
- `pages/Dashboard.py` - Main dashboard, uses `multi_domain_platform.services`
- `auth.py` - Authentication utilities (used by Home.py)
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- `secrets.toml` - Configuration
- `.gitignore` - Git configuration
- `CW2_TECHNICAL_REPORT.md` - Technical documentation
- `ER_DIAGRAM.txt`, `UML_DIAGRAM.txt`, `DFD_DIAGRAM.txt` - Diagrams
- `REQUIREMENTS_CHECK.md` - Requirements compliance

**multi_domain_platform/ (All Active):**
- All files in `models/` - Used by services and pages
- All files in `services/` - Used by Dashboard and pages
- All files in `database/` - Used by DatabaseManager
- All files in `pages/` - Streamlit pages accessible via navigation

### Legacy/Unused Files (Not Referenced in Active Code)

**Old Structure (app/):**
- `app/` directory - Old structure, replaced by `multi_domain_platform/`
- `app/data/` - Old data layer, replaced by `multi_domain_platform/services/database_manager.py`
- `app/models/` - Old models, replaced by `multi_domain_platform/models/`
- `app/services/` - Old services, replaced by `multi_domain_platform/services/`
- `app/repositories/` - Old repository pattern, replaced by services
- `app/examples/` - Example files, not used in production

**Old Structure (Streamlit/):**
- `Streamlit/` directory - Old Streamlit structure
- `Streamlit/Home.py` - Old home page (contains Russian text)
- `Streamlit/auth.py` - Old auth file (contains Russian text)
- `Streamlit/Dashboard.py` - Old dashboard
- `Streamlit/pages/` - Old pages structure

**Template/Reference Files:**
- `tz/` directory - Template files and examples (not used in production)
- `main.py` - Old entry point (not used)
- `test_db.py` - Test file (not used in production)

## Migration Status

### Before (Old Structure)
```
app/
├── data/          # Data access layer
├── models/        # OOP models
├── services/      # Business logic
└── repositories/  # Repository pattern

Streamlit/
├── Home.py
├── Dashboard.py
└── pages/
```

### After (Current Structure)
```
multi_domain_platform/
├── models/        # OOP models (refactored)
├── services/      # Business logic (includes DB operations)
├── database/      # Database files
└── pages/         # Streamlit pages

Root:
├── Home.py        # Main entry
└── pages/
    └── Dashboard.py
```

## Recommendations

1. **Remove Legacy Directories:**
   - `app/` - Completely replaced by `multi_domain_platform/`
   - `Streamlit/` - Contains old files with Russian text, not used
   - `tz/` - Template files, not needed in production

2. **Keep for Reference (Optional):**
   - `test_db.py` - May be useful for testing
   - `main.py` - May be useful as reference

3. **Language Compliance:**
   - ✅ All active files (`multi_domain_platform/`, `Home.py`, `pages/Dashboard.py`) are in English
   - ⚠️ Legacy files in `Streamlit/` contain Russian text (not used)

## Import Dependencies

**Home.py imports:**
- `auth.py` (root level)

**pages/Dashboard.py imports:**
- `multi_domain_platform.services.database_manager`
- `multi_domain_platform.services.ai_assistant`

**multi_domain_platform/pages/*.py import:**
- `multi_domain_platform.services.*`
- `multi_domain_platform.models.*`

**No active code imports from:**
- `app/` directory
- `Streamlit/` directory
- `tz/` directory

