from firebase_admin import firestore
from datetime import datetime, timedelta

db = firestore.client()

def get_all_profiles():
    docs = db.collection("users").stream()
    return [doc.to_dict() for doc in docs]

def time_match(user_time, other_time):
    try:
        u = datetime.strptime(user_time, "%H:%M")
        o = datetime.strptime(other_time, "%H:%M")
        return abs((u - o).total_seconds()) <= 1800  # ±30 minutes
    except:
        return False

def day_overlap(user_days, other_days):
    return len(set(user_days) & set(other_days)) >= 2

def get_matches(current_user):
    matches = []
    all_users = get_all_profiles()

    for other in all_users:
        if other.get("phone_number") == current_user.get("phone_number"):
            continue

        if other["role"] == current_user["role"]:
            continue

        if current_user["home_location"].lower() not in other["home_location"].lower():
            continue

        if current_user["destination_location"].lower() not in other["destination_location"].lower():
            continue

        if not time_match(current_user["morning_time"], other["morning_time"]):
            continue

        if not time_match(current_user["evening_time"], other["evening_time"]):
            continue

        if not day_overlap(current_user["travel_days"], other["travel_days"]):
            continue

        matches.append(other)

    return matches
