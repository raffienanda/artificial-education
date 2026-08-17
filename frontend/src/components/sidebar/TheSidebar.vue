<template>
  <!-- Desktop Sidebar -->
  <aside
    :class="[
      'hidden xl:flex flex-col bg-white dark:bg-gray-800 border-r border-gray-100 dark:border-gray-700 transition-all duration-300 overflow-hidden h-screen sticky top-0 z-30',
      collapsed ? 'w-[72px]' : 'w-[280px]',
    ]"
  >
    <SidebarContent :collapsed="collapsed" />
  </aside>

  <!-- Mobile Sidebar Overlay -->
  <Teleport to="body">
    <Transition name="sidebar-overlay">
      <div
        v-if="mobileOpen"
        class="fixed inset-0 z-50 xl:hidden"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="uiStore.toggleMobileSidebar()" />

        <!-- Drawer -->
        <Transition name="sidebar-drawer">
          <aside
            v-if="mobileOpen"
            class="absolute left-0 top-0 bottom-0 w-[280px] bg-white dark:bg-gray-800 shadow-elevated flex flex-col"
          >
            <SidebarContent :collapsed="false" @close="uiStore.toggleMobileSidebar()" />
          </aside>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
/**
 * TheSidebar — Responsive sidebar with desktop collapse and mobile drawer
 */
import { computed } from 'vue'
import { useUiStore } from '@/stores/ui'
import SidebarContent from './SidebarContent.vue'

const uiStore = useUiStore()
const collapsed = computed(() => uiStore.sidebarCollapsed)
const mobileOpen = computed(() => uiStore.sidebarMobileOpen)
</script>

<style scoped>
.sidebar-overlay-enter-active,
.sidebar-overlay-leave-active {
  transition: opacity 0.3s ease;
}
.sidebar-overlay-enter-from,
.sidebar-overlay-leave-to {
  opacity: 0;
}

.sidebar-drawer-enter-active {
  transition: transform 0.3s ease-out;
}
.sidebar-drawer-leave-active {
  transition: transform 0.2s ease-in;
}
.sidebar-drawer-enter-from,
.sidebar-drawer-leave-to {
  transform: translateX(-100%);
}
</style>
