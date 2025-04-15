import streamlit as st
from PIL import Image

def show_splash_screens():
    splash_images = [
        "images/splash1.png",
        "images/splash2.png",
        "images/splash3.png",
        "images/splash4.png",
        "images/splash5.png",
        "images/splash6.png",
        "images/splash7.png",
    ]

    # Session state initialization
    if 'splash_index' not in st.session_state:
        st.session_state.splash_index = 0

    if st.session_state.splash_index < len(splash_images):
        current_image = splash_images[st.session_state.splash_index]
        st.image(current_image, use_container_width=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next"):
                st.session_state.splash_index += 1
                st.experimental_rerun()

    else:
        st.session_state.page = "auth"  # Move to login/signup
        st.experimental_rerun()
