# Artificial Education — Intelligent Tutoring System (ITS)

Artificial Education adalah frontend aplikasi Intelligent Tutoring System (ITS) berbasis Vue 3, Vite, Tailwind CSS, Pinia, dan Vue Router. Aplikasi ini memiliki fitur pembelajaran adaptif menggunakan model Bayesian Knowledge Tracing (BKT), chatbot asisten AI, dan kuis latihan interaktif.

## Cara Menjalankan Aplikasi

Aplikasi ini menggunakan port **3000** sebagai default dev server.

### Langkah-langkah menjalankan secara manual:

1. **Buka Terminal / Command Prompt** pada direktori project ini:
   ```bash
   cd "d:\NANDA\!kode\artificial-education"
   ```

2. **Install Dependensi** (jika belum atau jika dipindahkan ke komputer lain):
   ```bash
   npm install
   ```

3. **Jalankan Development Server**:
   ```bash
   npm run dev
   ```

4. **Buka Browser**:
   Akses aplikasi melalui URL berikut:
   [http://localhost:3000](http://localhost:3000)

---

## Folder Structure

- `src/assets/`: Berisi CSS global dan kustomisasi animasi.
- `src/components/`: Berisi reusable components (common, sidebar, module, progress, chatbot, drill, header).
- `src/data/`: Dummy data untuk kuis, subtopic, progress, profile mahasiswa, dan chat AI.
- `src/stores/`: Pinia stores untuk mengatur global state (UI, user, modules, progress, chatbot, quiz).
- `src/services/`: Services pemanggil API (menggunakan mock data dengan simulasi delay, siap dihubungkan ke backend asli).
- `src/pages/`: Halaman utama Dashboard dengan grid responsif.
- `src/layouts/`: Layout container aplikasi.
- `src/composables/`: Fungsi pembantu reaktif (theme kustom, deteksi resolusi layar/breakpoint, animasi mengetik chatbot).
