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
    top_k: 5,
    // Web Search params
    browser_flag: false,
    access_key: '',
    embeddings_model_path: '',
    retrieve_topk: 3,
    template:
      '说明：您是一位认真的研究者。使用提供的网络搜索结果，对给定的问题写一个全面而详细的回复。\n用语言回答：中文\n问题：'
  }

  let modelParams = reactive({
    ...DEFAULT_MODEL_PARAMS
  })

  function getModelParams() {
    const _params = JSON.parse(localStorage.getItem('MODEL_PARAMS'))
    if (_params) {
      modelParams.response_length = _params?.response_length || DEFAULT_MODEL_PARAMS.response_length
      modelParams.temperature = _params?.temperature || DEFAULT_MODEL_PARAMS.temperature
      modelParams.top_p = _params?.top_p || DEFAULT_MODEL_PARAMS.top_p
      modelParams.top_k = _params?.top_k || DEFAULT_MODEL_PARAMS.top_k
      // Web Search params
      modelParams.browser_flag = _params?.browser_flag || DEFAULT_MODEL_PARAMS.browser_flag
      modelParams.access_key = _params?.access_key || DEFAULT_MODEL_PARAMS.access_key
      modelParams.embeddings_model_path =
        _params?.embeddings_model_path || DEFAULT_MODEL_PARAMS.embeddings_model_path
      modelParams.retrieve_topk = _params?.retrieve_topk || DEFAULT_MODEL_PARAMS.retrieve_topk
      modelParams.template = _params?.template || DEFAULT_MODEL_PARAMS.template
    } else {
      setModelParams(DEFAULT_MODEL_PARAMS)
    }
    return modelParams
  }

  getModelParams()

  function setModelParams(params) {
    modelParams = reactive(Object.assign({}, modelParams, params))
    // modelParams.response_length = params?.response_length
    // modelParams.temperature = params?.temperature
    // modelParams.top_p = params?.top_p
    // modelParams.top_k = params?.top_k
    // // Web Search params
    // modelParams.browser_flag = params?.browser_flag
    // modelParams.access_key = params?.access_key
    // modelParams.embeddings_model_path = params?.embeddings_model_path
    // modelParams.retrieve_topk = params?.retrieve_topk
    // modelParams.template = params?.template
    localStorage.setItem('MODEL_PARAMS', JSON.stringify(modelParams))
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
