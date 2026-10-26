import math


def calculate_split_info(data, attribute):
    """
    Menghitung Split Information pada algoritma C4.5

    Parameter:
    data      : DataFrame
    attribute : atribut SMART

    Return:
    nilai Split Information
    """


    total_data = len(data)

    split_info = 0


    # jumlah setiap nilai atribut

    value_counts = data[attribute].value_counts()


    for count in value_counts:

        probability = count / total_data


        if probability > 0:

            split_info -= (
                probability *
                math.log2(probability)
            )


    return split_info