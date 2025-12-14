# Git Cleanup Instructions for CW2

This guide will help you clean up your git repository to include only the files needed for the course work.

## Step 1: Remove Legacy Files from Git

Run these commands to remove unused directories from git tracking:

```bash
# Remove legacy directories from git (files stay locally)
git rm -r --cached app/
git rm -r --cached Streamlit/
git rm -r --cached tz/

# Remove database files if tracked
git ls-files | grep "\.db$" | xargs git rm --cached

# Remove secrets.toml if tracked
git rm --cached secrets.toml 2>/dev/null || true

# Remove test files if tracked
git rm --cached test_db.py 2>/dev/null || true
git rm --cached main.py 2>/dev/null || true
```

## Step 2: Add Only Required Files

```bash
# Add updated .gitignore first
git add .gitignore

# Add main application files
git add Home.py
git add auth.py
git add pages/Dashboard.py

# Add new multi_domain_platform structure
git add multi_domain_platform/

# Add documentation
git add README.md
git add CW2_TECHNICAL_REPORT.md
git add REQUIREMENTS_CHECK.md
git add PROJECT_STRUCTURE.md
git add STRUCTURE_MIGRATION.md
git add GIT_FILES.md
git add GIT_CLEANUP_INSTRUCTIONS.md

# Add diagrams
git add ER_DIAGRAM.txt
git add UML_DIAGRAM.txt
git add DFD_DIAGRAM.txt

# Add configuration
git add requirements.txt
```

## Step 3: Verify What Will Be Committed

```bash
# Check status
git status

# See what files are tracked
git ls-files | head -30

# Verify no legacy files
git ls-files | grep -E "(^app/|^Streamlit/|^tz/)" && echo "WARNING: Legacy files still tracked!" || echo "OK: No legacy files"
```

## Step 4: Commit Changes

```bash
git commit -m "CW2: Clean up repository - remove legacy files, add multi_domain_platform structure

- Removed legacy directories: app/, Streamlit/, tz/
- Added new multi_domain_platform/ structure
- Updated .gitignore to exclude unused files
- All code and documentation in English
- Only active files included"
```

## Step 5: Push to GitHub

```bash
git push origin main
```

## Quick Script (Alternative)

You can also use the provided cleanup script:

```bash
./cleanup_git.sh
```

Then review and commit:

```bash
git status
git commit -m "CW2: Clean repository structure"
git push
```

## Files That Should Be in Git

### ✅ Included:
- `Home.py` - Main entry point
- `auth.py` - Authentication
- `pages/Dashboard.py` - Dashboard
- `multi_domain_platform/` - Complete application structure
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- `CW2_TECHNICAL_REPORT.md` - Technical report
- `ER_DIAGRAM.txt`, `UML_DIAGRAM.txt`, `DFD_DIAGRAM.txt` - Diagrams
- `REQUIREMENTS_CHECK.md` - Requirements check
- `PROJECT_STRUCTURE.md` - Structure documentation
- `.gitignore` - Git ignore rules

### ❌ Excluded (via .gitignore):
- `app/` - Legacy directory
- `Streamlit/` - Legacy directory
- `tz/` - Template files
- `*.db` - Database files
- `secrets.toml` - Sensitive configuration
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files

## Verification Checklist

After cleanup, verify:

- [ ] No `app/` directory in git
- [ ] No `Streamlit/` directory in git
- [ ] No `tz/` directory in git
- [ ] No `*.db` files in git
- [ ] `multi_domain_platform/` is tracked
- [ ] All documentation files are tracked
- [ ] `.gitignore` is updated and tracked

## If Something Goes Wrong

If you accidentally remove something important:

```bash
# Restore a file from git
git restore <file>

# Or restore entire directory
git restore app/
```

## Final Repository Structure

After cleanup, your git repository should contain:

```
.
├── .gitignore
├── Home.py
├── auth.py
├── pages/
│   └── Dashboard.py
├── multi_domain_platform/
│   ├── models/
│   ├── services/
│   ├── database/
│   └── pages/
├── requirements.txt
├── README.md
├── CW2_TECHNICAL_REPORT.md
├── REQUIREMENTS_CHECK.md
├── PROJECT_STRUCTURE.md
├── STRUCTURE_MIGRATION.md
├── ER_DIAGRAM.txt
├── UML_DIAGRAM.txt
└── DFD_DIAGRAM.txt
```

No legacy directories, no database files, no secrets - only clean, active code and documentation.

