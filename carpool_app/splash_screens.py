import streamlit as st
from PIL import Image
import os

def show_splash_screens():
    st.markdown("<h2 style='text-align: center;'>Welcome to Commuters Family 🚗</h2>", unsafe_allow_html=True)
    
    splash_images = [f"carpool_app/images/splash{i}.png" for i in range(1, 8)]

    current_index = st.session_state.get("splash_index", 0)

    if current_index < len(splash_images):
        current_image = splash_images[current_index]
        
        if os.path.exists(current_image):
            st.image(current_image, use_container_width=True)
        else:
            st.error(f"Image not found: {current_image}")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("Next ➡️"):
                st.session_state.splash_index = current_index + 1
                st.experimental_rerun()
    else:
        st.session_state.page = "auth"
        st.session_state.splash_index = 0
        st.experimental_rerun()
