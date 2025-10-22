"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function RoomsList() {
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    room_number: "",
    room_type: "",
    capacity: 1,
    price: 0,
    status: "available",
  })

  useEffect(() => {
    fetchRooms()
  }, [])

  const fetchRooms = async () => {
    try {
      const response = await api.get("/rooms")
      setRooms(response.data)
    } catch (error) {
      console.error("Failed to fetch rooms:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post("/rooms", formData)
      setShowForm(false)
      setFormData({ room_number: "", room_type: "", capacity: 1, price: 0, status: "available" })
      fetchRooms()
    } catch (error) {
      alert("Failed to create room")
    }
  }

  const handleDelete = async (roomId) => {
    if (!confirm("Are you sure you want to delete this room?")) return

    try {
      await api.delete(`/rooms/${roomId}`)
      fetchRooms()
    } catch (error) {
      alert("Failed to delete room")
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "available":
        return "text-primary"
      case "occupied":
        return "text-yellow-500"
      case "maintenance":
        return "text-red-500"
      default:
        return "text-text"
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-6 md:py-8">
        <div className="animate-spin rounded-full h-6 w-6 md:h-8 md:w-8 border-b-2 border-primary"></div>
        <span className="ml-2 text-sm md:text-base">Loading rooms...</span>
      </div>
    )
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4 md:mb-6">
        <h2 className="text-xl md:text-2xl font-bold">Rooms</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-primary hover:bg-primary-hover text-white rounded-lg transition-colors text-sm md:text-base w-full sm:w-auto"
        >
          {showForm ? "Cancel" : "Add Room"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-background border border-border rounded-lg p-4 mb-6 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Room Number</label>
              <input
                type="text"
                value={formData.room_number}
                onChange={(e) => setFormData({ ...formData, room_number: e.target.value })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Room Type</label>
              <input
                type="text"
                value={formData.room_type}
                onChange={(e) => setFormData({ ...formData, room_type: e.target.value })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Capacity</label>
              <input
                type="number"
                min="1"
                value={formData.capacity}
                onChange={(e) => setFormData({ ...formData, capacity: Number.parseInt(e.target.value) })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Price (per month)</label>
              <input
                type="number"
                min="0"
                step="0.01"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: Number.parseFloat(e.target.value) })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-primary hover:bg-primary-hover text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm md:text-base"
          >
            Create Room
          </button>
        </form>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
        {rooms.filter(room => room && room.id).map((room) => (
          <div key={room.id} className="bg-background border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-3">
              <h3 className="font-semibold text-lg md:text-xl">Room {room.room_number || 'Unknown'}</h3>
              <button
                onClick={() => handleDelete(room.id)}
                className="text-red-500 hover:text-red-400 text-xs md:text-sm px-2 py-1 rounded hover:bg-red-50 transition-colors"
              >
                Delete
              </button>
            </div>
            <div className="space-y-1 text-sm text-text-muted">
              <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4">
                <p><span className="font-medium">Type:</span> {room.room_type || 'N/A'}</p>
                <p><span className="font-medium">Capacity:</span> {room.capacity || 0} person(s)</p>
              </div>
              <p><span className="font-medium">Price:</span> ₱{room.price || 0}/month</p>
              <p className={`font-medium ${getStatusColor(room.status)}`}>
                Status: {room.status ? room.status.toUpperCase() : 'UNKNOWN'}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
