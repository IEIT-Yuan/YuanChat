<script setup>
import Loading from './Loading.vue'
import Markdown from './Markdown.vue'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  sender: {
    type: String, // USER BOT
    default: 'BOT'
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  isNew: {
    type: Boolean,
    default: false
  }
})

const emits = defineEmits(['update', 'typingStopped', 'useRecommend'])

function typing() {
  emits('update')
}

function typingStopped(renderedResult) {
  emits('typingStopped', renderedResult)
}

const isUser = computed(() => {
  return props.sender === 'USER'
})

const sourceList = ref([
  {
    title: '日历网',
    detail: '2024法定假期，调休，节假日'
  },
  {
    title: '日历网',
    detail: '2024法定假期，调休，节假日'
  },
  {
    title: '日历网',
    detail: '2024法定假期，调休，节假日'
  },
  {
    title: '日历网',
    detail: '2024法定假期，调休，节假日'
  },
  {
    title: '日历网',
    detail: '2024法定假期，调休，节假日'
  },
  {
    title: '日历网',
    detail: '2024法定假期，调休，节假日'
  }
])
const relatedList = ref([
  '规划哈沙德回复规划哈沙德回复规划哈沙德回复规划哈沙德回复规划哈沙德回复规划哈沙德回复',
  '规划哈沙德回复规划哈沙德回复规划哈沙德回复',
  '规划哈沙德回复',
  '规划哈沙德回复',
  '规划哈沙德回复规划哈沙德回复规划哈沙德回复',
  '规划哈沙德回复',
  '规划哈沙德回复'
])

function useRecommend(value) {
  emits('useRecommend', value)
}
</script>

<template>
  <div class="chat-item_container" :class="{ user: isUser }">
    <div class="avatar">
      <img v-if="isUser" src="/avatar-user.png" alt="user" />
      <img v-else src="/avatar-yuan.png" alt="yuan" />
    </div>
    <div class="content">
      <template v-if="isLoading">
        <Loading />
      </template>
      <template v-else>
        <template v-if="isUser">
          {{ content }}
        </template>
        <template v-else>
          <Markdown
            :typing="isNew"
            :content="content"
            @typing="typing"
            @typingStopped="typingStopped"
          />
          <div class="chat-item-wse">
            <div class="chat-item-wse__title">Sources</div>
            <el-row gutter="5">
              <el-col :span="6" v-for="(source, index) in sourceList" :key="index">
                <el-card shadow="hover" class="source-container">
                  <div class="source-title">
                    <span>{{ source.title }}</span>
                  </div>
                  <div class="source-detail">
                    {{ source.detail }}
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <div class="chat-item-wse">
            <div class="chat-item-wse__title">Related</div>
            <el-tag
              class="recommend-prompt-tag"
              effect="plain"
              size="large"
              type="info"
              v-for="(content, index) in relatedList"
              :key="index"
              @click="useRecommend(content)"
              round
            >
              {{ content }}
            </el-tag>
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-item_container {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 12px;

  &:not(.user) {
    background-color: $color-white;
    border-radius: 10px;
  }

  .avatar {
    width: 36px;
    height: 36px;
    flex-shrink: 0;

    img {
      width: 100%;
      height: 100%;
    }
  }

  .content {
    margin-left: 15px;
    box-sizing: border-box;
    padding: 5px 0 12px 0;
    color: $color-black;
    width: 100%;
    flex: 1;
    font-size: 15px;
    line-height: 1.8;

    .chat-item-wse {
      margin: 20px 0;
      .chat-item-wse__title {
        font-size: 24px;
        color: $color-primary;
      }
      .source-container {
        margin-bottom: 10px;
        background-color: $color-grey-3;
        border-radius: 15px;
        .source-title {
          font-weight: bold;
        }
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

  &.user {
    .content {
      background-color: transparent;
    }
  }
}
</style>
