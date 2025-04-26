import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Commuters Family", layout="centered")
st.title("🚌 Commuters Family App")

if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.selectbox("Menu", ["Signup/Login", "Dashboard"])

# Mobile Number Authentication Flow
if menu == "Signup/Login":
    st.subheader("📱 Mobile Number Login")

    phone_number = st.text_input("Enter Mobile Number (with +92 format)")

    if st.button("Send OTP"):
        if phone_number:
            st.success("✅ Simulated OTP sent: Enter '123456' to verify!")

    otp = st.text_input("Enter OTP Code")
    if st.button("Verify OTP"):
        if otp == "123456":
            st.session_state.user = phone_number
            st.success("✅ Phone verified successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid OTP. Please enter '123456'.")

# After Login
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
            st.success("✅ Profile saved successfully! (Simulated)")
