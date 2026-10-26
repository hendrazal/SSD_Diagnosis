import joblib
import pandas as pd

from config import MODEL_PATH


# ==========================
# NAMA FITUR SMART
# HARUS SAMA DENGAN TRAINING
# ==========================
features = [
    'Reallocated_Sector_Count',
    'Hardware_ECC_Recovered',
    'Current_Pending_Sector_Count',
    'UltraDMA_CRC_Error_Count',
    'Power_On_Hours',
    'Power_Cycle_Count',
    'Total_LBA_Written',
    'Total_LBA_Read'
]


# ==========================
# FUNGSI PREDIKSI
# ==========================
def predict_ssd(data):
    """
    Parameter:
    data = dictionary berisi nilai SMART SSD

    Return:
    hasil prediksi dan confidence
    """
    # Load model setiap kali prediksi (untuk mendapatkan model terbaru)
    model = joblib.load(MODEL_PATH)
    
    # ubah dictionary menjadi dataframe
    input_data = pd.DataFrame(
        [data],
        columns=features
    )

    # prediksi kelas
    prediction = model.predict(input_data)

    # probabilitas/sebaran kelas
    probability = model.predict_proba(input_data)

    # Mengambil tingkat kepercayaan (confidence) untuk kelas yang diprediksi
    pred_class = prediction[0]
    class_idx = list(model.classes_).index(pred_class)
    confidence = probability[0][class_idx] * 100

    return {
        "status": pred_class,
        "confidence": round(confidence, 2)
    }


# ==========================
# TEST MANUAL
# ==========================
if __name__ == "__main__":
    sample_data = {
        'Reallocated_Sector_Count': 0,
        'Hardware_ECC_Recovered': 0,
        'Current_Pending_Sector_Count': 0,
        'UltraDMA_CRC_Error_Count': 3,
        'Power_On_Hours': 14631,
        'Power_Cycle_Count': 23,
        'Total_LBA_Written': 140872,
        'Total_LBA_Read': 330168
    }

    result = predict_ssd(sample_data)

    print("=" * 40)
    print("HASIL DIAGNOSIS SSD")
    print("=" * 40)
    print("Status SSD :", result["status"])
    print("Confidence :", result["confidence"], "%")