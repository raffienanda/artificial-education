<template>
  <div class="relative" ref="searchContainer">
    <div
      :class="[
        'flex items-center gap-2 bg-gray-100 dark:bg-gray-700 rounded-xl px-3 py-2 transition-all duration-200',
        focused ? 'ring-2 ring-primary-500/40 bg-white dark:bg-gray-800' : '',
      ]"
    >
      <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <input
        ref="inputRef"
        v-model="query"
        type="text"
        :placeholder="placeholder"
        class="bg-transparent text-sm text-gray-700 dark:text-gray-200 outline-none flex-1 placeholder-gray-400"
        @focus="focused = true"
        @blur="handleBlur"
        @input="onInput"
      />
      <kbd v-if="!query && !focused" class="hidden sm:inline text-[10px] bg-gray-200 dark:bg-gray-600 text-gray-500 dark:text-gray-400 px-1.5 py-0.5 rounded font-mono">
        ⌘K
      </kbd>
    </div>

    <!-- Search results dropdown -->
    <Transition name="dropdown">
      <div
        v-if="focused && filteredResults.length > 0"
        class="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-800 rounded-2xl shadow-elevated border border-gray-100 dark:border-gray-700 overflow-hidden z-50 max-h-64 overflow-y-auto"
      >
        <button
          v-for="result in filteredResults"
          :key="result.id"
          class="w-full px-4 py-3 flex items-center gap-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-left"
          @mousedown.prevent="selectResult(result)"
        >
          <span class="text-lg">{{ result.icon }}</span>
          <div>
            <p class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ result.title }}</p>
            <p class="text-xs text-gray-500">{{ result.description }}</p>
          </div>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
/**
 * SearchBar — Search input with debounced filtering and dropdown results
 */
import { ref, computed } from 'vue'
import { modules } from '@/data/modules'

const props = defineProps({
  placeholder: { type: String, default: 'Search modules...' },
})

const emit = defineEmits(['select'])

const query = ref('')
const focused = ref(false)
const inputRef = ref(null)

// Build searchable items from modules data
const searchableItems = modules.map((mod) => ({
  id: mod.id,
  title: mod.title,
  description: mod.description,
  icon: mod.icon,
}))

const filteredResults = computed(() => {
  if (!query.value.trim()) return []
  const q = query.value.toLowerCase()
  return searchableItems.filter(
    (item) =>
      item.title.toLowerCase().includes(q) || item.description.toLowerCase().includes(q)
  )
})

function onInput() {
  // Debounce can be added here for real API calls
}

function selectResult(result) {
  query.value = result.title
  focused.value = false
  emit('select', result)
}

function handleBlur() {
  setTimeout(() => {
    focused.value = false
  }, 150)
}

function focus() {
  inputRef.value?.focus()
}

defineExpose({ focus })
</script>

<style scoped>
.dropdown-enter-active {
  transition: all 0.2s ease-out;
}
.dropdown-leave-active {
  transition: all 0.15s ease-in;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
