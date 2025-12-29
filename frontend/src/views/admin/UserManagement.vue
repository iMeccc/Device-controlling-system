<!-- File: frontend/src/views/admin/UserManagement.vue (The TRULY FINAL and Correct Version) -->
<template>
  <div>
    <div class="header">
      <h1>用户管理</h1>
      <div>
        <el-upload
          action="" 
          :show-file-list="false"
          :before-upload="handleBeforeUpload"
          style="display: inline-block; margin-right: 10px;"
        >
          <el-button type="success">批量导入 (CSV)</el-button>
        </el-upload>
        <el-button type="primary" @click="openCreateDialog">添加新用户</el-button>
      </div>
    </div>
    
    <el-table :data="users" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="full_name" label="姓名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="role" label="角色" />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <!-- NEW: Edit Button -->
          <el-button size="small" @click="openEditDialog(scope.row)">编辑</el-button>
          <el-button 
            size="small" 
            type="danger" 
            @click="handleDelete(scope.row)"
            :disabled="scope.row.role === 'admin' || scope.row.id === authState.user?.id"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>

  <!-- UNIFIED Dialog for Creating and Editing Users -->
  <el-dialog v-model="dialogVisible" :title="isEditMode ? '编辑用户' : '添加新用户'">
    <el-form :model="userForm" label-width="80px">
      <el-form-item label="姓名">
        <el-input v-model="userForm.full_name" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="userForm.email" :disabled="isEditMode" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="userForm.password" type="password" :placeholder="isEditMode ? '留空则不修改密码' : ''" />
      </el-form-item>
      <el-form-item label="角色">
        <el-select v-model="userForm.role" placeholder="请选择角色">
          <el-option label="学生" value="student" />
          <el-option label="教师" value="teacher" />
          <el-option label="管理员" value="admin" />
        </el-select>
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
import Papa from 'papaparse';
// --- CRUCIAL: 'updateUser' is now imported ---
import { getUsers, createUser, deleteUser, bulkCreateUsers, updateUser } from '@/services/api';
import { authState } from '@/store/auth';

const users = ref([]);
const loading = ref(true);
const dialogVisible = ref(false);
const isEditMode = ref(false); // New state to track dialog mode

// --- CRUCIAL: Unified form for both create and edit ---
const userForm = reactive({
  id: null,
  full_name: '',
  email: '',
  password: '',
  role: 'student',
});

onMounted(async () => {
  await fetchData();
});

const fetchData = async () => {
  loading.value = true;
  try {
    users.value = await getUsers();
  } catch (error) {
    ElMessage.error('获取用户列表失败。');
  } finally {
    loading.value = false;
  }
};

const openCreateDialog = () => {
  isEditMode.value = false;
  // Reset form to default create state
  Object.assign(userForm, {
    id: null, full_name: '', email: '', password: '', role: 'student'
  });
  dialogVisible.value = true;
};

// --- NEW: Function to open the dialog in edit mode ---
const openEditDialog = (user) => {
  isEditMode.value = true;
  // Populate form with existing user data
  Object.assign(userForm, {
    id: user.id,
    full_name: user.full_name,
    email: user.email,
    password: '', // Clear password for security
    role: user.role,
  });
  dialogVisible.value = true;
};

// --- NEW: Unified submit handler for both create and edit ---
const handleSubmit = async () => {
  if (isEditMode.value) {
    // --- UPDATE LOGIC ---
    const updateData = {
      full_name: userForm.full_name,
      role: userForm.role,
    };
    // Only include the password if the user has entered a new one
    if (userForm.password) {
      updateData.password = userForm.password;
    }
    
    try {
      await updateUser(userForm.email, updateData);
      ElMessage.success('用户信息更新成功！');
      dialogVisible.value = false;
      await fetchData();
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '更新失败。');
    }
  } else {
    // --- CREATE LOGIC (from your old handleCreateUser) ---
    try {
      await createUser(userForm);
      ElMessage.success('用户创建成功！');
      dialogVisible.value = false;
      await fetchData();
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '创建用户失败。');
    }
  }
};

const handleDelete = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.full_name}" (${user.email}) 吗？`,
      '确认删除',
      { type: 'warning' }
    );
    
    await deleteUser(user.email);
    ElMessage.success('用户删除成功！');
    await fetchData();
    
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败。');
    }
  }
};

const handleBeforeUpload = (file) => {
  if (!file.type.includes('csv')) {
    ElMessage.error('仅支持上传 CSV 格式的文件！');
    return false;
  }

  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: async (results) => {
      const usersToCreate = results.data.map(row => ({
        email: row.email,
        full_name: row.full_name,
        password: row.password,
        role: row.role || 'student',
      }));
      
      if (usersToCreate.length === 0) {
        ElMessage.warning('CSV 文件为空或格式不正确。');
        return;
      }

      try {
        await bulkCreateUsers({ users: usersToCreate });
        ElMessage.success(`成功导入 ${usersToCreate.length} 个用户！`);
        await fetchData();
      } catch (error) {
        ElMessage.error('批量导入失败，请检查文件内容或联系管理员。');
      }
    },
    error: (error) => {
      ElMessage.error('文件解析失败: ' + error.message);
    }
  });

  return false;
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