/**
 * useTypingAnimation Composable
 * Provides character-by-character typing effect for chatbot AI responses
 */
import { ref, onUnmounted } from 'vue'

export function useTypingAnimation(speed = 15) {
  const displayedText = ref('')
  const isAnimating = ref(false)
  let intervalId = null

  /**
   * Animate text appearing character by character
   * @param {string} fullText - The complete text to animate
   * @returns {Promise<void>}
   */
  function animate(fullText) {
    return new Promise((resolve) => {
      displayedText.value = ''
      isAnimating.value = true
      let index = 0

      intervalId = setInterval(() => {
        if (index < fullText.length) {
          displayedText.value += fullText[index]
          index++
        } else {
          clearInterval(intervalId)
          intervalId = null
          isAnimating.value = false
          resolve()
        }
      }, speed)
    })
  }

  function stop() {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
      isAnimating.value = false
    }
  }

  function reset() {
    stop()
    displayedText.value = ''
  }

  onUnmounted(() => {
    stop()
  })

  return {
    displayedText,
    isAnimating,
    animate,
    stop,
    reset,
  }
}
