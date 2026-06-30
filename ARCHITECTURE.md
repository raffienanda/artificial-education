# System Architecture & Technical Specifications

## 1. Tech Stack Overview
* **Frontend:** Vue.js (Vite), Tailwind CSS, Pinia (State Management)
* **Backend:** Python (FastAPI) - Dipilih karena efisiensi *routing* asinkron dan integrasi *native* dengan ekosistem Machine Learning.
* **Database:** PostgreSQL (Relational Database) - Esensial untuk integritas struktural *Graph* relasi dan pencatatan *log* transaksional.
* **AI / ML Engine:** PyTorch / PyTorch Geometric (Untuk GKT) & Custom Reinforcement Learning Environment (Untuk Q-Learning).

## 2. High-Level Architecture
Sistem mengadopsi arsitektur *Client-Server* dengan pemisahan *logic* kecerdasan buatan:
1. **Vue.js Client:** Menangani UI/UX, merender *State* saat ini, dan mengirim objek *Action* mahasiswa melalui HTTP Requests.
2. **FastAPI Backend:** Bertindak sebagai *API Gateway*, memproses *business logic*, dan melakukan *Read/Write* ke *Database*.
3. **AI Core Service (Python):** * Menerima *log* interaksi mentah.
   * Memperbarui Q-Value menggunakan persamaan Bellman.
   * Melakukan *Graph Traversal* untuk menentukan status ketuntasan (*Knowledge State*).

## 3. Skema AI Hybrid
### A. Graph Knowledge Tracing (GKT) - *Macro Layer*
Beroperasi pada level Topik Utama (Modul).
* **Node:** Topik / Modul (Contoh: "Percabangan", "Perulangan", "Array").
* **Edge:** Hubungan prasyarat (Contoh: "Percabangan" $ightarrow$ "Perulangan").
* **Logic:** Jika skor *Mastery* pada *node* "Array" berada di bawah *threshold* kritis, model melakukan *back-tracking* melintasi *edge* menuju *node* prasyarat ("Perulangan") untuk mewajibkan evaluasi ulang fondasi.

### B. Q-Learning - *Micro Layer*
Beroperasi pada level Sub-Topik (Materi Spesifik).
* **State (S):** Tingkat penguasaan dan riwayat kegagalan mahasiswa saat ini di suatu sub-topik.
* **Action (A):** Menyajikan Teks (A1), Video Penjelasan (A2), atau Kuis Drill (A3).
* **Reward (R):** +100 untuk jawaban kuis benar pertama kali, -10 untuk jawaban salah (penalti ketidaktuntasan).
* **Update Rule:** $Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max Q(s',a') - Q(s,a)]$

## 4. Skema Database Inti (PostgreSQL Relational Schema)
* **`users`**: `id` (PK), `nim`, `nama`, `created_at`
* **`topik_gkt`**: `id` (PK), `judul_topik`, `deskripsi_topik`
* **`relasi_prasyarat`**: `id` (PK), `topik_tujuan_id` (FK), `prasyarat_id` (FK)
* **`sub_topik_ql`**: `id` (PK), `topik_id` (FK), `tipe_konten` (Enum), `isi_konten`
* **`log_interaksi`**: `id` (PK), `user_id` (FK), `sub_topik_id` (FK), `skor_evaluasi`, `durasi_interaksi_detik`, `timestamp`
