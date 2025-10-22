"use client"

import { useState } from "react"
import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate("/login")
  }

  return (
    <nav className="bg-card border-b border-border">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-lg md:text-xl font-bold">Boardinghouse System</h1>
          </div>

          {/* Desktop menu */}
          <div className="hidden md:flex items-center gap-4">
            <span className="text-text-muted">{user?.email}</span>
            <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">{user?.role}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500/10 text-red-500 border border-red-500/50 rounded-lg hover:bg-red-500/20 transition-colors"
            >
              Logout
            </button>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div className="w-6 h-6 flex flex-col justify-center">
              <span className={`block h-0.5 w-6 bg-current transform transition-all duration-300 ${isMobileMenuOpen ? 'rotate-45 translate-y-1' : '-translate-y-1'}`}></span>
              <span className={`block h-0.5 w-6 bg-current transform transition-all duration-300 ${isMobileMenuOpen ? 'opacity-0' : 'opacity-100'}`}></span>
              <span className={`block h-0.5 w-6 bg-current transform transition-all duration-300 ${isMobileMenuOpen ? '-rotate-45 -translate-y-1' : 'translate-y-1'}`}></span>
            </div>
          </button>
        </div>

        {/* Mobile menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-border py-4">
            <div className="flex flex-col gap-3">
              <div className="flex flex-col gap-2">
                <span className="text-text-muted text-sm">{user?.email}</span>
                <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm w-fit">{user?.role}</span>
              </div>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-500/10 text-red-500 border border-red-500/50 rounded-lg hover:bg-red-500/20 transition-colors w-fit"
              >
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
