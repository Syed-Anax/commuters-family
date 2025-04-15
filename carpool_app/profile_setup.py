# profile_setup.py

import streamlit as st
import pyrebase
from carpool_app.firebase_config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

def profile_setup():
    st.set_page_config(page_title="Profile Setup - Commuters Family")
    st.title("Create Your Profile")

    profile_type = st.radio("Select your role:", ["🚗 Rider", "🧍 Passenger"])

    # 🔹 Travel Schedule Section
    st.subheader("🕒 Daily Travel Schedule")
    morning_time = st.time_input("🌅 Morning Travel Time")
    evening_time = st.time_input("🌇 Evening Travel Time")

    st.markdown("📅 Select your travel days:")
    days_selected = st.multiselect(
        "Days",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )

    # 🔹 Travel Route
    st.subheader("🛣️ Your Daily Travel Route")
    home_location = st.text_input("🏠 Enter your home location")
    pickup_point = st.text_input("📍 Enter your **famous pickup point** (e.g. McDonald's, Gulshan Chowrangi)")
    destination = st.text_input("🎯 Enter your destination location")
    dropoff_point = st.text_input("🚏 Enter your **famous drop-off point** near destination")

    # 🔹 CNIC & Gender
    st.subheader("🆔 CNIC Verification")
    cnic_number = st.text_input("Enter your 13-digit CNIC number")

    gender = None
    if cnic_number and len(cnic_number) == 13 and cnic_number.isdigit():
        last_digit = int(cnic_number[-1])
        gender = "Female" if last_digit % 2 == 0 else "Male"
        st.info(f"Detected Gender: **{gender}**")
    else:
        gender = None

    # 🔹 Rider Form
    if profile_type == "🚗 Rider":
        st.subheader("🚘 Rider Vehicle Info")
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Bike", "Van", "Other"])
        make_model = st.text_input("Make & Model")
        engine_type = st.radio("Engine Type", ["Petrol", "Diesel", "Hybrid", "Electric"])
        ac_option = st.radio("AC Available?", ["Yes", "No"])

        vehicle_papers = st.file_uploader("Upload Vehicle Papers", type=["jpg", "jpeg", "png"])
        license = st.file_uploader("Upload Driving License", type=["jpg", "jpeg", "png"])
        rider_cnic_img = st.file_uploader("Upload CNIC Image", type=["jpg", "jpeg", "png"])

        if st.button("Save Rider Profile"):
            if cnic_number and gender and home_location and destination:
                rider_data = {
                    "email": st.session_state.get("email", "unknown@example.com"),
                    "role": "Rider",
                    "vehicle_type": vehicle_type,
                    "make_model": make_model,
                    "engine_type": engine_type,
                    "ac_option": ac_option,
                    "home_location": home_location,
                    "pickup_point": pickup_point,
                    "destination": destination,
                    "dropoff_point": dropoff_point,
                    "gender": gender,
                    "cnic": cnic_number,
                    "travel_days": days_selected,
                    "morning_time": str(morning_time),
                    "evening_time": str(evening_time)
                }
                db.child("users").child(rider_data["email"].replace(".", "_")).set(rider_data)
                st.success("✅ Rider profile saved to Firebase!")
            else:
                st.error("⚠️ Please complete all required fields.")

    # 🔹 Passenger Form
    else:
        st.subheader("🧍 Passenger Info")
        travel_purpose = st.text_input("Purpose of travel (e.g. Work, Study)")
        pax_cnic_img = st.file_uploader("Upload CNIC Image", type=["jpg", "jpeg", "png"])

        if st.button("Save Passenger Profile"):
            if cnic_number and gender and home_location and destination:
                pax_data = {
                    "email": st.session_state.get("email", "unknown@example.com"),
                    "role": "Passenger",
                    "travel_purpose": travel_purpose,
                    "home_location": home_location,
                    "pickup_point": pickup_point,
                    "destination": destination,
                    "dropoff_point": dropoff_point,
                    "gender": gender,
                    "cnic": cnic_number,
                    "travel_days": days_selected,
                    "morning_time": str(morning_time),
                    "evening_time": str(evening_time)
                }
                db.child("users").child(pax_data["email"].replace(".", "_")).set(pax_data)
                st.success("✅ Passenger profile saved to Firebase!")
            else:
                st.error("⚠️ Please complete all required fields.")

if __name__ == "__main__":
    profile_setup()
