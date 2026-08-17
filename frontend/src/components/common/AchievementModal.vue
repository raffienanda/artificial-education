<template>
  <Teleport to="body">
    <Transition name="modal-pop">
      <div v-if="show" class="fixed inset-0 z-[110] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm" @click="$emit('close')"></div>
        
        <!-- Modal Content -->
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl p-8 max-w-sm w-full text-center shadow-glass border border-white/20 overflow-hidden">
          <!-- Glow effect behind icon -->
          <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-warning-400/20 rounded-full blur-3xl pointer-events-none"></div>

          <!-- Icon -->
          <div class="relative w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-warning-100 to-warning-50 dark:from-warning-900/40 dark:to-warning-900/10 rounded-full flex items-center justify-center text-6xl shadow-inner border border-warning-200 dark:border-warning-700 animate-bounce-slow">
            {{ achievement?.icon || '🏆' }}
          </div>

          <!-- Text -->
          <h2 class="relative text-2xl font-black text-gray-900 dark:text-white mb-2 gradient-text">Pencapaian Baru!</h2>
          <h3 class="relative text-lg font-bold text-gray-800 dark:text-gray-200 mb-1">{{ achievement?.title || 'Level Up!' }}</h3>
          <p class="relative text-sm text-gray-500 dark:text-gray-400 mb-8">{{ achievement?.description || 'Kamu berhasil naik level berkat kerja kerasmu.' }}</p>

          <!-- Button -->
          <button 
            class="relative w-full py-3.5 px-4 bg-gradient-to-r from-warning-500 to-primary-500 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-300"
            @click="$emit('close')"
          >
            Lanjutkan Belajar
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
/**
 * AchievementModal — Pop-up for newly unlocked achievements or level ups
 */
defineProps({
  show: { type: Boolean, default: false },
  achievement: { type: Object, default: null }, // { title, description, icon }
})

defineEmits(['close'])
</script>

<style scoped>
.modal-pop-enter-active,
.modal-pop-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.modal-pop-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}
.modal-pop-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.animate-bounce-slow {
  animation: bounce-slow 3s infinite ease-in-out;
}
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
