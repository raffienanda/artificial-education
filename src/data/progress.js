/**
 * Progress & Mastery — Dummy Data (Indonesian)
 * Data penguasaan per sub-materi, radar chart, dan riwayat belajar
 */
export const overallMastery = 60

export const subtopicMastery = [
  { id: 'sub-m-01', name: 'Penjumlahan', mastery: 80, status: 'proficient', bkt: { pKnown: 0.80, pLearn: 0.15, pGuess: 0.25, pSlip: 0.10 } },
  { id: 'sub-m-02', name: 'Pengurangan', mastery: 60, status: 'learning', bkt: { pKnown: 0.60, pLearn: 0.20, pGuess: 0.25, pSlip: 0.12 } },
  { id: 'sub-m-03', name: 'Perkalian', mastery: 40, status: 'weak', bkt: { pKnown: 0.40, pLearn: 0.18, pGuess: 0.25, pSlip: 0.15 } },
  { id: 'sub-m-04', name: 'Pembagian', mastery: 70, status: 'learning', bkt: { pKnown: 0.70, pLearn: 0.12, pGuess: 0.25, pSlip: 0.08 } },
  { id: 'sub-m-05', name: 'Soal Cerita', mastery: 50, status: 'weak', bkt: { pKnown: 0.50, pLearn: 0.22, pGuess: 0.25, pSlip: 0.10 } },
]

export const radarChartData = {
  labels: ['Penjumlahan', 'Pengurangan', 'Perkalian', 'Pembagian', 'Soal Cerita'],
  datasets: [
    {
      label: 'Penguasaan',
      data: [80, 60, 40, 70, 50],
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
  { id: 'act-01', title: 'Penjumlahan & Pengurangan', time: 'Hari ini, 10:15', mastery: 80, icon: '📘', color: 'primary' },
  { id: 'act-02', title: 'Perkalian Bilangan Bulat', time: 'Kemarin, 14:20', mastery: 40, icon: '📕', color: 'danger' },
  { id: 'act-03', title: 'Pembagian Bilangan Bulat', time: '2 hari lalu, 09:30', mastery: 70, icon: '📗', color: 'success' },
  { id: 'act-04', title: 'Soal Cerita Bil. Bulat', time: '3 hari lalu, 16:45', mastery: 50, icon: '📙', color: 'warning' },
]

export const weeklyProgress = [
  { day: 'Sen', minutes: 35 },
  { day: 'Sel', minutes: 22 },
  { day: 'Rab', minutes: 45 },
  { day: 'Kam', minutes: 0 },
  { day: 'Jum', minutes: 30 },
  { day: 'Sab', minutes: 50 },
  { day: 'Min', minutes: 22 },
]
