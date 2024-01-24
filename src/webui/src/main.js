import { createPinia } from 'pinia'
import { i18n } from './locales'

import App from './App.vue'
import router from './router'
import '@/styles/index.scss'

import VWave from 'v-wave'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(VWave)

app.mount('#app')
