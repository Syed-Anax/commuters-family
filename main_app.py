import streamlit as st
from carpool_app.splash_screens import show_splash_screens
from carpool_app.login_signup import login_signup
from carpool_app.profile_setup import profile_setup
from carpool_app.homepage import show_homepage
from carpool_app.match_logic import match_logic

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'splash'

    if st.session_state.page == 'splash':
        show_splash_screens()
    elif st.session_state.page == 'auth':
        login_signup()
    elif st.session_state.page == 'setup':
        profile_setup()
    elif st.session_state.page == 'home':
        show_homepage()
    elif st.session_state.page == 'match':
        match_logic()

if __name__ == "__main__":
    main()
