#!/usr/bin/env python3
"""
Script to initialize the boardinghouse database with sample data
"""
import os
import sys
from dotenv import load_dotenv

# Add backend directory to path
sys.path.append('./backend')

from database import Neo4jConnection
from auth import get_password_hash

# Load environment variables
load_dotenv()

def initialize_database():
    """Initialize database with sample data"""
    # Connect to database
    db = Neo4jConnection(
        uri=os.getenv("NEO4J_URI"),
        user=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    try:
        print("🔗 Connecting to Neo4j...")
        db.connect()

        # Create constraints
        print("🔒 Creating database constraints...")
        db.create_constraints()

        # Create admin user
        print("👑 Creating admin user...")
        admin_email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@boardinghouse.com")
        admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

        existing_admin = db.get_user_by_email(admin_email)
        if not existing_admin:
            hashed_password = get_password_hash(admin_password)
            admin_id = db.create_user(admin_email, "admin", hashed_password, "admin")
            print(f"✅ Admin user created: {admin_email} / {admin_password}")
        else:
            print(f"✅ Admin user already exists: {admin_email}")

        # Create sample rooms
        print("🏠 Creating sample rooms...")

        # Check if rooms already exist
        existing_rooms = db.get_all_rooms()
        if not existing_rooms:
            # Create sample rooms
            rooms_data = [
                {"room_number": "101", "room_type": "Single", "capacity": 1, "price": 5000.00},
                {"room_number": "102", "room_type": "Single", "capacity": 1, "price": 5000.00},
                {"room_number": "201", "room_type": "Double", "capacity": 2, "price": 8000.00},
                {"room_number": "202", "room_type": "Double", "capacity": 2, "price": 8000.00},
                {"room_number": "301", "room_type": "Family", "capacity": 4, "price": 12000.00},
                {"room_number": "302", "room_type": "Family", "capacity": 4, "price": 12000.00},
            ]

            for room_data in rooms_data:
                room_id = db.create_room(**room_data)
                print(f"✅ Created room {room_data['room_number']} - {room_data['room_type']}")

            print(f"✅ Created {len(rooms_data)} sample rooms")
        else:
            print(f"✅ Rooms already exist: {len(existing_rooms)} rooms found")

        # Create sample users
        print("👤 Creating sample users...")
        sample_users = [
            {"email": "john.doe@example.com", "username": "john_doe", "password": "password123", "role": "user"},
            {"email": "jane.smith@example.com", "username": "jane_smith", "password": "password123", "role": "user"},
        ]

        for user_data in sample_users:
            existing_user = db.get_user_by_email(user_data["email"])
            if not existing_user:
                hashed_password = get_password_hash(user_data["password"])
                user_id = db.create_user(user_data["email"], user_data["username"], hashed_password, user_data["role"])
                print(f"✅ Created user: {user_data['email']}")
            else:
                print(f"✅ User already exists: {user_data['email']}")

        print("🎉 Database initialization complete!")
        print("\n📋 Sample Login Credentials:")
        print(f"Admin: {admin_email} / {admin_password}")
        print("Users: john.doe@example.com / password123")
        print("       jane.smith@example.com / password123")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

    finally:
        db.close()

    return True

if __name__ == "__main__":
    print("🚀 Initializing Boardinghouse Database...")
    success = initialize_database()
    if success:
        print("✅ Database initialized successfully!")
    else:
        print("❌ Database initialization failed!")
        sys.exit(1)
