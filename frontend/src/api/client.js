import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
})

export const setAuthToken = (token) => {
  if (token) {
    client.defaults.headers.common.Authorization = `Token ${token}`
  } else {
    delete client.defaults.headers.common.Authorization
  }
}

export default client
