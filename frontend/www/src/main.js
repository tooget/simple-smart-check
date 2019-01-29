import 'onsenui/css/onsenui.css'; // Onsen UI basic CSS
// import 'onsenui/css/onsen-css-components.css'; // Default Onsen UI CSS components
import './onsen-css-components.css'; // Onsen UI CSS components source for custom themes (requires cssnext)
import './vue-onsenui-smartcheck.css'; // CSS specific to this app

import Vue from 'vue';
import VueOnsen from 'vue-onsenui'; // For UMD
import VueSignature from 'vue-signature-pad';
// import VueOnsen from 'vue-onsenui/esm'; // For ESM
// import * as OnsenComponents from './onsen-components'; // For ESMz
import { router } from './helpers';
import { store } from './store';
import App from './App.vue';
import CustomToolbar from './partials/CustomToolbar.vue';


Vue.use(VueOnsen);
Vue.use(VueSignature);

// Register components globally
// Object.values(OnsenComponents).forEach(component => Vue.component(component.name, component)); // For ESM
Vue.component('custom-toolbar', CustomToolbar); // Common toolbar


new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App),
  beforeCreate() {
    // Shortcut for Material Design
    Vue.prototype.md = this.$ons.platform.isAndroid();

    // Set iPhoneX flag based on URL
    if (window.location.search.match(/iphonex/i)) {
      document.documentElement.setAttribute('onsflag-iphonex-portrait', '');
      document.documentElement.setAttribute('onsflag-iphonex-landscape', '');
    }
  }
});
