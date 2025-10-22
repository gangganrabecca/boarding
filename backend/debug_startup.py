#!/usr/bin/env python3
"""
Debug script to test FastAPI startup
"""
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, '.')

# Load environment variables
load_dotenv()

print("=== FASTAPI STARTUP DEBUG ===")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

try:
    print("\n1. Testing imports...")
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import OAuth2PasswordBearer
    from datetime import datetime
    import uvicorn
    from contextlib import asynccontextmanager

    print("✅ All FastAPI imports successful")

    print("\n2. Testing local imports...")
    from database import Neo4jConnection
    from models import UserCreate, Token, UserLogin
    from auth import verify_password, get_password_hash, create_access_token

    print("✅ All local imports successful")

    print("\n3. Testing database connection...")
    db = Neo4jConnection(
        uri=os.getenv("NEO4J_URI"),
        user=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    db.connect()
    print("✅ Database connection successful")

    # Test database operations
    existing_admin = db.get_user_by_email("admin@boardinghouse.com")
    print(f"✅ Admin user check: {'Found' if existing_admin else 'Not found'}")

    db.close()
    print("✅ Database closed successfully")

    print("\n4. Testing FastAPI app creation...")
    # Test the same lifespan logic as main.py
    @asynccontextmanager
    async def test_lifespan(app: FastAPI):
        print("🚀 Starting test application...")
        try:
            print(f"🔗 Connecting to Neo4j Aura at: {os.getenv('NEO4J_URI', 'N/A')}")

            # Use the same database connection logic
            if db.driver is None:
                print("🔗 Connecting to database...")
                db.connect()

            print("✅ Database connection successful")
            print("✅ Test application startup complete!")

        except Exception as e:
            print(f"❌ Error during startup: {e}")
            import traceback
            traceback.print_exc()
            raise

        yield

        print("🔌 Shutting down test application...")
        try:
            db.close()
            print("✅ Database connection closed")
        except Exception as e:
            print(f"⚠️ Error closing database connection: {e}")

    # Create test app
    test_app = FastAPI(title="Test App", lifespan=test_lifespan)
    print("✅ FastAPI app created successfully")

    print("\n=== DEBUG COMPLETE ===")
    print("✅ All components working correctly!")
    print("The issue might be with uvicorn or the specific main.py configuration")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
