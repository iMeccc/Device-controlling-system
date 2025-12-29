<template>
  <el-container class="admin-layout">
    <el-aside width="200px">
      <el-menu :router="true" default-active="/admin/users">
        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/instruments">
          <el-icon><Monitor /></el-icon>
          <span>仪器管理</span>
        </el-menu-item>
        <!-- We will add more links here later -->
      </el-menu>
    </el-aside>
    <el-main>
      <!-- The content of child routes will be rendered here -->
      <RouterView />
    </el-main>
  </el-container>
</template>

<script setup>
// Import icons from element-plus
import { User, Monitor } from '@element-plus/icons-vue';
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}
.el-aside {
  background-color: #f4f4f5;
}
.el-menu {
  height: 100%;
}
</style>