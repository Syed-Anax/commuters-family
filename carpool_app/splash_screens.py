# carpool_app/splash_screens.py

import streamlit as st
from PIL import Image
import os

def show_splash_screens():
    splash_images = [
        "carpool_app/images/splash1.png",
        "carpool_app/images/splash2.png",
        "carpool_app/images/splash3.png",
        "carpool_app/images/splash4.png",
        "carpool_app/images/splash5.png",
        "carpool_app/images/splash6.png",
        "carpool_app/images/splash7.png",
    ]

    if "splash_index" not in st.session_state:
        st.session_state.splash_index = 0

    current_image = splash_images[st.session_state.splash_index]

    if os.path.exists(current_image):
        image = Image.open(current_image)
        st.image(image, use_container_width=True)
    else:
        st.error(f"❌ Image not found: {current_image}")

    if st.session_state.splash_index < len(splash_images) - 1:
        if st.button("Next"):
            st.session_state.splash_index += 1
            st.experimental_rerun()
    else:
        if st.button("Get Started"):
            st.session_state.page = "auth"
            del st.session_state.splash_index
            st.experimental_rerun()
