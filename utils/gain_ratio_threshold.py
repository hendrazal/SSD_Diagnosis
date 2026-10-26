import pandas as pd

from utils.entropy import calculate_entropy


def calculate_gain_ratio_threshold(
    data,
    feature,
    target_column,
    threshold
):

    # Membagi data

    left = data[
        data[feature] <= threshold
    ]

    right = data[
        data[feature] > threshold
    ]


    # Jika salah satu kosong

    if len(left) == 0 or len(right) == 0:
        return 0


    total = len(data)


    # ======================
    # Entropy Dataset
    # ======================

    entropy_total = calculate_entropy(
        data,
        target_column
    )


    # ======================
    # Entropy kiri
    # ======================

    entropy_left = calculate_entropy(
        left,
        target_column
    )


    # ======================
    # Entropy kanan
    # ======================

    entropy_right = calculate_entropy(
        right,
        target_column
    )


    # ======================
    # Information Gain
    # ======================

    gain = (

        entropy_total

        -

        (

            (len(left)/total) * entropy_left

            +

            (len(right)/total) * entropy_right

        )

    )


    # ======================
    # Split Info
    # ======================

    import math

    split = 0

    for subset in [left, right]:

        p = len(subset) / total

        if p > 0:
            split -= p * math.log2(p)


    if split == 0:
        return 0


    return gain / split