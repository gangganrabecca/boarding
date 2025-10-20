from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Optional, List
import uvicorn
import os
import logging
import sys
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Local imports
from database import Neo4jConnection
from models import (
    User, UserCreate, UserLogin, Token,
    booking, bookingCreate, bookingUpdate,
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

# Debug: Log environment variables (without sensitive data)
logger.info("🚀 Starting Boardinghouse Management System...")
logger.info(f"🔗 Connecting to Neo4j Aura at: {os.getenv('NEO4J_URI', 'N/A')}")
logger.info(f"🔗 Neo4j Username: {os.getenv('NEO4J_USERNAME', 'N/A')}")
logger.info(f"🔗 JWT Secret Key configured: {'Yes' if os.getenv('JWT_SECRET_KEY') else 'No'}")

# ✅ Database connection
db = Neo4jConnection(
    uri=os.getenv("NEO4J_URI"),
    user=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

# Database dependency
def get_database():
    try:
        # Ensure database is connected
        if db.driver is None:
            db.connect()
        return db
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        if "authentication" in str(e).lower() or "unauthorized" in str(e).lower():
            raise HTTPException(
                status_code=500,
                detail="Database authentication failed. Please check your credentials."
            )
        elif "connection" in str(e).lower():
            raise HTTPException(
                status_code=500,
                detail="Database connection unavailable. Please try again later."
            )
        else:
            raise HTTPException(status_code=500, detail="Database connection unavailable")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Boardinghouse Management System...")

    try:
        # Connect to database with timeout
        logger.info(f"🔗 Connecting to Neo4j Aura at: {os.getenv('NEO4J_URI', 'N/A')}")

        # Use a timeout for database connection
        import asyncio

        async def connect_with_timeout():
            try:
                # Try to connect with a reasonable timeout
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, db.connect),
                    timeout=10.0
                )
                return True
            except asyncio.TimeoutError:
                logger.error("❌ Database connection timed out")
                return False
            except Exception as e:
                logger.error(f"❌ Database connection failed: {e}")
                return False

        connected = await connect_with_timeout()

        if connected:
            logger.info("✅ Database connection successful")

            # Test database connectivity (non-blocking)
            try:
                loop = asyncio.get_event_loop()
                test_result = await asyncio.wait_for(
                    loop.run_in_executor(None, test_database_connection),
                    timeout=5.0
                )
                if test_result:
                    logger.info("✅ Database operational test passed")
                else:
                    logger.warning("⚠️ Database operational test failed")
            except asyncio.TimeoutError:
                logger.warning("⚠️ Database operational test timed out")
            except Exception as e:
                logger.warning(f"⚠️ Database operational test error: {e}")

            # Create constraints (non-blocking)
            try:
                loop = asyncio.get_event_loop()
                await asyncio.wait_for(
                    loop.run_in_executor(None, db.create_constraints),
                    timeout=5.0
                )
                logger.info("🔒 Database constraints created/verified")
            except asyncio.TimeoutError:
                logger.warning("⚠️ Database constraint creation timed out")
            except Exception as constraint_error:
                logger.warning(f"⚠️ Could not create constraints: {constraint_error}")
                logger.info("ℹ️ Application will continue without database constraints")
        else:
            logger.error("❌ Could not establish database connection")
            logger.warning("⚠️ Application starting in LIMITED MODE - Database features will not work")

    except Exception as e:
        logger.error(f"❌ Unexpected error during startup: {e}")
        logger.warning("⚠️ Application starting in LIMITED MODE")

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

def test_database_connection():
    """Test database connectivity"""
    try:
        with db.driver.session() as session:
            result = session.run("RETURN 'Database operational' as status")
            record = result.single()
            return record['status'] == 'Database operational'
    except Exception:
        return False

app = FastAPI(title="Boardinghouse Management System", lifespan=lifespan)

# Serve static files in production (when SERVE_STATIC is True)
# Mount static files only for non-API routes to avoid conflicts
if os.getenv("SERVE_STATIC", "false").lower() == "true":
    import os
    from fastapi.staticfiles import StaticFiles

    static_path = os.path.join(os.getcwd(), "../frontend/dist")
    if os.path.exists(static_path):
        # Mount static files with a more specific path to avoid API conflicts
        app.mount("/assets", StaticFiles(directory=os.path.join(static_path, "assets")), name="static-assets")

        # Create a custom route for serving the main index.html for SPA routing
        from fastapi.responses import FileResponse

        @app.get("/")
        async def serve_spa():
            index_path = os.path.join(static_path, "index.html")
            if os.path.exists(index_path):
                return FileResponse(index_path)
            return {"error": "Frontend not found"}

        @app.get("/{full_path:path}")
        async def serve_spa_catchall(full_path: str):
            # Serve index.html for any non-API routes (SPA routing)
            if not full_path.startswith("api/"):
                index_path = os.path.join(static_path, "index.html")
                if os.path.exists(index_path):
                    return FileResponse(index_path)
            # Let API routes handle themselves
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")

        logger.info(f"✅ Serving static files from: {static_path}")
    else:
        logger.warning(f"⚠️ Static files not found at: {static_path}")
        logger.info("ℹ️ API-only mode - static files not available")

