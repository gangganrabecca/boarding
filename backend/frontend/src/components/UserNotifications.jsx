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
    return <div>Loading notifications...</div>
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Notifications</h2>

      {notifications.length === 0 ? (
        <p className="text-text-muted">No notifications</p>
      ) : (
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div key={notification.id} className={`border rounded-lg p-4 ${getStatusColor(notification.status)}`}>
              <p className="font-medium mb-1">{notification.message}</p>
              <p className="text-sm opacity-75">Status: {notification.status.toUpperCase()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
