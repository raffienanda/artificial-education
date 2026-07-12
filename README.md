# 🎓 Artificial Education

> **Intelligent Tutoring System (ITS)** dengan AI Hybrid — mendiagnosis dan mempersonalisasi jalur belajar mahasiswa secara adaptif.

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8.x-646CFF?logo=vite&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-Private-red)

---

## 📋 Deskripsi

**Artificial Education** adalah *Intelligent Tutoring System* (ITS) full-stack yang dirancang untuk memberikan pengalaman belajar mandiri yang adaptif. Sistem ini menggunakan model adaptif yang saat ini menggabungkan:

- **Graph Knowledge Tracing (GKT)** — *Macro Layer* untuk memetakan relasi prasyarat antar topik/modul dan melakukan *back-tracking* otomatis ketika skor pemahaman mahasiswa menurun.
- **Q-Learning Agent** — *Micro Layer* untuk menentukan aksi pembelajaran optimal (teks, video, atau kuis drill) di level sub-topik berdasarkan riwayat interaksi.

Catatan: Q-Learning sudah aktif sebagai machine learning utama. Neural GKT trainable awal sudah ditambahkan untuk level modul dengan pre test sebagai initial state dan graph prasyarat sebagai struktur hubungan. Model ini masih tahap bootstrap karena data mahasiswa nyata masih sedikit, jadi belum boleh diklaim sebagai hasil neural GKT yang sudah tervalidasi penuh.

Pilot project saat ini diterapkan pada mata kuliah **Algoritma dan Pemrograman**.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🔐 **Autentikasi** | Login/register dengan role-based access (Mahasiswa & Admin) |
| 📚 **Adaptive Module Viewer** | Menampilkan materi teks/video secara dinamis sesuai rekomendasi AI |
| 🧠 **GKT Engine** | Pelacakan pemahaman level makro dengan propagasi mundur ke modul prasyarat |
| 🤖 **Q-Learning Agent** | Penentuan aksi pembelajaran optimal di level sub-topik |
| 📝 **Interactive Drill & Practice** | Kuis interaktif sebagai environment pengumpul reward untuk Q-Learning |
| 📊 **Mastery Radar Tracker** | Visualisasi real-time tingkat pemahaman per topik (Radar Chart) |
| 💬 **AI Chatbot Assistant** | Asisten virtual kontekstual untuk menjawab pertanyaan materi |
| 🏆 **Gamification** | Sistem poin, badge, dan leaderboard untuk meningkatkan motivasi belajar |
| 🎯 **Rekomendasi AI** | Rekomendasi modul/materi berdasarkan analisis kelemahan mahasiswa |
| 🛠️ **Admin Panel** | Manajemen materi, soal, dan relasi prasyarat antar topik |

---

## 🏗️ Tech Stack

### Frontend
- **Framework:** Vue.js 3 (Composition API) + Vite 8
- **State Management:** Pinia 3
- **Routing:** Vue Router 4
- **Styling:** Tailwind CSS 3.4
- **Charts:** Chart.js + vue-chartjs
- **Icons:** Lucide Vue
- **HTTP Client:** Axios
- **Utilities:** VueUse, Marked (Markdown renderer)

### Backend
- **Framework:** Python FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL
- **Validation:** Pydantic 2
- **Server:** Uvicorn (ASGI)

### AI / ML Engine
- **GKT (Graph Knowledge Tracing):** Graph traversal untuk deteksi kelemahan prasyarat
- **Q-Learning:** Reinforcement Learning agent dengan Bellman update equation

---

## 📁 Struktur Proyek

