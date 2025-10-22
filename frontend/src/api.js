import axios from 'axios'

// Configure axios for development - use relative URLs to work with Vite proxy
// In production, this will use the deployed backend URL
const api = axios.create({
  baseURL: import.meta.env.DEV ? '/api' : (import.meta.env.VITE_API_URL || '/api'),
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add a request interceptor to handle proxy correctly
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Remove Content-Type header for FormData to let browser set it automatically
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add a response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error)

    // Handle authentication errors
    if (error.response?.status === 401) {
      // Clear token and redirect to login if needed
      localStorage.removeItem('token')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    // Handle database unavailable errors
    else if (error.response?.status === 503) {
      console.error('Database temporarily unavailable')
      // You could show a user-friendly message here
    }
    // Handle network errors (like connection timeout)
    else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      console.error('Network timeout - server might not be running')
      // For development, show a helpful error message
      if (import.meta.env.DEV) {
        console.error('💡 Make sure the backend server is running on port 8000')
      }
    }

    return Promise.reject(error)
  }
)

export default api
