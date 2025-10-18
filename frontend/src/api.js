import axios from 'axios'

// Configure axios for development - use relative URLs to work with Vite proxy
// In production, this will use the deployed backend URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add a request interceptor to handle proxy correctly
api.interceptors.request.use(
  (config) => {
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
    return Promise.reject(error)
  }
)

export default api
