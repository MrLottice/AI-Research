<template>
  <div class="molecular-biology-container">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Promotion /></el-icon>
        <h2 class="page-title">分子生物学前沿综述</h2>
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
        <!-- 论文信息输入 -->
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon blue"><Medal /></el-icon>
            <span class="label-text">论文题目<span class="required">*</span></span>
          </div>
          <el-input
            type="textarea"
            v-model="paperInfo"
            :rows="4"
            :maxlength="2000"
            placeholder="请输入论文的题目"
          />
          <div class="char-count">{{ paperInfo.length }} / 2000</div>
        </div>

        <!-- 补充材料 -->
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon blue"><InfoFilled /></el-icon>
            <span class="label-text">补充材料（可选）</span>
          </div>
          <el-input
            type="textarea"
            v-model="supplementaryInfo"
            :rows="8"
            :maxlength="5000"
            placeholder="请输入论文的关键词、实验过程、实验结果、创新点等信息"
          />
          <div class="char-count">{{ supplementaryInfo.length }} / 5000</div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="default" plain @click="clearInputs" :disabled="isLoading">清空</el-button>
          <el-button size="default" type="primary" @click="generateSubmission" :loading="isLoading">
            {{ isLoading ? '生成中...' : '生成综述' }}
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
        <div v-if="isLoading && !submissionGenerated" class="loading-result">
          <div class="loading-animation">
            <div class="loading-spinner"></div>
          </div>
          <p class="loading-text">AI正在生成分子生物学前沿综述...</p>
          <p class="loading-tips">这可能需要几分钟，请耐心等待</p>
        </div>

        <!-- 空结果状态 -->
        <div v-else-if="!isLoading && !submissionGenerated" class="empty-result">
          <div class="light-bulb-icon">
            <img src="https://img.icons8.com/ios/100/409eff/idea.png" alt="灵感" />
          </div>
          <p class="empty-text">暂无内容，尚未成功生成！</p>
        </div>

        <!-- 生成结果状态 -->
        <div v-else class="submission-result">
          <div class="submission-content" v-html="generatedSubmission"></div>
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
import { ref, nextTick } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  Promotion, 
  VideoPlay, 
  Medal, 
  InfoFilled, 
  List, 
  DocumentCopy, 
  Download 
} from '@element-plus/icons-vue';
import { marked } from 'marked';

const paperInfo = ref('');
const supplementaryInfo = ref('');
const submissionGenerated = ref(false);
const generatedSubmission = ref('');
const isLoading = ref(false);
const isCopying = ref(false);
const isDownloading = ref(false);
const rawContent = ref('');

// 清空输入
const clearInputs = () => {
  paperInfo.value = '';
  supplementaryInfo.value = '';
  generatedSubmission.value = '';
  rawContent.value = '';
};

// Markdown转HTML
const markdownToHtml = (markdown: string): string => {
  if (!markdown) return '';
  return marked.parse(markdown, {
    breaks: true,
    gfm: true
  }) as string;
};

// 生成结果
const generateSubmission = async () => {
  if (!paperInfo.value.trim()) {
    ElMessage.error('请先输入论文信息');
    return;
  }

  try {
    isLoading.value = true;
    submissionGenerated.value = false;
    generatedSubmission.value = '';
    rawContent.value = '';

    // 创建请求数据
    const formData = new FormData();
    formData.append('title', paperInfo.value);
    formData.append('examples', supplementaryInfo.value);
    formData.append('theme', 'review');

    // 发送请求到后端接口
    const response = await fetch('http://127.0.0.1:5000/dify_api', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 立即设置submissionGenerated为true，显示结果区域
    submissionGenerated.value = true;

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

      // 将接收到的数据添加到缓冲区
      buffer += decoder.decode(value, { stream: true });

      // 处理缓冲区中的完整消息
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || ''; // 保留最后一个不完整的消息

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            
            if (data.type === 'text') {
              // 直接使用full_text作为当前完整内容
              rawContent.value = data.full_text;
              // 将完整的Markdown内容转换为HTML
              generatedSubmission.value = markdownToHtml(rawContent.value);
              // 使用nextTick确保DOM更新后再滚动
              nextTick(() => {
                const resultSection = document.querySelector('.result-section');
                if (resultSection) {
                  resultSection.scrollTop = resultSection.scrollHeight;
                }
              });
            } else if (data.type === 'done') {
              // 生成完成
              ElMessage.success('综述生成成功！');
              isReading = false;
            } else if (data.type === 'error') {
              // 处理错误
              ElMessage.error(data.message || '生成过程中发生错误');
              isReading = false;
            }
          } catch (e) {
            console.error('解析响应数据失败:', e);
          }
        }
      }
    }
  } catch (error: any) {
    console.error('API请求错误:', error);
    
    if (error.name === 'AbortError') {
      ElMessage.error('请求超时，服务器响应时间过长');
    } else if (error.response) {
      const status = error.response.status || '未知';
      const message = error.response.data?.message || '未知错误';
      ElMessage.error(`服务器错误 (${status}): ${message}`);
    } else {
      ElMessage.error('网络请求失败，请检查后端服务是否启动');
    }
  } finally {
    isLoading.value = false;
  }
};

