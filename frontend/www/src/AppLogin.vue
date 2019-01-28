<template>
  <div class="jumbotron bg-white">
    <div class="col-sm-6 offset-sm-3">
      <div v-if="alert.message" :class="`alert ${alert.type}`">{{ alert.message }}</div>
      <div>
        <h1 align="center">smart-check</h1>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="username">username</label>
            <input type="text" v-model="username" name="username" class="form-control" :class="{ 'is-invalid': submitted && !username }" />
            <div v-show="submitted && !username" class="invalid-feedback">Username is required</div>
          </div>
          <div class="form-group">
            <label htmlFor="password">password</label>
            <input type="password" v-model="password" name="password" class="form-control" :class="{ 'is-invalid': submitted && !password }" />
            <div v-show="submitted && !password" class="invalid-feedback">Password is required</div>
          </div>
          <div class="form-group">
            <button class="btn btn-primary" :disabled="loggingIn">Sign in</button>
            <img v-show="loggingIn" src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA==" />
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { removeToken } from './helpers/auth-header'

export default {
  data () {
    return {
      username: '',
      password: '',
      submitted: false
    }
  },
  created () {
    this.$store.state.authentication.token = undefined;
    removeToken();
  },
  computed: {
    alert () {
      return this.$store.state.alert;
    },
    loggingIn () {
      return this.$store.state.authentication.token;
    }
  },
  watch:{
    $route (to, from){
      // clear alert on location change
      this.$store.dispatch('alert/clear');
    }
  },
  methods: {
    handleSubmit (e) {
      var CryptoJS = require("crypto-js");
      this.submitted = true;
      const username = this.username;
      const password = CryptoJS.PBKDF2(this.password, 'kisa', { iterations: 1, keySize: 256/32, hasher: CryptoJS.algo.SHA256 }).toString(CryptoJS.enc.Base64);
      const { dispatch } = this.$store;
      if (username && password) {
        dispatch('login', { username, password });
        this.$store.dispatch('alert/clear');
      }
    }
  }
};
</script>