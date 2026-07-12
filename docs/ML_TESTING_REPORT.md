# dokumen testing machine learning learning path

## 1. tujuan pengujian

Dokumen ini dibuat untuk menguji apakah komponen machine learning pada aplikasi learning path sudah berjalan secara logis dan dapat dibuktikan dengan data. Komponen yang diuji adalah:

1. neural gkt / graph knowledge tracing proxy untuk membaca state awal dan hubungan prasyarat antar modul.
2. q-learning untuk memilih strategi belajar pada level subtopik dan memperbarui q-value menggunakan persamaan bellman.

Catatan penting: data pada dokumen ini masih memakai data sintetis, bukan data mahasiswa nyata. Jadi angka akurasi di sini belum boleh dianggap sebagai akurasi final penelitian, tetapi bisa dipakai sebagai bukti awal bahwa mekanisme model sudah bisa diuji dan dievaluasi.

## 2. posisi implementasi saat ini

Pada aplikasi saat ini, neural gkt penuh belum dilatih dengan neural network karena belum tersedia data interaksi mahasiswa nyata dalam jumlah cukup. Namun struktur data untuk menuju neural gkt sudah disiapkan melalui:

- `knowledge_edges`: menyimpan hubungan prasyarat antar modul.
- `knowledge_states`: menyimpan estimasi penguasaan mahasiswa pada node modul/subtopik.
- `pre_test`: dipakai sebagai initial state sebelum mahasiswa membuka materi.
- `quiz` dan `post_test`: dipakai untuk memperbarui knowledge state setelah mahasiswa belajar.

Untuk q-learning, implementasi sudah berjalan langsung di aplikasi. Q-value diperbarui setelah mahasiswa menjawab assessment dengan rumus Bellman:

```text
Q(s,a) = Q(s,a) + alpha * (reward + gamma * max Q(s',a') - Q(s,a))
```

Dengan arti:

- `s`: state mahasiswa sekarang, misalnya `low:stable:multiplicity`.
- `a`: aksi belajar, misalnya `show_text`, `show_video`, `easy_quiz`, `drill`, atau `post_test`.
- `reward`: nilai dari hasil jawaban mahasiswa.
- `s'`: state mahasiswa setelah menjawab.
- `alpha`: learning rate.
- `gamma`: discount factor.

## 3. data testing

Karena data mahasiswa nyata belum tersedia, pengujian awal memakai data sintetis yang dibuat dengan script:

```text
backend/scripts/synthetic_ml_evaluation.py
```

Output data berada di:

```text
docs/evaluation/synthetic_interactions.csv
docs/evaluation/synthetic_q_learning_interactions.csv
docs/evaluation/metrics_summary.json
```

Konfigurasi data sintetis:

| item | nilai |
|---|---:|
| jumlah mahasiswa sintetis | 120 |
| jumlah modul | 3 |
| jumlah subtopik | 15 |
| jumlah sample testing gkt proxy | 1800 |
| random seed | 20260709 |

Data sintetis dibuat dengan asumsi setiap mahasiswa memiliki kemampuan awal berbeda, cognitive stage berbeda, dan preferensi strategi belajar berbeda. Pre test digunakan sebagai state awal, lalu quiz dan post test digunakan untuk mengukur perubahan performa.

## 4. skenario pengujian neural gkt proxy

Karena neural gkt penuh belum dilatih, pengujian dilakukan sebagai proxy graph knowledge tracing. Tujuannya adalah mengukur apakah informasi graph prasyarat membantu prediksi penguasaan dibanding hanya memakai pre test modul itu sendiri.

Model yang dibandingkan:

| model | penjelasan |
|---|---|
| baseline tanpa graph | prediksi hanya memakai skor pre test modul terkait |
| gkt graph proxy | prediksi memakai pre test modul terkait + sinyal modul prasyarat |

Hasil evaluasi:

| metrik | baseline tanpa graph | gkt graph proxy |
|---|---:|---:|
| accuracy | 0.6917 | 0.6950 |
| precision | 0.7150 | 0.7355 |
| recall | 0.6532 | 0.6236 |
| f1-score | 0.6827 | 0.6750 |
| mae | 0.3699 | 0.3757 |
| rmse | 0.4589 | 0.4498 |

Interpretasi:

GKT graph proxy memberi peningkatan kecil pada accuracy dan precision, dari 69.17% menjadi 69.50%, serta menurunkan RMSE dari 0.4589 menjadi 0.4498. Artinya, sinyal graph prasyarat mulai membantu prediksi, tetapi belum dominan. Ini wajar karena data masih sintetis dan model belum neural penuh.

