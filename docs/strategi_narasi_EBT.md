# 📑 Strategi Narasi & Arah Analisis Data EBT
### CELIOS — Riset Energi Terbarukan berbasis PODES 2024 vs 2021

## Overview

| Parameter | Keputusan |
|---|---|
| **Sumber Data** | File Excel: `Energi Terbarukan(AutoRecovered).xlsx` + 13 sheet PDF |
| **Narasi** | Ketiga narasi diangkat (lihat di bawah) |
| **Crosstab** | Tidak hanya tabulasi sederhana — akan diperkaya scoring/indeks & visualisasi |
| **Target Audiens** | Publik (media/jurnalis) & Pemerintah (policymaker) |
| **Level Analisis** | Sesuai data yang tersedia (provinsi dari PODES) |
| **Tone** | Data-driven — angka yang berbicara, bukan opini |
| **Output** | Streamlit app: dashboard + laporan visualisasi + tool analisis |

---

## 3 Narasi Besar

### Narasi 1: Desa Tambang vs Transisi Energi

> **Judul kerja:** *"Ekstraksi Tanpa Kompensasi: Potret Akses Energi Bersih di Desa Tambang Indonesia"*

**Inti:** Desa yang sumber daya alamnya sudah dieksploitasi industri tambang justru **tidak mendapat manfaat** dari transisi energi bersih.

**Data pendukung:**
- Desa tambang naik **56,4%** (599 → 937 desa) — ekspansi industri ekstraktif terus berjalan
- Kalimantan Tengah: **31,16%** desa-nya bergantung pada tambang
- Perlu dibuktikan lewat crosstab: apakah desa tambang memiliki akses EBT lebih rendah?

**Metode analisis:**
- Crosstab desa tambang × 10 dimensi EBT (sesuai brief Aulia)
- Selain tabulasi, tambahkan **scoring/indeks komposit** dari 10 dimensi
- Visualisasi perbandingan desa tambang vs non-tambang per indikator
- Uji korelasi: aktivitas tambang → pencemaran → akses energi

**Pertanyaan riset:**
1. Apakah desa tambang memiliki akses EBT (surya, air, biogas) lebih rendah dari desa non-tambang?
2. Apakah desa tambang mengalami pencemaran lebih tinggi?
3. Apakah desa tambang mendapat program pengembangan EBT lebih sedikit?
4. Bagaimana profil infrastruktur energi desa tambang?

---

### Narasi 2: Potensi Besar, Realisasi Nyaris Nol

> **Judul kerja:** *"120.000 Desa Punya Air, Hanya 1.039 yang Menyalakannya: Gap Potensi vs Realisasi EBT Indonesia"*

**Inti:** Indonesia memiliki potensi sumber daya EBT yang melimpah di tingkat desa, tapi realisasi pemanfaatannya **sangat kecil** — dan beberapa bahkan **menurun**.

**Data pendukung (angka yang berbicara):**

| Indikator | Potensi/Target | Realisasi | Rasio |
|---|---|---|---|
| Desa dengan sumber air → PLTA | 120.546 desa | 1.039 desa | **0,86%** |
| Desa punya mata air → energi | 23.076 desa | ? (perlu crosstab) | ? |
| Desa dengan program EBT | 84.276 desa (semua) | 4.525 desa | **5,37%** |
| Desa dengan infrastruktur energi | 84.276 desa (semua) | 7.346 desa | **8,72%** |
| Desa pakai biogas | 84.276 desa | 601 desa | **0,71%** |

**Tren yang mengkhawatirkan (2021 → 2024):**

| Indikator | 2021 | 2024 | Perubahan |
|---|---|---|---|
| PLTA realisasi | 1.272 | 1.039 | **↓ 18,3%** |
| Biogas | 749 | 601 | **↓ 19,8%** |
| Surya RT "sebagian besar" | 4.176 | 3.076 | **↓ 26,3%** |

