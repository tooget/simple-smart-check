import request from '@/utils/request'

export function login(username, password) {
  const requestBody = new FormData()
  requestBody.append('username', username)
  requestBody.append('password', password)

  return request({
    url: '/users/login',
    method: 'post',
    data: requestBody
  })
}

export function logout() {
  return request({
    url: '/users/logout',
    method: 'post'
  })
}
