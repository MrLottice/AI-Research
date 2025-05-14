import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { ElMessage } from 'element-plus'
import router from './router'

const app = createApp(App)

app.use(ElementPlus)
app.use(router)

// 全局配置 ElMessage
app.config.globalProperties.$message = ElMessage

app.mount('#app')
