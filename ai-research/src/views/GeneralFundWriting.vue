<template>
  <div class="general-fund-writing">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Money /></el-icon>
        <h2 class="page-title">国家自然科学基金面上项目</h2>
        <span class="version">v1.0.0</span>
      </div>
      <div class="header-right">
        <el-button class="tutorial-btn" type="primary" plain size="small">
          <el-icon><VideoPlay /></el-icon>
          <span>演示教程</span>
        </el-button>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 左侧输入区域 -->
      <div class="input-section">
        <!-- <div class="input-warning">
          <el-icon><Warning /></el-icon>
          <span>使用我们的服务时，确保您的输入和生成内容不违反任何适用法律和不侵犯第三方合法权益</span>
        </div> -->

        <!-- 项目信息输入 -->
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon blue"><Medal /></el-icon>
            <span class="label-text">项目名称<span class="required">*</span></span>
          </div>
          <el-input
            type="textarea"
            v-model="projectInfo.title"
            :rows="2"
            :maxlength="200"
            placeholder="请输入项目名称"
          />
          <div class="char-count">{{ projectInfo.title.length }} / 200</div>
        </div>

        <!-- 研究方向 -->
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon green"><Compass /></el-icon>
            <span class="label-text">研究方向<span class="required">*</span></span>
          </div>
          <el-input
            type="textarea"
            v-model="projectInfo.direction"
            :rows="3"
            :maxlength="500"
            placeholder="请输入研究方向"
          />
          <div class="char-count">{{ projectInfo.direction.length }} / 500</div>
        </div>

        <!-- 研究内容 -->
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon orange"><Document /></el-icon>
            <span class="label-text">研究内容<span class="required">*</span></span>
          </div>
          <el-input
            type="textarea"
            v-model="projectInfo.content"
            :rows="6"
            :maxlength="2000"
            placeholder="请输入研究内容"
          />
          <div class="char-count">{{ projectInfo.content.length }} / 2000</div>
        </div>

        <!-- 补充说明 -->
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon blue"><InfoFilled /></el-icon>
            <span class="label-text">补充说明（可选）</span>
          </div>
          <el-input
            type="textarea"
            v-model="projectInfo.additional"
            :rows="4"
            :maxlength="1000"
            placeholder="请输入补充说明，如创新点、研究基础等"
          />
          <div class="char-count">{{ projectInfo.additional.length }} / 1000</div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="large" plain @click="clearInputs" :disabled="isLoading">清空</el-button>
          <el-button size="large" type="primary" @click="generateOutline" :loading="isLoading">
            {{ isLoading ? '生成中...' : '生成申请书提纲' }}
          </el-button>
        </div>

        <div class="disclaimer-text">
          内容由AI生成，注意甄别，仅供参考。
        </div>
      </div>

      <!-- 右侧结果区域 -->
      <div class="result-section">
        <div class="result-header">
          <el-icon class="result-icon"><List /></el-icon>
          <span class="result-title">生成结果</span>
        </div>

        <!-- 加载中状态 -->
        <div v-if="isLoading && !outlineGenerated" class="loading-result">
          <div class="loading-animation">
            <div class="loading-spinner"></div>
          </div>
          <p class="loading-text">AI正在生成申请书提纲...</p>
          <p class="loading-tips">这可能需要几分钟，请耐心等待</p>
        </div>

        <!-- 空结果状态 -->
        <div v-else-if="!isLoading && !outlineGenerated" class="empty-result">
          <div class="light-bulb-icon">
            <img src="https://img.icons8.com/ios/100/409eff/idea.png" alt="灵感" />
          </div>
          <p class="empty-text">暂无内容，尚未成功生成！</p>
        </div>

        <!-- 生成结果状态 -->
        <div v-else class="outline-result">
          <div class="outline-content" v-html="generatedOutline"></div>
          <div class="result-actions">
            <el-button size="small" type="primary" plain @click="copyContent" :loading="isCopying">
              <el-icon><DocumentCopy /></el-icon>
              <span>复制</span>
            </el-button>
            <el-button size="small" type="success" plain @click="downloadContent" :loading="isDownloading">
              <el-icon><Download /></el-icon>
              <span>下载</span>
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  Money,
  VideoPlay,
  Medal,
  Compass,
  Document,
  InfoFilled,
  List,
  DocumentCopy,
  Download
} from '@element-plus/icons-vue';

const projectInfo = ref({
  title: '',
  direction: '',
  content: '',
  additional: ''
});

const isLoading = ref(false);
const isCopying = ref(false);
const isDownloading = ref(false);
const outlineGenerated = ref(false);
const generatedOutline = ref('');
const rawContent = ref('');

const clearInputs = () => {
  projectInfo.value = {
    title: '',
    direction: '',
    content: '',
    additional: ''
  };
  generatedOutline.value = '';
  rawContent.value = '';
  outlineGenerated.value = false;
};

