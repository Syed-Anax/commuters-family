# carpool_app/splash_screens.py
import streamlit as st
from PIL import Image
import os

def show_splash_screens():
    splash_images = [f"images/splash{i}.png" for i in range(1, 8)]

    if 'splash_index' not in st.session_state:
        st.session_state.splash_index = 0

    if st.session_state.splash_index < len(splash_images):
        current_image = splash_images[st.session_state.splash_index]
        
        # Check image file exists
        if os.path.exists(current_image):
            image = Image.open(current_image)
            st.image(image, use_container_width=True)
        else:
            st.error(f"❌ Image not found: {current_image}")
            return

        if st.button("Next"):
            st.session_state.splash_index += 1
            st.rerun()
    else:
        st.session_state.page = "auth"
        st.rerun()
