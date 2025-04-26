import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_secrets = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

# Streamlit page setup
st.set_page_config(page_title="Commuters Family", layout="centered")
st.title("🚌 Commuters Family App")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Signup", "Login", "Dashboard"])

# Session state to track logged-in user
if "user" not in st.session_state:
    st.session_state.user = None

# --- Signup ---
if menu == "Signup":
    st.subheader("🔐 Create New Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Signup"):
        if email and password:
            try:
                user = auth.create_user(
                    email=email,
                    password=password
                )
                st.success("✅ Signup successful! Please login now.")
            except Exception as e:
                st.error(f"❌ Signup failed: {e}")
        else:
            st.warning("⚠️ Please fill in both fields.")

# --- Login ---
elif menu == "Login":
    st.subheader("🔑 Login to Your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login"):
        if email and password:
            try:
                user = auth.get_user_by_email(email)
                st.session_state.user = user.uid
                st.success("✅ Login successful!")
            except Exception as e:
                st.error(f"❌ Login failed: {e}")
        else:
            st.warning("⚠️ Please enter your credentials.")

# --- Dashboard ---
elif menu == "Dashboard":
    if not st.session_state.user:
        st.warning("⚠️ Please login first to access the dashboard.")
    else:
        st.success("🎯 Welcome to your Dashboard!")
        st.write("🚀 More features coming soon...")
