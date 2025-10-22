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

  const [message, setMessage] = useState({ type: "", text: "" })

  const handleAction = async (notificationId, status) => {
    try {
      setMessage({ type: "info", text: `${status === "approved" ? "Approving" : "Rejecting"} booking...` })
      await api.put(`/notifications/${notificationId}`, { status })
      setMessage({
        type: "success",
        text: `Booking ${status} successfully!`
      })
      fetchNotifications()
    } catch (error) {
      setMessage({
        type: "error",
        text: error.response?.data?.detail || "Failed to update booking status",
      })
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "approved":
        return "bg-green-500/10 border-green-500/50 text-green-700"
      case "rejected":
        return "bg-red-500/10 border-red-500/50 text-red-700"
      case "pending":
        return "bg-yellow-500/10 border-yellow-500/50 text-yellow-700"
      default:
        return "bg-gray-500/10 border-gray-500/50 text-gray-700"
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        <span className="ml-2">Loading notifications...</span>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-xl md:text-2xl font-bold mb-4 md:mb-6">Booking Requests</h2>

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

      {notifications.length === 0 ? (
        <div className="text-center py-6 md:py-8">
          <div className="text-3xl md:text-4xl mb-2">📭</div>
          <p className="text-text-muted">No booking requests yet</p>
        </div>
      ) : (
        <div className="space-y-3 md:space-y-4">
          {notifications.map((notification) => (
            <div key={notification.id} className={`border rounded-lg p-3 md:p-4 ${getStatusColor(notification.status)}`}>
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
                <div className="flex-1">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                    <p className="font-medium text-sm md:text-base">{notification.message}</p>
                    <span className={`px-2 py-1 text-xs rounded-full w-fit ${
                      notification.status === "pending"
                        ? "bg-yellow-500/20 text-yellow-700"
                        : notification.status === "approved"
                        ? "bg-green-500/20 text-green-700"
                        : "bg-red-500/20 text-red-700"
                    }`}>
                      {notification.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs md:text-sm text-gray-600 mb-1">From: {notification.user?.username || notification.user?.email}</p>
                  <p className="text-xs text-gray-500">
                    {formatDate(notification.created_at)}
                    {notification.booking_id && ` • Booking ID: ${notification.booking_id}`}
                  </p>
                </div>

                {notification.status === "pending" && (
                  <div className="flex gap-2 sm:ml-4">
                    <button
                      onClick={() => handleAction(notification.id, "approved")}
                      className="px-3 py-2 md:px-4 md:py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors text-xs md:text-sm flex-1 sm:flex-none"
                    >
                      ✓ Approve
                    </button>
                    <button
                      onClick={() => handleAction(notification.id, "rejected")}
                      className="px-3 py-2 md:px-4 md:py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-xs md:text-sm flex-1 sm:flex-none"
                    >
                      ✗ Reject
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
