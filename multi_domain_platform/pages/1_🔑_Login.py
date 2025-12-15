"""
Login page for Multi-Domain Intelligence Platform
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from multi_domain_platform.services.auth_manager import AuthManager
from multi_domain_platform.services.database_manager import DatabaseManager

st.set_page_config(
    page_title="Login - Intelligence Platform",
    page_icon="🔑",
    layout="centered"
)

st.title("🔑 Login")
st.markdown("### Welcome to the Multi-Domain Intelligence Platform")

# Initialize database and auth manager
db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)

# Ensure session defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# If already logged in, show option to go to dashboard
if st.session_state.logged_in:
    st.success(f"✅ Already logged in as **{st.session_state.username}**")
    if st.button("Go to Dashboard", type="primary"):
        st.switch_page("Home.py")
    st.stop()

# Tabs for Login and Register
tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

# -------------------------
# REGISTER TAB
# -------------------------
with tab_register:
    st.subheader("Create New Account")
    
    with st.form("register_form"):
        reg_user = st.text_input("Username", key="reg_user")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        reg_pass2 = st.text_input("Confirm password", type="password", key="reg_pass2")
        reg_role = st.selectbox("Role", ["user", "admin", "analyst"], key="reg_role")
        
        submitted = st.form_submit_button("Create account", type="primary")
        if submitted:
            reg_user = reg_user.strip()
            
            if not reg_user:
                st.error("Username is required")
            elif len(reg_user) < 3:
                st.error("Username must be at least 3 characters")
            elif not reg_pass:
                st.error("Password is required")
            elif len(reg_pass) < 6:
                st.error("Password must be at least 6 characters")
            elif reg_pass != reg_pass2:
                st.error("Passwords do not match")
            else:
                success, message = auth_manager.register_user(reg_user, reg_pass, reg_role)
                if success:
                    st.success(f"✅ {message}")
                    st.info("💡 Go to the **Login** tab to sign in with your new account.")
                else:
                    st.error(f"❌ {message}")

# -------------------------
# LOGIN TAB
# -------------------------
with tab_login:
    st.subheader("Login to Your Account")
    
    with st.form("login_form"):
        user = st.text_input("Username", key="login_user")
        pw = st.text_input("Password", type="password", key="login_pass")
        
        submitted = st.form_submit_button("Log in", type="primary")
        if submitted:
            user = user.strip()
            
            if not user:
                st.error("❌ Please enter username")
            elif not pw:
                st.error("❌ Please enter password")
            else:
                success, user_obj = auth_manager.authenticate_user(user, pw)
                if success and user_obj:
                    st.session_state.logged_in = True
                    st.session_state.username = user_obj.username
                    st.session_state.user_role = user_obj.role
                    st.success("✅ Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

st.markdown("---")
st.caption("💡 Multi-Domain Intelligence Platform - Authentication System")


