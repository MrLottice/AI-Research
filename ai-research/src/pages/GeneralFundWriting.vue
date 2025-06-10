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

    <!-- 标签页导航 -->
    <div class="steps-navigation">
      <el-steps :active="getActiveStep" finish-status="success" align-center>
        <el-step title="立项依据" @click="activeTab = 'basis'" :status="getStepStatus('basis')">
          <template #icon>
            <div class="step-number">1</div>
          </template>
        </el-step>
        <el-step title="研究内容" @click="activeTab = 'content'" :status="getStepStatus('content')">
          <template #icon>
            <div class="step-number">2</div>
          </template>
        </el-step>
        <el-step title="研究方案" @click="activeTab = 'plan'" :status="getStepStatus('plan')">
          <template #icon>
            <div class="step-number">3</div>
          </template>
        </el-step>
        <el-step title="特色创新" @click="activeTab = 'innovation'" :status="getStepStatus('innovation')">
          <template #icon>
            <div class="step-number">4</div>
          </template>
        </el-step>
        <el-step title="年度计划" @click="activeTab = 'schedule'" :status="getStepStatus('schedule')">
          <template #icon>
            <div class="step-number">5</div>
          </template>
        </el-step>
        <el-step title="研究基础" @click="activeTab = 'foundation'" :status="getStepStatus('foundation')">
          <template #icon>
            <div class="step-number">6</div>
          </template>
        </el-step>
        <el-step title="工作条件" @click="activeTab = 'conditions'" :status="getStepStatus('conditions')">
          <template #icon>
            <div class="step-number">7</div>
          </template>
        </el-step>
        <el-step title="相关项目" @click="activeTab = 'relatedProjects'" :status="getStepStatus('relatedProjects')">
          <template #icon>
            <div class="step-number">8</div>
          </template>
        </el-step>
        <el-step title="基金完成情况" @click="activeTab = 'completedProjects'" :status="getStepStatus('completedProjects')">
          <template #icon>
            <div class="step-number">9</div>
          </template>
        </el-step>
        <el-step title="其他说明" @click="activeTab = 'others'" :status="getStepStatus('others')">
          <template #icon>
            <div class="step-number">10</div>
          </template>
        </el-step>
      </el-steps>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 左侧输入区域 -->
      <div class="input-section">
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon blue"><Document /></el-icon>
            <span class="label-text">{{ getCurrentTabTitle }}<span class="required" v-if="activeTab !== 'others'">*</span></span>
          </div>
          <el-input
            type="textarea"
            v-model="projectInfo[activeTab]"
            :rows="6"
            :maxlength="2000"
            :placeholder="getCurrentPlaceholder"
          />
          <div class="char-count">{{ projectInfo[activeTab]?.length || 0 }} / 2000</div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="large" plain @click="clearCurrentTab" :disabled="isLoading">清空</el-button>
          <el-button size="large" type="primary" @click="generateContent" :loading="isLoading">
            {{ isLoading ? '生成中...' : '开始生成' }}
          </el-button>
        </div>

        <div class="disclaimer-text">
          内容由AI生成，注意甄别，仅供参考。
        </div>
      </div>

      <!-- 右侧结果区域 -->
      <div class="result-section">
        <div class="result-header">
          <div class="header-left">
            <el-icon class="result-icon"><List /></el-icon>
            <span class="result-title">{{ getCurrentTabTitle }}生成结果</span>
          </div>
          <div class="result-actions" v-if="generatedResults[activeTab]">
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
          <p class="loading-text">AI正在生成...</p>
          <p class="loading-tips">这可能需要几分钟，请耐心等待</p>
        </div>

        <!-- 空结果状态 -->
        <div v-else-if="!generatedResults[activeTab]" class="empty-result">
          <div class="light-bulb-icon">
            <el-icon :size="60" color="#409eff"><Lightning /></el-icon>
          </div>
          <p class="empty-text">暂无内容，请点击"开始生成"按钮</p>
        </div>

        <!-- 生成结果状态 -->
        <div v-else class="outline-result">
          <div class="outline-content" v-html="generatedResults[activeTab]"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  Money,
  VideoPlay,
  Document,
  List,
  DocumentCopy,
  Download,
  Lightning
} from '@element-plus/icons-vue';

