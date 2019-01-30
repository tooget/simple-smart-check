import { userService } from '../services';
import { router } from '../helpers';
import { getToken, setToken, removeToken } from '../helpers/auth-header'

export const authentication = {
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
    login({ dispatch, commit }, { username, password }) {
      return new Promise((resolve, reject) => {
        userService.login(username, password).then(response => {
          const data = response.data
          setToken(data.return.access_token)
          commit('SET_TOKEN', data.return.access_token)
          commit('SET_USERNAME', data.username)
          resolve()
          router.push('/')
        }).catch(error => {
          dispatch('alert/error', error.response.data.message, { root: true });
          reject(error)
        })
      })
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        userService.logout().then(() => {
          resolve()
          router.push('/login');
        }).catch(error => {
          reject(error)
        })            
      })
    }
  }
}