"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function TenantsList() {
  const [tenants, setTenants] = useState([])
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    room_id: "",
  })

  useEffect(() => {
    fetchTenants()
    fetchRooms()
  }, [])

  const fetchTenants = async () => {
    try {
      const response = await api.get("/tenants")
      setTenants(response.data)
    } catch (error) {
      console.error("Failed to fetch tenants:", error)
    } finally {
      setLoading(false)
    }
  }

  const fetchRooms = async () => {
    try {
      const response = await api.get("/rooms")
      setRooms(response.data)
    } catch (error) {
      console.error("Failed to fetch rooms:", error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post("/tenants", formData)
      setShowForm(false)
      setFormData({ name: "", email: "", phone: "", room_id: "" })
      fetchTenants()
    } catch (error) {
      alert("Failed to create tenant")
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-6 md:py-8">
        <div className="animate-spin rounded-full h-6 w-6 md:h-8 md:w-8 border-b-2 border-primary"></div>
        <span className="ml-2 text-sm md:text-base">Loading tenants...</span>
      </div>
    )
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4 md:mb-6">
        <h2 className="text-xl md:text-2xl font-bold">Tenants</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-primary hover:bg-primary-hover text-white rounded-lg transition-colors text-sm md:text-base w-full sm:w-auto"
        >
          {showForm ? "Cancel" : "Add Tenant"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-background border border-border rounded-lg p-4 mb-6 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Phone</label>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Room</label>
              <select
                value={formData.room_id}
                onChange={(e) => setFormData({ ...formData, room_id: e.target.value })}
                className="w-full px-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                required
              >
                <option value="">Select a room</option>
                {rooms.map((room) => (
                  <option key={room.id} value={room.id}>
                    Room {room.room_number} - {room.room_type}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-primary hover:bg-primary-hover text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm md:text-base"
          >
            Add Tenant
          </button>
        </form>
      )}

      <div className="space-y-3 md:space-y-4">
        {tenants.map((tenant) => (
          <div key={tenant.id} className="bg-background border border-border rounded-lg p-4">
            <h3 className="font-semibold text-lg md:text-xl mb-2">{tenant.name}</h3>
            <div className="space-y-1 text-sm text-text-muted">
              <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4">
                <p><span className="font-medium">Email:</span> {tenant.email}</p>
                <p><span className="font-medium">Phone:</span> {tenant.phone}</p>
              </div>
              <p>
                <span className="font-medium">Room:</span> {tenant.room.room_number} - {tenant.room.room_type}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
