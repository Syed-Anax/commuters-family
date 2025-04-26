import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

st.title("🚌 Commuters Family App")

menu = st.sidebar.selectbox("Menu", ["Signup", "Login", "Dashboard"])

if "user" not in st.session_state:
    st.session_state.user = None

# Signup
if menu == "Signup":
    st.subheader("Create New Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        try:
            user = auth.create_user(email=email, password=password)
            st.success("Signup successful! Please login now.")
        except Exception as e:
            st.error(f"Signup error: {e}")

# Login
elif menu == "Login":
    st.subheader("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email)
            st.session_state.user = user.uid
            st.success("Login successful!")
        except Exception as e:
            st.error(f"Login error: {e}")

# Dashboard
elif menu == "Dashboard":
    if not st.session_state.user:
        st.warning("Please login first.")
    else:
        st.success("Welcome to your Dashboard!")
