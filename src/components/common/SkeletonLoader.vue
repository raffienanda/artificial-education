<template>
  <div class="animate-pulse">
    <!-- Text line skeleton -->
    <template v-if="type === 'text'">
      <div v-for="n in lines" :key="n" class="skeleton h-4 mb-2.5" :style="{ width: n === lines ? '60%' : '100%' }" />
    </template>

    <!-- Rectangle skeleton (for cards, images) -->
    <div v-else-if="type === 'rect'" class="skeleton" :style="{ width: width, height: height }" />

    <!-- Circle skeleton (for avatars) -->
    <div v-else-if="type === 'circle'" class="skeleton rounded-full" :style="{ width: size, height: size }" />

    <!-- Card skeleton (composed) -->
    <div v-else-if="type === 'card'" class="space-y-3">
      <div class="skeleton h-32 rounded-2xl" />
      <div class="skeleton h-4 w-3/4" />
      <div class="skeleton h-4 w-1/2" />
    </div>

    <!-- Chart skeleton -->
    <div v-else-if="type === 'chart'" class="flex items-center justify-center" :style="{ height: height || '200px' }">
      <div class="skeleton rounded-full" :style="{ width: '160px', height: '160px' }" />
    </div>
  </div>
</template>

<script setup>
/**
 * SkeletonLoader — Animated loading placeholder with configurable shapes
 */
defineProps({
  type: {
    type: String,
    default: 'text',
    validator: (v) => ['text', 'rect', 'circle', 'card', 'chart'].includes(v),
  },
  lines: { type: Number, default: 3 },
  width: { type: String, default: '100%' },
  height: { type: String, default: '20px' },
  size: { type: String, default: '48px' },
})
</script>
