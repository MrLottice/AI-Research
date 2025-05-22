<template>
  <div class="fund-review-container">
    <div class="main-content">
      <!-- 左侧上传区域 -->
      <div class="upload-section">
        <h2>评审材料</h2>
        <el-upload
          class="upload-area"
          drag
          :auto-upload="false"
          :multiple="true"
          :show-file-list="true"
          :on-change="handleFileChange"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持上传PDF、Word、Excel等格式文件
            </div>
          </template>
        </el-upload>


        <div class="action-buttons">
          <el-button type="primary" size="large" @click="handleSubmit" :loading="isLoading">
            {{ isLoading ? '评审中...' : '开始评审' }}
          </el-button>
        </div>
      </div>

      <!-- 右侧结果区域 -->
      <div class="result-section">
        <div class="result-header">
          <div class="header-left">
            <el-icon class="result-icon"><List /></el-icon>
            <span class="result-title">评审结果</span>
          </div>
          <div class="result-actions" v-if="showOutput">
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

        <!-- 加载中状态 -->
        <div v-if="isLoading" class="loading-result">
          <div class="loading-animation">
            <div class="loading-spinner"></div>
          </div>
          <p class="loading-text">AI正在评审项目...</p>
          <p class="loading-tips">这可能需要几分钟，请耐心等待</p>
        </div>

        <!-- 空结果状态 -->
        <div v-else-if="!showOutput" class="empty-result">
          <div class="light-bulb-icon">
            <img src="https://img.icons8.com/ios/100/409eff/idea.png" alt="灵感" />
          </div>
          <p class="empty-text">暂无评审结果，请先上传材料并点击"开始评审"</p>
        </div>

        <!-- 生成结果状态 -->
        <div v-else class="submission-result">
          <div class="markdown-body" v-html="formattedResult"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
import { ElMessage } from 'element-plus';
import { UploadFilled, Download, List, DocumentCopy } from '@element-plus/icons-vue';
import { marked } from 'marked';

const showOutput = ref(false);
const fileList = ref<Array<{name: string, size: string}>>([]);
const uploadedFiles = ref<File[]>([]);
const reviewResult = ref('');
const isDownloading = ref(false);
const isLoading = ref(false);
const isCopying = ref(false);

// 配置 marked 选项
marked.setOptions({
  breaks: true, // 允许回车换行
  gfm: true,    // 启用 GitHub 风格的 markdown
});

// 计算属性：将 markdown 转换为 HTML
const formattedResult = computed(() => {
  if (!reviewResult.value) return '';
  try {
    return marked(reviewResult.value);
  } catch (e) {
    console.error('Markdown 转换错误:', e);
    return reviewResult.value;
  }
});

const handleFileChange = (file: any) => {
  console.log('File changed:', file);
  uploadedFiles.value.push(file.raw);
  fileList.value.push({
    name: file.name,
    size: formatFileSize(file.size)
  });
};

const formatFileSize = (size: number) => {
  if (size < 1024) {
    return size + 'B';
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + 'KB';
  } else {
    return (size / (1024 * 1024)).toFixed(2) + 'MB';
  }
};

const handleSubmit = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请先上传评审材料');
    return;
  }

  try {
    isLoading.value = true;
    showOutput.value = false;
    reviewResult.value = '';

    const formData = new FormData();
    uploadedFiles.value.forEach((file) => {
      formData.append('file', file);
    });
    formData.append('theme', 'project_review');

    const response = await fetch('http://127.0.0.1:5000/upload_and_analyze', {
      method: 'POST',
      body: formData
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('无法读取响应流');
    }

    let buffer = '';
    let isReading = true;
    
    // 收到第一个响应就停止加载动画
    isLoading.value = false;
    showOutput.value = true;
    
    while (isReading) {
      const { done, value } = await reader.read();
      if (done) {
        isReading = false;
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === 'text') {
              reviewResult.value = data.full_text || data.content;
              // 改进自动滚动实现
              nextTick(() => {
                const submissionResult = document.querySelector('.submission-result');
                if (submissionResult) {
                  // 使用 requestAnimationFrame 确保在渲染后执行滚动
                  requestAnimationFrame(() => {
                    submissionResult.scrollTo({
                      top: submissionResult.scrollHeight,
                      behavior: 'smooth'
                    });
                  });
                }
              });
            } else if (data.type === 'error') {
              ElMessage.error(data.message);
              isReading = false;
            } else if (data.type === 'done') {
              ElMessage.success('评审完成！');
              isReading = false;
            }
          } catch (e) {
            console.warn('解析SSE消息失败:', e);
          }
        }
      }
    }

  } catch (error: any) {
    console.error('评审请求失败:', error);
    ElMessage.error(`评审请求失败：${error.message}`);
    showOutput.value = false;
    reviewResult.value = '';
  } finally {
    isLoading.value = false;
  }
};

