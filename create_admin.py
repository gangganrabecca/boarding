#!/usr/bin/env python3
"""
Script to manually create the admin user in the database
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import Neo4jConnection
from auth import get_password_hash

def create_admin_user():
    """Create admin user manually"""
    load_dotenv()

    # Database connection
    db = Neo4jConnection(
        uri=os.getenv("NEO4J_URI"),
        user=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    try:
        # Connect to database
        db.connect()
        print("✅ Connected to database")

        # Admin credentials
        admin_email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@test.com")
        admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")
        admin_username = "admin"
        admin_role = "admin"

        # Check if admin user exists
        existing_admin = db.get_user_by_email(admin_email)

        if existing_admin:
            print(f"✅ Admin user already exists: {admin_email}")
            return True

        # Create admin user
        hashed_password = get_password_hash(admin_password)
        admin_id = db.create_user(admin_email, admin_username, hashed_password, admin_role)

        print(f"✅ Admin user created successfully with ID: {admin_id}")
        print(f"📧 Email: {admin_email}")
        print(f"🔑 Password: {admin_password}")
        return True

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
