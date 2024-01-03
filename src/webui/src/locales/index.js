import { createI18n } from 'vue-i18n'
import zhCN from './lang/zh-CN'
import en from './lang/en'

const messages = {
  'zh-CN': {
    lang: zhCN
  },
  en: {
    lang: en
  }
}

export const defaultLang = localStorage.getItem('lang') || 'zh-CN'

export const i18n = createI18n({
  locale: defaultLang,
  legacy: false,
  globalInjection: true,
  fallbackLocale: 'zh-CN',
  messages
})

export function i18nRender(key) {
  return i18n.global.t(`${key}`)
}
