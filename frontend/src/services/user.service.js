import request from '../backend'

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
        }).then(response => {
            // login successful if there's a jwt token in the response
            if (response.data.return.access_token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(response.data.return));
            }
            
            return response;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}