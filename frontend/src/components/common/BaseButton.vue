<template>
  <button
    :class="[buttonClasses, { 'opacity-60 cursor-not-allowed': disabled || loading }]"
    :disabled="disabled || loading"
    class="ripple-container relative inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2"
    @click="handleClick"
  >
    <!-- Loading spinner -->
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>

    <!-- Icon slot -->
    <span v-if="$slots.icon && !loading" class="mr-2">
      <slot name="icon" />
    </span>

    <!-- Button text -->
    <slot />

    <!-- Ripple effect element -->
    <span ref="rippleRef" class="ripple-effect" v-if="showRipple" :style="rippleStyle" />
  </button>
</template>

<script setup>
/**
 * BaseButton — Reusable button component with variants, sizes, and ripple effect
 */
import { computed, ref } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'ghost', 'danger', 'success', 'outline'].includes(v),
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  disabled: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  rounded: { type: Boolean, default: false },
})

const emit = defineEmits(['click'])
const showRipple = ref(false)
const rippleStyle = ref({})

const variantClasses = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500 shadow-soft',
  secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 focus:ring-gray-400 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600',
  ghost: 'bg-transparent text-gray-600 hover:bg-gray-100 focus:ring-gray-400 dark:text-gray-300 dark:hover:bg-gray-800',
  danger: 'bg-danger-500 text-white hover:bg-danger-600 focus:ring-danger-400 shadow-soft',
  success: 'bg-success-500 text-white hover:bg-success-600 focus:ring-success-400 shadow-soft',
  outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500 dark:hover:bg-primary-900/20',
}

const sizeClasses = {
  sm: 'px-3 py-1.5 text-xs gap-1',
  md: 'px-4 py-2 text-sm gap-1.5',
  lg: 'px-6 py-3 text-base gap-2',
}

const buttonClasses = computed(() => [
  variantClasses[props.variant],
  sizeClasses[props.size],
  props.rounded ? 'rounded-full' : 'rounded-xl',
])

function handleClick(e) {
  if (props.disabled || props.loading) return

  // Create ripple effect
  const button = e.currentTarget
  const rect = button.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height)
  rippleStyle.value = {
    width: `${size}px`,
    height: `${size}px`,
    left: `${e.clientX - rect.left - size / 2}px`,
    top: `${e.clientY - rect.top - size / 2}px`,
  }
  showRipple.value = true
  setTimeout(() => {
    showRipple.value = false
  }, 600)

  emit('click', e)
}
</script>
