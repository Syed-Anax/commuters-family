# splash_screens.py

import streamlit as st
import time
import os

def show_splash_screens():
    splash_folder = "carpool_app/images"
    
    slides = [
        "slide1.png",
        "slide2.png",
        "slide3.png",
        "slide4.png",
        "slide5.png",
        "slide6.png",
        "slide7.png"
    ]

    # Streamlit settings
    st.set_page_config(layout="centered", page_title="Commuters Family")

    if "splash_index" not in st.session_state:
        st.session_state.splash_index = 0

    current_slide = os.path.join(splash_folder, slides[st.session_state.splash_index])
    st.image(current_slide, use_column_width=True)

    col1, col2 = st.columns([1, 1])
    with col2:
        if st.session_state.splash_index < len(slides) - 1:
            if st.button("Next ➡️"):
                st.session_state.splash_index += 1
                st.experimental_rerun()
        else:
            if st.button("Get Started 🚀"):
                st.session_state.splash_index = 0
                st.switch_page("carpool_app/login_signup.py")  # adjust if different
