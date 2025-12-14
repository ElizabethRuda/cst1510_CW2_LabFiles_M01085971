import streamlit as st

SPECIAL_CHARS = "!@#$%^&*()-_=+[]{};:,.<>?/\\|`~\"'"

def ensure_session_defaults():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    # demo users storage (week 9). later can connect DB service
    if "users" not in st.session_state:
        st.session_state.users = {}

def require_login():
    ensure_session_defaults()
    if not st.session_state.logged_in:
        st.error("Нужно войти в систему.")
        if st.button("Switch to login"):
            st.switch_page("Home.py")
        st.stop()

def validate_username(username: str):
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    return True, ""

def validate_password(password: str):
    if len(password) < 6 or len(password) > 50:
        return False, "Password must be between 6 and 50 characters."
    if not any(c.islower() for c in password):
        return False, "Password must include at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return False, "Password must include at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must include at least one digit."
    if not any(c in SPECIAL_CHARS for c in password):
        return False, "Password must include at least one special character."
    return True, ""

def password_strength(password: str) -> str:
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in SPECIAL_CHARS for c in password): score += 1

    if score <= 3:
        return "Weak"
    elif score <= 5:
        return "Medium"
    return "Strong"
