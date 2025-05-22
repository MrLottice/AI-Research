<template>
  <div class="home-layout">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <img src="../assets/sicaulogo.png" alt="学校 Logo" class="school-logo">
      </div>
      <div class="header-right">
        <el-avatar :size="36" src="https://img.icons8.com/color/96/000000/user-male-circle--v2.png"></el-avatar>
      </div>
    </el-header>
    <el-container class="main-container">
      <!-- 左侧菜单栏 -->
      <el-aside width="220px" class="aside">
        <div class="menu-title">
          <el-icon class="menu-icon"><Monitor /></el-icon>
          <h2>AI+科研</h2>
        </div>
        <el-menu :default-active="activeMenuItem" class="side-menu" @select="handleMenuSelect">
          <el-menu-item index="all-apps">
            <el-icon><Grid /></el-icon>
            <span>全部应用</span>
          </el-menu-item>
          <el-menu-item index="thesis-writing">
            <el-icon><Document /></el-icon>
            <span>硕博论文</span>
          </el-menu-item>
          <el-menu-item index="sci-paper">
            <el-icon><Monitor /></el-icon>
            <span>SCI论文</span>
          </el-menu-item>
          <el-menu-item index="review">
            <el-icon><Reading /></el-icon>
            <span>综述撰写</span>
          </el-menu-item>
          <el-menu-item index="nsfc">
            <el-icon><Connection /></el-icon>
            <span>国自然基金</span>
          </el-menu-item>
          <el-menu-item index="paper-review">
            <el-icon><List /></el-icon>
            <span>项目评审</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!-- 主内容区 -->
      <el-main class="main-content">
        <router-view />
        <template v-if="route.path === '/' || route.path === '/all-apps'">
          <div class="welcome-section">
            <img class="avatar" src="https://img.icons8.com/color/96/000000/user-male-circle--v2.png" />
            <div class="welcome-texts">
              <div class="welcome-title">
                <span>Hi，我是小农</span>
              </div>
              <div class="welcome-desc">
                我可以做助教好帮手，科研打磨、管理智脑，为你提供专业可定制的个性化服务，让我辅助你完成学习吧！
              </div>
            </div>
          </div>
          <div class="search-bar-card">
            <div class="input-button-wrapper">
              <el-input
                v-model="searchKeyword"
                class="search-input"
                placeholder="你想查询什么,快来问问吧"
                prefix-icon="el-icon-search"
              >
              </el-input>
              <el-button type="primary" :icon="Position" circle></el-button>
            </div>
            <div class="search-bar-actions">
            </div>
          </div>
          <div class="main-content-inner">
            <div class="section-title">全部应用</div>
            <div class="app-cards">
              <div
                v-for="app in appList"
                :key="app.title"
                class="app-card"
                :style="{ background: app.bg }"
                @click="handleCardClick(app.title)"
              >
                <div class="app-card-title">{{ app.title }}</div>
                <div class="app-card-desc">{{ app.desc }}</div>
              </div>
            </div>
          </div>
        </template>
      </el-main>
    </el-container>
    <!-- 添加页脚 -->
    <div class="footer">
      <div>Copyright © 2025 四川农业大学. Sichuan Agricultural University, All Rights Reserved.</div>
      <div>蜀ICP备09006192号-5 雅公网安备51180100004号</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { Monitor, Grid, Document, Reading, Connection, List, Position } from '@element-plus/icons-vue';
import { useRouter, useRoute } from 'vue-router';

const appList = ref([
  {
    title: 'SCI论著工作台',
    desc: '通过指定主题，AI辅助生成及交互式SCI论文的全文写作。',
    bg: 'linear-gradient(135deg, #7B1FA2 0%, #4A148C 100%)'
  },
  {
    title: '综述工作台',
    desc: '输入主题或摘要，AI辅助生成高质量综述型论文。',
    bg: 'linear-gradient(135deg, #6A1B9A 0%, #4527A0 100%)'
  },
  {
    title: '基金申请书工作台',
    desc: '通过选择学科领域及主题，AI辅助生成基金申请书文本。',
    bg: 'linear-gradient(135deg, #5E35B1 0%, #311B92 100%)'
  },
  {
    title: '文献生成研究方案',
    desc: '基于用户提供的论文或文献，辅助生成一份自然格式的研究内容和研究方案。',
    bg: 'linear-gradient(135deg, #8E24AA 0%, #6A1B9A 100%)'
  },
  {
    title: 'AI工作台',
    desc: '通过指定主题，AI辅助生成及交互式SCI论文的全文写作。',
    bg: 'linear-gradient(135deg, #7B1FA2 0%, #512DA8 100%)'
  },
  {
    title: '课题申请',
    desc: '输入主题或摘要，AI辅助生成课题申请书文本。',
    bg: 'linear-gradient(135deg, #6A1B9A 0%, #4527A0 100%)'
  },
  {
    title: '写作工具',
    desc: '通过选择学科领域和主题，AI辅助生成各类写作文本。',
    bg: 'linear-gradient(135deg, #5E35B1 0%, #4A148C 100%)'
  },
  {
    title: '文献阅读',
    desc: '基于用户提供的论文或文献，辅助生成一份自然格式的研究内容和研究方案。',
    bg: 'linear-gradient(135deg, #8E24AA 0%, #6A1B9A 100%)'
  }
]);

const activeMenuItem = ref('all-apps');
const router = useRouter();
const route = useRoute();
const searchKeyword = ref('');

const handleMenuSelect = (index: string) => {
  activeMenuItem.value = index;
  if (index === 'all-apps') {
    router.push('/');
  } else if (index === 'thesis-writing') {
    router.push('/collaboration');
  } else if (index === 'sci-paper') {
    router.push('/journal-submission');
  } else if (index === 'review') {
    router.push('/review-writing');
  } else if (index === 'paper-review') {
    router.push('/project-review');
  }
  // 其余菜单项可按需补充
};

