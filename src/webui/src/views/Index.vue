<script setup>
import SideBar from './components/SideBar.vue'
import ChatItem from './components/ChatItem.vue'
import Welcome from './components/Welcome.vue'
import Disclaimer from './components/Disclaimer.vue'
import useDatabase from '@/hooks/useDatabase'
import useSSE from '../hooks/useSSE'
import useAppStore from '@/stores/app'
import { Promotion } from '@element-plus/icons-vue'
import WebSearchConfig from './components/WebSearchConfig.vue'
import {
  getConversationList,
  getMessagesByConversionId,
  addMessage,
  updateMessage,
  addConversation,
  updateFeedback,
  deleteConversation as service_deleteConversation,
  editConversationName as service_editConversationName
} from '@/services'
import { nextTick } from 'vue'

const app = useAppStore()

const { db } = useDatabase()

const currentConversationId = ref('')

watch(
  () => currentConversationId.value,
  async () => {
    messages.value = await getMessagesByConversionId(currentConversationId.value)
    status.value = ''
    nextTick(() => {
      scrollToBottom()
    })
  }
)

// 对话列表
const conversations = ref([])

// 消息列表
const messages = ref([])

const RefChatList = ref(null)

function scrollToBottom() {
  nextTick(() => {
    RefChatList.value.scrollTop = RefChatList.value.scrollHeight
  })
}

const init = async () => {
  try {
    await db.open()

    // 初始化对话和对话内容表
    await initConversations()
    await initMessages()
  } catch (error) {
    console.error('Error initializing tables:', error)
  }
}

init()

const initConversations = async () => {
  conversations.value = await getConversationList()

  // 如果对话表为空，则创建一个示例对话
  if (conversations.value.length === 0) {
    // 将示例对话插入对话表
    await addConversation({ name: generateConversationName() })
    // 更新对话列表
    conversations.value = await getConversationList()
  }

  // 更新当前对话id为第一条对话
  currentConversationId.value = conversations.value[0].id
}

// 初始化消息表
const initMessages = async () => {
  // 查询当前对话的消息
  if (conversations.value.length > 0) {
    messages.value = await getMessagesByConversionId(currentConversationId.value)
    scrollToBottom()
  }
}

// 生成对话名称的逻辑
const generateConversationName = () => {
  return 'New Chat'
}

const modelParams = app.modelParams
const message = ref('')
const webSearchEngine = ref(modelParams.browser_flag)

function fetchResult(params) {
  return new Promise((resolve) => {
    useSSE('/sse/subscribe', {
      params: Object.assign({}, params, toRaw(app.getModelParams())),
      onmessage(ev) {
        try {
          const res = JSON.parse(ev.data)
          console.log('res', res)
          const { flag, resData } = res
          if (flag) {
            // const { message } = resData
            resolve(resData)
          }
        } catch (error) {
          console.error(error)
        }
      }
    })
  })
}

const AUTO_RENAME_LETTER_COUNT = 15

// 发送消息时自动重命名对话名称
function autoRenameConversation(id, name) {
  editConversationName(id, name)
}

// 发送消息
async function sendMessage() {
  if (!message.value) return
  // 创建message记录
  const msgItem = {
    conversation_id: currentConversationId.value,
    sender: 'USER',
    content: message.value
  }

  // 插入message
  await addMessage(msgItem)

  // 刷新messages列表
  messages.value = await getMessagesByConversionId(currentConversationId.value)

  const isFirstMessage = messages.value.length === 1
  if (isFirstMessage) {
    autoRenameConversation(
      currentConversationId.value,
      message.value.substring(0, AUTO_RENAME_LETTER_COUNT)
    )
  }

  // 清空输入框
  message.value = ''

  messages.value.push({
    isLoading: true
  })
  scrollToBottom()
  const MESSAGES_COUNT = app.maxMultiTurns || 0
  const _messages = messages.value.slice(-2 * (MESSAGES_COUNT + 1)).reduce((acc, cur) => {
    if (cur.sender) {
      if (cur.sender === 'USER') {
        acc.push({ question: cur.content, answer: '' })
      } else {
        if (acc.length) acc[acc.length - 1].answer = cur.content
      }
    }
    return acc
  }, [])
  const params = {
    messages: _messages,
    browser_flag: webSearchEngine.value
  }
  status.value = 'LOADING'
  const resData = await fetchResult(params)
  const resultMsg = resData.message
  const browser_flag = resData.browser_flag
  const sources = resData.refs || []
  const related = resData.peopleAlsoAsk || []

  // 构建result对象
  const result = {
    conversation_id: currentConversationId.value,
    sender: 'BOT',
    content: resultMsg,
    feedback: 0, // 默认无反馈
    webSearchFlag: browser_flag,
    sources: sources,
    related: related
  }
  await addMessage(result)
  messages.value = await getMessagesByConversionId(currentConversationId.value)
  scrollToBottom()
  messages.value[messages.value.length - 1].isNew = true
  status.value = ''
}

