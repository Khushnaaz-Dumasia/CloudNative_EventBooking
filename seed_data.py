import requests

# Define our service endpoints
USERS_URL = "http://localhost:8001/users"
EVENTS_URL = "http://localhost:8002/events"
BOOKINGS_URL = "http://localhost:8003/bookings"

def seed_data():
    print("🌱 Starting data seeding...")

    # 1. Create Users
    user_data = [
        {"name": "Khushnaaz", "email": "khush@example.com"},
        {"name": "Alice Smith", "email": "alice@example.com"}
    ]
    user_ids = []
    for user in user_data:
        response = requests.post(USERS_URL, json=user)
        if response.status_code == 200:
            user_ids.append(response.json()['id'])
            print(f"✅ Created User: {user['name']}")

    # 2. Create Events
    event_data = [
        {"title": "Cloud Computing Workshop", "location": "Tech Hub"},
        {"title": "Microservices Seminar", "location": "Online"}
    ]
    event_ids = []
    for event in event_data:
        response = requests.post(EVENTS_URL, json=event)
        if response.status_code == 200:
            event_ids.append(response.json()['id'])
            print(f"✅ Created Event: {event['title']}")

    # 3. Create a Sample Booking
    if user_ids and event_ids:
        booking = {"user_id": user_ids[0], "event_id": event_ids[0]}
        requests.post(BOOKINGS_URL, json=booking)
        print(f"✅ Created Sample Booking for User {user_ids[0]}")

if __name__ == "__main__":
    try:
        seed_data()
        print("\n✨ Seeding complete! Refresh your frontend at http://localhost:8080")
    except Exception as e:
        print(f"❌ Error: {e}. Make sure your services are running on ports 8001, 8002, and 8003.")