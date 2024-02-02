<script setup>
import { Plus } from '@element-plus/icons-vue'
import useAppStore from '@/stores/app'

const app = useAppStore()

const props = defineProps({
  conversations: {
    type: Array,
    default: () => []
  },
  currentConversationId: {
    type: [Number, String],
    default: undefined
  }
})

const emits = defineEmits([
  'createConversation',
  'changeConversation',
  'deleteConversation',
  'editConversationName'
])

function createConversation() {
  console.log('createConversation')
  emits('createConversation')
}

function changeConversation(id) {
  if (id === props.currentConversationId) return
  clearEditStatus()
  emits('changeConversation', id)
}

const editingConvId = ref('')
const editingName = ref('')

function clearEditStatus() {
  editingConvId.value = ''
  editingName.value = ''
}

function editConversationName(conv) {
  editingName.value = conv.name
  editingConvId.value = conv.id
}

function confirmChange(conv) {
  const { id } = conv
  emits('editConversationName', id, editingName.value)
  clearEditStatus()
}

function cancelChange() {
  clearEditStatus()
}

function deleteConversation(conv) {
  console.log(conv.id)
  const { id } = conv
  emits('deleteConversation', id)
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

const settingFlag = ref(false)

const language = ref(app.getLanguage())

function changeLang() {
  app.setLanguage(language.value)
}

function confirmParams() {
  app.setModelParams(toRaw(form))
  app.setMaxMultiTurns(maxMultiTurns.value)
}
</script>

<template>
  <div class="side-bar_container">
    <div class="logo">
      <a href="/">
        <img src="/logo.png" alt="logo" />
      </a>
    </div>

    <el-button class="new-conversation_btn" v-wave :icon="Plus" @click="createConversation">
      {{ $t('lang.newChat') }}
    </el-button>
    <div class="conversation-list_container">
      <div
        v-for="conv in conversations"
        :key="conv.id"
        class="conversation-item_container"
        :class="{ active: currentConversationId === conv.id }"
        @click="changeConversation(conv.id)"
        :title="conv.name"
      >
        <template v-if="editingConvId !== conv.id">
          <el-icon><IEpChatDotSquare /></el-icon>
          <span class="name">{{ conv.name }}</span>
          <span class="option" v-if="currentConversationId === conv.id">
            <IEpEdit class="option-btn" @click.stop="editConversationName(conv)" />
            <el-popconfirm
              :title="$t('lang.deleteConversationConfirm')"
              @confirm="deleteConversation(conv)"
              width="200"
            >
              <template #reference>
                <IEpDelete class="option-btn" />
              </template>
            </el-popconfirm>
          </span>
        </template>
        <template v-else>
          <el-input class="input_name name" v-model="editingName"></el-input>
          <div class="input_option option">
            <IEpCheck class="input_option-btn option-btn" @click="confirmChange(conv)" />
            <IEpClose class="input_option-btn option-btn" @click="cancelChange" />
          </div>
        </template>
      </div>
    </div>

    <div class="setting-container" :class="{ open: settingFlag }">
      <div class="setting-form-container" v-show="settingFlag">
        <el-form :model="form" label-position="top" class="setting-form">
          <el-form-item :label="$t('lang.responseLength')">
            <el-input-number
              @change="confirmParams"
              controls-position="right"
              v-model="form.response_length"
              :step="1"
              :min="0"
              :max="8000"
              step-strictly
              class="form-input"
            />
          </el-form-item>
          <el-form-item :label="$t('lang.temperature')">
            <el-input-number
              @change="confirmParams"
              controls-position="right"
              v-model="form.temperature"
              :precision="1"
              :step="0.1"
              :min="0"
              :max="1"
              step-strictly
              class="form-input"
            />
          </el-form-item>
          <el-form-item :label="$t('lang.topP')">
            <el-input-number
              @change="confirmParams"
              controls-position="right"
              v-model="form.top_p"
              :step="0.1"
              :precision="1"
              :min="0"
              :max="1"
              step-strictly
              class="form-input"
            />
          </el-form-item>
          <el-form-item :label="$t('lang.topK')">
            <el-input-number
              @change="confirmParams"
              controls-position="right"
              v-model="form.top_k"
              :step="1"
              :min="0"
              :max="10"
              step-strictly
              class="form-input"
            />
          </el-form-item>
          <el-form-item :label="$t('lang.max-multi-turns')">
            <el-input-number
              @change="confirmParams"
              controls-position="right"
              v-model="maxMultiTurns"
              :step="1"
              :min="0"
              :max="10"
              step-strictly
              class="form-input"
            />
          </el-form-item>
          <el-form-item :label="$t('lang.language')">
            <el-select v-model="language" class="form-input" @change="changeLang">
              <el-option label="中文" value="zh-CN"></el-option>
              <el-option label="English" value="en"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <el-text class="setting" @click="settingFlag = !settingFlag">
        <div style="display: flex; align-items: center">
          <el-icon size="16"><IEpSetting /></el-icon>
          <span>{{ $t('lang.setting') }}</span>
        </div>
        <el-icon size="16">
          <IEpArrowRight v-if="!settingFlag" />
          <IEpArrowUp v-else />
        </el-icon>
      </el-text>
    </div>
  </div>
</template>

<style scoped lang="scss">
.side-bar_container {
  background-color: $color-black-2;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  padding: 0 10px;

  .logo {
    margin-top: 20px;
    width: 120px;
    height: 48px;

    img {
      height: 100%;
    }
  }

  .new-conversation_btn {
    margin-top: 30px;
    margin-bottom: 24px;
    text-align: center;
    width: 175px;
    height: 40px;
    font-size: 18px;
    color: $color-white-2;
    background-color: $color-blue-1;
    border-radius: 20px;
    border: none;
    padding: 10px;

    &:hover {
      background: $color-blue-2;
    }
  }

  .conversation-list_container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-height: calc(100% - 200px);
    overflow-y: auto;

    &::-webkit-scrollbar {
      width: 0;
    }

    .conversation-item_container {
      color: $color-white-2;
      width: 100%;
      height: 40px;
      min-height: 40px;
      display: flex;
      justify-content: space-between;
      flex-direction: row;
      align-items: center;
      font-size: 14px;
      margin-bottom: 5px;
      cursor: pointer;
      transition:
        border-color 0.3s,
        background-color 0.3s,
        color 0.3s;
      box-sizing: border-box;
      border-radius: 10px;

      line-height: 2.5;
      padding: 0 20px;
      position: relative;
      white-space: nowrap;

      .name {
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        display: inline-block;
        flex: 1;
        margin-left: 10px;
      }

      .option {
        display: flex;
        align-items: center;
        width: 50px;
        flex-shrink: 0;

        .option-btn {
          margin-left: 6px;
        }
      }

      .input_name {
        &::v-deep(.el-input__wrapper) {
          background-color: $color-blue-2;
          padding: 0;
          font-size: 14px;
          box-shadow: none;

          .el-input__inner {
            border: 0;
            color: $color-white-2;
            border-radius: 0;
            outline: none;
          }
        }
      }

      &.active {
        background: $color-blue-2;
      }

      &:hover {
        background: $color-blue-2;
      }
    }
  }

  .setting-container {
    position: fixed;
    bottom: 0;
    width: 280px;
    height: 40px;
    background-color: $color-black-2;
    border-top: 1px solid $color-blue-2;
    transition: height 0.3s ease;
    will-change: height;

    &.open {
      height: 540px;
    }
    .setting {
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      color: $color-white-2;
      line-height: 40px;
      padding: 0 30px;

      &:hover {
        background-color: $color-blue-2;
      }
      span {
        margin-left: 10px;
      }
    }

    .setting-form-container {
      width: 100%;
      margin-top: 20px;
      .setting-form {
        padding: 0 20px;
        ::v-deep(.el-form-item__label) {
          color: $color-white-2;
        }
        .form-input {
          width: 220px;

          ::v-deep(.el-input-number__decrease),
          ::v-deep(.el-input-number__increase) {
            border-color: #25a4d4;
            background: #25a4d4;
            color: white;
            &:hover {
              background: #1b81b6;
              border-color: #1b81b6;
            }
          }
          ::v-deep(.el-input__wrapper) {
            background-color: $color-blue-2;
            box-shadow: 0 0 0 1px $color-blue-1;
            .el-input__inner {
              color: $color-white-2;
            }
          }

          ::v-deep(.el-select__wrapper) {
            background-color: $color-blue-2;
            box-shadow: 0 0 0 1px $color-blue-1;
            .el-select__selected-item {
              color: $color-white-2;
            }
          }
        }
      }
    }
  }
}
</style>
