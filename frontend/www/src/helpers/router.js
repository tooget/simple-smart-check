import Vue from 'vue';
import Router from 'vue-router';

import AppNavigator from '../AppNavigator.vue';
import AppLogin from '../AppLogin.vue';
import { getToken } from './auth-header'

Vue.use(Router);

export const router = new Router({
  mode: 'history',
  routes: [
    { path: '/', component: AppNavigator },
    { path: '/login', component: AppLogin },

    // otherwise redirect to home
    { path: '*', redirect: '/' }
  ]
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = getToken();

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})