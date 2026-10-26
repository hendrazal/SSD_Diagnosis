import math


def calculate_entropy(data, target_column):
    """
    Menghitung nilai entropy dataset.

    Parameter:
    data          : DataFrame pandas
    target_column : nama kolom target/label

    Return:
    nilai entropy
    """

    # jumlah seluruh data
    total_data = len(data)

    # jika data kosong
    if total_data == 0:
        return 0


    entropy = 0


    # menghitung jumlah setiap kelas
    class_counts = data[target_column].value_counts()


    # perhitungan entropy
    for count in class_counts:

        probability = count / total_data

        entropy -= probability * math.log2(probability)


    return entropy
