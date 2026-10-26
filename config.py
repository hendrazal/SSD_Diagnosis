import os

# Direktori utama proyek
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path dataset
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "dataset.csv")

# Path model hasil training
MODEL_PATH = os.path.join(BASE_DIR, "model", "model_c45.joblib")

# Path visualisasi Decision Tree
TREE_IMAGE_PATH = os.path.join(BASE_DIR, "model", "decision_tree.png")

# Konfigurasi aplikasi
WINDOW_TITLE = "Sistem Diagnosis SSD"
WINDOW_SIZE = "1200x700"

# Nama target/label pada dataset
TARGET_COLUMN = "Status"

# =====================================================
# KONFIGURASI REP (REDUCED ERROR PRUNING)
# =====================================================

# Path model REP (setelah pruning)
MODEL_PATH_REP = os.path.join(BASE_DIR, "model", "model_c45_rep.joblib")

# Path model unpruned (backup full tree sebelum pruning)
MODEL_PATH_UNPRUNED = os.path.join(BASE_DIR, "model", "model_c45_unpruned.joblib")

# Path visualisasi Decision Tree REP
TREE_IMAGE_PATH_REP = os.path.join(BASE_DIR, "model", "decision_tree_rep.png")
TREE_IMAGE_PATH_UNPRUNED = os.path.join(BASE_DIR, "model", "decision_tree_unpruned.png")

# Path metrics & comparison
PRUNING_METRICS_PATH = os.path.join(BASE_DIR, "model", "pruning_metrics.json")
COMPARISON_4_CONDITIONS_PATH = os.path.join(BASE_DIR, "model", "comparison_4_conditions.json")

# Path visualisasi comparison
COMPARISON_CHART_PATH = os.path.join(BASE_DIR, "model", "comparison_4_conditions.png")
OVERFITTING_CHART_PATH = os.path.join(BASE_DIR, "model", "overfitting_analysis.png")
CONFUSION_GRID_PATH = os.path.join(BASE_DIR, "model", "confusion_matrix_grid.png")
COMPLEXITY_CHART_PATH = os.path.join(BASE_DIR, "model", "complexity_comparison.png")

# Konfigurasi parameter REP
REP_CONFIG = {
    'train_size': 0.6,           # 60% data untuk training (36 data)
    'validation_size': 0.2,      # 20% data untuk validation (12 data)
    'test_size': 0.2,            # 20% data untuk testing (12 data)
    'min_samples_full': 2,       # Min samples untuk full tree (sebelum prune)
    'random_state': 42,          # Seed untuk reproducibility
    'stratify': True             # Stratified sampling untuk balance kelas
}