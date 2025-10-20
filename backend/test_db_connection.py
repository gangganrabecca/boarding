#!/usr/bin/env python3

import os
import sys
sys.path.append('./backend')

from dotenv import load_dotenv
from database import Neo4jConnection

# Load environment variables
load_dotenv('./backend/.env')

def test_neo4j_connection():
    """Test direct Neo4j connection and operations"""
    try:
        print("🔗 Connecting to Neo4j Aura...")
        db = Neo4jConnection(
            uri=os.getenv("NEO4J_URI"),
            user=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD")
        )

        db.connect()

        print("✅ Database connection successful")

        # Test basic query
        with db.driver.session() as session:
            result = session.run("RETURN 'Database operational' as status")
            record = result.single()
            print(f"✅ Basic query result: {record['status']}")

        # Test creating constraints
        print("🔒 Creating database constraints...")
        db.create_constraints()
        print("✅ Constraints created/verified")

        # Test creating a user
        print("👤 Creating test user...")
        user_id = db.create_user(
            email="test_user@example.com",
            username="testuser",
            password="hashedpassword123",
            role="user"
        )
        print(f"✅ User created with ID: {user_id}")

        # Test retrieving the user
        print("🔍 Retrieving test user...")
        user = db.get_user_by_email("test_user@example.com")
        if user:
            print(f"✅ User retrieved: {user['email']} - {user['username']} - {user['role']}")
        else:
            print("❌ User not found!")

        # Test retrieving all users
        print("📋 Retrieving all users...")
        # Let's check if there's a method to get all users (we might need to add this)
        with db.driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u")
            users = []
            for record in result:
                user_data = dict(record["u"])
                users.append(user_data)
                print(f"  - User: {user_data.get('email', 'N/A')}")

            print(f"✅ Found {len(users)} users in database")

        db.close()
        print("✅ Database connection closed")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = test_neo4j_connection()
    sys.exit(0 if success else 1)
