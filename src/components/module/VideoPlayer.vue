<template>
  <div class="rounded-2xl overflow-hidden bg-gray-900 relative group animate-fade-in-up">
    <!-- Video placeholder with gradient overlay -->
    <div class="relative aspect-video bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
      <!-- Decorative background pattern -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-4 left-4 w-20 h-20 border border-white/20 rounded-full" />
        <div class="absolute bottom-8 right-8 w-32 h-32 border border-white/10 rounded-full" />
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 border border-white/5 rounded-full" />
      </div>

      <!-- Play button -->
      <button class="relative z-10 w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center group-hover:bg-primary-500/80 transition-all duration-300 group-hover:scale-110">
        <svg class="w-7 h-7 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z" />
        </svg>
      </button>

      <!-- Duration badge -->
      <span class="absolute bottom-3 right-3 bg-black/60 text-white text-xs font-medium px-2 py-1 rounded-lg backdrop-blur-sm">
        {{ duration }}
      </span>
    </div>

    <!-- Video title -->
    <div class="p-3 flex items-center gap-2">
      <svg class="w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="m15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z" />
      </svg>
      <p class="text-sm text-gray-300 font-medium">{{ title }}</p>
    </div>
  </div>
</template>

<script setup>
/**
 * VideoPlayer — Styled video container with play button overlay
 */
defineProps({
  title: { type: String, default: 'Video Lesson' },
  duration: { type: String, default: '5:00' },
})
</script>
