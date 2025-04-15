import streamlit as st
from carpool_app.splash_screens import show_splash_screens
from carpool_app.login_signup import login_signup
from homepage import show_homepage

def main():
    # Session state initialize
    if 'page' not in st.session_state:
        st.session_state.page = 'splash'

    # Navigation logic
    if st.session_state.page == 'splash':
        show_splash_screens()
    elif st.session_state.page == 'auth':
        login_signup()
    elif st.session_state.page == 'home':
        show_homepage()

if __name__ == "__main__":
    main()
