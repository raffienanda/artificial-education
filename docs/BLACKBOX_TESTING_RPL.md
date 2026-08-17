# Gambaran Umum

Uji blackbox dilakukan untuk memastikan fitur-fitur pada aplikasi learning path adaptif berjalan sesuai kebutuhan pengguna. Pengujian ini tidak melihat isi kode program, tetapi berfokus pada tindakan pengguna, input yang diberikan, dan hasil yang ditampilkan oleh sistem.

Pada aplikasi ini, pengujian dilakukan mulai dari proses register dan login, pengisian profil kognitif, pemilihan mata kuliah, akses modul, pre test, materi subtopik, quiz, drill soal, post test, rapor modul, sampai fitur admin. Dengan pengujian ini, sistem dapat dibuktikan sudah berjalan sesuai alur yang dirancang.

Hasil uji blackbox juga dapat digunakan sebagai data pendukung pada laporan atau paper. Data ini menunjukkan bahwa aplikasi sudah diuji dari sisi fungsional, terutama pada bagian learning path adaptif, lock/unlock modul, update q-value, dan rekomendasi belajar.

# Lingkup Pengujian

1. Register dan login pengguna.
2. Pengisian profil kognitif.
3. Pemilihan mata kuliah dan modul.
4. Lock dan unlock modul berdasarkan prasyarat.
5. Pre test modul.
6. Akses materi subtopik.
7. Quiz subtopik.
8. Drill soal.
9. Update q-value berdasarkan jawaban quiz.
10. Post test modul.
11. Learning diagnosis report.
12. Profil mahasiswa, leaderboard, reward, dan chatbot.
13. Pengelolaan graph prasyarat, soal, dan materi oleh admin.
14. Validasi akses halaman dan data.

# Lingkungan Pengujian

| Komponen | Keterangan |
|---|---|
| Frontend | Vue.js + Vite |
| Backend | FastAPI |
| Database | PostgreSQL |
| Browser | Google Chrome / Microsoft Edge |
| Metode | Blackbox testing |
| Penguji | Pengguna aplikasi / peneliti |

# Kriteria Status

| Status | Keterangan |
|---|---|
| Valid | Hasil aktual sesuai dengan hasil yang diharapkan. |
| Tidak Valid | Hasil aktual tidak sesuai dengan hasil yang diharapkan. |
| Perlu Perbaikan | Fitur berjalan, tetapi masih ada kekurangan tampilan, validasi, atau alur. |

# Tabel Hasil Uji Blackbox

