import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
from geopy.distance import geodesic
from streamlit_folium import st_folium
import folium
import uuid

def show_homepage():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    st.set_page_config(page_title="Commuters Family", layout="centered")
    st.title("🚌 Commuters Family App")

    menu = st.sidebar.selectbox("Menu", ["Signup", "Login", "Dashboard"])

    if "user" not in st.session_state:
        st.session_state.user = None

    if menu == "Signup":
        st.subheader("🔐 Create Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            try:
                user = auth.create_user(email=email, password=password)
                st.success("Signup successful! Please login.")
            except Exception as e:
                st.error(str(e))

    elif menu == "Login":
        st.subheader("🔑 Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.user = user.uid
                st.success("Login successful!")
            except Exception as e:
                st.error("Login failed.")

    elif menu == "Dashboard":
        if not st.session_state.user:
            st.warning("Please login first.")
            return

        st.success("Welcome to your Dashboard!")
        role = st.radio("I am a:", ["Rider", "Passenger"])
        cnic_number = st.text_input("Enter your 13-digit CNIC number")
        gender = ""
        if len(cnic_number) == 13 and cnic_number.isdigit():
            last_digit = int(cnic_number[-1])
            gender = "Female" if last_digit % 2 == 0 else "Male"
            st.success(f"Gender Detected: **{gender}**")
        elif cnic_number:
            st.error("CNIC must be 13 digits.")

        st.subheader("📍 Home Location")
        home_map = folium.Map(location=[24.8607, 67.0011], zoom_start=12)
        folium.LatLngPopup().add_to(home_map)
        home_result = st_folium(home_map, height=350, width=700)
        home_lat, home_lng = None, None
        if home_result["last_clicked"]:
            home_lat = home_result["last_clicked"]["lat"]
            home_lng = home_result["last_clicked"]["lng"]

        st.subheader("🏢 Destination Location")
        dest_map = folium.Map(location=[24.8600, 67.0100], zoom_start=12)
        folium.LatLngPopup().add_to(dest_map)
        dest_result = st_folium(dest_map, height=350, width=700)
        dest_lat, dest_lng = None, None
        if dest_result["last_clicked"]:
            dest_lat = dest_result["last_clicked"]["lat"]
            dest_lng = dest_result["last_clicked"]["lng"]

        morning_time = st.time_input("Morning Time")
        evening_time = st.time_input("Evening Time")
        days = st.multiselect("Travel Days", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

        cnic_front = st.file_uploader("CNIC Front", type=["jpg", "jpeg", "png", "pdf"])
        cnic_back = st.file_uploader("CNIC Back", type=["jpg", "jpeg", "png", "pdf"])

        vehicle_data = {}
        if role == "Rider":
            vehicle_data["type"] = st.selectbox("Vehicle Type", ["Bike", "Car"])
            vehicle_data["make_model"] = st.text_input("Make & Model")
            vehicle_data["engine_type"] = st.selectbox("Engine Type", ["Petrol", "Diesel", "Electric"])
            vehicle_data["ac_status"] = st.radio("AC or Non-AC", ["AC", "Non-AC"])
            license_front = st.file_uploader("License Front", type=["jpg", "jpeg", "png", "pdf"])
            license_back = st.file_uploader("License Back", type=["jpg", "jpeg", "png", "pdf"])
        else:
            license_front = None
            license_back = None

        if st.button("Save Profile"):
            if not all([home_lat, home_lng, dest_lat, dest_lng]):
                st.error("Select locations on map.")
            elif not cnic_number or gender == "":
                st.error("Enter valid CNIC.")
            else:
                user_data = {
                    "uid": st.session_state.user,
                    "role": role,
                    "gender": gender,
                    "cnic": cnic_number,
                    "home": [home_lat, home_lng],
                    "destination": [dest_lat, dest_lng],
                    "morning_time": morning_time.strftime("%H:%M"),
                    "evening_time": evening_time.strftime("%H:%M"),
                    "days": days,
                    "vehicle_info": vehicle_data if role == "Rider" else None,
                    "documents": {
                        "cnic_front": cnic_front.name if cnic_front else None,
                        "cnic_back": cnic_back.name if cnic_back else None,
                        "license_front": license_front.name if license_front else None,
                        "license_back": license_back.name if license_back else None
                    }
                }
                db.collection("users").document(str(uuid.uuid4())).set(user_data)
                st.success("Profile saved successfully!")
