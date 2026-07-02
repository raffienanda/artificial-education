<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="uiStore.searchModalOpen" class="fixed inset-0 z-[100] flex items-start justify-center bg-black/40 p-4 pt-20 backdrop-blur-sm">
        <div class="w-full max-w-lg rounded-2xl bg-white p-4 shadow-elevated dark:bg-gray-800">
          <div class="mb-3 flex items-center justify-between">
            <h2 class="text-base font-bold text-gray-900 dark:text-white">Cari modul</h2>
            <button
              class="rounded-lg p-1 text-gray-400 transition hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-700"
              @click="uiStore.toggleSearchModal()"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <SearchBar placeholder="Cari modul..." @select="uiStore.toggleSearchModal()" />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { useUiStore } from '@/stores/ui'
import SearchBar from '@/components/common/SearchBar.vue'

const uiStore = useUiStore()
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
