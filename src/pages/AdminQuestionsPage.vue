<template>
  <AdminLayout>
      <div class="mb-4 grid gap-3 rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800 md:grid-cols-2">
        <label>
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">filter modul</span>
          <select v-model="selectedModuleId" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
            <option value="">semua modul</option>
            <option v-for="module in modules" :key="module.id" :value="module.id">
              {{ module.title }}
            </option>
          </select>
        </label>
        <label>
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">filter subtopik</span>
          <select v-model="selectedSubtopicId" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
            <option value="">semua subtopik</option>
            <option v-for="subtopic in availableSubtopics" :key="subtopic.id" :value="subtopic.id">
              {{ subtopic.title }}
            </option>
          </select>
        </label>
      </div>

      <div>
        <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <div class="mb-4 flex flex-wrap items-center justify-between gap-2">
            <h2 class="text-base font-bold text-gray-900 dark:text-white">daftar soal</h2>
            <div class="flex gap-2">
              <button class="rounded-xl border border-gray-200 px-4 py-2 text-sm font-bold text-gray-600 transition hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700/50" @click="loadQuestions">
                refresh
              </button>
              <button class="rounded-xl bg-primary-600 px-4 py-2 text-sm font-bold text-white transition hover:bg-primary-700" @click="openCreateQuestion">
                tambah soal
              </button>
            </div>
          </div>

          <div v-if="loading" class="py-10 text-center text-sm text-gray-500">memuat soal...</div>
          <div v-else-if="questions.length === 0" class="rounded-xl bg-gray-50 p-4 text-sm text-gray-500 dark:bg-gray-900/50">
            belum ada soal.
          </div>

          <div v-else class="space-y-2">
            <article v-for="question in questions" :key="question.id" class="rounded-xl border border-gray-100 p-3 dark:border-gray-700">
              <div class="flex flex-wrap items-start justify-between gap-3">
                <div class="min-w-0 flex-1">
                  <div class="mb-2 flex flex-wrap items-center gap-2">
                    <span class="rounded-lg bg-gray-100 px-2 py-0.5 text-xs font-bold text-gray-600 dark:bg-gray-900 dark:text-gray-300">
                      {{ question.difficulty }}
                    </span>
                    <span class="text-xs text-gray-400">{{ question.subtopic_id }}</span>
                  </div>
                  <p class="whitespace-pre-wrap text-sm font-semibold text-gray-800 dark:text-gray-100">{{ question.question_text }}</p>
                  <p class="mt-2 text-xs text-gray-500">
                    jawaban: <span class="font-bold">{{ question.correct_answer.toUpperCase() }}</span>
                  </p>
                </div>
                <div class="flex gap-2">
                  <button class="rounded-lg bg-primary-50 px-3 py-1.5 text-xs font-bold text-primary-600 hover:bg-primary-100" @click="editQuestion(question)">
                    edit
                  </button>
                  <button class="rounded-lg bg-danger-50 px-3 py-1.5 text-xs font-bold text-danger-600 hover:bg-danger-100" @click="deleteQuestion(question.id)">
                    hapus
                  </button>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>

      <div v-if="showFormModal" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-950/50 p-4">
        <form class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-gray-100 bg-white p-5 shadow-elevated dark:border-gray-700 dark:bg-gray-800" @submit.prevent="saveQuestion">
          <div class="mb-4 flex items-center justify-between gap-3">
            <h2 class="text-base font-bold text-gray-900 dark:text-white">
              {{ editingId ? 'edit soal' : 'tambah soal' }}
            </h2>
            <button type="button" class="rounded-lg px-3 py-1.5 text-sm font-bold text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700" @click="closeFormModal">
              tutup
            </button>
          </div>

          <label class="mb-3 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">subtopik</span>
            <select v-model="form.subtopic_id" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
              <option value="">pilih subtopik</option>
              <option v-for="subtopic in allSubtopics" :key="subtopic.id" :value="subtopic.id">
                {{ subtopic.title }}
              </option>
            </select>
          </label>

          <label class="mb-3 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">pertanyaan</span>
            <textarea v-model="form.question_text" rows="4" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900" />
          </label>

          <div class="mb-3 grid gap-2">
            <label v-for="option in form.options" :key="option.id" class="block">
              <span class="text-xs font-bold uppercase text-gray-400">opsi {{ option.label }}</span>
              <input v-model="option.text" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
            </label>
          </div>

          <div class="mb-3 grid grid-cols-2 gap-3">
            <label>
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">jawaban benar</span>
              <select v-model="form.correct_answer" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
                <option v-for="option in form.options" :key="option.id" :value="option.id">
                  {{ option.label }}
                </option>
              </select>
            </label>
            <label>
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">difficulty</span>
              <select v-model="form.difficulty" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900">
                <option value="mudah">mudah</option>
                <option value="sedang">sedang</option>
                <option value="sulit">sulit</option>
              </select>
            </label>
          </div>

          <label class="mb-4 block">
            <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">explanation</span>
            <textarea v-model="form.explanation" rows="3" class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900" />
          </label>

          <p v-if="error" class="mb-3 rounded-xl bg-danger-50 px-3 py-2 text-sm font-medium text-danger-600">
            {{ error }}
          </p>

          <div class="flex gap-2">
            <button class="flex-1 rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-primary-700">
              {{ editingId ? 'update soal' : 'simpan soal' }}
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
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { adminService } from '@/services/admin'
import { modulesService } from '@/services/modules'

