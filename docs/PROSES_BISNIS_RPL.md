# Gambaran Umum

Melalui aplikasi learning path adaptif ini, mahasiswa dapat belajar secara bertahap sesuai kemampuan awal, perkembangan belajar, dan hasil evaluasi yang mereka peroleh selama menggunakan aplikasi. Sistem tidak hanya menampilkan materi pembelajaran, tetapi juga membantu mengatur urutan belajar, membuka atau mengunci modul, memberi saran belajar, dan menampilkan rapor setelah mahasiswa menyelesaikan satu modul.

Secara garis besar, alur penggunaan aplikasi dimulai dari mahasiswa melakukan registrasi atau login. Setelah itu mahasiswa mengisi profil kognitif, memilih mata kuliah, lalu memilih modul yang tersedia. Pada awal modul, mahasiswa mengerjakan pre test untuk mengetahui kemampuan awal. Setelah pre test selesai, mahasiswa dapat mempelajari materi subtopik, mengerjakan quiz subtopik, dan menyelesaikan post test pada akhir modul.

Bagian adaptif pada aplikasi ini dibantu oleh Neural GKT dan Q-learning. Neural GKT digunakan pada level modul/topik untuk membantu membaca kesiapan mahasiswa berdasarkan graph prasyarat, hasil pre test, quiz, post test, dan interaksi belajar. Sementara itu, Q-learning digunakan pada level subtopik untuk memberi saran belajar seperti ringkasan materi, video, latihan, atau review. Setelah mahasiswa menjawab quiz, sistem menghitung reward dan memperbarui q-value menggunakan persamaan Bellman.

# User Yang Terlibat

| User | Peran |
|---|---|
| Mahasiswa | Menggunakan aplikasi untuk belajar, mengisi profil kognitif, memilih mata kuliah dan modul, mengerjakan pre test, quiz subtopik, drill soal, post test, serta melihat rapor modul. |
| Admin | Mengelola data pembelajaran seperti mata kuliah, modul, subtopik, materi, soal, dan graph prasyarat. |

# Proses Bisnis Utama

| No | Aktivitas | Aktor | Proses Sistem | Output |
|---|---|---|---|---|
| 1 | Register atau login | Mahasiswa | Sistem memvalidasi akun dan membuat sesi pengguna. | Mahasiswa masuk ke aplikasi. |
| 2 | Mengisi profil kognitif | Mahasiswa | Sistem menyimpan hasil instrumen sebagai konteks personal mahasiswa. | Profil kognitif tersimpan dan dikunci. |
| 3 | Memilih mata kuliah | Mahasiswa | Sistem menampilkan daftar modul berdasarkan mata kuliah yang dipilih. | Learning path mata kuliah tampil. |
| 4 | Memilih modul | Mahasiswa | Sistem mengecek prasyarat modul menggunakan graph prasyarat dan Neural GKT. | Modul terbuka atau tetap terkunci. |
| 5 | Mengerjakan pre test | Mahasiswa | Sistem menilai kemampuan awal mahasiswa dan membentuk initial state. | Kemampuan awal mahasiswa terbaca. |
| 6 | Mempelajari materi subtopik | Mahasiswa | Sistem menampilkan materi sesuai subtopik yang sedang terbuka. | Mahasiswa belajar sesuai urutan. |
| 7 | Menerima saran belajar | Mahasiswa | Q-learning menentukan saran belajar yang paling sesuai. | Saran belajar tampil ke mahasiswa. |
| 8 | Mengerjakan quiz subtopik | Mahasiswa | Sistem memeriksa jawaban dan menghitung reward. | Nilai quiz dan reward diperoleh. |
| 9 | Update q-value | Sistem | Q-learning memperbarui q-value menggunakan persamaan Bellman. | Q-value baru tersimpan. |
| 10 | Menentukan kelulusan quiz | Sistem | Sistem mengecek apakah quiz subtopik sudah lulus. | Lanjut subtopik berikutnya atau review. |
| 11 | Mengerjakan post test | Mahasiswa | Sistem mengevaluasi penguasaan akhir modul. | Skor post test tersimpan. |
| 12 | Membuat rapor diagnosis | Sistem | Sistem mengolah pre test, quiz, post test, q-value, progress, dan profil kognitif. | Learning diagnosis report tampil. |
| 13 | Menentukan rekomendasi akhir | Sistem | Sistem menentukan apakah mahasiswa dapat lanjut modul atau perlu penguatan. | Lanjut modul, review ringan, latihan tambahan, atau pendampingan. |

# Alur Sistem

1. Mahasiswa melakukan register atau login.
2. Mahasiswa mengisi profil kognitif.
3. Mahasiswa memilih mata kuliah.
4. Mahasiswa memilih modul yang tersedia.
5. Sistem memeriksa prasyarat modul menggunakan graph prasyarat dan Neural GKT.
6. Jika prasyarat terpenuhi, mahasiswa mengerjakan pre test.
7. Setelah pre test selesai, materi subtopik pertama dibuka.
8. Sistem menampilkan saran belajar berdasarkan Q-learning.
9. Mahasiswa mempelajari materi dan mengerjakan quiz subtopik.
10. Sistem menghitung reward dan memperbarui q-value menggunakan persamaan Bellman.
11. Jika quiz lulus, mahasiswa lanjut ke subtopik berikutnya.
12. Setelah semua subtopik selesai, mahasiswa mengerjakan post test.
13. Sistem membuat learning diagnosis report.
14. Sistem memberikan rekomendasi akhir dan menentukan apakah modul berikutnya terbuka.

# Komponen Internal Sistem

| Komponen | Fungsi |
|---|---|
| Graph Prasyarat | Menyimpan hubungan ketergantungan antar modul agar mahasiswa tidak langsung melompat ke materi lanjutan sebelum memahami materi dasar. |
| Neural GKT | Membantu membaca pola penguasaan mahasiswa pada level modul/topik dengan mempertimbangkan graph prasyarat, pre test, quiz, post test, dan interaksi belajar. |
| Q-learning | Menentukan saran belajar pada level subtopik dan memperbarui q-value berdasarkan reward dari hasil quiz. |
| Learning Diagnosis Report | Menggabungkan hasil pre test, quiz, post test, q-value, progress, dan profil kognitif untuk membuat rekomendasi akhir modul. |

# Data yang Dihasilkan dari Proses Bisnis

| Data | Sumber | Kegunaan |
|---|---|---|
| Data akun mahasiswa | Register/Login | Menyimpan progress pengguna. |
| Profil kognitif | Instrumen profil kognitif | Menjadi konteks personal dalam rekomendasi belajar. |
| Nilai pre test | Awal modul | Membaca kemampuan awal mahasiswa. |
| Aktivitas materi | Interaksi belajar | Membantu membaca strategi belajar yang dipilih mahasiswa. |
| Nilai quiz subtopik | Evaluasi subtopik | Menjadi reward untuk update q-value. |
| Q-value | Proses Q-learning | Menentukan strategi belajar yang lebih sesuai. |
| Nilai post test | Akhir modul | Mengevaluasi penguasaan akhir modul. |
| Learning diagnosis report | Gabungan hasil belajar | Menjadi dasar rekomendasi akhir modul. |

# Diagram

Diagram alur sistem learning path adaptif digunakan untuk menunjukkan urutan proses dari login/register sampai mahasiswa mendapatkan rekomendasi akhir. Diagram ini membantu menjelaskan posisi graph prasyarat atau Neural GKT pada level modul, serta Q-learning pada level subtopik.
