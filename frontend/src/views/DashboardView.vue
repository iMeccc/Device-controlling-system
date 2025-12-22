<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>仪器预约主控台</h1>
      <div>
        <el-button @click="goToMyReservations">我的预约</el-button>
        <el-button type="danger" @click="handleLogout">登出</el-button>
      </div>
    </header>
    
    <main class="dashboard-content">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>可用仪器列表</span>
          </div>
        </template>
        
        <el-table :data="instruments" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="仪器名称" />
          <el-table-column prop="model" label="型号" />
          <el-table-column prop="location" label="位置" />
          <el-table-column prop="status" label="当前状态" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="handleView(scope.row)">查看/预约</el-button>
            </template>
          </el-table-column>
        </el-table>

      </el-card>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import router from '@/router';
import { getInstruments } from '@/services/api';

const instruments = ref([]);
const loading = ref(true); // A ref to control the loading animation

// This function will run automatically when the component is mounted (loaded)
onMounted(async () => {
  try {
    const data = await getInstruments();
    instruments.value = data;
  } catch (error) {
    console.error('Failed to fetch instruments:', error);
    ElMessage.error('获取仪器列表失败，请稍后重试。');
  } finally {
    loading.value = false; // Hide loading animation regardless of success or failure
  }
});

const handleLogout = () => {
  localStorage.removeItem('access_token');
  router.push('/login');
};

const handleView = (instrument) => {
  // Use the router to navigate to the instrument's detail page
  router.push(`/instrument/${instrument.id}`);
};

const goToMyReservations = () => {
  router.push('/my-reservations');
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
  margin-bottom: 20px;
}
.card-header {
  font-weight: bold;
}
</style>