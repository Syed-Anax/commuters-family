from datetime import datetime, timedelta

def get_travel_alert(user_profile):
    today = datetime.now().strftime("%A")
    current_time = datetime.now().strftime("%H:%M")

    if today not in user_profile.get("travel_days", []):
        return None  # no travel today

    alert_time = user_profile.get("morning_time", "08:00")

    user_time = datetime.strptime(alert_time, "%H:%M")
    now = datetime.now()

    diff = abs((now - now.replace(hour=user_time.hour, minute=user_time.minute)).total_seconds())

    if diff <= 3600:  # within 1 hour
        return f"🕒 Reminder: You are scheduled to travel at {alert_time} today!"

    return None
