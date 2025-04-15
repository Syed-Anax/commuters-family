# splash_screens.py
import streamlit as st
import os

def show_splash_screens():
    image_files = [
        "images/splash1.png",
        "images/splash2.png",
        "images/splash3.png",
        "images/splash4.png",
        "images/splash5.png",
        "images/splash6.png",
        "images/splash7.png"
    ]

    current_index = 0

    if "splash_index" not in st.session_state:
        st.session_state.splash_index = 0

    current_image = image_files[st.session_state.splash_index]

    # ✅ Safe image loading
    if os.path.exists(current_image):
        st.image(current_image, use_container_width=True)
    else:
        st.warning(f"Image not found: {current_image}")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.splash_index > 0:
            if st.button("⬅️ Back"):
                st.session_state.splash_index -= 1
                st.experimental_rerun()
    with col3:
        if st.session_state.splash_index < len(image_files) - 1:
            if st.button("Next ➡️"):
                st.session_state.splash_index += 1
                st.experimental_rerun()
        else:
            if st.button("Get Started"):
                st.session_state.show_signup = True
                st.session_state.splash_index = 0
                st.experimental_rerun()
