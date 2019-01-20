import axios from 'axios'

export const HTTP = axios.create({
    baseURL: `https://backend.smartcheck.ml/api`,
    timeout: 5000,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
})

// Request Interceptor
HTTP.interceptors.request.use(function (config) {
  let user = JSON.parse(localStorage.getItem('user'));
  
  if (user && user.access_token) {
      config.headers['Authorization'] = 'Bearer ' + user.access_token;
      return config;
  } else {
      return {};
  }
})

// Response Interceptor to handle and log errors
HTTP.interceptors.response.use(function (response) {
    return response
  }, function (error) {
    // Handle Error
    console.log(error)
    return Promise.reject(error)
})