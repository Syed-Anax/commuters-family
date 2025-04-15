# login_signup.py

import streamlit as st
import pyrebase
from carpool_app.firebase_config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def show_login_signup():
    st.set_page_config(page_title="Login / Signup - Commuters Family")

    choice = st.sidebar.selectbox("Login / Signup", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Create Account"):
            if password == confirm_password:
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success("Account created successfully!")
                except Exception as e:
                    st.error("Error creating account. " + str(e))
            else:
                st.warning("Passwords do not match.")

    else:
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success("Logged in successfully!")
                # st.experimental_set_query_params(page="home")  # later
            except Exception as e:
                st.error("Login failed. " + str(e))

if __name__ == "__main__":
    show_login_signup()
# login_signup.py

import streamlit as st

def login_signup():
    st.title("Login or Signup")
    st.write("This is a placeholder login/signup page.")
