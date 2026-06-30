<template>
  <span
    :class="[
      'inline-flex items-center font-medium',
      sizeClasses[size],
      variantClasses[variant],
      pill ? 'rounded-full' : 'rounded-lg',
    ]"
  >
    <span v-if="dot" :class="['w-1.5 h-1.5 rounded-full mr-1.5', dotClasses[variant]]" />
    <slot />
  </span>
</template>

<script setup>
/**
 * BaseBadge — Color-coded badge with dot indicator and pill shape option
 */
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'success', 'warning', 'danger', 'neutral', 'info'].includes(v),
  },
  size: {
    type: String,
    default: 'sm',
    validator: (v) => ['xs', 'sm', 'md'].includes(v),
  },
  pill: { type: Boolean, default: true },
  dot: { type: Boolean, default: false },
})

const variantClasses = {
  primary: 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300',
  success: 'bg-success-100 text-success-600 dark:bg-success-900/30 dark:text-success-400',
  warning: 'bg-warning-100 text-warning-600 dark:bg-warning-900/30 dark:text-warning-400',
  danger: 'bg-danger-100 text-danger-600 dark:bg-danger-900/30 dark:text-danger-400',
  neutral: 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300',
  info: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-300',
}

const dotClasses = {
  primary: 'bg-primary-500',
  success: 'bg-success-500',
  warning: 'bg-warning-500',
  danger: 'bg-danger-500',
  neutral: 'bg-gray-400',
  info: 'bg-blue-500',
}

const sizeClasses = {
  xs: 'px-1.5 py-0.5 text-[10px]',
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
}
</script>
