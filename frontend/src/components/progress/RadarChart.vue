<template>
  <div class="w-full h-full flex items-center justify-center">
    <Radar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
/**
 * RadarChart — Visual representation of skills profile using Chart.js
 */
import { computed } from 'vue'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'
import { Radar } from 'vue-chartjs'
import { useUiStore } from '@/stores/ui'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

defineProps({
  chartData: { type: Object, required: true },
})

const uiStore = useUiStore()

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      min: 0,
      max: 100,
      ticks: { display: false, stepSize: 20 },
      grid: {
        color: uiStore.darkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
      },
      angleLines: {
        color: uiStore.darkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
      },
      pointLabels: {
        color: uiStore.darkMode ? 'rgba(255, 255, 255, 0.5)' : 'rgba(0, 0, 0, 0.5)',
        font: { size: 9, family: 'Inter' },
      },
    },
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: uiStore.darkMode ? 'rgba(31, 41, 55, 0.9)' : 'rgba(255, 255, 255, 0.9)',
      titleColor: uiStore.darkMode ? '#fff' : '#1f2937',
      bodyColor: uiStore.darkMode ? '#d1d5db' : '#4b5563',
      borderColor: uiStore.darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
      borderWidth: 1,
      padding: 8,
      boxPadding: 4,
      usePointStyle: true,
    },
  },
  animation: {
    duration: 1500,
    easing: 'easeOutQuart',
  },
}))
</script>
