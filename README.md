# Sistem Diagnosis Kerusakan SSD Menggunakan Algoritma C4.5

Aplikasi desktop berbasis Python dengan GUI Tkinter untuk mendiagnosis kesehatan SSD (Solid State Drive) menggunakan algoritma Decision Tree C4.5 kustom berdasarkan parameter S.M.A.R.T (Self-Monitoring, Analysis and Reporting Technology).

---

## 🎯 Fitur Utama

### 1. **Diagnosis SSD Baru**
- Input 8 parameter SMART SSD secara manual
- Prediksi status kesehatan (Normal/Rusak) menggunakan model C4.5
- Menampilkan probabilitas klasifikasi dengan progress bar kustom
- Analisis detail kerusakan dan rekomendasi perawatan
- Ikon visual besar untuk hasil diagnosis (✓ Normal / ✗ Rusak)

### 2. **Tambah Data Latih**
- Form input data latih baru langsung ke dataset CSV
- Pilihan status aktual (Normal/Rusak)
- Auto-increment nomor data
- Fitur latih ulang model setelah menambah data

### 3. **Visualisasi Pohon Keputusan Dinamis**
- Rendering pohon keputusan secara real-time menggunakan Canvas Tkinter
- **Highlight jalur keputusan** berdasarkan diagnosis terakhir (warna biru)
- Node dan cabang yang tidak dilewati ditampilkan abu-abu tipis
- Keterangan jalur keputusan di bawah canvas
- Dashboard metrik model (Akurasi, Kedalaman, Jumlah Leaf, Jumlah Data)
- Tombol popup **"Lihat Keterangan Atribut"** dengan tabel deskripsi parameter SMART

### 4. **Training Model**
- Algoritma C4.5 kustom (tanpa library sklearn decision tree)
- Menggunakan Gain Ratio untuk pemilihan atribut terbaik
- Support untuk data kontinu dengan threshold otomatis
- Evaluasi model (Accuracy, Classification Report, Confusion Matrix)

---

## 📦 Struktur Proyek

```
Sistem_Diagnosis_SSD/
├── app.py                 # Entry point GUI Tkinter
├── config.py              # Path dataset/model dan konfigurasi aplikasi
├── train_model.py         # Training model C4.5
├── predict.py             # Prediksi SSD menggunakan model tersimpan
├── requirements.txt       # Dependensi Python
├── dataset/dataset.csv    # Data latih SMART (separator ;)
├── model/                 # Model default dan metrik training
├── gui/                   # Halaman dan komponen GUI
└── utils/                 # Implementasi C4.5, loader, evaluator, dan helper algoritma
```

---

## 🚀 Cara Menjalankan

### Persyaratan

- Python 3.12 atau lebih baru
- Git, atau unduh source sebagai ZIP dari GitHub
- Tkinter tersedia pada instalasi Python (umumnya sudah termasuk di Windows)

### 1. Ambil source code

Clone repository:

```bash
git clone https://github.com/hendrazal/SSD_Diagnosis.git
cd SSD_Diagnosis
```

Atau unduh dan ekstrak ZIP repository, lalu buka terminal di folder hasil ekstraksi.

### 2. Buat virtual environment dan pasang dependensi

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Jika Tkinter belum tersedia di Linux, pasang paket Tkinter dari package manager distribusi (misalnya `python3-tk` di Debian/Ubuntu).

### 3. Jalankan aplikasi

```bash
python app.py
```

Repository menyertakan model default `model/model_c45.joblib`, jadi training ulang tidak diperlukan untuk menjalankan aplikasi. Jika file model tidak tersedia, latih model dari dataset:

```bash
python train_model.py
```

Training akan memperbarui model dan metrik di folder `model/`.

### 4. Verifikasi implementasi (opsional)

```bash
python test_implementation.py
```

Script ini memeriksa import, pemuatan model, prediksi, decision path, dan keberadaan file GUI.

---

## 📊 Parameter S.M.A.R.T yang Digunakan

