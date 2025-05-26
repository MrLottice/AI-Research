<template>
  <div class="fund-writing">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Money /></el-icon>
        <h2 class="page-title">国家自然科学基金</h2>
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

      <!-- 基金卡片列表 -->
      <div class="fund-cards">
        <el-card
          v-for="fund in filteredFunds"
          :key="fund.id"
          class="fund-card"
          @click="handleFundSelect(fund)"
        >
          <div class="card-header">
            <div class="app-icon">
              <el-icon :size="40" :color="fund.iconColor">
                <component :is="fund.icon"></component>
              </el-icon>
            </div>
            <div class="app-title">
              <h3 class="fund-title">{{ fund.title }}</h3>
              <el-tag
                :type="fund.tagType"
                size="small"
                class="type-tag"
              >
                {{ fund.label }}
              </el-tag>
            </div>
          </div>
          <div class="card-content">
            <p class="fund-description">{{ fund.description }}</p>
          </div>
          <div class="card-footer">
            <el-icon><arrow-right /></el-icon>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  Money,
  Document,
  Collection,
  Opportunity,
  Medal,
  ArrowRight
} from '@element-plus/icons-vue';

const activeTag = ref('all');

const tags = [
  { label: '全部', value: 'all' },
  { label: '面上项目', value: 'general' },
  { label: '青年基金', value: 'youth' },
  { label: '重点项目', value: 'key' },
  { label: '创新研究群体', value: 'group' }
];

const handleTagClick = (tag: string) => {
  activeTag.value = tag;
};

const funds = [
  {
    id: 1,
    type: 'general',
    title: '面上项目申请书',
    label: '面上项目',
    description: '国家自然科学基金面上项目申请书智能生成与修改，包括立项依据、研究内容、研究方案等。',
    icon: Document,
    iconColor: '#F56C6C',
    tagType: 'danger',
    category: 'general'
  },
  {
    id: 2,
    type: 'youth',
    title: '青年基金申请书',
    label: '青年基金',
    description: '青年科学基金项目申请书智能辅助系统，帮助青年科研人员提升申请书质量。',
    icon: Collection,
    iconColor: '#67C23A',
    tagType: 'success',
    category: 'youth'
  },
  {
    id: 3,
    type: 'key',
    title: '重点项目申请书',
    label: '重点项目',
    description: '国家自然科学基金重点项目申请书智能生成系统，突出创新性和科学价值。',
    icon: Opportunity,
    iconColor: '#E6A23C',
    tagType: 'warning',
    category: 'key'
  },
  {
    id: 4,
    type: 'group',
    title: '创新研究群体',
    label: '创新群体',
    description: '创新研究群体项目申请书智能辅助系统，突出团队优势和协同创新。',
    icon: Medal,
    iconColor: '#409EFF',
    tagType: 'primary',
    category: 'group'
  }
];

// 根据标签过滤基金项目
const filteredFunds = computed(() => {
  if (activeTag.value === 'all') {
    return funds;
  }
  return funds.filter(fund => fund.category === activeTag.value);
});

// 处理基金项目选择
const handleFundSelect = (fund: any) => {
  if (fund.type === 'general') {
    window.open('/fund-general', '_blank');
  } else if (fund.type === 'youth') {
    window.open('/fund-youth', '_blank');
  } else if (fund.type === 'key') {
    window.open('/fund-key', '_blank');
  } else if (fund.type === 'group') {
    window.open('/fund-group', '_blank');
  } else {
    ElMessage.info('该功能正在开发中，敬请期待！');
  }
};
</script>

<style scoped>
.fund-writing {
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  background-color: #f5f7fa;
  margin-top: -25px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: #fff;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
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

.fund-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  padding: 0 20px;
  align-items: stretch;
  max-width: 1600px;
  margin: 0 auto;
}

.fund-card {
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

.fund-card::after {
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

.fund-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #eaeaea;
}

.fund-card:hover::after {
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

.fund-title {
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

.fund-description {
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

.fund-card:hover .card-footer {
  opacity: 1;
  transform: translateX(0);
}
</style>
