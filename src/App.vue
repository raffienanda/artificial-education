<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'

const theme = useTheme()

onMounted(() => {
  // Initialize dark mode based on saved preference
  theme.init()
})
</script>
