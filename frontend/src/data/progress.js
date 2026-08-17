/**
 * Progress & Mastery — Dummy Data (Indonesian)
 * Data penguasaan per sub-materi, radar chart, dan riwayat belajar
 * Konteks: Mahasiswa Ilmu Komputer — Algoritma dan Pemrograman
 */
export const overallMastery = 48

export const subtopicMastery = [
  { id: 'sub-m-01', name: 'Sintaks Dasar', mastery: 75, status: 'proficient', bkt: { pKnown: 0.75, pLearn: 0.18, pGuess: 0.20, pSlip: 0.10 } },
  { id: 'sub-m-02', name: 'Logika & Kondisi', mastery: 55, status: 'learning', bkt: { pKnown: 0.55, pLearn: 0.22, pGuess: 0.25, pSlip: 0.12 } },
  { id: 'sub-m-03', name: 'Perulangan', mastery: 25, status: 'weak', bkt: { pKnown: 0.25, pLearn: 0.15, pGuess: 0.30, pSlip: 0.18 } },
  { id: 'sub-m-04', name: 'Debugging', mastery: 40, status: 'weak', bkt: { pKnown: 0.40, pLearn: 0.20, pGuess: 0.25, pSlip: 0.15 } },
  { id: 'sub-m-05', name: 'Pemecahan Masalah', mastery: 45, status: 'learning', bkt: { pKnown: 0.45, pLearn: 0.25, pGuess: 0.20, pSlip: 0.10 } },
]

export const radarChartData = {
  labels: ['Sintaks Dasar', 'Logika & Kondisi', 'Perulangan', 'Debugging', 'Pemecahan Masalah'],
  datasets: [
    {
      label: 'Penguasaan',
      data: [75, 55, 25, 40, 45],
      backgroundColor: 'rgba(37, 99, 235, 0.15)',
      borderColor: 'rgba(37, 99, 235, 0.8)',
      borderWidth: 2,
      pointBackgroundColor: '#2563EB',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
    },
  ],
}

export const recentActivities = [
  { id: 'act-01', title: 'Operator Perbandingan & Logika', time: 'Hari ini, 09:30', mastery: 55, icon: '📘', color: 'primary' },
  { id: 'act-02', title: 'Percabangan if-else', time: 'Hari ini, 10:15', mastery: 60, icon: '📗', color: 'success' },
  { id: 'act-03', title: 'Variabel dan Tipe Data', time: 'Kemarin, 14:20', mastery: 75, icon: '📗', color: 'success' },
  { id: 'act-04', title: 'Operasi Aritmatika', time: '2 hari lalu, 11:00', mastery: 70, icon: '📘', color: 'primary' },
  { id: 'act-05', title: 'Input dan Output', time: '3 hari lalu, 16:45', mastery: 40, icon: '📙', color: 'warning' },
]

export const weeklyProgress = [
  { day: 'Sen', minutes: 45 },
  { day: 'Sel', minutes: 30 },
  { day: 'Rab', minutes: 60 },
  { day: 'Kam', minutes: 15 },
  { day: 'Jum', minutes: 50 },
  { day: 'Sab', minutes: 25 },
  { day: 'Min', minutes: 10 },
]
