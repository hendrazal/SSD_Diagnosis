import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score


class ReducedErrorPruner:
    """
    Reduced Error Pruning (REP) untuk Decision Tree C4.5.
    
    REP adalah teknik post-pruning yang menggunakan validation set untuk
    menentukan node mana yang perlu di-prune. Algorithm bekerja dengan
    cara bottom-up: evaluasi setiap internal node, jika mengubahnya menjadi
    leaf tidak menurunkan accuracy di validation set, maka node tersebut
    di-prune (diubah menjadi leaf).
    
    Parameters:
    -----------
    tree : C45Tree
        Instance dari C45Tree yang sudah di-fit dengan training data
    X_val : pandas.DataFrame
        Features dari validation set
    y_val : pandas.Series
        Target labels dari validation set
    target_column : str
        Nama kolom target di dataset
    
    Attributes:
    -----------
    tree : C45Tree
        Reference ke decision tree yang akan di-prune
    X_val : DataFrame
        Validation features
    y_val : Series
        Validation labels
    target_column : str
        Nama kolom target
    pruning_log : list
        Log dari setiap pruning action yang dilakukan
    depth_before : int
        Kedalaman tree sebelum pruning
    leaves_before : int
        Jumlah leaves sebelum pruning
    accuracy_before : float
        Accuracy di validation set sebelum pruning
    
    Example:
    --------
    >>> from utils.c45 import C45Tree
    >>> from utils.pruner_rep import ReducedErrorPruner
    >>> 
    >>> # Build full tree
    >>> tree = C45Tree(min_samples=2)
    >>> tree.fit(train_data, 'Status', features)
    >>> 
    >>> # Apply REP pruning
    >>> pruner = ReducedErrorPruner(tree, X_val, y_val, 'Status')
    >>> pruner.prune()
    >>> 
    >>> # Get statistics
    >>> stats = pruner.get_pruning_stats()
    >>> print(f"Nodes pruned: {stats['nodes_pruned']}")
    >>> print(f"Accuracy improved: {stats['accuracy_after'] - stats['accuracy_before']}")
    """
    
    def __init__(self, tree, X_val, y_val, target_column):
        """
        Inisialisasi REP Pruner.
        
        Parameters:
        -----------
        tree : C45Tree
            Decision tree yang akan di-prune
        X_val : DataFrame
            Validation features
        y_val : Series
            Validation labels
        target_column : str
            Nama kolom target
        """
        self.tree = tree
        self.X_val = X_val
        self.y_val = y_val
        self.target_column = target_column
        self.pruning_log = []
        
        # Save baseline metrics
        self.depth_before = tree.get_depth()
        self.leaves_before = tree.get_n_leaves()
        self.accuracy_before = self._calculate_accuracy()
    
    def prune(self):
        """
        Apply Reduced Error Pruning ke decision tree.
        
        Algoritma:
        1. Calculate baseline accuracy di validation set
        2. Collect semua internal nodes dalam bottom-up order
        3. Untuk setiap node:
           - Backup state node
           - Convert node ke leaf (majority class)
           - Calculate accuracy baru
           - Jika accuracy >= baseline: keep as leaf (pruned)
           - Jika accuracy < baseline: revert ke internal node
        4. Update baseline accuracy setelah setiap successful prune
        
        Returns:
        --------
        dict
            Dictionary berisi pruning statistics
        """
        print("\n" + "="*60)
        print("REDUCED ERROR PRUNING (REP)")
        print("="*60)
        
        print(f"\nBaseline Metrics (Before Pruning):")
        print(f"  Depth           : {self.depth_before}")
        print(f"  Leaves          : {self.leaves_before}")
        print(f"  Validation Acc  : {self.accuracy_before:.4f}")
        
        # Collect all internal nodes in bottom-up order
        internal_nodes = self._collect_nodes_bottom_up(self.tree.root)
        
        print(f"\nTotal internal nodes to evaluate: {len(internal_nodes)}")
        print("\nPruning Process:")
        print("-" * 60)
        
        nodes_pruned = 0
        current_accuracy = self.accuracy_before
        
        for idx, node in enumerate(internal_nodes, 1):
            # Skip if already a leaf (might be pruned by previous iteration)
            if node.label is not None:
                continue
            
            # Backup original state
            backup = {
                'left': node.left,
                'right': node.right,
                'attribute': node.attribute,
                'threshold': node.threshold,
                'label': node.label
            }
            
            # Convert to leaf temporarily
            self._convert_to_leaf(node)
            
            # Calculate new accuracy
            new_accuracy = self._calculate_accuracy()
            
            # Decision: prune or revert?
            if new_accuracy >= current_accuracy:
                # Keep as leaf (pruned)
                nodes_pruned += 1
                accuracy_gain = new_accuracy - current_accuracy
                current_accuracy = new_accuracy
                
                log_entry = {
                    'node_index': idx,
                    'attribute': backup['attribute'],
                    'threshold': backup['threshold'],
                    'action': 'PRUNED',
                    'accuracy_before': current_accuracy - accuracy_gain,
                    'accuracy_after': new_accuracy,
                    'accuracy_gain': accuracy_gain
                }
                self.pruning_log.append(log_entry)
                
                print(f"  Node {idx:2d} [{backup['attribute']:30s} <= {backup['threshold']:8.2f}] "
                      f"-> PRUNED  (Acc: {new_accuracy:.4f}, Gain: {accuracy_gain:+.4f})")
            else:
                # Revert to internal node
                self._revert_node(node, backup)
                
                log_entry = {
                    'node_index': idx,
                    'attribute': backup['attribute'],
                    'threshold': backup['threshold'],
                    'action': 'KEPT',
                    'accuracy_before': current_accuracy,
                    'accuracy_after': new_accuracy,
                    'accuracy_loss': current_accuracy - new_accuracy
                }
                self.pruning_log.append(log_entry)
                
                # Optional: uncomment to see kept nodes
                # print(f"  Node {idx:2d} [{backup['attribute']:30s} <= {backup['threshold']:8.2f}] "
                #       f"-> KEPT    (Acc would drop to: {new_accuracy:.4f})")
        
        print("-" * 60)
        print(f"\nPruning Complete!")
        print(f"  Nodes Pruned    : {nodes_pruned}")
        print(f"  Accuracy Before : {self.accuracy_before:.4f}")
        print(f"  Accuracy After  : {current_accuracy:.4f}")
        print(f"  Improvement     : {current_accuracy - self.accuracy_before:+.4f}")
        print(f"  Depth Before    : {self.depth_before}")
        print(f"  Depth After     : {self.tree.get_depth()}")
        print(f"  Leaves Before   : {self.leaves_before}")
        print(f"  Leaves After    : {self.tree.get_n_leaves()}")
        print("="*60 + "\n")
        
        return self.get_pruning_stats()
    
    def _collect_nodes_bottom_up(self, node, nodes_list=None):
        """
        Collect semua internal nodes dalam post-order traversal (bottom-up).
        
        Post-order: left subtree → right subtree → parent node
        Ini memastikan child nodes di-evaluate sebelum parent nodes.
        
        Parameters:
        -----------
        node : C45Node
            Current node being traversed
        nodes_list : list, optional
            List untuk mengumpulkan nodes (digunakan untuk rekursi)
        
        Returns:
        --------
        list
            List of internal nodes dalam bottom-up order
        """
        if nodes_list is None:
            nodes_list = []
        
        if node is None:
            return nodes_list
        
        # Skip if already a leaf
        if node.label is not None:
            return nodes_list
        
        # Traverse left subtree first
        if node.left is not None:
            self._collect_nodes_bottom_up(node.left, nodes_list)
        
        # Then traverse right subtree
        if node.right is not None:
            self._collect_nodes_bottom_up(node.right, nodes_list)
        
        # Finally add parent node (post-order)
        nodes_list.append(node)
        
        return nodes_list
    
    def _convert_to_leaf(self, node):
        """
        Convert internal node menjadi leaf node.
        
        Leaf node akan menggunakan majority class dari class_counts yang
        tersimpan di node. Probability dihitung menggunakan Laplace smoothing
        yang sudah ada di C45Tree.
        
        Parameters:
        -----------
        node : C45Node
            Node yang akan diubah menjadi leaf
        """
        # Find majority class dari class_counts
        if node.class_counts:
            majority_class = max(node.class_counts, key=node.class_counts.get)
        else:
            # Fallback jika class_counts kosong
            majority_class = "Normal"
        
        # Set as leaf
        node.label = majority_class
        node.left = None
        node.right = None
        node.attribute = None
        node.threshold = None
        
        # Update probability dengan Laplace smoothing
        node.probability = self.tree._calculate_probability_laplace(
            node.class_counts,
            majority_class,
            node.samples
        )
    
    def _revert_node(self, node, backup):
        """
        Revert node kembali ke internal node state.
        
        Parameters:
        -----------
        node : C45Node
            Node yang akan di-revert
        backup : dict
            Backup state dari node sebelum diubah
        """
        node.left = backup['left']
        node.right = backup['right']
        node.attribute = backup['attribute']
        node.threshold = backup['threshold']
        node.label = backup['label']
    
    def _calculate_accuracy(self):
        """
        Calculate accuracy di validation set.
        
        Returns:
        --------
        float
            Accuracy score (0.0 to 1.0)
        """
        y_pred = self.tree.predict(self.X_val)
        return accuracy_score(self.y_val, y_pred)
    
    def get_pruning_stats(self):
        """
        Get comprehensive pruning statistics.
        
        Returns:
        --------
        dict
            Dictionary berisi:
            - nodes_pruned: jumlah nodes yang di-prune
            - accuracy_before: accuracy sebelum pruning
            - accuracy_after: accuracy setelah pruning
            - accuracy_improvement: improvement dalam accuracy
            - depth_before: tree depth sebelum pruning
            - depth_after: tree depth setelah pruning
            - depth_reduction: persentase pengurangan depth
            - leaves_before: jumlah leaves sebelum pruning
            - leaves_after: jumlah leaves setelah pruning
            - leaves_reduction: persentase pengurangan leaves
            - pruning_log: list detail setiap pruning action
        """
        depth_after = self.tree.get_depth()
        leaves_after = self.tree.get_n_leaves()
        accuracy_after = self._calculate_accuracy()
        
        nodes_pruned = sum(1 for log in self.pruning_log if log['action'] == 'PRUNED')
        
        # Calculate reduction percentages
        depth_reduction = 0.0
        if self.depth_before > 0:
            depth_reduction = ((self.depth_before - depth_after) / self.depth_before) * 100
        
        leaves_reduction = 0.0
        if self.leaves_before > 0:
            leaves_reduction = ((self.leaves_before - leaves_after) / self.leaves_before) * 100
        
        return {
            'nodes_pruned': nodes_pruned,
            'accuracy_before': float(self.accuracy_before),
            'accuracy_after': float(accuracy_after),
            'accuracy_improvement': float(accuracy_after - self.accuracy_before),
            'depth_before': int(self.depth_before),
            'depth_after': int(depth_after),
            'depth_reduction_percent': float(depth_reduction),
            'leaves_before': int(self.leaves_before),
            'leaves_after': int(leaves_after),
            'leaves_reduction_percent': float(leaves_reduction),
            'pruning_log': self.pruning_log
        }
