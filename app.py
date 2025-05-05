import streamlit as st
from utils.firebase_helper import (
    save_user_profile,
    get_user_profile,
    upgrade_to_premium,
    check_if_premium,
)
from utils.matching_helper import get_matches
from utils.chat_helper import get_messages, send_message
from utils.notification_helper import get_travel_alert

st.set_page_config(page_title="Commuters Family", layout="centered")

# Session setup
if "page" not in st.session_state:
    st.session_state.page = "start"
if "user" not in st.session_state:
    st.session_state.user = None
if "unlocked_matches" not in st.session_state:
    st.session_state.unlocked_matches = []
if "unlocked_count" not in st.session_state:
    st.session_state.unlocked_count = 0
MAX_FREE_UNLOCKS = 3

# Start page
if st.session_state.page == "start":
    st.title("🚌 Commuters Family App")
    st.subheader("Match with daily commuters like you!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Signup"):
            st.session_state.page = "signup"
    with col2:
        if st.button("🔐 Login"):
            st.session_state.page = "login"

# Signup page
if st.session_state.page == "signup":
    st.subheader("📝 Signup")
    phone = st.text_input("Enter Mobile Number (+92...)")
    if st.button("Send OTP [Signup]"):
        if phone:
            st.session_state.temp_phone = phone
            st.success("✅ Simulated OTP sent. Use 123456.")
            st.session_state.page = "verify_signup"

# Signup OTP
if st.session_state.page == "verify_signup":
    otp = st.text_input("Enter OTP [Signup]")
    if st.button("Verify OTP [Signup]"):
        if otp == "123456":
            st.session_state.user = st.session_state.temp_phone
            st.success("✅ Signup Successful!")
            if get_user_profile(st.session_state.user):
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "profile"
        else:
            st.error("❌ Invalid OTP. Use 123456.")

# Login page
if st.session_state.page == "login":
    st.subheader("🔐 Login")
    phone = st.text_input("Enter Mobile Number (+92...)")
    if st.button("Send OTP [Login]"):
        if phone:
            st.session_state.temp_phone = phone
            st.success("✅ Simulated OTP sent. Use 123456.")
            st.session_state.page = "verify_login"

# Login OTP
if st.session_state.page == "verify_login":
    otp = st.text_input("Enter OTP [Login]")
    if st.button("Verify OTP [Login]"):
        if otp == "123456":
            st.session_state.user = st.session_state.temp_phone
            st.success("✅ Login Successful!")
            if get_user_profile(st.session_state.user):
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "profile"
        else:
            st.error("❌ Invalid OTP. Use 123456.")

# Profile form
if st.session_state.page == "profile" and st.session_state.user:
    st.subheader("👤 Complete Your Profile")

    role = st.radio("Role", ["Rider", "Passenger"])
    name = st.text_input("Full Name")
    email = st.text_input("Email Address (required for notifications)")
    gender = st.radio("Gender", ["Male", "Female"])
    cnic = st.text_input("CNIC Number (Optional)")

    home_location = st.text_input("Home Location (e.g., Gulshan)")
    destination_location = st.text_input("Destination Location (e.g., Saddar)")

    morning_time = st.time_input("Morning Travel Time")
    evening_time = st.time_input("Evening Travel Time")

    travel_days = st.multiselect(
        "Select Travel Days",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    )

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
            "travel_days": travel_days,
        }
        save_user_profile(st.session_state.user, profile_data)
        st.success("✅ Profile Saved!")
        st.session_state.page = "dashboard"
        if not name or not home_location or not destination_location or not travel_days or not email:
    st.error("❌ Please fill all required fields including email.")
else:
    profile_data = {
        "phone_number": st.session_state.user,
        "name": name,
        "email": email,
        "gender": gender,
        "cnic": cnic,
        "role": role,
        "home_location": home_location,
        "destination_location": destination_location,
        "morning_time": morning_time.strftime("%H:%M"),
        "evening_time": evening_time.strftime("%H:%M"),
        "travel_days": travel_days,
    }
    save_user_profile(st.session_state.user, profile_data)
    st.success("✅ Profile Saved!")
    st.session_state.page = "dashboard"
else:
    # save the profile
# Dashboard
if st.session_state.page == "dashboard" and st.session_state.user:
    st.subheader("🎯 Dashboard")

    # Load user profile
    user_profile = get_user_profile(st.session_state.user)
    if not user_profile:
        st.warning("⚠️ Profile not found.")
    else:
        # 🚨 Travel Alert
        alert = None
        alert = get_travel_alert(user_profile)
        if alert:
            st.info(alert)

        # 👑 Premium Check
        is_premium = check_if_premium(st.session_state.user)

        if not is_premium:
            if st.button("🚀 Upgrade to Premium (PKR 500) [Simulated]"):
                upgrade_to_premium(st.session_state.user)
                st.success("✅ You are now a Premium Member!")
                st.rerun()

        # 🧠 Find Matches
        matches = get_matches(user_profile)

        if matches:
            st.success(f"✅ {len(matches)} matches found!")
            for match in matches:
                with st.expander(f"👤 {match['name']} | {match['role']} | {match['gender']}"):
                    st.write(f"📍 {match['home_location']} ➡ {match['destination_location']}")
                    st.write(f"🕒 {match['morning_time']} / {match['evening_time']}")
                    st.write(f"📅 Days: {', '.join(match['travel_days'])}")

                    # 🔐 Unlock contact logic
                    if match["phone_number"] in st.session_state.unlocked_matches or is_premium:
                        st.success(f"📞 Contact: {match['phone_number']}")
                    elif st.button(f"Connect with {match['name']}", key=match["phone_number"]):
                        if is_premium or st.session_state.unlocked_count < MAX_FREE_UNLOCKS:
                            st.session_state.unlocked_matches.append(match["phone_number"])
                            st.session_state.unlocked_count += 1
                            st.success(f"📞 Contact Unlocked: {match['phone_number']}")
                        else:
                            st.warning("🔐 Free match limit reached. Upgrade to unlock more.")

                    # 💬 Chat
                    if match["phone_number"] in st.session_state.unlocked_matches or is_premium:
                        with st.expander(f"💬 Chat with {match['name']}"):
                            messages = get_messages(
                                st.session_state.user, match["phone_number"]
                            )
                            for msg in messages:
                                st.write(f"🗨️ {msg['from']}: {msg['text']}")
                            new_msg = st.text_input(
                                f"Message to {match['name']}",
                                key=f"msg_{match['phone_number']}",
                            )
                            if st.button(f"Send to {match['name']}", key=f"send_{match['phone_number']}"):
                                if new_msg.strip() != "":
                                    send_message(
                                        st.session_state.user,
                                        match["phone_number"],
                                        new_msg,
                                    )
                                    st.success("✅ Message sent!")
                                    st.rerun()
        else:
            st.warning("😕 No matches found right now. Try updating your schedule or location.")

        # 🔚 Logout
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.page = "start"
            st.session_state.user = None
            st.session_state.unlocked_matches = []
            st.session_state.unlocked_count = 0
            st.experimental_rerun()
# Profile form
if st.session_state.page == "profile" and st.session_state.user:
    if not name or not home_location or not destination_location or not travel_days or not email:
    st.error("❌ Please fill all required fields including email.")
else:
    profile_data = {
        "phone_number": st.session_state.user,
        "name": name,
        "email": email,
        ...
