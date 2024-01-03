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

const emits = defineEmits(['update', 'typingStopped'])

function typing() {
  emits('update')
}

function typingStopped(renderedResult) {
  emits('typingStopped', renderedResult)
}

const isUser = computed(() => {
  return props.sender === 'USER'
})
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
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped lang="less">
.chat-item_container {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  margin: 10px auto;

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
    margin-left: 12px;
    box-sizing: border-box;
    padding: 14px 24px;
    color: @color-black;
    background-color: @color-white;
    border-radius: 10px;
    width: 100%;
    flex: 1;
    font-size: 15px;
    line-height: 1.8;
  }

  &.user {
    .content {
      background-color: transparent;
    }
  }
}
</style>
