<template>
  <AdminLayout>
      <div class="mb-4 rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800">
        <label class="block">
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">filter modul</span>
          <select v-model="selectedModuleId" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
            <option value="">semua modul</option>
            <option v-for="module in modules" :key="module.id" :value="module.id">
              {{ module.title }}
            </option>
          </select>
        </label>
      </div>

      <div>
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <div class="mb-4 flex flex-wrap items-center justify-between gap-2">
            <h2 class="text-base font-bold text-gray-900 dark:text-white">daftar subtopik</h2>
            <div class="flex gap-2">
              <button class="rounded-xl border border-gray-200 px-4 py-2 text-sm font-bold text-gray-600 transition hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700/50" @click="loadSubtopics">
                refresh
              </button>
              <button class="rounded-xl bg-primary-600 px-4 py-2 text-sm font-bold text-white transition hover:bg-primary-700" @click="openCreateSubtopic">
                tambah materi
              </button>
            </div>
          </div>

          <div v-if="loading" class="py-10 text-center text-sm text-gray-500">memuat subtopik...</div>
          <div v-else-if="subtopics.length === 0" class="rounded-xl bg-gray-50 p-4 text-sm text-gray-500 dark:bg-gray-900/50">
            belum ada subtopik.
          </div>

          <div v-else class="space-y-2">
            <article v-for="subtopic in subtopics" :key="subtopic.id" class="rounded-xl border border-gray-100 p-3 dark:border-gray-700">
              <div class="flex flex-wrap items-start justify-between gap-3">
                <div class="min-w-0 flex-1">
                  <p class="text-sm font-bold text-gray-800 dark:text-gray-100">{{ subtopic.title }}</p>
                  <p class="mt-1 text-xs text-gray-400">{{ subtopic.id }} | {{ moduleTitle(subtopic.module_id) }}</p>
                </div>
                <div class="flex gap-2">
                  <button class="rounded-lg bg-primary-50 px-3 py-1.5 text-xs font-bold text-primary-600 hover:bg-primary-100" @click="editSubtopic(subtopic)">
                    edit
                  </button>
                  <button class="rounded-lg bg-danger-50 px-3 py-1.5 text-xs font-bold text-danger-600 hover:bg-danger-100" @click="deleteSubtopic(subtopic.id)">
                    hapus
                  </button>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>

      <div v-if="showFormModal" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-950/50 p-4">
        <form class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-2xl border border-gray-100 bg-white p-5 shadow-elevated dark:border-gray-700 dark:bg-gray-800" @submit.prevent="saveSubtopic">
          <div class="mb-4 flex items-center justify-between gap-3">
            <h2 class="text-base font-bold text-gray-900 dark:text-white">
              {{ editingId ? 'edit subtopik' : 'tambah materi' }}
            </h2>
            <button type="button" class="rounded-lg px-3 py-1.5 text-sm font-bold text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700" @click="closeFormModal">
              tutup
            </button>
          </div>

          <label class="mb-3 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">modul</span>
            <select v-model="form.module_id" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
              <option value="">pilih modul</option>
              <option v-for="module in modules" :key="module.id" :value="module.id">
                {{ module.title }}
              </option>
            </select>
          </label>

          <label class="mb-3 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">judul subtopik</span>
            <input v-model="form.title" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
          </label>

          <label class="mb-4 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">content json</span>
            <textarea
              v-model="contentText"
              rows="16"
              spellcheck="false"
              class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 font-mono text-xs leading-relaxed dark:border-gray-700 dark:bg-gray-900"
            />
          </label>

          <p v-if="error" class="mb-3 rounded-xl bg-danger-50 px-3 py-2 text-sm font-medium text-danger-600">
            {{ error }}
          </p>

          <div class="flex gap-2">
            <button class="flex-1 rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-primary-700">
              {{ editingId ? 'update subtopik' : 'simpan materi' }}
            </button>
            <button type="button" class="rounded-xl border border-gray-200 px-4 py-2.5 text-sm font-bold text-gray-600 dark:border-gray-700 dark:text-gray-300" @click="closeFormModal">
              batal
            </button>
          </div>
        </form>
      </div>
  </AdminLayout>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { adminService } from '@/services/admin'
import { modulesService } from '@/services/modules'

const modules = ref([])
const subtopics = ref([])
const selectedModuleId = ref('')
const loading = ref(false)
const error = ref('')
const editingId = ref('')
const showFormModal = ref(false)

function defaultContent(title = 'Materi Baru') {
  return {
    title,
    tabs: [
      { id: 'ringkasan', label: 'Ringkasan Materi', icon: 'book' },
      { id: 'video', label: 'Video Pembelajaran', icon: 'play' },
      { id: 'contoh', label: 'Contoh Soal', icon: 'file-text' },
    ],
    sections: [
      { type: 'text', content: 'Tulis ringkasan materi di sini.' },
      { type: 'example', title: 'Contoh', items: ['Tulis contoh materi di sini.'] },
    ],
  }
}

const form = reactive({
  module_id: '',
  title: '',
})
const contentText = ref(JSON.stringify(defaultContent(), null, 2))

function moduleTitle(moduleId) {
  return modules.value.find((module) => module.id === moduleId)?.title || moduleId
}

async function loadModules() {
  modules.value = await modulesService.getModules()
}

async function loadSubtopics() {
  loading.value = true
  error.value = ''
  try {
    subtopics.value = await adminService.getSubtopics({
      module_id: selectedModuleId.value || undefined,
    })
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal memuat subtopik'
  } finally {
    loading.value = false
  }
}

function resetForm() {
  editingId.value = ''
  form.module_id = selectedModuleId.value || ''
  form.title = ''
  contentText.value = JSON.stringify(defaultContent(), null, 2)
}

function openCreateSubtopic() {
  resetForm()
  error.value = ''
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  resetForm()
  error.value = ''
}

async function saveSubtopic() {
  error.value = ''
  let content
  try {
    content = JSON.parse(contentText.value)
  } catch {
    error.value = 'content json belum valid'
    return
  }

  try {
    const payload = {
      module_id: form.module_id,
      title: form.title,
      content,
    }

    if (editingId.value) {
      await adminService.updateSubtopic(editingId.value, payload)
    } else {
      await adminService.createSubtopic(payload)
    }
    resetForm()
    showFormModal.value = false
    await loadSubtopics()
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal menyimpan subtopik'
  }
}

function editSubtopic(subtopic) {
  error.value = ''
  editingId.value = subtopic.id
  form.module_id = subtopic.module_id
  form.title = subtopic.title
  contentText.value = JSON.stringify(subtopic.content, null, 2)
  showFormModal.value = true
}

async function deleteSubtopic(subtopicId) {
  error.value = ''
  try {
    await adminService.deleteSubtopic(subtopicId)
    await loadSubtopics()
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal hapus subtopik'
  }
}

watch(selectedModuleId, () => {
  form.module_id = selectedModuleId.value || form.module_id
  loadSubtopics()
})

onMounted(async () => {
  await loadModules()
  await loadSubtopics()
})
</script>
