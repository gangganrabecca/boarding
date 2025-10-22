"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function UserNotifications() {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchNotifications()
  }, [])

  const fetchNotifications = async () => {
    try {
      const response = await api.get("/notifications")
      setNotifications(response.data)
    } catch (error) {
      console.error("Failed to fetch notifications:", error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "approved":
        return "bg-primary/10 border-primary/50 text-primary"
      case "rejected":
        return "bg-red-500/10 border-red-500/50 text-red-500"
      default:
        return "bg-yellow-500/10 border-yellow-500/50 text-yellow-500"
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-6 md:py-8">
        <div className="animate-spin rounded-full h-6 w-6 md:h-8 md:w-8 border-b-2 border-primary"></div>
        <span className="ml-2 text-sm md:text-base">Loading notifications...</span>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-xl md:text-2xl font-bold mb-4 md:mb-6">Notifications</h2>

      {notifications.length === 0 ? (
        <div className="text-center py-6 md:py-8">
          <div className="text-3xl md:text-4xl mb-2">🔔</div>
          <p className="text-text-muted text-sm md:text-base">No notifications yet</p>
        </div>
      ) : (
        <div className="space-y-3 md:space-y-4">
          {notifications.map((notification) => (
            <div key={notification.id} className={`border rounded-lg p-3 md:p-4 ${getStatusColor(notification.status)}`}>
              <p className="font-medium mb-2 text-sm md:text-base">{notification.message}</p>
              <p className="text-xs md:text-sm opacity-75">
                Status: {notification.status.toUpperCase()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
