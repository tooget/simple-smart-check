import Vue from 'vue'
import VueApollo from 'vue-apollo'
import { ApolloClient } from 'apollo-client'
import { ApolloLink, concat } from 'apollo-link'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import { getToken } from '@/utils/auth'

Vue.use(VueApollo)

const httpLink = new HttpLink({
  uri: process.env.GRAPHQL_API,
  transportBatching: true
})

const authMiddleware = new ApolloLink((operation, forward) => {
  // add the authorization to the headers
  operation.setContext({
    headers: {
      authorization: 'Bearer ' + getToken(),
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/json'
    }
  })
  return forward(operation)
})

export const apolloClient = new ApolloClient({
  // Provide the URL to the API server.
  link: concat(authMiddleware, httpLink),
  // Using a cache for blazingly
  // fast subsequent queries.
  cache: new InMemoryCache(),
  connectToDevTools: true
})

const apolloProvider = new VueApollo({
  // Default client
  defaultClient: apolloClient,
  // Default 'apollo' definition
  defaultOptions: {
    // See 'apollo' definition
    // For example: default query options
    $query: {
      loadingKey: 'loading',
      fetchPolicy: 'no-cache'
    }
  }
})

export default apolloProvider
