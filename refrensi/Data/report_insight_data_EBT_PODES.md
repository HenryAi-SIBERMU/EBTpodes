# 📊 Laporan Insight Data: Energi Terbarukan di Indonesia
### Sumber: PODES (Potensi Desa) 2024 vs 2021
### Disusun untuk: CELIOS — Center of Economic and Law Studies
### Tanggal: 10 Februari 2026

---

## 1. Gambaran Umum Data

| Parameter | Keterangan |
|---|---|
| **Sumber Data** | PODES (Potensi Desa) — BPS |
| **Periode Perbandingan** | 2024 vs 2021 |
| **Cakupan** | Seluruh Indonesia, 38 Provinsi |
| **Unit Analisis** | Desa/Kelurahan |
| **Total Desa 2024** | 84.276 desa |
| **Total Desa 2021** | 84.096 desa |
| **Jumlah Dimensi** | 10 dimensi energi terbarukan + 1 variabel Desa Tambang |

---

## 2. Kerangka Riset (Brief dari Aulia Lianasari)

Data diolah berdasarkan **10 dimensi** yang bersumber dari variabel PODES:

| No | Dimensi | Variabel PODES | Kode |
|---|---|---|---|
| 1 | Energi Surya — PJU | Penerangan jalan desa menggunakan lampu tenaga surya | R502a |
| 2 | Energi Surya — RT | Keluarga yang menggunakan lampu tenaga surya | R501c |
| 3 | Bioenergi | Penggunaan biogas sebagai bahan bakar memasak | R503a.6 |
| 4 | Energi Air (Hidro/Mikrohidro) | Pemanfaatan sungai/danau/waduk/embung untuk listrik | R510-R512 |
| 5 | Kebijakan & Program | Keberadaan program pengembangan energi terbarukan | R1504 |
| 6 | Infrastruktur Energi | Keberadaan sarana prasarana energi | R1503 |
| 7 | Aset Energi Alam | Keberadaan mata air milik desa | R1403 |
| 8 | Akses Energi (Non-PLN) | Keluarga pengguna listrik Non-PLN | R501a.2 |
| 9 | Akses Energi (Tanpa Listrik) | Keluarga bukan pengguna listrik | R501b |
| 10 | Kerusakan Lingkungan | Pencemaran air, tanah, udara | R514 |

**Variabel Crosstab:**
- **Indeks Desa Tambang** (binary: 1 = desa tambang, 0 = non-tambang)
- Definisi: Desa yang penghasilan utama penduduknya dari pertambangan (R403a) **ATAU** memiliki lokasi penggalian C (R518)

---

## 3. Ringkasan Data Per Dimensi

### 3.1 Energi Surya — Penerangan Jalan Umum (PJU)

| Kategori | 2024 | % | 2021 | % | Perubahan |
|---|---|---|---|---|---|
| **Ada** lampu PJU tenaga surya | 30.476 | 36,16% | 24.766 | 29,45% | **+23,06% ↑** |
| **Tidak ada** | 53.800 | 63,84% | 59.330 | 70,55% | -9,32% ↓ |

**Top 5 Provinsi dengan PJU Surya (2024):**
1. Jawa Tengah — 3.478 desa (11,41%)
2. Jawa Timur — 2.722 desa (8,93%)
3. Jawa Barat — 2.654 desa (8,71%)
4. Sumatera Utara — 2.246 desa (7,37%)
5. Sumatera Selatan — 1.618 desa (5,31%)

**Insight:** Penggunaan lampu PJU tenaga surya naik signifikan (+23%), menandakan adopsi EBT di level infrastruktur publik membaik. Namun, **hampir 2/3 desa masih gelap** tanpa PJU surya.

---

### 3.2 Energi Surya — Rumah Tangga

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| Ada, sebagian **besar** RT | 3.076 | 3,65% | 4.176 | 4,97% |
| Ada, sebagian **kecil** RT | 8.019 | 9,52% | 7.895 | 9,39% |
| **Tidak ada** | 73.181 | 86,83% | 72.025 | 85,65% |

