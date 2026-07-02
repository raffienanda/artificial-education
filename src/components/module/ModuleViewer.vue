<template>
  <div class="h-full min-h-0 flex flex-col overflow-hidden">
    <!-- Empty State -->
    <div v-if="!activeContent" class="flex-1 flex items-center justify-center">
      <div class="text-center py-16">
        <div class="text-6xl mb-4">📚</div>
        <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2">Pilih Modul</h2>
        <p class="text-gray-500 dark:text-gray-400 text-sm max-w-md mx-auto">
          Pilih modul dari sidebar untuk mulai belajar. Progres kamu akan tersimpan otomatis.
        </p>
      </div>
    </div>

    <!-- Module Content -->
    <template v-else>
      <div class="min-h-0 flex-1 overflow-y-auto pr-2 -mr-2">
      <!-- Header Row: Title + Tandai Selesai -->
      <div class="flex items-center justify-between mb-1 flex-shrink-0">
        <h2 class="text-lg font-bold text-gray-900 dark:text-white">Materi Modul</h2>
        <button class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-primary-200 dark:border-primary-700 text-primary-600 dark:text-primary-400 text-sm font-medium hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
          </svg>
          Tandai Selesai
        </button>
      </div>

      <!-- Module Title -->
      <h1 class="text-xl font-bold text-gray-900 dark:text-gray-50 mb-2">
        {{ activeContent.title }}
      </h1>

      <AdaptiveRecommendationPanel />

      <!-- Tab Bar -->
      <div class="flex items-center gap-2 mb-5 flex-shrink-0 border-b border-gray-100 dark:border-gray-700 pb-0">
        <button
          v-for="(tab, idx) in tabs"
          :key="tab.id"
          :class="[
            'flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-t-xl transition-all duration-200 -mb-[1px]',
            activeTab === idx
              ? 'bg-primary-600 text-white shadow-sm'
              : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 dark:text-gray-400',
          ]"
          @click="activeTab = idx"
        >
          <span>{{ tab.icon }}</span>
          {{ tab.label }}
        </button>
      </div>

      <!-- Content Area -->
      <div>
        <div v-if="contentSections.length === 0" class="rounded-2xl border border-dashed border-gray-200 bg-gray-50 p-5 text-center text-sm text-gray-500 dark:border-gray-700 dark:bg-gray-800/60 dark:text-gray-400">
          Konten untuk bagian ini belum tersedia.
        </div>
        <div v-else class="space-y-5">
          <!-- Only show non-text sections (text already shown as description) -->
          <template v-for="(section, index) in contentSections" :key="index">
            <!-- Text Summary Section -->
            <div v-if="section.type === 'text'" class="animate-fade-in-up">
              <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-700 dark:bg-gray-800">
                <p class="text-sm leading-relaxed text-gray-600 dark:text-gray-300">
                  {{ section.content }}
                </p>
              </div>
            </div>

            <!-- Formula / Rules Section -->
            <div v-else-if="section.type === 'formula'" class="animate-fade-in-up">
              <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5">
                <h3 class="font-bold text-gray-900 dark:text-gray-100 text-sm mb-3">{{ section.title }}</h3>
                <ul class="space-y-2">
                  <li
                    v-for="(line, i) in section.content.split('\n')"
                    :key="i"
                    class="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300"
                  >
                    <span class="text-gray-400 mt-0.5 flex-shrink-0">•</span>
                    <span>{{ line }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Number Line Section -->
            <div v-else-if="section.type === 'numberline'" class="animate-fade-in-up">
              <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5">
                <NumberLineSVG />
              </div>
            </div>

            <!-- Example Section -->
            <div v-else-if="section.type === 'example'" class="example-box animate-fade-in-up">
              <div class="flex items-center gap-2 mb-3">
                <span class="text-lg">💡</span>
                <h3 class="font-semibold text-green-700 dark:text-green-300 text-sm">{{ section.title }}</h3>
              </div>
              <ul class="space-y-2">
                <li
                  v-for="(item, i) in section.items"
                  :key="i"
                  class="flex items-start gap-2.5 text-sm text-green-800 dark:text-green-200"
                >
                  <span class="text-green-500 mt-1 flex-shrink-0">●</span>
                  <span>{{ item }}</span>
                </li>
              </ul>
            </div>

            <!-- Video Placeholder -->
            <div v-else-if="section.type === 'video'" class="animate-fade-in-up">
              <VideoPlayer :title="section.title" :duration="section.duration || '5:00'" />
            </div>

            <!-- Interactive Placeholder -->
            <div v-else-if="section.type === 'interactive'" class="animate-fade-in-up">
              <BaseCard class="border-2 border-dashed border-primary-200 dark:border-primary-700">
                <div class="text-center py-6">
                  <div class="text-3xl mb-2">🎮</div>
                  <h3 class="font-semibold text-gray-800 dark:text-gray-200 text-sm">{{ section.title }}</h3>
                  <p class="text-xs text-gray-500 mt-1">{{ section.description }}</p>
                </div>
              </BaseCard>
            </div>
          </template>
        </div>
      </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex-shrink-0 flex items-center justify-between pt-4 mt-4 border-t border-gray-100 dark:border-gray-700">
        <button
          :disabled="!modulesStore.hasPreviousSubtopic"
          :class="[
            'flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 border',
            modulesStore.hasPreviousSubtopic
              ? 'border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
              : 'border-gray-100 dark:border-gray-700 text-gray-300 dark:text-gray-600 cursor-not-allowed',
          ]"
          @click="modulesStore.previousSubtopic()"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Sebelumnya
        </button>

        <button
          class="flex items-center gap-2 px-5 py-2 rounded-xl text-sm font-medium bg-primary-600 text-white hover:bg-primary-700 transition-all duration-200 shadow-sm"
          @click="handleNext"
        >
          Selanjutnya
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
/**
 * ModuleViewer — Redesigned to match reference with tab bar, number line SVG, and Indonesian labels
 */