const handleCardClick = (title: string) => {
  if (title === 'SCI论著工作台') {
    router.push('/journal-submission');
    activeMenuItem.value = 'sci-paper';  // 更新菜单高亮状态
  }
    

  // 其他卡片的跳转逻辑可以在这里添加
};

// 根据当前路由设置高亮的菜单项
watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/') {
      activeMenuItem.value = 'all-apps';
    } else if (newPath === '/collaboration') { // 硕博论文 path
      activeMenuItem.value = 'thesis-writing';
    } else if (newPath === '/journal-submission') { // SCI论文 path
      activeMenuItem.value = 'sci-paper';
    } else if (newPath === '/review-writing') { // 综述撰写 path
      activeMenuItem.value = 'review';
    } else if (newPath === '/project-review') { // 项目评审 path
      activeMenuItem.value = 'paper-review';
    } else if (newPath === '/molecular-biology') { // 分子生物学 path
      activeMenuItem.value = 'molecular-biology';
    }
  },
  { immediate: true }
);
</script>

<style scoped>
.home-layout {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止出现滚动条 */
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
  gap: 16px;
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
.header-right {
  display: flex;
  align-items: center;
}
.school-logo {
  height: 60px;
  width: auto;
  object-fit: contain;
}
.main-container {
  flex: 1;
  overflow: hidden;
  min-height: 0; /* 防止 flex 子元素溢出 */
}
.aside {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  position: relative;
  z-index: 1;
  padding-top: 24px;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.side-menu {
  border-right: none;
  height: calc(100% - 70px);
  width: 100%;
}
.side-menu .el-menu-item {
  height: 60px;
  line-height: 60px;
  padding: 0 20px;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  justify-content: flex-start;
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
  background-color: #e6fffb;
  color: #13c2c2;
  border-right: 3px solid #13c2c2;
}
.side-menu .el-icon {
  margin-right: 10px;
  margin-left: 0;
}
.side-menu .el-menu-item span {
  transition: all 0.3s;
  font-weight: bold;
  text-align: left;
}
.main-content {
  background: #f9f9f9;
  padding: 40px 0 0 0;
  flex: 1;
  overflow-y: auto; /* 主内容区域可滚动 */
  min-height: 0; /* 防止 flex 子元素溢出 */
}
.welcome-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 0;
  margin-bottom: 12px;
  text-align: center;
  width: 100%;
}
.welcome-texts {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}
.welcome-title {
  font-size: 26px;
  font-weight: 600;
  color: #222;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.welcome-desc {
  font-size: 15px;
  color: #666;
  margin-top: 2px;
  text-align: center;
  max-width: 500px;
}
.search-bar-card {
  width: 700px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px 0 rgba(64,158,255,0.08);
  padding: 28px 32px 18px 32px;
  margin: 0 auto 32px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.input-button-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  width: 100%;
}
.search-input {
  flex-grow: 1;
  font-size: 18px;
}
.search-bar-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 2px;
}
.search-bar-tip {
  color: #888;
  font-size: 15px;
  margin-left: 8px;
  margin-right: 8px;
}
.main-content-inner {
  width: 1200px;
  margin: 0 auto;
}
.section-title {
  font-size: 22px;
  font-weight: 700;
  color: #08979c;
  margin-bottom: 24px;
  margin-left: 2px;
  text-align: left;
}
.app-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px 24px;
}
.app-card {
  border-radius: 14px;
  box-shadow: 0 2px 12px 0 rgba(156, 39, 176, 0.1);
  color: #fff;
  padding: 22px 20px 18px 20px;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  cursor: pointer;
  transition: all 0.3s ease;
  background-size: 200% 200%;
  background-position: 0% 0%;
  position: relative;
  overflow: hidden;
}
.app-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 24px rgba(156, 39, 176, 0.2);
  background-position: 100% 100%;
}
.app-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 100%);
  z-index: 1;
}
.app-card-title {
  position: relative;
  z-index: 2;
  font-size: 19px;
  font-weight: bold;
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 1);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}
.app-card-desc {
  position: relative;
  z-index: 2;
  font-size: 14px;
  opacity: 0.95;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}
.el-button {
  width: 40px;
  height: 40px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50% !important;
}
.el-button :deep(.el-icon) {
  font-size: 18px;
}
.menu-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 20px;
  margin-bottom: 20px;
  width: 100%;
}

.menu-title h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #08979c;
  text-align: center;
}

.menu-icon {
  font-size: 24px;
  color: #13c2c2;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  margin-bottom: 16px;
}

/* 修改搜索按钮颜色 */
.el-button.el-button--primary {
  background-color: #13c2c2 !important;
  border-color: #13c2c2 !important;
}

.el-button.el-button--primary:hover {
  background-color: #36cfc9 !important;
  border-color: #36cfc9 !important;
}

/* 修改菜单项激活状态的颜色 */
.side-menu .el-menu-item:hover {
  color: #13c2c2;
}

.side-menu .el-menu-item.is-active .el-icon {
  color: #13c2c2;
}

/* 添加页脚样式 */
.footer {
  background-color: #006666;
  color: white;
  text-align: center;
  padding: 20px 0 0 0;
  font-size: 14px;
  width: 100%;
  margin: 0;
  border-radius: 0;
  position: relative;
  bottom: 0;
  left: 0;
  right: 0;
  border-bottom: 15px solid #004d4d;
}

.footer div {
  line-height: 1.5;
  padding-bottom: 8px;
}
</style>
