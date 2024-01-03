<script setup>
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import en from 'element-plus/dist/locale/en.mjs'
import useAppStore from '@/stores/app'

const app = useAppStore()

const language = ref(app.language)

let locale = ref(language.value === 'zh-CN' ? zhCn : en)

watch(
  () => app.language,
  (newLang) => {
    locale.value = newLang === 'zh-CN' ? zhCn : en
    console.log(newLang, locale.value)
  }
)
</script>

<template>
  <el-config-provider :locale="locale">
    <RouterView />
  </el-config-provider>
</template>

<style scoped></style>
