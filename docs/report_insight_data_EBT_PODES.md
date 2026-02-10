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

> [!NOTE]
> Penggunaan lampu PJU tenaga surya naik signifikan (+23%), menandakan adopsi EBT di level infrastruktur publik membaik. Namun, **hampir 2/3 desa masih gelap** tanpa PJU surya.

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

> [!WARNING]
> Adopsi surya RT di level "sebagian besar" justru **TURUN** dari 4.176 (2021) ke 3.076 (2024). Kemungkinan ada masalah pemeliharaan panel surya setelah program selesai. Tingginya di Papua/Kalimantan bukan karena inovasi — tapi karena **tidak ada pilihan lain** (indikasi kemiskinan energi).

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

> [!CAUTION]
> Adopsi biogas **MENURUN** dan sangat terkonsentrasi di Jawa. Dari 84.276 desa, hanya 601 yang memanfaatkan biogas. Di luar Jawa, hampir **nihil**. Kegagalan program difusi teknologi biogas ke luar Jawa.

---

### 3.4 Energi Air (Hidro/Mikrohidro)

#### Pemanfaatan (Realisasi)

| Sumber | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Sungai** | 743 | 71,51% | 934 | 73,43% |
| **Saluran Irigasi** | 144 | 13,86% | 176 | 13,84% |
| **Danau/Waduk/Situ** | 135 | 12,99% | 135 | 10,61% |
| **Embung** | 17 | 1,64% | 27 | 2,12% |
| **Total** | **1.039** | — | **1.272** | — |

#### Potensi (Desa dengan sumber perairan)

| Sumber | 2024 | 2021 |
|---|---|---|
| **Sungai** | 67.050 | 66.636 |
| **Saluran Irigasi** | 36.685 | 35.926 |
| **Danau/Waduk** | 5.954 | 5.911 |
| **Embung** | 10.857 | 12.813 |
| **Total** | **120.546** | **121.286** |

> [!CAUTION]
> **GAP SANGAT BESAR:** 120.546 desa punya sumber perairan → hanya **1.039 yang memanfaatkan** (rasio 0,86%). Realisasi justru **TURUN 18,3%** dari 2021 ke 2024.

---

### 3.5 Kebijakan & Program Pengembangan EBT

| Kategori | 2024 | % |
|---|---|---|
| **Ada** program EBT | 4.525 | **5,37%** |
| **Tidak ada** | 79.751 | 94,63% |

> [!IMPORTANT]
> **94,63% desa TIDAK MEMILIKI program pengembangan EBT.** Papua Pegunungan (0,11%), Papua Selatan (0,07%) — wilayah paling membutuhkan justru paling minim program.

---

### 3.6 Infrastruktur Energi

| Kategori | 2024 | % |
|---|---|---|
| **Ada** sarana prasarana energi | 7.346 | 8,72% |
| **Tidak ada** | 76.930 | 91,28% |

---

### 3.7 Aset Energi Alam (Mata Air)

| Kategori | 2024 | % | 2021 | % |
|---|---|---|---|---|
| **Ada** mata air | 23.076 | 27,38% | 21.662 | 25,76% |
| **Tidak ada** | 52.714 | 62,55% | 53.973 | 64,18% |
| **Tidak diketahui** | 8.486 | 10,07% | 8.461 | 10,06% |

> [!TIP]
> Banyak desa punya mata air tapi belum dimanfaatkan untuk energi → indikasi *unused renewable potential*.

---

### 3.8 Akses Energi — Keluarga Non-PLN

| Kategori | 2024 | 2021 | Perubahan |
|---|---|---|---|
| **Total keluarga Non-PLN** | **1.177.328** | **1.526.832** | **-22,88% ↓** |

**Top 5 konsentrasi Non-PLN (2024):**
1. Kalimantan Barat — 136.046 (11,58%)
2. Papua Tengah — 117.044 (9,96%)
3. Sumatera Selatan — 113.779 (9,68%)
4. NTT — 109.203 (9,29%)
5. Kalimantan Tengah — 93.946 (7,99%)

---

### 3.9 Akses Energi — Keluarga Tanpa Listrik

| Kategori | 2024 | 2021 | Perubahan |
|---|---|---|---|
| **Total tanpa listrik** | **658.782** | **991.671** | **-33,56% ↓** |

**Top 5 konsentrasi tanpa listrik (2024):**
1. Papua Pegunungan — 157.563 (23,92%)
2. Papua Tengah — 129.220 (19,61%)
3. NTT — 86.822 (13,18%)
4. Sumatera Utara — 44.308 (6,73%)
5. Papua Selatan — 40.298 (6,12%)

> [!CAUTION]
> **658.782 keluarga Indonesia hidup tanpa listrik.** Papua Pegunungan + Papua Tengah + Papua Selatan = hampir **50% dari total keluarga tanpa listrik nasional.** Ini adalah **krisis keadilan energi**.

---

### 3.10 Kerusakan Lingkungan

