# pilot readiness checklist

Dokumen ini dipakai sebagai pegangan sebelum aplikasi dipakai demo ke dosen atau uji coba ke mahasiswa.

## status machine learning yang aman diklaim

Yang sudah berjalan:

- neural gkt bootstrap untuk adaptasi level topik/modul.
- q-learning untuk adaptasi level subtopik.
- update q-value memakai persamaan bellman setiap mahasiswa menjawab pre test, quiz, drill, atau post test.
- state q-learning memakai mastery, riwayat gagal terbaru, dan cognitive profile.
- neural gkt trainable untuk memprediksi state penguasaan modul dari pre test, quiz, post test, data seed, data sintetis, dan graph prasyarat.
- pre test menjadi initial assessment pada awal modul.
- post test menjadi evaluasi akhir modul.

Yang belum boleh diklaim penuh:

- neural gkt sudah aktif, tetapi model saat ini masih bootstrap karena data nyata masih sedikit.
- hasil training awal memakai campuran data seed, data nyata, dan data sintetis.
- neural gkt baru layak diklaim tervalidasi penuh setelah ada data interaksi mahasiswa nyata yang cukup untuk training dan evaluasi.

Kalimat aman untuk demo:

> untuk saat ini neural gkt sudah berjalan pada level topik/modul dengan data seed, data sintetis, dan hasil pre test, quiz, serta post test sebagai data training awal. q-learning tetap dipakai pada level subtopik untuk memilih strategi belajar dan memperbarui q-value dengan persamaan bellman. karena data mahasiswa nyata masih sedikit, neural gkt ini masih tahap bootstrap dan perlu divalidasi lagi setelah uji coba kelas.

## training neural gkt

Script training:

```cmd
cd /d D:\GITHUB\artificial-education\backend
D:\GITHUB\artificial-education\.venv\Scripts\python.exe scripts\train_neural_gkt.py
```

Output model tersimpan di:

```text
backend\storage\neural_gkt_model.json
```

Hasil training terakhir:

| metrik | nilai |
| --- | ---: |
| trained samples | 761 |
| seed samples | 9 |
| real samples | 32 |
| synthetic samples | 720 |
| MAE | 0.1216 |
| RMSE | 0.1480 |
| accuracy at 60% threshold | 0.8292 |

Catatan: angka ini cocok untuk demo teknis awal, tetapi belum boleh dianggap hasil penelitian final karena data nyata masih sedikit.

## hasil smoke test terakhir

Smoke test akun baru dijalankan lewat `backend/scripts/pilot_smoke_test.py`.

Hasil terakhir:

| area | hasil |
| --- | --- |
| akun baru | berhasil dibuat |
| cognitive profile | berhasil dikirim |
| modul 1 | pre test 5 soal, quiz 10 soal, post test 5 soal, status completed |
| modul 2 | pre test 5 soal, quiz 10 soal, post test 5 soal, status completed |
| modul 3 | pre test 5 soal, quiz 10 soal, post test 5 soal, status completed |
| interaction log | 50 interaksi tercatat |

Command:

```cmd
cd /d D:\GITHUB\artificial-education\backend
D:\GITHUB\artificial-education\.venv\Scripts\python.exe scripts\pilot_smoke_test.py
```

## checklist testing manual akun baru

Gunakan akun mahasiswa baru agar hasilnya bersih.

1. register akun mahasiswa baru.
2. login dengan akun tersebut.
3. buka profil kognitif.
4. isi semua instrumen skala 1 sampai 5.
5. pastikan profil kognitif terkunci setelah dikirim.
6. masuk dashboard.
7. pastikan modul 1 terbuka dan modul berikutnya masih terkunci.
8. klik modul 1.
9. kerjakan pre test modul 1.
10. pastikan subtopik 1 terbuka setelah pre test selesai.
11. buka saran belajar.
12. untuk demo dosen, aktifkan detail teknis dengan `localStorage.setItem('demo_debug','1')`.
13. kerjakan quiz subtopik 1.
14. pastikan q-value berubah di detail teknis.
15. pastikan subtopik 2 terbuka dan subtopik jauh belum ikut terbuka.
16. lanjutkan quiz sampai subtopik terakhir.
17. kerjakan post test modul 1.
18. pastikan rapor modul muncul.
19. jika lulus, pastikan modul 2 terbuka.
20. ulangi alur singkat sampai modul 2 atau 3 untuk demo lengkap.

