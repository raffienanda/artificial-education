<template>
  <BaseCard hover class="cursor-pointer group" @click="$emit('click', module)">
    <div class="flex items-center gap-3">
      <div class="text-2xl">{{ module.icon }}</div>
      <div class="flex-1 min-w-0">
        <h4 class="text-sm font-semibold text-gray-800 dark:text-gray-100 truncate group-hover:text-primary-600 transition-colors">
          {{ module.title }}
        </h4>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ module.estimatedTime }}</p>
      </div>
      <BaseBadge v-if="module.status === 'completed'" variant="success" size="xs">Done</BaseBadge>
      <BaseBadge v-else-if="module.status === 'in-progress'" variant="primary" size="xs">{{ module.progress }}%</BaseBadge>
      <BaseBadge v-else variant="neutral" size="xs">Locked</BaseBadge>
    </div>
    <div class="mt-3 progress-bar">
      <div
        class="progress-bar-fill"
        :class="module.status === 'completed' ? 'bg-success-400' : 'bg-primary-500'"
        :style="{ width: module.progress + '%' }"
      />
    </div>
  </BaseCard>
</template>

<script setup>
/**
 * ModuleCard — Compact card for module listings with progress bar
 */
import BaseCard from '@/components/common/BaseCard.vue'
import BaseBadge from '@/components/common/BaseBadge.vue'

defineProps({
  module: { type: Object, required: true },
})

defineEmits(['click'])
</script>
