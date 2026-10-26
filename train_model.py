import joblib
import json
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from utils.c45 import C45Tree
from utils.data_loader import load_dataset
from utils.evaluator import evaluate_model
from utils.visualizer import plot_c45_tree
from config import (
    TARGET_COLUMN,
    MODEL_PATH,
    TREE_IMAGE_PATH,
    MODEL_PATH_UNPRUNED
)


print("=" * 70)
print("TRAINING MODEL C4.5 DENGAN PRE-PRUNING")
print("=" * 70)


# =====================================================
# PRE-PRUNING CONFIGURATION
# =====================================================
MAX_DEPTH = 2                 # None = unlimited (pohon murni)
MIN_SAMPLES_SPLIT = 2       # 1 = no restriction (pohon murni)
MIN_SAMPLES_LEAF = 1          # Minimum samples di leaf node
MAX_LEAF_NODES = None            # None = unlimited leaf nodes
MIN_IMPURITY_DECREASE = 0.00  # Minimum gain ratio untuk split

print(f"\nPre-Pruning Parameters:")
print(f"  MAX_DEPTH             : {MAX_DEPTH if MAX_DEPTH else 'Unlimited'}")
print(f"  MIN_SAMPLES_SPLIT     : {MIN_SAMPLES_SPLIT}")
print(f"  MIN_SAMPLES_LEAF      : {MIN_SAMPLES_LEAF}")
print(f"  MAX_LEAF_NODES        : {MAX_LEAF_NODES if MAX_LEAF_NODES else 'Unlimited'}")
print(f"  MIN_IMPURITY_DECREASE : {MIN_IMPURITY_DECREASE}")


# =====================================================
# LOAD DATASET
# =====================================================
print("\n[1/6] Loading Dataset...")
df = load_dataset()

features = [
    "Reallocated_Sector_Count",
    "Hardware_ECC_Recovered",
    "Current_Pending_Sector_Count",
    "UltraDMA_CRC_Error_Count",
    "Power_On_Hours",
    "Power_Cycle_Count",
    "Total_LBA_Written",
    "Total_LBA_Read"
]


# =====================================================
# PREPROCESS DATA
# =====================================================
print("\n[2/6] Preprocessing Data...")
X = df[features].copy()
y = df[TARGET_COLUMN]

for col in features:
    X[col] = X[col].astype(str).str.replace(',', '.', regex=False)
    X[col] = pd.to_numeric(X[col], errors='coerce')

data_before = len(X)
data = pd.concat([X, y], axis=1)
data = data.dropna()
data_after = len(data)

X = data[features]
y = data[TARGET_COLUMN]

print(f"  Data before cleaning : {data_before}")
print(f"  Data after cleaning  : {data_after}")
print(f"  Features             : {len(features)}")


# =====================================================
# SPLIT DATA
# =====================================================
print("\n[3/6] Splitting Data...")
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print(f"  Training set : {len(X_train)} samples")
print(f"  Testing set  : {len(X_test)} samples")


# =====================================================
# BUILD DECISION TREE (PRE-PRUNING)
# =====================================================
print("\n[4/6] Building Decision Tree with Pre-Pruning...")
train_data = pd.concat([X_train, y_train], axis=1)

c45_model = C45Tree(
    max_depth=MAX_DEPTH,
    min_samples_split=MIN_SAMPLES_SPLIT,
    min_samples_leaf=MIN_SAMPLES_LEAF,
    max_leaf_nodes=MAX_LEAF_NODES,
    min_impurity_decrease=MIN_IMPURITY_DECREASE
)

c45_model.fit(
    train_data,
    TARGET_COLUMN,
    features
)

print(f"  Tree Depth   : {c45_model.get_depth()}")
print(f"  Tree Leaves  : {c45_model.get_n_leaves()}")
print(f"  Root Node    : {c45_model.root.attribute}")
print(f"  Root Thresh  : {c45_model.root.threshold:.2f}")


# =====================================================
# EVALUATE MODEL
# =====================================================
print("\n[5/6] Evaluating Model...")

y_train_pred = c45_model.predict(X_train)
y_test_pred = c45_model.predict(X_test)

train_eval = evaluate_model(y_train, y_train_pred)
test_eval = evaluate_model(y_test, y_test_pred)

print(f"\n  Training Accuracy : {train_eval['accuracy']:.4f}")
print(f"  Testing Accuracy  : {test_eval['accuracy']:.4f}")
print(f"  Overfitting Gap   : {train_eval['accuracy'] - test_eval['accuracy']:.4f}")

print("\n  Classification Report (Test Set):")
print(test_eval["classification_report"])


# =====================================================
# SAVE MODEL & METRICS
# =====================================================
print("\n[6/6] Saving Model & Metrics...")

joblib.dump(c45_model, MODEL_PATH)
print(f"  Model saved: {MODEL_PATH}")

metrics_data = {
    "max_depth": MAX_DEPTH,
    "min_samples_split": MIN_SAMPLES_SPLIT,
    "min_samples_leaf": MIN_SAMPLES_LEAF,
    "max_leaf_nodes": MAX_LEAF_NODES,
    "min_impurity_decrease": MIN_IMPURITY_DECREASE,
    "tree_depth": int(c45_model.get_depth()),
    "tree_leaves": int(c45_model.get_n_leaves()),
    "train_accuracy": float(train_eval["accuracy"]),
    "test_accuracy": float(test_eval["accuracy"]),
    "overfitting_gap": float(train_eval["accuracy"] - test_eval["accuracy"])
}

metrics_path = os.path.join(os.path.dirname(MODEL_PATH), "metrics.json")
with open(metrics_path, "w") as f:
    json.dump(metrics_data, f, indent=4)

print(f"  Metrics saved: {metrics_path}")


# =====================================================
# VISUALIZE TREE
# =====================================================
print("\nGenerating Decision Tree Visualization...")
plot_c45_tree(c45_model, TREE_IMAGE_PATH)
print(f"  Tree visualization saved: {TREE_IMAGE_PATH}")


print("\n" + "=" * 70)
print("TRAINING COMPLETE!")
print("=" * 70)
print(f"\nModel Performance:")
print(f"  Tree Depth        : {c45_model.get_depth()}")
print(f"  Tree Leaves       : {c45_model.get_n_leaves()}")
print(f"  Training Accuracy : {train_eval['accuracy']:.4f}")
print(f"  Testing Accuracy  : {test_eval['accuracy']:.4f}")
print("=" * 70 + "\n")
