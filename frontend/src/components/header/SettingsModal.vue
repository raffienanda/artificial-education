<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="uiStore.settingsModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div 
          class="absolute inset-0 bg-black/40 backdrop-blur-sm"
          @click="uiStore.toggleSettingsModal()"
        />

        <!-- Modal Dialog -->
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-elevated w-full max-w-md overflow-hidden flex flex-col max-h-[90vh]">
          <!-- Header -->
          <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between flex-shrink-0">
            <h2 class="text-lg font-bold text-gray-900 dark:text-white">Pengaturan</h2>
            <button 
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              @click="uiStore.toggleSettingsModal()"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="p-6 overflow-y-auto space-y-6">
            <div>
              <h3 class="mb-3 text-xs font-bold uppercase tracking-wider text-gray-500">Tampilan</h3>
              <div class="flex items-center justify-between rounded-2xl border border-gray-100 p-3 dark:border-gray-700">
                <div>
                  <p class="text-sm font-semibold text-gray-800 dark:text-gray-200">Dark mode</p>
                  <p class="text-xs text-gray-500">ubah tampilan terang atau gelap</p>
                </div>
                <button 
                  class="relative w-11 h-6 rounded-full transition-colors duration-200"
                  :class="uiStore.darkMode ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'"
                  @click="uiStore.toggleDarkMode()"
                >
                  <div 
                    class="absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-transform duration-200 shadow-sm"
                    :class="uiStore.darkMode ? 'transform translate-x-5' : ''"
                  />
                </button>
              </div>

              <div class="mt-4">
                <p class="mb-2 text-sm font-semibold text-gray-800 dark:text-gray-200">Tema aplikasi</p>
                <div class="grid grid-cols-2 gap-3">
                  <button
                    v-for="theme in themeOptions"
                    :key="theme.id"
                    class="rounded-2xl border p-3 text-left transition"
                    :class="[
                      uiStore.activeTheme === theme.id
                        ? 'border-primary-500 bg-primary-50 shadow-sm ring-2 ring-primary-100 dark:ring-primary-900/40'
                        : isOwnedTheme(theme.id)
                          ? 'border-primary-200 bg-primary-50/40 hover:border-primary-300 dark:border-primary-700 dark:bg-primary-900/10'
                          : 'border-gray-100 bg-white hover:border-primary-200 dark:border-gray-700 dark:bg-gray-900/40',
                      !canUseTheme(theme.id) ? 'cursor-not-allowed opacity-50' : ''
                    ]"
                    type="button"
                    :disabled="!canUseTheme(theme.id)"
                    @click="selectTheme(theme)"
                  >
                    <div class="mb-3 flex items-center justify-between">
                      <span class="h-8 w-8 rounded-xl border border-white shadow-sm" :class="theme.swatchClass" />
                      <span
                        v-if="uiStore.activeTheme === theme.id"
                        class="rounded-full bg-primary-600 px-2 py-0.5 text-[10px] font-bold text-white"
                      >
                        aktif
                      </span>
                      <span
                        v-else-if="isOwnedTheme(theme.id)"
                        class="rounded-full bg-primary-100 px-2 py-0.5 text-[10px] font-bold text-primary-700"
                      >
                        dimiliki
                      </span>
                      <span
                        v-else-if="!canUseTheme(theme.id)"
                        class="rounded-full bg-gray-100 px-2 py-0.5 text-[10px] font-bold text-gray-400 dark:bg-gray-700"
                      >
                        terkunci
                      </span>
                    </div>
                    <p class="text-sm font-bold text-gray-900 dark:text-white">{{ theme.name }}</p>
                    <p class="mt-1 text-xs leading-relaxed text-gray-500">{{ theme.description }}</p>
                    <p
                      v-if="isOwnedTheme(theme.id) && uiStore.activeTheme !== theme.id"
                      class="mt-2 text-xs font-bold text-primary-700 dark:text-primary-300"
                    >
                      klik untuk pakai tema ini
                    </p>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Footer -->
          <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 flex justify-end">
            <BaseButton variant="primary" @click="uiStore.toggleSettingsModal()">
              Simpan
            </BaseButton>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
/**
 * SettingsModal — Application settings dialog for appearance preferences.
 */
import { useUiStore } from '@/stores/ui'
import { useUserStore } from '@/stores/user'
import BaseButton from '@/components/common/BaseButton.vue'
import { computed } from 'vue'

const uiStore = useUiStore()
const userStore = useUserStore()

const themeOptions = [
  {
    id: 'default',
    name: 'Default',
    description: 'tampilan bawaan aplikasi',
    swatchClass: 'theme-swatch-default',
  },
  {
    id: 'theme-forest',
    name: 'Forest',
    description: 'hijau lembut untuk belajar',
    swatchClass: 'theme-swatch-forest',
  },
  {
    id: 'theme-ocean',
    name: 'Ocean',
    description: 'teal laut yang lebih segar',
    swatchClass: 'theme-swatch-ocean',
  },
  {
    id: 'theme-violet',
    name: 'Pink',
    description: 'pink lembut untuk variasi',
    swatchClass: 'theme-swatch-violet',
  },
]

const redeemedThemes = computed(() => new Set(userStore.profile.redeemedRewards || []))

function canUseTheme(themeId) {
  return themeId === 'default' || redeemedThemes.value.has(themeId)
}

function isOwnedTheme(themeId) {
  return themeId !== 'default' && redeemedThemes.value.has(themeId)
}

function selectTheme(theme) {
  if (!canUseTheme(theme.id)) return
  uiStore.applyTheme(theme.id, { userId: userStore.userId })
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95) translateY(10px);
}
</style>