**Provinsi dengan adopsi tertinggi (sebagian besar RT, 2024):**
1. Papua Pegunungan — 648 desa (21,07%)
2. Kalimantan Tengah — 327 desa (10,63%)
3. Kalimantan Barat — 305 desa (9,92%)
4. NTT — 301 desa (9,79%)
5. Papua Tengah — 298 desa (9,69%)

**Insight KRITIS:** Adopsi surya RT di level "sebagian besar" justru **TURUN** dari 4.176 (2021) ke 3.076 (2024). Ini kontra-intuitif — kemungkinan ada masalah pemeliharaan panel surya setelah program selesai. Tingginya adopsi di Papua/Kalimantan kemungkinan bukan karena inovasi, tapi karena **tidak ada pilihan lain** (indikasi kemiskinan energi).

---

### 3.3 Bioenergi (Biogas)

| Kategori | 2024 | % | 2021 | % | Perubahan |
|---|---|---|---|---|---|
| **Ada** pemanfaatan biogas | 601 | 0,71% | 749 | 0,89% | **-19,76% ↓** |
| **Tidak ada** | 83.675 | 99,29% | 83.347 | 99,11% | +0,39% |

**Dominasi adopsi biogas (2024):**
1. Jawa Timur — 216 desa (35,94% dari total desa biogas)
2. Jawa Tengah — 151 desa (25,12%)
3. Jawa Barat — 58 desa (9,65%)

**Insight:** Adopsi biogas **MENURUN** dan sangat terkonsentrasi di Jawa. Dari 84.276 desa, hanya 601 yang memanfaatkan biogas. Di luar Jawa, hampir **nihil**. Ini menandakan kegagalan program difusi teknologi biogas ke luar Jawa.

---

### 3.4 Energi Air (Hidro/Mikrohidro)

#### Pemanfaatan (Realisasi)

| Sumber | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Sungai** | 743 | 71,51% | 934 | 73,43% |
| **Saluran Irigasi** | 144 | 13,86% | 176 | 13,84% |
| **Danau/Waduk/Situ/Bendungan** | 135 | 12,99% | 135 | 10,61% |
| **Embung** | 17 | 1,64% | 27 | 2,12% |
| **Total desa memanfaatkan** | **1.039** | — | **1.272** | — |

#### Potensi (Desa yang memiliki sumber perairan)

| Sumber | 2024 | % | 2021 |
|---|---|---|---|
| **Sungai** | 67.050 | 55,62% | 66.636 |
| **Saluran Irigasi** | 36.685 | 30,43% | 35.926 |
| **Danau/Waduk** | 5.954 | 4,94% | 5.911 |
| **Embung** | 10.857 | 9,01% | 12.813 |
| **Total desa berpotensi** | **120.546** | — | **121.286** |

**Insight KRITIS:** 
- **GAP SANGAT BESAR** antara potensi dan realisasi: 120.546 desa punya sumber perairan, tapi **hanya 1.039 yang memanfaatkan** (rasio 0,86%)
- Realisasi justru **TURUN** dari 1.272 (2021) ke 1.039 (2024) — penurunan 18,3%
- Sulawesi Barat & Selatan paling aktif memanfaatkan energi air (sungai)
- Catatan: *Data potensi merepresentasikan jumlah desa yang memiliki sumber perairan, bukan kelayakan teknis untuk pembangunan pembangkit listrik*

---

### 3.5 Kebijakan & Program Pengembangan EBT

| Kategori | 2024 | % |
|---|---|---|
| **Ada** program pengembangan EBT | 4.525 | **5,37%** |
| **Tidak ada** | 79.751 | 94,63% |

**Top 5 Provinsi dengan Program EBT:**
1. Jawa Timur — 679 desa (15,01%)
2. Jawa Tengah — 516 desa (11,40%)
3. Jawa Barat — 476 desa (10,52%)
4. Aceh — 225 desa (4,97%)
5. Sumatera Selatan — 196 desa (4,33%)

**Insight:** **94,63% desa TIDAK MEMILIKI program pengembangan EBT.** Program terkemuka terkonsentrasi di Jawa. Papua Pegunungan (0,11%), Papua Selatan (0,07%) — wilayah paling membutuhkan justru paling minim program.