# ✅ CORS middleware - Environment-aware configuration
def get_cors_origins():
    """Get CORS origins based on environment"""
    base_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3001",
        "https://boardinghouse-app.onrender.com",
    ]

    # Add production frontend URL if available
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url and frontend_url not in base_origins:
        base_origins.append(frontend_url)

    return base_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/auth/register", response_model=Token)
async def register(user: UserCreate, database = Depends(get_database)):
    try:
        logger.info(f"Registration attempt for: {user.email}")

        # Check if user exists - handle errors gracefully
        try:
            existing_user = database.get_user_by_email(user.email)
            if existing_user:
                logger.warning(f"Registration failed - email already exists: {user.email}")
                raise HTTPException(status_code=400, detail="Email already registered")
        except HTTPException:
            raise  # Re-raise HTTP exceptions (like 400 for duplicate email)
        except Exception as e:
            logger.error(f"Error checking existing user for {user.email}: {e}")
            # If we can't check for existing users, assume it's a database issue
            raise HTTPException(status_code=500, detail="Unable to verify user registration status")

        # Validate input data
        if not user.email or not user.username or not user.password:
            logger.warning(f"Registration failed - missing required fields for: {user.email}")
            raise HTTPException(status_code=400, detail="Email, username, and password are required")

        # Create user
        try:
            hashed_password = get_password_hash(user.password)
            logger.info(f"Password hashed successfully for: {user.email}")
        except Exception as e:
            logger.error(f"Password hashing failed for {user.email}: {e}")
            raise HTTPException(status_code=500, detail="Error processing password")

        try:
            user_id = database.create_user(user.email, user.username, hashed_password, user.role)
            logger.info(f"User created successfully with ID: {user_id}")
        except HTTPException:
            raise  # Re-raise HTTP exceptions from database
        except Exception as db_error:
            logger.error(f"Database error creating user {user.email}: {db_error}")
            raise HTTPException(status_code=500, detail=f"Failed to create user in database: {str(db_error)}")

        # Create access token
        try:
            access_token = create_access_token(data={"sub": user.email, "role": user.role})
            logger.info(f"JWT token created successfully for user: {user.email}")
        except Exception as jwt_error:
            logger.error(f"JWT creation error for {user.email}: {jwt_error}")
            raise HTTPException(status_code=500, detail=f"Failed to create authentication token: {str(jwt_error)}")

        logger.info(f"Registration completed successfully for: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected registration error for {user.email}: {e}")
        raise HTTPException(status_code=500, detail="Registration failed. Please try again.")


@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), database = Depends(get_database)):
    try:
        logger.info(f"Login attempt for user: {form_data.username}")

        # Get user from database
        try:
            user = database.get_user_by_email(form_data.username)
            logger.info(f"User lookup result: {'Found' if user else 'Not found'}")
        except Exception as db_error:
            logger.error(f"Database error during user lookup: {db_error}")
            raise HTTPException(status_code=500, detail="Database connection error")

        if not user:
            logger.info("User not found - returning 401")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password
        try:
            password_valid = verify_password(form_data.password, user["password"])
            logger.info(f"Password verification result: {password_valid}")
        except Exception as pw_error:
            logger.error(f"Password verification error: {pw_error}")
            raise HTTPException(status_code=500, detail="Password verification failed")

        if not password_valid:
            logger.info("Invalid password - returning 401")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        try:
            access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})
            logger.info(f"JWT token created successfully for user: {user['email']}")
        except Exception as jwt_error:
            logger.error(f"JWT creation error: {jwt_error}")
            raise HTTPException(status_code=500, detail="Token creation failed")

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed. Please try again.")


