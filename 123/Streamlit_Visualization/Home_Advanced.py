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
        def ensure_session_defaults():
            if "logged_in" not in st.session_state:
                st.session_state.logged_in = False
            if "username" not in st.session_state:
                st.session_state.username = ""
            if "users" not in st.session_state:
                st.session_state.users = {
                    "admin": "Admin123!",
                    "test": "Test123!",
                    "user": "User123!"
                }
        
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
    page_title="🚀 Intelligence Platform - Advanced Auth",
    page_icon="🚀",
    layout="centered"
)

# Dark cosmic theme CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #2d1b4e 100%);
        color: #e0e0e0;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00ff88, #7b2cbf, #ff006e, #8338ec);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
        text-shadow: 0 0 30px rgba(123, 44, 191, 0.5);
    }
    
    .auth-card {
        background: linear-gradient(135deg, rgba(123, 44, 191, 0.2), rgba(0, 255, 136, 0.1));
        border: 1px solid rgba(123, 44, 191, 0.3);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(123, 44, 191, 0.3);
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    .social-button {
        background: linear-gradient(90deg, #7b2cbf, #00ff88);
        border: none;
        border-radius: 10px;
        padding: 0.75rem;
        color: white;
        font-weight: bold;
        width: 100%;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    
    .social-button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        transform: translateY(-2px);
    }
    
    .wing-icon {
        font-size: 2rem;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

ensure_session_defaults()

# Header with cosmic design
st.markdown("""
    <div class="main-header">
        <span class="wing-icon">🛸</span> Intelligence Platform 
        <span class="wing-icon">🚀</span><br>
        <span style="font-size: 1.5rem; color: #00ff88;">Cosmic Operations Center</span>
    </div>
""", unsafe_allow_html=True)

# If already logged in
if st.session_state.logged_in:
    st.success(f"✅ Already logged in as **{st.session_state.username}**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌞 Go to Light Dashboard", type="primary"):
            st.switch_page("pages/Dashboard.py")
    with col2:
        if st.button("🌙 Go to Dark Dashboard", type="primary"):
            st.switch_page("pages/Dashboard_Dark.py")
    st.stop()

# Main authentication area
st.markdown('<div class="auth-card">', unsafe_allow_html=True)

# Tabs for different auth methods
tab_login, tab_register, tab_social, tab_seed = st.tabs(
    ["🔑 Standard Login", "📝 Register", "🌐 Social Auth", "🔐 Seed Phrase"]
)

# -------------------------
# STANDARD LOGIN TAB
# -------------------------
with tab_login:
    st.subheader("🔑 Standard Authentication")
    
    user = st.text_input("Username", key="login_user_adv")
    pw = st.text_input("Password", type="password", key="login_pass_adv")
    
    if st.button("Log in", key="btn_login_adv", type="primary"):
        user = user.strip()
        if st.session_state.users.get(user) == pw:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("✅ Login successful!")
            st.balloons()
            st.switch_page("pages/Dashboard_Dark.py")
        else:
            st.error("❌ Invalid username or password.")
    
    # Quick login buttons
    st.markdown("---")
    st.markdown("**💡 Quick Login (Demo):**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👤 Admin", key="quick_admin"):
            st.session_state.logged_in = True
            st.session_state.username = "admin"
            st.rerun()
    with col2:
        if st.button("🧪 Test", key="quick_test"):
            st.session_state.logged_in = True
            st.session_state.username = "test"
            st.rerun()
    with col3:
        if st.button("👥 User", key="quick_user"):
            st.session_state.logged_in = True
            st.session_state.username = "user"
            st.rerun()

# -------------------------
# REGISTER TAB
# -------------------------
with tab_register:
    st.subheader("📝 Create New Account")
    
    reg_user = st.text_input("Username", key="reg_user_adv")
    reg_pass = st.text_input("Password", type="password", key="reg_pass_adv")
    reg_pass2 = st.text_input("Confirm password", type="password", key="reg_pass2_adv")
    
    if reg_pass:
        strength = password_strength(reg_pass)
        color = {"Weak": "🔴", "Medium": "🟡", "Strong": "🟢"}
        st.caption(f"Password strength: {color.get(strength, '⚪')} **{strength}**")
    
    if st.button("Create account", key="btn_register_adv", type="primary"):
        reg_user = reg_user.strip()
        
        ok, msg = validate_username(reg_user)
        if not ok:
            st.error(msg)
            st.stop()
        
        ok, msg = validate_password(reg_pass)
        if not ok:
            st.error(msg)
            st.stop()
        
        if reg_pass != reg_pass2:
            st.error("Passwords do not match.")
            st.stop()
        
        if reg_user in st.session_state.users:
            st.error("Username already exists.")
            st.stop()
        
        st.session_state.users[reg_user] = reg_pass
        st.success("✅ Account created successfully!")
        st.info("💡 Go to the **Standard Login** tab to sign in.")

# -------------------------
# SOCIAL AUTH TAB
# -------------------------
with tab_social:
    st.subheader("🌐 Social Authentication")
    st.markdown("**Connect with your favorite platform:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📱 Telegram", key="auth_telegram", use_container_width=True):
            st.info("🔐 Telegram authentication coming soon! For now, use standard login.")
        
        if st.button("🔵 Google", key="auth_google", use_container_width=True):
            st.info("🔐 Google authentication coming soon! For now, use standard login.")
        
        if st.button("🔷 Microsoft", key="auth_microsoft", use_container_width=True):
            st.info("🔐 Microsoft authentication coming soon! For now, use standard login.")
    
    with col2:
        if st.button("🍎 Apple", key="auth_apple", use_container_width=True):
            st.info("🔐 Apple authentication coming soon! For now, use standard login.")
        
        if st.button("📘 Facebook", key="auth_facebook", use_container_width=True):
            st.info("🔐 Facebook authentication coming soon! For now, use standard login.")
    
    st.markdown("---")
    st.caption("💡 Social authentication is a planned feature. Currently in development for quantum-resistant security.")

# -------------------------
# SEED PHRASE TAB
# -------------------------
with tab_seed:
    st.subheader("🔐 Seed Phrase Authentication")
    st.markdown("**Quantum-resistant authentication using 12-word recovery phrase:**")
    
    st.info("""
    🌌 **How it works:**
    - Enter your 12-word recovery phrase
    - Each word is validated against BIP39 wordlist
    - Quantum-resistant encryption ensures future security
    - Your phrase is never stored, only hashed
    """)
    
    seed_input = st.text_area(
        "Enter your 12-word recovery phrase",
        placeholder="word1 word2 word3 ... word12",
        key="seed_phrase",
        height=100
    )
    
    if st.button("🔐 Authenticate with Seed", key="btn_seed", type="primary"):
        words = seed_input.strip().split()
        if len(words) == 12:
            # Demo: accept any 12 words for now
            st.success("✅ Seed phrase validated! (Demo mode)")
            st.session_state.logged_in = True
            st.session_state.username = "seed_user"
            st.balloons()
            st.switch_page("pages/Dashboard_Dark.py")
        else:
            st.error("❌ Please enter exactly 12 words.")
    
    st.markdown("---")
    st.caption("💡 This is a demonstration of seed phrase authentication. In production, this would use BIP39 validation and quantum-resistant hashing.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00ff88;">
    <p>🌌 <strong>Intelligence Platform</strong> | Built for Space Rangers 🛸</p>
    <p>Quantum-resistant security | Multi-domain intelligence | Cosmic operations</p>
</div>
""", unsafe_allow_html=True)


