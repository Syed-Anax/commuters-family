import streamlit as st
import os

def show_splash_screens():
    st.markdown("<h2 style='text-align: center;'>Commuters Family App 🇵🇰</h2>", unsafe_allow_html=True)

    # ✅ Updated splash screen paths
    splash_images = [f"images/splash{i}.png" for i in range(1, 8)]

    if 'splash_index' not in st.session_state:
        st.session_state.splash_index = 0

    current_image = splash_images[st.session_state.splash_index]

    # ✅ Check image existence
    if os.path.exists(current_image):
        st.image(current_image, use_container_width=True)
    else:
        st.warning(f"⚠️ Image not found: {current_image}")
        return  # stop rerun if image missing

    # ✅ Next button logic
    if st.button("Next ➡️"):
        if st.session_state.splash_index < len(splash_images) - 1:
            st.session_state.splash_index += 1
            st.experimental_rerun()
        else:
            st.session_state.page = 'auth'
            st.experimental_rerun()
