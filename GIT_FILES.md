# Files to Include in Git for CW2

This document lists all files that should be committed to git for the course work.

## Required Files for Git

### Root Level Files
```
✅ Home.py                          # Main entry point
✅ auth.py                          # Authentication utilities
✅ requirements.txt                 # Python dependencies
✅ README.md                        # Project documentation
✅ .gitignore                       # Git ignore rules
✅ CW2_TECHNICAL_REPORT.md         # Technical report
✅ ER_DIAGRAM.txt                   # Entity-Relationship diagram
✅ UML_DIAGRAM.txt                  # UML diagram
✅ DFD_DIAGRAM.txt                  # Data Flow diagram
✅ REQUIREMENTS_CHECK.md            # Requirements compliance check
✅ PROJECT_STRUCTURE.md             # Project structure documentation
✅ STRUCTURE_MIGRATION.md           # Migration documentation
✅ GIT_FILES.md                     # This file
```

### Application Structure
```
✅ pages/
   └── Dashboard.py                 # Main dashboard

✅ multi_domain_platform/
   ├── models/
   │   ├── __init__.py
   │   ├── user.py
   │   ├── security_incident.py
   │   ├── dataset.py
   │   └── it_ticket.py
   ├── services/
   │   ├── __init__.py
   │   ├── database_manager.py
   │   ├── auth_manager.py
   │   └── ai_assistant.py
   ├── database/
   │   └── db.py                    # Database utilities (platform.db excluded)
   └── pages/
       ├── 1_🔑_Login.py
       ├── 2_🚨_Cybersecurity.py
       ├── 3_📊_Data_Science.py
       ├── 4_💻_IT_Operations.py
       └── 5_🤖_AI_Assistant.py
```

## Files Excluded from Git (via .gitignore)

### Legacy/Unused Directories
```
❌ app/                             # Old structure, replaced by multi_domain_platform/
❌ Streamlit/                       # Old Streamlit structure
❌ tz/                              # Template files
```

### Sensitive/Generated Files
```
❌ secrets.toml                     # Contains API keys (sensitive)
❌ *.db                             # Database files (generated)
❌ __pycache__/                     # Python cache
❌ *.pyc                            # Compiled Python files
❌ .env                             # Environment variables
```

### Optional Files (Excluded)
```
❌ test_db.py                        # Test files (optional)
❌ main.py                           # Old entry point (optional)
❌ DATA/                             # Data files (if large)
❌ screenshots/                      # Screenshots (if large)
```

## Git Commands

### Check what will be committed:
```bash
git status
```

### Add only required files:
```bash
# Add all files except those in .gitignore
git add .

# Or add specific files:
git add Home.py
git add auth.py
git add pages/
git add multi_domain_platform/
git add requirements.txt
git add README.md
git add *.md
git add *.txt
git add .gitignore
```

### Verify before commit:
```bash
# Check what will be committed
git status

# See file sizes
git ls-files | xargs ls -lh
```

### Commit:
```bash
git commit -m "CW2: Multi-Domain Intelligence Platform - Final structure"
```

## File Count Summary

**Included:**
- ~20 Python files (active code)
- ~5 Documentation files (.md)
- ~3 Diagram files (.txt)
- Configuration files (.gitignore, requirements.txt)

**Excluded:**
- Legacy directories (app/, Streamlit/, tz/)
- Database files (*.db)
- Cache files (__pycache__/)
- Sensitive files (secrets.toml)

## Notes

1. **Database files** (*.db) are excluded because:
   - They are generated files
   - They may contain test data
   - They can be recreated from schema

2. **Legacy directories** are excluded because:
   - They are not used in the active codebase
   - They contain old/duplicate code
   - They may contain Russian text (non-compliant)

3. **Secrets.toml** is excluded because:
   - It contains sensitive API keys
   - Should be configured locally
   - Can be documented in README

4. **All active code is in English** - compliant with requirements

