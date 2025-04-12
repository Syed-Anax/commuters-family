# main_app.py

import streamlit as st
from firebase_config import firebaseConfig
import pyrebase
from PIL import Image

# Firebase initialization
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Language options
if 'language' not in st.session_state:
    st.session_state.language = 'English'  # Default language

language_options = {
    'English': {
        'welcome': "Welcome to Commuters Family 🇵🇰",
        'tagline': "Connecting neighbors with same routes for daily commute!",
        'get_started': "Get Started"
    },
    'Urdu': {
        'welcome': "کميوٹرز فیملی میں خوش آمدید 🇵🇰",
        'tagline': "روزانہ سفر کرنے والے ہمسایوں کو جوڑنا!",
        'get_started': "شروع کریں"
    }
}

# Function to show landing page
def show_landing_page():
    logo = Image.open('images/logo.png')
    st.image(logo, width=150)

    lang = st.selectbox("Select Language / زبان منتخب کریں", ["English", "Urdu"])
    st.session_state.language = lang

    st.markdown(
        f"<h1 style='text-align: center; color: green;'>{language_options[lang]['welcome']}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<h4 style='text-align: center;'>{language_options[lang]['tagline']}</h4>",
        unsafe_allow_html=True
    )

    if st.button(language_options[lang]['get_started']):
        st.session_state.page = 'splash'
# Function to show splash (onboarding) screens
def show_splash_screens():
    if 'splash_index' not in st.session_state:
        st.session_state.splash_index = 0

    lang = st.session_state.language

    splash_images = [
        ("images/splash1.png", {
            "English": "Signup to connect with commuters nearby!",
            "Urdu": "قریبی ہمسایوں کے ساتھ رابطہ قائم کریں!"
        }),
        ("images/splash2.png", {
            "English": "Set your daily commute schedule easily.",
            "Urdu": "اپنے روزانہ کے سفر کا شیڈول آسانی سے بنائیں۔"
        }),
        ("images/splash3.png", {
            "English": "Get matched with nearby travel partners.",
            "Urdu": "قریبی سفر کے ساتھیوں کے ساتھ میل کھائیں۔"
        }),
        ("images/splash4.png", {
            "English": "Female match with female only for extra safety.",
            "Urdu": "خواتین کے لئے خواتین سے میل صرف اضافی تحفظ کے لیے۔"
        }),
        ("images/splash5.png", {
            "English": "Free Fuel Cost Calculator for Daily Commute!",
            "Urdu": "روزانہ سفر کے لئے مفت ایندھن لاگت کیلکولیٹر!"
        }),
        ("images/splash6.png", {
            "English": "Free Route Alerts for Traffic and Closures!",
            "Urdu": "ٹریفک اور بندشوں کے لئے مفت راستے کی اطلاعات!"
        }),
        ("images/splash7.png", {
            "English": "Share fuel cost and earn extra money!",
            "Urdu": "ایندھن کے اخراجات کو شیئر کریں اور اضافی پیسے کمائیں!"
        }),
        ("images/splash8.png", {
            "English": "Affordable Monthly Plans for Verified Users ⭐",
            "Urdu": "مصدقہ صارفین کے لیے سستی ماہانہ منصوبے ⭐"
        })
    ]

    current_image, captions = splash_images[st.session_state.splash_index]
    st.image(current_image, use_column_width=True)
    st.markdown(
        f"<h4 style='text-align: center;'>{captions[lang]}</h4>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous"):
            if st.session_state.splash_index > 0:
                st.session_state.splash_index -= 1
    with col2:
        if st.button("Skip"):
            st.session_state.page = 'login'
    with col3:
        if st.button("Next"):
            if st.session_state.splash_index < len(splash_images) - 1:
                st.session_state.splash_index += 1
            else:
                st.session_state.page = 'login'
# Function to show login/signup page
def show_login_signup():
    lang = st.session_state.language

    st.title("Login / Signup" if lang == "English" else "لاگ ان / سائن اپ")
    choice = st.selectbox("Select Option" if lang == "English" else "اختیار منتخب کریں", ["Login", "Signup"])

    email = st.text_input("Email" if lang == "English" else "ای میل")
    password = st.text_input("Password" if lang == "English" else "پاس ورڈ", type="password")

    if choice == "Signup":
        if st.button("Create Account" if lang == "English" else "اکاؤنٹ بنائیں"):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success("Account created successfully!" if lang == "English" else "اکاؤنٹ کامیابی سے بنایا گیا!")
                st.session_state.page = 'home'
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        if st.button("Login" if lang == "English" else "لاگ ان کریں"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success("Logged in successfully!" if lang == "English" else "کامیابی سے لاگ ان ہو گیا!")
                st.session_state.page = 'home'
            except Exception as e:
                st.error(f"Error: {e}")

# Function to show home page after login
def show_home():
    lang = st.session_state.language

    st.title("Welcome to Commuters Family App 🚗" if lang == "English" else "کميوٹرز فیملی ایپ میں خوش آمدید 🚗")
    st.success("You are successfully logged in!" if lang == "English" else "آپ کامیابی سے لاگ ان ہو چکے ہیں!")
    st.markdown("More features coming soon..." if lang == "English" else "مزید خصوصیات جلد آ رہی ہیں۔۔۔")

# Main app flow
def main():
    st.set_page_config(page_title="Commuters Family", page_icon="🚗", layout="centered")

    if 'page' not in st.session_state:
        st.session_state.page = 'landing'

    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'splash':
        show_splash_screens()
    elif st.session_state.page == 'login':
        show_login_signup()
    elif st.session_state.page == 'home':
        show_home()

if __name__ == "__main__":
    main()
