"use client"

import { useState } from "react"
import { useAuth } from "../context/AuthContext"
import Navbar from "../components/Navbar"
import BookingForm from "../components/BookingForm"
import MyBookings from "../components/MyBookings"
import UserNotifications from "../components/UserNotifications"
import AvailableRooms from "../components/AvailableRooms"
import DashboardOverview from "../components/DashboardOverview"

export default function UserDashboard() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState("overview")
  const [preselectedRoom, setPreselectedRoom] = useState(null)

  const handleBookRoom = (room) => {
    // Switch to booking tab and pre-fill the form with the selected room
    setPreselectedRoom(room)
    setActiveTab("booking")
    // Smooth scroll to booking form
    setTimeout(() => {
      const bookingForm = document.getElementById('booking-form')
      if (bookingForm) {
        bookingForm.scrollIntoView({ behavior: 'smooth' })
      }
    }, 100)
  }

  const handleBookingSuccess = () => {
    // Clear preselected room after successful booking
    setPreselectedRoom(null)
    setActiveTab("overview")
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl md:text-3xl font-bold mb-2">Welcome, {user?.username}</h1>
        <p className="text-text-muted mb-6 md:mb-8">Manage your bookings and notifications</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 md:gap-6 mb-6 md:mb-8">
          <button
            onClick={() => setActiveTab("overview")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "overview" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">📊</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Overview</h3>
            <p className="text-text-muted text-xs md:text-sm">My statistics</p>
          </button>

          <button
            onClick={() => setActiveTab("available")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "available" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">🏠</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Available Rooms</h3>
            <p className="text-text-muted text-xs md:text-sm">Browse available rooms</p>
          </button>

          <button
            onClick={() => setActiveTab("booking")}
            data-tab="booking"
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "booking" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">📝</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Booking</h3>
            <p className="text-text-muted text-xs md:text-sm">Book a new room</p>
          </button>

          <button
            onClick={() => setActiveTab("mybookings")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "mybookings"
                ? "bg-primary/10 border-primary"
                : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">📅</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">My Bookings</h3>
            <p className="text-text-muted text-xs md:text-sm">View and manage bookings</p>
          </button>

          <button
            onClick={() => setActiveTab("notifications")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "notifications"
                ? "bg-primary/10 border-primary"
                : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">🔔</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Notifications</h3>
            <p className="text-text-muted text-xs md:text-sm">Check your updates</p>
          </button>
        </div>

        <div className="bg-card border border-border rounded-lg p-4 md:p-6">
          {activeTab === "overview" && <DashboardOverview userRole="user" />}
          {activeTab === "available" && <AvailableRooms onBookRoom={handleBookRoom} />}
          {activeTab === "booking" && <BookingForm preselectedRoom={preselectedRoom} onBookingSuccess={handleBookingSuccess} />}
          {activeTab === "mybookings" && <MyBookings />}
          {activeTab === "notifications" && <UserNotifications />}
        </div>
      </div>
    </div>
  )
}
