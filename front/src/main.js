import Vue from 'vue'
import Vuex from 'vuex';
import App from './App.vue'
import {BootstrapVue} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.use(Vuex);
Vue.use(BootstrapVue)

const store = new Vuex.Store({
    state: {
        token: undefined,
    },
    mutations: {
        setToken(state, newToken) {
            state.token = newToken;
        }
    }
});

new Vue({
    render: h => h(App),
    store
}).$mount('#app')
