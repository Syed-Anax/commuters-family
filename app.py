import streamlit as st
from utils.firebase_helper import firebase_auth, save_user_profile
from streamlit_folium import st_folium
import folium
import time

st.set_page_config(page_title="Commuters Family", layout="centered")

st.title("🚌 Commuters Family App")

menu = st.sidebar.selectbox("Menu", ["Signup/Login", "Dashboard"])

if "user" not in st.session_state:
    st.session_state.user = None

if menu == "Signup/Login":
    st.subheader("📱 Mobile Number Login")

    phone_number = st.text_input("Enter Mobile Number (with country code e.g. +92xxxxxxxxxx)")
    otp_sent = st.button("Send OTP")

    if otp_sent and phone_number:
        # Simulate OTP sent
        st.success("✅ OTP Sent Successfully! (Simulated) Enter '123456' as OTP.")

    otp_code = st.text_input("Enter OTP")
    verify = st.button("Verify OTP")

    if verify:
        if otp_code == "123456":
            st.success("✅ Phone Verified Successfully!")
            st.session_state.user = phone_number  # Simulate user UID
            st.experimental_rerun()
        else:
            st.error("❌ Invalid OTP. Try '123456'.")

elif menu == "Dashboard":
    if not st.session_state.user:
        st.warning("⚠️ Please login first.")
    else:
        st.success(f"🎯 Welcome {st.session_state.user}!")

        st.subheader("👤 Complete Your Profile")

        role = st.radio("Role", ["Rider", "Passenger"])
        name = st.text_input("Full Name")
        gender = st.radio("Gender", ["Male", "Female"])
        cnic = st.text_input("CNIC Number (Optional)")

        st.subheader("📍 Set Home Location")
        home_map = folium.Map(location=[24.8607, 67.0011], zoom_start=12)
        folium.LatLngPopup().add_to(home_map)
        home_result = st_folium(home_map, height=300, width=700)
        home_lat, home_lng = None, None
        if home_result and home_result.get("last_clicked"):
            home_lat = home_result["last_clicked"]["lat"]
            home_lng = home_result["last_clicked"]["lng"]

        st.subheader("🏢 Set Destination Location")
        dest_map = folium.Map(location=[24.8600, 67.0100], zoom_start=12)
        folium.LatLngPopup().add_to(dest_map)
        dest_result = st_folium(dest_map, height=300, width=700)
        dest_lat, dest_lng = None, None
        if dest_result and dest_result.get("last_clicked"):
            dest_lat = dest_result["last_clicked"]["lat"]
            dest_lng = dest_result["last_clicked"]["lng"]

        morning_time = st.time_input("Morning Travel Time")
        evening_time = st.time_input("Evening Travel Time")

        if st.button("Save Profile"):
            user_data = {
                "phone_number": st.session_state.user,
                "role": role,
                "name": name,
                "gender": gender,
                "cnic": cnic,
                "home": [home_lat, home_lng],
                "destination": [dest_lat, dest_lng],
                "morning_time": morning_time.strftime("%H:%M"),
                "evening_time": evening_time.strftime("%H:%M"),
            }
            save_user_profile(st.session_state.user, user_data)
            st.success("✅ Profile Saved Successfully!")
