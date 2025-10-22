from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import uvicorn
import logging
import os
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Simple FastAPI app without database
app = FastAPI(title="Boardinghouse Management System - Minimal")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running (minimal mode)"}

# Simple login endpoint (mock)
@app.post("/api/auth/login")
async def login(form_data: dict):
    # Mock authentication - accept any email/password for testing
    if form_data.get("username") and form_data.get("password"):
        return {
            "access_token": "mock_token_123",
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Also handle the OAuth2PasswordRequestForm format that the frontend uses
from fastapi import Form
@app.post("/auth/login")
async def login_form(username: str = Form(), password: str = Form()):
    # Mock authentication - accept any email/password for testing
    if username and password:
        return {
            "access_token": "mock_token_123",
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/auth/me")
async def get_me():
    return {
        "id": "1",
        "email": "admin@boardinghouse.com",
        "username": "admin",
        "role": "admin"
    }

@app.get("/auth/me/full")
async def get_me_full():
    return {
        "id": "1",
        "email": "admin@boardinghouse.com",
        "username": "admin",
        "role": "admin",
        "created_at": "2024-01-01T00:00:00Z"
    }

# Mock rooms data
mock_rooms = [
    {
        "id": "1",
        "room_number": "101",
        "room_type": "single",
        "capacity": 1,
        "price": 5000,
        "status": "available"
    },
    {
        "id": "2",
        "room_number": "102",
        "room_type": "double",
        "capacity": 2,
        "price": 8000,
        "status": "available"
    },
    {
        "id": "3",
        "room_number": "201",
        "room_type": "suite",
        "capacity": 3,
        "price": 12000,
        "status": "occupied"
    }
]

@app.get("/api/rooms")
async def get_rooms():
    return mock_rooms

@app.get("/api/rooms/{room_id}")
async def get_room(room_id: str):
    room = next((r for r in mock_rooms if r["id"] == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# Mock bookings data
mock_bookings = [
    {
        "id": "booking_1",
        "room_id": "1",
        "start_date": "2024-02-01",
        "end_date": "2024-03-01",
        "duration": 1,
        "status": "approved",
        "created_at": "2024-01-01T00:00:00Z",
        "room": {
            "id": "1",
            "room_number": "101",
            "room_type": "single",
            "capacity": 1,
            "price": 5000,
            "status": "occupied"
        }
    },
    {
        "id": "booking_2",
        "room_id": "2",
        "start_date": "2024-02-15",
        "end_date": "2024-04-15",
        "duration": 2,
        "status": "pending",
        "created_at": "2024-01-15T00:00:00Z",
        "room": {
            "id": "2",
            "room_number": "102",
            "room_type": "double",
            "capacity": 2,
            "price": 8000,
            "status": "available"
        }
    }
]

@app.get("/api/bookings/my")
async def get_my_bookings():
    return mock_bookings

@app.post("/api/bookings")
async def create_booking(booking: dict):
    booking_id = f"booking_{len(mock_bookings) + 1}"
    new_booking = {
        "id": booking_id,
        "room_id": booking["room_id"],
        "start_date": booking["start_date"],
        "end_date": booking["end_date"],
        "duration": booking["duration"],
        "status": "pending",
        "created_at": "2024-01-01T00:00:00Z",
        "room": mock_rooms[int(booking["room_id"]) - 1]  # Get room data from mock_rooms
    }
    mock_bookings.append(new_booking)
    return {"id": booking_id, "message": "Booking created successfully"}

# Mock tenants data
mock_tenants = [
    {
        "id": "1",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "09123456789",
        "room": {"room_number": "101", "room_type": "single"}
    }
]
@app.get("/api/tenants")
async def get_tenants():
    return mock_tenants

@app.post("/api/tenants")
async def create_tenant(tenant: dict):
    tenant_id = f"tenant_{len(mock_tenants) + 1}"
    new_tenant = {
        "id": tenant_id,
        "name": tenant["name"],
        "email": tenant["email"],
        "phone": tenant["phone"],
        "room": {"room_number": "101", "room_type": "single"}
    }
    mock_tenants.append(new_tenant)
    return {"id": tenant_id, "message": "Tenant created successfully"}

# Mock notifications data
mock_notifications = [
    {
        "id": "1",
        "message": "New booking request for Room 101",
        "status": "pending",
        "user": {"username": "John Doe", "email": "john@example.com"},
        "created_at": "2024-01-01T00:00:00Z",
        "booking_id": "booking_1"
    }
]

@app.get("/api/notifications")
async def get_notifications():
    return mock_notifications

@app.post("/api/rooms")
async def create_room(room: dict):
    room_id = f"room_{len(mock_rooms) + 1}"
    new_room = {
        "id": room_id,
        "room_number": room.get("room_number", ""),
        "room_type": room.get("room_type", "single"),
        "capacity": room.get("capacity", 1),
        "price": room.get("price", 0),
        "status": "available"
    }
    mock_rooms.append(new_room)
    return {"id": room_id, "message": "Room created successfully"}

@app.delete("/api/rooms/{room_id}")
async def delete_room(room_id: str):
    global mock_rooms
    mock_rooms = [r for r in mock_rooms if r["id"] != room_id]
    return {"message": "Room deleted successfully"}

@app.put("/api/rooms/{room_id}")
async def update_room(room_id: str, room: dict):
    for i, r in enumerate(mock_rooms):
        if r["id"] == room_id:
            mock_rooms[i].update(room)
            break
    return {"message": "Room updated successfully"}

@app.delete("/api/bookings/{booking_id}")
async def cancel_booking(booking_id: str):
    global mock_bookings
    mock_bookings = [b for b in mock_bookings if b["id"] != booking_id]
    return {"message": "Booking cancelled successfully"}

@app.put("/api/bookings/{booking_id}")
async def update_booking(booking_id: str, booking: dict):
    for i, b in enumerate(mock_bookings):
        if b["id"] == booking_id:
            mock_bookings[i].update(booking)
            break
    return {"message": "Booking updated successfully"}

@app.put("/api/notifications/{notification_id}")
async def update_notification(notification_id: str, notification: dict):
    # Update notification status and related booking if needed
    for i, n in enumerate(mock_notifications):
        if n["id"] == notification_id:
            mock_notifications[i]["status"] = notification.get("status", n["status"])
            break

    # If notification is approved/rejected, update related booking
    if notification.get("status") in ["approved", "rejected"]:
        for i, b in enumerate(mock_bookings):
            if b.get("id") == f"booking_{notification_id}":
                mock_bookings[i]["status"] = notification["status"]
                # Update room status if booking is approved
                if notification["status"] == "approved":
                    for j, r in enumerate(mock_rooms):
                        if r["id"] == b["room_id"]:
                            mock_rooms[j]["status"] = "occupied"
                            break
                break

    return {"message": "Notification updated successfully"}

# Add endpoint for fetching user bookings (for user dashboard)
@app.get("/api/bookings/user/{user_id}")
async def get_user_bookings(user_id: str):
    return mock_bookings

# Add endpoint for user notifications
@app.get("/api/notifications/user/{user_id}")
async def get_user_notifications(user_id: str):
    return [n for n in mock_notifications if n.get("user_id") == user_id]
