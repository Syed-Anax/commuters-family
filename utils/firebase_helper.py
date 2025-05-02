import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_user_profile(uid, data):
    db.collection('users').document(uid).set(data)

def get_user_profile(phone_number):
    doc = db.collection("users").document(phone_number).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
def upgrade_to_premium(phone_number):
    db.collection("users").document(phone_number).update({"is_premium": True})

def check_if_premium(phone_number):
    doc = db.collection("users").document(phone_number).get()
    if doc.exists:
        return doc.to_dict().get("is_premium", False)
    return False