---

### 3.6 Infrastruktur Energi

| Kategori | 2024 | % |
|---|---|---|
| **Ada** sarana prasarana energi | 7.346 | 8,72% |
| **Tidak ada** | 76.930 | 91,28% |

**Insight:** Hanya 8,72% desa memiliki infrastruktur energi. Jawa Timur mendominasi (15,11% dari total desa berinfrastruktur), sementara Papua Pegunungan hanya 0,16%.

---

### 3.7 Aset Energi Alam (Mata Air)

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Ada** mata air | 23.076 | 27,38% | 21.662 | 25,76% |
| **Tidak ada** | 52.714 | 62,55% | 53.973 | 64,18% |
| **Tidak diketahui** | 8.486 | 10,07% | 8.461 | 10,06% |

**Top 5 Provinsi dengan mata air (2024):**
1. Jawa Tengah — 2.935 desa (12,72%)
2. Jawa Timur — 2.442 desa (10,58%)
3. Jawa Barat — 1.914 desa (8,29%)
4. NTT — 1.660 desa (7,19%)
5. Sumatera Utara — 1.541 desa (6,68%)

**Insight:** Ada potensi besar yang belum tergarap — banyak desa punya mata air tapi belum dimanfaatkan untuk energi (*unused renewable potential*). Jumlah desa bermata air naik dari 2021 ke 2024.

---

### 3.8 Akses Energi — Keluarga Pengguna Listrik Non-PLN

| Kategori | 2024 | 2021 | Perubahan |
|---|---|---|---|
| **Total keluarga Non-PLN** | **1.177.328** | **1.526.832** | **-22,88% ↓** |

**Top 5 Provinsi konsentrasi Non-PLN (2024):**
1. Kalimantan Barat — 136.046 keluarga (11,58%)
2. Sumatera Selatan — 113.779 keluarga (9,68%)
3. Papua Tengah — 117.044 keluarga (9,96%)
4. NTT — 109.203 keluarga (9,29%)
5. Kalimantan Tengah — 93.946 keluarga (7,99%)

**Insight:** Jumlah keluarga non-PLN turun 22,88%, menandakan perluasan PLN. Namun, masih ada **1,17 juta keluarga** yang bergantung pada listrik non-PLN — ini adalah **pasar potensial EBT** sekaligus **indikator ketimpangan energi**.

---

### 3.9 Akses Energi — Keluarga Tanpa Listrik

| Kategori | 2024 | 2021 | Perubahan |
|---|---|---|---|
| **Total keluarga tanpa listrik** | **658.782** | **991.671** | **-33,56% ↓** |

**Top 5 Provinsi konsentrasi tanpa listrik (2024):**
1. Papua Pegunungan — 157.563 keluarga (23,92%)
2. Papua Tengah — 129.220 keluarga (19,61%)
3. NTT — 86.822 keluarga (13,18%)
4. Sumatera Utara — 44.308 keluarga (6,73%)
5. Papua Selatan — 40.298 keluarga (6,12%)

**Insight KRITIS:** Meskipun turun 33,56%, masih ada **658.782 keluarga Indonesia yang hidup tanpa listrik sama sekali.** Papua mendominasi secara masif — Papua Pegunungan + Papua Tengah + Papua Selatan = **hampir 50% dari total keluarga tanpa listrik nasional.** Ini adalah **krisis keadilan energi**.

---

### 3.10 Kerusakan Lingkungan

#### Pencemaran Air

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Ada** pencemaran air | 11.019 | 13,07% | 10.683 | 12,70% |
| **Tidak ada** | 73.257 | 86,93% | 73.413 | 87,30% |

#### Pencemaran Tanah

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Ada** pencemaran tanah | 947 | 1,12% | 1.499 | 1,78% |
| **Tidak ada** | 83.329 | 98,88% | 82.597 | 98,22% |

#### Pencemaran Udara

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Ada** pencemaran udara | 4.754 | 5,64% | 5.644 | 6,71% |
| **Tidak ada** | 79.522 | 94,36% | 78.452 | 93,29% |

