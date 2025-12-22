<template>
  <div class="my-reservations-container">
    <el-page-header @back="goBack" content="我的预约" />
    <el-divider />

    <el-card class="box-card">
      <el-table :data="myReservations" style="width: 100%" v-loading="loading">
        <el-table-column prop="instrument.name" label="仪器名称" />
        <el-table-column prop="instrument.location" label="位置" />
        <el-table-column label="预约时间">
          <template #default="scope">
            <span>{{ formatDateTime(scope.row.start_time) }} - {{ formatDateTime(scope.row.end_time) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button 
              size="small" 
              type="danger" 
              @click="handleCancel(scope.row)"
              :disabled="!canBeCancelled(scope.row)"
            >
              取消预约
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import router from '@/router';
import { getMyReservations, cancelReservation } from '@/services/api'; // We'll add these next

const myReservations = ref([]);
const loading = ref(true);

onMounted(async () => {
  await fetchData();
});

const fetchData = async () => {
  loading.value = true;
  try {
    const data = await getMyReservations();
    // Sort reservations by start time, newest first
    myReservations.value = data.sort((a, b) => new Date(b.start_time) - new Date(a.start_time));
  } catch (error) {
    console.error('Failed to fetch my reservations:', error);
    ElMessage.error('获取预约列表失败。');
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.push('/dashboard');
};

const handleCancel = async (reservation) => {
  try {
    await ElMessageBox.confirm(
      '您确定要取消这个预约吗？此操作无法撤销。',
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '手滑了',
        type: 'warning',
      }
    );
    
    await cancelReservation(reservation.id);
    ElMessage.success('预约已成功取消！');
    await fetchData(); // Refresh the list
    
  } catch (error) {
    // This catches both API errors and the user clicking 'Cancel'
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '取消失败，请重试。');
    }
  }
};

const canBeCancelled = (reservation) => {
  // Only future, confirmed reservations can be cancelled
  return new Date(reservation.start_time) > new Date() && reservation.status === 'confirmed';
};

const formatDateTime = (isoString) => {
  if (!isoString) return '';
  return new Date(isoString).toLocaleString('zh-CN', { dateStyle: 'short', timeStyle: 'short' });
};
</script>

<style scoped>
.my-reservations-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}
</style>