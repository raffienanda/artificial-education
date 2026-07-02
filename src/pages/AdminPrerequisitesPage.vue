<template>
  <AdminLayout>
      <div class="grid gap-4 lg:grid-cols-[360px_1fr]">
        <form class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800" @submit.prevent="createRelation">
          <h2 class="mb-4 text-base font-bold text-gray-900 dark:text-white">tambah relasi</h2>

          <label class="mb-3 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">topik tujuan</span>
            <select v-model="form.topic_id" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
              <option value="">pilih topik</option>
              <option v-for="module in modules" :key="module.id" :value="module.id">
                {{ module.title }}
              </option>
            </select>
          </label>

          <label class="mb-3 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">prasyarat</span>
            <select v-model="form.prerequisite_id" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
              <option value="">pilih prasyarat</option>
              <option v-for="module in modules" :key="module.id" :value="module.id">
                {{ module.title }}
              </option>
            </select>
          </label>

          <label class="mb-4 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">threshold mastery</span>
            <input
              v-model.number="form.mastery_threshold"
              type="number"
              min="0"
              max="100"
              class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900"
            >
          </label>

          <p v-if="error" class="mb-3 rounded-xl bg-danger-50 px-3 py-2 text-sm font-medium text-danger-600">
            {{ error }}
          </p>

          <button class="w-full rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-primary-700">
            simpan relasi
          </button>
        </form>

        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-base font-bold text-gray-900 dark:text-white">relasi aktif</h2>
            <button class="text-sm font-semibold text-primary-600" @click="loadData">refresh</button>
          </div>

          <div v-if="loading" class="py-10 text-center text-sm text-gray-500">
            memuat relasi...
          </div>

          <div v-else-if="relations.length === 0" class="rounded-xl bg-gray-50 p-4 text-sm text-gray-500 dark:bg-gray-900/50">
            belum ada relasi prasyarat.
          </div>

          <div v-else class="space-y-2">
            <div
              v-for="relation in relations"
              :key="relation.id"
              class="rounded-xl border border-gray-100 p-3 dark:border-gray-700"
            >
              <div class="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p class="text-sm font-bold text-gray-800 dark:text-gray-100">
                    {{ moduleTitle(relation.prerequisite_id) }} -> {{ moduleTitle(relation.topic_id) }}
                  </p>
                  <p class="mt-0.5 text-xs text-gray-400">
                    {{ relation.prerequisite_id }} -> {{ relation.topic_id }}
                  </p>
                </div>

                <div class="flex items-center gap-2">
                  <input
                    v-model.number="relation.mastery_threshold"
                    type="number"
                    min="0"
                    max="100"
                    class="w-20 rounded-lg border border-gray-200 px-2 py-1.5 text-sm dark:border-gray-700 dark:bg-gray-900"
                  >
                  <button class="rounded-lg bg-primary-50 px-3 py-1.5 text-xs font-bold text-primary-600 hover:bg-primary-100" @click="updateRelation(relation)">
                    update
                  </button>
                  <button class="rounded-lg bg-danger-50 px-3 py-1.5 text-xs font-bold text-danger-600 hover:bg-danger-100" @click="deleteRelation(relation.id)">
                    hapus
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  </AdminLayout>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { adminService } from '@/services/admin'
import { modulesService } from '@/services/modules'

const modules = ref([])
const relations = ref([])
const loading = ref(false)
const error = ref('')

const form = reactive({
  topic_id: '',
  prerequisite_id: '',
  mastery_threshold: 60,
})

function moduleTitle(moduleId) {
  return modules.value.find((module) => module.id === moduleId)?.title || moduleId
}

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const [moduleData, relationData] = await Promise.all([
      modulesService.getModules(),
      adminService.getPrerequisites(),
    ])
    modules.value = moduleData
    relations.value = relationData
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal memuat data admin'
  } finally {
    loading.value = false
  }
}

async function createRelation() {
  error.value = ''
  try {
    await adminService.createPrerequisite({ ...form })
    form.topic_id = ''
    form.prerequisite_id = ''
    form.mastery_threshold = 60
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal menambah relasi'
  }
}

async function updateRelation(relation) {
  error.value = ''
  try {
    await adminService.updatePrerequisite(relation.id, {
      mastery_threshold: relation.mastery_threshold,
    })
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal update relasi'
  }
}

async function deleteRelation(relationId) {
  error.value = ''
  try {
    await adminService.deletePrerequisite(relationId)
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal hapus relasi'
  }
}

onMounted(loadData)
</script>
