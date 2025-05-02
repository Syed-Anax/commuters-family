from utils.firebase_helper import get_user_profile, upgrade_to_premium, check_if_premium
from utils.alert_helper import get_today_alert
from utils.firebase_helper import get_user_profile
# app.py (with auto-navigation + match-based dashboard + connect button + free limit)
import streamlit as st
from utils.firebase_helper import save_user_profile, get_user_profile
from utils.matching_helper import get_matches
from firebase_admin import firestore
from datetime import datetime

st.set_page_config(page_title="Commuters Family", layout="centered")
st.title("🚌 Commuters Family App")

db = firestore.client()

# Session State
if "page" not in st.session_state:
    st.session_state.page = "start"
if "user" not in st.session_state:
    st.session_state.user = None

# Check if profile already exists
def profile_exists(phone):
    return db.collection("users").document(phone).get().exists

# ------------------------------
# PAGE FLOW START
# ------------------------------
if st.session_state.page == "start":
    st.header("Welcome to Commuters Family App! 🚀")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Signup"):
            st.session_state.page = "signup"
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"

if st.session_state.page == "signup":
    st.subheader("📝 Signup with Mobile Number (Simulated)")
    phone = st.text_input("Enter Mobile Number (+92...) [Signup]")
    if st.button("Send OTP [Signup]"):
        if phone:
            st.session_state.temp_phone = phone
            st.success("✅ Simulated OTP sent! Use 123456")
            st.session_state.page = "verify_signup"

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

if st.session_state.page == "login":
    st.subheader("🔐 Login with Mobile Number (Simulated)")
    phone = st.text_input("Enter Mobile Number (+92...) [Login]")
    if st.button("Send OTP [Login]"):
        if phone:
            st.session_state.temp_phone = phone
            st.success("✅ Simulated OTP sent! Use 123456")
            st.session_state.page = "verify_login"

if st.session_state.page == "verify_login":
    st.subheader("🔐 Verify OTP for Login")
    otp = st.text_input("Enter OTP [Login]")
    if st.button("Verify OTP [Login]"):
        if otp == "123456":
            st.session_state.user = st.session_state.temp_phone
            st.success("✅ Login Successful!")
            # Check profile
            if profile_exists(st.session_state.user):
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "profile"
        else:
            st.error("❌ Invalid OTP. Please enter 123456.")

if st.session_state.page == "profile" and st.session_state.user:
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

if st.session_state.page == "dashboard" and st.session_state.user:
    st.header("🌟 Your Matches")
    profile = get_user_profile(st.session_state.user)
    matches = get_matches(profile)

    # Contact Unlock System
    if "unlocked_matches" not in st.session_state:
        st.session_state.unlocked_matches = []
    if "unlocked_count" not in st.session_state:
        st.session_state.unlocked_count = 0
    MAX_FREE_UNLOCKS = 3

    if matches:
        for match in matches:
            st.info(f"👤 {match['name']} ({match['role']})")
            st.write(f"📍 {match['home_location']} ➡ {match['destination_location']}")
            st.write(f"🕒 {match['morning_time']} - {match['evening_time']}")
            st.write(f"📅 Days: {', '.join(match['travel_days'])}")

            if match["phone_number"] in st.session_state.unlocked_matches:
                st.success(f"📞 Contact: {match['phone_number']}")
            elif st.button(f"Connect with {match['name']}", key=match['phone_number']):
                if is_premium or st.session_state.unlocked_count < MAX_FREE_UNLOCKS:
                    st.session_state.unlocked_matches.append(match["phone_number"])
                    st.session_state.unlocked_count += 1
                    st.success(f"📞 Contact Unlocked: {match['phone_number']}")
                else:
                    st.warning("🔐 Match limit reached. Please upgrade your plan to unlock more contacts.")
            st.markdown("---")
    else:
        st.warning("No matching users found right now. Try updating your profile.")

    if st.button("Logout"):
        st.session_state.page = "start"
        st.session_state.user = None
user_profile = get_user_profile(st.session_state.user)
if user_profile:
    st.subheader("🔔 Today's Travel Alert")
    alert = get_today_alert(user_profile)
    st.info(alert)
is_premium = check_if_premium(st.session_state.user)
if not is_premium:
    if st.button("🚀 Upgrade to Premium (PKR 500) [Demo Mode]"):
        upgrade_to_premium(st.session_state.user)
        st.success("✅ You are now a Premium Member! Unlimited matches unlocked.")
        st.rerun()
