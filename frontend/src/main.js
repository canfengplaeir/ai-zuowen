import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/css/main.css'
import Vcode from 'vue-puzzle-vcode'

const app = createApp(App)

app.use(router)
app.use(Vcode)

app.mount('#app') 