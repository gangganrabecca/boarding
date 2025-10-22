"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function AvailableRooms({ onBookRoom }) {
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [filterType, setFilterType] = useState("all")

  useEffect(() => {
    fetchAvailableRooms()
  }, [])

  const fetchAvailableRooms = async () => {
    try {
      setLoading(true)
      setError("")
      const response = await api.get("/rooms")
      // Filter only available rooms
      const availableRooms = response.data.filter(room => room.status === "available")
      setRooms(availableRooms)
    } catch (error) {
      console.error("Failed to fetch rooms:", error)
      setError("Failed to load available rooms. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const filteredRooms = rooms.filter(room => {
    if (filterType === "all") return true
    return room.room_type.toLowerCase() === filterType.toLowerCase()
  })

  const handleBookNow = (room) => {
    if (onBookRoom) {
      onBookRoom(room)
    } else {
      // Fallback to DOM manipulation if no callback provided
      const bookingTab = document.querySelector('[data-tab="booking"]')
      if (bookingTab) {
        bookingTab.click()
        // Smooth scroll to booking form
        setTimeout(() => {
          const bookingForm = document.getElementById('booking-form')
          if (bookingForm) {
            bookingForm.scrollIntoView({ behavior: 'smooth' })
          }
        }, 100)
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-6 md:py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-6 w-6 md:h-8 md:w-8 border-b-2 border-primary mx-auto"></div>
          <p className="text-text-muted mt-2 text-sm md:text-base">Loading available rooms...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-6 md:py-8">
        <div className="text-3xl md:text-4xl mb-4">❌</div>
        <h3 className="text-lg md:text-xl font-semibold mb-2 text-red-600">Error Loading Rooms</h3>
        <p className="text-text-muted mb-4 text-sm md:text-base">{error}</p>
        <button
          onClick={fetchAvailableRooms}
          className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors text-sm md:text-base"
        >
          Try Again
        </button>
      </div>
    )
  }

  if (rooms.length === 0) {
    return (
      <div className="text-center py-6 md:py-8">
        <div className="text-4xl md:text-6xl mb-4">🏠</div>
        <h3 className="text-lg md:text-xl font-semibold mb-2">No Available Rooms</h3>
        <p className="text-text-muted text-sm md:text-base">There are currently no rooms available for booking. Please check back later.</p>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-4 md:mb-6">
        <h2 className="text-xl md:text-2xl font-bold mb-2">Available Rooms</h2>
        <p className="text-text-muted mb-4 text-sm md:text-base">Browse and select from our available rooms for your stay</p>

        {/* Room Type Filter */}
        <div className="flex flex-wrap gap-2 mb-4">
          <button
            onClick={() => setFilterType("all")}
            className={`px-3 py-2 rounded-lg text-xs md:text-sm font-medium transition-colors ${
              filterType === "all"
                ? "bg-primary text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            All Types
          </button>
          <button
            onClick={() => setFilterType("single")}
            className={`px-3 py-2 rounded-lg text-xs md:text-sm font-medium transition-colors ${
              filterType === "single"
                ? "bg-primary text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            Single
          </button>
          <button
            onClick={() => setFilterType("double")}
            className={`px-3 py-2 rounded-lg text-xs md:text-sm font-medium transition-colors ${
              filterType === "double"
                ? "bg-primary text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            Double
          </button>
          <button
            onClick={() => setFilterType("suite")}
            className={`px-3 py-2 rounded-lg text-xs md:text-sm font-medium transition-colors ${
              filterType === "suite"
                ? "bg-primary text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            Suite
          </button>
        </div>

        <p className="text-xs md:text-sm text-text-muted">
          Showing {filteredRooms.length} of {rooms.length} available rooms
        </p>
      </div>

      {filteredRooms.length === 0 ? (
        <div className="text-center py-6 md:py-8">
          <div className="text-3xl md:text-4xl mb-2">🔍</div>
          <p className="text-text-muted text-sm md:text-base">No rooms match your filter criteria.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
          {filteredRooms.map((room) => (
            <div key={room.id} className="bg-card border border-border rounded-lg overflow-hidden hover:shadow-lg transition-all duration-200 hover:-translate-y-1">
              <div className="p-4 md:p-6">
                <div className="flex items-center justify-between mb-3 md:mb-4">
                  <h3 className="text-lg md:text-xl font-semibold">Room {room.room_number}</h3>
                  <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs md:text-sm font-medium">
                    Available
                  </span>
                </div>

                <div className="space-y-2 md:space-y-3 mb-4 md:mb-6">
                  <div className="flex items-center text-text-muted text-sm">
                    <span className="font-medium mr-2">Type:</span>
                    <span className="capitalize">{room.room_type}</span>
                  </div>

                  <div className="flex items-center text-text-muted text-sm">
                    <span className="font-medium mr-2">Capacity:</span>
                    <span>{room.capacity} person{room.capacity > 1 ? 's' : ''}</span>
                  </div>

                  <div className="flex items-center text-text-muted text-sm">
                    <span className="font-medium mr-2">Price:</span>
                    <span className="text-base md:text-lg font-bold text-primary">₱{room.price.toLocaleString()}</span>
                    <span className="text-xs md:text-sm text-gray-500 ml-1">/month</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <button
                    onClick={() => handleBookNow(room)}
                    className="w-full bg-primary text-white py-2 md:py-3 px-4 rounded-lg hover:bg-primary/90 transition-colors font-medium text-sm md:text-base"
                  >
                    Book Now
                  </button>
                  <button
                    onClick={() => {
                      // Could add a "View Details" functionality here
                      alert(`Room ${room.room_number} details:\nType: ${room.room_type}\nCapacity: ${room.capacity}\nPrice: ₱${room.price}/month`)
                    }}
                    className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors text-xs md:text-sm"
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