Hasil ini bisa dijelaskan ke dosen sebagai tahap awal bahwa graph prasyarat sudah dapat dimasukkan ke proses prediksi knowledge state, lalu nanti bisa dikembangkan menjadi neural gkt penuh ketika data interaksi mahasiswa sudah terkumpul.

## 5. skenario pengujian q-learning

Q-learning diuji dengan membandingkan dua kebijakan:

| policy | penjelasan |
|---|---|
| random policy | strategi belajar dipilih acak |
| q-learning adaptive policy | strategi dipilih berdasarkan q-value yang dipelajari |

Strategi belajar yang diuji:

- `show_text`
- `show_video`
- `easy_quiz`
- `hard_quiz`
- `review_previous`

Reward diberikan berdasarkan benar/salah jawaban, perubahan mastery, dan kesesuaian aksi dengan kondisi mahasiswa. Simulasi dilakukan selama 18 episode belajar per mahasiswa.

Hasil evaluasi:

| metrik | random policy | q-learning adaptive |
|---|---:|---:|
| rata-rata final mastery | 0.8527 | 0.9033 |
| pass rate minimal 60% | 0.8417 | 0.9083 |
| peningkatan mastery | - | +0.0506 |
| peningkatan pass rate | - | +0.0666 |

Interpretasi:

Pada data sintetis, q-learning adaptive menghasilkan rata-rata mastery akhir 90.33%, lebih tinggi dari random policy 85.27%. Pass rate juga naik dari 84.17% menjadi 90.83%. Ini menunjukkan bahwa strategi adaptif berbasis q-value lebih efektif dibanding memilih strategi belajar secara acak.

## 6. validasi rumus bellman

Selain simulasi, rumus Bellman juga diuji dengan hitungan manual.

Contoh:

```text
current_q = 10
reward = 100
next_max_q = 20
alpha = 0.1
gamma = 0.9

Q baru = 10 + 0.1 * (100 + 0.9 * 20 - 10)
Q baru = 20.8
```

Hasil fungsi aplikasi:

```text
expected = 20.8
actual   = 20.8
status   = pass
```

Artinya, update q-value di aplikasi sudah sesuai dengan persamaan Bellman.

## 7. batasan pengujian

Ada beberapa batasan yang harus dijelaskan secara jujur:

1. Data yang dipakai masih sintetis, belum berasal dari mahasiswa nyata.
2. Neural GKT penuh belum dilatih sebagai neural network karena butuh data historis interaksi mahasiswa.
3. Hasil GKT saat ini lebih tepat disebut graph knowledge tracing proxy atau neural gkt readiness test.
4. Reward q-learning masih berbasis desain heuristik, sehingga nanti perlu tuning setelah ada data nyata.
5. Akurasi model bisa berubah ketika jumlah mahasiswa, kualitas soal, dan pola belajar nyata mulai masuk.

## 8. kesimpulan sementara

Berdasarkan testing sintetis, q-learning sudah terbukti berjalan dan memberi peningkatan performa dibanding random policy. Update q-value juga sudah sesuai dengan persamaan Bellman. Untuk neural gkt, struktur data dan mekanisme graph sudah siap, tetapi akurasi yang diuji saat ini masih berupa proxy karena belum ada data mahasiswa nyata untuk training neural model penuh.

Kalimat aman untuk laporan:

> Pada tahap ini, aplikasi sudah menerapkan q-learning untuk adaptasi strategi belajar subtopik dengan update q-value menggunakan persamaan Bellman. Evaluasi awal menggunakan data sintetis menunjukkan q-learning adaptive menghasilkan mastery dan pass rate lebih baik dibanding random policy. Untuk bagian neural gkt, sistem sudah menyiapkan graph prasyarat dan knowledge state berbasis pre test sebagai initial state. Namun neural gkt penuh masih membutuhkan data interaksi mahasiswa nyata agar dapat dilatih dan dievaluasi lebih valid.

## 9. rencana pengujian lanjutan

Langkah berikutnya agar hasilnya lebih kuat:

1. Kumpulkan data mahasiswa nyata dari pre test, quiz, drill, dan post test.
2. Bandingkan rekomendasi sistem dengan hasil belajar aktual mahasiswa.
3. Tuning reward q-learning berdasarkan korelasi dengan peningkatan post test.
4. Latih model neural gkt penuh ketika data interaksi sudah cukup.
5. Evaluasi ulang dengan metrik accuracy, f1-score, MAE, RMSE, dan learning gain.
