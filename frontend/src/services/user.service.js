import axios from 'axios'

const HTTP = axios.create({
    baseURL: `https://backend.smartcheck.ml/api`,
    timeout: 5000,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  })

export const userService = {
    login,
    logout
};

function login(username, password) {
    const requestBody = new FormData()
    requestBody.append('username', username)
    requestBody.append('password', password)

    return HTTP.post(`/users/login`, requestBody)
        .then(response => {
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