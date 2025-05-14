<template>
  <div class="journal-submission-container">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Promotion /></el-icon>
        <h2 class="page-title">Nature Communications 投稿指南</h2>
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
        <div class="input-warning">
          <el-icon><Warning /></el-icon>
          <span>使用我们的服务时，确保您的输入和生成内容不违反任何适用法律和不侵犯第三方合法权益</span>
        </div>

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
            placeholder="请输入论文的标题"
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
            :rows="4"
            :maxlength="5000"
            placeholder="请输入论文的关键词、实验过程、实验结果、创新点等信息"
          />
          <div class="char-count">{{ supplementaryInfo.length }} / 5000</div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="large" plain @click="clearInputs" :disabled="isLoading">清空</el-button>
          <el-button size="large" type="primary" @click="generateSubmission" :loading="isLoading">
            {{ isLoading ? '生成中...' : '生成论文初稿' }}
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
        <div v-if="isLoading" class="loading-result">
          <div class="loading-animation">
            <div class="loading-spinner"></div>
          </div>
          <p class="loading-text">AI正在生成Nature Communications初稿...</p>
          <p class="loading-tips">这可能需要几分钟，请耐心等待</p>
        </div>

        <!-- 空结果状态 -->
        <div v-else-if="!submissionGenerated" class="empty-result">
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

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  Promotion, 
  VideoPlay, 
  Warning, 
  Medal, 
  InfoFilled, 
  List, 
  DocumentCopy, 
  Download 
} from '@element-plus/icons-vue';

export default defineComponent({
  name: 'NatureCommunicationsSubmission',
  components: {
    Promotion,
    VideoPlay,
    Warning,
    Medal,
    InfoFilled,
    List,
    DocumentCopy,
    Download
  },
  setup() {
    const paperInfo = ref('');
    const supplementaryInfo = ref('');
    const submissionGenerated = ref(false);
    const generatedSubmission = ref('');
    const isLoading = ref(false);
    const isCopying = ref(false);
    const isDownloading = ref(false);

    const clearInputs = () => {
      paperInfo.value = '';
      supplementaryInfo.value = '';
    };

    const generateSubmission = async () => {
      if (!paperInfo.value.trim()) {
        ElMessage.error('请先输入论文信息');
        return;
      }

      try {
        isLoading.value = true;
        submissionGenerated.value = false;
        
        // TODO: 实现与后端的交互逻辑
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        generatedSubmission.value = `
          <h2>Nature Communications 投稿指南</h2>
          <h3>1. 投稿要求</h3>
          <ul>
            <li>论文必须是原创性研究</li>
            <li>研究结果必须具有重要的科学意义</li>
            <li>实验方法必须详细且可重复</li>
          </ul>
          
          <h3>2. 格式要求</h3>
          <ul>
            <li>字数限制：正文不超过4000字</li>
            <li>图表数量：不超过6个</li>
            <li>参考文献：不超过40条</li>
          </ul>
          
          <h3>3. 投稿流程</h3>
          <ol>
            <li>准备投稿材料</li>
            <li>在线提交</li>
            <li>同行评议</li>
            <li>修改与回复</li>
          </ol>
        `;
        
        submissionGenerated.value = true;
        ElMessage.success('投稿指南生成成功！');
      } catch (error) {
        console.error('生成失败:', error);
        ElMessage.error('生成失败，请稍后重试');
      } finally {
        isLoading.value = false;
      }
    };

    const copyContent = async () => {
      if (!generatedSubmission.value) {
        ElMessage.error('没有可复制的内容');
        return;
      }
      
      try {
        isCopying.value = true;
        const tempElement = document.createElement('div');
        tempElement.innerHTML = generatedSubmission.value;
        const textContent = tempElement.textContent || tempElement.innerText || '';
        
        await navigator.clipboard.writeText(textContent);
        ElMessage.success('内容已复制到剪贴板');
      } catch (error) {
        console.error('复制失败:', error);
        ElMessage.error('复制失败，请手动复制');
      } finally {
        isCopying.value = false;
      }
    };

    const downloadContent = () => {
      if (!generatedSubmission.value) {
        ElMessage.error('没有可下载的内容');
        return;
      }
      
      try {
        isDownloading.value = true;
        const tempElement = document.createElement('div');
        tempElement.innerHTML = generatedSubmission.value;
        const textContent = tempElement.textContent || tempElement.innerText || '';
        
        const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `Nature_Communications_投稿指南_${new Date().toISOString().split('T')[0]}.txt`;
        link.click();
        
        URL.revokeObjectURL(link.href);
        ElMessage.success('投稿指南已下载');
      } catch (error) {
        console.error('下载失败:', error);
        ElMessage.error('下载失败，请稍后重试');
      } finally {
        setTimeout(() => {
          isDownloading.value = false;
        }, 500);
      }
    };

    return {
      paperInfo,
      supplementaryInfo,
      submissionGenerated,
      generatedSubmission,
      isLoading,
      isCopying,
      isDownloading,
      clearInputs,
      generateSubmission,
      copyContent,
      downloadContent
    };
  }
});
</script>

<style scoped>
.journal-submission-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f9f9f9;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
}

.light-bulb {
  color: #409EFF;
  font-size: 24px;
  margin-right: 10px;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.version {
  margin-left: 10px;
  color: #999;
  font-size: 14px;
}

.main-content {
  display: flex;
  flex: 1;
  padding: 20px;
  gap: 20px;
  overflow: hidden;
}

.input-section, .result-section {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  max-height: calc(100vh - 104px);
}

.input-warning {
  display: flex;
  align-items: flex-start;
  padding: 10px 15px;
  background-color: #ecf5ff;
  border-radius: 6px;
  margin-bottom: 20px;
  color: #409EFF;
  font-size: 14px;
  line-height: 1.5;
}

.input-warning .el-icon {
  margin-right: 8px;
  margin-top: 2px;
  flex-shrink: 0;
  color: #409EFF;
}

.input-block {
  margin-bottom: 25px;
}

.input-label {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.label-icon {
  margin-right: 8px;
  font-size: 18px;
}

.blue {
  color: #409EFF;
}

.label-text {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.required {
  color: #f56c6c;
  margin-left: 2px;
}

.char-count {
  text-align: right;
  color: #999;
  font-size: 12px;
  margin-top: 5px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  margin-bottom: 20px;
}

.disclaimer-text {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 20px;
}

.result-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
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

.submission-result {
  padding: 10px;
}

.submission-content {
  margin-bottom: 20px;
  line-height: 1.6;
}

.submission-content h2 {
  font-size: 24px;
  margin-top: 25px;
  margin-bottom: 15px;
  color: #409EFF;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 8px;
}

.submission-content h3 {
  margin-top: 20px;
  margin-bottom: 12px;
  font-size: 18px;
  color: #409EFF;
}

.submission-content ul, .submission-content ol {
  margin-left: 20px;
  margin-bottom: 15px;
  color: #555;
}

.submission-content li {
  margin-bottom: 5px;
}

.result-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.loading-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #409EFF;
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
</style> 