"use client"

import { useState } from "react"
import { useAuth } from "../context/AuthContext"
import Navbar from "../components/Navbar"
import TenantsList from "../components/TenantsList"
import RoomsList from "../components/RoomsList"
import AdminNotifications from "../components/AdminNotifications"

export default function AdminDashboard() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState("tenants")

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
        <p className="text-text-muted mb-8">Manage tenants, rooms, and bookings</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <button
            onClick={() => setActiveTab("tenants")}
            className={`p-6 rounded-lg border transition-all ${
              activeTab === "tenants" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-2xl mb-2">👥</div>
            <h3 className="text-xl font-semibold mb-1">Tenants</h3>
            <p className="text-text-muted text-sm">Manage tenant information</p>
          </button>

          <button
            onClick={() => setActiveTab("rooms")}
            className={`p-6 rounded-lg border transition-all ${
              activeTab === "rooms" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-2xl mb-2">🏢</div>
            <h3 className="text-xl font-semibold mb-1">Rooms</h3>
            <p className="text-text-muted text-sm">Manage room inventory</p>
          </button>

          <button
            onClick={() => setActiveTab("notifications")}
            className={`p-6 rounded-lg border transition-all ${
              activeTab === "notifications"
                ? "bg-primary/10 border-primary"
                : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-2xl mb-2">📬</div>
            <h3 className="text-xl font-semibold mb-1">Notifications</h3>
            <p className="text-text-muted text-sm">Review booking requests</p>
          </button>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          {activeTab === "tenants" && <TenantsList />}
          {activeTab === "rooms" && <RoomsList />}
          {activeTab === "notifications" && <AdminNotifications />}
        </div>
      </div>
    </div>
  )
}
