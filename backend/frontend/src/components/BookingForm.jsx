"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function BookingForm() {
  const [rooms, setRooms] = useState([])
  const [formData, setFormData] = useState({
    room_id: "",
    start_date: "",
    end_date: "",
    duration: 1,
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: "", text: "" })

  useEffect(() => {
    fetchRooms()
  }, [])

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

    try {
      await api.post("/bookings", formData)
      setMessage({ type: "success", text: "Booking created successfully! Waiting for admin approval." })
      setFormData({ room_id: "", start_date: "", end_date: "", duration: 1 })
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
    <div>
      <h2 className="text-2xl font-bold mb-6">Book a Room</h2>

      {message.text && (
        <div
          className={`px-4 py-3 rounded mb-4 ${
            message.type === "success"
              ? "bg-primary/10 border border-primary/50 text-primary"
              : "bg-red-500/10 border border-red-500/50 text-red-500"
          }`}
        >
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
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
              onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
              className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">End Date</label>
            <input
              type="date"
              value={formData.end_date}
              onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
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
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary hover:bg-primary-hover text-white font-medium py-2 px-4 rounded-lg transition-colors disabled:opacity-50"
        >
          {loading ? "Submitting..." : "Submit Booking"}
        </button>
      </form>
    </div>
  )
}