## checklist tampilan mobile dan laptop

Viewport minimal yang harus dicek sebelum demo:

| perangkat | ukuran cek | fokus pengecekan |
| --- | --- | --- |
| laptop dosen kecil | 1366 x 768 | dashboard tidak kepotong, sidebar bisa dipakai, drill/assessment nyaman |
| laptop standar | 1440 x 900 | layout utama seimbang, modul dan rekomendasi tidak saling menekan |
| tablet | 768 x 1024 | panel bisa scroll, tombol utama tetap terlihat |
| mobile | 390 x 844 | tidak ada teks keluar container, assessment tetap bisa dijawab |

Bagian yang wajib dicek visual:

- login dan register.
- cognitive profile.
- dashboard awal sebelum memilih modul.
- modul viewer.
- pre test, quiz, drill, dan post test.
- rapor modul.
- profil mahasiswa.
- leaderboard/gamification.
- admin graph, soal, dan materi.

## copywriting dan debug

Aturan tampilan mahasiswa:

- jangan tampilkan istilah q-value, bellman, neural gkt, atau debug secara default.
- gunakan kata sederhana seperti saran belajar, progress, latihan, evaluasi, dan rekomendasi.
- detail teknis hanya untuk admin atau mode demo dosen.

Mode debug:

```js
localStorage.setItem('demo_debug', '1')
location.reload()
```

Matikan mode debug:

```js
localStorage.removeItem('demo_debug')
location.reload()
```

## validasi soal oleh dosen

Kualitas soal berpengaruh langsung ke reward, mastery, dan q-value. Jadi sebelum uji coba kelas, soal perlu divalidasi dosen.

Checklist validasi setiap soal:

| aspek | pertanyaan cek |
| --- | --- |
| kesesuaian subtopik | apakah soal benar-benar mengukur subtopik yang dipilih? |
| tipe assessment | apakah soal cocok untuk pre test, quiz, drill, atau post test? |
| jawaban benar | apakah kunci jawabannya tidak ambigu? |
| distraktor | apakah opsi salah masuk akal dan tidak terlalu mudah ditebak? |
| tingkat kesulitan | apakah difficulty sesuai: mudah, sedang, atau sulit? |
| duplikasi | apakah soal berbeda dari pre test, quiz, dan post test lain? |
| bahasa | apakah kalimat mudah dipahami mahasiswa? |
| dampak q-value | apakah benar/salah pada soal ini memang mencerminkan penguasaan materi? |

## kebijakan reset akun dan data uji coba

Untuk uji coba kelas, data mahasiswa jangan dihapus manual dari banyak tabel karena ada foreign key. Gunakan endpoint reset learning data.

Endpoint:

```http
POST /api/admin/users/{user_id}/reset-learning-data
```

Yang direset:

- assessment attempts dan jawaban.
- interaction logs.
- q-values.
- knowledge states.
- cognitive profile dan jawaban instrumen.
- progress mastery.
- xp, streak, combo, skor, reward points, dan redeemed rewards.

Yang tidak dihapus:

- akun user.
- data modul.
- materi.
- soal.
- graph prasyarat.

Kapan dipakai:

- sebelum mahasiswa mencoba ulang dari awal.
- sebelum demo kedua dengan akun yang sama.
- setelah uji coba internal yang datanya tidak mau dipakai untuk analisis.

Untuk data penelitian asli, jangan reset sebelum data diekspor.

## aturan kelulusan modul

Modul berikutnya terbuka jika modul sebelumnya sudah memenuhi syarat:

- pre test sudah dikerjakan sebagai initial assessment.
- quiz subtopik sudah diselesaikan.
- post test modul sudah selesai.
- rata-rata mastery subtopik mencapai batas kelulusan.

Bobot mastery yang dipakai sekarang:

| aktivitas | benar | salah |
| --- | ---: | ---: |
| pre test | +8 | -3 |
| quiz | +18 | -8 |
| post test | +20 | -10 |
| drill | +6 | -4 |

Bobot ini membuat mahasiswa tidak cukup hanya membuka materi. Mereka perlu menjawab assessment dengan benar agar mastery dan q-value naik.
