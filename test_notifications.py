#!/usr/bin/env python3
"""
Test script to verify notification approval/rejection functionality
"""
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

# Test configuration
BACKEND_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@boardinghouse.com"
ADMIN_PASSWORD = "admin123"

def test_authentication():
    """Test login and get token"""
    print("🔐 Testing authentication...")

    response = requests.post(f"{BACKEND_URL}/api/auth/login", data={
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })

    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Authentication successful! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Authentication failed: {response.status_code} - {response.text}")
        return None

def test_notifications(token):
    """Test getting notifications"""
    print("📋 Testing notifications retrieval...")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BACKEND_URL}/api/notifications", headers=headers)

    if response.status_code == 200:
        notifications = response.json()
        print(f"✅ Found {len(notifications)} notifications")
        return notifications
    else:
        print(f"❌ Failed to get notifications: {response.status_code} - {response.text}")
        return []

def test_notification_approval(token, notification_id):
    """Test approving a notification"""
    print(f"✅ Testing notification approval for ID: {notification_id}")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{BACKEND_URL}/api/notifications/{notification_id}",
        json={"status": "approved"},
        headers=headers
    )

    if response.status_code == 200:
        print(f"✅ Notification {notification_id} approved successfully!")
        return True
    else:
        print(f"❌ Failed to approve notification: {response.status_code} - {response.text}")
        return False

def test_notification_rejection(token, notification_id):
    """Test rejecting a notification"""
    print(f"❌ Testing notification rejection for ID: {notification_id}")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{BACKEND_URL}/api/notifications/{notification_id}",
        json={"status": "rejected"},
        headers=headers
    )

    if response.status_code == 200:
        print(f"✅ Notification {notification_id} rejected successfully!")
        return True
    else:
        print(f"❌ Failed to reject notification: {response.status_code} - {response.text}")
        return False

def main():
    print("🧪 Starting notification functionality test...\n")

    # Test 1: Authentication
    token = test_authentication()
    if not token:
        print("❌ Cannot proceed without authentication")
        return

    print()

    # Test 2: Get notifications
    notifications = test_notifications(token)
    if not notifications:
        print("❌ No notifications found to test")
        return

    print()

    # Test 3: Test approval/rejection on first notification
    first_notification = notifications[0]
    notification_id = first_notification.get('id')
    current_status = first_notification.get('status')

    print(f"📋 First notification: ID={notification_id}, Status={current_status}")

    if current_status == "pending":
        # Test approval
        if test_notification_approval(token, notification_id):
            print("✅ Approval test passed!")

        # Test rejection (this will fail since it's already approved, but that's expected)
        if test_notification_rejection(token, notification_id):
            print("❌ Unexpected: Rejection succeeded on approved notification")
        else:
            print("✅ Rejection correctly failed on approved notification")
    else:
        print(f"⚠️ First notification is not pending (status: {current_status}), skipping approval/rejection test")

    print("\n🎉 Test completed!")

if __name__ == "__main__":
    main()
