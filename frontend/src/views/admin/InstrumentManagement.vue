<template>
  <div>
    <div class="header">
      <h1>仪器管理</h1>
      <el-button type="primary" @click="openCreateDialog">添加新仪器</el-button>
    </div>
    
    <el-table :data="instruments" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="仪器名称" />
      <el-table-column prop="model" label="型号" />
      <el-table-column prop="location" label="位置" />
      <el-table-column label="状态" width="120">
        <template #default="scope">
          <el-switch
            v-model="scope.row.status"
            active-value="available"
            inactive-value="maintenance"
            @change="handleStatusChange(scope.row)"
          />
          <span style="margin-left: 8px">{{ scope.row.status === 'available' ? '可用' : '维修中' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="openEditDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>

  <!-- Edit/Create Instrument Dialog -->
  <el-dialog v-model="dialogVisible" :title="isEditMode ? '编辑仪器' : '添加新仪器'">
    <el-form :model="instrumentForm" label-width="100px">
      <el-form-item label="仪器名称">
        <el-input v-model="instrumentForm.name" />
      </el-form-item>
      <el-form-item label="型号">
        <el-input v-model="instrumentForm.model" />
      </el-form-item>
      <el-form-item label="位置">
        <el-input v-model="instrumentForm.location" />
      </el-form-item>
       <el-form-item label="IP 地址">
        <el-input v-model="instrumentForm.ip_address" />
      </el-form-item>
       <el-form-item label="MAC 地址">
        <el-input v-model="instrumentForm.mac_address" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="instrumentForm.description" type="textarea" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit">
        {{ isEditMode ? '保存' : '创建' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getInstruments, createInstrument, updateInstrument, deleteInstrument } from '@/services/api';

const instruments = ref([]);
const loading = ref(true);
const dialogVisible = ref(false);
const isEditMode = ref(false);

const instrumentForm = reactive({
  id: null, name: '', model: '', location: '', description: '', ip_address: '', mac_address: ''
});

onMounted(async () => {
  await fetchData();
});

const fetchData = async () => {
  loading.value = true;
  try {
    instruments.value = await getInstruments();
  } catch (error) {
    ElMessage.error('获取仪器列表失败。');
  } finally {
    loading.value = false;
  }
};

const openCreateDialog = () => {
  isEditMode.value = false;
  Object.assign(instrumentForm, { id: null, name: '', model: '', location: '', description: '', ip_address: '', mac_address: '' });
  dialogVisible.value = true;
};

const openEditDialog = (instrument) => {
  isEditMode.value = true;
  Object.assign(instrumentForm, { ...instrument });
  dialogVisible.value = true;
};

const handleSubmit = async () => {
  try {
    if (isEditMode.value) {
      await updateInstrument(instrumentForm.id, instrumentForm);
      ElMessage.success('仪器更新成功！');
    } else {
      await createInstrument(instrumentForm);
      ElMessage.success('仪器创建成功！');
    }
    dialogVisible.value = false;
    await fetchData();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败。');
  }
};

const handleDelete = async (instrument) => {
  try {
    await ElMessageBox.confirm(`确定要删除仪器 "${instrument.name}" 吗？`, '确认删除', { type: 'warning' });
    await deleteInstrument(instrument.id);
    ElMessage.success('仪器删除成功！');
    await fetchData();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败。');
    }
  }
};

const handleStatusChange = async (instrument) => {
  try {
    await updateInstrument(instrument.id, { status: instrument.status });
    ElMessage.success(`仪器 "${instrument.name}" 状态已更新！`);
  } catch (error) {
    ElMessage.error('状态更新失败。');
    // Revert the switch state on failure
    instrument.status = instrument.status === 'available' ? 'maintenance' : 'available';
  }
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>