const modules = ref([])
const questions = ref([])
const selectedModuleId = ref('')
const selectedSubtopicId = ref('')
const loading = ref(false)
const error = ref('')
const editingId = ref('')
const showFormModal = ref(false)

const defaultOptions = () => [
  { id: 'a', label: 'A', text: '' },
  { id: 'b', label: 'B', text: '' },
  { id: 'c', label: 'C', text: '' },
  { id: 'd', label: 'D', text: '' },
]

const form = reactive({
  subtopic_id: '',
  question_text: '',
  options: defaultOptions(),
  correct_answer: 'a',
  explanation: '',
  difficulty: 'mudah',
})

const allSubtopics = computed(() => modules.value.flatMap((module) => module.subtopics || []))
const availableSubtopics = computed(() => {
  if (!selectedModuleId.value) return allSubtopics.value
  return modules.value.find((module) => module.id === selectedModuleId.value)?.subtopics || []
})

async function loadModules() {
  modules.value = await modulesService.getModules()
}

async function loadQuestions() {
  loading.value = true
  error.value = ''
  try {
    questions.value = await adminService.getQuestions({
      module_id: selectedModuleId.value || undefined,
      subtopic_id: selectedSubtopicId.value || undefined,
    })
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal memuat soal'
  } finally {
    loading.value = false
  }
}

function resetForm() {
  editingId.value = ''
  form.subtopic_id = selectedSubtopicId.value || ''
  form.question_text = ''
  form.options = defaultOptions()
  form.correct_answer = 'a'
  form.explanation = ''
  form.difficulty = 'mudah'
}

function openCreateQuestion() {
  resetForm()
  error.value = ''
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  resetForm()
  error.value = ''
}

async function saveQuestion() {
  error.value = ''
  try {
    if (editingId.value) {
      await adminService.updateQuestion(editingId.value, { ...form })
    } else {
      await adminService.createQuestion({ ...form })
    }
    resetForm()
    showFormModal.value = false
    await loadQuestions()
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal menyimpan soal'
  }
}

function editQuestion(question) {
  error.value = ''
  editingId.value = question.id
  form.subtopic_id = question.subtopic_id
  form.question_text = question.question_text
  form.options = question.options.map((option) => ({ ...option }))
  form.correct_answer = question.correct_answer
  form.explanation = question.explanation
  form.difficulty = question.difficulty
  showFormModal.value = true
}

async function deleteQuestion(questionId) {
  error.value = ''
  try {
    await adminService.deleteQuestion(questionId)
    await loadQuestions()
  } catch (err) {
    error.value = err.response?.data?.detail || 'gagal hapus soal'
  }
}

watch([selectedModuleId, selectedSubtopicId], () => {
  if (selectedModuleId.value && !availableSubtopics.value.some((subtopic) => subtopic.id === selectedSubtopicId.value)) {
    selectedSubtopicId.value = ''
  }
  form.subtopic_id = selectedSubtopicId.value || form.subtopic_id
  loadQuestions()
})

onMounted(async () => {
  await loadModules()
  await loadQuestions()
})
</script>
