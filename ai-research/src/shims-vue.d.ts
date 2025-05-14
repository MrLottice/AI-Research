/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 扩展ComponentCustomProperties接口
import { ComponentCustomProperties } from 'vue'
import { ElMessage } from 'element-plus'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $message: typeof ElMessage
  }
}
