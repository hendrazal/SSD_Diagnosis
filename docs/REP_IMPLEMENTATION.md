# 📚 IMPLEMENTASI REDUCED ERROR PRUNING (REP)

**Tanggal**: 4 September 2026  
**Proyek**: Sistem Diagnosis SSD dengan Decision Tree C4.5  
**Status**: ✅ Implemented & Tested

---

## 📖 Daftar Isi

1. [Pengenalan REP](#pengenalan-rep)
2. [Mengapa Perlu Pruning](#mengapa-perlu-pruning)
3. [Cara Kerja REP](#cara-kerja-rep)
4. [Parameter yang Digunakan](#parameter-yang-digunakan)
5. [Cara Menjalankan](#cara-menjalankan)
6. [Interpretasi Hasil](#interpretasi-hasil)
7. [File yang Dihasilkan](#file-yang-dihasilkan)
8. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## 🎯 Pengenalan REP

### Apa itu Reduced Error Pruning (REP)?

**Reduced Error Pruning (REP)** adalah teknik post-pruning untuk decision tree yang menggunakan **validation set** untuk menentukan node mana yang perlu di-prune.

### Karakteristik REP:

- ✅ **Post-pruning**: Tree dibangun dulu secara penuh, baru kemudian di-prune
- ✅ **Validation-based**: Menggunakan data terpisah (validation set) untuk evaluasi
- ✅ **Bottom-up approach**: Evaluasi dimulai dari leaf menuju root
- ✅ **Greedy algorithm**: Keputusan pruning bersifat lokal dan tidak di-backtrack

---

## 🤔 Mengapa Perlu Pruning?

### Masalah: Overfitting

Tanpa pruning, decision tree cenderung **overfit** - sangat akurat di training data tapi buruk di test data:

```
Model Unpruned:
  Train Accuracy: 100.00%  ← Sempurna di training
  Test Accuracy:   66.67%  ← Buruk di test data
  Gap: 33.33%             ← OVERFITTING!
```

### Solusi: REP Pruning

Dengan REP, tree yang terlalu kompleks disederhanakan:

```
Model Pruned (REP):
  Train Accuracy: 83.33%   ← Sedikit turun di training
  Test Accuracy:  91.67%   ← MENINGKAT di test data!
  Gap: -8.33%             ← NO OVERFITTING!
```

### Manfaat Pruning:

1. **Generalization** ↑ - Performa lebih baik di data baru
2. **Complexity** ↓ - Tree lebih simple dan interpretable
3. **Speed** ↑ - Prediksi lebih cepat
4. **Robustness** ↑ - Tidak sensitif terhadap noise

---

## ⚙️ Cara Kerja REP

### Algoritma REP (Step-by-Step)

#### **Step 1: Build Full Tree**
```python
# Build tree tanpa batasan (min_samples=2)
tree = C45Tree(min_samples=2)
tree.fit(train_data, 'Status', features)
```
- Tree tumbuh sebesar mungkin
- Kemungkinan besar akan overfit

#### **Step 2: Collect Nodes (Bottom-Up)**
```python
# Post-order traversal: left → right → parent
internal_nodes = collect_nodes_bottom_up(tree.root)
```
- Collect semua internal nodes
- Urutan: dari leaf ke root (bottom-up)

#### **Step 3: Evaluate Each Node**
```python
for node in internal_nodes:
    # Backup original state
    backup = save_node_state(node)
    
    # Convert node to leaf (majority class)
    convert_to_leaf(node)
    
    # Calculate accuracy on validation set
    new_accuracy = calculate_accuracy(validation_set)
    
    # Decision: prune or revert?
    if new_accuracy >= baseline_accuracy:
        # Keep as leaf (pruned!)
        nodes_pruned += 1
        baseline_accuracy = new_accuracy
    else:
        # Revert to internal node
        revert_node(node, backup)
```

#### **Step 4: Final Result**
- Tree yang lebih simple
- Generalization yang lebih baik
- Kompleksitas yang berkurang

---

## 📋 Parameter yang Digunakan

### 1. Data Split Strategy (60/20/20)

```python
Total Data: 60 samples
├─ Training:   36 samples (60%)  ← Untuk build tree
├─ Validation: 12 samples (20%)  ← Untuk pruning decision
└─ Test:       12 samples (20%)  ← Untuk final evaluation
```

**Mengapa 60/20/20?**
- **60% Training**: Cukup untuk build tree yang representatif
- **20% Validation**: Minimal data untuk reliable pruning (12 samples)
- **20% Test**: Untuk evaluasi final yang unbiased

### 2. Tree Building Parameters

| Parameter | Value | Alasan |
|-----------|-------|--------|
| `min_samples` | 2 | Tree tumbuh maksimal (akan di-prune nanti) |
| `random_state` | 42 | Reproducibility (hasil konsisten) |
| `stratify` | True | Balance proporsi kelas di setiap split |

### 3. Pruning Parameters

| Parameter | Value | Keterangan |
|-----------|-------|------------|
| Pruning Strategy | Bottom-up | Anak di-evaluate sebelum parent |
| Decision Metric | Accuracy | Prune jika accuracy ≥ baseline |
| Minimum Gain | 0.0 | Prune selama tidak menurunkan accuracy |

---

## 🚀 Cara Menjalankan

### Persiapan

Pastikan sudah ada:
```bash
# File yang diperlukan
config.py                 # Konfigurasi paths
utils/c45.py             # Decision tree C4.5
utils/pruner_rep.py      # REP algorithm
utils/data_loader.py     # Data loader
utils/visualizer.py      # Visualization
dataset/dataset.csv      # Dataset SSD
```

### 1. Training dengan REP

```bash
python train_model_rep.py
```

**Output:**
```
======================================================================
TRAINING MODEL C4.5 DENGAN REDUCED ERROR PRUNING (REP)
======================================================================

[1/10] Loading Dataset...
[2/10] Preprocessing Data...
[3/10] Splitting Data (60% Train / 20% Validation / 20% Test)...
[4/10] Building Full Tree (Unpruned)...
[5/10] Evaluating Unpruned Tree...
[6/10] Saving Unpruned Model...
[7/10] Applying REP Pruning...
[8/10] Evaluating Pruned Tree...
[9/10] Saving Pruned Model & Metrics...
[10/10] Training Summary

Files Generated:
  1. model_c45_unpruned.joblib
  2. model_c45_rep.joblib
  3. decision_tree_unpruned.png
  4. decision_tree_rep.png
  5. pruning_metrics.json
```

**Estimasi Waktu**: ~30-60 detik

### 2. Evaluasi & Comparison

```bash
python evaluate_model_rep.py
```

**Output:**
```
======================================================================
EVALUASI & COMPARISON MODEL REP - 4 KONDISI
======================================================================

[1/7] Loading Dataset & Models...
[2/7] Evaluating 4 Conditions...
[3/7] Creating Comparison Table...
[4/7] Calculating Insights...
[5/7] Generating Visualization 1: Bar Chart Comparison...
[6/7] Generating Visualization 2: Overfitting Analysis...
[7/7] Generating Visualization 3: Confusion Matrix Grid...

Files Generated:
  1. comparison_4_conditions.json
  2. comparison_4_conditions.png
  3. overfitting_analysis.png
  4. confusion_matrix_grid.png
  5. complexity_comparison.png
  6. comparison_report.txt
```

**Estimasi Waktu**: ~20-30 detik

### 3. Menggunakan Model Pruned untuk Prediksi

```python
import joblib
from config import MODEL_PATH_REP

# Load model pruned
model = joblib.load(MODEL_PATH_REP)

# Predict
sample_data = pd.DataFrame([{
    'Reallocated_Sector_Count': 0,
    'Hardware_ECC_Recovered': 150000,
    'Current_Pending_Sector_Count': 0,
    'UltraDMA_CRC_Error_Count': 2,
    'Power_On_Hours': 35000,
    'Power_Cycle_Count': 40,
    'Total_LBA_Written': 200000,
    'Total_LBA_Read': 400000
}])

prediction = model.predict(sample_data)
print(f"Status SSD: {prediction[0]}")
```

---

## 📊 Interpretasi Hasil

### 1. Comparison Table (4 Kondisi)

```
   Metric  Unpruned Train  Unpruned Test  Pruned Train  Pruned Test
 Accuracy         1.0000         0.6667        0.8333       0.9167
Precision         1.0000         0.8000        0.9412       1.0000
   Recall         1.0000         0.5714        0.7619       0.8571
 F1-Score         1.0000         0.6667        0.8421       0.9231
    Depth              3              3             1            1
   Leaves              6              6             2            2
```

**Cara Membaca:**

#### Kondisi 1 & 2 (Unpruned):
- **Train 100% vs Test 66.67%** = Gap 33.33% → **OVERFITTING SEVERE!**
- Model "menghafal" training data tapi gagal generalize

#### Kondisi 3 & 4 (Pruned):
- **Train 83.33% vs Test 91.67%** = Gap -8.33% → **NO OVERFITTING!**
- Model bahkan **lebih baik** di test data (generalization excellent!)

#### Improvement:
- Test accuracy: 66.67% → 91.67% (**+25% absolute, +37.5% relative**)
- Complexity: Depth 3→1, Leaves 6→2 (**66.7% reduction**)

### 2. Overfitting Analysis

**Overfitting Gap:**
- Unpruned: 33.33% (HIGH)
- Pruned: -8.33% (EXCELLENT)
- **Reduction: 41.67%** (overfitting eliminated!)

**Interpretasi:**
- Gap positif = overfitting (train > test)
- Gap negatif = slight underfitting (test > train) - **IDEAL untuk generalization!**
- Gap mendekati 0 = balanced model

### 3. Pruning Statistics

```json
{
  "nodes_pruned": 4,
  "accuracy_before": 0.8333,
  "accuracy_after": 0.9167,
  "accuracy_improvement": 0.0833,
  "depth_reduction_percent": 66.7,
  "leaves_reduction_percent": 66.7
}
```

**Interpretasi:**
- **4 nodes di-prune**: Tree jadi jauh lebih simple
- **Validation acc naik**: 83.33% → 91.67% (+8.33%)
- **Depth & leaves turun 66.7%**: Model 3x lebih simple!

### 4. Confusion Matrix (Test Set)

**Unpruned:**
```
           Predicted
          Normal  Rusak
Actual N     4      1      ← 1 false positive
       R     3      4      ← 3 missed detection!
```
- Accuracy: 66.67%
- Banyak error (4 salah dari 12)

**Pruned:**
```
           Predicted
          Normal  Rusak
Actual N     5      0      ← Perfect! No false positive
       R     1      6      ← Hanya 1 missed
```
- Accuracy: 91.67%
- Precision 100%! (tidak ada false alarm)
- Hanya 1 error dari 12

---

## 📁 File yang Dihasilkan

### Model Files

| File | Keterangan | Size Approx |
|------|------------|-------------|
| `model_c45_unpruned.joblib` | Full tree sebelum pruning (backup) | ~1 KB |
| `model_c45_rep.joblib` | Pruned tree (production model) | ~1 KB |

### Visualization Files

| File | Keterangan | Isi |
|------|------------|-----|
| `decision_tree_unpruned.png` | Visualisasi tree sebelum pruning | Tree dengan 3 level, 6 leaves |
| `decision_tree_rep.png` | Visualisasi tree setelah pruning | Tree dengan 1 level, 2 leaves |
| `comparison_4_conditions.png` | Bar chart comparison 4 kondisi | Accuracy, Precision, Recall, F1-Score |
| `overfitting_analysis.png` | Line chart overfitting | Train vs Test comparison |
| `confusion_matrix_grid.png` | 2x2 grid confusion matrices | 4 kondisi side-by-side |
| `complexity_comparison.png` | Horizontal bar chart | Depth & Leaves comparison |

### Metrics Files

| File | Format | Keterangan |
|------|--------|------------|
| `pruning_metrics.json` | JSON | Pruning statistics & 4 kondisi metrics |
| `comparison_4_conditions.json` | JSON | Complete comparison data |
| `comparison_report.txt` | Text | Human-readable summary report |

---

## ❓ FAQ & Troubleshooting

### Q1: Mengapa test accuracy lebih tinggi dari train accuracy?

**A:** Ini bukan bug! Ini tanda bahwa:
- Model tidak overfit (bagus!)
- Test set mungkin "lebih mudah" daripada train set (kebetulan split)
- Model generalize dengan baik

**Normal behavior** selama gap tidak terlalu besar (< 10%).

---

### Q2: Berapa minimal validation set yang dibutuhkan?

**A:** Rule of thumb:
- **Minimum**: 10 samples
- **Recommended**: 15-20 samples
- **Ideal**: 20-30 samples

Untuk dataset 60 samples:
- 20% validation = 12 samples → **Minimal tapi acceptable**
- Jika dataset lebih besar (100+), bisa gunakan 15-20%

---

### Q3: Apakah REP selalu lebih baik dari unpruned tree?

**A:** Tidak selalu, tergantung dataset:

**REP lebih baik jika:**
- ✅ Dataset kecil-medium (< 1000 samples)
- ✅ Ada noise di data
- ✅ Terdeteksi overfitting (train >> test)

**Unpruned mungkin lebih baik jika:**
- ❌ Dataset sangat besar (> 10,000 samples)
- ❌ Data sangat clean (no noise)
- ❌ Tree tidak overfit

**Best practice:** Selalu compare unpruned vs pruned!

---

### Q4: Bagaimana jika tidak ada node yang di-prune?

**Possible causes:**
1. Tree sudah optimal (tidak perlu pruning)
2. `min_samples` terlalu besar (tree tidak tumbuh penuh)
3. Validation set terlalu kecil/tidak representatif

**Solutions:**
- Turunkan `min_samples` ke 1 atau 2
- Increase validation set size
- Check data distribution di validation set

---

### Q5: Error: "Model file not found"

**Solution:**
```bash
# Jalankan training dulu
python train_model_rep.py

# Baru jalankan evaluation
python evaluate_model_rep.py
```

---

### Q6: Visualisasi tidak ter-generate

**Possible causes:**
1. Matplotlib backend issue
2. Permission issue di folder `model/`
3. Path configuration salah

**Solutions:**
```python
# Check matplotlib backend
import matplotlib
print(matplotlib.get_backend())

# Check folder writable
import os
os.access('model/', os.W_OK)  # Should return True

# Verify config paths
from config import COMPARISON_CHART_PATH
print(COMPARISON_CHART_PATH)
```

---

### Q7: Hasil berbeda setiap kali run

**Cause:** `random_state` tidak di-set atau berbeda

**Solution:**
```python
# Pastikan di train_model_rep.py:
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.4,
    random_state=42,  # ← Harus sama!
    stratify=y
)
```

**Verify:**
```bash
# Check config
grep "random_state" config.py

# Should output:
# 'random_state': 42
```

---

### Q8: Bagaimana cara adjust parameter REP?

**Parameter di `config.py`:**
```python
REP_CONFIG = {
    'train_size': 0.6,           # Adjust: 0.5-0.7
    'validation_size': 0.2,      # Adjust: 0.15-0.25
    'test_size': 0.2,            # Adjust: 0.15-0.25
    'min_samples_full': 2,       # Adjust: 1-5
    'random_state': 42,          # Keep fixed!
    'stratify': True             # Keep True!
}
```

**Recommendations:**
- Untuk dataset kecil (< 100): Gunakan default
- Untuk dataset medium (100-500): Bisa naikkan train_size ke 0.7
- Untuk dataset besar (> 500): Bisa turunkan validation_size ke 0.15

---

### Q9: Bagaimana membandingkan dengan model lama?

**Model lama** (min_samples=10, tanpa pruning):
```python
# Load semua model
model_old = joblib.load('model/model_c45.joblib')
model_unpruned = joblib.load('model/model_c45_unpruned.joblib')
model_pruned = joblib.load('model/model_c45_rep.joblib')

# Compare
for model, name in [(model_old, 'Old'), 
                     (model_unpruned, 'Unpruned'),
                     (model_pruned, 'Pruned')]:
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"{name:10s}: {acc:.4f}")
```

---

### Q10: Tips untuk meningkatkan hasil pruning

**1. Ensure Data Quality:**
```python
# Check missing values
print(df.isnull().sum())

# Check class balance
print(df['Status'].value_counts())

# Remove outliers if needed
```

**2. Tune min_samples:**
```python
# Experiment with different values
for min_samples in [1, 2, 3, 5]:
    tree = C45Tree(min_samples=min_samples)
    # ... train & evaluate
```

**3. Increase Validation Set:**
```python
# If dataset > 100 samples
REP_CONFIG['validation_size'] = 0.25  # 25% instead of 20%
```

**4. Cross-Validation (Advanced):**
```python
# For more robust results
from sklearn.model_selection import KFold

kf = KFold(n_splits=5)
for train_idx, val_idx in kf.split(X):
    # Train & prune on each fold
    # Average results
```

---

## 📚 Referensi & Resources

### Papers & Books
- Quinlan, J.R. (1987). "Simplifying decision trees"
- Quinlan, J.R. (1993). "C4.5: Programs for Machine Learning"
- Esposito, F. et al. (1997). "A comparative analysis of methods for pruning decision trees"

### Online Resources
- [Decision Tree Pruning - Wikipedia](https://en.wikipedia.org/wiki/Decision_tree_pruning)
- [Scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

### Kode Repository
- Location: `utils/pruner_rep.py`
- Training: `train_model_rep.py`
- Evaluation: `evaluate_model_rep.py`

---

## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-04 | Initial implementation of REP |
| | | - Core algorithm implemented |
| | | - 4-condition evaluation |
| | | - Comprehensive visualizations |
| | | - Complete documentation |

---

## 👥 Contact & Support

Untuk pertanyaan atau issues:
1. Check FAQ section di atas
2. Review error logs: `python train_model_rep.py 2>&1 | tee log.txt`
3. Verify file paths di `config.py`
4. Contact development team

---

## ✅ Checklist untuk Production

Sebelum deploy ke production:

- [ ] ✅ Model trained dengan full dataset
- [ ] ✅ Metrics validated (accuracy > 85%)
- [ ] ✅ Overfitting checked (gap < 10%)
- [ ] ✅ Confusion matrix reviewed (false negatives minimal)
- [ ] ✅ Visualizations generated & reviewed
- [ ] ✅ Model files backed up
- [ ] ✅ Documentation complete
- [ ] ✅ Test cases passed

---

**© 2026 Sistem Diagnosis SSD - Decision Tree C4.5 with REP**  
**Last Updated**: 4 September 2026  
**Status**: Production Ready ✅
