import axios from 'axios'

const HTTP = axios.create({
    baseURL: `http://localhost:5000/api`,
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
    const requestOptions = { username: username, password: password };
    return HTTP.post(`/auth/login`, requestOptions)
        .then(response => {
            // login successful if there's a jwt token in the response
            if (response.data.access_token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(response.data));
            }
            
            return response;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}