import { ref, computed, watch } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useRecommendationStore } from '@/stores/recommendation'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import BaseCard from '@/components/common/BaseCard.vue'
import AdaptiveRecommendationPanel from '@/components/recommendation/AdaptiveRecommendationPanel.vue'
import VideoPlayer from './VideoPlayer.vue'
import NumberLineSVG from './NumberLineSVG.vue'

const modulesStore = useModulesStore()
const recommendationStore = useRecommendationStore()
const userStore = useUserStore()
const toast = useToast()

const activeTab = ref(0)

const activeModule = computed(() => modulesStore.activeModule)
const activeSubtopic = computed(() => modulesStore.activeSubtopic)
const activeContent = computed(() => modulesStore.activeContent)

const tabs = computed(() => {
  return activeContent.value?.tabs || [
    { id: 'ringkasan', label: 'Ringkasan Materi', icon: '📖' },
    { id: 'video', label: 'Video Pembelajaran', icon: '▶️' },
    { id: 'contoh', label: 'Contoh Soal', icon: '📝' },
  ]
})

// Filter content sections by active tab.
const contentSections = computed(() => {
  if (!activeContent.value?.sections) return []
  const sections = activeContent.value.sections
  const activeTabId = tabs.value[activeTab.value]?.id
  const tabTypes = {
    ringkasan: ['text', 'formula', 'numberline'],
    video: ['video'],
    contoh: ['example', 'interactive'],
  }
  const allowedTypes = tabTypes[activeTabId]
  if (!allowedTypes) return sections

  return sections.filter((section) => allowedTypes.includes(section.type))
})

function handleNext() {
  if (modulesStore.hasNextSubtopic) {
    modulesStore.nextSubtopic()
    activeTab.value = 0
  } else {
    toast.success('Bagian modul selesai! 🎉')
  }
}

// Reset tab on subtopic change
watch(() => modulesStore.activeSubtopicIndex, () => {
  activeTab.value = 0
})

watch(
  () => recommendationStore.microAction,
  (action) => {
    const targetTab = {
      show_text: 'ringkasan',
      show_video: 'video',
      easy_quiz: 'contoh',
      hard_quiz: 'contoh',
      review_previous: 'ringkasan',
    }[action]

    if (!targetTab) return

    const targetIndex = tabs.value.findIndex((tab) => tab.id === targetTab)
    if (targetIndex >= 0) {
      activeTab.value = targetIndex
    }
  },
)

watch(
  () => [activeModule.value?.id, activeSubtopic.value?.id],
  ([moduleId, subtopicId]) => {
    if (!moduleId || !subtopicId) {
      recommendationStore.clear()
      return
    }

    recommendationStore.fetchNext({
      userId: userStore.userId,
      currentModuleId: moduleId,
      currentSubtopicId: subtopicId,
    })
    recommendationStore.fetchLogs({ userId: userStore.userId })
  },
  { immediate: true },
)
</script>
