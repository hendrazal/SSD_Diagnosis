import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    classification_report
)
from config import MODEL_PATH, BASE_DIR
from utils.data_loader import load_dataset
from sklearn.model_selection import train_test_split
import os


def evaluate_model(show_plot=True, save_plot=True):
    """
    Evaluasi model C4.5 dengan menampilkan:
    - Confusion Matrix
    - Accuracy
    - Precision
    - Recall
    - F1-Score
    - Classification Report
    
    Parameters:
    - show_plot: Menampilkan plot confusion matrix (default: True)
    - save_plot: Menyimpan plot ke file (default: True)
    
    Returns:
    - Dictionary berisi semua metrics
    """
    
    print('='*70)
    print('EVALUASI MODEL C4.5 - CONFUSION MATRIX & METRICS')
    print('='*70)
    print()

    # Load dataset
    df = load_dataset()

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

    TARGET_COLUMN = 'Status'

    # Preprocessing
    X = df[features].copy()
    y = df[TARGET_COLUMN]

    for col in features:
        X[col] = X[col].astype(str).str.replace(',', '.', regex=False)
        X[col] = pd.to_numeric(X[col], errors='coerce')

    data = pd.concat([X, y], axis=1)
    data = data.dropna()

    X = data[features]
    y = data[TARGET_COLUMN]

    # Split data (sama dengan train_model.py)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f'Total Data        : {len(df)}')
    print(f'Data Training     : {len(X_train)}')
    print(f'Data Testing      : {len(X_test)}')
    print()

    # Load model
    print('Loading model...')
    model = joblib.load(MODEL_PATH)
    print(f'Model loaded from: {MODEL_PATH}')
    print()

    # Prediksi
    print('Melakukan prediksi...')
    y_pred = model.predict(X_test)
    print('Prediksi selesai.')
    print()

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=['Normal', 'Rusak'])

    print('='*70)
    print('CONFUSION MATRIX:')
    print('='*70)
    print()
    print('                    Predicted')
    print('                  Normal    Rusak')
    print(f'Actual  Normal      {cm[0][0]:3d}       {cm[0][1]:3d}')
    print(f'        Rusak       {cm[1][0]:3d}       {cm[1][1]:3d}')
    print()

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label='Rusak')
    recall = recall_score(y_test, y_pred, pos_label='Rusak')
    f1 = f1_score(y_test, y_pred, pos_label='Rusak')

    print('='*70)
    print('METRICS EVALUASI:')
    print('='*70)
    print(f'Accuracy  : {accuracy:.4f} ({accuracy*100:.2f}%)')
    print(f'Precision : {precision:.4f} ({precision*100:.2f}%)')
    print(f'Recall    : {recall:.4f} ({recall*100:.2f}%)')
    print(f'F1-Score  : {f1:.4f} ({f1*100:.2f}%)')
    print()

    # Penjelasan Metrics
    print('='*70)
    print('PENJELASAN METRICS:')
    print('='*70)
    print('Accuracy  : Persentase prediksi yang benar dari seluruh prediksi')
    print('Precision : Dari semua yang diprediksi Rusak, berapa yang benar Rusak')
    print('Recall    : Dari semua yang sebenarnya Rusak, berapa yang terdeteksi')
    print('F1-Score  : Harmonic mean dari Precision dan Recall')
    print()

    # Classification Report
    print('='*70)
    print('CLASSIFICATION REPORT:')
    print('='*70)
    print(classification_report(y_test, y_pred))

    # Detail Confusion Matrix
    tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]

    print('='*70)
    print('DETAIL CONFUSION MATRIX:')
    print('='*70)
    print(f'True Positive (TP)  : {tp:2d}  (Prediksi Rusak, Aktual Rusak)')
    print(f'True Negative (TN)  : {tn:2d}  (Prediksi Normal, Aktual Normal)')
    print(f'False Positive (FP) : {fp:2d}  (Prediksi Rusak, Aktual Normal)')
    print(f'False Negative (FN) : {fn:2d}  (Prediksi Normal, Aktual Rusak)')
    print()

    # Interpretasi
    print('='*70)
    print('INTERPRETASI HASIL:')
    print('='*70)
    print(f'Total Data Test     : {len(y_test)}')
    print(f'Prediksi Benar      : {tp + tn} ({(tp+tn)/len(y_test)*100:.2f}%)')
    print(f'Prediksi Salah      : {fp + fn} ({(fp+fn)/len(y_test)*100:.2f}%)')
    print()
    
    if fp > 0:
        print(f'WARNING: Ada {fp} SSD Normal yang diprediksi sebagai Rusak (False Alarm)')
    if fn > 0:
        print(f'WARNING: Ada {fn} SSD Rusak yang diprediksi sebagai Normal (Missed Detection)')
    if fp == 0 and fn == 0:
        print('PERFECT: Semua prediksi sempurna!')
    print()

    # Visualisasi Confusion Matrix
    if show_plot or save_plot:
        print('Membuat visualisasi Confusion Matrix...')
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Confusion Matrix (Count)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Normal', 'Rusak'],
                    yticklabels=['Normal', 'Rusak'],
                    cbar_kws={'label': 'Count'},
                    ax=axes[0])
        axes[0].set_title('Confusion Matrix (Count)', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Actual', fontsize=12)
        axes[0].set_xlabel('Predicted', fontsize=12)
        
        # Plot 2: Confusion Matrix (Percentage)
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        sns.heatmap(cm_percent, annot=True, fmt='.1f', cmap='Blues', 
                    xticklabels=['Normal', 'Rusak'],
                    yticklabels=['Normal', 'Rusak'],
                    cbar_kws={'label': 'Percentage (%)'},
                    ax=axes[1])
        axes[1].set_title('Confusion Matrix (Percentage)', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Actual', fontsize=12)
        axes[1].set_xlabel('Predicted', fontsize=12)
        
        plt.tight_layout()
        
        if save_plot:
            output_path = os.path.join(BASE_DIR, 'model', 'confusion_matrix.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f'Visualisasi disimpan di: {output_path}')
        
        if show_plot:
            plt.show()
        else:
            plt.close()
    
    print()
    print('='*70)
    print('EVALUASI SELESAI')
    print('='*70)
    
    # Return metrics as dictionary
    results = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm,
        'true_positive': tp,
        'true_negative': tn,
        'false_positive': fp,
        'false_negative': fn,
        'y_test': y_test,
        'y_pred': y_pred
    }
    
    return results


if __name__ == "__main__":
    # Jalankan evaluasi
    results = evaluate_model(show_plot=False, save_plot=True)
    
    # Akses hasil jika dibutuhkan
    print(f'\nAccuracy: {results["accuracy"]:.4f}')
    print(f'F1-Score: {results["f1_score"]:.4f}')