const generateOutline = async () => {
  if (!projectInfo.value.title.trim()) {
    ElMessage.error('请输入项目名称');
    return;
  }
  if (!projectInfo.value.direction.trim()) {
    ElMessage.error('请输入研究方向');
    return;
  }
  if (!projectInfo.value.content.trim()) {
    ElMessage.error('请输入研究内容');
    return;
  }

  try {
    isLoading.value = true;
    outlineGenerated.value = false;
    generatedOutline.value = '';
    rawContent.value = '';
    
    // 创建FormData对象
    const formData = new FormData();
    formData.append('title', projectInfo.value.title);
    formData.append('direction', projectInfo.value.direction);
    formData.append('content', projectInfo.value.content);
    formData.append('additional', projectInfo.value.additional);
    formData.append('type', 'fund_general');
    
    // 使用fetch API发送请求
    const response = await fetch('http://127.0.0.1:5000/dify_api', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 设置生成状态
    outlineGenerated.value = true;

    // 创建响应流读取器
    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('无法获取响应流');
    }

    const decoder = new TextDecoder();
    let buffer = '';
    let isReading = true;

    while (isReading) {
      const { done, value } = await reader.read();
      if (done) {
        isReading = false;
        break;
      }
      
      buffer += decoder.decode(value, { stream: true });
      generatedOutline.value = buffer;
      rawContent.value = buffer;
    }

  } catch (error) {
    console.error('Error:', error);
    ElMessage.error('生成失败，请稍后重试');
  } finally {
    isLoading.value = false;
  }
};

const copyContent = async () => {
  if (!rawContent.value) {
    ElMessage.warning('没有可复制的内容');
    return;
  }

  try {
    isCopying.value = true;
    await navigator.clipboard.writeText(rawContent.value);
    ElMessage.success('复制成功');
  } catch (error) {
    console.error('Copy failed:', error);
    ElMessage.error('复制失败');
  } finally {
    isCopying.value = false;
  }
};

const downloadContent = () => {
  if (!rawContent.value) {
    ElMessage.warning('没有可下载的内容');
    return;
  }

  try {
    isDownloading.value = true;
    const blob = new Blob([rawContent.value], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `面上项目申请书提纲_${new Date().toLocaleDateString()}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    ElMessage.success('下载成功');
  } catch (error) {
    console.error('Download failed:', error);
    ElMessage.error('下载失败');
  } finally {
    isDownloading.value = false;
  }
};
</script>

<style scoped>
.general-fund-writing {
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  background-color: #f5f7fa;
  margin-top: -25px;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: #fff;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
  width: 100%;
  box-sizing: border-box;
  margin-left: -20px;
  margin-right: -20px;
  padding-left: 40px;
  padding-right: 40px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.light-bulb {
  font-size: 24px;
  color: #409EFF;
}

.page-title {
  font-size: 20px;
  color: #333;
  margin: 0;
  font-weight: 700;
}

.version {
  font-size: 14px;
  color: #909399;
  margin-left: 8px;
}

.main-content {
  display: flex;
  gap: 20px;
  height: calc(100vh - 140px);
  width: 100%;
  margin: 0 -20px;
  padding: 0 20px;
  box-sizing: border-box;
}

.input-section {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
  overflow-y: auto;
}

.input-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #fff8e6;
  border-radius: 4px;
  margin-bottom: 20px;
  color: #e6a23c;
  font-size: 14px;
}

.input-block {
  margin-bottom: 24px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.label-icon {
  font-size: 18px;
}

.label-icon.blue {
  color: #409EFF;
}

.label-icon.green {
  color: #67C23A;
}

.label-icon.orange {
  color: #E6A23C;
}

.label-text {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.required {
  color: #F56C6C;
  margin-left: 4px;
}

.char-count {
  text-align: right;
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
  justify-content: center;
}

.disclaimer-text {
  margin-top: 16px;
  color: #909399;
  font-size: 12px;
  text-align: center;
}

.result-section {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #EBEEF5;
}

.result-icon {
  font-size: 20px;
  color: #409EFF;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.loading-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-animation {
  margin-bottom: 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #409EFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 16px;
  color: #303133;
  margin-bottom: 8px;
}

.loading-tips {
  font-size: 14px;
  color: #909399;
}

.empty-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.light-bulb-icon {
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-text {
  color: #909399;
  font-size: 14px;
}

.outline-result {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.outline-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.6;
  color: #303133;
}

.result-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  justify-content: flex-end;
}

.tutorial-btn {
  display: flex;
  align-items: center;
  gap: 4px;
}

:deep(.el-textarea__inner) {
  font-size: 14px;
  line-height: 1.6;
}

:deep(.el-button) {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style> 