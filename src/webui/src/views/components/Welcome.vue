<script setup>
import { Refresh } from '@element-plus/icons-vue'
import { getRecommendList as service_getRecommendList } from '@/services/index'

const emits = defineEmits(['useRecommend'])

const recommendList = ref([])

function getRecommendList() {
  return service_getRecommendList().then((res) => {
    recommendList.value = res
  })
}

getRecommendList()

function useRecommend(content) {
  emits('useRecommend', content)
}
</script>

<template>
  <div class="welcome-container">
    <h2>{{ $t('lang.welcomeHeader') }}</h2>
    <p>{{ $t('lang.welcomeParagraph1') }}</p>
    <el-divider></el-divider>
    <el-row class="recommend-prompt_row">
      <span class="recommend-prompt_title">{{ $t('lang.recommend') }}</span>
      <el-link
        :underline="false"
        type="primary"
        :icon="Refresh"
        class="refresh-prompt_opt"
        @click="getRecommendList"
      >
        {{ $t('lang.refresh') }}
      </el-link>
    </el-row>
    <el-row class="recommend-prompt_row">
      <el-tag
        class="recommend-prompt-tag"
        effect="plain"
        size="large"
        type="info"
        v-for="(content, index) in recommendList"
        :key="index"
        @click="useRecommend(content)"
        round
      >
        {{ content }}
      </el-tag>
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.welcome-container {
  box-sizing: border-box;
  padding: 14px 24px;
  color: $color-black;
  background-color: $color-white;
  border-radius: 10px;
  width: 100%;
  flex: 1;
  font-size: 15px;
  line-height: 1.8;

  .recommend-prompt_row {
    margin: 10px auto;
    text-align: left;
    color: $color-black-1;
    font-size: 14px;

    .refresh-prompt_opt {
      margin-left: 10px;
      color: $color-primary;
    }

    .recommend-prompt_title {
      color: $color-black-1;
    }

    .recommend-prompt-tag {
      margin-right: 10px;
      margin-bottom: 10px;
      cursor: pointer;
      background-color: $color-grey-3;
      color: $color-black-1;
      font-size: 14px;
      white-space: pre-wrap;
      border: none;
      padding: 20px;
      border-radius: 10px;
      &:hover {
        background-color: $color-blue-2;
      }
    }
  }
}
</style>
