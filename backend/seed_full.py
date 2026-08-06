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
import app.models
from app.models.user import User
from app.models.module import Course, Module, Subtopic
from app.models.question import Question
from app.models.progress import UserProgress
from app.models.assessment import AssessmentAnswer
from app.models.cognitive import CognitiveItem
from app.models.knowledge import KnowledgeEdge
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

        additional_courses = [
            {
                "id": "course-db-01",
                "title": "Basis Data",
                "description": "Pelajari konsep database, relasi tabel, SQL dasar, dan perancangan data.",
                "icon": "database",
            },
            {
                "id": "course-web-01",
                "title": "Pemrograman Web",
                "description": "Pelajari struktur web, HTML, CSS, JavaScript, dan dasar pengembangan frontend.",
                "icon": "globe",
            },
            {
                "id": "course-ml-01",
                "title": "Pengantar Machine Learning",
                "description": "Kenali konsep data, model, training, evaluasi, dan penerapan machine learning sederhana.",
                "icon": "brain",
            },
        ]
        for course_data in additional_courses:
            extra_course = db.query(Course).filter(Course.id == course_data["id"]).first()
            if not extra_course:
                db.add(Course(**course_data))
                print(f"[+] Course '{course_data['title']}' created")
            else:
                extra_course.title = course_data["title"]
                extra_course.description = course_data["description"]
                extra_course.icon = course_data["icon"]
                print(f"[=] Course '{course_data['title']}' already exists")
        db.commit()

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

        lesson_tabs = [
            {"id": "ringkasan", "label": "Ringkasan Materi", "icon": "📖"},
            {"id": "video", "label": "Video Pembelajaran", "icon": "▶️"},
            {"id": "contoh", "label": "Contoh Soal", "icon": "📝"},
        ]

        def lesson_content(title, summary, key_title, key_points, example_title, examples, video_focus):
            return {
                "title": title,
                "tabs": lesson_tabs,
                "sections": [
                    {"type": "text", "content": summary},
                    {
                        "type": "formula",
                        "title": key_title,
                        "content": "\n".join(key_points),
                        "description": "Gunakan poin ini sebagai pegangan sebelum mengerjakan quiz subtopik.",
                    },
                    {
                        "type": "video",
                        "title": f"Video: {title}",
                        "duration": "6:00",
                        "description": video_focus,
                    },
                    {
                        "type": "example",
                        "title": example_title,
                        "items": examples,
                    },
                ],
            }

        lesson_materials = {
            "sub-001-1": lesson_content(
                "Pengantar Algoritma dan Program",
                "Algoritma adalah rancangan langkah untuk menyelesaikan masalah secara runtut. Program adalah bentuk implementasi algoritma memakai bahasa pemrograman agar komputer bisa menjalankan instruksi tersebut. Sebelum menulis kode, mahasiswa perlu memahami masalah, menentukan input-output, menyusun langkah, lalu menguji hasilnya.",
                "Alur Membuat Program",
                [
                    "1. Pahami masalah dan tujuan program",
                    "2. Tentukan input, proses, dan output",
                    "3. Susun algoritma dalam bahasa natural, pseudocode, atau flowchart",
                    "4. Ubah algoritma menjadi kode program",
                    "5. Jalankan, uji, dan perbaiki kesalahan",
                ],
                "Contoh Alur Sederhana",
                [
                    "Masalah: menampilkan sapaan.\nAlgoritma: mulai -> siapkan teks -> tampilkan teks -> selesai.",
                    "Python:\nnama = input(\"Nama: \")\nprint(\"Halo,\", nama)",
                ],
                "Video menjelaskan bedanya masalah, algoritma, pseudocode, flowchart, dan program.",
            ),
            "sub-001-2": lesson_content(
                "Variabel dan Tipe Data",
                "Variabel adalah tempat menyimpan nilai agar bisa dipakai kembali oleh program. Tipe data menjelaskan jenis nilai yang disimpan, misalnya bilangan bulat, bilangan desimal, teks, atau nilai logika. Penamaan variabel sebaiknya jelas supaya kode mudah dibaca.",
                "Tipe Data Dasar",
                [
                    "int: bilangan bulat, contoh 10",
                    "float: bilangan desimal, contoh 3.75",
                    "str: teks, contoh \"Algoritma\"",
                    "bool: True atau False",
                    "Gunakan nama variabel yang menggambarkan isinya",
                ],
                "Contoh Deklarasi",
                [
                    "nama = \"Rani\"\numur = 19\nipk = 3.65\naktif = True",
                    "total = 0\nharga_barang = 15000\njumlah_barang = 3",
                ],
                "Video mencontohkan cara memilih tipe data sesuai kebutuhan program.",
            ),
            "sub-001-3": lesson_content(
                "Operasi Aritmatika dan Ekspresi",
                "Operasi aritmatika digunakan untuk mengolah nilai numerik. Ekspresi adalah gabungan nilai, variabel, dan operator yang menghasilkan nilai baru. Urutan operasi tetap mengikuti prioritas seperti matematika: kurung, pangkat, kali/bagi, lalu tambah/kurang.",
                "Operator Penting",
                [
                    "+ untuk penjumlahan",
                    "- untuk pengurangan",
                    "* untuk perkalian",
                    "/ untuk pembagian desimal",
                    "// untuk pembagian bulat",
                    "% untuk sisa bagi",
                    "** untuk pangkat",
                ],
                "Contoh Ekspresi",
                [
                    "harga = 5000\njumlah = 3\ntotal = harga * jumlah\nprint(total)  # 15000",
                    "hasil = 2 + 3 * 4\nprint(hasil)  # 14",
                ],
                "Video membahas prioritas operator dan cara membaca ekspresi bertingkat.",
            ),
            "sub-001-4": lesson_content(
                "Input dan Output",
                "Input adalah data yang diberikan pengguna ke program. Output adalah hasil yang ditampilkan program. Pada Python, input() membaca data sebagai string, sehingga data angka perlu dikonversi dulu sebelum dihitung.",
                "Pola Input dan Output",
                [
                    "Gunakan input() untuk mengambil masukan",
                    "Gunakan print() untuk menampilkan keluaran",
                    "input() menghasilkan string",
                    "Konversi input angka dengan int() atau float() sebelum operasi hitung",
                ],
                "Contoh Program Interaktif",
                [
                    "nama = input(\"Nama: \")\nprint(\"Halo,\", nama)",
                    "umur = int(input(\"Umur: \"))\nprint(\"Tahun depan:\", umur + 1)",
                ],
                "Video memperlihatkan alur program interaktif dari input, proses, sampai output.",
            ),
            "sub-001-5": lesson_content(
                "Konversi Tipe Data (Type Casting)",
                "Type casting adalah proses mengubah nilai dari satu tipe data ke tipe lain. Konversi sering dibutuhkan saat input berbentuk teks tetapi perlu diproses sebagai angka. Konversi harus dilakukan hati-hati karena nilai yang tidak valid dapat menyebabkan error.",
                "Fungsi Konversi",
                [
                    "int(\"42\") menjadi 42",
                    "float(\"3.14\") menjadi 3.14",
                    "str(100) menjadi \"100\"",
                    "bool(0) menjadi False",
                    "int(\"3.14\") error, gunakan int(float(\"3.14\")) jika memang perlu",
                ],
                "Contoh Type Casting",
                [
                    "angka_text = \"25\"\nangka = int(angka_text)\nprint(angka + 5)  # 30",
                    "nilai = float(input(\"Nilai: \"))\nprint(nilai >= 75)",
                ],
                "Video menjelaskan kapan data perlu dikonversi dan error yang sering muncul.",
            ),
            "sub-002-1": lesson_content(
                "Operator Perbandingan dan Logika",
                "Operator perbandingan menghasilkan nilai True atau False. Operator logika menggabungkan beberapa kondisi agar program bisa mengambil keputusan yang lebih kompleks.",
                "Operator yang Sering Dipakai",
                [
                    "== untuk sama dengan",
                    "!= untuk tidak sama dengan",
                    "> dan < untuk lebih besar atau lebih kecil",
                    ">= dan <= untuk batas inklusif",
                    "and bernilai True jika semua kondisi True",
                    "or bernilai True jika minimal satu kondisi True",
                    "not membalik nilai boolean",
                ],
                "Contoh Kondisi",
                [
                    "umur = 19\npunya_ktp = True\nboleh_daftar = umur >= 17 and punya_ktp",
                    "nilai = 68\nremedial = nilai < 70",
                ],
                "Video mengurai ekspresi boolean langkah demi langkah.",
            ),
            "sub-002-2": lesson_content(
                "Percabangan if dan if-else",
                "Percabangan membuat program memilih jalur berdasarkan kondisi. Blok if berjalan ketika kondisi True, sedangkan else menjadi jalur alternatif ketika kondisi False.",
                "Pola if-else",
                [
                    "Tulis kondisi yang menghasilkan True atau False",
                    "Gunakan indentasi untuk blok kode Python",
                    "else tidak memakai kondisi",
                    "Pastikan setiap jalur menghasilkan output yang jelas",
                ],
                "Contoh if-else",
                [
                    "umur = int(input(\"Umur: \"))\nif umur >= 18:\n    print(\"Dewasa\")\nelse:\n    print(\"Belum dewasa\")",
                    "angka = -3\nif angka >= 0:\n    print(\"Non-negatif\")\nelse:\n    print(\"Negatif\")",
                ],
                "Video menunjukkan cara membaca alur True dan False pada if-else.",
            ),
            "sub-002-3": lesson_content(
                "Percabangan Bertingkat (elif / else-if)",
                "elif digunakan ketika program memiliki lebih dari dua kemungkinan keputusan. Kondisi diperiksa dari atas ke bawah, dan ketika satu kondisi terpenuhi, kondisi berikutnya tidak diperiksa lagi.",
                "Cara Menyusun elif",
                [
                    "Letakkan kondisi paling spesifik atau paling tinggi di atas",
                    "Gunakan elif untuk pilihan tambahan",
                    "Gunakan else sebagai pilihan terakhir",
                    "Hindari kondisi yang saling tumpang tindih tanpa sengaja",
                ],
                "Contoh Kategori Nilai",
                [
                    "skor = 78\nif skor >= 85:\n    grade = \"A\"\nelif skor >= 70:\n    grade = \"B\"\nelif skor >= 55:\n    grade = \"C\"\nelse:\n    grade = \"D\"\nprint(grade)",
                ],
                "Video membahas kenapa urutan kondisi pada elif sangat penting.",
            ),
            "sub-002-4": lesson_content(
                "Percabangan Bersarang (Nested If)",
                "Nested if adalah percabangan di dalam percabangan lain. Struktur ini cocok ketika keputusan kedua baru boleh dicek setelah keputusan pertama terpenuhi. Gunakan secukupnya agar kode tetap mudah dibaca.",
                "Kapan Nested If Dipakai",
                [
                    "Saat validasi tahap kedua bergantung pada tahap pertama",
                    "Saat kondisi memiliki hubungan bertingkat",
                    "Saat satu aksi hanya boleh berjalan setelah syarat utama lolos",
                    "Jika terlalu dalam, pertimbangkan operator logika atau fungsi terpisah",
                ],
                "Contoh Validasi Login",
                [
                    "username = input(\"Username: \")\npassword = input(\"Password: \")\nif username == \"admin\":\n    if password == \"1234\":\n        print(\"Login berhasil\")\n    else:\n        print(\"Password salah\")\nelse:\n    print(\"Username tidak ditemukan\")",
                ],
                "Video menampilkan alur nested if dalam bentuk pohon keputusan.",
            ),
            "sub-002-5": lesson_content(
                "Studi Kasus Percabangan",
                "Percabangan sering dipakai untuk membuat program responsif terhadap pilihan pengguna, seperti kalkulator, sistem nilai, validasi login, atau validasi input. Pada studi kasus, fokus utamanya adalah memilih kondisi yang benar dan menangani kondisi tidak valid.",
                "Langkah Membangun Studi Kasus",
                [
                    "Tentukan pilihan atau kondisi yang mungkin terjadi",
                    "Buat jalur if, elif, dan else",
                    "Tangani input tidak valid",
                    "Uji setiap cabang minimal satu kali",
                ],
                "Contoh Kalkulator",
                [
                    "a = float(input(\"Angka pertama: \"))\nop = input(\"Operator: \")\nb = float(input(\"Angka kedua: \"))\nif op == \"+\":\n    print(a + b)\nelif op == \"/\" and b != 0:\n    print(a / b)\nelse:\n    print(\"Operasi tidak valid\")",
                ],
                "Video menggabungkan if, elif, else, dan validasi pada kasus kalkulator.",
            ),
            "sub-003-1": lesson_content(
                "Perulangan for",
                "Perulangan for digunakan ketika jumlah pengulangan sudah diketahui atau data yang diproses bisa diiterasi. Di Python, for sering dipakai bersama range(), list, string, atau koleksi data lain.",
                "Pola for",
                [
                    "range(5) menghasilkan 0 sampai 4",
                    "range(1, 6) menghasilkan 1 sampai 5",
                    "range(start, stop, step) memakai batas stop yang tidak ikut",
                    "for juga bisa membaca item dalam list satu per satu",
                ],
                "Contoh for",
                [
                    "for i in range(1, 6):\n    print(i)",
                    "buah = [\"apel\", \"jeruk\", \"mangga\"]\nfor item in buah:\n    print(item)",
                ],
                "Video menjelaskan range dan iterasi list dengan visual urutan angka.",
            ),
            "sub-003-2": lesson_content(
                "Perulangan while",
                "Perulangan while berjalan selama kondisi masih True. while cocok ketika jumlah pengulangan belum pasti, misalnya menunggu input valid atau mengulang sampai target tercapai.",
                "Hal yang Harus Dijaga",
                [
                    "Kondisi harus bisa berubah menjadi False",
                    "Perbarui variabel kontrol di dalam loop",
                    "Gunakan while untuk kasus berbasis kondisi",
                    "Waspadai infinite loop jika kondisi tidak pernah berubah",
                ],
                "Contoh while",
                [
                    "angka = 1\nwhile angka <= 3:\n    print(angka)\n    angka += 1",
                    "password = \"\"\nwhile password != \"1234\":\n    password = input(\"Password: \")\nprint(\"Berhasil\")",
                ],
                "Video memperlihatkan perubahan variabel kontrol di setiap iterasi while.",
            ),
            "sub-003-3": lesson_content(
                "break, continue, dan else pada Loop",
                "break menghentikan loop sepenuhnya, sedangkan continue melewati sisa proses pada iterasi saat ini dan lanjut ke iterasi berikutnya. Pada Python, else pada loop berjalan jika loop selesai tanpa break.",
                "Kontrol Loop",
                [
                    "break: keluar dari loop",
                    "continue: loncat ke iterasi berikutnya",
                    "else pada loop: berjalan jika loop selesai normal",
                    "Gunakan kontrol loop agar proses pencarian dan filter lebih efisien",
                ],
                "Contoh Kontrol Loop",
                [
                    "for angka in [3, 7, 9]:\n    if angka == 7:\n        print(\"Ketemu\")\n        break",
                    "for i in range(1, 6):\n    if i % 2 == 0:\n        continue\n    print(i)",
                ],
                "Video membandingkan alur break dan continue dalam satu diagram.",
            ),
            "sub-003-4": lesson_content(
                "Perulangan Bersarang (Nested Loop)",
                "Nested loop adalah loop di dalam loop. Loop luar biasanya mengatur baris, sedangkan loop dalam mengatur kolom. Konsep ini sering dipakai untuk tabel, matriks, pola, dan data dua dimensi.",
                "Membaca Nested Loop",
                [
                    "Satu putaran loop luar menjalankan loop dalam sampai selesai",
                    "Jumlah total iterasi sering kali baris dikali kolom",
                    "Gunakan nama variabel yang jelas seperti baris dan kolom",
                    "Perhatikan indentasi agar blok loop tidak tertukar",
                ],
                "Contoh Pola",
                [
                    "for baris in range(1, 4):\n    for kolom in range(baris):\n        print(\"*\", end=\"\")\n    print()",
                    "for i in range(1, 4):\n    for j in range(1, 4):\n        print(i * j, end=\" \")\n    print()",
                ],
                "Video memperlihatkan urutan eksekusi loop luar dan loop dalam.",
            ),
            "sub-003-5": lesson_content(
                "Studi Kasus Perulangan",
                "Perulangan dapat digunakan untuk menyelesaikan masalah algoritmik seperti faktorial, deret Fibonacci, penjumlahan data, dan pengecekan bilangan prima. Kuncinya adalah menentukan nilai awal, kondisi berhenti, dan pembaruan nilai di setiap iterasi.",
                "Pola Penyelesaian",
                [
                    "Tentukan nilai awal",
                    "Tentukan proses yang diulang",
                    "Tentukan kapan pengulangan berhenti",
                    "Simpan hasil sementara jika diperlukan",
                ],
                "Contoh Studi Kasus",
                [
                    "n = 5\nfaktorial = 1\nfor i in range(1, n + 1):\n    faktorial *= i\nprint(faktorial)",
                    "n = 6\na, b = 0, 1\nfor _ in range(n):\n    print(a)\n    a, b = b, a + b",
                ],
                "Video mengaitkan loop dengan pola algoritma faktorial dan Fibonacci.",
            ),
        }

        for subtopic_id, material in lesson_materials.items():
            subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()
            if not subtopic:
                continue
            subtopic.content = material
            print(f"[~] Lesson material for '{subtopic_id}' synced")
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

        questions_data.extend([
            {
                "id": "q-pre-001",
                "subtopic_id": "sub-001-1",
                "question_text": "Pre test Modul 1: Apa tujuan utama algoritma sebelum menulis kode program?",
                "options": [
                    {"id": "a", "text": "Membuat tampilan program menjadi lebih berwarna", "label": "A"},
                    {"id": "b", "text": "Menyusun langkah logis untuk menyelesaikan masalah", "label": "B"},
                    {"id": "c", "text": "Menghapus semua error secara otomatis", "label": "C"},
                    {"id": "d", "text": "Mengganti bahasa Python menjadi bahasa lain", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Algoritma membantu menyusun langkah penyelesaian masalah sebelum program ditulis.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-002",
                "subtopic_id": "sub-001-2",
                "question_text": "Pre test Modul 1: Variabel pada program biasanya dipakai untuk...",
                "options": [
                    {"id": "a", "text": "Menyimpan data yang akan diproses", "label": "A"},
                    {"id": "b", "text": "Menutup program secara paksa", "label": "B"},
                    {"id": "c", "text": "Membuat komputer tidak bisa menerima input", "label": "C"},
                    {"id": "d", "text": "Menghapus seluruh file Python", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Variabel digunakan untuk menyimpan nilai seperti angka, teks, atau hasil perhitungan.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-007",
                "subtopic_id": "sub-001-3",
                "question_text": "Pre test Modul 1: Operator aritmatika digunakan untuk...",
                "options": [
                    {"id": "a", "text": "Menghitung atau mengolah nilai angka", "label": "A"},
                    {"id": "b", "text": "Menghapus semua variabel dari program", "label": "B"},
                    {"id": "c", "text": "Mengubah Python menjadi bahasa lain", "label": "C"},
                    {"id": "d", "text": "Menutup aplikasi secara otomatis", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Operator aritmatika seperti +, -, *, dan / digunakan untuk melakukan perhitungan.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-008",
                "subtopic_id": "sub-001-4",
                "question_text": "Pre test Modul 1: Fungsi input() pada Python digunakan untuk...",
                "options": [
                    {"id": "a", "text": "Menerima data dari pengguna", "label": "A"},
                    {"id": "b", "text": "Mencetak hasil ke layar", "label": "B"},
                    {"id": "c", "text": "Menghentikan program", "label": "C"},
                    {"id": "d", "text": "Membuat komentar program", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "input() dipakai untuk mengambil masukan dari pengguna saat program berjalan.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-009",
                "subtopic_id": "sub-001-5",
                "question_text": "Pre test Modul 1: Output dari print('Halo') adalah...",
                "options": [
                    {"id": "a", "text": "Halo", "label": "A"},
                    {"id": "b", "text": "'Halo'", "label": "B"},
                    {"id": "c", "text": "print", "label": "C"},
                    {"id": "d", "text": "Tidak ada output", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "print('Halo') menampilkan teks Halo ke layar tanpa tanda kutip.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-post-001",
                "subtopic_id": "sub-001-4",
                "question_text": "Post test Modul 1: Apa output dari kode berikut jika input pengguna adalah 8?\n\nangka = int(input())\nprint(angka + 2)",
                "options": [
                    {"id": "a", "text": "82", "label": "A"},
                    {"id": "b", "text": "10", "label": "B"},
                    {"id": "c", "text": "angka + 2", "label": "C"},
                    {"id": "d", "text": "Error", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Input '8' diubah menjadi integer, lalu ditambah 2 sehingga hasilnya 10.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-002",
                "subtopic_id": "sub-001-5",
                "question_text": "Post test Modul 1: Manakah urutan yang benar untuk membaca input angka dan mencetak kuadratnya?",
                "options": [
                    {"id": "a", "text": "n = int(input()); print(n * n)", "label": "A"},
                    {"id": "b", "text": "print(n * n); n = input()", "label": "B"},
                    {"id": "c", "text": "n = print(input()); int(n)", "label": "C"},
                    {"id": "d", "text": "input = n; print(int)", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Nilai perlu dibaca dulu, dikonversi ke integer, lalu baru dihitung dan dicetak.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-pre-003",
                "subtopic_id": "sub-002-1",
                "question_text": "Pre test Modul 2: Percabangan digunakan ketika program perlu...",
                "options": [
                    {"id": "a", "text": "Menjalankan semua perintah tanpa syarat", "label": "A"},
                    {"id": "b", "text": "Memilih aksi berdasarkan kondisi tertentu", "label": "B"},
                    {"id": "c", "text": "Mengulang kode terus menerus", "label": "C"},
                    {"id": "d", "text": "Mengubah file menjadi database", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Percabangan membuat program memilih jalur eksekusi sesuai kondisi.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-004",
                "subtopic_id": "sub-002-2",
                "question_text": "Pre test Modul 2: Ekspresi 7 > 3 menghasilkan nilai...",
                "options": [
                    {"id": "a", "text": "True", "label": "A"},
                    {"id": "b", "text": "False", "label": "B"},
                    {"id": "c", "text": "None", "label": "C"},
                    {"id": "d", "text": "Error", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Karena 7 memang lebih besar dari 3, hasil ekspresinya True.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-010",
                "subtopic_id": "sub-002-3",
                "question_text": "Pre test Modul 2: Operator and menghasilkan True jika...",
                "options": [
                    {"id": "a", "text": "Semua kondisi bernilai True", "label": "A"},
                    {"id": "b", "text": "Salah satu kondisi bernilai False", "label": "B"},
                    {"id": "c", "text": "Program tidak punya kondisi", "label": "C"},
                    {"id": "d", "text": "Variabel belum dibuat", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Operator and hanya menghasilkan True jika semua kondisi yang dibandingkan bernilai True.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-011",
                "subtopic_id": "sub-002-4",
                "question_text": "Pre test Modul 2: Nested if berarti...",
                "options": [
                    {"id": "a", "text": "Percabangan if di dalam percabangan lain", "label": "A"},
                    {"id": "b", "text": "Perulangan tanpa kondisi", "label": "B"},
                    {"id": "c", "text": "Variabel yang menyimpan teks", "label": "C"},
                    {"id": "d", "text": "Operator untuk pembagian", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Nested if adalah struktur if yang berada di dalam blok if atau else lain.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-012",
                "subtopic_id": "sub-002-5",
                "question_text": "Pre test Modul 2: Pada kalkulator sederhana, percabangan bisa dipakai untuk...",
                "options": [
                    {"id": "a", "text": "Memilih operasi berdasarkan operator yang dimasukkan", "label": "A"},
                    {"id": "b", "text": "Menghapus semua angka sebelum dihitung", "label": "B"},
                    {"id": "c", "text": "Membuat loop berjalan selamanya", "label": "C"},
                    {"id": "d", "text": "Mengubah input menjadi komentar", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Percabangan dapat memilih aksi berbeda, misalnya tambah, kurang, kali, atau bagi.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-post-003",
                "subtopic_id": "sub-002-3",
                "question_text": "Post test Modul 2: Jika nilai = 90, bagian mana yang dijalankan?\n\nif nilai >= 80:\n    print('lulus')\nelse:\n    print('ulang')",
                "options": [
                    {"id": "a", "text": "lulus", "label": "A"},
                    {"id": "b", "text": "ulang", "label": "B"},
                    {"id": "c", "text": "nilai", "label": "C"},
                    {"id": "d", "text": "Tidak ada output", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Kondisi 90 >= 80 bernilai True, maka blok if dijalankan.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-004",
                "subtopic_id": "sub-002-5",
                "question_text": "Post test Modul 2: Pada kalkulator, kondisi apa yang perlu dicek sebelum operasi pembagian?",
                "options": [
                    {"id": "a", "text": "Apakah pembagi bernilai nol", "label": "A"},
                    {"id": "b", "text": "Apakah operator selalu tambah", "label": "B"},
                    {"id": "c", "text": "Apakah variabel berupa warna", "label": "C"},
                    {"id": "d", "text": "Apakah program sudah punya loop", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Pembagian dengan nol tidak valid, jadi harus dicegah dengan percabangan.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-pre-005",
                "subtopic_id": "sub-003-1",
                "question_text": "Pre test Modul 3: Perulangan dipakai ketika program perlu...",
                "options": [
                    {"id": "a", "text": "Menjalankan proses berulang", "label": "A"},
                    {"id": "b", "text": "Menghapus kondisi if", "label": "B"},
                    {"id": "c", "text": "Membuat variabel tidak bisa diubah", "label": "C"},
                    {"id": "d", "text": "Menjalankan hanya satu baris kode selamanya", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Loop digunakan untuk menjalankan instruksi berulang sesuai jumlah atau kondisi tertentu.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-006",
                "subtopic_id": "sub-003-2",
                "question_text": "Pre test Modul 3: Loop while berjalan selama kondisinya bernilai...",
                "options": [
                    {"id": "a", "text": "True", "label": "A"},
                    {"id": "b", "text": "False", "label": "B"},
                    {"id": "c", "text": "None", "label": "C"},
                    {"id": "d", "text": "String", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "while akan terus berjalan selama kondisi bernilai True.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-013",
                "subtopic_id": "sub-003-3",
                "question_text": "Pre test Modul 3: Perintah break pada loop digunakan untuk...",
                "options": [
                    {"id": "a", "text": "Menghentikan loop sebelum selesai secara normal", "label": "A"},
                    {"id": "b", "text": "Melewati satu iterasi lalu lanjut", "label": "B"},
                    {"id": "c", "text": "Membuat variabel baru", "label": "C"},
                    {"id": "d", "text": "Mencetak semua data", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "break dipakai untuk keluar dari loop ketika kondisi tertentu terpenuhi.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-014",
                "subtopic_id": "sub-003-4",
                "question_text": "Pre test Modul 3: Nested loop adalah...",
                "options": [
                    {"id": "a", "text": "Loop yang berada di dalam loop lain", "label": "A"},
                    {"id": "b", "text": "Kondisi if tanpa else", "label": "B"},
                    {"id": "c", "text": "Input yang selalu berupa teks", "label": "C"},
                    {"id": "d", "text": "Fungsi untuk menghapus layar", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Nested loop berarti sebuah perulangan dijalankan di dalam perulangan lain.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-pre-015",
                "subtopic_id": "sub-003-5",
                "question_text": "Pre test Modul 3: Algoritma faktorial 3! menghitung...",
                "options": [
                    {"id": "a", "text": "3 * 2 * 1", "label": "A"},
                    {"id": "b", "text": "3 + 2 + 1", "label": "B"},
                    {"id": "c", "text": "3 - 2 - 1", "label": "C"},
                    {"id": "d", "text": "3 / 2 / 1", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Faktorial menghitung perkalian berurutan dari angka tersebut sampai 1.",
                "difficulty": "mudah",
                "assessment_type": "pre_test"
            },
            {
                "id": "q-post-005",
                "subtopic_id": "sub-003-3",
                "question_text": "Post test Modul 3: Apa output kode berikut?\n\nfor i in range(3):\n    if i == 1:\n        continue\n    print(i)",
                "options": [
                    {"id": "a", "text": "0 dan 2", "label": "A"},
                    {"id": "b", "text": "0, 1, dan 2", "label": "B"},
                    {"id": "c", "text": "1 saja", "label": "C"},
                    {"id": "d", "text": "Error", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Saat i bernilai 1, continue melewati print, sehingga yang tercetak 0 dan 2.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-006",
                "subtopic_id": "sub-003-5",
                "question_text": "Post test Modul 3: Algoritma faktorial 4! menghasilkan...",
                "options": [
                    {"id": "a", "text": "10", "label": "A"},
                    {"id": "b", "text": "16", "label": "B"},
                    {"id": "c", "text": "24", "label": "C"},
                    {"id": "d", "text": "44", "label": "D"}
                ],
                "correct_answer": "c",
                "explanation": "4! = 4 * 3 * 2 * 1 = 24.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            }
        ])

        questions_data.extend([
            {
                "id": "q-post-007",
                "subtopic_id": "sub-001-1",
                "question_text": "Post test Modul 1: Urutan yang paling tepat sebelum membuat program adalah...",
                "options": [
                    {"id": "a", "text": "Menulis kode dulu, baru memahami masalah", "label": "A"},
                    {"id": "b", "text": "Memahami masalah, membuat algoritma, lalu menulis kode", "label": "B"},
                    {"id": "c", "text": "Menghapus output agar program cepat selesai", "label": "C"},
                    {"id": "d", "text": "Langsung menjalankan program tanpa testing", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Program yang baik dimulai dari memahami masalah, menyusun algoritma, menulis kode, lalu menguji hasilnya.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-008",
                "subtopic_id": "sub-001-2",
                "question_text": "Post test Modul 1: Apa output kode berikut?\n\nx = 4\ny = 2.5\nprint(x + y)",
                "options": [
                    {"id": "a", "text": "6", "label": "A"},
                    {"id": "b", "text": "6.5", "label": "B"},
                    {"id": "c", "text": "42.5", "label": "C"},
                    {"id": "d", "text": "Error", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Integer 4 dijumlahkan dengan float 2.5 menghasilkan float 6.5.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-009",
                "subtopic_id": "sub-001-3",
                "question_text": "Post test Modul 1: Berapakah hasil ekspresi berikut?\n\n(10 + 2) * 3 - 4",
                "options": [
                    {"id": "a", "text": "32", "label": "A"},
                    {"id": "b", "text": "18", "label": "B"},
                    {"id": "c", "text": "34", "label": "C"},
                    {"id": "d", "text": "20", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Kurung dikerjakan dulu: 10 + 2 = 12, lalu 12 * 3 = 36, kemudian 36 - 4 = 32.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-010",
                "subtopic_id": "sub-002-1",
                "question_text": "Post test Modul 2: Ekspresi logika mana yang bernilai True?",
                "options": [
                    {"id": "a", "text": "(3 > 5) or (2 == 4)", "label": "A"},
                    {"id": "b", "text": "(7 >= 7) and (5 != 3)", "label": "B"},
                    {"id": "c", "text": "not (10 > 1)", "label": "C"},
                    {"id": "d", "text": "(4 < 2) and True", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "7 >= 7 bernilai True dan 5 != 3 juga True, sehingga True and True menghasilkan True.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-011",
                "subtopic_id": "sub-002-2",
                "question_text": "Post test Modul 2: Apa output kode berikut?\n\numur = 17\nif umur >= 18:\n    print('dewasa')\nelse:\n    print('belum')",
                "options": [
                    {"id": "a", "text": "dewasa", "label": "A"},
                    {"id": "b", "text": "belum", "label": "B"},
                    {"id": "c", "text": "umur", "label": "C"},
                    {"id": "d", "text": "Tidak ada output", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Kondisi 17 >= 18 bernilai False, sehingga blok else dijalankan.",
                "difficulty": "mudah",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-012",
                "subtopic_id": "sub-002-4",
                "question_text": "Post test Modul 2: Nested if paling tepat digunakan ketika...",
                "options": [
                    {"id": "a", "text": "Satu kondisi perlu dicek setelah kondisi lain terpenuhi", "label": "A"},
                    {"id": "b", "text": "Program tidak punya kondisi sama sekali", "label": "B"},
                    {"id": "c", "text": "Semua variabel harus dihapus", "label": "C"},
                    {"id": "d", "text": "Loop harus berjalan tanpa batas", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Nested if cocok saat pengecekan kedua bergantung pada hasil pengecekan pertama.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-013",
                "subtopic_id": "sub-003-1",
                "question_text": "Post test Modul 3: Apa output kode berikut?\n\nfor i in range(1, 5):\n    print(i)",
                "options": [
                    {"id": "a", "text": "1 2 3 4", "label": "A"},
                    {"id": "b", "text": "1 2 3 4 5", "label": "B"},
                    {"id": "c", "text": "0 1 2 3 4", "label": "C"},
                    {"id": "d", "text": "5 saja", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "range(1, 5) menghasilkan angka 1 sampai 4, batas akhir 5 tidak ikut.",
                "difficulty": "mudah",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-014",
                "subtopic_id": "sub-003-2",
                "question_text": "Post test Modul 3: Pada while loop, apa yang harus diperhatikan agar tidak terjadi infinite loop?",
                "options": [
                    {"id": "a", "text": "Kondisi loop harus bisa berubah menjadi False", "label": "A"},
                    {"id": "b", "text": "Variabel tidak boleh digunakan", "label": "B"},
                    {"id": "c", "text": "print harus selalu dihapus", "label": "C"},
                    {"id": "d", "text": "Loop harus memakai string", "label": "D"}
                ],
                "correct_answer": "a",
                "explanation": "Agar while berhenti, kondisi loop perlu berubah menjadi False pada saat tertentu.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            },
            {
                "id": "q-post-015",
                "subtopic_id": "sub-003-4",
                "question_text": "Post test Modul 3: Nested loop paling cocok untuk memproses...",
                "options": [
                    {"id": "a", "text": "Data satu angka saja", "label": "A"},
                    {"id": "b", "text": "Data berbentuk baris dan kolom", "label": "B"},
                    {"id": "c", "text": "Password tanpa kondisi", "label": "C"},
                    {"id": "d", "text": "Komentar program", "label": "D"}
                ],
                "correct_answer": "b",
                "explanation": "Nested loop sering dipakai untuk data dua dimensi seperti tabel, matriks, atau pola.",
                "difficulty": "sedang",
                "assessment_type": "post_test"
            }
        ])

        question_rewrites = {
            "q-pre-001": {
                "question_text": "Pre test Modul 1: Sebelum menulis kode, hal pertama yang perlu dipahami adalah...",
                "options": [
                    {"id": "a", "text": "Warna tampilan editor kode", "label": "A"},
                    {"id": "b", "text": "Masalah yang ingin diselesaikan", "label": "B"},
                    {"id": "c", "text": "Jumlah file di laptop", "label": "C"},
                    {"id": "d", "text": "Nama aplikasi yang paling populer", "label": "D"},
                ],
                "correct_answer": "b",
                "explanation": "Program yang baik dimulai dari memahami masalah, baru menyusun langkah penyelesaiannya.",
                "difficulty": "mudah",
            },
            "q-pre-002": {
                "question_text": "Pre test Modul 1: Jika program perlu mengingat nama pengguna, konsep yang paling sesuai adalah...",
                "options": [
                    {"id": "a", "text": "Variabel", "label": "A"},
                    {"id": "b", "text": "Komentar", "label": "B"},
                    {"id": "c", "text": "Error", "label": "C"},
                    {"id": "d", "text": "Folder", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Variabel dipakai untuk menyimpan data agar dapat digunakan kembali oleh program.",
                "difficulty": "mudah",
            },
            "q-pre-007": {
                "question_text": "Pre test Modul 1: Ketika program menghitung total harga dari harga satuan dan jumlah barang, konsep yang dipakai adalah...",
                "options": [
                    {"id": "a", "text": "Operasi aritmatika", "label": "A"},
                    {"id": "b", "text": "Komentar program", "label": "B"},
                    {"id": "c", "text": "Penghapusan file", "label": "C"},
                    {"id": "d", "text": "Pengaturan tema", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Menghitung total harga membutuhkan operator aritmatika seperti perkalian dan penjumlahan.",
                "difficulty": "mudah",
            },
            "q-pre-008": {
                "question_text": "Pre test Modul 1: Jika program meminta pengguna memasukkan umur, fungsi Python yang paling sesuai adalah...",
                "options": [
                    {"id": "a", "text": "input()", "label": "A"},
                    {"id": "b", "text": "print()", "label": "B"},
                    {"id": "c", "text": "range()", "label": "C"},
                    {"id": "d", "text": "break", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "input() digunakan untuk menerima masukan dari pengguna saat program berjalan.",
                "difficulty": "mudah",
            },
            "q-pre-009": {
                "question_text": "Pre test Modul 1: Data dari input() di Python awalnya dibaca sebagai tipe...",
                "options": [
                    {"id": "a", "text": "str", "label": "A"},
                    {"id": "b", "text": "int", "label": "B"},
                    {"id": "c", "text": "float", "label": "C"},
                    {"id": "d", "text": "bool", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "input() selalu menghasilkan string, sehingga input angka perlu dikonversi sebelum dihitung.",
                "difficulty": "mudah",
            },
            "q-post-001": {
                "question_text": "Post test Modul 1: Program kasir menerima jumlah barang sebagai input teks. Agar jumlah barang bisa dikalikan dengan harga satuan, langkah yang benar adalah...",
                "options": [
                    {"id": "a", "text": "Mengubah input dengan int() lalu melakukan perkalian", "label": "A"},
                    {"id": "b", "text": "Langsung mengalikan string dengan harga", "label": "B"},
                    {"id": "c", "text": "Menghapus input sebelum dihitung", "label": "C"},
                    {"id": "d", "text": "Mengubah harga menjadi nama variabel", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Jumlah barang dari input() berbentuk string, sehingga perlu dikonversi ke integer sebelum dihitung.",
                "difficulty": "sedang",
            },
            "q-post-002": {
                "question_text": "Post test Modul 1: Seorang mahasiswa ingin membaca nilai ujian desimal seperti 82.5 lalu mengecek apakah nilainya lulus. Potongan kode yang paling tepat adalah...",
                "options": [
                    {"id": "a", "text": "nilai = float(input()); print(nilai >= 75)", "label": "A"},
                    {"id": "b", "text": "nilai = input(); print(nilai + 75)", "label": "B"},
                    {"id": "c", "text": "nilai = print(input()); nilai >= 75", "label": "C"},
                    {"id": "d", "text": "float = input(nilai); print(75)", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Nilai desimal perlu dibaca sebagai float, lalu dibandingkan dengan batas kelulusan.",
                "difficulty": "sedang",
            },
            "q-post-007": {
                "question_text": "Post test Modul 1: Dalam studi kasus menghitung luas persegi panjang, urutan kerja yang paling tepat adalah...",
                "options": [
                    {"id": "a", "text": "Cetak hasil, lalu minta panjang dan lebar", "label": "A"},
                    {"id": "b", "text": "Ambil panjang dan lebar, hitung luas, lalu tampilkan hasil", "label": "B"},
                    {"id": "c", "text": "Hapus nilai panjang sebelum dihitung", "label": "C"},
                    {"id": "d", "text": "Ubah semua angka menjadi komentar", "label": "D"},
                ],
                "correct_answer": "b",
                "explanation": "Program perlu menerima input, memproses rumus luas, lalu menampilkan output.",
                "difficulty": "sedang",
            },
            "q-post-008": {
                "question_text": "Post test Modul 1: Apa tipe data paling tepat untuk menyimpan status apakah mahasiswa sudah mengisi pre test?",
                "options": [
                    {"id": "a", "text": "str", "label": "A"},
                    {"id": "b", "text": "bool", "label": "B"},
                    {"id": "c", "text": "float", "label": "C"},
                    {"id": "d", "text": "list komentar", "label": "D"},
                ],
                "correct_answer": "b",
                "explanation": "Status selesai atau belum selesai paling tepat direpresentasikan dengan nilai boolean.",
                "difficulty": "sedang",
            },
            "q-post-009": {
                "question_text": "Post test Modul 1: Dalam kode total = (harga - diskon) * jumlah, bagian yang dihitung pertama adalah...",
                "options": [
                    {"id": "a", "text": "harga - diskon", "label": "A"},
                    {"id": "b", "text": "diskon * jumlah", "label": "B"},
                    {"id": "c", "text": "total * harga", "label": "C"},
                    {"id": "d", "text": "jumlah - total", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Bagian dalam tanda kurung diproses lebih dulu sebelum dikalikan dengan jumlah.",
                "difficulty": "sedang",
            },
            "q-pre-003": {
                "question_text": "Pre test Modul 2: Percabangan dibutuhkan ketika program harus...",
                "options": [
                    {"id": "a", "text": "Memilih jalur berdasarkan kondisi", "label": "A"},
                    {"id": "b", "text": "Mengulang kode tanpa berhenti", "label": "B"},
                    {"id": "c", "text": "Menyimpan semua data sebagai gambar", "label": "C"},
                    {"id": "d", "text": "Menghapus operator perbandingan", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Percabangan dipakai saat program perlu memilih aksi sesuai kondisi tertentu.",
                "difficulty": "mudah",
            },
            "q-post-003": {
                "question_text": "Post test Modul 2: Sistem beasiswa memberi status 'diterima' jika nilai >= 85 dan kehadiran >= 80. Ekspresi yang tepat adalah...",
                "options": [
                    {"id": "a", "text": "nilai >= 85 and kehadiran >= 80", "label": "A"},
                    {"id": "b", "text": "nilai >= 85 or kehadiran < 80", "label": "B"},
                    {"id": "c", "text": "nilai == kehadiran", "label": "C"},
                    {"id": "d", "text": "not nilai", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Kedua syarat harus terpenuhi, sehingga operator yang tepat adalah and.",
                "difficulty": "sedang",
            },
            "q-post-004": {
                "question_text": "Post test Modul 2: Pada fitur kalkulator, alasan utama mengecek pembagi sebelum operasi pembagian adalah...",
                "options": [
                    {"id": "a", "text": "Mencegah pembagian dengan nol", "label": "A"},
                    {"id": "b", "text": "Agar semua hasil menjadi nol", "label": "B"},
                    {"id": "c", "text": "Agar operator tambah tidak bisa dipakai", "label": "C"},
                    {"id": "d", "text": "Agar input selalu berupa teks", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Pembagian dengan nol tidak valid dan perlu ditangani dengan percabangan.",
                "difficulty": "sedang",
            },
            "q-pre-005": {
                "question_text": "Pre test Modul 3: Loop paling cocok dipakai ketika program perlu...",
                "options": [
                    {"id": "a", "text": "Melakukan proses yang sama berkali-kali", "label": "A"},
                    {"id": "b", "text": "Menghilangkan semua variabel", "label": "B"},
                    {"id": "c", "text": "Menjalankan percabangan hanya sekali", "label": "C"},
                    {"id": "d", "text": "Mengubah kode menjadi gambar", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Loop digunakan untuk menjalankan instruksi berulang sesuai jumlah atau kondisi tertentu.",
                "difficulty": "mudah",
            },
            "q-post-005": {
                "question_text": "Post test Modul 3: Pada proses mencari angka pertama yang habis dibagi 7, kontrol loop yang paling tepat dipakai setelah angka ditemukan adalah...",
                "options": [
                    {"id": "a", "text": "break", "label": "A"},
                    {"id": "b", "text": "continue", "label": "B"},
                    {"id": "c", "text": "input", "label": "C"},
                    {"id": "d", "text": "float", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "break menghentikan loop setelah target ditemukan sehingga pencarian tidak perlu lanjut.",
                "difficulty": "sedang",
            },
            "q-post-006": {
                "question_text": "Post test Modul 3: Dalam program faktorial, nilai hasil sementara biasanya diperbarui dengan cara...",
                "options": [
                    {"id": "a", "text": "Dikalikan dengan angka iterasi saat ini", "label": "A"},
                    {"id": "b", "text": "Selalu diubah menjadi string kosong", "label": "B"},
                    {"id": "c", "text": "Dibandingkan dengan operator or", "label": "C"},
                    {"id": "d", "text": "Dihapus setiap loop berjalan", "label": "D"},
                ],
                "correct_answer": "a",
                "explanation": "Faktorial menghitung perkalian berurutan, sehingga hasil sementara dikalikan pada tiap iterasi.",
                "difficulty": "sedang",
            },
        }

        for q_data in questions_data:
            rewrite = question_rewrites.get(q_data["id"])
            if rewrite:
                q_data.update(rewrite)

        seen_assessment_questions = {}
        for q_data in questions_data:
            assessment_type = q_data.get("assessment_type", "quiz")
            if assessment_type not in {"pre_test", "quiz", "post_test"}:
                continue
            normalized_text = " ".join(q_data["question_text"].lower().split())
            duplicate_id = seen_assessment_questions.get(normalized_text)
            if duplicate_id:
                raise ValueError(
                    f"Duplicate assessment question text between {duplicate_id} and {q_data['id']}"
                )
            seen_assessment_questions[normalized_text] = q_data["id"]

        for q_data in questions_data:
            q_data.setdefault("assessment_type", "quiz")

        drill_questions = []
        for q_data in list(questions_data):
            if q_data["assessment_type"] != "quiz":
                continue

            drill_question = {
                **q_data,
                "id": q_data["id"].replace("q-", "q-drill-", 1),
                "question_text": f"Latihan drill: {q_data['question_text']}",
                "assessment_type": "drill",
            }
            drill_questions.append(drill_question)

        questions_data.extend(drill_questions)

        canonical_question_ids = {q_data["id"] for q_data in questions_data}
        canonical_posttest_keys = {
            (q_data["subtopic_id"], q_data["question_text"])
            for q_data in questions_data
            if q_data["assessment_type"] == "post_test"
        }
        duplicate_posttests = db.query(Question).filter(
            Question.assessment_type == "post_test",
            Question.id.notin_(canonical_question_ids),
        ).all()

        for duplicate in duplicate_posttests:
            duplicate_key = (duplicate.subtopic_id, duplicate.question_text)
            if duplicate_key not in canonical_posttest_keys:
                continue

            db.query(AssessmentAnswer).filter(
                AssessmentAnswer.question_id == duplicate.id
            ).delete(synchronize_session=False)
            db.delete(duplicate)
            print(f"[-] Duplicate post test question '{duplicate.id}' removed")

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
                    difficulty=q_data["difficulty"],
                    assessment_type=q_data["assessment_type"]
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
                existing_q.assessment_type = q_data["assessment_type"]
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

            existing_edge = db.query(KnowledgeEdge).filter(
                KnowledgeEdge.source_node_id == relation["prerequisite_id"],
                KnowledgeEdge.source_node_type == "module",
                KnowledgeEdge.target_node_id == relation["topic_id"],
                KnowledgeEdge.target_node_type == "module",
                KnowledgeEdge.relation_type == "prerequisite",
            ).first()
            if not existing_edge:
                db.add(KnowledgeEdge(
                    source_node_id=relation["prerequisite_id"],
                    source_node_type="module",
                    target_node_id=relation["topic_id"],
                    target_node_type="module",
                    relation_type="prerequisite",
                    weight=relation["mastery_threshold"] / 100.0,
                ))
                print(f"[+] Knowledge edge {relation['prerequisite_id']} -> {relation['topic_id']} created")
            else:
                existing_edge.weight = relation["mastery_threshold"] / 100.0

        # ==============================
        # 6. Seed Cognitive Instrument Items (Perry Scheme)
        # ==============================
        cognitive_items = [
            {"code": "D1", "stage": "dualism", "statement": "Dalam pengetahuan, dasarnya adalah fakta. Tugas mahasiswa adalah menguasai fakta sesuai yang disampaikan dosen."},
            {"code": "D2", "stage": "dualism", "statement": "Pengetahuan adalah kemampuan untuk menemukan jawaban yang benar."},
            {"code": "M3", "stage": "multiplicity", "statement": "Dosen sengaja menyajikan sudut pandang berbeda-beda karena ingin mahasiswanya berpikir dan menemukan jawaban mandiri."},
            {"code": "C4", "stage": "commitment", "statement": "Dosen bukanlah satu-satunya pemberi pengetahuan. Dosen adalah pemandu dan fasilitator. Tanggung jawab untuk belajar ada pada diri mahasiswa sendiri."},
            {"code": "R5", "stage": "relativism", "statement": "Saya tidak bisa menganalisis dan menimbang terlalu lama; cepat atau lambat saya harus memutuskan dan bertindak."},
            {"code": "C6", "stage": "commitment", "statement": "Pengetahuan adalah kemampuan untuk mempertahankan pendapat dengan alasan kuat, meskipun orang lain tidak setuju."},
            {"code": "C7", "stage": "commitment", "statement": "Belajar menjadi matang saat harus mempertimbangkan semua pendapat sebelum menentukan tindakan."},
            {"code": "D8", "stage": "dualism", "statement": "Pengetahuan adalah kemampuan untuk meningkatkan fakta dan data."},
            {"code": "R9", "stage": "relativism", "statement": "Kualitas suatu pendapat bergantung pada fakta yang mendukungnya."},
            {"code": "R10", "stage": "relativism", "statement": "Selama mahasiswa mengembangkan pendapat mereka, mahasiswa tidak boleh dinilai salah hanya karena berbeda pandangan dengan dosen."},
            {"code": "M12", "stage": "multiplicity", "statement": "Jika para ahli tidak sependapat dalam suatu topik, maka setiap orang berhak mempunyai pendapatnya sendiri."},
            {"code": "R14", "stage": "relativism", "statement": "Orang yang berpengetahuan menggunakan apa yang mereka ketahui untuk menilai ide, data, dan nilai tertentu."},
            {"code": "C16", "stage": "commitment", "statement": "Orang yang berpengetahuan sudah menemukan sudut pandang sendiri dan bertindak sesuai itu."},
            {"code": "C17", "stage": "commitment", "statement": "Mahasiswa akan lebih mudah mengerti jika dosen fokus menjelaskan fakta, bukan banyak berteori."},
            {"code": "M19", "stage": "multiplicity", "statement": "Mahasiswa yang sukses adalah yang paling mampu memahami ekspektasi dosen."},
            {"code": "M20", "stage": "multiplicity", "statement": "Setiap orang berhak atas pendapatnya sendiri. Tidak ada yang benar atau yang salah."},
        ]

        for item_data in cognitive_items:
            item = db.query(CognitiveItem).filter(CognitiveItem.code == item_data["code"]).first()
            if not item:
                db.add(CognitiveItem(**item_data))
                print(f"[+] Cognitive item {item_data['code']} created")
            else:
                item.stage = item_data["stage"]
                item.statement = item_data["statement"]
                print(f"[~] Cognitive item {item_data['code']} updated")

        db.commit()
        print("\n[OK] Database seeding complete!")
        print(f"   Modules: {db.query(Module).count()}")
        print(f"   Subtopics: {db.query(Subtopic).count()}")
        print(f"   Questions: {db.query(Question).count()}")
        print(f"   User Progress: {db.query(UserProgress).count()}")
        print(f"   Topic Prerequisites: {db.query(TopicPrerequisite).count()}")
        print(f"   Knowledge Edges: {db.query(KnowledgeEdge).count()}")
        print(f"   Cognitive Items: {db.query(CognitiveItem).count()}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] {str(e).encode('ascii', 'replace').decode()}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
