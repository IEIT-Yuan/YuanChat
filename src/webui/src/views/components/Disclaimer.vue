<script setup>
import { yuanChat, yuanModel } from './disclaimer'
import useAppStore from '@/stores/app'

const app = useAppStore()
const language = ref(app.getLanguage())
const visible = ref(false)
const title = ref('')
const content = ref('')

const emits = defineEmits(['close'])

function show(type) {
  visible.value = true
  if (type === 'yuanChat') {
    title.value = language.value === 'zh-CN' ? yuanChat.titleCN : yuanChat.titleEN
    content.value = language.value === 'zh-CN' ? yuanChat.cn : yuanChat.en
  } else if (type === 'yuanModel') {
    title.value = yuanModel.titleCN
    content.value = yuanModel.cn
  }
}

function close() {
  visible.value = false
  emits('close')
}
defineExpose({ show })
</script>
<template>
  <el-dialog v-model="visible" @close="close" class="disclaimer-dialog" :show-close="false">
    <div v-html="content"></div>
    <template #footer>
      <el-button type="primary" @click="close">确 定</el-button>
    </template>
  </el-dialog>
</template>
<style lang="scss">
.disclaimer-dialog {
  .el-dialog__body {
    max-height: 700px;
    overflow: auto;
    line-height: 1.5;
  }
}
</style>
