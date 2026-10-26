import os
import pandas as pd

from config import DATASET_PATH


def load_dataset():
    """
    Membaca dataset SSD dari file CSV.
    """

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset tidak ditemukan:\n{DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH, sep=";")

    # Menghapus kolom kosong (Unnamed)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Menghapus spasi di awal dan akhir nama kolom
    df.columns = df.columns.str.strip()

    return df