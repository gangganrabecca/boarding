from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional, List
import os
import logging
from dotenv import load_dotenv

from database import Neo4jConnection
from models import (
    User, UserCreate, UserLogin, Token,
    Booking, BookingCreate, BookingUpdate,
    Room, RoomCreate, RoomUpdate,
    Tenant, TenantCreate,
    Notification, NotificationUpdate
)
from auth import (
    verify_password, get_password_hash, create_access_token,
    decode_access_token, get_current_user, get_current_admin
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Boardinghouse Management System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
db = Neo4jConnection(
    uri=os.getenv("NEO4J_URI"),
    user=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

# Database dependency
def get_database():
    return db

from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Boardinghouse Management System...")
    logger.info(f"🔗 Connecting to Neo4j Aura at: {os.getenv('NEO4J_URI', 'N/A')}")
    
    try:
        # Connect to database with timeout protection
        db.connect()
        logger.info("✅ Neo4j Aura database connected successfully!")
        
        # Create constraints and indexes (with error handling)
        try:
            db.create_constraints()
            logger.info("🔒 Database constraints created/verified")
        except Exception as constraint_error:
            logger.warning(f"⚠️ Could not create constraints: {constraint_error}")
            logger.info("ℹ️ Application will continue without database constraints")
        
        # Test database accessibility
        try:
            with db.driver.session() as session:
                result = session.run("RETURN 'Database operational' as status")
                record = result.single()
                logger.info(f"🗄️ Database status: {record['status']}")
        except Exception as test_error:
            logger.warning(f"⚠️ Database test failed: {test_error}")
            logger.info("ℹ️ Application will continue with limited database functionality")
            
    except Exception as e:
        logger.error(f"❌ Failed to connect to Neo4j Aura: {e}")
        logger.warning("⚠️ Application starting in LIMITED MODE - Database features will not work")
        logger.info("💡 To enable full functionality, please check:")
        logger.info("   • Neo4j Aura instance status")
        logger.info("   • Network connectivity")
        logger.info("   • Database credentials")
    
    logger.info("🎉 Application startup complete!")
    yield
    
    # Shutdown
    logger.info("🔌 Shutting down application...")
    try:
        db.close()
        logger.info("✅ Database connection closed")
    except Exception as e:
        logger.warning(f"⚠️ Error closing database connection: {e}")
        logger.info("ℹ️ Application shutdown complete")

app = FastAPI(title="Boardinghouse Management System", lifespan=lifespan)

# Authentication endpoints
@app.post("/api/auth/register", response_model=Token)
async def register(user: UserCreate):
    # Check if user exists
    existing_user = db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = get_password_hash(user.password)
    user_id = db.create_user(user.email, user.username, hashed_password, user.role)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

# Booking endpoints
@app.post("/api/bookings", response_model=dict)
async def create_booking(booking: BookingCreate, current_user: dict = Depends(get_current_user)):
    # Check if room exists and is available
    room = db.get_room_by_id(booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room["status"] != "available":
        raise HTTPException(status_code=400, detail="Room is not available")
    
    # Create booking
    booking_id = db.create_booking(
        user_id=current_user["id"],
        room_id=booking.room_id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        duration=booking.duration
    )
    
    # Create notification for admin
    db.create_notification(
        user_id=current_user["id"],
        booking_id=booking_id,
        message=f"New booking request from {current_user['username']}",
        notification_type="booking_request"
    )
    
    return {"id": booking_id, "message": "Booking created successfully"}

@app.get("/api/bookings/my", response_model=List[dict])
async def get_my_bookings(current_user: dict = Depends(get_current_user)):
    bookings = db.get_user_bookings(current_user["id"])
    return bookings

@app.put("/api/bookings/{booking_id}", response_model=dict)
async def update_booking(
    booking_id: str,
    booking: BookingUpdate,
    current_user: dict = Depends(get_current_user)
):
    # Check if booking exists and belongs to user
    existing_booking = db.get_booking_by_id(booking_id)
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if existing_booking["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update booking
    db.update_booking(booking_id, booking.dict(exclude_unset=True))
    return {"message": "Booking updated successfully"}

@app.delete("/api/bookings/{booking_id}")
async def cancel_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    # Check if booking exists and belongs to user
    existing_booking = db.get_booking_by_id(booking_id)
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if existing_booking["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Cancel booking
    db.update_booking(booking_id, {"status": "cancelled"})
    return {"message": "Booking cancelled successfully"}

# Room endpoints
@app.get("/api/rooms", response_model=List[dict])
async def get_rooms():
    rooms = db.get_all_rooms()
    return rooms

@app.get("/api/rooms/{room_id}", response_model=dict)
async def get_room(room_id: str):
    room = db.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.post("/api/rooms", response_model=dict)
async def create_room(room: RoomCreate, current_user: dict = Depends(get_current_admin)):
    room_id = db.create_room(
        room_number=room.room_number,
        room_type=room.room_type,
        capacity=room.capacity,
        price=room.price,
        status=room.status
    )
    return {"id": room_id, "message": "Room created successfully"}

@app.put("/api/rooms/{room_id}", response_model=dict)
async def update_room(
    room_id: str,
    room: RoomUpdate,
    current_user: dict = Depends(get_current_admin)
):
    existing_room = db.get_room_by_id(room_id)
    if not existing_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db.update_room(room_id, room.dict(exclude_unset=True))
    return {"message": "Room updated successfully"}

@app.delete("/api/rooms/{room_id}")
async def delete_room(room_id: str, current_user: dict = Depends(get_current_admin)):
    db.delete_room(room_id)
    return {"message": "Room deleted successfully"}

# Tenant endpoints (Admin only)
@app.get("/api/tenants", response_model=List[dict])
async def get_tenants(current_user: dict = Depends(get_current_admin)):
    tenants = db.get_all_tenants()
    return tenants

@app.post("/api/tenants", response_model=dict)
async def create_tenant(tenant: TenantCreate, current_user: dict = Depends(get_current_admin)):
    tenant_id = db.create_tenant(
        name=tenant.name,
        email=tenant.email,
        phone=tenant.phone,
        room_id=tenant.room_id
    )
    return {"id": tenant_id, "message": "Tenant created successfully"}

# Notification endpoints
@app.get("/api/notifications", response_model=List[dict])
async def get_notifications(current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "admin":
        notifications = db.get_all_notifications()
    else:
        notifications = db.get_user_notifications(current_user["id"])
    return notifications

@app.put("/api/notifications/{notification_id}", response_model=dict)
async def update_notification(
    notification_id: str,
    notification: NotificationUpdate,
    current_user: dict = Depends(get_current_admin)
):
    db.update_notification(notification_id, notification.dict(exclude_unset=True))
    
    # If approving/rejecting booking, update booking status
    if notification.status in ["approved", "rejected"]:
        notif = db.get_notification_by_id(notification_id)
        if notif and notif.get("booking_id"):
            db.update_booking(notif["booking_id"], {"status": notification.status})
            
            # Update room status if approved
            if notification.status == "approved":
                booking = db.get_booking_by_id(notif["booking_id"])
                if booking:
                    db.update_room(booking["room_id"], {"status": "occupied"})
    
    return {"message": "Notification updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
