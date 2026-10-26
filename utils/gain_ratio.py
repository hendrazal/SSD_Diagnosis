from utils.information_gain import calculate_information_gain
from utils.split_info import calculate_split_info


def calculate_gain_ratio(
        data,
        attribute,
        target_column
):
    """
    Menghitung Gain Ratio algoritma C4.5

    Parameter:
    data          : DataFrame
    attribute     : atribut SMART
    target_column : label

    Return:
    nilai gain ratio
    """


    gain = calculate_information_gain(
        data,
        attribute,
        target_column
    )


    split_info = calculate_split_info(
        data,
        attribute
    )


    # mencegah pembagian dengan nol

    if split_info == 0:
        return 0


    gain_ratio = gain / split_info


    return gain_ratio