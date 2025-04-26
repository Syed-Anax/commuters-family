import pyrebase
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json

# Load Firebase credentials from Streamlit secrets
firebase_secrets = dict(st.secrets["firebase"])

firebase_config = {
    "apiKey": firebase_secrets.get("api_key"),
    "authDomain": f"{firebase_secrets.get('project_id')}.firebaseapp.com",
    "databaseURL": "",
    "projectId": firebase_secrets.get("project_id"),
    "storageBucket": f"{firebase_secrets.get('project_id')}.appspot.com",
    "messagingSenderId": firebase_secrets.get("client_id"),
    "appId": firebase_secrets.get("app_id"),
}

firebase = pyrebase.initialize_app(firebase_config)
firebase_auth = firebase.auth()

# Initialize Firestore DB
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def send_otp(phone_number):
    return firebase_auth.sign_in_with_phone_number(phone_number)

def verify_otp(verification_id, otp):
    return firebase_auth.sign_in_with_custom_token(verification_id)

def save_user_profile(uid, data):
    db.collection('users').document(uid).set(data)

