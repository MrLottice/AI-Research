<template>
  <div class="thesis-outline-container">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Lightbulb /></el-icon>
        <h2 class="page-title">硕士开题报告Step 1: 生成提纲</h2>
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

        <!-- 课题输入 -->
        <div class="input-block">
          <div class="input-label">
            <el-icon class="label-icon blue"><Medal /></el-icon>
            <span class="label-text">课题<span class="required">*</span></span>
          </div>
          <el-input
            type="textarea"
            v-model="thesisTitle"
            :rows="4"
            :maxlength="2000"
            placeholder="请输入课题要点及其实际开题报告大纲。例如：miRNA A通过靶向B基因清除TGF-β-诱导的xxx疾病中的成纤维细胞活化及纤维化"
          />
          <div class="char-count">{{ thesisTitle.length }} / 2000</div>
          <div class="import-btn">
            <el-button size="small" plain>
              <el-icon><Download /></el-icon>
              <span>从收藏导入</span>
            </el-button>
          </div>
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
            placeholder="请输入课题的关键词、科学假设、实验方法等补充信息，补充信息越详尽，生成的开题报告将更符合您的实际情况。"
          />
          <div class="char-count">{{ supplementaryInfo.length }} / 5000</div>
          <div class="import-btn">
            <el-button size="small" plain>
              <el-icon><Download /></el-icon>
              <span>从收藏导入</span>
            </el-button>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="large" plain @click="clearInputs" :disabled="isLoading">清空</el-button>
          <el-button size="large" type="primary" @click="generateOutline" :loading="isLoading">
            {{ isLoading ? '生成中...' : '提交' }}
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

        <!-- 加载中状态 - 流式输出版 -->
        <div v-if="isLoading && !isStreaming" class="loading-result">
          <div class="loading-animation">
            <div class="loading-spinner"></div>
          </div>
          <p class="loading-text">正在准备生成硕士开题报告提纲...</p>
          <p class="loading-tips">这可能需要几秒钟，请耐心等待</p>
        </div>

        <!-- 空结果状态 -->
        <div v-else-if="!outlineGenerated && !isStreaming" class="empty-result">
          <div class="light-bulb-icon">
            <img src="https://img.icons8.com/ios/100/409eff/idea.png" alt="灵感" />
          </div>
          <p class="empty-text">暂无内容，尚未成功生成！</p>
        </div>

        <!-- 生成结果状态 - 包含流式输出 -->
        <div v-else class="outline-result">
          <div class="outline-content" v-html="generatedOutline"></div>
          <div v-if="isStreaming" class="streaming-indicator">
            <div class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>AI正在思考并生成内容...</p>
          </div>
          <div v-if="!isStreaming" class="result-actions">
            <el-button size="small" type="primary" plain @click="copyContent" :loading="isCopying">
              <el-icon><Copy /></el-icon>
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
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

