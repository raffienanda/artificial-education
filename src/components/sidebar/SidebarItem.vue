<template>
  <div class="relative">
    <!-- Connecting vertical line -->
    <div
      v-if="!isLast"
      :class="[
        'absolute left-[18px] top-[44px] w-[2px] h-6',
        module.status === 'completed' ? 'bg-primary-400' : 'bg-gray-200 dark:bg-gray-600',
      ]"
    />

    <!-- Module item button -->
    <button
      :class="[
        'w-full flex items-center gap-3 px-2 py-2.5 rounded-xl transition-all duration-200 group text-left mb-1',
        isActive
          ? 'bg-primary-50 dark:bg-primary-900/20'
          : 'hover:bg-gray-50 dark:hover:bg-gray-700/50',
        module.status === 'locked' ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
      ]"
      :disabled="module.status === 'locked'"
      @click="$emit('click', module)"
    >
      <!-- Numbered circle -->
      <div
        :class="[
          'w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-bold transition-all duration-200',
          isActive
            ? 'bg-primary-600 text-white shadow-sm'
            : module.status === 'completed'
              ? 'bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400'
              : 'bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-400',
        ]"
      >
        {{ number }}
      </div>

      <!-- Module info -->
      <div class="flex-1 min-w-0">
        <p
          :class="[
            'text-sm font-semibold leading-tight',
            isActive ? 'text-primary-700 dark:text-primary-300' : 'text-gray-800 dark:text-gray-200',
          ]"
        >
          {{ module.title }}
        </p>
        <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">
          {{ module.subMateriCount || module.subtopics?.length || 0 }} sub-materi
        </p>
      </div>

      <!-- Arrow indicator for active -->
      <svg
        v-if="isActive"
        class="w-4 h-4 text-primary-500 flex-shrink-0"
        fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template>

<script setup>
/**
 * SidebarItem — Numbered module item matching reference design
 */
defineProps({
  module: { type: Object, required: true },
  number: { type: Number, required: true },
  isActive: { type: Boolean, default: false },
  isLast: { type: Boolean, default: false },
  collapsed: { type: Boolean, default: false },
})

defineEmits(['click'])
</script>
