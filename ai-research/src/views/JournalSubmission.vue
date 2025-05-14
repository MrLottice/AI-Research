<template>
  <div class="journal-submission-container">
    <!-- 顶部标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <el-icon class="light-bulb"><Promotion /></el-icon>
        <h2 class="page-title">期刊投稿与撤回</h2>
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
          <div class="journal-header">
            <h3 class="journal-title">{{ journal.title }}</h3>
            <el-tag
              :type="getImpactFactorType(journal.impactFactor)"
              class="impact-factor"
            >
              IF: {{ journal.impactFactor }}
            </el-tag>
          </div>
          <p class="journal-description">{{ journal.description }}</p>
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
  VideoPlay
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
    VideoPlay
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
    
    return {
      activeTag,
      tags,
      journals,
      filteredJournals,
      openJournal,
      getImpactFactorType,
      handleTagClick
    };
  }
});
</script>

<style scoped>
.journal-submission-container {
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

.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.category-tags {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.category-tag {
  cursor: pointer;
  transition: all 0.3s;
  padding: 10px 25px;
  font-size: 16px;
}

.category-tag:hover {
  transform: translateY(-2px);
}

.journal-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 30px;
  padding: 20px;
}

.journal-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
  padding: 25px;
}

.journal-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.journal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.journal-title {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #333;
  flex: 1;
  margin-right: 15px;
}

.impact-factor {
  flex-shrink: 0;
  font-size: 16px;
  padding: 8px 15px;
}

.journal-description {
  margin: 0;
  color: #666;
  font-size: 16px;
  line-height: 1.6;
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