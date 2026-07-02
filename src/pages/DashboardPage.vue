<template>
  <div class="h-full w-full p-2 sm:p-4 lg:p-6 lg:overflow-hidden overflow-y-auto">
    <!-- Dashboard CSS Grid Layout -->
    <div 
      class="w-full min-h-0 grid gap-4 lg:gap-5 relative lg:h-full"
      :class="[
        'grid-cols-1 lg:grid-cols-[1fr_320px] xl:grid-cols-[1fr_360px]',
        'grid-rows-auto lg:grid-rows-[minmax(0,1fr)_340px]'
      ]"
    >
      <!-- Center Top: Module Viewer -->
      <BaseCard 
        class="min-h-0 flex flex-col lg:row-start-1 lg:col-start-1 overflow-hidden"
        :padding="false"
      >
        <div class="h-full min-h-0 p-4 sm:p-5 lg:p-6 flex flex-col overflow-hidden">
          <ModuleViewer />
        </div>
      </BaseCard>

      <!-- Center Bottom: Learning Progress -->
      <BaseCard 
        class="min-h-0 flex flex-col lg:row-start-2 lg:col-start-1 overflow-hidden"
        :padding="false"
      >
        <div class="h-full p-4 sm:p-5 flex flex-col overflow-y-auto scrollbar-hide">
          <ProgressPanel />
        </div>
      </BaseCard>

      <!-- Right Column: Chatbot + Practice Drill -->
      <div class="min-h-0 flex flex-col gap-4 lg:row-start-1 lg:row-span-2 lg:col-start-2">
        <BaseCard
          class="hidden min-h-0 lg:flex flex-col overflow-hidden border-none transition-all duration-300"
          :class="uiStore.chatbotDesktopVisible ? 'flex-1' : 'h-14 flex-shrink-0'"
          :padding="false"
        >
          <ChatbotPanel v-if="uiStore.chatbotDesktopVisible" />
          <button
            v-else
            class="flex h-full w-full items-center justify-between gap-3 px-4 text-left text-primary-600 transition-colors hover:bg-primary-50 dark:text-primary-300 dark:hover:bg-primary-900/20"
            title="Tampilkan chatbot"
            @click="uiStore.toggleChatbotDesktop()"
          >
            <span class="flex items-center gap-2">
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span class="text-sm font-bold">Chatbot AI</span>
            </span>
            <span class="text-xs font-semibold text-gray-400">Tampilkan</span>
          </button>
        </BaseCard>

        <BaseCard
          class="min-h-0 flex flex-col overflow-hidden"
          :class="uiStore.chatbotDesktopVisible ? 'lg:h-[340px] lg:flex-shrink-0' : 'lg:flex-1'"
          :padding="false"
        >
          <div class="h-full min-h-0 p-4 sm:p-5 flex flex-col overflow-y-auto scrollbar-hide">
            <PracticePanel />
          </div>
        </BaseCard>
      </div>
    </div>

    <!-- Mobile Floating Chatbot Button -->
    <button 
      class="lg:hidden fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-tr from-primary-500 to-secondary-500 rounded-full shadow-elevated text-white flex items-center justify-center z-40 hover:scale-105 transition-transform"
      @click="uiStore.toggleChatbotMobile()"
    >
      <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    </button>

    <!-- Mobile Chatbot Overlay -->
    <Teleport to="body">
      <Transition name="slide-up">
        <div 
          v-if="uiStore.chatbotMobileOpen"
          class="lg:hidden fixed inset-0 z-50 bg-white dark:bg-gray-900 flex flex-col"
        >
          <ChatbotPanel @close="uiStore.toggleChatbotMobile()" />
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
/**
 * DashboardPage — Main dashboard that auto-loads the first module on mount
 */
import { onMounted } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useUiStore } from '@/stores/ui'
import { useProgressStore } from '@/stores/progress'
import { useChatbotStore } from '@/stores/chatbot'

import BaseCard from '@/components/common/BaseCard.vue'
import ModuleViewer from '@/components/module/ModuleViewer.vue'
import ProgressPanel from '@/components/progress/ProgressPanel.vue'
import ChatbotPanel from '@/components/chatbot/ChatbotPanel.vue'
import PracticePanel from '@/components/drill/PracticePanel.vue'

const modulesStore = useModulesStore()
const uiStore = useUiStore()
const progressStore = useProgressStore()
const chatbotStore = useChatbotStore()

onMounted(async () => {
  // Load all initial data in parallel
  await Promise.all([
    modulesStore.fetchCourse(),
    modulesStore.fetchModules(),
    progressStore.fetchAll(),
    chatbotStore.fetchConversation(),
  ])

})
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}

</style>
