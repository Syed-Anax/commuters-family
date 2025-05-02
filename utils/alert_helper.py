from datetime import datetime
import random

def get_today_alert(user_profile):
    today = datetime.now().strftime("%A")  # e.g. Monday
    if today not in user_profile.get("travel_days", []):
        return "🔔 No travel scheduled for today. Enjoy your break!"
    
    destination = user_profile.get("destination_location", "your route")
    
    # Simulated fake condition
    jam_chance = random.randint(1, 5)
    if jam_chance == 1:
        return f"⚠️ Alert: Traffic jam reported on your route to {destination}!"
    else:
        return f"🚀 Route to {destination} is clear. Safe travels!"
