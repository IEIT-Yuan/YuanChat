import { defineStore } from 'pinia'
import { i18n } from '@/locales'

const useAppStore = defineStore('app', () => {
  function getLanguage() {
    return localStorage.getItem('lang') || 'zh-CN'
  }

  const language = ref(getLanguage())

  function setLanguage(lang) {
    language.value = lang
    i18n.global.locale.value = lang
    localStorage.setItem('lang', lang)
  }

  const DEFAULT_MODEL_PARAMS = {
    response_length: 5000,
    temperature: 1.0,
    top_p: 1.0,
    top_k: 5
  }

  const modelParams = reactive({
    ...DEFAULT_MODEL_PARAMS
  })

  function getModelParams() {
    console.log('getModelParams')
    const _params = JSON.parse(localStorage.getItem('MODEL_PARAMS'))
    if (_params) {
      modelParams.response_length = _params?.response_length || DEFAULT_MODEL_PARAMS.response_length
      modelParams.temperature = _params?.temperature || DEFAULT_MODEL_PARAMS.temperature
      modelParams.top_p = _params?.top_p || DEFAULT_MODEL_PARAMS.top_p
      modelParams.top_k = _params?.top_k || DEFAULT_MODEL_PARAMS.top_k
    } else {
      setModelParams(DEFAULT_MODEL_PARAMS)
    }
    return modelParams
  }

  getModelParams()

  function setModelParams(params) {
    modelParams.response_length = params?.response_length
    modelParams.temperature = params?.temperature
    modelParams.top_p = params?.top_p
    modelParams.top_k = params?.top_k
    localStorage.setItem('MODEL_PARAMS', JSON.stringify(params))
  }

  const DEFAULT_MAX_MULTI_TURNS = 0

  const maxMultiTurns = ref(DEFAULT_MAX_MULTI_TURNS)

  function getMaxMultiTurns() {
    const _maxMultiTurns = localStorage.getItem('MAX_MULTI_TURNS')
    if (_maxMultiTurns) {
      maxMultiTurns.value = Number(_maxMultiTurns)
    } else {
      setMaxMultiTurns(DEFAULT_MAX_MULTI_TURNS)
    }
    return maxMultiTurns
  }

  getMaxMultiTurns()

  function setMaxMultiTurns(value) {
    maxMultiTurns.value = value
    localStorage.setItem('MAX_MULTI_TURNS', JSON.stringify(value))
  }

  return {
    language,
    getLanguage,
    setLanguage,
    modelParams,
    getModelParams,
    setModelParams,
    maxMultiTurns,
    getMaxMultiTurns,
    setMaxMultiTurns
  }
})

export default useAppStore
