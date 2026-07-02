<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="mb-4 flex-shrink-0">
      <h2 class="text-lg font-bold text-gray-900 dark:text-white">Progress Modul</h2>
    </div>

    <div class="flex-1 overflow-y-auto pr-1 -mr-1 scrollbar-hide space-y-4">
      <!-- Three-card row: Radar + Average + History -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Card 1: Radar Chart -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-4 shadow-soft">
          <p class="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2">Tingkat Penguasaan per Sub-Materi</p>
          <div class="h-[180px] relative">
            <RadarChart v-if="radarChartData" :chartData="radarChartData" />
            <SkeletonLoader v-else type="chart" height="180px" />
          </div>
          <!-- Labels under radar -->
          <div class="flex flex-wrap gap-x-3 gap-y-1 mt-2 justify-center">
            <span v-for="sub in subtopicMastery" :key="sub.id" class="text-[10px] text-gray-500">
              <span class="font-medium text-gray-700 dark:text-gray-300">{{ sub.name }}</span>
              <span :class="sub.mastery >= 70 ? 'text-primary-500' : 'text-danger-500'" class="ml-0.5 font-bold">{{ sub.mastery }}%</span>
            </span>
          </div>
        </div>

        <!-- Card 2: Average Mastery + Status -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-5 shadow-soft flex flex-col">
          <p class="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-3">Rata-rata Penguasaan</p>
          <div class="flex-1 flex flex-col items-center justify-center">
            <span class="text-5xl font-extrabold text-gray-900 dark:text-white leading-none">{{ overallMastery }}%</span>
            <div class="flex items-center gap-1.5 mt-2">
              <span class="w-2.5 h-2.5 rounded-full" :class="statusDotColor" />
              <span class="text-sm font-medium" :class="statusTextColor">{{ statusLabel }}</span>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
            <p class="text-xs font-semibold text-gray-500 mb-1">Status</p>
            <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
              {{ recommendations?.statusMessage || 'Kamu perlu fokus pada 2 materi yang belum dikuasai.' }}
            </p>
          </div>
        </div>

        <!-- Card 3: Riwayat Belajar -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-4 shadow-soft">
          <p class="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-3">Riwayat Belajar</p>
          <div class="space-y-3">
            <div
              v-for="act in recentActivities"
              :key="act.id"
              class="flex items-center gap-3"
            >
              <div
                :class="[
                  'w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0',
                  activityBg(act.color),
                ]"
              >
                {{ act.icon }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-xs font-semibold text-gray-800 dark:text-gray-200 truncate">{{ act.title }}</p>
                <p class="text-[10px] text-gray-400 dark:text-gray-500">{{ act.time }}</p>
              </div>
              <span
                :class="[
                  'text-xs font-bold px-2 py-0.5 rounded-full',
                  act.mastery >= 70 ? 'bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400' : 'bg-danger-100 text-danger-600 dark:bg-danger-900/30 dark:text-danger-400',
                ]"
              >
                {{ act.mastery }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom info banner -->
      <div class="flex items-center gap-2 px-4 py-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-100 dark:border-gray-700">
        <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
        </svg>
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Sistem akan mengulang materi dengan penguasaan di bawah 80%.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * ProgressPanel — Redesigned to match reference with 3-card row layout
 */
import { computed, onMounted } from 'vue'
import { useProgressStore } from '@/stores/progress'
import RadarChart from './RadarChart.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'

const progressStore = useProgressStore()

const overallMastery = computed(() => progressStore.overallMastery)
const subtopicMastery = computed(() => progressStore.subtopicMastery)
const radarChartData = computed(() => progressStore.radarChartData)
const recentActivities = computed(() => progressStore.recentActivities)
const recommendations = computed(() => progressStore.recommendations)

const statusLabel = computed(() => {
  if (overallMastery.value >= 80) return 'Baik'
  if (overallMastery.value >= 60) return 'Cukup'
  if (overallMastery.value >= 40) return 'Kurang'
  return 'Perlu Perbaikan'
})

const statusDotColor = computed(() => {
  if (overallMastery.value >= 80) return 'bg-success-500'
  if (overallMastery.value >= 60) return 'bg-warning-500'
  return 'bg-danger-500'
})

const statusTextColor = computed(() => {
  if (overallMastery.value >= 80) return 'text-success-600 dark:text-success-400'
  if (overallMastery.value >= 60) return 'text-warning-600 dark:text-warning-400'
  return 'text-danger-600 dark:text-danger-400'
})

function activityBg(color) {
  const map = {
    primary: 'bg-primary-100 dark:bg-primary-900/30',
    success: 'bg-success-100 dark:bg-success-900/30',
    warning: 'bg-warning-100 dark:bg-warning-900/30',
    danger: 'bg-danger-100 dark:bg-danger-900/30',
  }
  return map[color] || map.primary
}

onMounted(() => {
  progressStore.fetchAll()
})
</script>
