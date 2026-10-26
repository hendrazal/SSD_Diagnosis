"""
Script test untuk memverifikasi implementasi baru tanpa GUI
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("TEST IMPLEMENTASI SISTEM DIAGNOSIS SSD")
print("=" * 60)

# Test 1: Import modules
print("\n[TEST 1] Mengimport modules...")
try:
    from utils.c45 import C45Tree, C45Node
    print("[OK] utils.c45 berhasil diimport")
except Exception as e:
    print(f"[ERROR] Error import utils.c45: {e}")
    sys.exit(1)

try:
    import joblib
    import pandas as pd
    from config import MODEL_PATH
    print("[OK] Dependencies berhasil diimport")
except Exception as e:
    print(f"[ERROR] Error import dependencies: {e}")
    sys.exit(1)

# Test 2: Load model
print("\n[TEST 2] Memuat model C4.5...")
if not os.path.exists(MODEL_PATH):
    print(f"[ERROR] Model tidak ditemukan di {MODEL_PATH}")
    print("  Silakan jalankan train_model.py terlebih dahulu")
    sys.exit(1)

try:
    model = joblib.load(MODEL_PATH)
    print(f"[OK] Model berhasil dimuat dari {MODEL_PATH}")
    print(f"  - Root attribute: {model.root.attribute if model.root else 'None'}")
    print(f"  - Tree depth: {model.get_depth()}")
    print(f"  - Number of leaves: {model.get_n_leaves()}")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    sys.exit(1)

# Test 3: Test method get_decision_path
print("\n[TEST 3] Testing method get_decision_path()...")
try:
    # Check if method exists
    if not hasattr(model, 'get_decision_path'):
        print("[ERROR] Method get_decision_path() tidak ditemukan di model")
        sys.exit(1)
    
    # Test dengan sample data
    sample_data = pd.Series({
        'Reallocated_Sector_Count': 0,
        'Hardware_ECC_Recovered': 0,
        'Current_Pending_Sector_Count': 0,
        'UltraDMA_CRC_Error_Count': 3,
        'Power_On_Hours': 14631,
        'Power_Cycle_Count': 23,
        'Total_LBA_Written': 140872,
        'Total_LBA_Read': 330168
    })
    
    path = model.get_decision_path(sample_data)
    
    print("[OK] Method get_decision_path() berhasil dijalankan")
    print(f"  - Jumlah node dalam path: {len(path)}")
    
except Exception as e:
    print(f"[ERROR] Error testing get_decision_path(): {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test prediksi
print("\n[TEST 4] Testing prediksi dengan decision path...")
try:
    input_data = pd.DataFrame([sample_data])
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    
    print("[OK] Prediksi berhasil")
    print(f"  - Hasil prediksi: {prediction[0]}")
    print(f"  - Probabilitas: {probability[0]}")
    
except Exception as e:
    print(f"[ERROR] Error testing prediksi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Verify GUI files
print("\n[TEST 5] Verifikasi file GUI...")
gui_files = [
    "gui/input_page.py",
    "gui/result_page.py",
    "gui/dataset_page.py",
    "gui/visualization_page.py",
    "gui/main_window.py"
]

all_exist = True
for gui_file in gui_files:
    full_path = os.path.join(os.path.dirname(__file__), gui_file)
    if os.path.exists(full_path):
        print(f"[OK] {gui_file} exists")
    else:
        print(f"[ERROR] {gui_file} NOT FOUND")
        all_exist = False

if not all_exist:
    sys.exit(1)

print("\n" + "=" * 60)
print("SEMUA TEST BERHASIL!")
print("=" * 60)
print("\nImplementasi siap digunakan. Jalankan 'python app.py' untuk memulai GUI.")
