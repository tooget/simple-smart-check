import { login, logout } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/auth'

const user = {
  state: {
    token: getToken(),
    username: ''
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_USERNAME: (state, username) => {
      state.name = username
    }
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      var CryptoJS = require('crypto-js')
      const username = userInfo.username
      const password = CryptoJS.PBKDF2(userInfo.password, 'AnyKey', { iterations: 1, keySize: 256 / 32, hasher: CryptoJS.algo.SHA256 }).toString(CryptoJS.enc.Base64)
      return new Promise((resolve, reject) => {
        login(username, password).then(response => {
          const result = JSON.parse(response.data.usersLogin.result)
          setToken(result.accessToken)
          commit('SET_TOKEN', result.accessToken)
          commit('SET_USERNAME', result.username)
          resolve()
        }).catch(error => {
          console.log(error.graphQLErrors[0].message)
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        logout(state.token).then(() => {
          commit('SET_TOKEN', '')
          removeToken()
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    }
  }
}

export default user
