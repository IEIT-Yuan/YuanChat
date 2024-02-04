import useDatabase from '../hooks/useDatabase'
import { getRandomElements } from '@/utils/util'

const baseUrl = import.meta.env.BASE_URL

const { conversationsDb, messagesDb, db } = useDatabase()

// conversation
export function getConversationList() {
  return conversationsDb.reverse().toArray()
}

export function addConversation({ name }) {
  return conversationsDb.add({
    name,
    start_time: new Date().getTime()
  })
}

export async function deleteConversation(id) {
  return db.transaction('rw', conversationsDb, messagesDb, async () => {
    await messagesDb.where('conversation_id').equals(id).delete()
    await conversationsDb.delete(id)
  })
}

export function editConversationName(id, name) {
  return conversationsDb.update(id, { name })
}

// message
export function getAllMessagesList() {
  return messagesDb.toArray()
}

export function getMessagesByConversionId(conversation_id) {
  return messagesDb.where('conversation_id').equals(conversation_id).toArray()
}

export function addMessage({ content, sender, conversation_id, feedback }) {
  return messagesDb.add({
    content,
    sender,
    conversation_id,
    feedback,
    timestamp: new Date().getTime()
  })
}

export function updateMessage({ content, id }) {
  return messagesDb.update(id, { content })
}

export function updateFeedback({ feedback, id }) {
  return messagesDb.update(id, { feedback })
}
// welcome

// 返回的推荐问题数量
const RECOMMENDS_COUNT = 5

export function getRecommendList() {
  return fetch(`${baseUrl}recommends.json`)
    .then((res) => res.json())
    .then((data) => {
      return getRandomElements(data, RECOMMENDS_COUNT)
    })
}
