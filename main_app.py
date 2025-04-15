# main_app.py

import os
import streamlit as st
from carpool_app.splash_screens import show_splash_screens
from carpool_app.login_signup import login_signup

# Add more imports as needed:
# from carpool_app.profile_setup import setup_profile
# from carpool_app.match_profiles import match_profiles
# from carpool_app.dashboard import show_dashboard (future)

def show_landing_page():
    logo_path = "images/logo.png"
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        st.warning("Logo not found!")

    st.markdown(
        "<h3 style='text-align: center;'>Welcome to Commuters Family App 🇵🇰</h3>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

def main():
    st.set_page_config(
        page_title="Commuters Family",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False

    # Show Landing + Splash Screens
    if not st.session_state.authenticated and not st.session_state.show_signup:
        show_landing_page()
        show_splash_screens()

    # Show Signup/Login form
    elif st.session_state.show_signup:
        login_signup()

    # After login
    elif st.session_state.authenticated:
        st.success("🎉 You are logged in successfully!")
        # You can call: setup_profile() or match_profiles() here
        # Example: setup_profile()
        st.info("👷 Dashboard or next features coming soon...")

if __name__ == "__main__":
    main()
