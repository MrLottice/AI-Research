<template>
  <div class="review-writing">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Promotion /></el-icon>
        <h2 class="page-title">项目评审</h2>
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

      <!-- 评审卡片列表 -->
      <div class="review-cards">
        <el-card
          v-for="review in filteredReviews"
          :key="review.id"
          class="review-card"
          @click="handleReviewSelect(review.type)"
        >
          <div class="card-header">
            <div class="app-icon">
              <el-icon :size="40" :color="review.iconColor">
                <component :is="review.icon"></component>
              </el-icon>
            </div>
            <div class="app-title">
              <h3 class="review-title">{{ review.title }}</h3>
              <el-tag
                :type="review.tagType"
                size="small"
                class="type-tag"
              >
                {{ review.label }}
              </el-tag>
            </div>
          </div>
          <div class="card-content">
            <p class="review-description">{{ review.description }}</p>
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
  Promotion,
  Document,
  Files,
  Histogram,
  Money,
  Medal,
  ArrowRight
} from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

const activeTag = ref('all');
const selectedType = ref('');
const router = useRouter();

const tags = [
  { label: '全部', value: 'all' },
  { label: '论文评审', value: 'paper' },
  { label: '项目评审', value: 'project' },
  { label: '基金评审', value: 'fund' },
  { label: '专利评审', value: 'patent' }
];

const handleTagClick = (tag: string) => {
  activeTag.value = tag;
};

const reviews = [
  {
    id: 1,
    type: 'student-paper',
    title: '论文评审',
    label: '论文评审',
    description: '针对本科生、研究生论文的专业评审，提供详细的修改建议和评分标准。',
    icon: Document,
    iconColor: '#F56C6C',
    tagType: 'danger',
    category: 'paper'
  },
  {
    id: 2,
    type: 'material',
    title: '材料评审',
    label: '材料评审',
    description: '对各类材料文档进行专业评估，提供全面的评审意见和改进建议。',
    icon: Files,
    iconColor: '#67C23A',
    tagType: 'success',
    category: 'project'
  },
  {
    id: 3,
    type: 'research-project',
    title: '科研项目评审',
    label: '项目评审',
    description: '针对科研项目的可行性、创新性、研究方法等方面进行全面评估。',
    icon: Histogram,
    iconColor: '#E6A23C',
    tagType: 'warning',
    category: 'project'
  },
  {
    id: 4,
    type: 'fund-project',
    title: '基金项目评审',
    label: '基金评审',
    description: '对基金申请项目进行专业评估，包括学术价值、研究方案等多维度分析。',
    icon: Money,
    iconColor: '#409EFF',
    tagType: 'primary',
    category: 'fund'
  },
  {
    id: 5,
    type: 'patent',
    title: '专利评审',
    label: '专利评审',
    description: '专利申请技术评估，包括创新性、实用性和产业化价值等方面的评审。',
    icon: Medal,
    iconColor: '#909399',
    tagType: 'info',
    category: 'patent'
  }
];

// 根据标签过滤评审
const filteredReviews = computed(() => {
  if (activeTag.value === 'all') {
    return reviews;
  }
  return reviews.filter(review => review.category === activeTag.value);
});

// 处理评审类型选择
const handleReviewSelect = (type: string) => {
  selectedType.value = type;
  if (type === 'fund-project') {
    router.push('/fund-project-review');
  } else {
    ElMessage.info('该评审功能正在开发中，敬请期待！');
  }
};
</script>

<style scoped>
.review-writing {
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

.review-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  padding: 0 20px;
  align-items: stretch;
  max-width: 1600px;
  margin: 0 auto;
}

.review-card {
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

.review-card::after {
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

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #eaeaea;
}

.review-card:hover::after {
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

.review-title {
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

.review-description {
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

.review-card:hover .card-footer {
  opacity: 1;
  transform: translateX(0);
}
</style>
