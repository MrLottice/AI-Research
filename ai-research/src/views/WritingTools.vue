<template>
  <div class="writing-tools">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Promotion /></el-icon>
        <h2 class="page-title">硕博论文写作</h2>
        <span class="version">v1.0.0</span>
      </div>
      <div class="header-right">
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 分类标签 -->
      <div class="category-tags">
        <el-tag
          v-for="tag in tags"
          :key="tag.value"
          :type="activeTag === tag.value ? 'primary' : 'info'"
          class="category-tag"
          @click="handleTagClick(tag.value)"
        >
          {{ tag.label }}
        </el-tag>
      </div>

      <!-- 应用卡片列表 -->
      <div class="application-cards">
        <el-card
          v-for="app in filteredApplications"
          :key="app.title"
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
              <h3 class="app-title-text">{{ app.title }}</h3>
              <el-tag
                :type="getTagType(app.type)"
                size="small"
                class="type-tag"
              >
                {{ getTagLabel(app.type) }}
              </el-tag>
            </div>
          </div>
          <div class="card-content">
            <p class="app-description">{{ app.description }}</p>
          </div>
          <div class="card-footer">
            <el-icon><arrow-right /></el-icon>
          </div>
        </el-card>
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
      { label: '硕士研究生', value: 'master' },
      { label: '博士研究生', value: 'doctor' }
    ];
    
    const applications = ref([
      {
        title: '硕士开题报告Step 1: 生成提纲',
        description: '输入硕士课题要点及其相关补充材料（关键词、实验方法等），生成课题开题报告大纲。',
        icon: 'Files',
        iconColor: '#409EFF',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '硕士开题报告Step 2: 生成全文',
        description: '用户输入开题报告大纲，生成开题报告全文。',
        icon: 'DocumentChecked',
        iconColor: '#67C23A',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '研究生学位论文中期报告',
        description: '用户输入课题名称、已完成的实验结果和未来研究计划，生成研究生学位论文中期报告。',
        icon: 'Notebook',
        iconColor: '#E6A23C',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '硕士论文Step 1: 生成提纲',
        description: '用户输入实验方法和结果，生成硕士论文提纲。',
        icon: 'Document',
        iconColor: '#F56C6C',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '硕士论文Step 2: 生成前言',
        description: '用户输入实验方法、结果和理论，生成硕士论文前言部分。',
        icon: 'Collection',
        iconColor: '#909399',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '硕士论文Step 3: 生成正文',
        description: '用户输入实验方法、结果和理论，生成硕士论文正文部分。',
        icon: 'DocumentCopy',
        iconColor: '#409EFF',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '科研计划书Step 1: 生成提纲',
        description: '输入科研计划的课题范围或目标研究方向、分子、通路等信息，生成科研计划书提纲。',
        icon: 'DataAnalysis',
        iconColor: '#67C23A',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '科研计划书Step 2: 生成正文',
        description: '输入科研计划书提纲，生成科研计划书正文。',
        icon: 'Management',
        iconColor: '#E6A23C',
        type: 'master',
        appType: 'generate'
      },
      {
        title: '博士开题报告Step 1: 生成提纲',
        description: '输入博士课题要点及其相关补充材料（关键词、实验方法等），生成课题开题报告大纲。',
        icon: 'DocumentAdd',
        iconColor: '#F56C6C',
        type: 'doctor',
        appType: 'generate'
      },
      {
        title: '博士开题报告Step 2: 生成全文',
        description: '用户输入开题报告大纲，生成开题报告全文。',
        icon: 'Document',
        iconColor: '#409EFF',
        type: 'doctor',
        appType: 'generate'
      },
      {
        title: '博士论文Step 1: 生成摘要',
        description: '用户输入实验方法和结果，生成博士论文的摘要部分。',
        icon: 'EditPen',
        iconColor: '#67C23A',
        type: 'doctor',
        appType: 'generate'
      },
      {
        title: '博士论文Step 2: 生成前言',
        description: '用户输入论文主题、实验方法和结果，生成博士论文的前言部分，运用最新和课题设计。',
        icon: 'Reading',
        iconColor: '#E6A23C',
        type: 'doctor',
        appType: 'generate'
      },
      {
        title: '博士论文Step 3: 生成正文',
        description: '用户输入实验方法、结果和理论，生成博士论文正文部分。',
        icon: 'DocumentCopy',
        iconColor: '#F56C6C',
        type: 'doctor',
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
        window.open('/thesis-outline', '_blank');
        return;
      }
      
      if (app.title === '期刊投稿与撤回') {
        window.open('/journal-submission', '_blank');
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
    
    const getTagType = (type: string) => {
      switch (type) {
        case 'master':
          return 'success';
        case 'doctor':
          return 'danger';
        default:
          return 'info';
      }
    };
    
    const getTagLabel = (type: string) => {
      switch (type) {
        case 'master':
          return '硕士生';
        case 'doctor':
          return '博士生';
        default:
          return '通用';
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
      handleTagClick,
      getTagType,
      getTagLabel
    };
  }
});
</script>

<style scoped>
.writing-tools {
  padding: 0 20px 40px 20px;
  background-color: #f5f7fa;
  box-sizing: border-box;
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

.application-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  padding: 0 20px;
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
  min-height: 200px;
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  height: 64px;
  margin-bottom: 28px;
  margin-top: 0;
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
  padding: 20px;
}

.category-tags {
  display: flex;
  gap: 18px;
  margin-bottom: 36px;
  flex-wrap: wrap;
}

.category-tag {
  cursor: pointer;
  transition: all 0.3s;
  padding: 12px 32px;
  font-size: 18px;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(64,158,255,0.08);
  color: #409EFF;
  border: 1.5px solid #e6f0fa;
  font-weight: 500;
  margin-bottom: 6px;
}

.category-tag:hover {
  background: #ecf5ff;
  color: #1769aa;
  box-shadow: 0 4px 16px rgba(64,158,255,0.15);
  border-color: #b3d8fd;
  transform: translateY(-2px) scale(1.04);
}

.category-tag.el-tag--primary {
  background: linear-gradient(90deg, #409EFF 60%, #67C23A 100%);
  color: #fff;
  border-color: #409EFF;
  box-shadow: 0 4px 16px rgba(64,158,255,0.18);
}

.application-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  padding: 0 20px;
  align-items: stretch;
  max-width: 1600px;
  margin: 0 auto;
}

.app-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  min-height: 200px;
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

.app-title {
  flex: 1;
}

.app-title-text {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.type-tag {
  flex-shrink: 0;
  font-size: 14px;
  padding: 4px 8px;
}

.card-content {
  flex-grow: 1;
  color: #606266;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 15px;
}

.app-description {
  margin: 0;
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
</style> 