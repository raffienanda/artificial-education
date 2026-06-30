/**
 * Quiz Questions — Dummy Data (Indonesian)
 * Soal latihan drill dalam Bahasa Indonesia
 */
export const questions = [
  {
    id: 'q-001',
    moduleId: 'mod-001',
    subtopic: 'Penjumlahan dan Pengurangan',
    question: 'Berapa hasil dari −5 + 8 = … ?',
    options: [
      { id: 'a', text: '3', label: 'A' },
      { id: 'b', text: '−3', label: 'B' },
      { id: 'c', text: '13', label: 'C' },
      { id: 'd', text: '−13', label: 'D' },
    ],
    correctAnswer: 'a',
    explanation: 'Karena tanda berbeda, kurangi angka yang lebih kecil dari yang lebih besar: 8 − 5 = 3. Karena 8 lebih besar dan bertanda positif, hasilnya +3.',
    difficulty: 'mudah',
  },
  {
    id: 'q-002',
    moduleId: 'mod-001',
    subtopic: 'Penjumlahan dan Pengurangan',
    question: 'Berapa hasil dari (−12) + (−7) = … ?',
    options: [
      { id: 'a', text: '−19', label: 'A' },
      { id: 'b', text: '19', label: 'B' },
      { id: 'c', text: '−5', label: 'C' },
      { id: 'd', text: '5', label: 'D' },
    ],
    correctAnswer: 'a',
    explanation: 'Karena kedua bilangan bertanda negatif, jumlahkan nilainya dan hasilnya tetap negatif: (−12) + (−7) = −(12 + 7) = −19.',
    difficulty: 'mudah',
  },
  {
    id: 'q-003',
    moduleId: 'mod-001',
    subtopic: 'Perkalian Bilangan Bulat',
    question: 'Berapa hasil dari (−4) × (−6) = … ?',
    options: [
      { id: 'a', text: '24', label: 'A' },
      { id: 'b', text: '−24', label: 'B' },
      { id: 'c', text: '10', label: 'C' },
      { id: 'd', text: '−10', label: 'D' },
    ],
    correctAnswer: 'a',
    explanation: 'Perkalian dua bilangan negatif menghasilkan bilangan positif. (−4) × (−6) = +24. Ingat: negatif × negatif = positif.',
    difficulty: 'mudah',
  },
  {
    id: 'q-004',
    moduleId: 'mod-001',
    subtopic: 'Pembagian Bilangan Bulat',
    question: 'Berapa hasil dari (−36) ÷ 9 = … ?',
    options: [
      { id: 'a', text: '−4', label: 'A' },
      { id: 'b', text: '4', label: 'B' },
      { id: 'c', text: '−27', label: 'C' },
      { id: 'd', text: '27', label: 'D' },
    ],
    correctAnswer: 'a',
    explanation: 'Pembagian bilangan negatif dengan positif menghasilkan negatif. 36 ÷ 9 = 4, jadi (−36) ÷ 9 = −4.',
    difficulty: 'mudah',
  },
  {
    id: 'q-005',
    moduleId: 'mod-001',
    subtopic: 'Penjumlahan dan Pengurangan',
    question: 'Suhu di puncak gunung −3°C. Setelah matahari terbit, suhu naik 7°C. Berapa suhu sekarang?',
    options: [
      { id: 'a', text: '4°C', label: 'A' },
      { id: 'b', text: '−4°C', label: 'B' },
      { id: 'c', text: '10°C', label: 'C' },
      { id: 'd', text: '−10°C', label: 'D' },
    ],
    correctAnswer: 'a',
    explanation: 'Suhu awal −3°C naik 7°C berarti: −3 + 7 = 4°C. Tanda berbeda, kurangi: 7 − 3 = 4, ambil tanda positif karena 7 > 3.',
    difficulty: 'sedang',
  },
]
