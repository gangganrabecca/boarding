"use client"

import { useState, useEffect } from "react"
import api from "../api"

export default function AdminNotifications() {
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

  const handleAction = async (notificationId, status) => {
    try {
      await api.put(`/notifications/${notificationId}`, { status })
      fetchNotifications()
    } catch (error) {
      alert("Failed to update notification")
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "approved":
        return "bg-primary/10 border-primary/50"
      case "rejected":
        return "bg-red-500/10 border-red-500/50"
      default:
        return "bg-yellow-500/10 border-yellow-500/50"
    }
  }

  if (loading) {
    return <div>Loading notifications...</div>
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Booking Requests</h2>

      {notifications.length === 0 ? (
        <p className="text-text-muted">No notifications</p>
      ) : (
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div key={notification.id} className={`border rounded-lg p-4 ${getStatusColor(notification.status)}`}>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="font-medium mb-1">{notification.message}</p>
                  <p className="text-sm text-text-muted mb-2">From: {notification.user.email}</p>
                  <p className="text-sm font-medium">Status: {notification.status.toUpperCase()}</p>
                </div>

                {notification.status === "pending" && (
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleAction(notification.id, "approved")}
                      className="px-4 py-2 bg-primary hover:bg-primary-hover text-white rounded-lg transition-colors"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => handleAction(notification.id, "rejected")}
                      className="px-4 py-2 bg-red-500/10 text-red-500 border border-red-500/50 rounded-lg hover:bg-red-500/20 transition-colors"
                    >
                      Reject
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
