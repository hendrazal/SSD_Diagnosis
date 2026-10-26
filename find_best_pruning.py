import joblib
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from utils.c45 import C45Tree
from utils.data_loader import load_dataset
from utils.evaluator import evaluate_model
from config import TARGET_COLUMN


print("=" * 80)
print("MENCARI 3 KOMBINASI PRUNING TERBAIK (FAST VERSION)")
print("=" * 80)


# =====================================================
# LOAD & PREPROCESS DATA
# =====================================================
print("\n[1/3] Loading & Preprocessing Data...")
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

X = df[features].copy()
y = df[TARGET_COLUMN]

for col in features:
    X[col] = X[col].astype(str).str.replace(',', '.', regex=False)
    X[col] = pd.to_numeric(X[col], errors='coerce')

data = pd.concat([X, y], axis=1)
data = data.dropna()
X = data[features]
y = data[TARGET_COLUMN]

print(f"  Total samples: {len(X)}")


# =====================================================
# SPLIT DATA
# =====================================================
print("\n[2/3] Splitting Data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"  Training: {len(X_train)} samples")
print(f"  Testing: {len(X_test)} samples")


# =====================================================
# DEFINE CONFIGURATIONS TO TEST (15 configs only)
# =====================================================
print("\n[3/3] Testing Model...")
print("-" * 80)

test_configs = [
    # Baseline
    {'name': 'Normal', 'max_depth': None, 'min_samples_split': 1, 'min_samples_leaf': 1, 
     'max_leaf_nodes': None, 'min_impurity_decrease': 0.0},
    
    # Simple depth pruning
    {'name': 'Depth-3', 'max_depth': 2, 'min_samples_split': 2, 'min_samples_leaf': 1, 
     'max_leaf_nodes': None, 'min_impurity_decrease': 0.0},
    {'name': 'Depth-4', 'max_depth': 3, 'min_samples_split': 2, 'min_samples_leaf': 1, 
     'max_leaf_nodes': None, 'min_impurity_decrease': 0.0},
    
    # Min samples pruning
    {'name': 'Split-5', 'max_depth': None, 'min_samples_split': 5, 'min_samples_leaf': 1, 
     'max_leaf_nodes': None, 'min_impurity_decrease': 0.0},
    
    # Leaf nodes limit
    {'name': 'MaxLeaf-5', 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 
     'max_leaf_nodes': 5, 'min_impurity_decrease': 0.0},
    {'name': 'MaxLeaf-7', 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 
     'max_leaf_nodes': 7, 'min_impurity_decrease': 0.0},
    
]

results = []
train_data = pd.concat([X_train, y_train], axis=1)

for idx, config in enumerate(test_configs, 1):
    try:
        print(f"[{idx:2d}/{len(test_configs)}] {config['name']:20s} ", end='', flush=True)
        
        model = C45Tree(
            max_depth=config['max_depth'],
            min_samples_split=config['min_samples_split'],
            min_samples_leaf=config['min_samples_leaf'],
            max_leaf_nodes=config['max_leaf_nodes'],
            min_impurity_decrease=config['min_impurity_decrease']
        )
        
        model.fit(train_data, TARGET_COLUMN, features)
        
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        train_eval = evaluate_model(y_train, y_train_pred)
        test_eval = evaluate_model(y_test, y_test_pred)
        
        train_acc = train_eval['accuracy']
        test_acc = test_eval['accuracy']
        overfitting_gap = train_acc - test_acc
        
        depth = model.get_depth()
        leaves = model.get_n_leaves()
        
        # Score calculation
        score = test_acc * 0.7 + max(0, 1 - abs(overfitting_gap) * 5) * 0.2 + max(0, 1 - (depth + leaves) / 30.0) * 0.1
        
        results.append({
            'name': config['name'],
            'max_depth': config['max_depth'],
            'min_samples_split': config['min_samples_split'],
            'min_samples_leaf': config['min_samples_leaf'],
            'max_leaf_nodes': config['max_leaf_nodes'],
            'min_impurity_decrease': config['min_impurity_decrease'],
            'train_accuracy': float(train_acc),
            'test_accuracy': float(test_acc),
            'overfitting_gap': float(overfitting_gap),
            'tree_depth': int(depth),
            'tree_leaves': int(leaves),
            'score': float(score)
        })
        
        print(f">> Test: {test_acc:.4f}, Train: {train_acc:.4f}, Depth: {depth}, Leaves: {leaves}")
        
    except Exception as e:
        print(f">> FAILED: {str(e)}")
        continue


# =====================================================
# SORT & SELECT TOP 3
# =====================================================
print("\n" + "=" * 80)
print("TOP PRUNING TERBAIK")
print("=" * 80)

results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)
top_3 = results_sorted[:3]

for i, config in enumerate(top_3, 1):
    print(f"\n{'-' * 80}")
    print(f"RANK #{i}: {config['name']} (Score: {config['score']:.4f})")
    print(f"{'-' * 80}")
    print(f"Parameters:")
    print(f"  MAX_DEPTH             = {config['max_depth']}")
    print(f"  MIN_SAMPLES_SPLIT     = {config['min_samples_split']}")
    print(f"  MIN_SAMPLES_LEAF      = {config['min_samples_leaf']}")
    print(f"  MAX_LEAF_NODES        = {config['max_leaf_nodes']}")
    print(f"  MIN_IMPURITY_DECREASE = {config['min_impurity_decrease']}")
    print(f"\nResults:")
    print(f"  Tree Depth        : {config['tree_depth']}")
    print(f"  Tree Leaves       : {config['tree_leaves']}")
    print(f"  Training Accuracy : {config['train_accuracy']*100:.2f}%")
    print(f"  Testing Accuracy  : {config['test_accuracy']*100:.2f}%")
    print(f"  Overfitting Gap   : {abs(config['overfitting_gap'])*100:.2f}%")


# =====================================================
# SAVE RESULTS
# =====================================================
output_data = {
    'top_3': top_3,
    'all_results': results_sorted,
    'total_tested': len(results)
}

output_path = "model/best_pruning_configs.json"
with open(output_path, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"\n{'=' * 80}")
print(f"Results saved: {output_path}")
print(f"{'=' * 80}\n")