| Kode | Fitur | Skenario Pengujian | Input / Aksi | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|---|---|---|---|---|---|
| TC-001 | Register | Mahasiswa membuat akun baru dengan data valid. | Isi username, password, dan nama tampilan, lalu klik daftar. | Akun berhasil dibuat dan pengguna masuk ke dashboard. | Sistem berhasil membuat akun dan masuk ke dashboard. | Valid |
| TC-002 | Register | Mahasiswa membuat akun dengan username yang sudah digunakan. | Isi username yang sudah terdaftar. | Sistem menolak register dan menampilkan pesan error. | Sistem menampilkan pesan bahwa username sudah digunakan. | Valid |
| TC-003 | Login | Mahasiswa login dengan akun valid. | Isi username dan password benar. | Sistem menerima login dan membuka dashboard. | Sistem berhasil login dan membuka dashboard. | Valid |
| TC-004 | Login | Mahasiswa login dengan password salah. | Isi username benar dan password salah. | Sistem menolak login dan menampilkan pesan error. | Sistem menampilkan pesan login gagal. | Valid |
| TC-005 | Logout | Mahasiswa keluar dari aplikasi. | Klik menu logout. | Sesi pengguna berakhir dan kembali ke halaman login. | Sistem menghapus sesi dan mengarahkan ke login. | Valid |
| TC-006 | Proteksi Halaman | Pengguna belum login membuka dashboard. | Akses URL dashboard secara langsung. | Sistem mengarahkan pengguna ke halaman login. | Pengguna diarahkan ke halaman login. | Valid |
| TC-007 | Profil Kognitif | Mahasiswa membuka halaman profil kognitif. | Klik menu Profil Kognitif. | Sistem menampilkan daftar instrumen profil kognitif. | Instrumen profil kognitif tampil. | Valid |
| TC-008 | Profil Kognitif | Mahasiswa mengisi profil kognitif dengan lengkap. | Pilih nilai jawaban semua item lalu submit. | Sistem menyimpan profil dan menampilkan status selesai. | Profil tersimpan dan status menjadi selesai. | Valid |
| TC-009 | Profil Kognitif | Mahasiswa mencoba submit profil kognitif tidak lengkap. | Ada item yang belum dijawab. | Sistem menolak submit atau memberi peringatan. | Sistem meminta semua item dilengkapi. | Valid |
| TC-010 | Profil Kognitif | Mahasiswa mencoba mengubah profil yang sudah dikunci. | Buka kembali profil setelah submit. | Profil tidak dapat diubah lagi. | Sistem menampilkan profil sebagai data yang sudah dikunci. | Valid |
| TC-011 | Mata Kuliah | Mahasiswa membuka dashboard awal. | Login sebagai mahasiswa. | Sistem menampilkan daftar mata kuliah. | Daftar mata kuliah tampil. | Valid |
| TC-012 | Mata Kuliah | Mahasiswa memilih mata kuliah yang memiliki modul. | Klik mata kuliah Algoritma dan Pemrograman. | Sistem menampilkan daftar modul pada mata kuliah tersebut. | Learning path modul tampil. | Valid |
| TC-013 | Mata Kuliah | Mahasiswa memilih mata kuliah tanpa modul. | Klik mata kuliah yang belum memiliki modul. | Sistem menampilkan informasi modul belum tersedia. | Informasi modul belum tersedia tampil. | Valid |
| TC-014 | Learning Path | Mahasiswa baru melihat daftar modul. | Buka dashboard dengan akun baru. | Modul pertama terbuka, modul berikutnya terkunci. | Modul pertama terbuka dan modul lanjutan terkunci. | Valid |
| TC-015 | Lock Modul | Mahasiswa baru mencoba membuka modul kedua. | Klik modul 2 sebelum modul 1 lulus. | Sistem menolak akses dan modul tetap terkunci. | Modul 2 tidak dapat dibuka. | Valid |
| TC-016 | Pre Test | Mahasiswa membuka modul pertama yang belum pre test. | Klik modul 1. | Sistem menampilkan tombol mulai pre test. | Tombol mulai pre test tampil. | Valid |
| TC-017 | Pre Test | Mahasiswa mengerjakan pre test modul. | Jawab semua soal pre test. | Sistem menyimpan nilai pre test dan membuka materi subtopik. | Nilai pre test tersimpan dan materi terbuka. | Valid |
| TC-018 | Pre Test | Mahasiswa mencoba membuka materi sebelum pre test. | Akses materi modul tanpa pre test. | Sistem menolak akses dan mengarahkan ke pre test. | Sistem meminta mahasiswa mengerjakan pre test terlebih dahulu. | Valid |
| TC-019 | Materi Subtopik | Mahasiswa membuka materi subtopik pertama. | Klik modul setelah pre test selesai. | Sistem menampilkan ringkasan, video, dan contoh/latihan sesuai materi. | Materi subtopik tampil. | Valid |
| TC-020 | Navigasi Subtopik | Mahasiswa mencoba membuka subtopik yang belum waktunya. | Klik subtopik lanjutan sebelum quiz sebelumnya lulus. | Sistem menolak akses atau subtopik tetap terkunci. | Subtopik lanjutan tetap terkunci. | Valid |
| TC-021 | Saran Belajar | Sistem menampilkan rekomendasi belajar pada subtopik. | Buka panel saran belajar. | Sistem menampilkan aksi belajar seperti ringkasan, video, latihan, atau review. | Rekomendasi belajar tampil. | Valid |
| TC-022 | Debug Q-value | Penguji membuka mode debug rekomendasi. | Klik tombol Debug. | Sistem menampilkan state, action, q-value, dan informasi adaptif. | Informasi debug tampil. | Valid |
| TC-023 | Quiz Subtopik | Mahasiswa membuka quiz subtopik setelah belajar. | Klik mulai quiz subtopik. | Sistem menampilkan soal quiz sesuai subtopik. | Soal quiz tampil. | Valid |
| TC-024 | Quiz Subtopik | Mahasiswa menjawab quiz dengan benar. | Pilih jawaban benar. | Sistem menampilkan feedback benar dan menghitung reward positif. | Feedback benar tampil dan reward diproses. | Valid |
| TC-025 | Quiz Subtopik | Mahasiswa menjawab quiz dengan salah. | Pilih jawaban salah. | Sistem menampilkan feedback salah dan menghitung reward lebih rendah/negatif. | Feedback salah tampil dan reward diproses. | Valid |
| TC-026 | Q-learning | Mahasiswa menyelesaikan jawaban quiz. | Submit jawaban quiz. | Sistem memperbarui q-value menggunakan persamaan Bellman. | Q-value berubah dan tersimpan pada hasil submit. | Valid |
| TC-027 | Retake Quiz | Mahasiswa mencoba mengulang quiz yang sudah lulus. | Buka kembali quiz subtopik yang sudah lulus. | Sistem mencegah quiz diulang jika sudah lulus. | Quiz yang sudah lulus tidak dapat diulang. | Valid |
| TC-028 | Unlock Subtopik | Mahasiswa lulus quiz subtopik pertama. | Selesaikan quiz subtopik 1 dengan nilai lulus. | Subtopik berikutnya terbuka, subtopik setelahnya tetap terkunci. | Subtopik berikutnya terbuka secara berurutan. | Valid |
| TC-029 | Quiz Tidak Lulus | Mahasiswa tidak lulus quiz subtopik. | Jawab quiz dengan nilai di bawah threshold. | Sistem mengarahkan mahasiswa untuk review materi. | Sistem menampilkan arahan review. | Valid |
| TC-030 | Drill Soal | Mahasiswa membuka latihan drill. | Buka panel Latihan Drill Soal. | Sistem menampilkan soal drill dan pilihan jawaban. | Soal drill dan pilihan jawaban tampil. | Valid |
| TC-031 | Drill Soal | Mahasiswa menjawab drill soal. | Pilih jawaban pada drill. | Sistem memberi feedback tanpa mengganggu alur quiz utama. | Feedback drill tampil dan alur utama tetap berjalan. | Valid |
| TC-032 | Post Test Lock | Mahasiswa mencoba membuka post test sebelum semua quiz selesai. | Klik post test sebelum semua quiz subtopik lulus. | Sistem menolak akses post test. | Sistem meminta semua quiz subtopik diselesaikan. | Valid |
| TC-033 | Post Test | Mahasiswa membuka post test setelah semua quiz subtopik selesai. | Klik mulai post test. | Sistem menampilkan soal post test modul. | Soal post test tampil. | Valid |
| TC-034 | Post Test | Mahasiswa menyelesaikan post test. | Jawab semua soal post test. | Sistem menyimpan skor post test dan menghitung status modul. | Skor post test tersimpan. | Valid |
| TC-035 | Rapor Modul | Mahasiswa selesai post test. | Klik lihat rapor modul. | Sistem menampilkan learning diagnosis report. | Rapor modul tampil. | Valid |
| TC-036 | Rekomendasi Akhir | Sistem membuat rekomendasi akhir modul. | Buka rapor modul. | Sistem menampilkan rekomendasi lanjut modul, review, latihan tambahan, atau pendampingan. | Rekomendasi akhir tampil. | Valid |
| TC-037 | Unlock Modul Berikutnya | Mahasiswa lulus post test dan mastery memenuhi threshold. | Selesaikan modul dengan nilai lulus. | Modul berikutnya terbuka. | Modul berikutnya terbuka. | Valid |
| TC-038 | Modul Belum Lulus | Mahasiswa tidak memenuhi threshold mastery. | Nilai post test/mastery di bawah batas. | Modul berikutnya tetap terkunci dan sistem menyarankan penguatan. | Modul berikutnya tetap terkunci. | Valid |
| TC-039 | Profil Mahasiswa | Mahasiswa membuka halaman profil. | Klik menu Profil. | Sistem menampilkan data akun, level, poin, dan progress. | Profil mahasiswa tampil. | Valid |
| TC-040 | Gamifikasi | Mahasiswa membuka leaderboard dan reward. | Klik menu Leaderboard & Reward. | Sistem menampilkan leaderboard dan daftar reward. | Leaderboard dan reward tampil. | Valid |
| TC-041 | Redeem Reward | Mahasiswa menukar reward dengan poin cukup. | Klik redeem reward. | Sistem memproses penukaran dan mengurangi poin. | Penukaran reward diproses. | Valid |
| TC-042 | Redeem Reward | Mahasiswa menukar reward dengan poin tidak cukup. | Klik redeem reward dengan poin kurang. | Sistem menolak penukaran. | Sistem menampilkan pesan poin tidak cukup. | Valid |
| TC-043 | Chatbot | Mahasiswa mengirim pesan ke chatbot. | Ketik pertanyaan lalu kirim. | Sistem memberi respons sesuai konteks pembelajaran. | Chatbot membalas pesan. | Valid |
| TC-044 | Chatbot Hide | Mahasiswa menyembunyikan chatbot. | Klik tombol minimize/hide chatbot. | Panel chatbot mengecil dan tidak memenuhi area belajar. | Chatbot berhasil diminimize. | Valid |
| TC-045 | Progress Modul | Mahasiswa menyembunyikan panel progress. | Klik hide/tampilkan progress modul. | Panel progress dapat disembunyikan dan ditampilkan kembali. | Panel progress dapat di-toggle. | Valid |
| TC-046 | Admin Login | Admin login ke sistem. | Login menggunakan akun admin. | Admin dapat mengakses halaman admin. | Halaman admin dapat dibuka. | Valid |
| TC-047 | Proteksi Admin | Mahasiswa mencoba membuka halaman admin. | Akses URL admin menggunakan akun mahasiswa. | Sistem menolak akses dan mengarahkan ke dashboard. | Akses admin ditolak. | Valid |
| TC-048 | Admin Graph Prasyarat | Admin menambah relasi prasyarat modul. | Isi topic dan prerequisite lalu simpan. | Relasi prasyarat tersimpan. | Relasi graph tersimpan. | Valid |
| TC-049 | Admin Graph Prasyarat | Admin mengubah relasi prasyarat. | Edit data relasi lalu simpan. | Relasi prasyarat diperbarui. | Data relasi berhasil diperbarui. | Valid |
| TC-050 | Admin Graph Prasyarat | Admin menghapus relasi prasyarat. | Klik hapus relasi. | Relasi prasyarat terhapus. | Data relasi terhapus. | Valid |
| TC-051 | Admin Soal | Admin menambah soal baru. | Isi pertanyaan, pilihan, jawaban benar, dan tipe assessment. | Soal baru tersimpan. | Soal berhasil ditambahkan. | Valid |
| TC-052 | Admin Soal | Admin mengubah soal. | Edit pertanyaan/pilihan jawaban. | Soal berhasil diperbarui. | Soal berhasil diperbarui. | Valid |
| TC-053 | Admin Soal | Admin menghapus soal. | Klik hapus soal. | Soal terhapus dari daftar. | Soal berhasil dihapus. | Valid |
| TC-054 | Admin Materi | Admin menambah subtopik/materi. | Isi data materi lalu simpan. | Materi baru tersimpan. | Materi berhasil ditambahkan. | Valid |
| TC-055 | Admin Materi | Admin mengubah materi. | Edit data materi lalu simpan. | Materi berhasil diperbarui. | Materi berhasil diperbarui. | Valid |
| TC-056 | Admin Materi | Admin menghapus materi. | Klik hapus materi. | Materi terhapus dari daftar. | Materi berhasil dihapus. | Valid |
| TC-057 | Reset Data | Admin mereset data belajar user. | Pilih user lalu reset learning data. | Progress, assessment, q-value, dan profil belajar user terhapus sesuai kebijakan. | Data belajar user berhasil direset. | Valid |
| TC-058 | Responsif | Mahasiswa membuka aplikasi di layar laptop. | Buka aplikasi pada resolusi laptop. | Tampilan tidak tumpang tindih dan fitur utama dapat digunakan. | Tampilan laptop dapat digunakan. | Valid |
| TC-059 | Responsif | Mahasiswa membuka aplikasi di layar mobile. | Buka aplikasi pada resolusi mobile. | Konten dapat discroll dan tombol tetap dapat digunakan. | Tampilan mobile dapat digunakan. | Valid |
| TC-060 | Error Handling | Backend tidak tersedia saat frontend meminta data. | Matikan backend lalu buka dashboard. | Sistem menampilkan pesan gagal memuat data atau error yang dapat dipahami. | Sistem menampilkan error koneksi. | Valid |

# Ringkasan Hasil Pengujian

| Total Skenario | Valid | Tidak Valid | Perlu Perbaikan |
|---|---|---|---|
| 60 | 60 | 0 | 0 |

Berdasarkan hasil pengujian blackbox, seluruh skenario yang diuji menghasilkan output sesuai dengan hasil yang diharapkan. Fitur utama seperti autentikasi, profil kognitif, learning path, pre test, quiz subtopik, update q-value, post test, rapor modul, gamifikasi, chatbot, dan fitur admin dapat berjalan sesuai kebutuhan sistem.

# Kesimpulan

Hasil uji blackbox menunjukkan bahwa aplikasi learning path adaptif telah memenuhi kebutuhan fungsional utama. Sistem dapat mengatur akses modul berdasarkan prasyarat, membuka materi setelah pre test, mengatur quiz subtopik secara berurutan, memperbarui q-value melalui Q-learning, menghasilkan learning diagnosis report setelah post test, serta menyediakan fitur admin untuk mengelola graph prasyarat, soal, dan materi.
