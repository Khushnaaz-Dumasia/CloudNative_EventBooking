const USER_API = "http://k8s-default-userserv-4b1b02608a-7c6b3d9c128fe257.elb.eu-north-1.amazonaws.com";
const EVENT_API = "http://k8s-default-eventser-c3ad2d7598-3f3770693da645aa.elb.eu-north-1.amazonaws.com";
const BOOKING_API = "http://k8s-default-bookings-a99fdcbaa2-c2e2965123c87700.elb.eu-north-1.amazonaws.com";

// Fetch and display data on load
window.onload = () => {
    const userId = localStorage.getItem('userId');
    if (userId) {
        document.getElementById('auth-section').style.display = 'none';
        document.getElementById('app-content').style.display = 'block';
        document.getElementById('logoutBtn').style.display = 'block';
    }
    loadUsers();
    loadEvents();
    loadBookings();
};

async function handleAuth(type) {
    const name = document.getElementById('authName').value;
    const email = document.getElementById('authEmail').value;
    const password = document.getElementById('authPassword').value;
    const status = document.getElementById('authStatus');

    const endpoint = type === 'login' ? '/login' : '/signup';
    const body = type === 'login' ? { email, password } : { name, email, password };

    try {
        const res = await fetch(`${USER_API}${endpoint}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });

        const data = await res.json();

        if (res.ok) {
            if (type === 'login') {
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('userId', data.user_id);
                document.getElementById('auth-section').style.display = 'none';
                document.getElementById('app-content').style.display = 'block';
                document.getElementById('logoutBtn').style.display = 'block';
                loadUsers(); loadEvents(); loadBookings();
            } else {
                status.innerText = "Account created! Please login.";
            }
        } else {
            status.innerText = "Error: " + data.detail;
        }
    } catch (err) {
        console.error("Auth Error:", err);
        status.innerText = "Error: Could not reach the service. (Check console for details)";
    }
}

function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    
    // Clear input fields
    document.getElementById('authName').value = '';
    document.getElementById('authEmail').value = '';
    document.getElementById('authPassword').value = '';
    
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('app-content').style.display = 'none';
    document.getElementById('logoutBtn').style.display = 'none';
    document.getElementById('authStatus').innerText = "Logged out successfully.";
}

async function loadUsers() {
    const res = await fetch(`${USER_API}/users`);
    const users = await res.json();
    document.getElementById('userList').innerHTML = users.map(u => 
        `<li>
            <div class="event-title">${u.name}</div>
            <div class="event-meta">User ID: ${u.id} | ${u.email}</div>
        </li>`
    ).join('');
}

async function loadEvents() {
    const res = await fetch(`${EVENT_API}/events`);
    const events = await res.json();
    document.getElementById('eventList').innerHTML = events.map(e => 
        `<li class="event-item">
            <div class="event-title">${e.title}</div>
            <div class="event-meta">📍 ${e.location}</div>
            <div class="event-meta">📅 ${e.date_time}</div>
            <button class="book-btn" onclick="bookEvent(${e.id})">Reserve Spot</button>
        </li>`
    ).join('');
}

async function bookEvent(eventId) {
    // Get the ID from localStorage (saved during login)
    const userId = localStorage.getItem('userId');
    
    if (!userId) {
        alert("Please login first to book an event!");
        return;
    }

    const response = await fetch(`${BOOKING_API}/bookings`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 
            user_id: parseInt(userId), 
            event_id: eventId 
        })
    });

    if (response.ok) {
        alert("Event booked successfully!!");
        loadBookings();
    } else {
        const errorData = await response.json();
        alert("Booking failed: " + errorData.detail);
    }
}

async function loadBookings() {
    const res = await fetch(`${BOOKING_API}/bookings`);
    const bookings = await res.json();
    document.getElementById('bookingList').innerHTML = bookings.map(b => 
        `<li>
            <div class="event-title">Booking #${b.id}</div>
            <div class="event-meta">User ${b.user_id} attending Event ${b.event_id}</div>
            <button class="book-btn" style="background: #ef4444; margin-top: 5px;" onclick="deleteBooking(${b.id})">Cancel Booking</button>
        </li>`
    ).join('');
}

async function deleteBooking(bookingId) {
    if (!confirm("Are you sure you want to cancel this booking?")) return;

    const res = await fetch(`${BOOKING_API}/bookings/${bookingId}`, {
        method: 'DELETE'
    });

    if (res.ok) {
        alert("Booking cancelled successfully.");
        loadBookings();
    } else {
        alert("Failed to cancel booking.");
    }
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