```
artificial-education/
├── src/                          # Frontend (Vue.js)
│   ├── assets/                   # CSS global & animasi kustom
│   ├── components/               # Reusable UI components
│   │   ├── chatbot/              # Komponen AI chatbot
│   │   ├── common/               # Komponen umum (button, modal, dll.)
│   │   ├── drill/                # Komponen kuis drill
│   │   ├── header/               # Header navigasi
│   │   ├── module/               # Viewer materi modul
│   │   ├── progress/             # Progress & radar chart
│   │   ├── recommendation/       # Komponen rekomendasi AI
│   │   └── sidebar/              # Sidebar navigasi
│   ├── composables/              # Composable functions
│   │   ├── useBreakpoint.js      # Deteksi resolusi layar
│   │   ├── useTheme.js           # Theme kustom (dark/light)
│   │   ├── useToast.js           # Notifikasi toast
│   │   └── useTypingAnimation.js # Animasi mengetik chatbot
│   ├── data/                     # Data statis & mock data
│   ├── layouts/                  # Layout container
│   ├── pages/                    # Halaman aplikasi
│   │   ├── LoginPage.vue         # Halaman login
│   │   ├── DashboardPage.vue     # Dashboard utama
│   │   ├── ProfilePage.vue       # Profil mahasiswa
│   │   ├── GamificationPage.vue  # Halaman gamifikasi
│   │   ├── AdminMaterialsPage.vue    # Admin: kelola materi
│   │   ├── AdminPrerequisitesPage.vue # Admin: kelola prasyarat
│   │   └── AdminQuestionsPage.vue     # Admin: kelola soal
│   ├── router/                   # Konfigurasi routing
│   ├── services/                 # API service layer (Axios)
│   │   ├── api.js                # Base Axios instance
│   │   ├── auth.js               # Service autentikasi
│   │   ├── modules.js            # Service modul/materi
│   │   ├── quiz.js               # Service kuis
│   │   ├── progress.js           # Service progress belajar
│   │   ├── chatbot.js            # Service AI chatbot
│   │   ├── recommendation.js     # Service rekomendasi
│   │   ├── gamification.js       # Service gamifikasi
│   │   └── admin.js              # Service admin panel
│   ├── stores/                   # Pinia state management
│   │   ├── user.js               # State autentikasi & profil
│   │   ├── modules.js            # State modul pembelajaran
│   │   ├── quiz.js               # State kuis & drill
│   │   ├── progress.js           # State progress belajar
│   │   ├── chatbot.js            # State AI chatbot
│   │   ├── recommendation.js     # State rekomendasi
│   │   ├── gamification.js       # State gamifikasi
│   │   └── ui.js                 # State UI (sidebar, theme, toast)
│   ├── App.vue                   # Root component
│   └── main.js                   # Entry point
│
├── backend/                      # Backend (FastAPI + Python)
│   ├── app/
│   │   ├── api/endpoints/        # API endpoint handlers
│   │   │   ├── auth.py           # Endpoint autentikasi
│   │   │   ├── modules.py        # Endpoint modul/materi
│   │   │   ├── quiz.py           # Endpoint kuis & evaluasi
│   │   │   ├── progress.py       # Endpoint progress belajar
│   │   │   ├── recommendation.py # Endpoint rekomendasi AI
│   │   │   ├── gamification.py   # Endpoint gamifikasi
│   │   │   └── admin.py          # Endpoint admin panel
│   │   ├── core/                 # Konfigurasi & database setup
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── services/             # Business logic layer
│   │   ├── ml/                   # Machine Learning engine
│   │   │   ├── gkt.py            # Graph Knowledge Tracing
│   │   │   └── q_learning.py     # Q-Learning agent
│   │   └── main.py               # FastAPI app entry point
│   ├── db_init.py                # Database initialization script
│   ├── seed_full.py              # Database seeder (data lengkap)
│   └── requirements.txt          # Python dependencies
│
├── index.html                    # HTML entry point
├── vite.config.js                # Vite configuration
├── tailwind.config.js            # Tailwind CSS configuration
├── postcss.config.js             # PostCSS configuration
├── package.json                  # Node.js dependencies
├── ARCHITECTURE.md               # Dokumentasi arsitektur sistem
└── PRD.md                        # Product Requirements Document
```

---

## 🚀 Cara Menjalankan

### Prasyarat

- **Node.js** ≥ 18.x
- **Python** ≥ 3.10
- **PostgreSQL** ≥ 15
- **npm** ≥ 9.x

### 1. Clone Repository

```bash
git clone https://github.com/raffienanda/artificial-education.git
cd artificial-education
```

### 2. Setup Backend via CMD

Jalankan dari **Command Prompt / CMD**, bukan PowerShell.

```cmd
cd /d D:\GITHUB\artificial-education

REM Buat virtual environment
python -m venv .venv

REM Aktivasi virtual environment
.venv\Scripts\activate.bat

REM Install dependensi Python
pip install -r backend\requirements.txt

REM Inisialisasi database
python backend\db_init.py

REM Seed data awal / data demo lengkap
python backend\seed_full.py
```

Setelah setup selesai, jalankan backend dari folder `backend`:

```cmd
cd /d D:\GITHUB\artificial-education\backend
D:\GITHUB\artificial-education\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Backend akan berjalan di: [http://localhost:8000](http://localhost:8000)  
Dokumentasi API (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

Kalau virtual environment sudah aktif dan posisi terminal sudah berada di folder `backend`, bisa juga pakai:

```cmd
python -m uvicorn app.main:app --reload --port 8000
```

Jika muncul error `'uvicorn' is not recognized`, gunakan `python -m uvicorn` seperti contoh di atas, bukan langsung `uvicorn`.

Jika muncul error `No module named 'backend'`, berarti command dijalankan dengan target app yang salah. Gunakan:

```cmd
cd /d D:\GITHUB\artificial-education\backend
D:\GITHUB\artificial-education\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Jika muncul error `No module named uvicorn`, install ulang dependency backend:

```cmd
cd /d D:\GITHUB\artificial-education
.venv\Scripts\activate.bat
pip install -r backend\requirements.txt
```

### 3. Setup Frontend

Jalankan dari root project di CMD lain:

```cmd
cd /d D:\GITHUB\artificial-education

REM Install dependensi Node.js
npm install

REM Jalankan development server
npm run dev
```