// 复制内容
const copyContent = async () => {
  isCopying.value = true;
  try {
    const text = document.querySelector('.submission-content')?.textContent || '';
    await navigator.clipboard.writeText(text);
    ElMessage.success('内容已复制到剪贴板！');
  } catch (error) {
    ElMessage.error('复制失败，请手动复制！');
  } finally {
    isCopying.value = false;
  }
};

// 下载内容
const downloadContent = () => {
  if (!generatedSubmission.value) {
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
      <title>${paperInfo.value || '分子生物学前沿综述'}</title>
      </head>
      <body>
      ${generatedSubmission.value}
      </body>
      </html>`;
    
    // 生成文件名
    let fileName = paperInfo.value.trim();
    // 如果论文标题太长，截取前30个字符
    if (fileName.length > 30) {
      fileName = fileName.substring(0, 30) + '...';
    }
    // 去除文件名中的非法字符
    fileName = fileName.replace(/[\\/:*?"<>|]/g, '_');
    // 如果标题为空，使用默认名称
    if (!fileName) {
      fileName = `分子生物学前沿综述_${new Date().toISOString().split('T')[0]}`;
    }
    
    const blob = new Blob([wordContent], { type: 'application/vnd.ms-word;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${fileName}.doc`;
    link.click();
    
    URL.revokeObjectURL(link.href);
    ElMessage.success('综述已下载为Word文档');
  } catch (error) {
    console.error('下载失败:', error);
    ElMessage.error('下载失败，请稍后重试');
  } finally {
    setTimeout(() => {
      isDownloading.value = false;
    }, 500);
  }
};
</script>

<style scoped>
.molecular-biology-container {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px 20px;
  background: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  width: 100%;
  box-sizing: border-box;
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
  margin: 0;
  font-size: 20px;
  color: #303133;
  font-weight: bold;
}

.version {
  font-size: 14px;
  color: #909399;
  margin-left: 8px;
}

.tutorial-btn {
  display: flex;
  align-items: center;
  gap: 6px;
}

.main-content {
  flex: 1;
  display: flex;
  gap: 20px;
  min-height: 0;
  padding: 0 20px;
  box-sizing: border-box;
}

.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  min-height: 0;
}

.input-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #fdf6ec;
  border-radius: 4px;
  margin-bottom: 20px;
  color: #e6a23c;
}

.input-warning .el-icon {
  font-size: 18px;
}

.input-block {
  margin-bottom: 24px;
}

.input-label {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 8px;
}

.label-icon {
  font-size: 16px;
}

.label-icon.blue {
  color: #409EFF;
}

.label-text {
  font-size: 16px;
  color: #000000;
  font-weight: bold;
}

.required {
  color: #F56C6C;
  margin-left: 4px;
}

.char-count {
  text-align: right;
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  margin-bottom: 16px;
  justify-content: center;
}

.action-buttons .el-button {
  min-width: 80px;
  height: 36px;
  font-size: 14px;
}

.disclaimer-text {
  text-align: center;
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.result-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.result-icon {
  font-size: 18px;
  color: #409EFF;
}

.result-title {
  font-size: 18px;
  color: #303133;
  font-weight: bold;
}

.loading-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
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
  font-size: 18px;
  color: #303133;
  margin-bottom: 8px;
}

.loading-tips {
  font-size: 16px;
  color: #909399;
}

.empty-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.light-bulb-icon {
  margin-bottom: 16px;
}

.light-bulb-icon img {
  width: 64px;
  height: 64px;
}

.empty-text {
  font-size: 16px;
  color: #909399;
}

.submission-result {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.submission-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 16px;
  line-height: 1.6;
}

.submission-content :deep(h1) {
  font-size: 26px;
  margin-bottom: 20px;
  color: #000000;
  font-weight: bold;
}

.submission-content :deep(h2) {
  font-size: 22px;
  margin: 15px 0;
  color: #000000;
  font-weight: bold;
}

.submission-content :deep(p) {
  margin: 10px 0;
  color: #000000;
  font-size: 16px;
  line-height: 1.8;
}

.submission-content :deep(ul), .submission-content :deep(ol) {
  margin: 10px 0;
  padding-left: 20px;
}

.submission-content :deep(li) {
  margin: 5px 0;
  color: #000000;
  font-size: 16px;
  line-height: 1.8;
}

.result-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.result-actions .el-button {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