**Top provinsi pencemaran air (2024):** Jawa Barat (12,29%), Jawa Tengah (12,40%), Jawa Timur (9,99%), Kalimantan Barat (6,17%), Kalimantan Tengah (5,19%)

**Insight:** Pencemaran air **NAIK**, sementara pencemaran tanah dan udara turun. Kalimantan (Barat, Tengah, Selatan, Timur, Utara) memiliki proporsi pencemaran **sangat tinggi relatif terhadap jumlah desanya** — kemungkinan berkorelasi kuat dengan aktivitas pertambangan.

---

### 3.11 Desa Tambang

#### A. Desa dengan Lokasi Penggalian C

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Ada** lokasi penggalian C | 15.927 | 18,90% | 16.334 | 19,42% |
| **Tidak ada** | 68.349 | 81,10% | 67.762 | 80,58% |

#### B. Penghasilan Utama dari Pertambangan

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Ada** | 937 | 1,11% | 599 | 0,71% |
| **Tidak ada** | 83.339 | 98,89% | 83.497 | 99,29% |

**Top 5 Provinsi desa pertambangan (2024):**
1. Kalimantan Tengah — 292 desa (**31,16%** dari total desa tambang!)
2. Kalimantan Timur — 94 desa (10,03%)
3. Kalimantan Barat — 50 desa (5,34%)
4. Kepulauan Bangka Belitung — 60 desa (6,40%)
5. Sulawesi Tenggara — 49 desa (5,23%)

**Insight:** Jumlah desa dengan penghasilan utama dari pertambangan **NAIK 56,4%** (599 → 937 desa). Kalimantan Tengah menyumbang sepertiga dari seluruh desa tambang nasional. Data ini penting untuk crosstab dengan dimensi EBT.

---

## 4. Temuan Kritis untuk Perspektif CELIOS

### ⚡ Ketimpangan Energi yang Mendalam
- **658.782 keluarga** masih hidup tanpa listrik — terkonsentrasi di Papua & NTT
- Sebaliknya, Jawa mendominasi hampir semua indikator positif EBT
- Gap Jawa vs luar Jawa sangat mencolok di semua dimensi

### 🔋 Gap Potensi vs Realisasi EBT
- **120.546 desa** punya sumber perairan → hanya **1.039** yang memanfaatkan (0,86%)
- **23.076 desa** punya mata air → berapa yang dimanfaatkan untuk energi? (perlu crosstab)
- Program EBT hanya menjangkau **5,37%** desa

### 🏭 Paradoks Desa Tambang
- Desa tambang **NAIK 56,4%** — ekspansi industri ekstraktif berlanjut
- Perlu dibuktikan: Apakah desa tambang lebih buruk dalam akses EBT?
- Kalimantan Tengah: 31% desa-nya bergantung pada tambang + pencemaran air/tanah tinggi

### 📉 Tren Mengkhawatirkan
- Realisasi energi air **TURUN** 18,3% (1.272 → 1.039 desa)
- Adopsi biogas **TURUN** 19,8% (749 → 601 desa)
- Lampu surya RT "sebagian besar" **TURUN** (4.176 → 3.076 desa)
- Pencemaran air **NAIK** (12,70% → 13,07%)

### ✅ Satu-satunya Tren Positif
- Lampu PJU surya **NAIK** 23% (24.766 → 30.476 desa)
- Keluarga tanpa listrik **TURUN** 33,56% (perluasan PLN)
- Keluarga non-PLN **TURUN** 22,88%

---

## 5. Rekomendasi Analisis Lanjutan (untuk Streamlit)

1. **Crosstab Desa Tambang × 10 Dimensi EBT** — sesuai brief Aulia
2. **Peta Korelasi Provinsi** — pencemaran × desa tambang × akses energi
3. **Indeks Kerentanan Energi** — komposit dari non-PLN, tanpa listrik, tanpa program EBT
4. **Gap Analysis** — potensi perairan vs realisasi per provinsi
5. **Tren 2021 → 2024** — identifikasi provinsi yang membaik vs memburuk

---

*Laporan ini disusun berdasarkan ekstraksi data dari 13 file PDF PODES yang disediakan oleh tim riset CELIOS.*