interface ProjectInfo {
  [key: string]: string;
  basis: string;
  content: string;
  plan: string;
  innovation: string;
  schedule: string;
  foundation: string;
  conditions: string;
  relatedProjects: string;
  completedProjects: string;
  others: string;
}

interface GeneratedResults {
  [key: string]: string;
}

const activeTab = ref('basis');
const isLoading = ref(false);
const isCopying = ref(false);
const isDownloading = ref(false);

const projectInfo = ref<ProjectInfo>({
  basis: '',
  content: '',
  plan: '',
  innovation: '',
  schedule: '',
  foundation: '',
  conditions: '',
  relatedProjects: '',
  completedProjects: '',
  others: ''
});

const generatedResults = ref<GeneratedResults>({});

const tabTitles: { [key: string]: string } = {
  basis: '立项依据',
  content: '研究内容',
  plan: '研究方案',
  innovation: '特色创新',
  schedule: '年度计划',
  foundation: '研究基础',
  conditions: '工作条件',
  relatedProjects: '相关项目',
  completedProjects: '基金完成情况',
  others: '其他说明'
};

const placeholderTexts: { [key: string]: string } = {
  basis: '研究意义、国内外研究现状及发展动态分析，需结合科学研究发展趋势来论述科学意义；或结合国民经济和社会发展中迫切需要解决的关键科技问题来论述其应用前景...',
  content: '请描述本项目的研究内容、研究目标、关键科学问题等,此部分为重点阐述内容',
  plan: '包括研究方法、技术路线、实验手段、关键技术等说明',
  innovation: '请描述本项目的特色与创新点，包括理论创新、技术创新等...',
  schedule: '包括拟组织的重要学术交流活动、国际合作与交流计划等...',
  foundation: '与本项目相关的研究工作积累和已取得的研究工作成绩',
  conditions: '包括已具备的实验条件，尚缺少的实验条件和拟解决的途径，包括利用国家实验室、全国重点实验室和部门重点实验室等研究基地的计划与落实情况',
  relatedProjects: '申请人和主要参与者正在承担的与本项目相关的科研项目情况，包括国家自然科学基金的项目和国家其他科技计划项目，要注明项目的资助机构、项目类别、批准号、项目名称、获资助金额、起止年月、与本项目的关系及负责的内容等',
  completedProjects: '对申请人负责的前一个已资助期满的科学基金项目（项目名称及批准号）完成情况、后续研究进展及与本申请项目的关系加以详细说明。另附该项目的研究工作总结摘要（限500字）和相关成果详细目录',
  others: '申请人同年申请不同类型的国家自然科学基金项目情况、具有高级专业技术职务（职称）的申请人或者主要参与者是否存在同年申请或者参与申请国家自然科学基金项目的单位不一致的情况、具有高级专业技术职务（职称）的申请人或者主要参与者是否存在与正在承担的国家自然科学基金项目的单位不一致的情况；如存在上述情况'
};

const tabOrder = [
  'basis',
  'content',
  'plan',
  'innovation',
  'schedule',
  'foundation',
  'conditions',
  'relatedProjects',
  'completedProjects',
  'others'
];

const getActiveStep = computed(() => {
  return tabOrder.indexOf(activeTab.value) + 1;
});

const getStepStatus = (tabName: string) => {
  const currentIndex = tabOrder.indexOf(activeTab.value);
  const targetIndex = tabOrder.indexOf(tabName);
  
  if (targetIndex === currentIndex) {
    return 'process';
  } else if (targetIndex < currentIndex) {
    return 'finish';
  }
  return 'wait';
};

const getCurrentTabTitle = computed(() => {
  return tabTitles[activeTab.value] || '';
});

const getCurrentPlaceholder = computed(() => {
  return placeholderTexts[activeTab.value] || `请详细描述${getCurrentTabTitle.value}`;
});

