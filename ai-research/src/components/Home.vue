<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <el-icon class="logo-icon" :size="28">
          <Monitor />
        </el-icon>
        <h2 class="site-title">AI+科研</h2>
      </div>
      <div class="header-center">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索内容..."
          prefix-icon="el-icon-search"
          class="search-input"
        >
          <template #prefix>
            <el-icon><search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="header-right">
        <el-avatar :size="36" src="https://placeholder.co/36x36"></el-avatar>
      </div>
    </el-header>

    <el-container class="main-container">
      <!-- 左侧菜单栏 -->
      <el-aside width="220px" class="aside">
        <el-menu
          :default-active="activeMenuItem"
          class="side-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="all-apps">
            <el-icon><grid /></el-icon>
            <span>全部应用</span>
          </el-menu-item>
          <el-menu-item index="chat">
            <el-icon><chat-dot-round /></el-icon>
            <span>智能对话</span>
          </el-menu-item>
          <el-menu-item index="ai-workspace">
            <el-icon><monitor /></el-icon>
            <span>AI工作台</span>
          </el-menu-item>
          <el-menu-item index="project-application">
            <el-icon><document /></el-icon>
            <span>课题申请</span>
          </el-menu-item>
          <el-menu-item index="collaboration">
            <el-icon><connection /></el-icon>
            <span>写作工具</span>
          </el-menu-item>
          <el-menu-item index="papers">
            <el-icon><reading /></el-icon>
            <span>文献阅读</span>
          </el-menu-item>
          <el-menu-item index="basic-research">
            <el-icon><list /></el-icon>
            <span>基础科研</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 右侧内容区域 -->
      <el-main class="main-content">
        <router-view v-if="$route.path !== '/'" />
        <div v-if="$route.path === '/'" class="welcome">
          <h2>欢迎使用 AI+科研 平台</h2>
          <p>请从左侧菜单选择功能</p>
          
          <div class="feature-cards">
            <el-card v-for="(feature, index) in features" :key="index" class="feature-card">
              <el-icon class="feature-icon">
                <component :is="featureIcons[feature.icon]"></component>
              </el-icon>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
              <el-button type="primary" @click="handleMenuSelect(feature.key)">开始使用</el-button>
            </el-card>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, shallowRef } from 'vue';
import { 
  Search, 
  ChatDotRound, 
  Document, 
  Monitor, 
  Connection, 
  Reading, 
  List,
  Grid
} from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'HomeView',
  components: {
    Search,
    ChatDotRound,
    Document,
    Monitor,
    Connection,
    Reading,
    List,
    Grid
  },
  setup() {
    const router = useRouter();
    const searchKeyword = ref('');
    const activeMenuItem = ref('');
    const currentView = shallowRef(null);
    
    const featureIcons = {
      chat: ChatDotRound,
      document: Document,
      monitor: Monitor
    };
    
    const features = [
      {
        title: '智能对话',
        description: '与先进的AI进行自然语言交流，解答疑问和获取专业建议',
        icon: 'chat',
        key: 'chat'
      },
      {
        title: '课题申请',
        description: '轻松准备和管理科研项目的申请材料，提高申请成功率',
        icon: 'document',
        key: 'project-application'
      },
      {
        title: 'AI工作台',
        description: '利用AI辅助进行数据分析、实验设计和结果可视化',
        icon: 'monitor',
        key: 'ai-workspace'
      }
    ];

    const handleMenuSelect = (index: string) => {
      activeMenuItem.value = index;
      
      // 使用router进行导航
      if (index) {
        // 将菜单项ID转换为路由路径
        const path = `/${index}`;
        console.log(`导航到路径: ${path}`);
        
        // 实际执行导航
        router.push(path);
      }
    };

    return {
      searchKeyword,
      activeMenuItem,
      currentView,
      handleMenuSelect,
      features,
      featureIcons
    };
  }
});
</script>

<style scoped>
.home-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  height: 70px;
  position: relative;
  z-index: 2;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo-icon {
  margin-right: 10px;
  color: #409EFF;
  font-size: 28px;
}

.site-title {
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  color: #409EFF;
}

.header-center {
  flex: 1;
  max-width: 500px;
  margin: 0 40px;
}

.search-input {
  width: 100%;
}

.main-container {
  flex: 1;
  overflow: hidden;
}

.aside {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  position: relative;
  z-index: 1;
  padding-top: 20px;
}

.side-menu {
  border-right: none;
  height: 100%;
}

.side-menu .el-menu-item {
  height: 60px;
  line-height: 60px;
  padding: 0 20px;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 8px;
  border-radius: 4px;
  margin-left: 8px;
  margin-right: 8px;
}

.side-menu .el-menu-item:last-child {
  margin-bottom: 0;
}

.side-menu .el-menu-item.is-active {
  background-color: #ecf5ff;
  color: #409EFF;
  border-right: 3px solid #409EFF;
}

.side-menu .el-icon {
  margin-right: 10px;
  font-size: 18px;
}

.side-menu .el-menu-item span {
  transition: all 0.3s;
  font-weight: bold;
}

.side-menu .el-menu-item .el-icon {
  margin-right: 8px;
  margin-left: -15px;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
}

.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #606266;
}

.welcome h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.welcome p {
  font-size: 16px;
  margin-bottom: 40px;
}

.feature-cards {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 30px;
  margin-top: 30px;
}

.feature-card {
  width: 300px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 15px;
}

.feature-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #303133;
}

.feature-card p {
  font-size: 14px;
  color: #606266;
  margin-bottom: 20px;
}
</style>
