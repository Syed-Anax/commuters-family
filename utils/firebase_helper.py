import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_user_profile(uid, data):
    db.collection('users').document(uid).set(data)
