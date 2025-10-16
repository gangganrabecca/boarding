"use client"

import { createContext, useContext, useState, useEffect } from "react"
import api from "../api"

const AuthContext = createContext()

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem("token"))

  useEffect(() => {
    if (token) {
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [token])

  const fetchUser = async () => {
    try {
      const response = await api.get("/auth/me")
      setUser(response.data)
    } catch (error) {
      console.error("Failed to fetch user:", error)
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const formData = new FormData()
    formData.append("username", email)
    formData.append("password", password)

    const response = await api.post("/auth/login", formData)
    const { access_token } = response.data

    localStorage.setItem("token", access_token)
    setToken(access_token)
    api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`

    await fetchUser()
  }

  const register = async (email, username, password, role = "user") => {
    const response = await api.post("/auth/register", {
      email,
      username,
      password,
      role,
    })
    const { access_token } = response.data

    localStorage.setItem("token", access_token)
    setToken(access_token)
    api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`

    await fetchUser()
  }

  const logout = () => {
    localStorage.removeItem("token")
    setToken(null)
    setUser(null)
    delete api.defaults.headers.common["Authorization"]
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
