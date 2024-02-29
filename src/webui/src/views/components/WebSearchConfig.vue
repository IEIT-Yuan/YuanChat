<script setup>
import useAppStore from '@/stores/app'
import { i18nRender } from '../../locales'

const app = useAppStore()

const visible = ref(false)
const form = reactive({
  accessKey: '',
  embeddingModelPath: '',
  retrieve_topk: 3,
  template: ''
})

const rules = reactive({
  accessKey: [
    {
      required: true,
      message: i18nRender('lang.noEmpty')
    }
  ],
  embeddingModelPath: [
    {
      required: true,
      message: i18nRender('lang.noEmpty')
    }
  ]
})

function initWsConfig() {
  const modelParams = app.getModelParams()
  form.accessKey = modelParams.access_key
  form.embeddingModelPath = modelParams.embeddings_model_path
  form.retrieve_topk = modelParams.retrieve_topk
  form.template = modelParams.template
}

const emits = defineEmits(['success', 'close'])

const formRef = ref(null)
function handleConfirm() {
  formRef.value.validate((valid) => {
    if (valid) {
      app.setModelParams({
        access_key: form.accessKey,
        embeddings_model_path: form.embeddingModelPath,
        retrieve_topk: form.retrieve_topk,
        template: form.template
      })
      visible.value = false
      emits('success')
    }
  })
}

function show() {
  visible.value = true
}

function close() {
  visible.value = false
  emits('close')
}

onMounted(() => {
  initWsConfig()
})

defineExpose({
  show
})
</script>
<template>
  <el-dialog
    :title="$t('lang.wsConfigSetting')"
    width="600px"
    v-model="visible"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    @close="close"
  >
    <el-form ref="formRef" :model="form" label-width="150px" :rules="rules" label-position="top">
      <el-form-item label="Serper API Key" prop="accessKey" required>
        <el-input v-model="form.accessKey"></el-input>
      </el-form-item>
      <el-form-item :label="$t('lang.embeddingModelPath')" prop="embeddingModelPath" required>
        <el-input v-model="form.embeddingModelPath"></el-input>
      </el-form-item>
      <el-form-item :label="$t('lang.sourceTopK')">
        <el-input-number
          controls-position="right"
          v-model="form.retrieve_topk"
          :step="1"
          :min="1"
          :max="8"
          step-strictly
        ></el-input-number>
      </el-form-item>
      <el-form-item :label="$t('lang.llmTemplate')">
        <el-input
          type="textarea"
          v-model="form.template"
          :rows="4"
          :autosize="{ minRows: 2, maxRows: 6 }"
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="handleConfirm">
        {{ $t('lang.confirm') }}
      </el-button>
      <el-button type="" @click="close">
        {{ $t('lang.cancel') }}
      </el-button>
    </template>
  </el-dialog>
</template>
<style lang=""></style>
