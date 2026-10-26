# Integrasi Model Pre-Pruning ke GUI

> Catatan: Dokumen ini menjelaskan implementasi GUI versi terdahulu. Halaman dan tombol konfigurasi model sudah dihapus dari aplikasi; training model tetap tersedia melalui `train_model.py` dan tombol latih ulang di halaman dataset.

## 🎯 Overview

Model pre-pruning C4.5 berhasil diintegrasikan ke dalam GUI Sistem Diagnosis SSD. User sekarang dapat mengkonfigurasi dan train model langsung dari interface tanpa perlu menjalankan script Python terpisah.

---

## ✨ Fitur Baru

### 1. **Halaman Konfigurasi Model**
   - Form input untuk 5 parameter pre-pruning
   - Preset cepat (Murni, Light, Heavy)
   - Real-time training langsung dari GUI
   - Display informasi model (depth, leaves, accuracy)

### 2. **Parameter Pre-Pruning**

| Parameter | Deskripsi | Default | Contoh |
|-----------|-----------|---------|--------|
| `max_depth` | Kedalaman maksimum pohon | None | 5, 7, None |
| `min_samples_split` | Min samples untuk split node | 2 | 5, 10 |
| `min_samples_leaf` | Min samples di leaf node | 1 | 3, 5 |
| `max_leaf_nodes` | Max jumlah leaf nodes | None | 5, 10, None |
| `min_impurity_decrease` | Min gain ratio untuk split | 0.0 | 0.01, 0.02 |

### 3. **Preset Cepat**

- **Murni**: Pohon tanpa batasan (max accuracy, high complexity)
  - max_depth=None, min_samples_split=1, min_samples_leaf=1, max_leaf_nodes=None, min_impurity_decrease=0.0

- **Light**: Pruning ringan (balanced)
  - max_depth=5, min_samples_split=3, min_samples_leaf=2, max_leaf_nodes=None, min_impurity_decrease=0.0

- **Heavy**: Pruning agresif (low complexity, better generalization)
  - max_depth=3, min_samples_split=10, min_samples_leaf=5, max_leaf_nodes=5, min_impurity_decrease=0.01

---

## 🚀 Cara Menggunakan

### **Step 1: Buka GUI**
```bash
python app.py
```

### **Step 2: Navigasi ke Konfigurasi Model**
- Klik tombol **"Konfigurasi Model"** di halaman Input Data

### **Step 3: Atur Parameter**
- **Opsi A**: Input manual parameter di form
- **Opsi B**: Klik salah satu preset (Murni/Light/Heavy)

### **Step 4: Train Model**
- Klik tombol **"Train Model"**
- Tunggu proses training selesai (beberapa detik)
- Model baru otomatis tersimpan dan langsung digunakan

### **Step 5: Gunakan Model Baru**
- Kembali ke halaman Input Data
- Lakukan prediksi menggunakan model yang baru di-train

---

## 📁 File yang Dimodifikasi

### **File Baru:**
```
gui/model_config_page.py    # Halaman konfigurasi model (486 lines)
```

### **File yang Diupdate:**
```
gui/main_window.py          # Tambah import ModelConfigPage
gui/input_page.py           # Tambah tombol "Konfigurasi Model"
predict.py                  # Load model dinamis setiap prediksi
```

---

## 🔧 Teknis Implementasi

### **1. Dynamic Model Loading**
```python
# predict.py - Load model setiap kali prediksi
def predict_ssd(data):
    model = joblib.load(MODEL_PATH)  # Fresh load
    # ... prediction logic
```

### **2. Training Pipeline**
```python
# model_config_page.py
def train_model(self):
    # 1. Parse parameters dari form
    # 2. Load & preprocess dataset
    # 3. Train model dengan C45Tree
    # 4. Evaluate (train & test)
    # 5. Save model ke MODEL_PATH
    # 6. Save metrics ke metrics.json
```

### **3. Model Info Display**
```python
# Otomatis load dari metrics.json
{
    "max_depth": 5,
    "min_samples_split": 3,
    "tree_depth": 4,
    "tree_leaves": 6,
    "train_accuracy": 0.95,
    "test_accuracy": 0.88
}
```

---

## 📊 Perbandingan Model

### **Model Murni vs Pruned**

| Aspek | Murni (None,1,1,None,0.0) | Pruned (3,10,5,5,0.01) |
|-------|---------------------------|------------------------|
| **Depth** | 6 | 3 |
| **Leaves** | 7 | 3 |
| **Train Acc** | 100% | 93.75% |
| **Test Acc** | 77.78% | 91.67% |
| **Overfitting** | 22.22% | 2.08% |
| **Kompleksitas** | Tinggi | Rendah |

**Rekomendasi**: Gunakan pruned model untuk generalisasi lebih baik!

---

## 🎨 UI/UX Features

### **Panel Kiri - Configuration**
- Form input dengan hint text
- Preset buttons untuk quick selection
- Train button dengan feedback visual

### **Panel Kanan - Information**
- Real-time display info model
- Tree structure (depth & leaves)
- Performance metrics (accuracy, overfitting gap)
- Parameter yang sedang digunakan

### **User Experience**
- ✅ Validasi input otomatis
- ✅ Konfirmasi sebelum training
- ✅ Progress indicator saat training
- ✅ Success message dengan summary
- ✅ Error handling yang informatif

---

## 🔍 Troubleshooting

### **Model tidak berubah setelah training:**
- Pastikan tidak ada error saat training
- Check file `model/model_c45.joblib` apakah updated
- Restart aplikasi jika perlu

### **Training terlalu lama:**
- Normal jika dataset besar (>100 samples)
- Gunakan parameter yang lebih restrictive

### **Error "module not found":**
```bash
# Pastikan semua dependencies terinstall
pip install -r requirements.txt
```

---

## 📝 Notes

- Model otomatis tersimpan ke `model/model_c45.joblib`
- Metrics tersimpan ke `model/metrics.json`
- Training menggunakan split 70% train / 30% test
- Random state = 42 untuk reproducibility

---

## ✅ Testing Checklist

- [x] Halaman Model Config dapat diakses dari Input Page
- [x] Form parameter dapat diisi manual
- [x] Preset buttons berfungsi
- [x] Training berhasil dengan berbagai parameter
- [x] Model baru langsung digunakan untuk prediksi
- [x] Info model terupdate setelah training
- [x] Error handling berfungsi dengan baik
- [x] UI responsive dan user-friendly

---

## 🎯 Next Steps (Optional)

1. **Model Comparison**: Tambah fitur untuk compare multiple models
2. **History**: Simpan history training dengan timestamp
3. **Best Model Finder**: Integrasi script `find_best_pruning.py`
4. **Export/Import**: Export model configuration ke JSON
5. **Validation Set**: Tambah opsi split train/val/test

---

**Dokumentasi dibuat:** 2026-09-08  
**Status:** ✅ Production Ready