| No | Parameter | Kode SMART | Deskripsi |
|----|-----------|------------|-----------|
| 1 | **Reallocated Sector Count** | SMART 5 | Jumlah sektor rusak yang telah dialokasikan ulang ke area cadangan |
| 2 | **Hardware ECC Recovered** | SMART C3 | Jumlah error bit yang diperbaiki oleh ECC internal controller |
| 3 | **Current Pending Sector Count** | SMART C5 | Sektor yang menunggu realokasi karena gangguan baca/tulis |
| 4 | **UltraDMA CRC Error Count** | SMART C7 | Error transmisi data antara SSD dan motherboard |
| 5 | **Power-On Hours** | SMART 9 | Total jam penggunaan SSD sejak pertama digunakan |
| 6 | **Power Cycle Count** | SMART 12 | Jumlah siklus power on/off SSD |
| 7 | **Total LBA Written (GB)** | - | Total data yang ditulis ke SSD (Gigabyte) |
| 8 | **Total LBA Read (GB)** | - | Total data yang dibaca dari SSD (Gigabyte) |

---

## 🎨 Spesifikasi Desain GUI

### Palet Warna
- **Background Utama**: `#F8F9FA` (Abu-abu terang kebiruan)
- **Sidebar**: `#0F3494` (Biru tua pekat)
- **Card Background**: `#FFFFFF` (Putih bersih)
- **Accent Normal**: `#10B981` (Hijau Emerald)
- **Accent Rusak**: `#EF4444` (Merah Coral)
- **Accent Aktif/Jalur**: `#2563EB` (Biru Royal)
- **Teks Utama**: `#1E293B`
- **Teks Sekunder**: `#64748B`

### Layout
- **Sidebar Navigasi**: 220px lebar tetap
- **Content Area**: Responsive dengan padding 30px
- **Form Grid**: 2 kolom untuk 8 parameter SMART
- **Card Style**: Rounded corners dengan border halus `#E2E8F0`

---

## 🔬 Algoritma C4.5 Kustom

### Keunggulan Implementasi
1. **Gain Ratio** untuk mengatasi bias Information Gain terhadap atribut dengan banyak nilai unik
2. **Threshold Otomatis** untuk atribut kontinu (mencari split point terbaik)
3. **Pruning Implisit** dengan `min_samples` parameter
4. **Decision Path Tracking** untuk visualisasi jalur keputusan

### Formula

**Entropy:**
```
H(S) = -Σ p(i) * log2(p(i))
```

**Information Gain:**
```
IG(S, A) = H(S) - Σ (|Sv| / |S|) * H(Sv)
```

**Split Information:**
```
SplitInfo(S, A) = -Σ (|Sv| / |S|) * log2(|Sv| / |S|)
```

**Gain Ratio:**
```
GainRatio(S, A) = IG(S, A) / SplitInfo(S, A)
```

---

## 🆕 Fitur Baru yang Diimplementasi

### 1. **Method get_decision_path() di utils/c45.py**
Melacak jalur keputusan dari root ke leaf untuk data tertentu.

**Return:**
- `path`: List node yang dilewati
- `directions`: List arah ('left'/'right'/'root')
- `path_text`: String deskripsi jalur (contoh: "Reallocated_Sector_Count = 0.00 <= 1.00 -> Hasil: Normal")

### 2. **Visualisasi Dinamis Canvas Tkinter**
Menggantikan sistem Matplotlib statis dengan:
- Canvas drawing real-time
- Highlight jalur keputusan warna biru tebal
- Node lain abu-abu tipis
- Scrollable untuk pohon besar

### 3. **Custom Progress Bar**
Progress bar horizontal kustom menggunakan Frame Tkinter dengan:
- Warna hijau untuk Normal (`#10B981`)
- Warna merah untuk Rusak (`#EF4444`)
- Persentase di tengah bar

### 4. **Popup Keterangan Atribut**
Window `tk.Toplevel` dengan `ttk.Treeview` berisi tabel deskripsi 8 parameter SMART.

### 5. **Tombol Navigasi ke Visualisasi**
Dari halaman hasil diagnosis, user dapat langsung membuka visualisasi pohon dengan jalur keputusan yang di-highlight.