| Jenis Pencemaran | 2024 Ada | % | 2021 Ada | % | Tren |
|---|---|---|---|---|---|
| **Air** | 11.019 | 13,07% | 10.683 | 12,70% | **↑ NAIK** |
| **Tanah** | 947 | 1,12% | 1.499 | 1,78% | ↓ turun |
| **Udara** | 4.754 | 5,64% | 5.644 | 6,71% | ↓ turun |

> [!WARNING]
> Pencemaran air **NAIK**. Kalimantan memiliki proporsi pencemaran **sangat tinggi relatif terhadap jumlah desanya** — berkorelasi kuat dengan aktivitas pertambangan.

---

### 3.11 Desa Tambang

| Indikator | 2024 | % | 2021 | % | Tren |
|---|---|---|---|---|---|
| Ada lokasi penggalian C | 15.927 | 18,90% | 16.334 | 19,42% | ↓ turun |
| Penghasilan utama tambang | 937 | 1,11% | 599 | 0,71% | **+56,4% ↑** |

**Top Provinsi desa pertambangan (2024):**
1. Kalimantan Tengah — 292 desa (**31,16%!**)
2. Kalimantan Timur — 94 desa (10,03%)
3. Kepulauan Bangka Belitung — 60 desa (6,40%)

---

## 4. Temuan Kritis — Perspektif CELIOS

### ⚡ Ketimpangan Energi yang Mendalam
- **658.782 keluarga** tanpa listrik — terkonsentrasi di Papua & NTT
- Jawa mendominasi hampir semua indikator positif EBT
- Gap Jawa vs luar Jawa sangat mencolok di semua dimensi

### 🔋 Gap Potensi vs Realisasi EBT
- **120.546 desa** punya sumber perairan → hanya **1.039** memanfaatkan (0,86%)
- Program EBT hanya menjangkau **5,37%** desa
- Biogas dan energi air justru **menurun**

### 🏭 Paradoks Desa Tambang
- Desa tambang **NAIK 56,4%** — ekspansi industri ekstraktif berlanjut
- Kalimantan Tengah: 31% desa bergantung tambang + pencemaran tinggi
- Perlu dibuktikan via crosstab: desa tambang lebih buruk dalam akses EBT?

### 📉 Tren Mengkhawatirkan
- Realisasi energi air **↓ 18,3%**
- Adopsi biogas **↓ 19,8%**
- Lampu surya RT "sebagian besar" **↓**
- Pencemaran air **↑**

### ✅ Tren Positif
- Lampu PJU surya **↑ 23%**
- Keluarga tanpa listrik **↓ 33,56%** (perluasan PLN)
- Keluarga non-PLN **↓ 22,88%**

---

## 5. Rencana Analisis Lanjutan — Detail Metode & Algoritma

### 5.1 Crosstab Desa Tambang × 10 Dimensi EBT

**Tujuan:** Membuktikan apakah desa tambang memiliki akses EBT lebih buruk dari desa non-tambang.

| Komponen | Detail |
|---|---|
| **Metode** | Tabulasi silang (Cross-tabulation) |
| **Library** | `pandas.crosstab()` |
| **Input** | Kolom binary desa tambang (1/0) × setiap dimensi EBT (ada/tidak) |
| **Output** | Tabel frekuensi 2×2 per dimensi |
| **Uji Statistik** | Chi-Square Test of Independence (`scipy.stats.chi2_contingency`) |
| **Formula** | χ² = Σ ((O - E)² / E) — O = observed, E = expected |
| **Threshold** | p-value < 0.05 → hubungan signifikan |
| **Tujuan uji** | Membuktikan apakah ada/tidaknya EBT **tergantung** pada status desa tambang atau hanya kebetulan |

**Contoh output crosstab:**

|  | Punya Program EBT | Tidak Punya | Total |
|---|---|---|---|
| **Desa Tambang** | ? | ? | 937 |
| **Desa Non-Tambang** | ? | ? | 83.339 |
| **Total** | 4.525 | 79.751 | 84.276 |

---

### 5.2 Indeks Kerentanan Energi (IKE)

**Tujuan:** Membuat skor komposit per provinsi yang menggambarkan "seberapa rentan" provinsi tersebut dalam hal energi.

| Komponen | Detail |
|---|---|
| **Metode** | Composite Index — Weighted Sum + Min-Max Normalization |
| **Normalisasi** | Min-Max: `X_norm = (X - X_min) / (X_max - X_min)` |
| **Bobot** | Equal weight (masing-masing 20%) atau bisa disesuaikan |
| **Library** | `pandas`, `sklearn.preprocessing.MinMaxScaler` |
| **Arah** | Semakin tinggi skor = semakin rentan |

**Komponen IKE (5 variabel):**

| No | Variabel | Arah | Bobot |
|---|---|---|---|
| 1 | % keluarga tanpa listrik | ↑ semakin buruk | 20% |
| 2 | % keluarga non-PLN | ↑ semakin buruk | 20% |
| 3 | % desa tanpa program EBT | ↑ semakin buruk | 20% |
| 4 | % desa tanpa infrastruktur energi | ↑ semakin buruk | 20% |
| 5 | % desa dengan pencemaran air | ↑ semakin buruk | 20% |

