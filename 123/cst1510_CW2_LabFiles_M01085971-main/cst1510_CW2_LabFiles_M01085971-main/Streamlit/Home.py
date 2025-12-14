import streamlit as st
from auth import (
    ensure_session_defaults,
    validate_username,
    validate_password,
    password_strength
)

st.set_page_config(page_title="Welcome", page_icon="🔐", layout="centered")
ensure_session_defaults()

st.title("🔐 Welcome")

tab_login, tab_register = st.tabs(["Login", "Register"])

# -------------------------
# REGISTER
# -------------------------
with tab_register:
    st.subheader("Register")

    reg_user = st.text_input("Username", key="reg_user")
    reg_pass = st.text_input("Password", type="password", key="reg_pass")
    reg_pass2 = st.text_input("Confirm password", type="password", key="reg_pass2")

    if reg_pass:
        st.caption(f"Password strength: **{password_strength(reg_pass)}**")

    if st.button("Create account", key="btn_register"):
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

        # save user (Week 9 demo storage)
        st.session_state.users[reg_user] = reg_pass
        st.success("Account created ✅ Now go to Login tab.")

# -------------------------
# LOGIN
# -------------------------
with tab_login:
    st.subheader("Login")

    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log in", key="btn_login"):
        user = user.strip()
        if st.session_state.users.get(user) == pw:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("Logged in ✅")
            st.switch_page("pages/CyberIncidents.py")
        else:
            st.error("Invalid username or password.")
