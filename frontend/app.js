const USER_API = "http://localhost:8001";
const EVENT_API = "http://localhost:8002";
const BOOKING_API = "http://localhost:8003";

// Fetch and display data on load
window.onload = () => {
    loadUsers();
    loadEvents();
    loadBookings();
};

async function loadUsers() {
    const res = await fetch(`${USER_API}/users`);
    const users = await res.json();
    document.getElementById('userList').innerHTML = users.map(u => `<li>${u.name} (ID: ${u.id})</li>`).join('');
}

async function loadEvents() {
    const res = await fetch(`${EVENT_API}/events`);
    const events = await res.json();
    document.getElementById('eventList').innerHTML = events.map(e => 
        `<li>${e.title} at ${e.location} 
         <button onclick="bookEvent(${e.id})">Book</button></li>`
    ).join('');
}

async function bookEvent(eventId) {
    const userId = prompt("Enter your User ID to book:");
    if (!userId) return;

    await fetch(`${BOOKING_API}/bookings`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ user_id: parseInt(userId), event_id: eventId })
    });
    loadBookings();
}

async function loadBookings() {
    const res = await fetch(`${BOOKING_API}/bookings`);
    const bookings = await res.json();
    // In a real app, you'd fetch user/event names here to replace the IDs
    document.getElementById('bookingList').innerHTML = bookings.map(b => 
        `<li>Booking #${b.id}: User ${b.user_id} registered for Event ${b.event_id}</li>`
    ).join('');
}

async function createUser() {
    const name = document.getElementById('userName').value;
    const email = document.getElementById('userEmail').value;
    await fetch(`${USER_API}/users`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, email })
    });
    loadUsers();
}