<template>
  <div>
    <h1>权限管理</h1>
    <el-card>
      <div class="permission-selector">
        <span class="selector-label">搜索用户:</span>
        <el-select
          v-model="selectedUserId"
          placeholder="输入姓名或邮箱进行搜索"
          filterable
          remote
          :remote-method="searchUsers"
          :loading="loading.users"
          clearable
          style="flex-grow: 1;"
        >
          <el-option
            v-for="user in userList"
            :key="user.id"
            :label="`${user.full_name} (${user.email})`"
            :value="user.id"
          />
        </el-select>
      </div>
  
      <el-divider />
  
      <div v-if="selectedUser" v-loading="loading.permissions">
        <h3>为 "{{ selectedUser.full_name }}" 授权仪器</h3>
        <el-table :data="instrumentList" v-loading="loading.instruments">
          <el-table-column prop="name" label="仪器名称" />
          <el-table-column prop="location" label="位置" />
          <el-table-column label="授权" width="100">
            <template #default="scope">
              <el-checkbox
                :model-value="hasPermission(scope.row.id)"
                @change="handlePermissionChange($event, scope.row.id)"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-empty v-else description="请先搜索并选择一个用户以管理其权限" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { getUsers, getInstruments, grantPermission, revokePermission } from '@/services/api';

const userList = ref([]);
const instrumentList = ref([]);
const selectedUserId = ref(null);
const loading = ref({ users: false, instruments: true, permissions: false });

const selectedUser = computed(() => {
  return userList.value.find(u => u.id === selectedUserId.value);
});

onMounted(async () => {
  loading.value.instruments = true;
  try {
    instrumentList.value = await getInstruments();
  } catch (error) {
    ElMessage.error('获取仪器列表失败。');
  } finally {
    loading.value.instruments = false;
  }
});

const searchUsers = async (query) => {
  if (query) {
    loading.value.users = true;
    try {
      userList.value = (await getUsers({ search: query, limit: 50 })).filter(u => u.role !== 'admin');
    } catch(e) { ElMessage.error('搜索用户失败。') } 
    finally { loading.value.users = false; }
  } else {
    userList.value = [];
  }
};

const hasPermission = (instrumentId) => {
  if (!selectedUser.value) return false;
  return selectedUser.value.authorized_instruments.some(inst => inst.id === instrumentId);
};

const handlePermissionChange = async (isChecked, instrumentId) => {
  if (!selectedUser.value) return;
  loading.value.permissions = true;
  
  const permissionData = {
    user_id: selectedUser.value.id,
    instrument_id: instrumentId,
  };

  try {
    let updatedUser;
    if (isChecked) {
      updatedUser = await grantPermission(permissionData);
      ElMessage.success('授权成功！');
    } else {
      updatedUser = await revokePermission(permissionData);
      ElMessage.success('权限已撤销！');
    }
    
    // --- CRUCIAL FIX: Manually update the user's data in the list ---
    const userIndex = userList.value.findIndex(u => u.id === selectedUserId.value);
    if (userIndex !== -1) {
      userList.value[userIndex] = updatedUser;
    }
  } catch (error) {
    ElMessage.error('操作失败。');
  } finally {
    loading.value.permissions = false;
  }
};
</script>

<style scoped>
.permission-selector {
  display: flex;
  align-items: center;
  gap: 10px; /* Add some space */
}
.selector-label {
  flex-shrink: 0; /* Prevent the label from shrinking */
}
</style>