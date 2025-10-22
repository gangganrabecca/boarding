#!/usr/bin/env python3
"""
Minimal test script to check database connection and notification functionality
"""
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

try:
    from database import Neo4jConnection

    # Test database connection
    print("🔗 Testing database connection...")
    db = Neo4jConnection(
        uri=os.getenv("NEO4J_URI"),
        user=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    print("🔌 Connecting to database...")
    db.connect()

    # Test basic query
    print("✅ Testing basic query...")
    with db.driver.session() as session:
        result = session.run("RETURN 'Database operational' as status")
        record = result.single()
        print(f"📊 Database status: {record['status']}")

    # Test notifications
    print("🔔 Testing notifications...")
    notifications = db.get_all_notifications()
    print(f"📋 Found {len(notifications)} notifications")

    for notif in notifications[:3]:  # Show first 3
        print(f"  - ID: {notif.get('id')}, Status: {notif.get('status')}, Message: {notif.get('message', '')[:50]}...")

    print("✅ Database and notifications test completed successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
