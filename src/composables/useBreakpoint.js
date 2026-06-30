/**
 * useBreakpoint Composable
 * Reactive breakpoint detection for responsive layouts
 */
import { ref, onMounted, onUnmounted, computed } from 'vue'

export function useBreakpoint() {
  const width = ref(typeof window !== 'undefined' ? window.innerWidth : 1200)

  function onResize() {
    width.value = window.innerWidth
  }

  onMounted(() => {
    window.addEventListener('resize', onResize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', onResize)
  })

  const isMobile = computed(() => width.value < 768)
  const isTablet = computed(() => width.value >= 768 && width.value < 1280)
  const isDesktop = computed(() => width.value >= 1280)

  const breakpoint = computed(() => {
    if (width.value < 768) return 'mobile'
    if (width.value < 1280) return 'tablet'
    return 'desktop'
  })

  return {
    width,
    isMobile,
    isTablet,
    isDesktop,
    breakpoint,
  }
}
