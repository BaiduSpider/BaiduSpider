import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'
import App from './App.vue'

Vue.use(Vuetify)

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  render: h => h(App)
})
