<template>
  <div class="writing-tools">
    <!-- 顶部应用类型导航 -->
    <div class="app-types">
      <div class="app-type-tabs">
        <div 
          class="app-type-tab" 
          :class="{ active: activeAppType === 'all' }"
          @click="switchAppType('all')"
        >
          <el-icon><grid /></el-icon>
          <span>全部应用类型</span>
        </div>
        <div 
          class="app-type-tab"
          :class="{ active: activeAppType === 'generate' }"
          @click="switchAppType('generate')"
        >
          <el-icon><histogram /></el-icon>
          <span>生成类应用</span>
        </div>
        <div 
          class="app-type-tab"
          @click="showUnderConstruction('对话类应用')"
        >
          <el-icon><chat-round /></el-icon>
          <span>对话类应用</span>
        </div>
        <div 
          class="app-type-tab"
          @click="showUnderConstruction('写作类应用')"
        >
          <el-icon><edit /></el-icon>
          <span>写作类应用</span>
        </div>
      </div>
    </div>
    
    <!-- 功能标签选择 -->
    <div class="function-tags">
      <div class="tag-list">
        <div 
          v-for="tag in tags" 
          :key="tag.value"
          :class="['tag-item', { active: activeTag === tag.value }]"
          @click="handleTagClick(tag.value)"
        >
          {{ tag.label }}
        </div>
      </div>
    </div>
    
    <!-- 应用卡片列表 -->
    <div class="application-list">
      <!-- 第一行卡片 -->
      <div class="card-row">
        <div 
          v-for="(app, index) in filteredApplications.slice(0, 3)" 
          :key="index"
          class="app-card"
          @click="openApplication(app)"
        >
          <div class="card-header">
            <div class="app-icon">
              <el-icon :size="40" :color="app.iconColor">
                <component :is="app.icon"></component>
              </el-icon>
            </div>
            <div class="app-title">
              <h3>{{ app.title }}</h3>
              <el-tag size="small" type="warning">硕博课题</el-tag>
            </div>
          </div>
          <div class="card-content">
            <p>{{ app.description }}</p>
          </div>
          <div class="card-footer">
            <el-icon><arrow-right /></el-icon>
          </div>
        </div>
      </div>
      
      <!-- 第二行卡片 -->
      <div class="card-row" v-if="filteredApplications.length > 3">
        <div 
          v-for="(app, index) in filteredApplications.slice(3, 6)" 
          :key="index+3" 
          class="app-card"
          @click="openApplication(app)"
        >
          <div class="card-header">
            <div class="app-icon">
              <el-icon :size="40" :color="app.iconColor">
                <component :is="app.icon"></component>
              </el-icon>
            </div>
            <div class="app-title">
              <h3>{{ app.title }}</h3>
              <el-tag size="small" type="warning">硕博课题</el-tag>
            </div>
          </div>
          <div class="card-content">
            <p>{{ app.description }}</p>
          </div>
          <div class="card-footer">
            <el-icon><arrow-right /></el-icon>
          </div>
        </div>
      </div>
      
      <!-- 第三行卡片 -->
      <div class="card-row" v-if="filteredApplications.length > 6">
        <div 
          v-for="(app, index) in filteredApplications.slice(6, 9)" 
          :key="index+6" 
          class="app-card"
          @click="openApplication(app)"
        >
          <div class="card-header">
            <div class="app-icon">
              <el-icon :size="40" :color="app.iconColor">
                <component :is="app.icon"></component>
              </el-icon>
            </div>
            <div class="app-title">
              <h3>{{ app.title }}</h3>
              <el-tag size="small" type="warning">硕博课题</el-tag>
            </div>
          </div>
          <div class="card-content">
            <p>{{ app.description }}</p>
          </div>
          <div class="card-footer">
            <el-icon><arrow-right /></el-icon>
          </div>
        </div>
      </div>
 
      <!-- 第四行卡片 -->
      <div class="card-row" v-if="filteredApplications.length > 9">
        <div 
          v-for="(app, index) in filteredApplications.slice(9, 12)" 
          :key="index+9" 
          class="app-card"
          @click="openApplication(app)"
        >
          <div class="card-header">
            <div class="app-icon">
              <el-icon :size="40" :color="app.iconColor">
                <component :is="app.icon"></component>
              </el-icon>
            </div>
            <div class="app-title">
              <h3>{{ app.title }}</h3>
              <el-tag size="small" type="warning">硕博课题</el-tag>
            </div>
          </div>
          <div class="card-content">
            <p>{{ app.description }}</p>
          </div>
          <div class="card-footer">
            <el-icon><arrow-right /></el-icon>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  Grid, 
  Histogram, 
  ChatRound, 
  Edit, 
  ArrowRight, 
  Document, 
  Collection,
  Connection,
  Reading,
  DocumentCopy,
  Promotion,
  EditPen,
  Link,
  ChatDotRound,
  Files,
  DocumentChecked,
  Notebook,
  DataAnalysis,
  DocumentAdd,
  Management
} from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'WritingTools',
  components: {
    Grid,
    Histogram,
    ChatRound,
    Edit,
    ArrowRight,
    Document,
    Collection,
    Connection,
    Reading,
    DocumentCopy,
    Promotion,
    EditPen,
    Link,
    ChatDotRound,
    Files,
    DocumentChecked,
    Notebook,
    DataAnalysis,
    DocumentAdd,
    Management
  },
  setup() {
    const activeTag = ref('all');
    const activeAppType = ref('all');
    const router = useRouter();
    
    const tags = [
      { label: '全部', value: 'all' },
      { label: '分步论文写作', value: 'paper' },
      { label: '综述写作', value: 'abstract' },
      { label: '文章段落写作', value: 'paragraph' },
      { label: '预读课题', value: 'preread' },
      { label: '辅助工具', value: 'tools' },
      { label: '投稿与修回', value: 'submit' },
      { label: '专利申请', value: 'patent' },
      { label: '出国留学', value: 'abroad' },
      { label: '翻译工具', value: 'translation' }
    ];
    
    const applications = ref([
      {
        title: '硕士开题报告Step 1: 生成提纲',
        description: '输入硕士课题要点及其相关补充材料（关键词、实验方法等），生成课题开题报告大纲。',
        icon: 'Files',
        iconColor: '#409EFF',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '硕士开题报告Step 2: 生成全文',
        description: '用户输入开题报告大纲，生成开题报告全文。',
        icon: 'DocumentChecked',
        iconColor: '#67C23A',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '研究生学位论文中期报告',
        description: '用户输入课题名称、已完成的实验结果和未来研究计划，生成研究生学位论文中期报告。',
        icon: 'Notebook',
        iconColor: '#E6A23C',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '硕士论文Step 1: 生成提纲',
        description: '用户输入实验方法和结果，生成硕士论文提纲。',
        icon: 'Document',
        iconColor: '#F56C6C',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '硕士论文Step 2: 生成前言',
        description: '用户输入实验方法、结果和理论，生成硕士论文前言部分。',
        icon: 'Collection',
        iconColor: '#909399',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '硕士论文Step 3: 生成正文',
        description: '用户输入实验方法、结果和理论，生成硕士论文正文部分。',
        icon: 'DocumentCopy',
        iconColor: '#409EFF',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '科研计划书Step 1: 生成提纲',
        description: '输入科研计划的课题范围或目标研究方向、分子、通路等信息，生成科研计划书提纲。',
        icon: 'DataAnalysis',
        iconColor: '#67C23A',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '科研计划书Step 2: 生成正文',
        description: '输入科研计划书提纲，生成科研计划书正文。',
        icon: 'Management',
        iconColor: '#E6A23C',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '博士开题报告Step 1: 生成提纲',
        description: '输入博士课题要点及其相关补充材料（关键词、实验方法等），生成课题开题报告大纲。',
        icon: 'DocumentAdd',
        iconColor: '#F56C6C',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '博士开题报告Step 2: 生成全文',
        description: '用户输入开题报告大纲，生成开题报告全文。',
        icon: 'Document',
        iconColor: '#409EFF',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '博士论文Step 1: 生成摘要',
        description: '用户输入实验方法和结果，生成博士论文的摘要部分。',
        icon: 'EditPen',
        iconColor: '#67C23A',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '博士论文Step 2: 生成前言',
        description: '用户输入论文主题、实验方法和结果，生成博士论文的前言部分，运用最新和课题设计。',
        icon: 'Reading',
        iconColor: '#E6A23C',
        type: 'paper',
        appType: 'generate'
      },
      {
        title: '期刊投稿与撤回',
        description: '提供Nature、Science、Cell等顶级期刊的投稿指南和撤回流程。',
        icon: 'Promotion',
        iconColor: '#409EFF',
        type: 'submit',
        appType: 'generate'
      }
    ]);
    
    // 根据应用类型和标签过滤应用
    const filteredApplications = computed(() => {
      let result = applications.value;
      
      // 根据应用类型筛选
      if (activeAppType.value !== 'all') {
        result = result.filter(app => app.appType === activeAppType.value);
      }
      
      // 根据标签筛选
      if (activeTag.value !== 'all') {
        result = result.filter(app => app.type === activeTag.value);
      }
      
      return result;
    });
    
    // 切换应用类型
    const switchAppType = (type: string) => {
      activeAppType.value = type;
    };
    
    // 显示正在建设中的提示
    const showUnderConstruction = (typeName: string) => {
      ElMessage({
        message: `${typeName}功能正在建设中，敬请期待！`,
        type: 'info',
        duration: 3000
      });
    };
    
    const openApplication = (app: any) => {
      console.log('打开应用：', app.title);
      
      // 根据应用标题判断跳转路径
      if (app.title === '硕士开题报告Step 1: 生成提纲') {
        router.push('/thesis-outline');
        return;
      }
      
      if (app.title === '期刊投稿与撤回') {
        router.push('/journal-submission');
        return;
      }
      
      // 其他应用显示即将上线的提示
      ElMessage({
        message: '该功能即将上线，敬请期待！',
        type: 'success',
        duration: 3000
      });
    };
    
    // 修改标签点击事件处理
    const handleTagClick = (tagValue: string) => {
      activeTag.value = tagValue;
      if (tagValue === 'submit') {
        router.push('/journal-submission');
      }
    };
    
    return {
      activeTag,
      activeAppType,
      tags,
      applications,
      filteredApplications,
      switchAppType,
      showUnderConstruction,
      openApplication,
      handleTagClick
    };
  }
});
</script>

