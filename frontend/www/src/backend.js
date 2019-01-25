import axios from 'axios'

// 创建axios实例
const service = axios.create({
  baseURL: 'https://backend.smartcheck.ml/api', // api 的 base_url, http://localhost:5000/api
  timeout: 60000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  config => {
    const user = JSON.parse(localStorage.getItem('user'))

    if (user && user.access_token) {
      config.headers['Authorization'] = 'Bearer ' + user.access_token
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  response => {
    /**
     * code为非20000是抛错 可结合自己业务进行修改
     */
    if (response.status !== 200 || response.status !== 201) {
      // 50008:非法的token; 50012:其他客户端登录了;  50014:Token 过期了;
      if (response.status === 500 || response.status === 501 || response.status === 502 || response.status === 503) {
        return Promise.reject('response.status is not suitable')
      } else {
        return response
      }
    } else {
      return Promise.reject('response.status is undefined')
    }
  },
  error => {
    return Promise.reject(error)
  }
)

export default service
