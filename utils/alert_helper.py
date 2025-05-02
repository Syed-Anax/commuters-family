# utils/alert_helper.py
from datetime import datetime
import random

def get_today_alert(profile):
    now = datetime.now()
    current_day = now.strftime("%A")  # e.g., Monday
    current_time = now.strftime("%H:%M")

    if current_day not in profile.get("travel_days", []):
        return "🔔 No travel scheduled for today. Enjoy your break!"

    # Fake jam logic for demo
    jammed_routes = ["Shahrah-e-Faisal", "Korangi Road", "University Road"]
    is_jammed = random.choice([True, False])

    if is_jammed:
        return f"⚠️ Alert: Traffic jam reported on your route to {profile.get('destination_location')}!"
    else:
        return f"🚀 Route to {profile.get('destination_location')} is clear. Safe travels!"
