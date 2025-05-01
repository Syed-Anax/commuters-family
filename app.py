import streamlit as st
from utils.firebase_helper import save_user_profile

st.set_page_config(page_title="Commuters Family", layout="centered")
st.title("🚌 Commuters Family App")

# Session Setup
if "page" not in st.session_state:
    st.session_state.page = "start"
if "user" not in st.session_state:
    st.session_state.user = None

# ------------------------------
# PAGE FLOW START
# ------------------------------

# Start Page: Signup or Login options
if st.session_state.page == "start":
    st.header("Welcome to Commuters Family App! 🚀")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Signup"):
            st.session_state.page = "signup"
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"

# Signup Page
if st.session_state.page == "signup":
    st.subheader("📝 Signup with Mobile Number (Simulated)")
    phone = st.text_input("Enter Mobile Number (+92...) [Signup]")

    if st.button("Send OTP [Signup]"):
        if phone:
            st.session_state.temp_phone = phone
            st.success("✅ Simulated OTP sent! Use 123456")
            st.session_state.page = "verify_signup"

# Verify Signup OTP
if st.session_state.page == "verify_signup":
    st.subheader("🔐 Verify OTP for Signup")
    otp = st.text_input("Enter OTP [Signup]")

    if st.button("Verify OTP [Signup]"):
        if otp == "123456":
            st.session_state.user = st.session_state.temp_phone
            st.success("✅ Signup Successful!")
            st.session_state.page = "profile"
        else:
            st.error("❌ Invalid OTP. Please enter 123456.")

# Login Page
if st.session_state.page == "login":
    st.subheader("🔐 Login with Mobile Number (Simulated)")
    phone = st.text_input("Enter Mobile Number (+92...) [Login]")

    if st.button("Send OTP [Login]"):
        if phone:
            st.session_state.temp_phone = phone
            st.success("✅ Simulated OTP sent! Use 123456")
            st.session_state.page = "verify_login"

# Verify Login OTP
if st.session_state.page == "verify_login":
    st.subheader("🔐 Verify OTP for Login")
    otp = st.text_input("Enter OTP [Login]")

    if st.button("Verify OTP [Login]"):
        if otp == "123456":
            st.session_state.user = st.session_state.temp_phone
            st.success("✅ Login Successful!")
            st.session_state.page = "profile"
        else:
            st.error("❌ Invalid OTP. Please enter 123456.")

# Profile Completion Page
if st.session_state.page == "profile" and st.session_state.user:
    st.success(f"🎯 Welcome {st.session_state.user}!")
    st.subheader("👤 Complete Your Profile")

    role = st.radio("Role", ["Rider", "Passenger"])
    name = st.text_input("Full Name")
    gender = st.radio("Gender", ["Male", "Female"])
    cnic = st.text_input("CNIC Number (Optional)")

    home_location = st.text_input("Home Location (City or Area)")
    destination_location = st.text_input("Destination Location (City or Area)")

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
        st.success("✅ Profile Saved Successfully!")
        st.session_state.page = "dashboard"

# Dashboard Page
if st.session_state.page == "dashboard" and st.session_state.user:
    st.balloons()
    st.header("🎉 Dashboard")
    st.success("✅ You are now fully onboarded into Commuters Family App!")

    st.write("🚗 Start Finding your commute partners now...")
    if st.button("Logout"):
        st.session_state.page = "start"
        st.session_state.user = None
