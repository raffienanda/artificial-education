"""
Comprehensive Database Seeder for Artificial Education
Seeds all modules, subtopics, questions, and user progress from frontend dummy data.
"""
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.migrations import ensure_runtime_columns
from app.models.user import User
from app.models.module import Course, Module, Subtopic
from app.models.question import Question
from app.models.progress import UserProgress
from app.models.learning_path import TopicPrerequisite
from app.core.security import hash_password


def seed_all():
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    ensure_runtime_columns(engine)
    db = SessionLocal()

    try:
        # ==============================
        # 1. Seed User
        # ==============================
        user = db.query(User).filter(User.username == "student_cs").first()
        if not user:
            user = User(
                username="student_cs",
                display_name="Student CS",
                password_hash=hash_password("password123"),
                role="student",
                xp=500,
                combo=0,
                total_score=0,
                reward_points=75,
                current_streak=1,
                longest_streak=1,
                redeemed_rewards=[],
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("[+] User 'student_cs' created")
        else:
            user.display_name = user.display_name or "Student CS"
            user.password_hash = user.password_hash or hash_password("password123")
            user.role = user.role or "student"
            user.reward_points = user.reward_points or 75
            user.current_streak = user.current_streak or 1
            user.longest_streak = user.longest_streak or user.current_streak
            user.redeemed_rewards = user.redeemed_rewards or []
            print("[=] User 'student_cs' already exists")

        admin_user = db.query(User).filter(User.username == "dosen_demo").first()
        if not admin_user:
            admin_user = User(
                username="dosen_demo",
                display_name="Dosen Demo",
                password_hash=hash_password("admin123"),
                role="admin",
                xp=0,
                combo=0,
                total_score=0,
                reward_points=0,
                current_streak=0,
                longest_streak=0,
                redeemed_rewards=[],
            )
            db.add(admin_user)
            db.commit()
            print("[+] Admin user 'dosen_demo' created")
        else:
            admin_user.display_name = admin_user.display_name or "Dosen Demo"
            admin_user.password_hash = admin_user.password_hash or hash_password("admin123")
            admin_user.role = "admin"
            admin_user.reward_points = admin_user.reward_points or 0
            admin_user.current_streak = admin_user.current_streak or 0
            admin_user.longest_streak = admin_user.longest_streak or 0
            admin_user.redeemed_rewards = admin_user.redeemed_rewards or []
            print("[=] Admin user 'dosen_demo' already exists")

        # ==============================
        # 2. Seed Course, Modules & Subtopics
        # ==============================
        course = db.query(Course).filter(Course.id == "course-algo-01").first()
        if not course:
            course = Course(
                id="course-algo-01",
                title="Algoritma dan Pemrograman",
                description="Kuasai dasar-dasar algoritma dan pemrograman melalui pembelajaran adaptif berbasis AI",
                icon="computer",
            )
            db.add(course)
            db.commit()
            print("[+] Course 'Algoritma dan Pemrograman' created")
        else:
            course.title = "Algoritma dan Pemrograman"
            course.description = "Kuasai dasar-dasar algoritma dan pemrograman melalui pembelajaran adaptif berbasis AI"
            course.icon = "computer"
            db.commit()
            print("[=] Course 'Algoritma dan Pemrograman' already exists")

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
                "status": "in-progress",
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
                    course_id=course.id,
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
                existing_mod.title = mod_data["title"]
                existing_mod.course_id = course.id
                existing_mod.icon = mod_data["icon"]
                existing_mod.description = mod_data["description"]
                existing_mod.difficulty = mod_data["difficulty"]
                existing_mod.estimated_time = mod_data["estimated_time"]
                existing_mod.order = mod_data["order"]
                existing_mod.status = mod_data["status"]
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

        example_sections = {
            "sub-001-3": {
                "type": "example",
                "title": "Contoh Ekspresi",
                "items": [
                    "harga = 5000\njumlah = 3\ntotal = harga * jumlah\nprint(total)  # 15000",
                    "sisa = 17 % 5\nprint(sisa)  # 2",
                ],
            },
            "sub-001-5": {
                "type": "example",
                "title": "Contoh Type Casting",
                "items": [
                    "umur_text = \"20\"\numur = int(umur_text)\nprint(umur + 1)  # 21",
                    "nilai = \"87.5\"\nnilai_float = float(nilai)\nprint(nilai_float)  # 87.5",
                ],
            },
            "sub-002-1": {
                "type": "example",
                "title": "Contoh Kondisi Logika",
                "items": [
                    "umur = 19\npunya_ktp = True\nif umur >= 17 and punya_ktp:\n    print(\"Boleh daftar\")",
                    "nilai = 80\nif nilai >= 75:\n    print(\"Lulus\")",
                ],
            },
            "sub-002-3": {
                "type": "example",
                "title": "Contoh Kategori Nilai",
                "items": [
                    "skor = 68\nif skor >= 80:\n    print(\"Sangat Baik\")\nelif skor >= 60:\n    print(\"Baik\")\nelse:\n    print(\"Perlu Latihan\")",
                ],
            },
            "sub-003-1": {
                "type": "example",
                "title": "Contoh Perulangan for",
                "items": [
                    "for i in range(1, 6):\n    print(i)  # 1 sampai 5",
                    "buah = [\"apel\", \"jeruk\", \"mangga\"]\nfor item in buah:\n    print(item)",
                ],
            },
            "sub-003-2": {
                "type": "example",
                "title": "Contoh Perulangan while",
                "items": [
                    "angka = 1\nwhile angka <= 3:\n    print(angka)\n    angka += 1",
                    "password = \"\"\nwhile password != \"1234\":\n    password = input(\"Password: \")\nprint(\"Berhasil\")",
                ],
            },
        }

        for subtopic_id, example_section in example_sections.items():
            subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()
            if not subtopic:
                continue
            content = dict(subtopic.content or {})
            sections = list(content.get("sections") or [])
            sections = [section for section in sections if section.get("type") != "example"]
            sections.append(example_section)
            content["sections"] = sections
            subtopic.content = content
            print(f"[~] Example section for '{subtopic_id}' synced")
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
            },
            {
                "id": "q-008",
                "subtopic_id": "sub-001-1",
                "question_text": "Apa pengertian algoritma yang paling tepat?",
                "options": [
                    {"id": "a", "text": "Bahasa pemrograman khusus untuk membuat website", "label": "A"},
                    {"id": "b", "text": "Urutan langkah logis untuk menyelesaikan masalah", "label": "B"},
                    {"id": "c", "text": "Aplikasi untuk menjalankan kode Python", "label": "C"},
                    {"id": "d", "text": "Kumpulan error dalam sebuah program", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Algoritma adalah urutan langkah logis dan sistematis untuk menyelesaikan masalah.",
                "difficulty": "mudah"
            },
            {
                "id": "q-009",
                "subtopic_id": "sub-001-1",
                "question_text": "Urutan umum pengembangan program yang paling masuk akal adalah...",
                "options": [
                    {"id": "a", "text": "Coding, testing, memahami masalah, desain algoritma", "label": "A"},
                    {"id": "b", "text": "Memahami masalah, desain algoritma, coding, testing", "label": "B"},
                    {"id": "c", "text": "Testing, coding, desain algoritma, memahami masalah", "label": "C"},
                    {"id": "d", "text": "Dokumentasi, testing, coding, memahami masalah", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Program sebaiknya dimulai dari memahami masalah, merancang algoritma, menulis kode, lalu menguji hasilnya.",
                "difficulty": "sedang"
            },
            {
                "id": "q-010",
                "subtopic_id": "sub-001-2",
                "question_text": "Tipe data yang cocok untuk menyimpan nilai True atau False adalah...",
                "options": [
                    {"id": "a", "text": "int", "label": "A"},
                    {"id": "b", "text": "float", "label": "B"},
                    {"id": "c", "text": "bool", "label": "C"},
                    {"id": "d", "text": "str", "label": "D"}
                ],
                "correct_answer": "c",
                "explanation": "Boolean atau bool digunakan untuk menyimpan nilai logika True atau False.",
                "difficulty": "mudah"
            },
            {
                "id": "q-011",
                "subtopic_id": "sub-001-3",
                "question_text": "Berapakah hasil dari ekspresi Python berikut?\n\n2 + 3 * 4",
                "options": [
                    {"id": "a", "text": "20", "label": "A"},
                    {"id": "b", "text": "14", "label": "B"},
                    {"id": "c", "text": "24", "label": "C"},
                    {"id": "d", "text": "9", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Perkalian dikerjakan lebih dulu. 3 * 4 = 12, lalu 2 + 12 = 14.",
                "difficulty": "mudah"
            },
            {
                "id": "q-012",
                "subtopic_id": "sub-001-4",
                "question_text": "Fungsi Python yang digunakan untuk menerima input dari keyboard adalah...",
                "options": [
                    {"id": "a", "text": "print()", "label": "A"},
                    {"id": "b", "text": "input()", "label": "B"},
                    {"id": "c", "text": "scan()", "label": "C"},
                    {"id": "d", "text": "readline()", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "input() digunakan untuk menerima masukan dari pengguna melalui keyboard.",
                "difficulty": "mudah"
            },
            {
                "id": "q-013",
                "subtopic_id": "sub-001-4",
                "question_text": "Apa output dari kode berikut jika pengguna mengetik Budi?\n\nnama = input('Nama: ')\nprint('Halo,', nama)",
                "options": [
                    {"id": "a", "text": "Halo, nama", "label": "A"},
                    {"id": "b", "text": "Halo, Budi", "label": "B"},
                    {"id": "c", "text": "Nama: Budi", "label": "C"},
                    {"id": "d", "text": "Error", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Nilai input disimpan ke variabel nama, lalu print menampilkan Halo, Budi.",
                "difficulty": "sedang"
            },
            {
                "id": "q-014",
                "subtopic_id": "sub-001-5",
                "question_text": "Manakah kode yang benar untuk mengubah string '25' menjadi integer di Python?",
                "options": [
                    {"id": "a", "text": "str('25')", "label": "A"},
                    {"id": "b", "text": "int('25')", "label": "B"},
                    {"id": "c", "text": "float_int('25')", "label": "C"},
                    {"id": "d", "text": "bool('25')", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "int('25') mengubah string angka menjadi integer 25.",
                "difficulty": "mudah"
            },
            {
                "id": "q-015",
                "subtopic_id": "sub-002-1",
                "question_text": "Operator perbandingan untuk 'tidak sama dengan' di Python adalah...",
                "options": [
                    {"id": "a", "text": "!=", "label": "A"},
                    {"id": "b", "text": "==", "label": "B"},
                    {"id": "c", "text": "<=", "label": "C"},
                    {"id": "d", "text": "=>", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Operator != digunakan untuk mengecek apakah dua nilai tidak sama.",
                "difficulty": "mudah"
            },
            {
                "id": "q-016",
                "subtopic_id": "sub-002-4",
                "question_text": "Apa yang dimaksud dengan nested if?",
                "options": [
                    {"id": "a", "text": "Loop yang berhenti otomatis", "label": "A"},
                    {"id": "b", "text": "Percabangan if yang berada di dalam if lain", "label": "B"},
                    {"id": "c", "text": "Variabel yang menyimpan banyak nilai", "label": "C"},
                    {"id": "d", "text": "Fungsi untuk mencetak output", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Nested if adalah percabangan if di dalam blok if lain.",
                "difficulty": "mudah"
            },
            {
                "id": "q-017",
                "subtopic_id": "sub-002-4",
                "question_text": "Pada validasi login, nested if cocok digunakan ketika...",
                "options": [
                    {"id": "a", "text": "Pengecekan password dilakukan setelah username benar", "label": "A"},
                    {"id": "b", "text": "Semua kondisi harus diabaikan", "label": "B"},
                    {"id": "c", "text": "Program hanya mencetak satu teks", "label": "C"},
                    {"id": "d", "text": "Tidak ada kondisi yang saling bergantung", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Nested if berguna saat kondisi kedua bergantung pada hasil kondisi pertama.",
                "difficulty": "sedang"
            },
            {
                "id": "q-018",
                "subtopic_id": "sub-002-5",
                "question_text": "Pada kalkulator sederhana, percabangan biasanya dipakai untuk...",
                "options": [
                    {"id": "a", "text": "Memilih operasi berdasarkan operator yang dimasukkan", "label": "A"},
                    {"id": "b", "text": "Menghapus semua variabel", "label": "B"},
                    {"id": "c", "text": "Mengubah Python menjadi C++", "label": "C"},
                    {"id": "d", "text": "Menghentikan komputer", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Percabangan dapat menentukan operasi mana yang dijalankan, misalnya tambah, kurang, kali, atau bagi.",
                "difficulty": "mudah"
            },
            {
                "id": "q-019",
                "subtopic_id": "sub-002-5",
                "question_text": "Mengapa pembagian dengan nol perlu dicek pada studi kasus kalkulator?",
                "options": [
                    {"id": "a", "text": "Karena hasilnya selalu 1", "label": "A"},
                    {"id": "b", "text": "Karena dapat menyebabkan error atau operasi tidak valid", "label": "B"},
                    {"id": "c", "text": "Karena membuat string menjadi integer", "label": "C"},
                    {"id": "d", "text": "Karena operator / tidak bisa dipakai", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Pembagian dengan nol tidak valid, sehingga program perlu menangani kondisi tersebut.",
                "difficulty": "sedang"
            },
            {
                "id": "q-020",
                "subtopic_id": "sub-003-2",
                "question_text": "Perulangan while akan terus berjalan selama...",
                "options": [
                    {"id": "a", "text": "Kondisinya bernilai True", "label": "A"},
                    {"id": "b", "text": "Kondisinya bernilai False", "label": "B"},
                    {"id": "c", "text": "Tidak ada variabel", "label": "C"},
                    {"id": "d", "text": "Program tidak memiliki input", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "while mengeksekusi blok kode selama kondisi bernilai True.",
                "difficulty": "mudah"
            },
            {
                "id": "q-021",
                "subtopic_id": "sub-003-2",
                "question_text": "Apa risiko utama jika kondisi while tidak pernah menjadi False?",
                "options": [
                    {"id": "a", "text": "Syntax error", "label": "A"},
                    {"id": "b", "text": "Infinite loop", "label": "B"},
                    {"id": "c", "text": "Variabel otomatis terhapus", "label": "C"},
                    {"id": "d", "text": "Semua output menjadi kosong", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Jika kondisi while selalu True, loop dapat berjalan tanpa henti atau infinite loop.",
                "difficulty": "sedang"
            },
            {
                "id": "q-022",
                "subtopic_id": "sub-003-3",
                "question_text": "Keyword yang digunakan untuk menghentikan loop sepenuhnya adalah...",
                "options": [
                    {"id": "a", "text": "continue", "label": "A"},
                    {"id": "b", "text": "break", "label": "B"},
                    {"id": "c", "text": "skip", "label": "C"},
                    {"id": "d", "text": "pass", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "break digunakan untuk keluar dari loop secara langsung.",
                "difficulty": "mudah"
            },
            {
                "id": "q-023",
                "subtopic_id": "sub-003-3",
                "question_text": "Apa fungsi keyword continue di dalam loop?",
                "options": [
                    {"id": "a", "text": "Menghentikan seluruh program", "label": "A"},
                    {"id": "b", "text": "Melewati sisa kode pada iterasi saat ini dan lanjut ke iterasi berikutnya", "label": "B"},
                    {"id": "c", "text": "Mengubah tipe data menjadi integer", "label": "C"},
                    {"id": "d", "text": "Mencetak output ke layar", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "continue melewati sisa proses pada iterasi berjalan, lalu loop lanjut ke iterasi berikutnya.",
                "difficulty": "sedang"
            },
            {
                "id": "q-024",
                "subtopic_id": "sub-003-4",
                "question_text": "Nested loop adalah...",
                "options": [
                    {"id": "a", "text": "Loop di dalam loop lain", "label": "A"},
                    {"id": "b", "text": "If di dalam if lain", "label": "B"},
                    {"id": "c", "text": "Variabel tanpa nilai", "label": "C"},
                    {"id": "d", "text": "Input yang selalu salah", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Nested loop berarti terdapat loop yang dijalankan di dalam loop lain.",
                "difficulty": "mudah"
            },
            {
                "id": "q-025",
                "subtopic_id": "sub-003-4",
                "question_text": "Nested loop sering dipakai untuk memproses data berbentuk...",
                "options": [
                    {"id": "a", "text": "Satu angka tunggal saja", "label": "A"},
                    {"id": "b", "text": "Tabel, matriks, atau pola baris-kolom", "label": "B"},
                    {"id": "c", "text": "Password terenkripsi", "label": "C"},
                    {"id": "d", "text": "Nama file program", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Nested loop cocok untuk struktur dua dimensi seperti tabel, matriks, dan pola.",
                "difficulty": "sedang"
            },
            {
                "id": "q-026",
                "subtopic_id": "sub-003-5",
                "question_text": "Pada perhitungan faktorial 5!, operasi utama yang dilakukan adalah...",
                "options": [
                    {"id": "a", "text": "5 + 4 + 3 + 2 + 1", "label": "A"},
                    {"id": "b", "text": "5 * 4 * 3 * 2 * 1", "label": "B"},
                    {"id": "c", "text": "5 / 4 / 3 / 2 / 1", "label": "C"},
                    {"id": "d", "text": "5 - 4 - 3 - 2 - 1", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Faktorial adalah hasil perkalian bilangan dari n sampai 1. Jadi 5! = 5 * 4 * 3 * 2 * 1.",
                "difficulty": "mudah"
            },
            {
                "id": "q-027",
                "subtopic_id": "sub-003-5",
                "question_text": "Dalam algoritma cek bilangan prima, mengapa kita perlu mencari faktor pembagi?",
                "options": [
                    {"id": "a", "text": "Karena bilangan prima punya pembagi selain 1 dan dirinya sendiri", "label": "A"},
                    {"id": "b", "text": "Karena bilangan prima tidak boleh punya pembagi selain 1 dan dirinya sendiri", "label": "B"},
                    {"id": "c", "text": "Karena semua bilangan prima harus genap", "label": "C"},
                    {"id": "d", "text": "Karena angka 1 selalu prima", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Bilangan prima hanya memiliki dua pembagi, yaitu 1 dan dirinya sendiri. Jika ada faktor lain, maka bukan prima.",
                "difficulty": "sedang"
            },
            {
                "id": "q-028",
                "subtopic_id": "sub-002-2",
                "question_text": "Pada struktur if-else, blok else akan dijalankan ketika...",
                "options": [
                    {"id": "a", "text": "Kondisi if bernilai True", "label": "A"},
                    {"id": "b", "text": "Kondisi if bernilai False", "label": "B"},
                    {"id": "c", "text": "Program belum memiliki variabel", "label": "C"},
                    {"id": "d", "text": "Input selalu berupa angka", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Blok else menjadi jalur alternatif ketika kondisi if tidak terpenuhi atau bernilai False.",
                "difficulty": "sedang"
            },
            {
                "id": "q-029",
                "subtopic_id": "sub-002-3",
                "question_text": "Pada rangkaian if-elif-else, apa yang terjadi setelah salah satu kondisi elif bernilai True?",
                "options": [
                    {"id": "a", "text": "Semua kondisi berikutnya tetap diperiksa", "label": "A"},
                    {"id": "b", "text": "Program langsung keluar dari seluruh aplikasi", "label": "B"},
                    {"id": "c", "text": "Blok kondisi tersebut dijalankan dan kondisi berikutnya dilewati", "label": "C"},
                    {"id": "d", "text": "Nilai variabel otomatis menjadi nol", "label": "D"}
                ],
                "correct_answer": "c",
                "explanation": "Pada if-elif-else, setelah satu kondisi terpenuhi, bloknya dijalankan dan kondisi di bawahnya tidak diperiksa lagi.",
                "difficulty": "mudah"
            },
            {
                "id": "q-030",
                "subtopic_id": "sub-003-1",
                "question_text": "Perulangan for paling cocok digunakan ketika...",
                "options": [
                    {"id": "a", "text": "Jumlah iterasi sudah diketahui atau datanya bisa diiterasi", "label": "A"},
                    {"id": "b", "text": "Program tidak membutuhkan kondisi apa pun", "label": "B"},
                    {"id": "c", "text": "Kita hanya ingin membuat variabel string", "label": "C"},
                    {"id": "d", "text": "Semua input harus ditolak", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "for cocok untuk mengulang berdasarkan range atau koleksi data yang dapat diiterasi.",
                "difficulty": "mudah"
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

        # ==============================
        # 5. Seed Topic Prerequisite Graph for GKT
        # ==============================
        prerequisite_data = [
            {"topic_id": "mod-002", "prerequisite_id": "mod-001", "mastery_threshold": 60.0},
            {"topic_id": "mod-003", "prerequisite_id": "mod-002", "mastery_threshold": 60.0},
        ]

        for relation in prerequisite_data:
            existing_relation = db.query(TopicPrerequisite).filter(
                TopicPrerequisite.topic_id == relation["topic_id"],
                TopicPrerequisite.prerequisite_id == relation["prerequisite_id"],
            ).first()

            if not existing_relation:
                db.add(TopicPrerequisite(**relation))
                print(f"[+] Prerequisite {relation['prerequisite_id']} -> {relation['topic_id']} created")
            else:
                existing_relation.mastery_threshold = relation["mastery_threshold"]
                print(f"[=] Prerequisite {relation['prerequisite_id']} -> {relation['topic_id']} already exists")

        db.commit()
        print("\n[OK] Database seeding complete!")
        print(f"   Modules: {db.query(Module).count()}")
        print(f"   Subtopics: {db.query(Subtopic).count()}")
        print(f"   Questions: {db.query(Question).count()}")
        print(f"   User Progress: {db.query(UserProgress).count()}")
        print(f"   Topic Prerequisites: {db.query(TopicPrerequisite).count()}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] {str(e).encode('ascii', 'replace').decode()}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
