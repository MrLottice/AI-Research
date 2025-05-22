<template>
  <div class="review-writing">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Promotion /></el-icon>
        <h2 class="page-title">综述撰写</h2>
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

      <!-- 综述卡片列表 -->
      <div class="review-cards">
        <el-card
          v-for="review in filteredReviews"
          :key="review.id"
          class="review-card"
          @click="openReview(review)"
        >
          <div class="card-header">
            <div class="app-icon">
               <el-icon :size="40" :color="getIconColor(review.category)">
                 <component :is="getReviewIcon(review.category)"></component>
               </el-icon>
            </div>
            <div class="app-title">
              <h3 class="review-title">{{ review.title }}</h3>
              <el-tag
                :type="getTypeTag(review.type)"
                size="small"
                class="type-tag"
              >
                {{ review.type }}
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
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Promotion, Document, Files, Opportunity, ArrowRight, Cpu } from '@element-plus/icons-vue';

interface Review {
  id: number;
  title: string;
  type: string;
  description: string;
  category: string;
}

const activeTag = ref('all');
const router = useRouter();

const tags = [
  { label: '全部', value: 'all' },
  { label: '医学综述', value: 'medical' },
  { label: '生物综述', value: 'biology' },
  { label: '化学综述', value: 'chemistry' },
  { label: '物理综述', value: 'physics' }
];

const handleTagClick = (tag: string) => {
  activeTag.value = tag;
};

const reviews = ref<Review[]>([
  {
    id: 1,
    title: '医学研究进展综述',
    type: '医学综述',
    description: '系统总结医学领域最新研究进展，包括疾病机制、治疗方法、临床实践等方面',
    category: 'medical'
  },
  {
    id: 2,
    title: '生物技术发展综述',
    type: '生物综述',
    description: '全面回顾生物技术领域的重要突破，包括基因编辑、细胞治疗、生物信息学等',
    category: 'biology'
  },
  {
    id: 3,
    title: '药物研发新进展',
    type: '医学综述',
    description: '总结药物研发领域的最新成果，包括新靶点发现、药物设计、临床试验等',
    category: 'medical'
  },
  {
    id: 4,
    title: '分子生物学前沿',
    type: '生物综述',
    description: '探讨分子生物学领域的前沿进展，包括信号通路、基因调控、蛋白质组学等',
    category: 'biology'
  },
  {
    id: 5,
    title: '材料化学新进展',
    type: '化学综述',
    description: '总结材料化学领域的最新研究成果，包括新型材料、纳米技术、能源材料等',
    category: 'chemistry'
  },
  {
    id: 6,
    title: '量子物理前沿',
    type: '物理综述',
    description: '探讨量子物理领域的前沿进展，包括量子计算、量子通信、量子传感等',
    category: 'physics'
  }
]);

// 根据标签过滤综述
const filteredReviews = computed(() => {
  if (activeTag.value === 'all') {
    return reviews.value;
  }
  return reviews.value.filter(review => review.category === activeTag.value);
});

const openReview = (review: Review) => {
  console.log('Opening review:', review.title);
  if (review.title === '分子生物学前沿') {
    router.push('/molecular-biology');
  } else {
    ElMessage.info('该综述详情页面正在开发中，敬请期待！');
  }
};

const getTypeTag = (type: string) => {
  switch (type) {
    case '医学综述':
      return 'danger';
    case '生物综述':
      return 'success';
    case '化学综述':
      return 'warning';
    case '物理综述':
      return 'info';
    default:
      return '';
  }
};

const getReviewIcon = (category: string) => {
  switch (category) {
    case 'medical':
      return Document;
    case 'biology':
      return Files;
    case 'chemistry':
      return Cpu;
    case 'physics':
      return Opportunity;
    default:
      return Document;
  }
};

const getIconColor = (category: string) => {
  switch (category) {
    case 'medical':
      return '#F56C6C'; // 红色
    case 'biology':
      return '#67C23A'; // 绿色
    case 'chemistry':
      return '#E6A23C'; // 黄色
    case 'physics':
      return '#409EFF'; // 蓝色
    default:
      return '#909399'; // 灰色
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
