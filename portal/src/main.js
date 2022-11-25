import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router) 
/*global variable to set api URL. USAGE on <setup>: const apiURL = inject('ENDPOINT_PATH'), importing inject from vue */
app.provide('ENDPOINT_PATH', "http://localhost:5000/api")
app.mount('#app')
