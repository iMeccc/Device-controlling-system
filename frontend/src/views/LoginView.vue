<template>
  <div class="login-container">
    <h1>大型仪器共享管理系统</h1>
    <el-form class="login-form">
      <el-form-item label="邮箱地址">
        <el-input v-model="email" placeholder="请输入您的邮箱"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="password" type="password" placeholder="请输入您的密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>


<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus'; // Import message component
import { login } from '@/services/api'; // Import our login function
import router from '@/router'; // Import the router

const email = ref('');
const password = ref('');

const handleLogin = async () => {
  if (!email.value || !password.value) {
    ElMessage.error('邮箱和密码不能为空！');
    return;
  }

  try {
    const data = await login(email.value, password.value);
    console.log('Login successful:', data);
    
    // Store the access token for future use
    localStorage.setItem('access_token', data.access_token);
    
    ElMessage.success('登录成功！即将跳转...');
    
    // Redirect to the dashboard page after a short delay
    setTimeout(() => {
      // We will create the '/dashboard' route in the next step
      // For now, let's just log it
      console.log("Redirecting to dashboard...");
      router.push('/dashboard'); 
    }, 1000);

  } catch (error) {
    console.error('Login failed:', error.response?.data?.detail || '服务器错误');
    ElMessage.error(error.response?.data?.detail || '登录失败，请检查您的凭据。');
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.login-form {
  margin-top: 20px;
}
</style>