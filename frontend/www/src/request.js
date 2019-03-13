import axios from 'axios'
import store from './store'
import { getToken } from './helpers/auth-header'

const baseURL = (process.env.NODE_ENV !== 'production') 
  ? 'http://localhost:5000/api/' 
  : 'https://backend.smartcheck.gq/api'

// 创建axios实例
const service = axios.create({
  baseURL: baseURL,
  timeout: 60000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  config => {
    if (store.getters.token) {
      config.headers['Authorization'] = 'Bearer ' + getToken() // 让每个请求携带自定义token 请根据实际情况自行修改
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
        MessageBox.confirm(
          '你已被登出，可以取消继续留在该页面，或者重新登录',
          '确定登出',
          {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
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