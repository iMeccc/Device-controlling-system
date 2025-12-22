import { createApp } from 'vue'

// --- 1. Import Element Plus ---
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' // Import the CSS styles

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

// --- 2. Use Element Plus ---
app.use(ElementPlus) // Register the Element Plus plugin

app.mount('#app')