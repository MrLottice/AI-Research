<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    
    <el-card class="demo-card">
      <h2>你好</h2>
      <el-button type="primary" @click="showMessage">点击我</el-button>
    </el-card>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';

@Options({
  props: {
    msg: String
  }
})
export default class HelloWorld extends Vue {
  msg!: string;
  
  showMessage() {
    console.log('按钮点击');
    this.$message.success('你好，Element Plus!');
  }
}
</script>

<style scoped>
.hello {
  padding: 20px;
}
.demo-card {
  margin-top: 20px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}
</style>
