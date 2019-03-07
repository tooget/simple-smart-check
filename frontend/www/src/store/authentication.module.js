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
          const result = JSON.parse(response.data.usersLogin.result)
          setToken(result.accessToken)
          commit('SET_TOKEN', result.accessToken)
          commit('SET_USERNAME', result.username)
          resolve()
          router.push('/')
        }).catch(error => {
          dispatch('alert/error', error.graphQLErrors[0].message, { root: true });
          reject(error)
        })
      })
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        userService.logout().then(() => {
          commit('SET_TOKEN', undefined)
          removeToken()
          resolve()
          router.push('/login');
        }).catch(error => {
          reject(error)
        })            
      })
    }
  }
}