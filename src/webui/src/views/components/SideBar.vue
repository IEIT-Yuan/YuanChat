<script setup>
import { Plus } from '@element-plus/icons-vue'

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

const emits = defineEmits(['createConversation', 'changeConversation', 'deleteConversation'])

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
</script>

<template>
  <div class="side-bar_container">
    <el-button class="new-conversation_btn" :icon="Plus" @click="createConversation">
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
  </div>
</template>

<style scoped lang="less">
.side-bar_container {
  background-color: @color-blue-5;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  padding: 0 10px;

  .new-conversation_btn {
    margin-top: 30px;
    margin-bottom: 24px;
    text-align: center;
    width: 175px;
    height: 40px;
    font-size: 20px;
    background: none;
    color: @color-white;
    border-radius: 20px;
    border: solid 2px @color-white;
    padding: 10px;

    &:hover {
      background-color: @color-blue-3;
    }
  }

  .conversation-list_container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 24px;
    background-color: rgba(255, 255, 255, 0.43);
    box-sizing: border-box;
    padding: 10px;
    min-height: 400px;
    max-height: calc(100% - 120px);
    overflow-y: auto;

    &::-webkit-scrollbar {
      width: 0;
    }

    .conversation-item_container {
      color: @color-white;
      width: 100%;
      height: 40px;
      min-height: 40px;
      display: flex;
      justify-content: space-between;
      flex-direction: row;
      align-items: center;
      font-size: 16px;
      margin-bottom: 10px;
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
          background-color: @color-blue-4;
          padding: 0;
          font-size: 16px;
          box-shadow: none;

          .el-input__inner {
            border: 0;
            color: @color-white;
            border-radius: 0;
            outline: none;
          }
        }
      }

      &.active {
        background: @color-blue-4;
      }

      &:hover {
        background: @color-blue-4;
      }
    }
  }
}
</style>
