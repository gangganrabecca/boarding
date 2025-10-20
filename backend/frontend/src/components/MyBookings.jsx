"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function MyBookings() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBookings()
  }, [])

  const fetchBookings = async () => {
    try {
      const response = await api.get("/bookings/my")
      setBookings(response.data)
    } catch (error) {
      console.error("Failed to fetch bookings:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (bookingId) => {
    if (!confirm("Are you sure you want to cancel this booking?")) return

    try {
      await api.delete(`/bookings/${bookingId}`)
      fetchBookings()
    } catch (error) {
      alert("Failed to cancel booking")
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "approved":
        return "text-primary"
      case "pending":
        return "text-yellow-500"
      case "rejected":
        return "text-red-500"
      case "cancelled":
        return "text-text-muted"
      default:
        return "text-text"
    }
  }

  if (loading) {
    return <div>Loading bookings...</div>
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">My Bookings</h2>

      {bookings.length === 0 ? (
        <p className="text-text-muted">No bookings yet</p>
      ) : (
        <div className="space-y-4">
          {bookings.map((booking) => (
            <div key={booking.id} className="bg-background border border-border rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg mb-2">
                    Room {booking.room.room_number} - {booking.room.room_type}
                  </h3>
                  <div className="space-y-1 text-sm text-text-muted">
                    <p>Start Date: {booking.start_date}</p>
                    <p>End Date: {booking.end_date}</p>
                    <p>Duration: {booking.duration} months</p>
                    <p>Price: ${booking.room.price}/month</p>
                    <p className={`font-medium ${getStatusColor(booking.status)}`}>
                      Status: {booking.status.toUpperCase()}
                    </p>
                  </div>
                </div>

                {booking.status === "pending" && (
                  <button
                    onClick={() => handleCancel(booking.id)}
                    className="px-4 py-2 bg-red-500/10 text-red-500 border border-red-500/50 rounded-lg hover:bg-red-500/20 transition-colors"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