**Metode analisis:**
- Gap analysis potensi vs realisasi per provinsi
- Tren naik/turun per provinsi (2021 → 2024)
- Ranking provinsi berdasarkan "efisiensi pemanfaatan potensi"
- Identifikasi provinsi dengan gap terbesar (potensi tinggi, realisasi nol)

**Pertanyaan riset:**
1. Mengapa realisasi PLTA, biogas, dan surya RT justru turun?
2. Provinsi mana yang paling "menyia-nyiakan" potensi EBT-nya?
3. Apakah ada korelasi antara keberadaan program EBT dan realisasi pemanfaatan?

---

### Narasi 3: Ketimpangan Energi = Ketimpangan Keadilan

> **Judul kerja:** *"658.782 Keluarga Tanpa Listrik: Peta Ketidakadilan Energi di Indonesia"*

**Inti:** Akses energi di Indonesia sangat timpang — beban ketiadaan listrik dipikul wilayah timur Indonesia, sementara program & infrastruktur EBT terkonsentrasi di Jawa.

**Data pendukung:**

**Siapa yang paling gelap?**

| Provinsi | Keluarga tanpa listrik (2024) | % nasional |
|---|---|---|
| Papua Pegunungan | 157.563 | 23,92% |
| Papua Tengah | 129.220 | 19,61% |
| NTT | 86.822 | 13,18% |
| Sumatera Utara | 44.308 | 6,73% |
| Papua Selatan | 40.298 | 6,12% |

**Siapa yang paling dapat program EBT?**

| Provinsi | Desa dengan program EBT | % dari total desa berprogram |
|---|---|---|
| Jawa Timur | 679 | 15,01% |
| Jawa Tengah | 516 | 11,40% |
| Jawa Barat | 476 | 10,52% |

**Kontras kritis:** Papua Pegunungan punya 157.563 keluarga tanpa listrik tapi hanya **5 desa** (0,11%) yang punya program EBT.

**Metode analisis:**
- Indeks ketimpangan energi per provinsi
- Scatter plot: kebutuhan energi (tanpa listrik) vs ketersediaan program EBT
- Heatmap regional: Indonesia Timur vs Barat
- Analisis apakah EBT surya di Papua = inovasi atau kemiskinan energi?

**Pertanyaan riset:**
1. Apakah distribusi program EBT proporsional dengan kebutuhan?
2. Wilayah mana yang paling "ditinggalkan" dalam transisi energi?
3. Apakah penggunaan surya di Papua/NTT = keberhasilan EBT atau kegagalan PLN?

---

## Struktur Output Streamlit

Berdasarkan 3 narasi + audiens publik & pemerintah:

### Halaman 1: Overview Nasional
- Ringkasan angka kunci (KPI cards)
- Tren 2021 → 2024 (naik/turun per dimensi)
- Peta Indonesia dengan heat overlay

### Halaman 2: Narasi 1 — Desa Tambang × EBT
- Crosstab interaktif desa tambang vs non-tambang
- Perbandingan visual 10 dimensi
- Indeks komposit desa tambang

### Halaman 3: Narasi 2 — Gap Potensi vs Realisasi
- Bar chart gap per provinsi
- Tren menurun (PLTA, biogas, surya)
- Ranking provinsi "potensi terbuang"

### Halaman 4: Narasi 3 — Ketimpangan Energi
- Peta ketimpangan (tanpa listrik vs program EBT)
- Scatter plot kebutuhan vs intervensi
- Top/bottom provinsi

### Halaman 5: Eksplorasi Data
- Filter interaktif per provinsi, tahun, dimensi
- Tabel data mentah yang bisa didownload
- Custom crosstab

---

## Status & Next Steps

- [ ] Baca dan pahami struktur file Excel mentah
- [ ] Diskusi final narasi & validasi dengan user
- [ ] Mulai coding Streamlit setelah diskusi selesai