**Formula:**
```
IKE_provinsi = Σ (bobot_i × nilai_norm_i)

Contoh:
IKE_Papua_Pegunungan = 0.2×(norm_tanpa_listrik) + 0.2×(norm_non_PLN)
                     + 0.2×(norm_tanpa_program) + 0.2×(norm_tanpa_infra)
                     + 0.2×(norm_pencemaran)
```

---

### 5.3 Gap Analysis — Potensi vs Realisasi per Provinsi

**Tujuan:** Mengukur "seberapa besar potensi EBT yang terbuang" di setiap provinsi.

| Komponen | Detail |
|---|---|
| **Metode** | Gap Ratio + Ranking |
| **Formula Gap** | `Gap_Ratio = (Potensi - Realisasi) / Potensi × 100` |
| **Formula Efisiensi** | `Efisiensi = Realisasi / Potensi × 100` |
| **Ranking** | Sort ascending by efisiensi → provinsi terburuk = potensi paling terbuang |
| **Library** | `pandas.DataFrame.sort_values()` |
| **Visualisasi** | Diverging bar chart (potensi kiri, realisasi kanan) |

**Diterapkan pada 3 pasangan data:**

| Potensi | Realisasi | Gap Nasional |
|---|---|---|
| Desa dengan sumber perairan (120.546) | Desa pakai PLTA (1.039) | 99,14% |
| Desa dengan mata air (23.076) | Desa pakai energi air (1.039) | 95,5% |
| Semua desa (84.276) | Desa punya program EBT (4.525) | 94,63% |

---

### 5.4 Korelasi Antar Dimensi per Provinsi

**Tujuan:** Mengukur hubungan antar variabel secara statistik, bukan asumsi logis.

| Komponen | Detail |
|---|---|
| **Metode** | Spearman Rank Correlation (data ordinal/tidak normal) |
| **Formula** | `ρ = 1 - (6 × Σd²) / (n × (n² - 1))` — d = selisih rank |
| **Library** | `scipy.stats.spearmanr` |
| **Input** | 38 provinsi × variabel-variabel numerik |
| **Output** | Correlation matrix + p-value matrix |
| **Visualisasi** | Heatmap korelasi (`plotly.express.imshow`) |

**Pasangan korelasi yang diuji:**

| Variabel A | Variabel B | Hipotesis |
|---|---|---|
| % desa tambang | % pencemaran air | Positif (tambang → cemar) |
| % desa tambang | % punya program EBT | Negatif (tambang → tanpa program) |
| % tanpa listrik | % desa tambang | Positif? (perlu diuji) |
| % punya surya RT | % tanpa listrik | Positif (surya = pengganti karena tak ada PLN) |
| % punya program EBT | % realisasi PLTA | Positif (program → realisasi?) |

---

### 5.5 Tren Perubahan 2021 → 2024 per Provinsi

**Tujuan:** Mengidentifikasi provinsi yang membaik vs memburuk dalam setiap dimensi.

| Komponen | Detail |
|---|---|
| **Metode** | Rate of Change + Classification |
| **Formula** | `ΔRate = ((V₂₀₂₄ - V₂₀₂₁) / V₂₀₂₁) × 100` |
| **Klasifikasi** | Membaik (>5%), Stagnan (-5% s/d +5%), Memburuk (<-5%) |
| **Library** | `pandas` |
| **Visualisasi** | Grouped bar chart / slope chart per provinsi |

**Diterapkan pada:**

| Dimensi | Tren Nasional | Yang Diukur per Provinsi |
|---|---|---|
| PJU Surya | +23,06% ↑ | Provinsi mana yang paling naik/turun? |
| Surya RT | -26,3% ↓ | Provinsi mana yang kehilangan adopsi? |
| Biogas | -19,76% ↓ | Provinsi mana yang masih bertahan? |
| PLTA | -18,3% ↓ | Provinsi mana yang paling kehilangan? |
| Tanpa listrik | -33,56% ↓ | Provinsi mana yang paling lambat turun? |
| Pencemaran air | +3,14% ↑ | Provinsi mana yang paling naik? |

---

### 5.6 Ringkasan Metode Keseluruhan

| No | Analisis | Metode | Library | Output |
|---|---|---|---|---|
| 1 | Crosstab Tambang × EBT | Chi-Square Test | `scipy.stats` | Tabel 2×2 + p-value |
| 2 | Indeks Kerentanan Energi | Min-Max + Weighted Sum | `pandas`, `sklearn` | Skor 0–1 per provinsi |
| 3 | Gap Potensi vs Realisasi | Gap Ratio + Ranking | `pandas` | % efisiensi per provinsi |
| 4 | Korelasi Antar Dimensi | Spearman Correlation | `scipy.stats` | Heatmap r + p-value |
| 5 | Tren 2021–2024 | Rate of Change | `pandas` | Klasifikasi per provinsi |

> [!IMPORTANT]
> Semua metode di atas akan menggunakan **data mentah dari Excel** (`Energi Terbarukan(AutoRecovered).xlsx`), bukan dari teks extract PDF. Ini menjamin akurasi angka dan memungkinkan analisis di level yang lebih granular.
