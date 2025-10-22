"use client"

import { useState } from "react"
import { useAuth } from "../context/AuthContext"
import Navbar from "../components/Navbar"
import TenantsList from "../components/TenantsList"
import RoomsList from "../components/RoomsList"
import AdminNotifications from "../components/AdminNotifications"
import DashboardOverview from "../components/DashboardOverview"

export default function AdminDashboard() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState("overview")

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl md:text-3xl font-bold mb-2">Admin Dashboard</h1>
        <p className="text-text-muted mb-6 md:mb-8">Manage tenants, rooms, and bookings</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
          <button
            onClick={() => setActiveTab("overview")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "overview" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">📊</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Overview</h3>
            <p className="text-text-muted text-xs md:text-sm">System statistics</p>
          </button>

          <button
            onClick={() => setActiveTab("tenants")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "tenants" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">👥</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Tenants</h3>
            <p className="text-text-muted text-xs md:text-sm">Manage tenant information</p>
          </button>

          <button
            onClick={() => setActiveTab("rooms")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "rooms" ? "bg-primary/10 border-primary" : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">🏢</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Rooms</h3>
            <p className="text-text-muted text-xs md:text-sm">Manage room inventory</p>
          </button>

          <button
            onClick={() => setActiveTab("notifications")}
            className={`p-4 md:p-6 rounded-lg border transition-all ${
              activeTab === "notifications"
                ? "bg-primary/10 border-primary"
                : "bg-card border-border hover:border-primary/50"
            }`}
          >
            <div className="text-xl md:text-2xl mb-2">📬</div>
            <h3 className="text-lg md:text-xl font-semibold mb-1">Notifications</h3>
            <p className="text-text-muted text-xs md:text-sm">Review booking requests</p>
          </button>
        </div>

        <div className="bg-card border border-border rounded-lg p-4 md:p-6">
          {activeTab === "overview" && <DashboardOverview userRole="admin" />}
          {activeTab === "tenants" && <TenantsList />}
          {activeTab === "rooms" && <RoomsList />}
          {activeTab === "notifications" && <AdminNotifications />}
        </div>
      </div>
    </div>
  )
}
