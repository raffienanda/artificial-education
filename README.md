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

- **Neural Graph Knowledge Tracing (Neural GKT)** — *Macro Layer* untuk memprediksi penguasaan topik/modul dari pre test, quiz, post test, data seed kurikulum, data sintetis, dan graph prasyarat.
- **Q-Learning Agent** — *Micro Layer* untuk menentukan aksi pembelajaran optimal (teks, video, atau kuis drill) di level sub-topik berdasarkan riwayat interaksi.

Catatan: Neural GKT sudah aktif sebagai model makro berbasis artifact `backend/storage/neural_gkt_model.json`. Model dilatih dari data seed, data sintetis, dan hasil pre test, quiz, serta post test yang sudah masuk database. Karena data mahasiswa nyata masih sedikit, klaim yang aman adalah Neural GKT bootstrap/trainable, belum model final yang tervalidasi kelas nyata.

Pilot project saat ini diterapkan pada mata kuliah **Algoritma dan Pemrograman**.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🔐 **Autentikasi** | Login/register dengan role-based access (Mahasiswa & Admin) |
| 📚 **Adaptive Module Viewer** | Menampilkan materi teks/video secara dinamis sesuai rekomendasi AI |
| 🧠 **Neural GKT Engine** | Prediksi penguasaan level makro berdasarkan graph prasyarat dan data assessment |
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
- **Neural GKT:** Model trainable untuk prediksi penguasaan topik/modul dari graph prasyarat, pre test, quiz, post test, data seed, dan data sintetis
- **Q-Learning:** Reinforcement Learning agent dengan Bellman update equation

---

## 📁 Struktur Proyek

Struktur terbaru untuk SUS test dan demo sudah dipisah menjadi dua bagian utama: `frontend` dan `backend`.

```text
artificial-education/
├── frontend/                     # Frontend Vue + Vite
│   ├── src/                      # Source code UI
│   ├── public/                   # Asset publik frontend
│   ├── index.html                # Entry HTML
│   ├── package.json              # Dependency frontend
│   ├── vite.config.js            # Konfigurasi Vite
│   ├── tailwind.config.js        # Konfigurasi Tailwind
│   └── postcss.config.js         # Konfigurasi PostCSS
│
├── backend/                      # Backend FastAPI
│   ├── app/                      # Source code API, model, service, dan ML
│   ├── scripts/                  # Script uji, training, dan evaluasi
│   ├── storage/                  # Artifact model Neural GKT
│   ├── requirements.txt          # Dependency backend
│   ├── db_init.py                # Inisialisasi database
│   └── seed_full.py              # Seed data demo
│
├── docs/                         # Dokumen RPL, proses bisnis, blackbox, dan SUS/support
├── postman/                      # Koleksi pengujian API
├── .venv/                        # Virtual environment lokal, tidak ikut hosting
├── README.md                     # Panduan project
├── ARCHITECTURE.md               # Dokumentasi arsitektur
└── PRD.md                        # Product Requirements Document
```

Struktur detail lama di bawah ini menjelaskan isi komponen dan service utama.

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
├── frontend/                     # Frontend app, config Vite, Tailwind, dan package.json
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

Jalankan dari folder `frontend` di CMD lain:

```cmd
cd /d D:\GITHUB\artificial-education\frontend

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
cd /d D:\GITHUB\artificial-education\frontend
set VITE_ALLOWED_HOSTS=nama-domain-ngrok-kamu.ngrok-free.dev
npm run dev
```

### 5. Build untuk Produksi

```cmd
cd /d D:\GITHUB\artificial-education\frontend
npm run build
npm run preview
```

### 6. Deployment Hemat untuk SUS Test

Skema hosting yang disarankan untuk tahap SUS test:

- **Frontend:** Hostinger Web Hosting
- **Backend:** Koyeb free tier
- **Database:** Supabase free tier

#### A. Setup Database Supabase

1. Buat project baru di Supabase.
2. Buka menu **Connect** pada project Supabase.
3. Salin connection string PostgreSQL dari bagian pooler.
4. Pastikan connection string memakai format seperti ini:

```text
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@[REGION].pooler.supabase.com:6543/postgres?sslmode=require
```

5. Simpan connection string tersebut untuk env `DATABASE_URL` di Koyeb.

#### B. Deploy Backend ke Koyeb

Deploy backend dari folder `backend`.

Environment variable yang perlu diisi di Koyeb:

```text
SECRET_KEY=isi-dengan-random-secret-yang-panjang
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=connection-string-supabase
BACKEND_CORS_ORIGINS=https://domain-frontend-kamu
```

Jika Koyeb meminta run command, gunakan:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

File `backend/Procfile` juga sudah disiapkan untuk menjalankan command backend secara otomatis.

Setelah backend berhasil deploy, cek URL:

```text
https://nama-backend.koyeb.app/
https://nama-backend.koyeb.app/docs
```

#### C. Seed Database Production

Setelah backend sudah memakai database Supabase, seed data awal dapat dijalankan dari lokal dengan env `DATABASE_URL` Supabase.

PowerShell:

```powershell
cd D:\GITHUB\artificial-education\backend
$env:DATABASE_URL="connection-string-supabase"
..\.venv\Scripts\python.exe seed_full.py
```

CMD:

```cmd
cd /d D:\GITHUB\artificial-education\backend
set DATABASE_URL=connection-string-supabase
D:\GITHUB\artificial-education\.venv\Scripts\python.exe seed_full.py
```

#### D. Build Frontend untuk Hostinger

Buat file `frontend/.env.production`:

```text
VITE_API_BASE_URL=https://nama-backend.koyeb.app/api
```

Lalu build frontend:

```cmd
cd /d D:\GITHUB\artificial-education\frontend
npm run build
```

Upload isi folder berikut ke `public_html` Hostinger:

```text
frontend/dist/
```

File `.htaccess` untuk Vue Router sudah disiapkan di `frontend/public/.htaccess` dan akan ikut masuk ke hasil build.

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

Catatan rancangan: pre test dipakai sebagai initial state mahasiswa di awal modul, quiz subtopik memperbarui state subtopik dan Q-Learning sekaligus menjadi sinyal training Neural GKT, sedangkan post test dipakai sebagai target evaluasi akhir. Model Neural GKT saat ini dilatih dari kombinasi data seed, data sintetis, dan hasil assessment yang sudah tersimpan.

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
│ Neural GKT Engine│  │  Q-Learning Agent│
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