export default defineComponent({
  name: 'MasterThesisProposalOutline',
  components: {
    ...ElementPlusIconsVue
  },
  setup() {
    const thesisTitle = ref('');
    const supplementaryInfo = ref('');
    const outlineGenerated = ref(false);
    const generatedOutline = ref('');
    const isLoading = ref(false);
    const isCopying = ref(false);
    const isDownloading = ref(false);
    const streamingContent = ref('');
    const isStreaming = ref(false);
    let abortController: AbortController | null = null;

    // 辅助函数：将Markdown文本转换为HTML
    const markdownToHtml = (markdownText: string): string => {
      if (!markdownText || markdownText.includes('<')) {
        return markdownText; // 如果已经包含HTML标签，则不处理
      }
      
      // 预处理 - 处理加粗文本和表格
      let processedText = markdownText;
      
      // 处理加粗文本 (**text**)
      processedText = processedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // 处理斜体文本 (*text*)
      processedText = processedText.replace(/\*([^*]+)\*/g, '<em>$1</em>');
      
      // 处理表格
      // 将表格标记拆分为行
      const lines = processedText.split('\n');
      const processedLines = [];
      let inTable = false;
      let tableContent = '';
      let isTableHeader = false;
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // 检测表格开始
        if (line.startsWith('|') && line.endsWith('|')) {
          // 如果是表格的第一行
          if (!inTable) {
            inTable = true;
            tableContent = '<table class="md-table"><thead>';
            isTableHeader = true;
          }
          
          // 处理表格分隔行 (| --- | --- |)
          if (line.includes('---')) {
            isTableHeader = false;
            tableContent += '</thead><tbody>';
            continue;
          }
          
          // 处理正常的表格行
          const cells = line.split('|').filter(cell => cell.trim() !== '');
          if (cells.length > 0) {
            tableContent += '<tr>';
            cells.forEach(cell => {
              if (isTableHeader) {
                tableContent += `<th>${cell.trim()}</th>`;
              } else {
                tableContent += `<td>${cell.trim()}</td>`;
              }
            });
            tableContent += '</tr>';
          }
          
          // 检查下一行是否还是表格，如果不是则结束表格
          if (i === lines.length - 1 || !lines[i + 1].trim().startsWith('|')) {
            tableContent += isTableHeader ? '</thead></table>' : '</tbody></table>';
            processedLines.push(tableContent);
            inTable = false;
          }
        } else if (!inTable) {
          processedLines.push(line);
        }
      }
      
      // 用处理后的行替换原文本
      processedText = processedLines.join('\n');
      
      // 继续处理其他Markdown格式
      const lines2 = processedText.split('\n');
      const htmlLines = lines2.map(line => {
        // 处理标题
        if (line.trim().match(/^#{1,6}\s/)) {
          const matches = line.trim().match(/^(#{1,6})\s/);
          if (matches && matches[1]) {
            const titleLevel = matches[1].length;
            const titleText = line.trim().replace(/^#{1,6}\s/, '');
            return `<h${titleLevel}>${titleText}</h${titleLevel}>`;
          }
        }
        
        // 处理中文数字标题 (一、二、三、等)
        if (line.trim().match(/^[一二三四五六七八九十][、.．]/)) {
          return `<h3>${line}</h3>`;
        }
        
        // 处理列表项 - 无序列表 (- 或 *)
        if (line.trim().match(/^[-*]\s/)) {
          return `<li>${line.trim().replace(/^[-*]\s/, '')}</li>`;
        }
        
        // 处理有序列表项 (1. 2. 等)
        if (line.trim().match(/^\d+\.\s/)) {
          return `<li>${line.trim().replace(/^\d+\.\s/, '')}</li>`;
        }
        
        // 如果这行是一个完整的表格，直接返回
        if (line.startsWith('<table') && line.endsWith('</table>')) {
          return line;
        }
        
        // 处理普通段落
        return line.trim() ? `<p>${line}</p>` : '<br/>';
      });
      
      // 对列表项进行分组处理
      let result = '';
      let inList = false;
      let listType = '';
      
      for (let i = 0; i < htmlLines.length; i++) {
        const line = htmlLines[i];
        
        if (line.startsWith('<li>')) {
          if (!inList) {
            // 开始一个新列表
            inList = true;
            // 判断是否有序列表
            listType = htmlLines[i-1] && htmlLines[i-1].startsWith('<li>') ? listType : 'ul';
            result += `<${listType}>`;
          }
          result += line;
        } else {
          if (inList) {
            // 结束列表
            result += `</${listType}>`;
            inList = false;
          }
          result += line;
        }
      }
      
      // 关闭可能残留的列表
      if (inList) {
        result += `</${listType}>`;
      }
      
      return result;
    };

    const clearInputs = () => {
      thesisTitle.value = '';
      supplementaryInfo.value = '';
    };

    // 修改生成提纲函数以支持流式输出
    const generateOutline = async () => {
      if (!thesisTitle.value.trim()) {
        ElMessage.error('请先输入课题信息');
        return;
      }

      try {
        // 设置加载状态
        isLoading.value = true;
        outlineGenerated.value = false;
        generatedOutline.value = '';

        // 创建FormData对象
        const formData = new FormData();
        formData.append('title', thesisTitle.value);
        formData.append('examples', supplementaryInfo.value);
        formData.append('theme', 'master_thesis_proposal');
        
        // 创建一个新的AbortController
        abortController = new AbortController();

        // 发送请求到Flask后端
        const response = await fetch('http://10.137.0.20:5000/dify_api', {
          method: 'POST',
          body: formData,
          headers: {
            'Accept': 'text/event-stream',
          },
          signal: abortController.signal
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 获取响应的ReadableStream
        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error('无法获取响应流');
        }

        // 读取流数据
        let isDone = false;
        let buffer = '';
        let hasReceivedFirstChunk = false;
        
        while (!isDone) {
          const { done, value } = await reader.read();
          isDone = done;
          
          if (value) {
            // 将Uint8Array转换为文本并添加到缓冲区
            buffer += new TextDecoder().decode(value);
            
            // 处理缓冲区中的所有完整消息
            const lines = buffer.split('\n');
            buffer = lines.pop() || ''; // 保留最后一个不完整的行
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  // 提取JSON部分（去掉'data: '前缀）
                  const jsonStr = line.substring(6);
                  const jsonData = JSON.parse(jsonStr);
                  
                  if (jsonData.type === 'text' && jsonData.content) {
                    if (!hasReceivedFirstChunk) {
                      // 收到第一个数据块时，更新状态
                      isLoading.value = false;
                      outlineGenerated.value = true;
                      hasReceivedFirstChunk = true;
                    }
                    // 将新的内容转换为HTML并更新显示
                    generatedOutline.value = markdownToHtml(jsonData.full_text);
                  } else if (jsonData.type === 'done') {
                    // 处理完成事件
                    isLoading.value = false;
                    outlineGenerated.value = true;
                    generatedOutline.value = markdownToHtml(jsonData.full_text);
                    ElMessage.success('提纲生成完成！');
                  } else if (jsonData.type === 'error') {
                    // 处理错误事件
                    throw new Error(jsonData.message || '生成过程中发生错误');
                  }
                } catch (e) {
                  console.warn('解析消息失败:', e, line);
                }
              }
            }
          }
        }
      } catch (error: any) {
        console.error('API请求错误:', error);
        
        if (error.name === 'AbortError' || error.message === 'canceled') {
          ElMessage.info('请求已取消');
        } else {
          ElMessage.error('生成失败，请稍后重试');
        }
        
        outlineGenerated.value = false;
      } finally {
        isLoading.value = false;
        abortController = null;
      }
    };

    // 复制生成的内容
    const copyContent = async () => {
      if (!generatedOutline.value) {
        ElMessage.error('没有可复制的内容');
        return;
      }
      
      try {
        isCopying.value = true;
        
        // 创建一个临时元素来存储HTML内容
        const tempElement = document.createElement('div');
        tempElement.innerHTML = generatedOutline.value;
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

    // 下载生成的内容
    const downloadContent = () => {
      if (!generatedOutline.value) {
        ElMessage.error('没有可下载的内容');
        return;
      }
      
      try {
        isDownloading.value = true;
        
        // 创建一个临时元素来存储HTML内容
        const tempElement = document.createElement('div');
        tempElement.innerHTML = generatedOutline.value;
        const textContent = tempElement.textContent || tempElement.innerText || '';
        
        // 创建Blob对象
        const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
        
        // 创建下载链接
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `硕士开题报告提纲_${new Date().toISOString().split('T')[0]}.txt`;
        link.click();
        
        // 释放URL对象
        URL.revokeObjectURL(link.href);
        
        ElMessage.success('提纲已下载');
      } catch (error) {
        console.error('下载失败:', error);
        ElMessage.error('下载失败，请稍后重试');
      } finally {
        setTimeout(() => {
          isDownloading.value = false;
        }, 500); // 添加短暂延迟，让按钮动画效果更明显
      }
    };

    return {
      thesisTitle,
      supplementaryInfo,
      outlineGenerated,
      generatedOutline,
      isLoading,
      isCopying,
      isDownloading,
      isStreaming,
      streamingContent,
      clearInputs,
      generateOutline,
      copyContent,
      downloadContent
    };
  }
});
</script>

<style scoped>
.thesis-outline-container {
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

.tutorial-btn {
  display: flex;
  align-items: center;
}

.tutorial-btn .el-icon {
  margin-right: 5px;
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

.import-btn {
  margin-top: 10px;
  text-align: right;
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

.outline-result {
  padding: 10px;
}

.outline-content {
  margin-bottom: 20px;
  line-height: 1.6;
}

.outline-content h1 {
  font-size: 24px;
  margin-top: 25px;
  margin-bottom: 15px;
  color: #409EFF;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 8px;
}

.outline-content h2 {
  font-size: 20px;
  margin-top: 20px;
  margin-bottom: 12px;
  color: #409EFF;
}

.outline-content h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 18px;
  color: #409EFF;
}

.outline-content h4, .outline-content h5, .outline-content h6 {
  margin-top: 15px;
  margin-bottom: 8px;
  color: #333;
}

.outline-content p {
  margin-bottom: 8px;
  color: #555;
  text-align: justify;
}

.outline-content ul, .outline-content ol {
  margin-left: 20px;
  margin-bottom: 15px;
  color: #555;
}

.outline-content li {
  margin-bottom: 5px;
}

.outline-content code {
  background-color: #f5f7fa;
  padding: 2px 4px;
  border-radius: 3px;
  color: #e6a23c;
  font-family: Consolas, Monaco, 'Andale Mono', monospace;
}

.outline-content a {
  color: #409EFF;
  text-decoration: none;
}

.outline-content a:hover {
  text-decoration: underline;
}

.result-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

:deep(.el-textarea__inner) {
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
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

/* 自定义滚动条样式 */
.input-section::-webkit-scrollbar,
.result-section::-webkit-scrollbar {
  width: 8px;
}

.input-section::-webkit-scrollbar-track,
.result-section::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.input-section::-webkit-scrollbar-thumb,
.result-section::-webkit-scrollbar-thumb {
  background: #409EFF;
  border-radius: 4px;
}

.input-section::-webkit-scrollbar-thumb:hover,
.result-section::-webkit-scrollbar-thumb:hover {
  background: #337ecc;
}

.outline-content .md-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 0.9em;
}

.outline-content .md-table th,
.outline-content .md-table td {
  padding: 12px 15px;
  text-align: left;
  border: 1px solid #ddd;
}

.outline-content .md-table th {
  background-color: #ecf5ff;
  color: #409EFF;
  font-weight: bold;
}

.outline-content .md-table tr:hover {
  background-color: #f8f9fa;
}

.outline-content strong {
  font-weight: bold;
  color: #409EFF;
}

.outline-content em {
  font-style: italic;
  color: #606266;
}

/* 添加流式输出相关样式 */
.streaming-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  padding: 10px;
  background-color: #ecf5ff;
  border-radius: 4px;
}

.typing-dots {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.typing-dots span {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin: 0 3px;
  background-color: #409EFF;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
  animation-delay: 0s;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: scale(1);
    opacity: 0.4;
  }
  30% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.streaming-indicator p {
  margin: 0;
  color: #409EFF;
  font-size: 14px;
}

/* 优化流式输出内容的过渡效果 */
.outline-content {
  transition: all 0.3s ease;
}

.outline-result {
  position: relative;
}
</style> 