---

## 📝 Format Dataset (dataset.csv)

**Separator:** `;` (titik koma)

**Struktur:**
```csv
No;Reallocated_Sector_Count;Hardware_ECC_Recovered;Current_Pending_Sector_Count;UltraDMA_CRC_Error_Count;Power_On_Hours;Power_Cycle_Count;Total_LBA_Written;Total_LBA_Read;Status
1;2;16;0;1;11847;29;2352;135686;Rusak
2;8;4904;0;0;9287;21;92303;3771;Rusak
3;0;0;0;3;14631;23;140872;330168;Normal
...
```

**Kolom:**
- `No`: Nomor urut (auto-increment)
- 8 kolom parameter SMART (numerik)
- `Status`: Label kelas ("Normal" atau "Rusak")

---

## 🧪 Testing

### Manual Testing Checklist

**Test 1: Input & Prediksi**
- [ ] Buka halaman "Diagnosis SSD Baru"
- [ ] Isi semua 8 parameter SMART
- [ ] Klik "Prediksi"
- [ ] Verifikasi hasil tampil dengan ikon besar
- [ ] Verifikasi progress bar kustom muncul
- [ ] Verifikasi analisis kerusakan ditampilkan

**Test 2: Visualisasi Dinamis**
- [ ] Dari halaman hasil, klik "Lihat Visualisasi Pohon Keputusan"
- [ ] Verifikasi pohon digambar di Canvas
- [ ] Verifikasi jalur keputusan di-highlight warna biru
- [ ] Verifikasi keterangan jalur di bawah canvas
- [ ] Scroll canvas untuk melihat seluruh pohon

**Test 3: Keterangan Atribut**
- [ ] Di halaman visualisasi, klik "Lihat Keterangan Atribut"
- [ ] Verifikasi popup terbuka dengan tabel 8 parameter
- [ ] Verifikasi deskripsi lengkap untuk setiap parameter

**Test 4: Tambah Data Latih**
- [ ] Buka halaman "Tambah Data Latih"
- [ ] Isi 8 parameter dan pilih Status
- [ ] Klik "Simpan ke Dataset"
- [ ] Verifikasi data tersimpan di dataset.csv
- [ ] Klik "Latih Ulang Model C4.5"
- [ ] Verifikasi model berhasil diupdate

---

## 🐛 Troubleshooting

### Error: "Model tidak ditemukan"
**Solusi:** Jalankan `python train_model.py` terlebih dahulu.

### Error: "TclError: Can't find a usable init.tcl"
**Solusi:** Tkinter tidak terinstall dengan benar. Reinstall Python dengan opsi Tcl/Tk enabled.

### Error: "UnicodeEncodeError"
**Solusi:** Sudah diperbaiki - karakter Unicode special (✓, ✗, →) diganti dengan ASCII.

### Visualisasi pohon terlalu kecil/besar
**Solusi:** Gunakan scrollbar horizontal/vertikal untuk navigasi, atau adjust `canvas_width` dan `canvas_height` di `visualization_page.py`.

---

## 📚 Referensi

1. Quinlan, J. R. (1993). C4.5: Programs for Machine Learning. Morgan Kaufmann.
2. S.M.A.R.T Attributes: https://en.wikipedia.org/wiki/S.M.A.R.T.
3. Tkinter Canvas: https://docs.python.org/3/library/tkinter.html

---

## 👨‍💻 Pengembang

**Hendra** - Sistem Diagnosis SSD untuk Skripsi

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik (skripsi).

---

## ✅ Status Implementasi

- [x] Algoritma C4.5 kustom
- [x] GUI Tkinter dengan 4 halaman
- [x] Input & Prediksi SSD
- [x] Tambah data latih
- [x] Visualisasi pohon dinamis dengan Canvas
- [x] Highlight jalur keputusan
- [x] Custom progress bar
- [x] Popup keterangan atribut SMART
- [x] Training & evaluasi model
- [x] Testing script

**Proyek Selesai 100%** ✓