function messageUpdate() {
  scrollToBottom()
}

function typingStopped(renderedResult) {
  const id = messages.value[messages.value.length - 1].id
  updateMessage({ id, content: renderedResult })
}

async function createConversation() {
  // 检查最新一条对话是否为空 如果没有内容则拒绝新建对话
  const firstConversationId = conversations.value[0].id
  const firstConvMessages = await getMessagesByConversionId(firstConversationId)
  if (!firstConvMessages.length) return

  const newConversationId = await addConversation({ name: generateConversationName() })
  currentConversationId.value = newConversationId
  conversations.value = await getConversationList()
}

function changeConversation(id) {
  currentConversationId.value = id
}

async function deleteConversation(id) {
  await service_deleteConversation(id)
  conversations.value = await getConversationList()

  // 如果删除后没有对话
  if (conversations.value.length === 0) {
    // 将示例对话插入对话表
    await addConversation({ name: generateConversationName() })
    // 更新对话列表
    conversations.value = await getConversationList()
  }
  if (id === currentConversationId.value) {
    currentConversationId.value = conversations.value[0].id
  }
}

async function editConversationName(id, name) {
  await service_editConversationName(id, name)
  conversations.value = await getConversationList()
}

const status = ref('')

function keydown(e) {
  if (!e.shiftKey && e.keyCode === 13) {
    e.cancelBubble = true //ie阻止冒泡行为
    e.stopPropagation() //Firefox阻止冒泡行为
    e.preventDefault() //取消事件的默认动作*换行
    if ('LOADING' === status.value) return
    sendMessage()
  }
}

// 输入推荐问题
function useRecommend(content) {
  message.value = content
}

function getImageUrl(type, feedback) {
  let path = ''
  if (type === 1) {
    path = feedback === 1 ? 'icon_thumb_up_active' : 'icon_thumb_up_default'
  } else if (type === 2) {
    path = feedback === 2 ? 'icon_thumb_down_active' : 'icon_thumb_down_default'
  }
  return `${import.meta.env.BASE_URL}icons/${path}.png`
}

// 更新回馈信息
function sendFeedback(message, feedback) {
  if (message.feedback === feedback) {
    feedback = 0
  }
  updateFeedback({
    feedback,
    id: message.id
  }).then(() => {
    initMessages()
  })
}

const dislcaimerModelFlag = ref(false)
const disclainmerModelRef = ref(null)
function openDisclainmerModel(type) {
  dislcaimerModelFlag.value = true
  nextTick(() => {
    disclainmerModelRef.value.show(type)
  })
}

const wsConfigRef = ref(null)
const wsConfigFlag = ref(false)
function webSearchEngineChange() {
  if (webSearchEngine.value) {
    webSearchEngine.value = false

    app.setModelParams({
      browser_flag: webSearchEngine.value
    })
  } else {
    wsConfigFlag.value = true
    nextTick(() => {
      wsConfigRef.value.show()
    })
  }
}

function wsConfigSuccess() {
  webSearchEngine.value = true
  wsConfigFlag.value = false
  app.setModelParams({
    browser_flag: webSearchEngine.value
  })
}
</script>

