<script setup>
import TopBar from './components/TopBar.vue'
</script>

<template>
  <el-container class="basic-layout">
    <el-header height="60px" class="basic-layout_header">
      <TopBar></TopBar>
    </el-header>
    <router-view></router-view>
  </el-container>
</template>

<style scoped lang="less">
html {
  .basic-layout {
    box-sizing: border-box;
    height: 100vh;
    background-color: @color-white-1;

    .basic-layout_header {
      background-color: @color-white;
      box-shadow: 0 5px 4px 0 rgba(136, 136, 136, 0.2);
    }
  }
}
</style>