<style scoped>
.writing-tools {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100%;
}

.app-types {
  background-color: white;
  padding: 15px 20px;
  border-radius: 12px;
  margin-bottom: 25px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.app-type-tabs {
  display: flex;
  gap: 40px;
  padding: 0 10px;
}

.app-type-tab {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  transition: all 0.3s;
}

.app-type-tab:hover {
  color: #409EFF;
  background-color: #ecf5ff;
}

.app-type-tab.active {
  color: #409EFF;
  font-weight: bold;
  background-color: #ecf5ff;
}

.function-tags {
  margin-bottom: 30px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 0 20px;
}

.tag-item {
  background-color: white;
  border-radius: 20px;
  padding: 10px 25px;
  font-size: 15px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  border: 1px solid #ebeef5;
}

.tag-item:hover {
  color: #409EFF;
  border-color: #409EFF;
  transform: translateY(-2px);
}

.tag-item.active {
  background-color: #409EFF;
  color: white;
  border-color: #409EFF;
}

.card-row {
  display: flex;
  gap: 25px;
  margin-bottom: 25px;
}

.app-card {
  flex: 1;
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  min-height: 220px;
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.app-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, #409EFF, #67C23A, #E6A23C, #F56C6C);
  transform: translateY(5px);
  transition: transform 0.3s;
}

.app-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #eaeaea;
}

.app-card:hover::after {
  transform: translateY(0);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.app-icon {
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background-color: #f5f7fa;
}

.app-title h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.card-content {
  flex-grow: 1;
  color: #606266;
  font-size: 15px;
  line-height: 1.6;
}

.card-footer {
  margin-top: 18px;
  text-align: right;
  color: #409EFF;
  font-size: 16px;
  opacity: 0;
  transform: translateX(-20px);
  transition: all 0.3s;
}

.app-card:hover .card-footer {
  opacity: 1;
  transform: translateX(0);
}

.el-tag {
  border-radius: 4px;
  padding: 2px 8px;
}
</style> 