const clearCurrentTab = () => {
  projectInfo.value[activeTab.value] = '';
  generatedResults.value[activeTab.value] = '';
};

const generateContent = async () => {
  if (!projectInfo.value[activeTab.value]?.trim()) {
    ElMessage.error(`请填写${getCurrentTabTitle.value}`);
    return;
  }

  const maxRetries = 3;
  const timeout = 10000;
  let currentRetry = 0;

  const makeRequest = async () => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      isLoading.value = true;
      // 清空当前标签页的生成结果
      generatedResults.value[activeTab.value] = '';
      
      // 构造请求数据
      const requestData = {
        theme: 'fund_writing',
        content: projectInfo.value[activeTab.value],
        paragraph: tabTitles[activeTab.value]
      };
      
      console.log('发送请求数据：', requestData);
      
      const response = await fetch('http://10.137.0.20:5000/dify_api', {
        method: 'POST',
        headers: {
          'Accept': 'text/event-stream',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('请求错误：', response.status, errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法获取响应流');
      }

      const decoder = new TextDecoder();
      let buffer = '';
      let isReading = true;
      let rawContent = '';
      let hasReceivedFirstChunk = false;
      
      while (isReading) {
        const { done, value } = await reader.read();
        if (done) {
          isReading = false;
          continue;
        }

        // 将接收到的数据添加到缓冲区
        buffer += decoder.decode(value, { stream: true });

        // 处理缓冲区中的完整消息
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // 保留最后一个不完整的消息
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.slice(6); // 移除 "data: " 前缀
              if (!jsonStr.trim()) continue;
              
              const data = JSON.parse(jsonStr);
              
              if (data.type === 'text' && data.full_text) {
                if (!hasReceivedFirstChunk) {
                  hasReceivedFirstChunk = true;
                  isLoading.value = false; // 收到第一个响应时就停止加载状态
                }
                
                // 更新原始内容
                rawContent = data.full_text;
                // 将 Markdown 转换为 HTML
                const htmlContent = markdownToHtml(rawContent);
                // 更新显示内容
                generatedResults.value[activeTab.value] = htmlContent;
                
                // 自动滚动到底部
                await nextTick(() => {
                  const resultElement = document.querySelector('.outline-content');
                  if (resultElement) {
                    resultElement.scrollTop = resultElement.scrollHeight;
                  }
                });
              }
            } catch (e) {
              console.error('解析 JSON 失败:', e);
            }
          }
        }
      }

    } catch (error) {
      clearTimeout(timeoutId);
      
      if ((error as { name?: string }).name === 'AbortError') {
        console.log('请求超时，准备重试');
        throw new Error('请求超时');
      }
      throw error;
    }
  };

  while (currentRetry < maxRetries) {
    try {
      await makeRequest();
      break; // 如果成功，跳出循环
    } catch (error) {
      currentRetry++;
      console.error(`第 ${currentRetry} 次请求失败:`, error);
      
      if (currentRetry === maxRetries) {
        ElMessage.error('生成失败，请稍后重试');
        console.error('Error:', error);
        break;
      } else {
        ElMessage.warning(`请求超时，正在进行第 ${currentRetry + 1} 次重试...`);
      }
    }
  }

  isLoading.value = false;
};

// Markdown 转 HTML 的辅助函数
const markdownToHtml = (markdownText: string): string => {
  if (!markdownText || typeof markdownText !== 'string') {
    return markdownText || '';
  }

  let processedText = markdownText;

  // 处理有序列表（确保序号正确显示）
  processedText = processedText.replace(/^\d+\.\s+(.+)$/gm, (match, content, index) => {
    return `<li value="${index + 1}">${content.trim()}</li>`;
  });
  processedText = processedText.replace(/(<li[^>]*>.*?<\/li>\n?)+/g, '<ol>$&</ol>');

  // 处理标题
  processedText = processedText.replace(/^(#{1,6})\s+(.+)$/gm, (match, hashes, content) => {
    const level = hashes.length;
    return `<h${level}>${content.trim()}</h${level}>`;
  });

  // 处理加粗
  processedText = processedText.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // 处理斜体
  processedText = processedText.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // 处理无序列表
  processedText = processedText.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>');
  processedText = processedText.replace(/(<li>.*?<\/li>\n?)+/g, '<ul>$&</ul>');

  // 处理引用
  processedText = processedText.replace(/^>\s+(.+)$/gm, '<blockquote>$1</blockquote>');

  // 处理段落
  const lines = processedText.split('\n');
  let inList = false;
  processedText = lines.map(line => {
    const trimmedLine = line.trim();
    if (trimmedLine === '') return '';
    if (trimmedLine.startsWith('<') && trimmedLine.endsWith('>')) {
      inList = trimmedLine.startsWith('<li>') || trimmedLine.startsWith('<ul>') || trimmedLine.startsWith('<ol>');
      return line;
    }
    if (inList) return line;
    return `<p>${line}</p>`;
  }).filter(line => line !== '').join('\n');

  return processedText;
};

