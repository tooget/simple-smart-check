import request from '../request'

export const userService = {
    login,
    logout
};

function login(username, password) {
    const requestBody = new FormData()
    requestBody.append('username', username)
    requestBody.append('password', password)

    return request({
        url: '/users/login',
        method: 'post',
        data: requestBody
    })
}

function logout() {
    // remove user from local storage to log user out
    return request({
        url: '/users/logout',
        method: 'post'
    })
}