@app.get("/api/auth/me")
async def get_me(request: Request):
    """Get current user profile - simplified version for debugging"""
    try:
        # Get authorization header
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="No token provided")

        token = authorization.split(" ")[1]

        # Decode token (simplified - just check if it exists)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid token")

        # For now, return a test response to verify endpoint works
        return {
            "message": "Authentication endpoint is working",
            "token_provided": True,
            "status": "authenticated"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_me endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user profile")

@app.get("/api/auth/me/full")
async def get_me_full(current_user: dict = Depends(get_current_user)):
    """Get current user profile - full version"""
    try:
        return {
            "id": current_user["id"],
            "email": current_user["email"],
            "username": current_user["username"],
            "role": current_user["role"],
            "created_at": current_user["created_at"]
        }
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user profile")

# ============================================
# 🏥 HEALTH CHECK ROUTES
# ============================================

@app.get("/health")
async def health_check(database = Depends(get_database)):
    """Health check endpoint for deployment monitoring"""
    try:
        # Test database connection
        db_status = "healthy"
        try:
            with database.driver.session() as session:
                result = session.run("RETURN 'Database operational' as status")
                record = result.single()
                if record['status'] != 'Database operational':
                    db_status = "unhealthy"
        except Exception as e:
            logger.error(f"Health check database error: {e}")
            db_status = "unhealthy"

        return {
            "status": "healthy" if db_status == "healthy" else "unhealthy",
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# ============================================
# 🏠 BOOKING ROUTES
# ============================================

@app.post("/api/bookings", response_model=dict)
async def create_booking(booking: BookingCreate, current_user: dict = Depends(get_current_user), database = Depends(get_database)):
    room = database.get_room_by_id(booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room["status"] != "available":
        raise HTTPException(status_code=400, detail="Room is not available")

    booking_id = database.create_booking(
        user_id=current_user["id"],
        room_id=booking.room_id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        duration=booking.duration
    )

    database.create_notification(
        user_id=current_user["id"],
        booking_id=booking_id,
        message=f"New booking request from {current_user['username']}",
        notification_type="booking_request"
    )

    return {"id": booking_id, "message": "Booking created successfully"}


@app.get("/api/bookings/my", response_model=List[dict])
async def get_my_bookings(current_user: dict = Depends(get_current_user), database = Depends(get_database)):
    return database.get_user_bookings(current_user["id"])


@app.put("/api/bookings/{booking_id}", response_model=dict)
async def update_booking(booking_id: str, booking: BookingUpdate, current_user: dict = Depends(get_current_user), database = Depends(get_database)):
    existing_booking = database.get_booking_by_id(booking_id)
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if existing_booking["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    database.update_booking(booking_id, booking.dict(exclude_unset=True))
    return {"message": "Booking updated successfully"}


@app.delete("/api/bookings/{booking_id}")
async def cancel_booking(booking_id: str, current_user: dict = Depends(get_current_user), database = Depends(get_database)):
    existing_booking = database.get_booking_by_id(booking_id)
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if existing_booking["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    database.update_booking(booking_id, {"status": "cancelled"})
    return {"message": "Booking cancelled successfully"}

# ============================================
# 🏡 ROOM ROUTES
# ============================================

@app.get("/api/rooms", response_model=List[dict])
async def get_rooms(database = Depends(get_database)):
    return database.get_all_rooms()


@app.get("/api/rooms/{room_id}", response_model=dict)
async def get_room(room_id: str, database = Depends(get_database)):
    room = database.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@app.post("/api/rooms", response_model=dict)
async def create_room(room: RoomCreate, current_user: dict = Depends(get_current_admin), database = Depends(get_database)):
    room_id = database.create_room(**room.dict())
    return {"id": room_id, "message": "Room created successfully"}


@app.put("/api/rooms/{room_id}", response_model=dict)
async def update_room(room_id: str, room: RoomUpdate, current_user: dict = Depends(get_current_admin), database = Depends(get_database)):
    database.update_room(room_id, room.dict(exclude_unset=True))
    return {"message": "Room updated successfully"}


@app.delete("/api/rooms/{room_id}")
async def delete_room(room_id: str, current_user: dict = Depends(get_current_admin), database = Depends(get_database)):
    database.delete_room(room_id)
    return {"message": "Room deleted successfully"}

# ============================================
# 👥 TENANT ROUTES (Admin only)
# ============================================

@app.get("/api/tenants", response_model=List[dict])
async def get_tenants(current_user: dict = Depends(get_current_admin), database = Depends(get_database)):
    return database.get_all_tenants()


@app.post("/api/tenants", response_model=dict)
async def create_tenant(tenant: TenantCreate, current_user: dict = Depends(get_current_admin), database = Depends(get_database)):
    tenant_id = database.create_tenant(**tenant.dict())
    return {"id": tenant_id, "message": "Tenant created successfully"}

# ============================================
# 🔔 NOTIFICATION ROUTES
# ============================================

@app.get("/api/notifications", response_model=List[dict])
async def get_notifications(current_user: dict = Depends(get_current_user), database = Depends(get_database)):
    if current_user["role"] == "admin":
        return database.get_all_notifications()
    return database.get_user_notifications(current_user["id"])


@app.put("/api/notifications/{notification_id}", response_model=dict)
async def update_notification(notification_id: str, notification: NotificationUpdate, current_user: dict = Depends(get_current_admin), database = Depends(get_database)):
    database.update_notification(notification_id, notification.dict(exclude_unset=True))

    if notification.status in ["approved", "rejected"]:
        notif = database.get_notification_by_id(notification_id)
        if notif and notif.get("booking_id"):
            database.update_booking(notif["booking_id"], {"status": notification.status})

            if notification.status == "approved":
                booking = database.get_booking_by_id(notif["booking_id"])
                if booking and booking.get("room"):
                    database.update_room(booking["room"]["id"], {"status": "occupied"})

    return {"message": "Notification updated successfully"}

# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
