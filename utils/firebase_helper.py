import requests
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    firebase_secrets = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Firebase REST API endpoints
API_KEY = st.secrets["firebase"]["api_key"]
FIREBASE_AUTH_BASE_URL = "https://identitytoolkit.googleapis.com/v1"

def send_otp(phone_number):
    url = f"{FIREBASE_AUTH_BASE_URL}/accounts:sendVerificationCode?key={API_KEY}"
    payload = {
        "phoneNumber": phone_number,
        "recaptchaToken": "mock"  # Streamlit Web can't handle reCAPTCHA easily, simulation for now
    }
    response = requests.post(url, json=payload)
    return response.json()

def verify_otp(session_info, otp_code):
    url = f"{FIREBASE_AUTH_BASE_URL}/accounts:signInWithPhoneNumber?key={API_KEY}"
    payload = {
        "sessionInfo": session_info,
        "code": otp_code
    }
    response = requests.post(url, json=payload)
    return response.json()

def save_user_profile(uid, data):
    db.collection('users').document(uid).set(data)
