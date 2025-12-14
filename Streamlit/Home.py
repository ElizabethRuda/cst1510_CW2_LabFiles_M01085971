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
            
            # Всегда добавляем тестовых пользователей, если их нет
            default_users = {
                "admin": "Admin123!",
                "test": "Test123!",
                "user": "User123!"
            }
            
            # Добавляем тестовых пользователей, если их еще нет
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
    
    # Кнопка для инициализации тестовых пользователей (если их нет)
    if not st.session_state.users or len(st.session_state.users) == 0:
        st.warning("⚠️ Тестовые пользователи не инициализированы.")
        if st.button("🔧 Инициализировать тестовых пользователей", type="secondary"):
            st.session_state.users = {
                "admin": "Admin123!",
                "test": "Test123!",
                "user": "User123!"
            }
            st.success("✅ Тестовые пользователи инициализированы!")
            st.rerun()
    
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pass")
    
    # Показываем подсказку с тестовыми аккаунтами
    with st.expander("💡 Тестовые аккаунты"):
        st.markdown("""
        | Логин | Пароль |
        |-------|--------|
        | `admin` | `Admin123!` |
        | `test` | `Test123!` |
        | `user` | `User123!` |
        """)
    
    if st.button("Log in", key="btn_login", type="primary"):
        user = user.strip()
        
        # Проверка наличия пользователей
        if not st.session_state.users:
            st.error("❌ Нет зарегистрированных пользователей. Используйте кнопку выше для инициализации.")
            st.stop()
        
        # Проверка логина
        if not user:
            st.error("❌ Введите логин")
            st.stop()
        
        # Проверка пароля
        if not pw:
            st.error("❌ Введите пароль")
            st.stop()
        
        # Проверка учетных данных
        stored_password = st.session_state.users.get(user)
        if stored_password and stored_password == pw:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("✅ Login successful!")
            st.balloons()
            st.switch_page("pages/Dashboard.py")
        else:
            st.error("❌ Invalid username or password.")
            st.info(f"💡 Доступные пользователи: {', '.join(st.session_state.users.keys())}")

# Footer
st.markdown("---")

# Показываем информацию о пользователях
if st.session_state.users:
    user_list = ', '.join(st.session_state.users.keys())
    st.info(f"💡 **Доступные аккаунты:** {user_list}")
    with st.expander("🔐 Тестовые учетные данные"):
        st.markdown("""
        | Логин | Пароль |
        |-------|--------|
        | `admin` | `Admin123!` |
        | `test` | `Test123!` |
        | `user` | `User123!` |
        """)
else:
    st.warning("⚠️ Тестовые пользователи не инициализированы. Перезапустите приложение или используйте кнопку инициализации.")

# Link to advanced version
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**🚀 Advanced Version:**")
    if st.button("🌌 Go to Advanced Auth", use_container_width=True):
        st.switch_page("Home_Advanced.py")
with col2:
    st.markdown("**📊 Dashboard Versions:**")
    if st.button("🌙 Dark Mode", use_container_width=True):
        if st.session_state.logged_in:
            st.switch_page("pages/Dashboard_Dark.py")
        else:
            st.warning("Please login first!")

st.caption("💡 This is a demo authentication system. For production, use database-backed authentication.")

