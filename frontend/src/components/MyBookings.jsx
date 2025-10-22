"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function MyBookings() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState({ type: "", text: "" })

  useEffect(() => {
    fetchBookings()
  }, [])

  const fetchBookings = async () => {
    try {
      setLoading(true)
      setMessage({ type: "", text: "" })
      const response = await api.get("/bookings/my")
      setBookings(response.data)
    } catch (error) {
      console.error("Failed to fetch bookings:", error)
      setMessage({
        type: "error",
        text: "Failed to load bookings. Please try again."
      })
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (bookingId) => {
    if (!confirm("Are you sure you want to cancel this booking? This action cannot be undone.")) return

    try {
      setMessage({ type: "info", text: "Cancelling booking..." })
      await api.delete(`/bookings/${bookingId}`)
      setMessage({
        type: "success",
        text: "Booking cancelled successfully!"
      })
      fetchBookings()
    } catch (error) {
      setMessage({
        type: "error",
        text: error.response?.data?.detail || "Failed to cancel booking"
      })
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "approved":
        return "bg-green-500/10 border-green-500/50 text-green-700"
      case "pending":
        return "bg-yellow-500/10 border-yellow-500/50 text-yellow-700"
      case "rejected":
        return "bg-red-500/10 border-red-500/50 text-red-700"
      case "cancelled":
        return "bg-gray-500/10 border-gray-500/50 text-gray-700"
      default:
        return "bg-gray-500/10 border-gray-500/50 text-gray-700"
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const calculateTotalPrice = (booking) => {
    return (booking.room.price * booking.duration).toLocaleString()
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-6 md:py-8">
        <div className="animate-spin rounded-full h-6 w-6 md:h-8 md:w-8 border-b-2 border-primary"></div>
        <span className="ml-2 text-sm md:text-base">Loading your bookings...</span>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-xl md:text-2xl font-bold mb-4 md:mb-6">My Bookings</h2>

      {message.text && (
        <div
          className={`px-3 py-2 md:px-4 md:py-3 rounded mb-4 ${
            message.type === "success"
              ? "bg-green-500/10 border border-green-500/50 text-green-700"
              : message.type === "error"
              ? "bg-red-500/10 border border-red-500/50 text-red-700"
              : "bg-blue-500/10 border border-blue-500/50 text-blue-700"
          }`}
        >
          {message.text}
        </div>
      )}

      {bookings.length === 0 ? (
        <div className="text-center py-6 md:py-8">
          <div className="text-3xl md:text-4xl mb-2">📅</div>
          <h3 className="text-lg md:text-xl font-semibold mb-2">No Bookings Yet</h3>
          <p className="text-text-muted mb-4 text-sm md:text-base">You haven't made any bookings yet. Browse available rooms to get started!</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors text-sm md:text-base"
          >
            Browse Available Rooms
          </button>
        </div>
      ) : (
        <div className="space-y-3 md:space-y-4">
          {bookings.map((booking) => (
            <div key={booking.id} className={`border rounded-lg p-4 md:p-6 ${getStatusColor(booking.status)}`}>
              <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                <div className="flex-1">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-3">
                    <h3 className="font-semibold text-lg md:text-xl">
                      Room {booking.room.room_number}
                    </h3>
                    <span className={`px-2 py-1 rounded-full text-xs md:text-sm font-medium w-fit ${
                      booking.status === "approved"
                        ? "bg-green-500/20 text-green-700"
                        : booking.status === "pending"
                        ? "bg-yellow-500/20 text-yellow-700"
                        : booking.status === "rejected"
                        ? "bg-red-500/20 text-red-700"
                        : "bg-gray-500/20 text-gray-700"
                    }`}>
                      {booking.status.toUpperCase()}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4 mb-4">
                    <div className="space-y-2">
                      <div className="flex items-center text-xs md:text-sm">
                        <span className="font-medium text-gray-600 mr-2">Type:</span>
                        <span className="capitalize">{booking.room.room_type}</span>
                      </div>
                      <div className="flex items-center text-xs md:text-sm">
                        <span className="font-medium text-gray-600 mr-2">Capacity:</span>
                        <span>{booking.room.capacity} person{booking.room.capacity > 1 ? 's' : ''}</span>
                      </div>
                      <div className="flex items-center text-xs md:text-sm">
                        <span className="font-medium text-gray-600 mr-2">Duration:</span>
                        <span>{booking.duration} month{booking.duration > 1 ? 's' : ''}</span>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center text-xs md:text-sm">
                        <span className="font-medium text-gray-600 mr-2">Check-in:</span>
                        <span>{formatDate(booking.start_date)}</span>
                      </div>
                      <div className="flex items-center text-xs md:text-sm">
                        <span className="font-medium text-gray-600 mr-2">Check-out:</span>
                        <span>{formatDate(booking.end_date)}</span>
                      </div>
                      <div className="flex items-center text-xs md:text-sm">
                        <span className="font-medium text-gray-600 mr-2">Monthly Rate:</span>
                        <span>₱{booking.room.price.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between pt-3 border-t border-gray-200 gap-2">
                    <div className="text-base md:text-lg font-bold">
                      Total: ₱{calculateTotalPrice(booking)}
                    </div>

                    <div className="text-xs text-gray-500">
                      Booked on {formatDate(booking.created_at)}
                    </div>
                  </div>
                </div>

                <div className="flex flex-col gap-2 lg:ml-4 lg:min-w-[120px]">
                  {booking.status === "pending" && (
                    <>
                      <button
                        onClick={() => handleCancel(booking.id)}
                        className="px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-xs md:text-sm w-full"
                      >
                        ✗ Cancel Booking
                      </button>
                      <span className="text-xs text-gray-500 text-center">Waiting for approval</span>
                    </>
                  )}

                  {booking.status === "approved" && (
                    <div className="text-center">
                      <div className="text-green-600 font-medium text-xs md:text-sm mb-1">✓ Approved</div>
                      <span className="text-xs text-gray-500">Your booking is confirmed</span>
                    </div>
                  )}

                  {booking.status === "rejected" && (
                    <div className="text-center">
                      <div className="text-red-600 font-medium text-xs md:text-sm mb-1">✗ Rejected</div>
                      <span className="text-xs text-gray-500">Contact admin for details</span>
                    </div>
                  )}

                  {booking.status === "cancelled" && (
                    <div className="text-center">
                      <div className="text-gray-600 font-medium text-xs md:text-sm mb-1">✗ Cancelled</div>
                      <span className="text-xs text-gray-500">Booking was cancelled</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
