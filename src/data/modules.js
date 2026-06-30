/**
 * Learning Modules — Dummy Data (Indonesian)
 * Algoritma dan Pemrograman untuk Mahasiswa Ilmu Komputer
 * Arsitektur Graph Knowledge Tracing (GKT)
 */
export const course = {
  id: 'course-algo-01',
  title: 'Algoritma dan Pemrograman',
  description: 'Kuasai dasar-dasar algoritma dan pemrograman melalui pembelajaran adaptif berbasis AI',
  icon: '💻',
  totalModules: 3,
}

export const modules = [
  {
    id: 'mod-001',
    title: 'Dasar & Variabel',
    icon: '🧱',
    description: 'Pelajari konsep dasar pemrograman, tipe data, variabel, dan operasi aritmatika',
    difficulty: 'Dasar',
    estimatedTime: '60 menit',
    order: 1,
    status: 'in-progress',
    progress: 65,
    subMateriCount: 5,
    subtopics: [
      {
        id: 'sub-001-1',
        title: 'Pengantar Algoritma dan Program',
        completed: true,
        content: {
          title: 'Pengantar Algoritma dan Program',
          tabs: [
            {
              id: 'ringkasan',
              label: 'Ringkasan Materi',
              icon: '📖',
            },
            {
              id: 'video',
              label: 'Video Pembelajaran',
              icon: '▶️',
            },
            {
              id: 'contoh',
              label: 'Contoh Soal',
              icon: '📝',
            },
          ],
          sections: [
            {
              type: 'text',
              content: 'Algoritma adalah urutan langkah-langkah logis dan sistematis untuk menyelesaikan suatu masalah. Program adalah implementasi algoritma dalam bahasa pemrograman tertentu sehingga dapat dieksekusi oleh komputer.',
            },
            {
              type: 'formula',
              title: 'Siklus Pengembangan Program',
              content: '1. Definisi Masalah\n2. Merancang Algoritma (Pseudocode / Flowchart)\n3. Menulis Kode Program (Coding)\n4. Kompilasi / Interpretasi\n5. Pengujian (Testing & Debugging)\n6. Dokumentasi',
              description: 'Setiap program yang baik melewati siklus ini secara iteratif.',
            },
            {
              type: 'example',
              title: 'Contoh Pseudocode Sederhana',
              items: [
                'MULAI\n  TAMPILKAN "Halo, Dunia!"\nSELESAI',
                'Dalam Python:\nprint("Halo, Dunia!")\n\nDalam C++:\n#include <iostream>\nint main() {\n    std::cout << "Halo, Dunia!" << std::endl;\n    return 0;\n}',
              ],
            },
          ],
        },
      },
      {
        id: 'sub-001-2',
        title: 'Variabel dan Tipe Data',
        completed: true,
        content: {
          title: 'Variabel dan Tipe Data',
          sections: [
            {
              type: 'text',
              content: 'Variabel adalah wadah untuk menyimpan data di dalam memori komputer. Setiap variabel memiliki nama, tipe data, dan nilai. Tipe data menentukan jenis nilai yang dapat disimpan dan operasi yang dapat dilakukan.',
            },
            {
              type: 'formula',
              title: 'Tipe Data Dasar',
              content: 'int     → Bilangan bulat (contoh: 10, -3, 0)\nfloat   → Bilangan desimal (contoh: 3.14, -0.5)\nstr     → Teks/string (contoh: "Halo")\nbool    → Nilai logika (True / False)\nchar    → Karakter tunggal (contoh: \'A\', \'z\')',
              description: 'Python menggunakan dynamic typing, sedangkan C++ menggunakan static typing.',
            },
            {
              type: 'example',
              title: 'Deklarasi Variabel',
              items: [
                'Python:\nnama = "Budi"\numur = 20\nip_semester = 3.75\nis_aktif = True',
                'C++:\nstring nama = "Budi";\nint umur = 20;\nfloat ip_semester = 3.75;\nbool is_aktif = true;',
              ],
            },
          ],
        },
      },
      {
        id: 'sub-001-3',
        title: 'Operasi Aritmatika dan Ekspresi',
        completed: true,
        content: {
          title: 'Operasi Aritmatika dan Ekspresi',
          sections: [
            {
              type: 'text',
              content: 'Operasi aritmatika digunakan untuk melakukan perhitungan matematika pada variabel numerik. Hasil operasi dapat disimpan ke variabel lain atau langsung ditampilkan.',
            },
            {
              type: 'formula',
              title: 'Operator Aritmatika',
              content: '+   → Penjumlahan        (5 + 3 = 8)\n-   → Pengurangan        (10 - 4 = 6)\n*   → Perkalian          (3 * 7 = 21)\n/   → Pembagian          (15 / 4 = 3.75)\n//  → Pembagian bulat    (15 // 4 = 3)\n%   → Modulo (sisa bagi) (15 % 4 = 3)\n**  → Pangkat            (2 ** 3 = 8)',
              description: 'Prioritas operator mengikuti aturan matematika: pangkat → kali/bagi → tambah/kurang.',
            },
          ],
        },
      },
      {
        id: 'sub-001-4',
        title: 'Input dan Output',
        completed: false,
        content: {
          title: 'Input dan Output',
          sections: [
            {
              type: 'text',
              content: 'Program interaktif memerlukan mekanisme untuk menerima masukan (input) dari pengguna dan menampilkan keluaran (output). Fungsi input membaca data dari keyboard, sedangkan fungsi output menampilkan data ke layar.',
            },
            {
              type: 'example',
              title: 'Contoh Input/Output',
              items: [
                'Python:\nnama = input("Masukkan nama: ")\nprint("Halo,", nama)\nprint(f"Selamat datang, {nama}!")',
                'C++:\nstring nama;\ncout << "Masukkan nama: ";\ncin >> nama;\ncout << "Halo, " << nama << endl;',
              ],
            },
          ],
        },
      },
      {
        id: 'sub-001-5',
        title: 'Konversi Tipe Data (Type Casting)',
        completed: false,
        content: {
          title: 'Konversi Tipe Data (Type Casting)',
          sections: [
            {
              type: 'text',
              content: 'Konversi tipe data adalah proses mengubah nilai dari satu tipe data ke tipe data lain. Hal ini sering diperlukan saat melakukan operasi antar tipe data yang berbeda atau saat menerima input dari pengguna.',
            },
            {
              type: 'formula',
              title: 'Fungsi Konversi di Python',
              content: 'int("42")    → 42        (string ke integer)\nfloat("3.14") → 3.14     (string ke float)\nstr(100)     → "100"     (integer ke string)\nint(3.99)    → 3         (float ke int, dibulatkan ke bawah)\nbool(0)      → False     (nol = False, selainnya = True)',
              description: 'Hati-hati: int("abc") akan menghasilkan error karena "abc" bukan angka valid.',
            },
          ],
        },
      },
    ],
  },
  {
    id: 'mod-002',
    title: 'Percabangan (Control Flow)',
    icon: '🔀',
    description: 'Memahami logika percabangan menggunakan if, else, elif/else-if, dan operator logika',
    difficulty: 'Menengah',
    estimatedTime: '75 menit',
    order: 2,
    status: 'in-progress',
    progress: 30,
    subMateriCount: 5,
    subtopics: [
      {
        id: 'sub-002-1',
        title: 'Operator Perbandingan dan Logika',
        completed: true,
        content: {
          title: 'Operator Perbandingan dan Logika',
          sections: [
            {
              type: 'text',
              content: 'Operator perbandingan digunakan untuk membandingkan dua nilai dan menghasilkan nilai boolean (True/False). Operator logika digunakan untuk menggabungkan beberapa kondisi.',
            },
            {
              type: 'formula',
              title: 'Operator Perbandingan',
              content: '==  → Sama dengan         (5 == 5 → True)\n!=  → Tidak sama dengan   (5 != 3 → True)\n>   → Lebih besar         (7 > 3 → True)\n<   → Lebih kecil         (2 < 8 → True)\n>=  → Lebih besar/sama    (5 >= 5 → True)\n<=  → Lebih kecil/sama    (3 <= 4 → True)',
              description: '',
            },
            {
              type: 'formula',
              title: 'Operator Logika',
              content: 'and  → Keduanya harus True   (True and False → False)\nor   → Salah satu True cukup  (True or False → True)\nnot  → Membalikkan nilai       (not True → False)',
              description: 'Dalam C++, gunakan && (and), || (or), dan ! (not).',
            },
          ],
        },
      },
      {
        id: 'sub-002-2',
        title: 'Percabangan if dan if-else',
        completed: true,
        content: {
          title: 'Percabangan if dan if-else',
          sections: [
            {
              type: 'text',
              content: 'Struktur if digunakan untuk mengeksekusi blok kode hanya jika suatu kondisi bernilai True. Struktur if-else menyediakan alternatif eksekusi ketika kondisi bernilai False.',
            },
            {
              type: 'formula',
              title: 'Sintaks if-else',
              content: 'Python:\nif kondisi:\n    # blok jika True\nelse:\n    # blok jika False\n\nC++:\nif (kondisi) {\n    // blok jika true\n} else {\n    // blok jika false\n}',
              description: 'Perhatikan indentasi pada Python dan kurung kurawal pada C++.',
            },
            {
              type: 'example',
              title: 'Contoh: Cek Bilangan Positif/Negatif',
              items: [
                'angka = int(input("Masukkan angka: "))\nif angka >= 0:\n    print("Bilangan positif")\nelse:\n    print("Bilangan negatif")',
              ],
            },
          ],
        },
      },
      {
        id: 'sub-002-3',
        title: 'Percabangan Bertingkat (elif / else-if)',
        completed: false,
        content: {
          title: 'Percabangan Bertingkat (elif / else-if)',
          sections: [
            {
              type: 'text',
              content: 'Ketika ada lebih dari dua kemungkinan kondisi, gunakan elif (Python) atau else if (C++) untuk memeriksa kondisi secara bertingkat dari atas ke bawah.',
            },
            {
              type: 'formula',
              title: 'Sintaks elif',
              content: 'nilai = int(input("Masukkan nilai: "))\n\nif nilai >= 85:\n    grade = "A"\nelif nilai >= 70:\n    grade = "B"\nelif nilai >= 55:\n    grade = "C"\nelif nilai >= 40:\n    grade = "D"\nelse:\n    grade = "E"\n\nprint(f"Grade Anda: {grade}")',
              description: 'Kondisi diperiksa dari atas ke bawah. Begitu satu kondisi True, blok di bawahnya tidak diperiksa lagi.',
            },
          ],
        },
      },
      {
        id: 'sub-002-4',
        title: 'Percabangan Bersarang (Nested If)',
        completed: false,
        content: {
          title: 'Percabangan Bersarang (Nested If)',
          sections: [
            {
              type: 'text',
              content: 'Percabangan bersarang adalah struktur if di dalam if. Digunakan ketika keputusan kedua bergantung pada hasil keputusan pertama. Hindari nested if terlalu dalam karena menurunkan keterbacaan kode.',
            },
            {
              type: 'example',
              title: 'Contoh: Validasi Login',
              items: [
                'username = input("Username: ")\npassword = input("Password: ")\n\nif username == "admin":\n    if password == "1234":\n        print("Login berhasil!")\n    else:\n        print("Password salah!")\nelse:\n    print("Username tidak ditemukan!")',
              ],
            },
          ],
        },
      },
      {
        id: 'sub-002-5',
        title: 'Studi Kasus Percabangan',
        completed: false,
        content: {
          title: 'Studi Kasus Percabangan',
          sections: [
            {
              type: 'text',
              content: 'Terapkan konsep percabangan untuk menyelesaikan masalah nyata dalam pemrograman, seperti kalkulator sederhana, sistem grading, dan validasi input.',
            },
            {
              type: 'example',
              title: 'Contoh: Kalkulator Sederhana',
              items: [
                'a = float(input("Angka pertama: "))\nop = input("Operator (+, -, *, /): ")\nb = float(input("Angka kedua: "))\n\nif op == "+":\n    hasil = a + b\nelif op == "-":\n    hasil = a - b\nelif op == "*":\n    hasil = a * b\nelif op == "/":\n    if b != 0:\n        hasil = a / b\n    else:\n        print("Error: Pembagian dengan nol!")\n        hasil = None\nelse:\n    print("Operator tidak valid!")\n    hasil = None\n\nif hasil is not None:\n    print(f"Hasil: {hasil}")',
                'Studi Kasus 2 — Cek Tahun Kabisat:\ntahun = int(input("Masukkan tahun: "))\nif (tahun % 4 == 0 and tahun % 100 != 0) or (tahun % 400 == 0):\n    print(f"{tahun} adalah tahun kabisat")\nelse:\n    print(f"{tahun} bukan tahun kabisat")',
              ],
            },
          ],
        },
      },
    ],
  },
  {
    id: 'mod-003',
    title: 'Perulangan (Looping)',
    icon: '🔁',
    description: 'Menguasai konsep perulangan menggunakan for, while, dan teknik kontrol loop',
    difficulty: 'Menengah',
    estimatedTime: '80 menit',
    order: 3,
    status: 'locked',
    progress: 0,
    subMateriCount: 5,
    subtopics: [
      {
        id: 'sub-003-1',
        title: 'Perulangan for',
        completed: false,
        content: {
          title: 'Perulangan for',
          sections: [
            {
              type: 'text',
              content: 'Perulangan for digunakan ketika jumlah iterasi sudah diketahui. Di Python, for bekerja dengan iterable (range, list, string). Di C++, for memiliki tiga komponen: inisialisasi, kondisi, dan increment.',
            },
            {
              type: 'formula',
              title: 'Sintaks Perulangan for',
              content: 'Python:\nfor i in range(5):       # i = 0, 1, 2, 3, 4\n    print(i)\n\nfor i in range(1, 11):   # i = 1, 2, ..., 10\n    print(i)\n\nC++:\nfor (int i = 0; i < 5; i++) {\n    cout << i << endl;\n}',
              description: 'range(start, stop, step) → start inklusif, stop eksklusif.',
            },
          ],
        },
      },
      {
        id: 'sub-003-2',
        title: 'Perulangan while',
        completed: false,
        content: {
          title: 'Perulangan while',
          sections: [
            {
              type: 'text',
              content: 'Perulangan while mengeksekusi blok kode selama kondisi masih bernilai True. Cocok digunakan ketika jumlah iterasi belum diketahui dan bergantung pada suatu kondisi tertentu.',
            },
            {
              type: 'formula',
              title: 'Sintaks Perulangan while',
              content: 'Python:\ncount = 0\nwhile count < 5:\n    print(f"Iterasi ke-{count}")\n    count += 1\n\nC++:\nint count = 0;\nwhile (count < 5) {\n    cout << "Iterasi ke-" << count << endl;\n    count++;\n}',
              description: 'PERINGATAN: Pastikan kondisi while akan menjadi False di suatu titik, jika tidak terjadi infinite loop!',
            },
          ],
        },
      },
      {
        id: 'sub-003-3',
        title: 'break, continue, dan else pada Loop',
        completed: false,
        content: {
          title: 'break, continue, dan else pada Loop',
          sections: [
            {
              type: 'text',
              content: 'Keyword break menghentikan loop sepenuhnya, continue melewati iterasi saat ini dan lanjut ke iterasi berikutnya. Python memiliki fitur unik: else pada loop yang dieksekusi jika loop selesai tanpa break.',
            },
            {
              type: 'example',
              title: 'Contoh Penggunaan break dan continue',
              items: [
                'Break — Mencari angka dalam list:\ndata = [3, 7, 2, 9, 5]\ntarget = 9\nfor angka in data:\n    if angka == target:\n        print(f"Ditemukan: {target}")\n        break\nelse:\n    print("Tidak ditemukan")',
                'Continue — Cetak bilangan ganjil saja:\nfor i in range(1, 11):\n    if i % 2 == 0:\n        continue\n    print(i)   # Output: 1, 3, 5, 7, 9',
              ],
            },
          ],
        },
      },
      {
        id: 'sub-003-4',
        title: 'Perulangan Bersarang (Nested Loop)',
        completed: false,
        content: {
          title: 'Perulangan Bersarang (Nested Loop)',
          sections: [
            {
              type: 'text',
              content: 'Nested loop adalah loop di dalam loop. Loop luar mengontrol jumlah baris, dan loop dalam mengontrol jumlah kolom. Umum digunakan untuk memproses data 2 dimensi seperti matriks atau membuat pola.',
            },
            {
              type: 'example',
              title: 'Contoh: Mencetak Pola Bintang',
              items: [
                'Pola segitiga bintang:\nn = 5\nfor i in range(1, n + 1):\n    for j in range(i):\n        print("*", end="")\n    print()\n\nOutput:\n*\n**\n***\n****\n*****',
                'Tabel perkalian 1-5:\nfor i in range(1, 6):\n    for j in range(1, 6):\n        print(f"{i*j:4}", end="")\n    print()',
              ],
            },
          ],
        },
      },
      {
        id: 'sub-003-5',
        title: 'Studi Kasus Perulangan',
        completed: false,
        content: {
          title: 'Studi Kasus Perulangan',
          sections: [
            {
              type: 'text',
              content: 'Terapkan konsep perulangan untuk menyelesaikan masalah algoritmik klasik: menghitung faktorial, deret Fibonacci, dan mencari bilangan prima.',
            },
            {
              type: 'example',
              title: 'Studi Kasus',
              items: [
                'Faktorial:\nn = int(input("Masukkan n: "))\nfaktorial = 1\nfor i in range(1, n + 1):\n    faktorial *= i\nprint(f"{n}! = {faktorial}")',
                'Fibonacci:\nn = int(input("Jumlah suku: "))\na, b = 0, 1\nfor _ in range(n):\n    print(a, end=" ")\n    a, b = b, a + b',
                'Cek Bilangan Prima:\nnum = int(input("Masukkan bilangan: "))\nis_prima = True\nif num < 2:\n    is_prima = False\nfor i in range(2, int(num**0.5) + 1):\n    if num % i == 0:\n        is_prima = False\n        break\nprint(f"{num} {\\"prima\\" if is_prima else \\"bukan prima\\"}")',
              ],
            },
          ],
        },
      },
    ],
  },
]
