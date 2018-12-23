import axios from 'axios'

const HTTP = axios.create({
  baseURL: `https://backend.smartcheck.ml/api/`,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  }
})

// Request Interceptor
HTTP.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Bearer ' + localStorage.token
  return config
})

// Response Interceptor to handle and log errors
HTTP.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {

  fetchResource () {
    return HTTP.get(`resource/xxx`)
      .then(response => response.data)
  },

  fetchSecureResource () {
    return HTTP.get(`secure-resource/zzz`)
      .then(response => response.data)
  },

  fetchSecureResourceContract (email, className) {
    return HTTP.get(`secure-resource/contract`, {
      params: {
          email: email,
          className: className
      }
    })
      .then(response => response.data)
  }
}
