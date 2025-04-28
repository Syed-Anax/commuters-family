import streamlit as st
from utils.firebase_helper import save_user_profile
import requests
from streamlit_folium import st_folium
import folium
from streamlit_geocoder import geocoder

st.set_page_config(page_title="Commuters Family", layout="centered")
st.title("🚌 Commuters Family App")

# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None

# Navigation
menu = st.sidebar.radio("Navigate", ["Home", "Login", "Signup", "Dashboard"])

# Home Page
if menu == "Home":
    st.header("Welcome to Commuters Family App")
    st.markdown("🚀 Find your daily commuting partner with ease!")

# Login Page
if menu == "Login":
    st.subheader("🔐 Login with Mobile Number (Simulated)")
    phone = st.text_input("Enter Mobile Number (+92...)")

    if st.button("Send OTP"):
        if phone:
            st.success("✅ Simulated OTP sent: Use 123456")

    otp = st.text_input("Enter OTP")
    if st.button("Verify OTP"):
        if otp == "123456":
            st.session_state.user = phone
            st.success("✅ Login Successful!")
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("❌ Invalid OTP. Use 123456.")

# Signup Page
if menu == "Signup":
    st.subheader("📝 Signup with Mobile Number (Simulated)")
    phone = st.text_input("Enter Mobile Number (+92...) [Signup]")

    if st.button("Send OTP [Signup]"):
        if phone:
            st.success("✅ Simulated OTP sent: Use 123456")

    otp = st.text_input("Enter OTP [Signup]")
    if st.button("Verify OTP [Signup]"):
        if otp == "123456":
            st.session_state.user = phone
            st.success("✅ Signup Successful!")
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("❌ Invalid OTP. Use 123456.")

# Dashboard Page
if menu == "Dashboard" or st.session_state.page == "dashboard":
    if not st.session_state.user:
        st.warning("⚠️ Please login or signup first.")
    else:
        st.success(f"🎯 Welcome {st.session_state.user}!")

        st.subheader("👤 Complete Your Profile")

        role = st.radio("Role", ["Rider", "Passenger"])
        name = st.text_input("Full Name")
        gender = st.radio("Gender", ["Male", "Female"])
        cnic = st.text_input("CNIC Number (Optional)")

        st.subheader("📍 Set Home Location (Search)")
        home_location = geocoder("Enter Home Location")

        st.subheader("🏢 Set Destination Location (Search)")
        destination_location = geocoder("Enter Destination Location")

        morning_time = st.time_input("Morning Travel Time")
        evening_time = st.time_input("Evening Travel Time")

        travel_days = st.multiselect("Select Travel Days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        if st.button("Save Profile"):
            profile_data = {
                "phone_number": st.session_state.user,
                "name": name,
                "gender": gender,
                "cnic": cnic,
                "role": role,
                "home_location": home_location,
                "destination_location": destination_location,
                "morning_time": morning_time.strftime("%H:%M"),
                "evening_time": evening_time.strftime("%H:%M"),
                "travel_days": travel_days
            }
            save_user_profile(st.session_state.user, profile_data)
            st.success("✅ Profile saved successfully!")
