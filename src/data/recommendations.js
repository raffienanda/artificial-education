/**
 * AI Recommendations — Dummy Data (Indonesian)
 * Rekomendasi berdasarkan analisis BKT
 */
export const recommendations = {
  weakTopics: [
    {
      id: 'rec-01',
      subtopic: 'Perkalian',
      mastery: 40,
      reason: 'Di bawah batas penguasaan 80%',
      estimatedTime: '10 menit',
      priority: 'high',
    },
    {
      id: 'rec-02',
      subtopic: 'Soal Cerita',
      mastery: 50,
      reason: 'Di bawah batas penguasaan 80%',
      estimatedTime: '8 menit',
      priority: 'high',
    },
    {
      id: 'rec-03',
      subtopic: 'Pengurangan',
      mastery: 60,
      reason: 'Perlu latihan lebih lanjut',
      estimatedTime: '5 menit',
      priority: 'medium',
    },
  ],
  totalEstimatedTime: '15 menit',
  message: 'Kamu perlu fokus pada 2 sub-materi yang belum dikuasai.',
  statusMessage: 'Kamu perlu fokus pada 2 sub-materi yang belum dikuasai.',
  nextMilestone: {
    title: 'Buka Modul Pecahan',
    requirement: 'Selesaikan Bilangan Bulat dengan penguasaan 80%',
    progress: 60,
  },
}
