# match_profiles.py

import streamlit as st
import pyrebase
from carpool_app.firebase_config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

def match_profiles(current_user_email):
    st.title("🚘 Find Your Travel Match")

    # ✅ 1. Current User Profile
    user_data = db.child("users").order_by_child("email").equal_to(current_user_email).get()
    
    if not user_data.each():
        st.warning("Your profile was not found in the database.")
        return

    current_user = user_data.each()[0].val()
    user_role = current_user["role"]
    gender = current_user["gender"]

    st.info(f"👤 Logged in as: {user_role} - {gender}")

    # ✅ 2. Get All Other Users
    all_users = db.child("users").get()
    matched_users = []

    for user in all_users.each():
        data = user.val()
        if data["email"] == current_user_email:
            continue

        # ✅ Role Inversion: Rider finds Passenger, and vice versa
        if data["role"] == user_role:
            continue

        if data["gender"] != gender:
            continue

        # ✅ Matching Criteria
        if (
            data["home_location"].lower() == current_user["home_location"].lower() and
            data["destination"].lower() == current_user["destination"].lower() and
            data["pickup_point"].lower() == current_user["pickup_point"].lower() and
            data["dropoff_point"].lower() == current_user["dropoff_point"].lower() and
            data["morning_time"] == current_user["morning_time"] and
            set(data["travel_days"]) == set(current_user["travel_days"])
        ):
            matched_users.append(data)

    # ✅ 3. Show Matches
    if matched_users:
        st.success(f"🎯 {len(matched_users)} Match(es) Found!")
        for match in matched_users:
            st.markdown(f"""
            ---
            👤 **{match['role']}**  
            🏠 From: {match['home_location']}  
            🎯 To: {match['destination']}  
            📍 Pickup: {match['pickup_point']}  
            🚏 Drop-off: {match['dropoff_point']}  
            🕒 Time: {match['morning_time']}  
            📅 Days: {', '.join(match['travel_days'])}
            ---
            """)
    else:
        st.warning("No perfect matches found yet. Try again later!")

