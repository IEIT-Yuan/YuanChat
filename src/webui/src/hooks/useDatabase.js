import Dexie from 'dexie'

const useDatabase = () => {
  const db = new Dexie('yuanChat')
  db.version(1).stores({
    conversations: '++id, name, start_time',
    messages: '++id, conversation_id, sender, content, timestamp'
  })

  return {
    db,
    conversationsDb: db.table('conversations'),
    messagesDb: db.table('messages')
  }
}

export default useDatabase
