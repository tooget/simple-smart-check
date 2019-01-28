import Cookies from 'js-cookie'

const TokenKey = 'user'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token, { expires: (1 / 1440) * 60 })
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}