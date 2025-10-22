"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function BookingForm({ preselectedRoom = null, onBookingSuccess }) {
  const [rooms, setRooms] = useState([])
  const [formData, setFormData] = useState({
    room_id: preselectedRoom?.id || "",
    start_date: "",
    end_date: "",
    duration: 1,
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: "", text: "" })

  useEffect(() => {
    fetchRooms()
    // If a room is preselected, set it in the form
    if (preselectedRoom) {
      setFormData(prev => ({ ...prev, room_id: preselectedRoom.id }))
    }
  }, [preselectedRoom])

  useEffect(() => {
    // Auto-calculate duration when dates change
    if (formData.start_date && formData.end_date) {
      const startDate = new Date(formData.start_date)
      const endDate = new Date(formData.end_date)
      const diffTime = Math.abs(endDate - startDate)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      const diffMonths = Math.max(1, Math.ceil(diffDays / 30))

      if (diffMonths !== formData.duration) {
        setFormData(prev => ({ ...prev, duration: diffMonths }))
      }
    }
  }, [formData.start_date, formData.end_date])

  const handleDateChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))

    // Clear duration if dates are invalid
    if (field === 'start_date' || field === 'end_date') {
      const startDate = field === 'start_date' ? new Date(value) : new Date(formData.start_date)
      const endDate = field === 'end_date' ? new Date(value) : new Date(formData.end_date)

      if (startDate && endDate && startDate >= endDate) {
        setMessage({ type: "error", text: "End date must be after start date" })
      } else {
        setMessage({ type: "", text: "" })
      }
    }
  }

  const fetchRooms = async () => {
    try {
      const response = await api.get("/rooms")
      setRooms(response.data.filter((room) => room.status === "available"))
    } catch (error) {
      console.error("Failed to fetch rooms:", error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ type: "", text: "" })

    // Validate dates
    if (formData.start_date && formData.end_date) {
      const startDate = new Date(formData.start_date)
      const endDate = new Date(formData.end_date)

      if (startDate >= endDate) {
        setMessage({ type: "error", text: "End date must be after start date" })
        setLoading(false)
        return
      }
    }

    try {
      await api.post("/bookings", formData)
      setMessage({ type: "success", text: "Booking created successfully! Waiting for admin approval." })
      setFormData({ room_id: "", start_date: "", end_date: "", duration: 1 })

      // Call success callback if provided
      if (onBookingSuccess) {
        onBookingSuccess()
      }

      fetchRooms()
    } catch (error) {
      setMessage({
        type: "error",
        text: error.response?.data?.detail || "Failed to create booking",
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div id="booking-form">
      <h2 className="text-xl md:text-2xl font-bold mb-4 md:mb-6">Book a Room</h2>

      {message.text && (
        <div
          className={`px-3 py-2 md:px-4 md:py-3 rounded mb-4 ${
            message.type === "success"
              ? "bg-primary/10 border border-primary/50 text-primary"
              : "bg-red-500/10 border border-red-500/50 text-red-500"
          }`}
        >
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4 md:space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">Select Room</label>
          <select
            value={formData.room_id}
            onChange={(e) => setFormData({ ...formData, room_id: e.target.value })}
            className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            required
          >
            <option value="">Choose a room</option>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                Room {room.room_number} - {room.room_type} (${room.price}/month)
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Start Date</label>
            <input
              type="date"
              value={formData.start_date}
              onChange={(e) => handleDateChange('start_date', e.target.value)}
              min={new Date().toISOString().split('T')[0]}
              className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">End Date</label>
            <input
              type="date"
              value={formData.end_date}
              onChange={(e) => handleDateChange('end_date', e.target.value)}
              min={formData.start_date || new Date().toISOString().split('T')[0]}
              className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Duration (months)</label>
          <input
            type="number"
            min="1"
            value={formData.duration}
            onChange={(e) => setFormData({ ...formData, duration: Number.parseInt(e.target.value) })}
            className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            required
            readOnly
          />
          <p className="text-xs text-text-muted mt-1">Auto-calculated based on selected dates</p>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary hover:bg-primary-hover text-white font-medium py-3 px-4 rounded-lg transition-colors disabled:opacity-50 text-sm md:text-base"
        >
          {loading ? "Submitting..." : "Submit Booking"}
        </button>
      </form>
    </div>
  )
}
