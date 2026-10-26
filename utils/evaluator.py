from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def evaluate_model(y_true, y_pred):
    """
    Mengevaluasi kinerja model klasifikasi.
    
    Parameter:
    y_true : array-like, label aktual/sebenarnya
    y_pred : array-like, label hasil prediksi model
    
    Return:
    dict berisi nilai metrik evaluasi (accuracy, confusion_matrix, classification_report)
    """
    accuracy = accuracy_score(y_true, y_pred)
    conf_matrix = confusion_matrix(y_true, y_pred)
    class_report = classification_report(y_true, y_pred)
    
    return {
        "accuracy": accuracy,
        "confusion_matrix": conf_matrix,
        "classification_report": class_report
    }
