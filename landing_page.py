# landing_page.py
import streamlit as st
from PIL import Image

def show_landing_page():
    st.set_page_config(page_title="Commuters Family", page_icon="🚗", layout="centered")

    st.markdown(
        """
        <style>
        body {
            background-color: #F5FFF5;
        }
        .main {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    logo = Image.open("images/logo.png")
    st.image(logo, width=150, use_container_width=False)

    st.markdown("<h1 style='text-align: center;'>Commuters Family 🚗🇵🇰</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Connecting neighbors with same routes for daily commute!</h4>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### About the App:")
    st.write("""
    Commuters Family app helps daily travelers to find carpool partners based on same route, timing, and days.  
    Save fuel, reduce cost, and meet friendly commuters! 🚗🤝
    """)

    if st.button("Get Started ➡️"):
        st.session_state.page = "onboarding"

# If you want to test directly:
if __name__ == "__main__":
    show_landing_page()
