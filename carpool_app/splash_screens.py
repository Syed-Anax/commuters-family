import streamlit as st
import os

def show_splash_screens():
    # List of splash screen image paths (inside carpool_app/images folder)
    splash_images = [
    "carpool_app/images/splash1.png",
    "carpool_app/images/splash2.png",
    "carpool_app/images/splash3.png",
    "carpool_app/images/splash4.png",
    "carpool_app/images/splash5.png",
    "carpool_app/images/splash6.png",
    "carpool_app/images/splash7.png",
]
    ]

    if 'splash_index' not in st.session_state:
        st.session_state.splash_index = 0

    current_index = st.session_state.splash_index
    current_image = splash_images[current_index]

    # ✅ Check if image file exists
    if os.path.exists(current_image):
        st.image(current_image, use_container_width=True)
    else:
        st.warning(f"Image not found: {current_image}")

    # Next button
    if st.button("Next ➡"):
        if current_index < len(splash_images) - 1:
            st.session_state.splash_index += 1
            st.experimental_rerun()
        else:
            st.session_state.page = 'auth'
            st.experimental_rerun()
