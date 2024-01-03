<script setup>
import { Setting } from '@element-plus/icons-vue'
import useAppStore from '@/stores/app'

const app = useAppStore()

function handleLanguageChange(command) {
  app.setLanguage(command)
}

const settingVisible = ref(false)

function showSetting() {
  settingVisible.value = true
}

const form = reactive({
  ...app.modelParams
})

const maxMultiTurns = ref(0)

function initParams() {
  const _params = app.modelParams
  form.response_length = _params?.response_length
  form.temperature = _params?.temperature
  form.top_p = _params?.top_p
  form.top_k = _params?.top_k

  maxMultiTurns.value = app.maxMultiTurns
}

initParams()

function confirm() {
  settingVisible.value = false
  app.setModelParams(toRaw(form))
  app.setMaxMultiTurns(maxMultiTurns.value)
}
</script>

<template>
  <div class="top_bar_container">
    <div class="header_container">
      <a href="/">
        <div class="logo">
          <img src="/logo.png" alt="logo" />
        </div>
      </a>
    </div>
    <div>
      <span>
        <el-icon size="23" class="setting" @click="showSetting"><Setting /></el-icon>
      </span>
      <el-dropdown @command="handleLanguageChange">
        <span class="language">
          <img alt="logo" src="@/assets/language.svg" width="23" height="23" />
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="zh-CN"> 中文</el-dropdown-item>
            <el-dropdown-item command="en"> English</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <el-dialog
      v-model="settingVisible"
      :title="$t('lang.setting')"
      :close-on-click-modal="false"
      width="800px"
    >
      <el-form :model="form" label-width="140px" :inline="true">
        <el-form-item :label="$t('lang.responseLength')">
          <el-input-number
            v-model="form.response_length"
            :step="1"
            :min="0"
            :max="8000"
            step-strictly
          />
        </el-form-item>
        <el-form-item :label="$t('lang.temperature')">
          <el-input-number
            v-model="form.temperature"
            :precision="1"
            :step="0.1"
            :min="0"
            :max="1"
            step-strictly
          />
        </el-form-item>
        <el-form-item :label="$t('lang.topP')">
          <el-input-number
            v-model="form.top_p"
            :step="0.1"
            :precision="1"
            :min="0"
            :max="1"
            step-strictly
          />
        </el-form-item>
        <el-form-item :label="$t('lang.topK')">
          <el-input-number v-model="form.top_k" :step="1" :min="0" :max="10" step-strictly />
        </el-form-item>
        <el-form-item label="max-multi-turns">
          <el-input-number v-model="maxMultiTurns" :step="1" :min="0" :max="10" step-strictly />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="confirm"> {{ $t('lang.confirm') }} </el-button>
          <el-button @click="settingVisible = false"> {{ $t('lang.cancel') }} </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="less">
.top_bar_container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;

  .header_container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60px;

    .logo {
      width: 120px;
      height: 48px;

      img {
        height: 100%;
      }
    }
  }

  .setting {
    cursor: pointer;
    margin-right: 20px;
  }

  .language {
    cursor: pointer;
  }
}
</style>