Frontend akan berjalan di: [http://localhost:3000](http://localhost:3000)

### 4. Membuka Demo via ngrok

Pastikan backend dan frontend sudah berjalan:

- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:3000](http://localhost:3000)

Jalankan ngrok dari CMD:

```cmd
ngrok http 3000
```

Gunakan URL `https://...ngrok-free...` yang muncul dari ngrok untuk dibagikan ke dosen atau teman. Frontend sudah memakai base API `/api`, dan Vite sudah mem-proxy `/api` ke backend lokal `http://127.0.0.1:8000`, jadi cukup satu tunnel ngrok untuk frontend.

Jika ngrok memberi domain lain dan Vite menolak host, jalankan frontend dengan tambahan host:

```cmd
set VITE_ALLOWED_HOSTS=nama-domain-ngrok-kamu.ngrok-free.dev
npm run dev
```

### 5. Build untuk Produksi

```cmd
cd /d D:\GITHUB\artificial-education
npm run build
npm run preview
```

---

## 🗄️ Skema Database

| Tabel | Deskripsi |
|-------|-----------|
| `users` | Akun mahasiswa dan admin, termasuk XP, streak, level, dan poin reward |
| `courses` | Mata kuliah yang menaungi modul pembelajaran |
| `modules` | Modul/topik utama, misalnya dasar variabel, percabangan, dan perulangan |
| `subtopics` | Subtopik atau materi kecil di dalam setiap modul |
| `questions` | Bank soal dengan tipe `pre_test`, `drill`, `quiz`, dan `post_test` |
| `assessment_attempts` | Riwayat pengerjaan assessment formal per akun, modul, subtopik, skor, status lulus, dan waktu selesai |
| `assessment_answers` | Detail jawaban mahasiswa per soal dalam satu attempt |
| `user_progress` | Mastery subtopik yang dipakai Q-Learning dan visual progress |
| `q_values` | Nilai Q per user-subtopik-action yang diperbarui dengan persamaan Bellman |
| `interaction_logs` | Log interaksi belajar untuk audit dan calon data training |
| `topic_prerequisites` | Graph prasyarat antar modul untuk gating learning path |
| `knowledge_edges` | Representasi edge graph pengetahuan yang disiapkan untuk Neural GKT |
| `knowledge_states` | State penguasaan user pada node modul/subtopik sebagai initial/updated knowledge state |
| `cognitive_items` | Butir instrumen perkembangan kognitif dari dosen |
| `cognitive_responses` | Jawaban mahasiswa terhadap instrumen kognitif |
| `cognitive_profiles` | Profil kognitif ringkas mahasiswa berdasarkan hasil instrumen |

Catatan rancangan: pre test dipakai sebagai initial state mahasiswa di awal modul, quiz subtopik memperbarui state subtopik dan Q-Learning, sedangkan post test dipakai sebagai evaluasi akhir untuk membuka modul berikutnya. Tabel `knowledge_edges` dan `knowledge_states` disiapkan supaya implementasi sekarang tetap bisa berjalan, tetapi datanya tetap siap dikembangkan ke Neural GKT saat interaksi mahasiswa sudah cukup.

Instrumen perkembangan kognitif Perry dipakai sebagai profil tambahan mahasiswa. Jawaban instrumen disimpan di `cognitive_responses`, diringkas ke `cognitive_profiles`, lalu tahap dominannya ikut masuk ke state Q-Learning, misalnya `low:stable:dualism`. Dengan begitu sistem tidak hanya membaca benar/salah jawaban, tetapi juga mulai membedakan pola rekomendasi berdasarkan cara berpikir mahasiswa.

---

## 🧠 Arsitektur AI Hybrid

```
┌─────────────────────────────────────────────────┐
│                   Vue.js Client                 │
│          (Mengirim Action mahasiswa)             │
└────────────────────┬────────────────────────────┘
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────┐
│               FastAPI Backend                    │
│           (API Gateway + Business Logic)         │
└────────────────────┬────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│   GKT Engine     │  │  Q-Learning Agent│
│  (Macro Layer)   │  │  (Micro Layer)   │
│                  │  │                  │
│ • Graph Traversal│  │ • Bellman Update │
│ • Back-tracking  │  │ • Action Select  │
│ • Mastery Check  │  │ • Reward Calc    │
└──────────────────┘  └──────────────────┘
          │                     │
          └──────────┬──────────┘
                     ▼
          ┌──────────────────┐
          │   PostgreSQL DB  │
          └──────────────────┘
```

---

## 📖 Dokumentasi Tambahan

- [ARCHITECTURE.md](ARCHITECTURE.md) — Arsitektur sistem & spesifikasi teknis lengkap
- [PRD.md](PRD.md) — Product Requirements Document

---

## 👥 Tim Pengembang

**Artificial Education** dikembangkan sebagai proyek penelitian untuk pengembangan Intelligent Tutoring System adaptif.

---

<p align="center">
  Dibuat dengan ❤️ untuk pendidikan yang lebih cerdas dan adaptif.
</p>