<template>
  <el-container class="chat-page_wrapper">
    <el-aside width="280px">
      <SideBar
        :conversations="conversations"
        :currentConversationId="currentConversationId"
        @createConversation="createConversation"
        @changeConversation="changeConversation"
        @deleteConversation="deleteConversation"
        @editConversationName="editConversationName"
      />
    </el-aside>
    <el-main class="chat-main_wrapper">
      <div class="chat-container">
        <div class="chat-list_container" ref="RefChatList">
          <template v-if="messages.length">
            <div class="chat-item_container" v-for="msg in messages" :key="msg.id">
              <ChatItem
                :content="msg.content"
                :sender="msg.sender"
                :isLoading="msg.isLoading"
                :is-new="msg.isNew"
                :webSearchFlag="msg.webSearchFlag"
                :sourceList="msg.sources"
                :relatedList="msg.related"
                @update="messageUpdate"
                @typingStopped="typingStopped"
                @useRecommend="useRecommend"
              />
              <div class="chat-feedback" v-if="msg.sender === 'BOT'">
                <img
                  @click="sendFeedback(msg, 1)"
                  :src="getImageUrl(1, msg.feedback)"
                  class="icon"
                />
                <img
                  @click="sendFeedback(msg, 2)"
                  :src="getImageUrl(2, msg.feedback)"
                  class="icon"
                />
              </div>
            </div>
          </template>
          <template v-else>
            <Welcome @useRecommend="useRecommend" />
          </template>
        </div>
        <div class="chat-input_container">
          <el-input
            v-model="message"
            class="chat-input"
            type="textarea"
            resize="none"
            :autosize="{ minRows: 3, maxRows: 6 }"
            :placeholder="$t('lang.inputPlaceholder')"
            @keydown="keydown($event)"
          />
          <div class="chat-input-btn_container">
            <el-tooltip
              :content="webSearchEngine ? $t('lang.wsEnabled') : $t('lang.wsDisabled')"
              placement="top"
            >
              <el-button class="chat-input-btn" @click="webSearchEngineChange">
                <img v-if="webSearchEngine" src="@/assets/network.svg" class="input-icon" alt="" />
                <img v-else src="@/assets/network_disconnected.svg" class="input-icon" alt="" />
              </el-button>
            </el-tooltip>
            <el-button
              class="chat-input-btn"
              :icon="Promotion"
              @click="sendMessage"
              :disabled="!message || 'LOADING' === status"
            ></el-button>
          </div>
        </div>
        <div class="disclaimer-container">
          {{ $t('lang.disclaimer') }}
          <el-link
            type="primary"
            style="font-size: 12px"
            @click="openDisclainmerModel('yuanModel')"
          >
            《源2.0模型开源许可协议》
          </el-link>
          {{ $t('lang.and') }}
          <el-link type="primary" style="font-size: 12px" @click="openDisclainmerModel('yuanChat')">
            《YuanChat开源许可协议》
          </el-link>
          。
        </div>
      </div>
    </el-main>
  </el-container>
  <Disclaimer
    ref="disclainmerModelRef"
    v-if="dislcaimerModelFlag"
    @close="dislcaimerModelFlag = false"
  />
  <WebSearchConfig
    ref="wsConfigRef"
    v-if="wsConfigFlag"
    @close="wsConfigFlag = false"
    @success="wsConfigSuccess"
  />
</template>

<style scoped lang="scss">
.chat-page_wrapper {
  overflow: auto;
  .chat-main_wrapper {
    display: flex;
    flex-direction: column;
  }

  .chat-container {
    overflow: hidden;
    overflow-x: auto;
    position: relative;
    width: 100%;
    margin: 0 auto;
    flex: 1;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;

    .chat-list_container {
      width: 960px;
      margin: 0 auto;
      flex: 1;
      overflow-y: auto;
      padding-bottom: 24px;

      &::-webkit-scrollbar {
        width: 0;
      }

      .chat-feedback {
        display: flex;
        justify-content: flex-end;
        .icon {
          display: inline-block;
          width: 18px;
          height: 18px;
          margin-top: 5px;
          margin-right: 5px;
          cursor: pointer;
          padding: 5px;
          &:hover {
            background-color: $color-blue-2;
          }
        }
      }
    }

    .chat-input_container {
      width: 980px;
      flex-shrink: 0;
      flex-grow: 0;
      position: relative;
      margin: 0 auto;

      .chat-input {
        :deep(.el-textarea__inner) {
          border-radius: 10px;
        }
      }

      .chat-input-btn_container {
        align-items: center;
        display: flex;
        position: absolute;
        bottom: 5px;
        right: 10px;

        .chat-input-btn {
          width: 40px;
          height: 40px;
          border-radius: 10%;
          border: none;
          text-align: center;
          font-size: 24px;
          &:not(.is-disabled)::v-deep(.el-icon) {
            color: $color-primary;
          }
          &:hover {
            color: inherit;
            background-color: $color-white-4;
          }

          &.is-disabled {
            border-color: $color-white-3;
            color: $color-grey-1;
          }

          .input-icon {
            width: 24px;
            height: 24px;
          }
        }
      }
    }

    .disclaimer-container {
      font-size: 12px;
      margin-top: 10px;
    }
  }
}
</style>
