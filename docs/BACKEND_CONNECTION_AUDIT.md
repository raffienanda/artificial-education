# audit koneksi backend

status terakhir: frontend build berhasil dan endpoint utama sudah dites dengan akun baru.

## sudah lewat backend

- login, register, dan data user aktif
- daftar modul, status lock modul, dan status selesai subtopik
- pre test, quiz subtopik, drill, dan post test
- penyimpanan jawaban, attempt assessment, mastery, q-value, xp, combo, streak, dan poin
- gate pembelajaran: pre test selesai, quiz subtopik selesai, post test selesai, dan modul lulus
- rekomendasi learning path, q-learning, interaction log, dan debug q-value
- cognitive profile dan hasil profil kognitif
- gamifikasi: leaderboard dan reward
- admin graph prasyarat, soal, dan materi
- chatbot tutor melalui endpoint backend `/api/chatbot`

## yang memang masih lokal di browser

- token login dan data user ringan untuk session browser
- preferensi tampilan seperti dark mode, panel chatbot/progress disembunyikan, dan mode debug demo
- layout label grafik progress dari `src/data/progress.js`
- fallback tampilan profil/notifikasi dari `src/data/student.js`

## hasil tes akun fresh

- akun baru hanya mendapat `mod-001: in_progress`, sedangkan `mod-002` dan `mod-003` locked
- pre test modul 2 untuk akun baru ditolak backend dengan `403 Modul masih terkunci`
- sebelum pre test modul 1 selesai, subtopik 2 ditolak dengan `403 Pre test modul harus diselesaikan terlebih dahulu`
- setelah pre test modul 1 selesai, hanya subtopik 1 yang terbuka
- setelah quiz subtopik 1 selesai, subtopik 2 terbuka dan subtopik 3 tetap terkunci
- post test modul 1 ditolak sampai semua quiz subtopik dalam modul selesai
- setelah submit quiz, q-value dan interaction log terbentuk di backend

## catatan klaim machine learning

bagian yang sudah berjalan sebagai machine learning adaptif adalah q-learning pada level subtopik, karena q-value berubah dari reward hasil jawaban mahasiswa dengan update bellman. neural gkt sudah disiapkan sebagai model trainable untuk level modul, tetapi jangan diklaim sebagai neural gkt penuh yang sudah matang sebelum ada data interaksi mahasiswa yang cukup dan proses training/evaluasi yang valid.
