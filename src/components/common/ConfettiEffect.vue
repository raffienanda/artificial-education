<template>
  <div v-if="active" class="fixed inset-0 pointer-events-none z-[100] overflow-hidden">
    <div
      v-for="i in 50"
      :key="i"
      class="confetti-piece absolute top-0"
      :style="getConfettiStyle(i)"
    ></div>
  </div>
</template>

<script setup>
/**
 * ConfettiEffect — Lightweight CSS-based confetti animation
 */
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  active: { type: Boolean, default: false },
})

const colors = ['#fde047', '#3b82f6', '#ef4444', '#22c55e', '#a855f7']

function getConfettiStyle(i) {
  const left = Math.random() * 100
  const animationDuration = Math.random() * 2 + 3 // 3-5 seconds
  const animationDelay = Math.random() * 1.5 // 0-1.5 seconds delay
  const width = Math.random() * 6 + 6 // 6-12px
  const height = width * (Math.random() * 0.5 + 1) // rectangle shape
  const bg = colors[Math.floor(Math.random() * colors.length)]

  return {
    left: `${left}%`,
    width: `${width}px`,
    height: `${height}px`,
    backgroundColor: bg,
    animation: `confetti-fall ${animationDuration}s ${animationDelay}s linear forwards`,
  }
}
</script>

<style>
@keyframes confetti-fall {
  0% {
    transform: translateY(-10vh) rotate(0deg) skew(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(110vh) rotate(720deg) skew(20deg);
    opacity: 0;
  }
}
</style>
