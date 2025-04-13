# homepage.py
import streamlit as st
from PIL import Image

def show_homepage():
    st.set_page_config(page_title="Commuters Family Home", page_icon="🏠", layout="centered")

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

    st.markdown("<h2 style='text-align: center;'>Welcome to Commuters Family 🚗🇵🇰</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.success("You're successfully logged in! 🎉")

    st.markdown("#### Features Available:")
    st.write("""
    - Search nearby commuters
    - Match with daily travelers
    - Share travel cost & fuel
    - Secure rides with trusted users
    - Live traffic route notifications
    - Free fuel calculator
    - Female to Female matches (for extra safety)
    """)

# If you want to test directly:
if __name__ == "__main__":
    show_homepage()
