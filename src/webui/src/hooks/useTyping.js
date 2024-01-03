const useTyping = ({ content, typingCallback, speed, stopTypingCallback }) => {
  const typingTimer = ref(null)
  const timerStopped = ref(true)
  const renderedResult = ref('')

  const arr = content.split('')

  function typing() {
    if (!arr.length || timerStopped.value) {
      timerStopped.value = true
      if (typingTimer) {
        clearTimeout(typingTimer)
      }
      return
    }
    typingTimer.value = setTimeout(() => {
      renderedResult.value += arr.shift()
      typingCallback()
      typing()
    }, speed)
  }

  function stopTyping() {
    timerStopped.value = true
    if (typingTimer) {
      clearTimeout(typingTimer)
    }
    stopTypingCallback()
  }

  return {
    typingTimer,
    timerStopped,
    renderedResult,
    typing,
    stopTyping
  }
}

export default useTyping
