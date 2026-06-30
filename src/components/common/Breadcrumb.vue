<template>
  <nav class="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
    <template v-for="(crumb, index) in items" :key="index">
      <router-link
        v-if="crumb.to && index < items.length - 1"
        :to="crumb.to"
        class="hover:text-primary-600 transition-colors"
      >
        {{ crumb.label }}
      </router-link>
      <span v-else :class="index === items.length - 1 ? 'text-gray-800 dark:text-gray-200 font-medium' : ''">
        {{ crumb.label }}
      </span>
      <svg
        v-if="index < items.length - 1"
        class="w-3.5 h-3.5 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
      </svg>
    </template>
  </nav>
</template>

<script setup>
/**
 * Breadcrumb — Navigation breadcrumb with chevron separators
 */
defineProps({
  items: {
    type: Array,
    required: true,
    // Each item: { label: string, to?: string }
  },
})
</script>
