# Product Requirements Document (PRD)
> **Project Name:** Artificial Education (Adaptive ITS)
> **Version:** 1.0.0
> **Status:** Active Research / Development
> **Pilot Project:** Mata Kuliah Algoritma dan Pemrograman

## 1. Ringkasan Eksekutif
Artificial Education adalah *Intelligent Tutoring System* (ITS) yang dirancang untuk memberikan pengalaman belajar mandiri yang adaptif. Sistem ini menggunakan model *Machine Learning Hybrid* untuk mengevaluasi tingkat pemahaman pengguna secara *real-time* dan menyusun *learning path* yang dipersonalisasi.

## 2. Latar Belakang & Masalah
Dalam pembelajaran ilmu komputer yang berjenjang, kegagalan pemahaman pada konsep lanjutan (misalnya: Perulangan / Looping) sering kali berakar dari lemahnya pemahaman pada konsep prasyarat fondasinya (misalnya: Variabel dan Percabangan / If-Else). Sistem e-learning konvensional umumnya kaku; mereka hanya memaksa pengulangan pada bab yang gagal tanpa mendiagnosis akar masalah. Dibutuhkan sistem cerdas yang mampu mendiagnosis rantai prasyarat tersebut.

## 3. Visi Produk
Membangun ekosistem belajar yang tidak hanya "menilai", tetapi "mendiagnosis dan mengobati" kelemahan kognitif pengguna melalui intervensi AI tingkat makro (Topik) dan mikro (Sub-Topik).

## 4. Persona Pengguna
* **Mahasiswa Ilmu Komputer:** Pengguna utama (End-User) yang akan berinteraksi dengan materi, asisten chatbot, dan mengerjakan soal *drill*.
* **Dosen / Peneliti:** Pengguna manajerial yang memantau pergerakan *Graph* pemahaman mahasiswa dan mengevaluasi konvergensi nilai Q-Learning pada sistem.

## 5. Fitur Utama
1. **Adaptive Module Viewer:** Menampilkan materi teks/video secara dinamis sesuai rekomendasi AI.
2. **Macro-Level Tracing (GKT Engine):** Algoritma yang memetakan keterkaitan prasyarat antar modul. Mampu melakukan propagasi mundur ke modul dasar jika skor pemahaman lanjutan turun drastis.
3. **Micro-Level Pathing (Q-Learning Agent):** Agen AI yang menentukan aksi spesifik selanjutnya (Misal: berikan teks, berikan video, atau berikan kuis) di dalam sebuah sub-topik.
4. **Interactive Drill & Practice:** Area kuis (*flashcard-style*) yang berfungsi sebagai *environment* pengumpul *reward* untuk pembaruan skor Bellman.
5. **Mastery Radar Tracker:** Visualisasi *real-time* tingkat pemahaman mahasiswa per topik dalam bentuk *Radar Chart*.
6. **AI Chatbot Assistant:** Asisten virtual kontekstual untuk menjawab keraguan materi *on-the-fly*.

## 6. Metrik Keberhasilan (Success Metrics)
* Peningkatan akurasi diagnosis pemahaman mahasiswa (*Knowledge Tracing Accuracy*).
* Tercapainya konvergensi *reward* yang stabil pada *Q-Table* seiring bertambahnya iterasi pengguna.
* Penurunan waktu rata-rata (efisiensi) mahasiswa untuk mencapai penguasaan modul (*Mastery Level*).
