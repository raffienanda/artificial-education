<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import { useUserStore } from '@/stores/user'

const theme = useTheme()
const userStore = useUserStore()

onMounted(() => {
  // Initialize dark mode based on saved preference
  theme.init()
  userStore.initAuth()
})
</script>
