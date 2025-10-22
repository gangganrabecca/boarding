"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function DashboardOverview({ userRole, showTitle = false }) {
  const [stats, setStats] = useState({
    totalRooms: 0,
    availableRooms: 0,
    occupiedRooms: 0,
    totalBookings: 0,
    pendingBookings: 0,
    approvedBookings: 0,
    totalTenants: 0,
    totalNotifications: 0,
    pendingNotifications: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [userRole])

  const fetchStats = async () => {
    try {
      setLoading(true)

      // Fetch rooms data
      const roomsResponse = await api.get("/rooms")
      const rooms = roomsResponse.data

      // Fetch bookings data (based on user role)
      let bookingsResponse
      if (userRole === "admin") {
        // Admin can see all bookings via notifications endpoint
        bookingsResponse = await api.get("/notifications")
        const notifications = bookingsResponse.data
        const bookings = notifications.filter(n => n.booking_id).map(n => ({ id: n.booking_id, status: n.status }))
        bookingsResponse = { data: bookings }
      } else {
        // User can only see their own bookings
        bookingsResponse = await api.get("/bookings/my")
      }
      const bookings = bookingsResponse.data

      // Fetch tenants data (admin only)
      let tenantsResponse = { data: [] }
      if (userRole === "admin") {
        tenantsResponse = await api.get("/tenants")
      }
      const tenants = tenantsResponse.data

      // Calculate statistics
      const newStats = {
        totalRooms: rooms.length,
        availableRooms: rooms.filter(room => room.status === "available").length,
        occupiedRooms: rooms.filter(room => room.status === "occupied").length,
        totalBookings: bookings.length,
        pendingBookings: bookings.filter(booking => booking.status === "pending").length,
        approvedBookings: bookings.filter(booking => booking.status === "approved").length,
        totalTenants: tenants.length,
        totalNotifications: userRole === "admin" ? bookingsResponse.data.length : 0,
        pendingNotifications: bookings.filter(booking => booking.status === "pending").length
      }

      setStats(newStats)
    } catch (error) {
      console.error("Failed to fetch dashboard stats:", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-card border border-border rounded-lg p-4 md:p-6 animate-pulse">
            <div className="h-3 md:h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-6 md:h-8 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  const adminStats = [
    {
      title: "Total Rooms",
      value: stats.totalRooms,
      icon: "🏠",
      color: "text-blue-600",
      bgColor: "bg-blue-50"
    },
    {
      title: "Available Rooms",
      value: stats.availableRooms,
      icon: "✅",
      color: "text-green-600",
      bgColor: "bg-green-50"
    },
    {
      title: "Occupied Rooms",
      value: stats.occupiedRooms,
      icon: "🏡",
      color: "text-orange-600",
      bgColor: "bg-orange-50"
    },
    {
      title: "Total Tenants",
      value: stats.totalTenants,
      icon: "👥",
      color: "text-purple-600",
      bgColor: "bg-purple-50"
    }
  ]

  const userStats = [
    {
      title: "My Bookings",
      value: stats.totalBookings,
      icon: "📅",
      color: "text-blue-600",
      bgColor: "bg-blue-50"
    },
    {
      title: "Approved",
      value: stats.approvedBookings,
      icon: "✅",
      color: "text-green-600",
      bgColor: "bg-green-50"
    },
    {
      title: "Pending",
      value: stats.pendingBookings,
      icon: "⏳",
      color: "text-yellow-600",
      bgColor: "bg-yellow-50"
    },
    {
      title: "Available Rooms",
      value: stats.availableRooms,
      icon: "🏠",
      color: "text-green-600",
      bgColor: "bg-green-50"
    }
  ]

  const displayStats = userRole === "admin" ? adminStats : userStats

  return (
    <div>
      {showTitle && <h2 className="text-xl md:text-2xl font-bold mb-4 md:mb-6">System Overview</h2>}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {displayStats.map((stat, index) => (
          <div key={index} className="bg-card border border-border rounded-lg p-4 md:p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs md:text-sm font-medium text-text-muted mb-1">{stat.title}</p>
                <p className="text-2xl md:text-3xl font-bold">{stat.value}</p>
              </div>
              <div className={`w-10 h-10 md:w-12 md:h-12 ${stat.bgColor} rounded-lg flex items-center justify-center text-xl md:text-2xl`}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
