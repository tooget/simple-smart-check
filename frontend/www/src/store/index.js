import Vue from 'vue';
import Vuex from 'vuex';

import { navigator } from './navigator.module';
import { splitter } from './splitter.module';
import { tabbar } from './tabbar.module';

import { alert } from './alert.module';
import { authentication } from './authentication.module';

import { attendanceLog } from './attendanceLog.module';

import getters from './getters'

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules: {
        navigator,
        splitter,
        tabbar,
        alert,
        authentication,
        attendanceLog
    },
    getters
});

export default store