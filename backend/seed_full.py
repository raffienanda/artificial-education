"""
Comprehensive Database Seeder for Artificial Education
Seeds all modules, subtopics, questions, and user progress from frontend dummy data.
"""
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.module import Module, Subtopic
from app.models.question import Question
from app.models.progress import UserProgress


def seed_all():
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ==============================
        # 1. Seed User
        # ==============================
        user = db.query(User).filter(User.username == "student_cs").first()
        if not user:
            user = User(username="student_cs", xp=500, combo=0, total_score=0)
            db.add(user)
            db.commit()
            db.refresh(user)
            print("[+] User 'student_cs' created")
        else:
            print("[=] User 'student_cs' already exists")

        # ==============================
        # 2. Seed Modules & Subtopics
        # ==============================
        modules_data = [
            {
                "id": "mod-001",
                "title": "Dasar & Variabel",
                "icon": "🧱",
                "description": "Pelajari konsep dasar pemrograman, tipe data, variabel, dan operasi aritmatika",
                "difficulty": "Dasar",
                "estimated_time": "60 menit",
                "order": 1,
                "status": "in-progress",
                "subtopics": [
                    {
                        "id": "sub-001-1",
                        "title": "Pengantar Algoritma dan Program",
                        "content": {
                            "title": "Pengantar Algoritma dan Program",
                            "tabs": [
                                {"id": "ringkasan", "label": "Ringkasan Materi", "icon": "📖"},
                                {"id": "video", "label": "Video Pembelajaran", "icon": "▶️"},
                                {"id": "contoh", "label": "Contoh Soal", "icon": "📝"}
                            ],
                            "sections": [
                                {"type": "text", "content": "Algoritma adalah urutan langkah-langkah logis dan sistematis untuk menyelesaikan suatu masalah. Program adalah implementasi algoritma dalam bahasa pemrograman tertentu sehingga dapat dieksekusi oleh komputer."},
                                {"type": "formula", "title": "Siklus Pengembangan Program", "content": "1. Definisi Masalah\n2. Merancang Algoritma (Pseudocode / Flowchart)\n3. Menulis Kode Program (Coding)\n4. Kompilasi / Interpretasi\n5. Pengujian (Testing & Debugging)\n6. Dokumentasi", "description": "Setiap program yang baik melewati siklus ini secara iteratif."},
                                {"type": "example", "title": "Contoh Pseudocode Sederhana", "items": ["MULAI\n  TAMPILKAN \"Halo, Dunia!\"\nSELESAI", "Dalam Python:\nprint(\"Halo, Dunia!\")\n\nDalam C++:\n#include <iostream>\nint main() {\n    std::cout << \"Halo, Dunia!\" << std::endl;\n    return 0;\n}"]}
                            ]
                        }
                    },
                    {
                        "id": "sub-001-2",
                        "title": "Variabel dan Tipe Data",
                        "content": {
                            "title": "Variabel dan Tipe Data",
                            "sections": [
                                {"type": "text", "content": "Variabel adalah wadah untuk menyimpan data di dalam memori komputer. Setiap variabel memiliki nama, tipe data, dan nilai. Tipe data menentukan jenis nilai yang dapat disimpan dan operasi yang dapat dilakukan."},
                                {"type": "formula", "title": "Tipe Data Dasar", "content": "int     → Bilangan bulat (contoh: 10, -3, 0)\nfloat   → Bilangan desimal (contoh: 3.14, -0.5)\nstr     → Teks/string (contoh: \"Halo\")\nbool    → Nilai logika (True / False)\nchar    → Karakter tunggal (contoh: 'A', 'z')", "description": "Python menggunakan dynamic typing, sedangkan C++ menggunakan static typing."},
                                {"type": "example", "title": "Deklarasi Variabel", "items": ["Python:\nnama = \"Budi\"\numur = 20\nip_semester = 3.75\nis_aktif = True", "C++:\nstring nama = \"Budi\";\nint umur = 20;\nfloat ip_semester = 3.75;\nbool is_aktif = true;"]}
                            ]
                        }
                    },
                    {
                        "id": "sub-001-3",
                        "title": "Operasi Aritmatika dan Ekspresi",
                        "content": {
                            "title": "Operasi Aritmatika dan Ekspresi",
                            "sections": [
                                {"type": "text", "content": "Operasi aritmatika digunakan untuk melakukan perhitungan matematika pada variabel numerik. Hasil operasi dapat disimpan ke variabel lain atau langsung ditampilkan."},
                                {"type": "formula", "title": "Operator Aritmatika", "content": "+   → Penjumlahan        (5 + 3 = 8)\n-   → Pengurangan        (10 - 4 = 6)\n*   → Perkalian          (3 * 7 = 21)\n/   → Pembagian          (15 / 4 = 3.75)\n//  → Pembagian bulat    (15 // 4 = 3)\n%   → Modulo (sisa bagi) (15 % 4 = 3)\n**  → Pangkat            (2 ** 3 = 8)", "description": "Prioritas operator mengikuti aturan matematika: pangkat → kali/bagi → tambah/kurang."}
                            ]
                        }
                    },
                    {
                        "id": "sub-001-4",
                        "title": "Input dan Output",
                        "content": {
                            "title": "Input dan Output",
                            "sections": [
                                {"type": "text", "content": "Program interaktif memerlukan mekanisme untuk menerima masukan (input) dari pengguna dan menampilkan keluaran (output). Fungsi input membaca data dari keyboard, sedangkan fungsi output menampilkan data ke layar."},
                                {"type": "example", "title": "Contoh Input/Output", "items": ["Python:\nnama = input(\"Masukkan nama: \")\nprint(\"Halo,\", nama)\nprint(f\"Selamat datang, {nama}!\")", "C++:\nstring nama;\ncout << \"Masukkan nama: \";\ncin >> nama;\ncout << \"Halo, \" << nama << endl;"]}
                            ]
                        }
                    },
                    {
                        "id": "sub-001-5",
                        "title": "Konversi Tipe Data (Type Casting)",
                        "content": {
                            "title": "Konversi Tipe Data (Type Casting)",
                            "sections": [
                                {"type": "text", "content": "Konversi tipe data adalah proses mengubah nilai dari satu tipe data ke tipe data lain. Hal ini sering diperlukan saat melakukan operasi antar tipe data yang berbeda atau saat menerima input dari pengguna."},
                                {"type": "formula", "title": "Fungsi Konversi di Python", "content": "int(\"42\")    → 42        (string ke integer)\nfloat(\"3.14\") → 3.14     (string ke float)\nstr(100)     → \"100\"     (integer ke string)\nint(3.99)    → 3         (float ke int, dibulatkan ke bawah)\nbool(0)      → False     (nol = False, selainnya = True)", "description": "Hati-hati: int(\"abc\") akan menghasilkan error karena \"abc\" bukan angka valid."}
                            ]
                        }
                    }
                ]
            },
            {
                "id": "mod-002",
                "title": "Percabangan (Control Flow)",
                "icon": "🔀",
                "description": "Memahami logika percabangan menggunakan if, else, elif/else-if, dan operator logika",
                "difficulty": "Menengah",
                "estimated_time": "75 menit",
                "order": 2,
                "status": "in-progress",
                "subtopics": [
                    {
                        "id": "sub-002-1",
                        "title": "Operator Perbandingan dan Logika",
                        "content": {
                            "title": "Operator Perbandingan dan Logika",
                            "sections": [
                                {"type": "text", "content": "Operator perbandingan digunakan untuk membandingkan dua nilai dan menghasilkan nilai boolean (True/False). Operator logika digunakan untuk menggabungkan beberapa kondisi."},
                                {"type": "formula", "title": "Operator Perbandingan", "content": "==  → Sama dengan         (5 == 5 → True)\n!=  → Tidak sama dengan   (5 != 3 → True)\n>   → Lebih besar         (7 > 3 → True)\n<   → Lebih kecil         (2 < 8 → True)\n>=  → Lebih besar/sama    (5 >= 5 → True)\n<=  → Lebih kecil/sama    (3 <= 4 → True)", "description": ""},
                                {"type": "formula", "title": "Operator Logika", "content": "and  → Keduanya harus True   (True and False → False)\nor   → Salah satu True cukup  (True or False → True)\nnot  → Membalikkan nilai       (not True → False)", "description": "Dalam C++, gunakan && (and), || (or), dan ! (not)."}
                            ]
                        }
                    },
                    {
                        "id": "sub-002-2",
                        "title": "Percabangan if dan if-else",
                        "content": {
                            "title": "Percabangan if dan if-else",
                            "sections": [
                                {"type": "text", "content": "Struktur if digunakan untuk mengeksekusi blok kode hanya jika suatu kondisi bernilai True. Struktur if-else menyediakan alternatif eksekusi ketika kondisi bernilai False."},
                                {"type": "formula", "title": "Sintaks if-else", "content": "Python:\nif kondisi:\n    # blok jika True\nelse:\n    # blok jika False\n\nC++:\nif (kondisi) {\n    // blok jika true\n} else {\n    // blok jika false\n}", "description": "Perhatikan indentasi pada Python dan kurung kurawal pada C++."},
                                {"type": "example", "title": "Contoh: Cek Bilangan Positif/Negatif", "items": ["angka = int(input(\"Masukkan angka: \"))\nif angka >= 0:\n    print(\"Bilangan positif\")\nelse:\n    print(\"Bilangan negatif\")"]}
                            ]
                        }
                    },
                    {
                        "id": "sub-002-3",
                        "title": "Percabangan Bertingkat (elif / else-if)",
                        "content": {
                            "title": "Percabangan Bertingkat (elif / else-if)",
                            "sections": [
                                {"type": "text", "content": "Ketika ada lebih dari dua kemungkinan kondisi, gunakan elif (Python) atau else if (C++) untuk memeriksa kondisi secara bertingkat dari atas ke bawah."},
                                {"type": "formula", "title": "Sintaks elif", "content": "nilai = int(input(\"Masukkan nilai: \"))\n\nif nilai >= 85:\n    grade = \"A\"\nelif nilai >= 70:\n    grade = \"B\"\nelif nilai >= 55:\n    grade = \"C\"\nelif nilai >= 40:\n    grade = \"D\"\nelse:\n    grade = \"E\"\n\nprint(f\"Grade Anda: {grade}\")", "description": "Kondisi diperiksa dari atas ke bawah. Begitu satu kondisi True, blok di bawahnya tidak diperiksa lagi."}
                            ]
                        }
                    },
                    {
                        "id": "sub-002-4",
                        "title": "Percabangan Bersarang (Nested If)",
                        "content": {
                            "title": "Percabangan Bersarang (Nested If)",
                            "sections": [
                                {"type": "text", "content": "Percabangan bersarang adalah struktur if di dalam if. Digunakan ketika keputusan kedua bergantung pada hasil keputusan pertama. Hindari nested if terlalu dalam karena menurunkan keterbacaan kode."},
                                {"type": "example", "title": "Contoh: Validasi Login", "items": ["username = input(\"Username: \")\npassword = input(\"Password: \")\n\nif username == \"admin\":\n    if password == \"1234\":\n        print(\"Login berhasil!\")\n    else:\n        print(\"Password salah!\")\nelse:\n    print(\"Username tidak ditemukan!\")"]}
                            ]
                        }
                    },
                    {
                        "id": "sub-002-5",
                        "title": "Studi Kasus Percabangan",
                        "content": {
                            "title": "Studi Kasus Percabangan",
                            "sections": [
                                {"type": "text", "content": "Terapkan konsep percabangan untuk menyelesaikan masalah nyata dalam pemrograman, seperti kalkulator sederhana, sistem grading, dan validasi input."},
                                {"type": "example", "title": "Contoh: Kalkulator Sederhana", "items": ["a = float(input(\"Angka pertama: \"))\nop = input(\"Operator (+, -, *, /): \")\nb = float(input(\"Angka kedua: \"))\n\nif op == \"+\":\n    hasil = a + b\nelif op == \"-\":\n    hasil = a - b\nelif op == \"*\":\n    hasil = a * b\nelif op == \"/\":\n    if b != 0:\n        hasil = a / b\n    else:\n        print(\"Error: Pembagian dengan nol!\")\n        hasil = None\nelse:\n    print(\"Operator tidak valid!\")\n    hasil = None\n\nif hasil is not None:\n    print(f\"Hasil: {hasil}\")"]}
                            ]
                        }
                    }
                ]
            },
            {
                "id": "mod-003",
                "title": "Perulangan (Looping)",
                "icon": "🔁",
                "description": "Menguasai konsep perulangan menggunakan for, while, dan teknik kontrol loop",
                "difficulty": "Menengah",
                "estimated_time": "80 menit",
                "order": 3,
                "status": "locked",
                "subtopics": [
                    {
                        "id": "sub-003-1",
                        "title": "Perulangan for",
                        "content": {
                            "title": "Perulangan for",
                            "sections": [
                                {"type": "text", "content": "Perulangan for digunakan ketika jumlah iterasi sudah diketahui. Di Python, for bekerja dengan iterable (range, list, string). Di C++, for memiliki tiga komponen: inisialisasi, kondisi, dan increment."},
                                {"type": "formula", "title": "Sintaks Perulangan for", "content": "Python:\nfor i in range(5):       # i = 0, 1, 2, 3, 4\n    print(i)\n\nfor i in range(1, 11):   # i = 1, 2, ..., 10\n    print(i)\n\nC++:\nfor (int i = 0; i < 5; i++) {\n    cout << i << endl;\n}", "description": "range(start, stop, step) → start inklusif, stop eksklusif."}
                            ]
                        }
                    },
                    {
                        "id": "sub-003-2",
                        "title": "Perulangan while",
                        "content": {
                            "title": "Perulangan while",
                            "sections": [
                                {"type": "text", "content": "Perulangan while mengeksekusi blok kode selama kondisi masih bernilai True. Cocok digunakan ketika jumlah iterasi belum diketahui dan bergantung pada suatu kondisi tertentu."},
                                {"type": "formula", "title": "Sintaks Perulangan while", "content": "Python:\ncount = 0\nwhile count < 5:\n    print(f\"Iterasi ke-{count}\")\n    count += 1\n\nC++:\nint count = 0;\nwhile (count < 5) {\n    cout << \"Iterasi ke-\" << count << endl;\n    count++;\n}", "description": "PERINGATAN: Pastikan kondisi while akan menjadi False di suatu titik, jika tidak terjadi infinite loop!"}
                            ]
                        }
                    },
                    {
                        "id": "sub-003-3",
                        "title": "break, continue, dan else pada Loop",
                        "content": {
                            "title": "break, continue, dan else pada Loop",
                            "sections": [
                                {"type": "text", "content": "Keyword break menghentikan loop sepenuhnya, continue melewati iterasi saat ini dan lanjut ke iterasi berikutnya. Python memiliki fitur unik: else pada loop yang dieksekusi jika loop selesai tanpa break."},
                                {"type": "example", "title": "Contoh Penggunaan break dan continue", "items": ["Break — Mencari angka dalam list:\ndata = [3, 7, 2, 9, 5]\ntarget = 9\nfor angka in data:\n    if angka == target:\n        print(f\"Ditemukan: {target}\")\n        break\nelse:\n    print(\"Tidak ditemukan\")", "Continue — Cetak bilangan ganjil saja:\nfor i in range(1, 11):\n    if i % 2 == 0:\n        continue\n    print(i)   # Output: 1, 3, 5, 7, 9"]}
                            ]
                        }
                    },
                    {
                        "id": "sub-003-4",
                        "title": "Perulangan Bersarang (Nested Loop)",
                        "content": {
                            "title": "Perulangan Bersarang (Nested Loop)",
                            "sections": [
                                {"type": "text", "content": "Nested loop adalah loop di dalam loop. Loop luar mengontrol jumlah baris, dan loop dalam mengontrol jumlah kolom. Umum digunakan untuk memproses data 2 dimensi seperti matriks atau membuat pola."},
                                {"type": "example", "title": "Contoh: Mencetak Pola Bintang", "items": ["Pola segitiga bintang:\nn = 5\nfor i in range(1, n + 1):\n    for j in range(i):\n        print(\"*\", end=\"\")\n    print()\n\nOutput:\n*\n**\n***\n****\n*****", "Tabel perkalian 1-5:\nfor i in range(1, 6):\n    for j in range(1, 6):\n        print(f\"{i*j:4}\", end=\"\")\n    print()"]}
                            ]
                        }
                    },
                    {
                        "id": "sub-003-5",
                        "title": "Studi Kasus Perulangan",
                        "content": {
                            "title": "Studi Kasus Perulangan",
                            "sections": [
                                {"type": "text", "content": "Terapkan konsep perulangan untuk menyelesaikan masalah algoritmik klasik: menghitung faktorial, deret Fibonacci, dan mencari bilangan prima."},
                                {"type": "example", "title": "Studi Kasus", "items": ["Faktorial:\nn = int(input(\"Masukkan n: \"))\nfaktorial = 1\nfor i in range(1, n + 1):\n    faktorial *= i\nprint(f\"{n}! = {faktorial}\")", "Fibonacci:\nn = int(input(\"Jumlah suku: \"))\na, b = 0, 1\nfor _ in range(n):\n    print(a, end=\" \")\n    a, b = b, a + b"]}
                            ]
                        }
                    }
                ]
            }
        ]

        for mod_data in modules_data:
            existing_mod = db.query(Module).filter(Module.id == mod_data["id"]).first()
            if not existing_mod:
                mod = Module(
                    id=mod_data["id"],
                    title=mod_data["title"],
                    icon=mod_data["icon"],
                    description=mod_data["description"],
                    difficulty=mod_data["difficulty"],
                    estimated_time=mod_data["estimated_time"],
                    order=mod_data["order"],
                    status=mod_data["status"]
                )
                db.add(mod)
                db.commit()
                print(f"[+] Module '{mod_data['title']}' created")

                for sub_data in mod_data["subtopics"]:
                    sub = Subtopic(
                        id=sub_data["id"],
                        module_id=mod_data["id"],
                        title=sub_data["title"],
                        content=sub_data["content"]
                    )
                    db.add(sub)
                db.commit()
                print(f"    +-- {len(mod_data['subtopics'])} subtopics created")
            else:
                print(f"[=] Module '{mod_data['title']}' already exists")
                # Still check for missing subtopics
                for sub_data in mod_data["subtopics"]:
                    existing_sub = db.query(Subtopic).filter(Subtopic.id == sub_data["id"]).first()
                    if not existing_sub:
                        sub = Subtopic(
                            id=sub_data["id"],
                            module_id=mod_data["id"],
                            title=sub_data["title"],
                            content=sub_data["content"]
                        )
                        db.add(sub)
                        print(f"    [+] Subtopic '{sub_data['title']}' added")
                db.commit()

        # ==============================
        # 3. Seed Questions
        # ==============================
        questions_data = [
            {
                "id": "q-001",
                "subtopic_id": "sub-001-2",
                "question_text": "Manakah deklarasi variabel yang BENAR di Python?",
                "options": [
                    {"id": "a", "text": "int umur = 20", "label": "A"},
                    {"id": "b", "text": "umur = 20", "label": "B"},
                    {"id": "c", "text": "var umur = 20", "label": "C"},
                    {"id": "d", "text": "let umur = 20", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Python menggunakan dynamic typing, sehingga tidak perlu menuliskan tipe data saat deklarasi. Cukup tulis nama_variabel = nilai.",
                "difficulty": "mudah"
            },
            {
                "id": "q-002",
                "subtopic_id": "sub-001-3",
                "question_text": "Berapakah hasil dari ekspresi berikut di Python?\n\n17 // 5",
                "options": [
                    {"id": "a", "text": "3.4", "label": "A"},
                    {"id": "b", "text": "3", "label": "B"},
                    {"id": "c", "text": "2", "label": "C"},
                    {"id": "d", "text": "4", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Operator // adalah floor division (pembagian bulat) di Python. 17 dibagi 5 = 3.4, dibulatkan ke bawah menjadi 3.",
                "difficulty": "mudah"
            },
            {
                "id": "q-003",
                "subtopic_id": "sub-002-2",
                "question_text": "Apa output dari kode Python berikut?\n\nx = 15\nif x > 20:\n    print(\"Besar\")\nelse:\n    print(\"Kecil\")",
                "options": [
                    {"id": "a", "text": "Besar", "label": "A"},
                    {"id": "b", "text": "Kecil", "label": "B"},
                    {"id": "c", "text": "BesarKecil", "label": "C"},
                    {"id": "d", "text": "Error", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Variabel x bernilai 15. Kondisi x > 20 (15 > 20) bernilai False, sehingga blok else yang dieksekusi dan mencetak \"Kecil\".",
                "difficulty": "mudah"
            },
            {
                "id": "q-004",
                "subtopic_id": "sub-002-3",
                "question_text": "Perhatikan kode berikut:\n\nnilai = 72\nif nilai >= 85:\n    grade = \"A\"\nelif nilai >= 70:\n    grade = \"B\"\nelif nilai >= 55:\n    grade = \"C\"\nelse:\n    grade = \"D\"\n\nBerapakah nilai variabel grade?",
                "options": [
                    {"id": "a", "text": "A", "label": "A"},
                    {"id": "b", "text": "B", "label": "B"},
                    {"id": "c", "text": "C", "label": "C"},
                    {"id": "d", "text": "D", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "nilai = 72. Kondisi pertama (72 >= 85) = False. Kondisi kedua (72 >= 70) = True, maka grade = \"B\".",
                "difficulty": "sedang"
            },
            {
                "id": "q-005",
                "subtopic_id": "sub-002-1",
                "question_text": "Apa hasil dari ekspresi logika berikut di Python?\n\n(5 > 3) and (10 == 10) or (not True)",
                "options": [
                    {"id": "a", "text": "True", "label": "A"},
                    {"id": "b", "text": "False", "label": "B"},
                    {"id": "c", "text": "Error", "label": "C"},
                    {"id": "d", "text": "None", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Evaluasi: (5 > 3) = True, (10 == 10) = True, (not True) = False. True and True = True. True or False = True.",
                "difficulty": "sedang"
            },
            {
                "id": "q-006",
                "subtopic_id": "sub-001-5",
                "question_text": "Apa yang terjadi jika kode Python berikut dijalankan?\n\nhasil = int(\"3.14\")",
                "options": [
                    {"id": "a", "text": "hasil bernilai 3", "label": "A"},
                    {"id": "b", "text": "hasil bernilai 3.14", "label": "B"},
                    {"id": "c", "text": "ValueError (Error)", "label": "C"},
                    {"id": "d", "text": "hasil bernilai 4", "label": "D"}
                ],
                "correct_answer": "c",
                "explanation": "Fungsi int() tidak bisa langsung mengonversi string desimal \"3.14\" ke integer. Solusi yang benar: int(float(\"3.14\")).",
                "difficulty": "sedang"
            },
            {
                "id": "q-007",
                "subtopic_id": "sub-003-1",
                "question_text": "Berapa kali perintah print() akan dieksekusi pada kode berikut?\n\nfor i in range(2, 10, 3):\n    print(i)",
                "options": [
                    {"id": "a", "text": "2 kali", "label": "A"},
                    {"id": "b", "text": "3 kali", "label": "B"},
                    {"id": "c", "text": "4 kali", "label": "C"},
                    {"id": "d", "text": "8 kali", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "range(2, 10, 3) menghasilkan: 2, 5, 8. Jadi print() dieksekusi 3 kali.",
                "difficulty": "sedang"
            }
        ]

        for q_data in questions_data:
            existing_q = db.query(Question).filter(Question.id == q_data["id"]).first()
            if not existing_q:
                q = Question(
                    id=q_data["id"],
                    subtopic_id=q_data["subtopic_id"],
                    question_text=q_data["question_text"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data["explanation"],
                    difficulty=q_data["difficulty"]
                )
                db.add(q)
                print(f"[+] Question '{q_data['id']}' created")
            else:
                # Update existing question with full text
                existing_q.question_text = q_data["question_text"]
                existing_q.options = q_data["options"]
                existing_q.correct_answer = q_data["correct_answer"]
                existing_q.explanation = q_data["explanation"]
                existing_q.difficulty = q_data["difficulty"]
                print(f"[~] Question '{q_data['id']}' updated")

        db.commit()

        # ==============================
        # 4. Seed User Progress
        # ==============================
        progress_data = [
            {"topic_id": "sub-001-1", "mastery": 100.0, "status": "proficient"},
            {"topic_id": "sub-001-2", "mastery": 85.0, "status": "proficient"},
            {"topic_id": "sub-001-3", "mastery": 70.0, "status": "learning"},
            {"topic_id": "sub-001-4", "mastery": 40.0, "status": "learning"},
            {"topic_id": "sub-001-5", "mastery": 20.0, "status": "learning"},
            {"topic_id": "sub-002-1", "mastery": 60.0, "status": "learning"},
            {"topic_id": "sub-002-2", "mastery": 45.0, "status": "learning"},
        ]

        for p_data in progress_data:
            existing_p = db.query(UserProgress).filter(
                UserProgress.user_id == user.id,
                UserProgress.topic_id == p_data["topic_id"]
            ).first()
            if not existing_p:
                p = UserProgress(
                    user_id=user.id,
                    topic_id=p_data["topic_id"],
                    mastery=p_data["mastery"],
                    status=p_data["status"],
                    p_known=p_data["mastery"] / 100.0,
                    p_learn=0.2,
                    p_guess=0.25,
                    p_slip=0.1
                )
                db.add(p)
                print(f"[+] Progress for '{p_data['topic_id']}' created ({p_data['mastery']}%)")
            else:
                existing_p.mastery = p_data["mastery"]
                existing_p.status = p_data["status"]
                print(f"[~] Progress for '{p_data['topic_id']}' updated ({p_data['mastery']}%)")

        db.commit()
        print("\n[OK] Database seeding complete!")
        print(f"   Modules: {db.query(Module).count()}")
        print(f"   Subtopics: {db.query(Subtopic).count()}")
        print(f"   Questions: {db.query(Question).count()}")
        print(f"   User Progress: {db.query(UserProgress).count()}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] {str(e).encode('ascii', 'replace').decode()}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
