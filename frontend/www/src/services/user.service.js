import USERS_LOGIN from '../graphql/UsersLogin.gql'
import USERS_LOGOUT from '../graphql/UsersLogout.gql'
import { apolloClient } from '../apollo'

export const userService = {
    login,
    logout
};

async function login(username, password) {
    return await apolloClient.mutate({
      mutation: USERS_LOGIN,
      variables: { username: username, password: password }
    })
  }

async function logout() {
    return await apolloClient.mutate({
      mutation: USERS_LOGOUT
    })
}