const downloadContent = () => {
  if (!reviewResult.value) {
    ElMessage.error('没有可下载的内容');
    return;
  }
  
  try {
    isDownloading.value = true;
    
    // 创建一个简单的Word文档内容
    const wordContent = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
      <head>
      <meta charset="utf-8">
      <title>项目评审结果</title>
      </head>
      <body>
      ${formattedResult.value}
      </body>
      </html>`;
    
    // 生成文件名
    const fileName = `项目评审结果_${new Date().toLocaleDateString().replace(/\//g, '-')}`;
    
    const blob = new Blob([wordContent], { type: 'application/vnd.ms-word;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${fileName}.doc`;
    link.click();
    
    URL.revokeObjectURL(link.href);
    ElMessage.success('评审结果已下载为Word文档');
  } catch (error) {
    console.error('下载失败:', error);
    ElMessage.error('下载失败，请稍后重试');
  } finally {
    setTimeout(() => {
      isDownloading.value = false;
    }, 500);
  }
};

const copyContent = async () => {
  if (!reviewResult.value) {
    ElMessage.error('没有可复制的内容');
    return;
  }
  
  try {
    isCopying.value = true;
    await navigator.clipboard.writeText(reviewResult.value);
    ElMessage.success('内容已复制到剪贴板');
  } catch (error) {
    console.error('复制失败:', error);
    ElMessage.error('复制失败，请手动复制');
  } finally {
    isCopying.value = false;
  }
};
</script>

<style scoped>
.fund-review-container {
  padding: 20px;
  width: 100%;
  height: 100vh;
  box-sizing: border-box;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-content {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0; /* 重要：允许内容收缩 */
}

.upload-section, .result-section {
  flex: 1;
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 重要：防止内容溢出 */
}

.result-section {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%; /* 确保父容器占满高度 */
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
  flex-shrink: 0; /* 防止header被压缩 */
}

.header-left {
  display: flex;
  align-items: center;
}

.result-icon {
  color: #409EFF;
  font-size: 20px;
  margin-right: 8px;
}

.result-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.result-actions {
  display: flex;
  gap: 8px;
}

.loading-result, .empty-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.submission-result {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  height: 100%;
  max-height: 100%;
  scroll-behavior: smooth;
  width: 100%;
}

.markdown-body {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 8px;
  /* box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05); */
  line-height: 1.8;
  font-size: 15px;
  color: #24292e;
  height: 100%;
  width: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}

h2 {
  margin: 0 0 24px 0;
  font-size: 24px;
  color: #333;
  font-weight: 600;
}

.upload-area {
  width: 100%;
  margin-bottom: 16px;
}

.action-buttons {
  margin-bottom: 24px;
  text-align: center;
}

.file-list {
  margin: 20px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.file-list h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}

.file-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.file-list li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.file-list li:last-child {
  border-bottom: none;
}

.loading-animation {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 30px;
}

.loading-spinner {
  position: absolute;
  top: 0;
  left: 0;
  width: 80px;
  height: 80px;
  border: 5px solid rgba(64, 158, 255, 0.2);
  border-top-color: #409EFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner::after {
  content: "";
  position: absolute;
  top: 15px;
  left: 15px;
  right: 15px;
  bottom: 15px;
  border: 3px solid rgba(64, 158, 255, 0.2);
  border-top-color: #409EFF;
  border-radius: 50%;
  animation: spin 1.5s linear infinite reverse;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 18px;
  font-weight: 500;
  color: #409EFF;
  margin-bottom: 10px;
}

.loading-tips {
  font-size: 14px;
  color: #909399;
  text-align: center;
  max-width: 300px;
  line-height: 1.5;
}

.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #999;
}

.light-bulb-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.light-bulb-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.empty-text {
  font-size: 16px;
  color: #999;
}

:deep(.markdown-body) {
  /* 标题样式 */
  h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
  }

  h1 { font-size: 2em; }
  h2 { font-size: 1.5em; }
  h3 { font-size: 1.25em; }
  h4 { font-size: 1em; }

  /* 段落样式 */
  p {
    margin-top: 0;
    margin-bottom: 16px;
  }

  /* 列表样式 */
  ul, ol {
    padding-left: 2em;
    margin-top: 0;
    margin-bottom: 16px;
  }

  li {
    margin: 0.25em 0;
  }

  /* 引用样式 */
  blockquote {
    padding: 0 1em;
    color: #6a737d;
    border-left: 0.25em solid #dfe2e5;
    margin: 0 0 16px 0;
  }

  /* 代码样式 */
  code {
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    background-color: rgba(27,31,35,0.05);
    border-radius: 3px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  }

  pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 3px;
    margin-bottom: 16px;
  }

  pre code {
    padding: 0;
    margin: 0;
    background-color: transparent;
  }

  /* 表格样式 */
  table {
    border-spacing: 0;
    border-collapse: collapse;
    margin-bottom: 16px;
    width: 100%;
  }

  table th,
  table td {
    padding: 6px 13px;
    border: 1px solid #dfe2e5;
  }

  table th {
    font-weight: 600;
    background-color: #f6f8fa;
  }

  /* 分割线样式 */
  hr {
    height: 0.25em;
    padding: 0;
    margin: 24px 0;
    background-color: #e1e4e8;
    border: 0;
  }

  /* 链接样式 */
  a {
    color: #0366d6;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }
}

.download-button {
  display: none;
}
</style>
