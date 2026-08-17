# uji model machine learning learning path adaptif

Tanggal uji: 11-08-2026 08:32 WIB

## tujuan
Pengujian ini dipakai untuk membuktikan bahwa bagian machine learning tidak hanya tampil di antarmuka, tetapi menghasilkan prediksi dan pembaruan nilai. Model yang diuji adalah neural GKT untuk prediksi level modul/topik dan q-learning untuk rekomendasi belajar level subtopik.

## data uji
- Data sintetis: 120 mahasiswa sintetis
- Jumlah sampel neural GKT bootstrap: 1800 sampel
- Model tersimpan: 761 sampel training (9 seed, 32 real, 720 sintetis)

## hasil neural GKT
| Model | Accuracy | Precision | Recall | F1 | MAE | RMSE |
|---|---:|---:|---:|---:|---:|---:|
| Baseline tanpa graph | 0.6917 | 0.715 | 0.6532 | 0.6827 | 0.3699 | 0.4589 |
| Neural GKT bootstrap | 0.695 | 0.7355 | 0.6236 | 0.675 | 0.3757 | 0.4498 |
| Model tersimpan | 0.8292 | - | - | - | 0.1216 | 0.148 |

## hasil q-learning
| Policy | Mean final mastery | Pass rate 60% |
|---|---:|---:|
| Q-learning adaptif | 0.9033 | 0.9083 |
| Random baseline | 0.8527 | 0.8417 |

Kenaikan q-learning terhadap random baseline: mastery +0.0506 dan pass rate +0.0666.

## uji skenario prediksi neural GKT
| ID | Skenario | Expected | Actual | Status |
|---|---|---|---|---|
| GKT-01 | mahasiswa mulai modul 1, tidak ada prasyarat | continue ke mod-001 | continue ke mod-001 | PASS |
| GKT-02 | modul 2 dengan prasyarat modul 1 kuat | continue ke mod-002 | continue ke mod-002 | PASS |
| GKT-03 | modul 2 tetapi modul 1 lemah | back trace ke mod-001 | back trace ke mod-001 | PASS |
| GKT-04 | modul 3 tetapi modul 2 lemah | back trace ke mod-002 | back trace ke mod-002 | PASS |

## uji rumus Bellman q-learning
| ID | Kondisi | Expected Q baru | Actual Q baru | Status |
|---|---|---:|---:|---|
| QL-01 | Q=0, reward=100, next max=0 | 10.00 | 10.00 | PASS |
| QL-02 | Q=10, reward=50, next max=20 | 15.80 | 15.80 | PASS |
| QL-03 | Q=15, reward=-10, next max=0 | 12.50 | 12.50 | PASS |

## kesimpulan
Pengujian menunjukkan bahwa neural GKT sudah dapat menghasilkan keputusan continue atau back trace sesuai kondisi prasyarat, sedangkan q-learning sudah memperbarui q-value sesuai persamaan Bellman. Hasil simulasi juga menunjukkan q-learning adaptif memberi capaian mastery dan pass rate lebih tinggi dibanding random baseline. Untuk klaim penelitian, hasil ini masih dapat disebut sebagai uji awal berbasis data sintetis, sedangkan validasi akurasi final tetap perlu data interaksi mahasiswa asli.
