<script setup>
import { Marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'
import { markedHighlight } from 'marked-highlight'
import markedKatex from 'marked-katex-extension'
import 'katex/dist/katex.min.css'
import { UUID, copy } from '@/utils/util'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import 'element-plus/es/components/message/style/css'
import useTyping from '@/hooks/useTyping'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  typing: {
    type: Boolean,
    default: false
  }
})

const result = ref('')

const emits = defineEmits(['typing', 'typingStopped'])

function typingCallback() {
  render(renderedResult.value)
  emits('typing')
}

function stopTypingCallback() {
  emits('typingStopped', renderedResult.value)
}

const { typing, stopTyping, timerStopped, renderedResult } = useTyping({
  content: props.content,
  typingCallback,
  speed: 15,
  stopTypingCallback
})

function init() {
  renderedResult.value = ''
  if (props.typing) {
    timerStopped.value = false
    typing()
  } else {
    render(props.content)
  }
}

init()

function render(content) {
  const marked = new Marked({
    async: false,
    breaks: true,
    gfm: true,
    pedantic: false,
    mangle: false, // 控制台警告去除
    headerIds: false // 控制台警告去除
  })
  // 代码高亮
  marked.use(
    markedHighlight({
      async: false,
      langPrefix: 'hljs language-',
      highlight(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          const language = hljs.getLanguage(lang) ? lang : 'plaintext'
          const preCode = hljs.highlight(code, { language }).value
          // 以换行进行分割
          const lines = preCode.split(/\n/)
          if (lines.length) {
            const codeId = UUID(16)
            // 添加代码语言
            const headerDiv =
              '<div class="code-block-header">' +
              `<span class="code-block-header-lang">${lang}</span>` +
              `<span class="code-block-header-copy" onclick="handleCopy('${codeId}')">复制代码</span>` +
              `<textarea style="display:none;position: absolute;top: -9999px;left: -9999px;z-index: -9999;" id="${codeId}">${code.replace(
                /<\/textarea>/g,
                '&lt;/textarea>'
              )}</textarea>` +
              '</div>'

            const codeList = lines.map((item, index) => {
              return (
                '<li><span class="line-num" data-line="' +
                (index + 1) +
                '"></span>' +
                item +
                '</li>'
              )
            })

            // 添加自定义行号
            const lineDiv = '<ul>' + codeList.join('') + '</ul>'
            return '<div class="code-block">' + headerDiv + lineDiv + '</div>'
          }
          return ''
        }
      }
    })
  )
  // 渲染公式
  marked.use(
    markedKatex({
      throwOnError: false
    })
  )

  result.value = marked.parse(content)
}

const { t } = useI18n()

window.handleCopy = (codeId) => {
  const textarea = document.getElementById(codeId)
  copy(textarea.value)
  ElMessage.success(t('lang.copySuccess'))
}
</script>

<template>
  <div v-html="result" class="content_markdown"></div>
  <el-link v-if="!timerStopped" @click="stopTyping">{{ $t('lang.stopTyping') }}</el-link>
</template>

<style scoped lang="less">
@import './code.less';

.content_markdown {
  &::v-deep(> p) {
    margin: 0;
  }
}
</style>
