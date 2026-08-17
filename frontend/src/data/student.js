/**
 * Student Profile — Dummy Data (Indonesian)
 * Data profil siswa, pencapaian, streak, dan target harian
 */
export const studentProfile = {
  id: 'student-001',
  name: 'Nanda Prasetyo',
  email: 'nanda@student.edu',
  avatar: null,
  initials: 'NP',
  grade: 'Kelas 7 SMP',
  school: 'SMP Negeri 1 Jakarta',
  joinDate: '2026-01-15',
  totalStudyHours: 127,
  currentStreak: 12,
  longestStreak: 24,
  dailyGoal: 30, // menit
  todayStudyTime: 22, // menit
  level: 14,
  xp: 2840,
  xpToNextLevel: 3500,
}

export const achievements = [
  {
    id: 'ach-001',
    title: 'Langkah Pertama',
    description: 'Selesaikan pelajaran pertamamu',
    icon: '🎯',
    earned: true,
    earnedDate: '2026-01-15',
  },
  {
    id: 'ach-002',
    title: 'Skor Sempurna',
    description: 'Dapatkan 100% di kuis',
    icon: '⭐',
    earned: true,
    earnedDate: '2026-02-03',
  },
  {
    id: 'ach-003',
    title: 'Pejuang Mingguan',
    description: 'Belajar 7 hari berturut-turut',
    icon: '🔥',
    earned: true,
    earnedDate: '2026-02-10',
  },
  {
    id: 'ach-004',
    title: 'Penjelajah Matematika',
    description: 'Selesaikan 3 modul matematika',
    icon: '🧮',
    earned: true,
    earnedDate: '2026-03-20',
  },
  {
    id: 'ach-005',
    title: 'Master Ilmu',
    description: 'Capai penguasaan 90% pada topik apapun',
    icon: '🏆',
    earned: false,
    earnedDate: null,
  },
  {
    id: 'ach-006',
    title: 'Pelajar Cepat',
    description: 'Selesaikan modul dalam waktu kurang dari 20 menit',
    icon: '⚡',
    earned: false,
    earnedDate: null,
  },
]

export const notifications = [
  {
    id: 'notif-001',
    type: 'reminder',
    title: 'Pengingat Target Harian',
    message: 'Kamu tinggal 8 menit lagi untuk mencapai target harian!',
    time: '5 menit lalu',
    read: false,
  },
  {
    id: 'notif-002',
    type: 'achievement',
    title: 'Pencapaian Terbuka!',
    message: 'Kamu mendapatkan badge "Penjelajah Matematika" 🧮',
    time: '2 jam lalu',
    read: false,
  },
  {
    id: 'notif-003',
    type: 'recommendation',
    title: 'Rekomendasi AI',
    message: 'Review materi Perkalian untuk meningkatkan penguasaan',
    time: '1 hari lalu',
    read: true,
  },
  {
    id: 'notif-004',
    type: 'streak',
    title: 'Peringatan Streak 🔥',
    message: 'Kamu sudah streak 12 hari! Terus semangat!',
    time: '1 hari lalu',
    read: true,
  },
]

export const learningHistory = [
  { date: '2026-06-29', topic: 'Bilangan Bulat', subtopic: 'Penjumlahan', duration: 22, score: 85 },
  { date: '2026-06-28', topic: 'Bilangan Bulat', subtopic: 'Pengurangan', duration: 30, score: 92 },
  { date: '2026-06-27', topic: 'Bilangan Bulat', subtopic: 'Pembagian', duration: 25, score: 78 },
  { date: '2026-06-26', topic: 'Bilangan Bulat', subtopic: 'Perkalian', duration: 35, score: 88 },
  { date: '2026-06-25', topic: 'Bilangan Bulat', subtopic: 'Soal Cerita', duration: 20, score: 95 },
]
