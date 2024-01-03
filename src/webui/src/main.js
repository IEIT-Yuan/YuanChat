import { createPinia } from 'pinia'
import { i18n } from './locales'

import App from './App.vue'
import router from './router'
import '@/styles/index.less'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.mount('#app')
