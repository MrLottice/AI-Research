<template>
  <div class="journal-submission-container">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Promotion /></el-icon>
        <h2 class="page-title">期刊投稿</h2>
        <span class="version">v1.0.0</span>
      </div>
      <div class="header-right">
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 期刊分类标签 -->
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

      <!-- 期刊卡片列表 -->
      <div class="journal-cards">
        <el-card
          v-for="journal in filteredJournals"
          :key="journal.id"
          class="journal-card"
          @click="openJournal(journal)"
        >
          <div class="card-header">
            <div class="app-icon">
              <el-icon :size="40" :color="getIconColor(journal.category)">
                <component :is="getJournalIcon(journal.category)"></component>
              </el-icon>
            </div>
            <div class="app-title">
              <h3 class="journal-title">{{ journal.title }}</h3>
              <el-tag
                :type="getImpactFactorType(journal.impactFactor)"
                size="small"
                class="impact-factor"
              >
                IF: {{ journal.impactFactor }}
              </el-tag>
            </div>
          </div>
          <div class="card-content">
             <p class="journal-description">{{ journal.description }}</p>
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
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { 
  Promotion,
  Document,
  Tools,
  FirstAidKit,
  ArrowRight
} from '@element-plus/icons-vue';

interface Journal {
  id: number;
  title: string;
  impactFactor: number;
  description: string;
  category: string;
}

export default defineComponent({
  name: 'JournalSubmission',
  components: {
    Promotion,
    Document,
    Tools,
    FirstAidKit,
    ArrowRight
  },
  setup() {
    const activeTag = ref('all');
    const router = useRouter();
    
    const tags = [
      { label: '全部', value: 'all' },
      { label: 'Nature', value: 'Nature' },
      { label: 'Science', value: 'Science' },
      { label: 'Cell', value: 'Cell' },
      { label: '医学', value: 'Medicine' }
    ];
    
    const handleTagClick = (tag: string) => {
      activeTag.value = tag;
    };
    
    const journals = ref<Journal[]>([
      {
        id: 1,
        title: 'Nature Genetics',
        impactFactor: 41.307,
        description: '发表遗传学和基因组学领域的重要原创研究',
        category: 'Nature'
      },
      {
        id: 2,
        title: 'Nature Communications',
        impactFactor: 16.6,
        description: '发表自然科学各个领域的高质量研究',
        category: 'Nature'
      },
      {
        id: 3,
        title: 'Science',
        impactFactor: 56.9,
        description: '发表所有科学领域的重要研究成果',
        category: 'Science'
      },
      {
        id: 4,
        title: 'Cell',
        impactFactor: 64.5,
        description: '发表生命科学领域的重要发现',
        category: 'Cell'
      },
      {
        id: 5,
        title: 'The Lancet',
        impactFactor: 79.321,
        description: '发表医学领域的重要研究成果',
        category: 'Medicine'
      },
      {
        id: 6,
        title: 'Nature Medicine',
        impactFactor: 87.241,
        description: '发表医学研究领域的重要发现',
        category: 'Medicine'
      }
    ]);
    
    // 根据标签过滤期刊
    const filteredJournals = computed(() => {
      if (activeTag.value === 'all') {
        return journals.value;
      }
      return journals.value.filter(journal => journal.category === activeTag.value);
    });
    
    const openJournal = (journal: Journal) => {
      console.log('Opening journal:', journal.title);
      if (journal.title === 'Nature Genetics') {
        router.push('/nature-genetics-submission');
      } else if (journal.title === 'Nature Communications') {
        router.push('/nature-communications-submission');
      } else {
        ElMessage.info('该期刊的投稿指南正在开发中，敬请期待！');
      }
    };
    
    const getImpactFactorType = (impactFactor: number) => {
      if (impactFactor >= 20) return 'danger';
      if (impactFactor >= 10) return 'warning';
      return 'success';
    };

    const getJournalIcon = (category: string) => {
      switch (category) {
        case 'Nature':
          return Document;
        case 'Science':
          return Tools;
        case 'Cell':
          return Document;
        case 'Medicine':
          return FirstAidKit;
        default:
          return Document;
      }
    };

    const getIconColor = (category: string) => {
      switch (category) {
        case 'Nature':
          return '#F56C6C'; // 红色
        case 'Science':
          return '#67C23A'; // 绿色
        case 'Cell':
          return '#E6A23C'; // 黄色
        case 'Medicine':
          return '#409EFF'; // 蓝色
        default:
          return '#909399'; // 灰色
      }
    };
    
    return {
      activeTag,
      tags,
      journals,
      filteredJournals,
      openJournal,
      getImpactFactorType,
      handleTagClick,
      getJournalIcon,
      getIconColor
    };
  }
});
</script>

<style scoped>
.journal-submission-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100%;
  background: #f9f9f9;
  padding: 0;
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
  max-width: 98%;
  width: 100%;
  margin-left: auto;
  margin-right: auto;

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
  flex: 1;
  padding: 30px;
  overflow-y: auto;
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

.category-tag.el-tag--primary,
.category-tag.primary,
.category-tag.selected {
  background: linear-gradient(90deg, #409EFF 60%, #67C23A 100%);
  color: #fff;
  border-color: #409EFF;
  box-shadow: 0 4px 16px rgba(64,158,255,0.18);
}

.journal-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  padding: 0 20px;
  align-items: stretch;
}

.journal-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  min-height: 230px;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.journal-card::after {
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

.journal-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #eaeaea;
}

.journal-card:hover::after {
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

.journal-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.impact-factor {
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

.journal-description {
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

.journal-card:hover .card-footer {
  opacity: 1;
  transform: translateX(0);
}

/* 自定义滚动条样式 */
.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb {
  background: #409EFF;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #337ecc;
}
</style> 