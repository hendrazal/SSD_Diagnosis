import numpy as np
import pandas as pd

from utils.gain_ratio_threshold import calculate_gain_ratio_threshold


class C45Node:
    def __init__(
        self,
        attribute=None,
        threshold=None,
        label=None,
        samples=0,
        probability=1.0,
        class_counts=None
    ):
        self.attribute = attribute
        self.threshold = threshold
        self.label = label
        self.samples = samples
        self.probability = probability

        self.class_counts = (
            class_counts
            if class_counts is not None
            else {}
        )

        self.left = None
        self.right = None


class C45Tree:
    """
    Implementasi algoritma C4.5 untuk data numerik
    dengan opsi pre-pruning.

    Parameter:
    - max_depth:
        Membatasi kedalaman maksimum pohon.
        None = tidak dibatasi.

    - min_samples_split:
        Jumlah minimum data pada node agar
        node dapat dilakukan splitting.

    - min_samples_leaf:
        Jumlah minimum data yang harus ada di leaf node.
        Split akan dibatalkan jika menghasilkan leaf < min_samples_leaf.

    - max_leaf_nodes:
        Maksimum jumlah leaf nodes.
        None = tidak dibatasi.

    - min_impurity_decrease:
        Minimum penurunan gain ratio untuk melakukan split.
        Split hanya dilakukan jika gain_ratio >= min_impurity_decrease.
    """

    def __init__(
        self,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        max_leaf_nodes=None,
        min_impurity_decrease=0.0
    ):
        self.root = None
        self.target_column = None
        self.features = None
        self.classes_ = []

        # Parameter pruning
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        
        # Track jumlah leaf untuk max_leaf_nodes
        self.current_leaf_count = 0

    # ========================================================
    # FIT
    # ========================================================

    def fit(
        self,
        data,
        target_column,
        features
    ):
        self.target_column = target_column
        self.features = features

        self.classes_ = sorted(
            data[target_column]
            .unique()
            .tolist()
        )

        # Reset leaf count untuk max_leaf_nodes
        self.current_leaf_count = 0

        self.root = self._build_tree(
            data,
            list(features),
            depth=0
        )

        return self

    # ========================================================
    # PROBABILITY DENGAN LAPLACE SMOOTHING
    # ========================================================

    def _calculate_probability_laplace(
        self,
        class_counts,
        total_samples
    ):
        alpha = 1

        jumlah_kelas = len(
            self.classes_
        )

        probabilities = {}

        for cls in self.classes_:

            count = class_counts.get(
                cls,
                0
            )

            probability = (
                count + alpha
            ) / (
                total_samples
                + alpha * jumlah_kelas
            )

            probabilities[cls] = probability

        return probabilities

    # ========================================================
    # MENCARI THRESHOLD TERBAIK
    # ========================================================

    def _find_best_threshold(
        self,
        data,
        attribute
    ):
        values = (
            data[attribute]
            .dropna()
            .unique()
        )

        if len(values) <= 1:
            return None, -np.inf

        values = np.sort(values)

        thresholds = []

        for i in range(len(values) - 1):

            threshold = (
                values[i] + values[i + 1]
            ) / 2

            thresholds.append(
                threshold
            )

        best_threshold = None
        best_gain_ratio = -np.inf

        for threshold in thresholds:

            gain_ratio = calculate_gain_ratio_threshold(
                data,
                attribute,
                self.target_column,
                threshold
            )

            if gain_ratio > best_gain_ratio:

                best_gain_ratio = gain_ratio
                best_threshold = threshold

        return (
            best_threshold,
            best_gain_ratio
        )

    # ========================================================
    # MEMBANGUN TREE
    # ========================================================

    def _build_tree(
        self,
        data,
        features,
        depth
    ):

        # ----------------------------------------------------
        # JUMLAH DATA
        # ----------------------------------------------------

        jumlah_data = len(data)

        # ----------------------------------------------------
        # CLASS COUNTS
        # ----------------------------------------------------

        class_counts = (
            data[self.target_column]
            .value_counts()
            .to_dict()
        )

        # ----------------------------------------------------
        # KELAS MAYORITAS
        # ----------------------------------------------------

        majority_class = (
            data[self.target_column]
            .mode()
            .iloc[0]
        )

        # ----------------------------------------------------
        # PROBABILITY
        # ----------------------------------------------------

        probabilities = (
            self._calculate_probability_laplace(
                class_counts,
                jumlah_data
            )
        )

        majority_probability = probabilities[
            majority_class
        ]

        # ----------------------------------------------------
        # KONDISI 1:
        # DATA SUDAH MURNI
        # ----------------------------------------------------

        if data[self.target_column].nunique() == 1:

            self.current_leaf_count += 1

            return C45Node(
                label=majority_class,
                samples=jumlah_data,
                probability=majority_probability,
                class_counts=class_counts
            )

        # ----------------------------------------------------
        # KONDISI 2:
        # MINIMUM SAMPLE SPLIT
        # ----------------------------------------------------

        if jumlah_data < self.min_samples_split:

            self.current_leaf_count += 1

            return C45Node(
                label=majority_class,
                samples=jumlah_data,
                probability=majority_probability,
                class_counts=class_counts
            )

        # ----------------------------------------------------
        # KONDISI 3:
        # MAX DEPTH
        # ----------------------------------------------------

        if (
            self.max_depth is not None
            and depth >= self.max_depth
        ):

            self.current_leaf_count += 1

            return C45Node(
                label=majority_class,
                samples=jumlah_data,
                probability=majority_probability,
                class_counts=class_counts
            )

        # ----------------------------------------------------
        # KONDISI 4:
        # MAX LEAF NODES
        # ----------------------------------------------------

        if (
            self.max_leaf_nodes is not None
            and self.current_leaf_count >= self.max_leaf_nodes
        ):

            self.current_leaf_count += 1

            return C45Node(
                label=majority_class,
                samples=jumlah_data,
                probability=majority_probability,
                class_counts=class_counts
            )

        # ----------------------------------------------------
        # KONDISI 5:
        # TIDAK ADA FITUR
        # ----------------------------------------------------

        if len(features) == 0:

            self.current_leaf_count += 1

            return C45Node(
                label=majority_class,
                samples=jumlah_data,
                probability=majority_probability,
                class_counts=class_counts
            )

        # ----------------------------------------------------
        # MENCARI ATTRIBUTE DAN THRESHOLD TERBAIK
        # ----------------------------------------------------

        best_attribute = None
        best_threshold = None
        best_gain_ratio = -np.inf

        for attribute in features:

            threshold, gain_ratio = (
                self._find_best_threshold(
                    data,
                    attribute
                )
            )

            if threshold is None:
                continue

            if gain_ratio > best_gain_ratio:

                best_gain_ratio = gain_ratio
                best_attribute = attribute
                best_threshold = threshold

        # ----------------------------------------------------
        # TIDAK ADA SPLIT VALID ATAU MIN_IMPURITY_DECREASE
        # ----------------------------------------------------

        if (
            best_attribute is None
            or best_gain_ratio <= 0
            or best_gain_ratio < self.min_impurity_decrease
        ):

            self.current_leaf_count += 1

            return C45Node(
                label=majority_class,
                samples=jumlah_data,
                probability=majority_probability,
                class_counts=class_counts
            )

        # ----------------------------------------------------
        # SPLIT DATA
        # ----------------------------------------------------

        left_data = data[
            data[best_attribute]
            <= best_threshold
        ]

        right_data = data[
            data[best_attribute]
            > best_threshold
        ]

        # ----------------------------------------------------
        # JIKA SALAH SATU CABANG KOSONG ATAU MIN_SAMPLES_LEAF
        # ----------------------------------------------------

        if (
            len(left_data) == 0
            or len(right_data) == 0
            or len(left_data) < self.min_samples_leaf
            or len(right_data) < self.min_samples_leaf
        ):

            self.current_leaf_count += 1

            return C45Node(
                label=majority_class,
                samples=jumlah_data,
                probability=majority_probability,
                class_counts=class_counts
            )

        # ----------------------------------------------------
        # NODE INTERNAL
        # ----------------------------------------------------

        node = C45Node(
            attribute=best_attribute,
            threshold=best_threshold,
            samples=jumlah_data,
            probability=majority_probability,
            class_counts=class_counts
        )

        # ----------------------------------------------------
        # RECURSIVE TREE
        # ----------------------------------------------------

        node.left = self._build_tree(
            left_data,
            features,
            depth + 1
        )

        node.right = self._build_tree(
            right_data,
            features,
            depth + 1
        )

        return node

    # ========================================================
    # PREDICT SATU DATA
    # ========================================================

    def predict_row(self, row):

        node = self.root

        while node is not None:

            # -----------------------------------------------
            # NODE LEAF
            # -----------------------------------------------

            if node.attribute is None:

                return node.label

            # -----------------------------------------------
            # LEFT
            # -----------------------------------------------

            if (
                row[node.attribute]
                <= node.threshold
            ):

                node = node.left

            # -----------------------------------------------
            # RIGHT
            # -----------------------------------------------

            else:

                node = node.right

        return None

    # ========================================================
    # PREDICT
    # ========================================================

    def predict(self, X):

        predictions = []

        for _, row in X.iterrows():

            predictions.append(
                self.predict_row(row)
            )

        return np.array(
            predictions
        )

    # ========================================================
    # PREDICT PROBA
    # ========================================================

    def predict_proba(self, X):

        hasil = []

        for _, row in X.iterrows():

            node = self.root

            while node is not None:

                if node.attribute is None:
                    break

                if (
                    row[node.attribute]
                    <= node.threshold
                ):
                    node = node.left
                else:
                    node = node.right

            # Gunakan Laplace smoothing untuk probability
            alpha = 1
            jumlah_kelas = len(self.classes_)
            total_samples = node.samples
            
            probabilities = []

            for cls in self.classes_:
                count = node.class_counts.get(cls, 0)
                # Laplace smoothing: (count + alpha) / (total + alpha * num_classes)
                prob = (count + alpha) / (total_samples + alpha * jumlah_kelas)
                probabilities.append(prob)

            hasil.append(
                probabilities
            )

        return np.array(
            hasil
        )

    # ========================================================
    # TREE DEPTH
    # ========================================================

    def get_depth(self):

        if self.root is None:
            return 0

        return self._get_depth(
            self.root
        )

    def _get_depth(self, node):

        if node is None:
            return 0

        if (
            node.left is None
            and node.right is None
        ):
            return 1

        return 1 + max(
            self._get_depth(node.left),
            self._get_depth(node.right)
        )

    # ========================================================
    # JUMLAH LEAF
    # ========================================================

    def get_n_leaves(self):

        if self.root is None:
            return 0

        return self._get_n_leaves(
            self.root
        )

    def _get_n_leaves(self, node):

        if node is None:
            return 0

        if (
            node.left is None
            and node.right is None
        ):
            return 1

        return (
            self._get_n_leaves(node.left)
            +
            self._get_n_leaves(node.right)
        )

    # ========================================================
    # DECISION PATH
    # ========================================================

    def get_decision_path(self, row):

        path = []
        node_objects = []  # Track actual node objects untuk highlight

        node = self.root

        while node is not None:

            # -----------------------------------------------
            # LEAF
            # -----------------------------------------------

            if node.attribute is None:

                path.append({
                    "type": "leaf",
                    "label": node.label,
                    "samples": node.samples
                })
                
                node_objects.append(node)

                break

            # -----------------------------------------------
            # KONDISI SPLIT
            # -----------------------------------------------

            value = row[
                node.attribute
            ]
            
            # Track node object
            node_objects.append(node)

            if value <= node.threshold:

                path.append({
                    "type": "split",
                    "attribute": node.attribute,
                    "value": value,
                    "operator": "<=",
                    "threshold": node.threshold,
                    "direction": "left"
                })

                node = node.left

            else:

                path.append({
                    "type": "split",
                    "attribute": node.attribute,
                    "value": value,
                    "operator": ">",
                    "threshold": node.threshold,
                    "direction": "right"
                })

                node = node.right

        return node_objects