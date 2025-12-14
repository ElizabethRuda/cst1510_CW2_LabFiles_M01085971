import streamlit as st
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import auth functions
try:
    from auth import (
        ensure_session_defaults,
        validate_username,
        validate_password,
        password_strength
    )
except ImportError:
    # Fallback if auth.py is in Streamlit folder
    STREAMLIT_DIR = Path(__file__).resolve().parent
    if (STREAMLIT_DIR / "auth.py").exists():
        sys.path.insert(0, str(STREAMLIT_DIR))
        from auth import (
            ensure_session_defaults,
            validate_username,
            validate_password,
            password_strength
        )
    else:
        # Simple fallback
        def ensure_session_defaults():
            if "logged_in" not in st.session_state:
                st.session_state.logged_in = False
            if "username" not in st.session_state:
                st.session_state.username = ""
            if "users" not in st.session_state:
                st.session_state.users = {}
            
            # Always add test users if they don't exist
            default_users = {
                "admin": "Admin123!",
                "test": "Test123!",
                "user": "User123!"
            }
            
            # Add test users if they are not already present
            for username, password in default_users.items():
                if username not in st.session_state.users:
                    st.session_state.users[username] = password
        
        def validate_username(username):
            if len(username) < 3 or len(username) > 20:
                return False, "Username must be between 3 and 20 characters."
            if not username.isalnum():
                return False, "Username must contain only letters and numbers."
            return True, ""
        
        def validate_password(password):
            if len(password) < 6 or len(password) > 50:
                return False, "Password must be between 6 and 50 characters."
            if not any(c.islower() for c in password):
                return False, "Password must include at least one lowercase letter."
            if not any(c.isupper() for c in password):
                return False, "Password must include at least one uppercase letter."
            if not any(c.isdigit() for c in password):
                return False, "Password must include at least one digit."
            special_chars = "!@#$%^&*()-_=+[]{};:,.<>?/\\|`~\"'"
            if not any(c in special_chars for c in password):
                return False, "Password must include at least one special character."
            return True, ""
        
        def password_strength(password):
            score = 0
            if len(password) >= 8: score += 1
            if len(password) >= 12: score += 1
            if any(c.islower() for c in password): score += 1
            if any(c.isupper() for c in password): score += 1
            if any(c.isdigit() for c in password): score += 1
            special_chars = "!@#$%^&*()-_=+[]{};:,.<>?/\\|`~\"'"
            if any(c in special_chars for c in password): score += 1
            if score <= 3:
                return "Weak"
            elif score <= 5:
                return "Medium"
            return "Strong"

st.set_page_config(
    page_title="Welcome - Intelligence Platform",
    page_icon="🔐",
    layout="centered"
)

ensure_session_defaults()

st.title("🔐 Intelligence Platform")
st.markdown("### Welcome to the Multi-Domain Intelligence Platform Dashboard")

# If already logged in, show option to go to dashboard
if st.session_state.logged_in:
    st.success(f"✅ Already logged in as **{st.session_state.username}**")
    if st.button("Go to Dashboard", type="primary"):
        st.switch_page("pages/Dashboard.py")
    st.stop()

# Tabs for Login and Register
tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

# -------------------------
# REGISTER TAB
# -------------------------
with tab_register:
    st.subheader("Create New Account")
    
    reg_user = st.text_input("Username", key="reg_user")
    reg_pass = st.text_input("Password", type="password", key="reg_pass")
    reg_pass2 = st.text_input("Confirm password", type="password", key="reg_pass2")
    
    if reg_pass:
        strength = password_strength(reg_pass)
        color = {"Weak": "🔴", "Medium": "🟡", "Strong": "🟢"}
        st.caption(f"Password strength: {color.get(strength, '⚪')} **{strength}**")
    
    if st.button("Create account", key="btn_register", type="primary"):
        reg_user = reg_user.strip()
        
        # Validate username
        ok, msg = validate_username(reg_user)
        if not ok:
            st.error(msg)
            st.stop()
        
        # Validate password
        ok, msg = validate_password(reg_pass)
        if not ok:
            st.error(msg)
            st.stop()
        
        # Check password match
        if reg_pass != reg_pass2:
            st.error("Passwords do not match.")
            st.stop()
        
        # Check if user exists
        if reg_user in st.session_state.users:
            st.error("Username already exists. Please choose another.")
            st.stop()
        
        # Save user (demo storage - in production use database)
        st.session_state.users[reg_user] = reg_pass
        st.success("✅ Account created successfully! You can now log in.")
        st.info("💡 Go to the **Login** tab to sign in with your new account.")

# -------------------------
# LOGIN TAB
# -------------------------
with tab_login:
    st.subheader("Login to Your Account")
    
    # Button to initialize test users (if they don't exist)
    if not st.session_state.users or len(st.session_state.users) == 0:
        st.warning("⚠️ Test users are not initialized.")
        if st.button("🔧 Initialize Test Users", type="secondary"):
            st.session_state.users = {
                "admin": "Admin123!",
                "test": "Test123!",
                "user": "User123!"
            }
            st.success("✅ Test users initialized!")
            st.rerun()
    
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pass")
    
    # Show test accounts hint
    with st.expander("💡 Test Accounts"):
        st.markdown("""
        | Username | Password |
        |----------|----------|
        | `admin` | `Admin123!` |
        | `test` | `Test123!` |
        | `user` | `User123!` |
        """)
    
    if st.button("Log in", key="btn_login", type="primary"):
        user = user.strip()
        
        # Check if users exist
        if not st.session_state.users:
            st.error("❌ No registered users. Use the button above to initialize.")
            st.stop()
        
        # Check username
        if not user:
            st.error("❌ Please enter username")
            st.stop()
        
        # Check password
        if not pw:
            st.error("❌ Please enter password")
            st.stop()
        
        # Verify credentials
        stored_password = st.session_state.users.get(user)
        if stored_password and stored_password == pw:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("✅ Login successful!")
            st.balloons()
            st.switch_page("pages/Dashboard.py")
        else:
            st.error("❌ Invalid username or password.")
            st.info(f"💡 Available users: {', '.join(st.session_state.users.keys())}")

# Footer
st.markdown("---")

# Show user information
if st.session_state.users:
    user_list = ', '.join(st.session_state.users.keys())
    st.info(f"💡 **Available accounts:** {user_list}")
    with st.expander("🔐 Test Credentials"):
        st.markdown("""
        | Username | Password |
        |----------|----------|
        | `admin` | `Admin123!` |
        | `test` | `Test123!` |
        | `user` | `User123!` |
        """)
else:
    st.warning("⚠️ Test users are not initialized. Restart the application or use the initialization button.")

# Link to advanced version
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    # Advanced version removed - using basic version only
    st.info("📊 Multi-Domain Intelligence Platform")
    
with col2:
    st.markdown("**📊 Dashboard:**")
    if st.button("📊 Go to Dashboard", use_container_width=True):
        if st.session_state.logged_in:
            st.switch_page("pages/Dashboard.py")
        else:
            st.warning("Please login first!")

st.caption("💡 This is a demo authentication system. For production, use database-backed authentication.")

