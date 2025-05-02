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
def upgrade_to_premium(phone_number):
    db.collection("users").document(phone_number).update({"is_premium": True})

def check_if_premium(phone_number):
    doc = db.collection("users").document(phone_number).get()
    if doc.exists:
        return doc.to_dict().get("is_premium", False)
    return False
