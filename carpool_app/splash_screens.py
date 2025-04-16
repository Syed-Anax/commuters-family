# carpool_app/splash_screens.py
import streamlit as st
from PIL import Image
import os

def show_splash_screens():
    if 'splash_index' not in st.session_state:
        st.session_state.splash_index = 1

    total_splashes = 7
    current_index = st.session_state.splash_index
    image_path = f"images/splash{current_index}.png"

    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, use_container_width=True)
    else:
        st.warning(f"Image not found: {image_path}")

    if current_index < total_splashes:
        if st.button("Next ➡️"):
            st.session_state.splash_index += 1
            st.experimental_rerun()
    else:
        st.session_state.page = 'auth'
        st.experimental_rerun()