const copyContent = async () => {
  if (!generatedResults.value[activeTab.value]) {
    ElMessage.warning('没有可复制的内容');
    return;
  }

  try {
    isCopying.value = true;
    await navigator.clipboard.writeText(generatedResults.value[activeTab.value]);
    ElMessage.success('复制成功');
  } catch (error) {
    console.error('Copy failed:', error);
    ElMessage.error('复制失败');
  } finally {
    isCopying.value = false;
  }
};

const downloadContent = () => {
  if (!generatedResults.value[activeTab.value]) {
    ElMessage.warning('没有可下载的内容');
    return;
  }

  try {
    isDownloading.value = true;
    
    // 创建Word文档的HTML内容
    const wordContent = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office' 
            xmlns:w='urn:schemas-microsoft-com:office:word' 
            xmlns='http://www.w3.org/TR/REC-html40'>
      <head>
        <meta charset="utf-8">
        <title>${tabTitles[activeTab.value]}</title>
        <style>
          body { font-family: 'SimSun', serif; line-height: 1.8; }
          p { text-indent: 2em; margin: 0.5em 0; }
          h1, h2, h3, h4, h5, h6 { font-weight: bold; margin: 0.8em 0 0.4em; }
          ul, ol { margin: 0.5em 0; padding-left: 2em; }
          li { margin: 0.3em 0; }
        </style>
      </head>
      <body>
        <h1 style="text-align: center; margin-bottom: 1em;">${tabTitles[activeTab.value]}</h1>
        ${generatedResults.value[activeTab.value]}
      </body>
      </html>
    `;
    
    // 生成文件名
    const fileName = `${tabTitles[activeTab.value]}_${new Date().toLocaleDateString('zh-CN').replace(/\//g, '')}`;
    
    // 创建Blob对象
    const blob = new Blob([wordContent], { type: 'application/vnd.ms-word;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    // 创建下载链接
    const link = document.createElement('a');
    link.href = url;
    link.download = `${fileName}.doc`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    ElMessage.success('文档已下载');
  } catch (error) {
    console.error('下载失败:', error);
    ElMessage.error('下载失败，请稍后重试');
  } finally {
    isDownloading.value = false;
  }
};

// 监听标签页切换
watch(activeTab, () => {
  isLoading.value = false;
});
</script>

<style scoped>
.general-fund-writing {
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  background-color: #f5f7fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: -20px -20px 10px -20px;
  background: #fff;
  padding: 20px 40px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
  width: calc(100% + 40px);
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
  font-size: 20px;
  color: #333;
  margin: 0;
  font-weight: 600;
}

.version {
  font-size: 14px;
  color: #909399;
  margin-left: 8px;
}

.tutorial-btn {
  display: flex;
  align-items: center;
  gap: 4px;
}

.steps-navigation {
  margin: 5px 0 15px 0;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
}

:deep(.el-steps) {
  overflow-x: auto;
  padding-bottom: 10px;
}

:deep(.el-steps__item) {
  cursor: pointer;
}

:deep(.el-step__icon) {
  width: 30px;
  height: 30px;
}

:deep(.step-number) {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}

:deep(.el-step__head.is-wait) .step-number {
  background-color: #C0C4CC;
  color: white;
}

:deep(.el-step__head.is-process) .step-number {
  background-color: #409EFF;
  color: white;
}

:deep(.el-step__head.is-finish) .step-number {
  background-color: #409EFF;
  color: white;
}

:deep(.el-step__line) {
  height: 2px;
}

:deep(.el-step__line-inner) {
  border-width: 2px;
}

:deep(.el-step.is-horizontal .el-step__line) {
  height: 2px;
  top: 15px;
  left: 50%;
  right: -50%;
}

:deep(.el-step__head.is-wait) {
  color: #C0C4CC;
  border-color: #C0C4CC;
}

:deep(.el-step__title.is-wait) {
  color: #C0C4CC;
}

:deep(.el-step__head.is-process) {
  color: #409EFF;
  border-color: #409EFF;
}

:deep(.el-step__title.is-process) {
  color: #409EFF;
  font-weight: bold;
}

:deep(.el-step__head.is-finish) {
  color: #409EFF;
  border-color: #409EFF;
}

:deep(.el-step__title.is-finish) {
  color: #409EFF;
}

:deep(.el-step.is-horizontal .el-step__line.is-wait) {
  background-color: #C0C4CC;
}

:deep(.el-step__line.is-finish) {
  background-color: #409EFF;
}

.main-content {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0;
}

.input-section, .result-section {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.input-block {
  flex: 1;
  display: flex;
  flex-direction: column;
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

.label-text {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.required {
  color: #F56C6C;
  margin-left: 4px;
}

:deep(.el-textarea__inner) {
  flex: 1;
  min-height: 300px !important;
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
  margin-top: 20px;
  justify-content: center;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #EBEEF5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
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

.outline-result {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  position: relative;
}

.outline-content {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  white-space: pre-wrap;
  font-size: 15px;
  line-height: 1.8;
  color: #333;
  transition: all 0.3s ease;
  overflow-y: auto;
  max-height: calc(100vh - 355px);
  position: relative;
  border: 1px solid #e4e7ed;
  
  :deep(ol) {
    counter-reset: item;
    list-style-type: decimal;
    margin: 0.5em 0;
    padding-left: 2em;
  }

  :deep(ol li) {
    display: block;
    margin: 0.3em 0;
    line-height: 1.8;
  }

  :deep(ol li::before) {
    content: counters(item, ".") ". ";
    counter-increment: item;
  }

  :deep(p) {
    margin: 0.5em 0;
    line-height: 1.8;
    text-align: justify;
    text-indent: 2em;
  }

  :deep(ul), :deep(ol) {
    margin: 0.5em 0;
    padding-left: 2em;
  }

  :deep(li) {
    margin: 0.3em 0;
    line-height: 1.8;
  }

  :deep(blockquote) {
    margin: 0.5em 0;
    padding: 0.5em 1em;
    border-left: 4px solid #42b983;
    background-color: #f8f8f8;
    color: #666;
  }

  :deep(strong) {
    font-weight: 600;
    color: #2c3e50;
  }

  :deep(em) {
    font-style: italic;
    color: #34495e;
  }
}

.outline-content :deep(h1),
.outline-content :deep(h2),
.outline-content :deep(h3),
.outline-content :deep(h4),
.outline-content :deep(h5),
.outline-content :deep(h6) {
  margin: 0.8em 0 0.4em;
  line-height: 1.4;
  color: #2c3e50;
  font-weight: 600;
}

.outline-content :deep(h1) { font-size: 1.8em; }
.outline-content :deep(h2) { font-size: 1.5em; }
.outline-content :deep(h3) { font-size: 1.3em; }
.outline-content :deep(h4) { font-size: 1.2em; }
.outline-content :deep(h5) { font-size: 1.1em; }
.outline-content :deep(h6) { font-size: 1em; }

.loading-result, .empty-result {
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

.light-bulb-icon {
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-text {
  color: #909399;
  font-size: 14px;
}

.disclaimer-text {
  margin-top: 16px;
  color: #909399;
  font-size: 12px;
  text-align: center;
}
</style> 