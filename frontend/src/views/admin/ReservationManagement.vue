<template>
  <div>
    <h1>预约总览与管理</h1>
    <el-card>
      <div class="filter-container">
        <el-select
          v-model="filters.user_id"
          placeholder="输入姓名或邮箱搜索用户"
          clearable
          filterable
          remote
          :remote-method="searchUsers"
          :loading="loading.users"
          @change="handleFilterChange"
        >
          <el-option 
            v-for="user in userListForFilter" 
            :key="user.id" 
            :label="`${user.full_name} (${user.email})`" 
            :value="user.id" 
          />
        </el-select>
        
        <el-select v-model="filters.instrument_id" placeholder="按仪器筛选" clearable @change="handleFilterChange">
          <el-option v-for="inst in instrumentList" :key="inst.id" :label="inst.name" :value="inst.id" />
        </el-select>
      </div>

      <el-table :data="allReservations" style="width: 100%" v-loading="loading.reservations">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="user.full_name" label="预约人" />
        <el-table-column prop="instrument.name" label="仪器名称" />
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
              @click="handleForceCancel(scope.row)"
              :disabled="!canBeCancelled(scope.row)"
            >
              强制取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- Pagination Component -->
      <el-pagination
        background layout="prev, pager, next, total"
        :total="totalReservations" :page-size="pageSize"
        @current-change="handlePageChange"
        style="margin-top: 20px; justify-content: flex-end;"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getAllReservations, cancelReservation, getUsers, getInstruments } from '@/services/api';

const allReservations = ref([]);
const loading = reactive({ users: false, instruments: true, reservations: true });
const userListForFilter = ref([]);
const instrumentList = ref([]);
const filters = reactive({ user_id: null, instrument_id: null });
const currentPage = ref(1);
const pageSize = ref(10);
const totalReservations = ref(0);

onMounted(async () => {
  // --- CRUCIAL FIX: Access reactive properties directly ---
  loading.instruments = true;
  try {
    instrumentList.value = await getInstruments();
  } catch (error) {
    ElMessage.error('获取仪器筛选选项失败。');
  } finally {
    loading.instruments = false;
  }
  await fetchData();
});

const searchUsers = async (query) => {
  if (query) {
    loading.users = true;
    try {
      userListForFilter.value = await getUsers({ search: query, limit: 50 });
    } finally {
      loading.users = false;
    }
  } else {
    userListForFilter.value = [];
  }
};

const fetchData = async () => {
  loading.reservations = true;
  try {
    const params = {
      user_id: filters.user_id || null,
      instrument_id: filters.instrument_id || null,
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
    };
    const response = await getAllReservations(params);
    allReservations.value = response.data;
    totalReservations.value = response.total;
  } catch (error) {
    ElMessage.error('获取预约列表失败。');
  } finally {
    loading.reservations = false;
  }
};

const handleFilterChange = () => {
  currentPage.value = 1;
  fetchData();
};

const handlePageChange = (page) => {
  currentPage.value = page;
  fetchData();
};

const handleForceCancel = async (reservation) => {
  try {
    await ElMessageBox.confirm(
      `确定要强制取消用户 "${reservation.user.full_name}" 的这条预约吗？`,
      '确认操作',
      { type: 'warning' }
    );
    
    await cancelReservation(reservation.id);
    ElMessage.success('预约已强制取消！');
    await fetchData();
    
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '操作失败。');
    }
  }
};

const canBeCancelled = (reservation) => {
  return new Date(reservation.start_time) > new Date() && reservation.status === 'confirmed';
};

const formatDateTime = (isoString) => {
  if (!isoString) return '';
  return new Date(isoString).toLocaleString('zh-CN', { dateStyle: 'short', timeStyle: 'short' });
};
</script>

<style scoped>
.filter-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
</style>