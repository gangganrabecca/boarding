"use client"

import { useState } from "react"
import { useAuth } from "../context/AuthContext"
import Navbar from "../components/Navbar"
import BookingForm from "../components/BookingForm"
import MyBookings from "../components/MyBookings"
import UserNotifications from "../components/UserNotifications"

export default function UserDashboard() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState("booking")

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-2">Welcome, {user?.username}</h1>
        <p className="text-text-muted mb-8">Manage your bookings and notifications</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <button
            onClick={() => setActiveTab("booking")}
            className={`p-6 rounded-lg border transition-all ${
              activeTab === "booking" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-2xl mb-2">📝</div>
            <h3 className="text-xl font-semibold mb-1">Booking</h3>
            <p className="text-text-muted text-sm">Book a new room</p>
          </button>

          <button
            onClick={() => setActiveTab("mybookings")}
            className={`p-6 rounded-lg border transition-all ${
              activeTab === "mybookings"
                ? "bg-primary/10 border-primary"
                : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-2xl mb-2">🏠</div>
            <h3 className="text-xl font-semibold mb-1">My Bookings</h3>
            <p className="text-text-muted text-sm">View and manage bookings</p>
          </button>

          <button
            onClick={() => setActiveTab("notifications")}
            className={`p-6 rounded-lg border transition-all ${
              activeTab === "notifications"
                ? "bg-primary/10 border-primary"
                : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-2xl mb-2">🔔</div>
            <h3 className="text-xl font-semibold mb-1">Notifications</h3>
            <p className="text-text-muted text-sm">Check your updates</p>
          </button>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          {activeTab === "booking" && <BookingForm />}
          {activeTab === "mybookings" && <MyBookings />}
          {activeTab === "notifications" && <UserNotifications />}
        </div>
      </div>
    </div>
  )
}
