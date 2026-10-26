from utils.entropy import calculate_entropy


def calculate_information_gain(
        data,
        attribute,
        target_column
):
    """
    Menghitung Information Gain sebuah atribut.

    Parameter:
    data          : DataFrame
    attribute     : nama atribut SMART
    target_column : label

    Return:
    nilai information gain
    """


    # entropy awal dataset

    entropy_total = calculate_entropy(
        data,
        target_column
    )


    # jumlah data keseluruhan

    total_data = len(data)


    # entropy setelah dilakukan split atribut

    weighted_entropy = 0


    # kelompokkan berdasarkan nilai atribut

    values = data[attribute].unique()


    for value in values:


        subset = data[
            data[attribute] == value
        ]


        subset_probability = len(subset) / total_data


        subset_entropy = calculate_entropy(
            subset,
            target_column
        )


        weighted_entropy += (
            subset_probability *
            subset_entropy
        )


    # Information Gain

    information_gain = (
        entropy_total -
        weighted_entropy
    )


    return information_gain