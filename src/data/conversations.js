/**
 * Chatbot Conversations — Dummy Data (Indonesian)
 * Percakapan contoh dan template respon AI dalam Bahasa Indonesia
 */
export const conversationHistory = [
  {
    id: 'msg-001',
    role: 'ai',
    content: 'Hai! Aku Asisten AI-mu 😊\nAda yang ingin kamu tanyakan tentang materi ini?',
    timestamp: '2026-06-29T10:22:00',
  },
]

export const quickReplies = [
  { id: 'qr-01', text: 'Apa aturan tanda pada penjumlahan?', icon: '' },
  { id: 'qr-02', text: 'Bisa beri contoh soal?', icon: '' },
  { id: 'qr-03', text: 'Kenapa −5 + 3 = −2?', icon: '' },
  { id: 'qr-04', text: 'Tips cepat mengerjakan soal?', icon: '' },
]

/**
 * Template respon AI untuk berbagai pertanyaan.
 * Di produksi, respons ini akan dihasilkan oleh backend AI.
 */
export const aiResponses = {
  'Apa aturan tanda pada penjumlahan?': 'Berikut aturan tanda pada penjumlahan bilangan bulat:\n\n1. **(+) + (+) = (+)** → Positif + Positif = Positif\n   Contoh: 3 + 5 = 8\n\n2. **(−) + (−) = (−)** → Negatif + Negatif = Negatif\n   Contoh: (−3) + (−5) = −8\n\n3. **(+) + (−)** → Kurangi, ambil tanda yang lebih besar\n   Contoh: 7 + (−3) = 4\n\n4. **(−) + (+)** → Kurangi, ambil tanda yang lebih besar\n   Contoh: (−7) + 3 = −4\n\nMau coba latihan soal? 💪',
  'Bisa beri contoh soal?': 'Tentu! Coba kerjakan soal berikut ya 📝\n\n**Soal 1 (Mudah):** (−3) + 5 = ?\n\n**Soal 2 (Sedang):** (−8) + (−4) + 6 = ?\n\n**Soal 3 (Tantangan):** 12 + (−7) − (−3) = ?\n\nCoba jawab satu per satu, nanti aku periksa! ✨',
  'Kenapa −5 + 3 = −2?': 'Pertanyaan bagus! Mari kita bahas step by step 🔍\n\n**−5 + 3 = −2** karena:\n\n1. Tanda kedua bilangan **berbeda** (negatif dan positif)\n2. Kurangi yang kecil dari yang besar: **5 − 3 = 2**\n3. Ambil tanda dari bilangan yang **lebih besar nilainya**: |−5| = 5 > |3| = 3\n4. Karena 5 bertanda negatif, hasilnya **−2** ✅\n\nBayangkan di garis bilangan: mulai dari 0, mundur 5 langkah ke −5, lalu maju 3 langkah. Kamu akan berhenti di **−2**! 📏',
  'Tips cepat mengerjakan soal?': 'Ini tips cepat mengerjakan soal bilangan bulat! ⚡\n\n**1. Hafal aturan tanda:**\n   - Sama = Positif (+×+ = +, −×− = +)\n   - Beda = Negatif (+×− = −)\n\n**2. Gunakan garis bilangan:**\n   - Positif → maju ke kanan\n   - Negatif → mundur ke kiri\n\n**3. Trik cepat penjumlahan:**\n   - Tanda sama → jumlahkan, pakai tanda itu\n   - Tanda beda → kurangi, pakai tanda yang besar\n\n**4. Cek ulang dengan estimasi:**\n   - Bilangan negatif + positif kecil = masih negatif\n   - Bilangan negatif + positif besar = jadi positif\n\nSemangat belajar! 🚀',
}
