"use client"

import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate("/login")
  }

  return (
    <nav className="bg-card border-b border-border">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold">Boardinghouse System</h1>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-text-muted">{user?.email}</span>
            <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">{user?.role}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500/10 text-red-500 border border-red-500/50 rounded-lg hover:bg-red-500/20 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
