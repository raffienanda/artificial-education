<template>
  <div
    :class="[
      'bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 transition-all duration-300',
      rounded ? 'rounded-2xl' : 'rounded-xl',
      hover ? 'hover-lift cursor-pointer' : '',
      glass ? 'glass-card' : 'shadow-card',
      padding ? paddingClass : '',
      $attrs.class,
    ]"
  >
    <!-- Card header -->
    <div v-if="$slots.header || title" class="px-5 pt-5 pb-0">
      <slot name="header">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-semibold text-gray-800 dark:text-gray-100">{{ title }}</h3>
          <slot name="headerAction" />
        </div>
        <p v-if="subtitle" class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{{ subtitle }}</p>
      </slot>
    </div>

    <!-- Card body -->
    <div :class="['min-h-0 flex-1', padding ? paddingClass : '', !$slots.header && !title ? '' : 'pt-3']">
      <slot />
    </div>

    <!-- Card footer -->
    <div v-if="$slots.footer" class="px-5 pb-5 pt-3 border-t border-gray-100 dark:border-gray-700 mt-3">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
/**
 * BaseCard — Reusable card container with soft shadow, rounded corners, and hover lift
 */
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  hover: { type: Boolean, default: false },
  glass: { type: Boolean, default: false },
  rounded: { type: Boolean, default: true },
  padding: { type: Boolean, default: true },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
})

const paddingClass = computed(() => {
  const map = { sm: 'p-3', md: 'p-5', lg: 'p-6' }
  return map[props.size]
})
</script>
