from pathlib import Path

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

from pymetsa.paths import get_data_folder_path

COLUMN_NAMES = ['id', 'gridcellid', 'age', 'basalarea', 'volume', 'sampleplot', 'Class',
                '0_1_0_mean', '0_1_0_std', '0_1_0_min', '0_1_0_max',
                '0_1_1_mean', '0_1_1_std', '0_1_1_min', '0_1_1_max',
                '0_1_2_mean', '0_1_2_std', '0_1_2_min', '0_1_2_max',
                '1_1_0_mean', '1_1_0_std', '1_1_0_min', '1_1_0_max',
                '1_1_1_mean', '1_1_1_std', '1_1_1_min', '1_1_1_max',
                '1_1_2_mean', '1_1_2_std', '1_1_2_min', '1_1_2_max',
                '2_1_0_mean', '2_1_0_std', '2_1_0_min', '2_1_0_max',
                '2_1_1_mean', '2_1_1_std', '2_1_1_min', '2_1_1_max',
                '2_1_2_mean', '2_1_2_std', '2_1_2_min', '2_1_2_max',
                '3_1_0_mean', '3_1_0_std', '3_1_0_min', '3_1_0_max',
                '3_1_1_mean', '3_1_1_std', '3_1_1_min', '3_1_1_max',
                '3_1_2_mean', '3_1_2_std', '3_1_2_min', '3_1_2_max',
                '4_1_0_mean', '4_1_0_std', '4_1_0_min', '4_1_0_max',
                '4_1_1_mean', '4_1_1_std', '4_1_1_min', '4_1_1_max',
                '4_1_2_mean', '4_1_2_std', '4_1_2_min', '4_1_2_max',
                '5_1_0_mean', '5_1_0_std', '5_1_0_min', '5_1_0_max',
                '5_1_1_mean', '5_1_1_std', '5_1_1_min', '5_1_1_max',
                '5_1_2_mean', '5_1_2_std', '5_1_2_min', '5_1_2_max',
                '6_1_0_mean', '6_1_0_std', '6_1_0_min', '6_1_0_max',
                '6_1_1_mean', '6_1_1_std', '6_1_1_min', '6_1_1_max',
                '6_1_2_mean', '6_1_2_std', '6_1_2_min', '6_1_2_max',
                '7_1_0_mean', '7_1_0_std', '7_1_0_min', '7_1_0_max',
                '7_1_1_mean', '7_1_1_std', '7_1_1_min', '7_1_1_max',
                '7_1_2_mean', '7_1_2_std', '7_1_2_min', '7_1_2_max',
                '8_1_0_mean', '8_1_0_std', '8_1_0_min', '8_1_0_max',
                '8_1_1_mean', '8_1_1_std', '8_1_1_min', '8_1_1_max',
                '8_1_2_mean', '8_1_2_std', '8_1_2_min', '8_1_2_max',
                '9_1_0_mean', '9_1_0_std', '9_1_0_min', '9_1_0_max',
                '9_1_1_mean', '9_1_1_std', '9_1_1_min', '9_1_1_max',
                '9_1_2_mean', '9_1_2_std', '9_1_2_min', '9_1_2_max',
                '10_1_0_mea', '10_1_0_std', '10_1_0_min', '10_1_0_max',
                '10_1_1_mea', '10_1_1_std', '10_1_1_min', '10_1_1_max',
                '10_1_2_mea', '10_1_2_std', '10_1_2_min', '10_1_2_max',
                '11_1_0_mea', '11_1_0_std', '11_1_0_min', '11_1_0_max',
                '11_1_1_mea', '11_1_1_std', '11_1_1_min', '11_1_1_max',
                '11_1_2_mea', '11_1_2_std', '11_1_2_min', '11_1_2_max',
                '12_1_0_mea', '12_1_0_std', '12_1_0_min', '12_1_0_max',
                '12_1_1_mea', '12_1_1_std', '12_1_1_min', '12_1_1_max',
                '12_1_2_mea', '12_1_2_std', '12_1_2_min', '12_1_2_max',
                '13_1_0_mea', '13_1_0_std', '13_1_0_min', '13_1_0_max',
                '13_1_1_mea', '13_1_1_std', '13_1_1_min', '13_1_1_max',
                '13_1_2_mea', '13_1_2_std', '13_1_2_min', '13_1_2_max',
                '13_2_0_mea', '13_2_0_std', '13_2_0_min', '13_2_0_max',
                '13_2_1_mea', '13_2_1_std', '13_2_1_min', '13_2_1_max',
                '13_2_2_mea', '13_2_2_std', '13_2_2_min', '13_2_2_max',
                '13_3_0_mea', '13_3_0_std', '13_3_0_min', '13_3_0_max',
                '13_3_1_mea', '13_3_1_std', '13_3_1_min', '13_3_1_max',
                '13_3_2_mea', '13_3_2_std', '13_3_2_min', '13_3_2_max',
                '13_4_0_mea', '13_4_0_std', '13_4_0_min', '13_4_0_max',
                '13_4_1_mea', '13_4_1_std', '13_4_1_min', '13_4_1_max',
                '13_4_2_mea', '13_4_2_std', '13_4_2_min', '13_4_2_max',
                '13_5_0_mea', '13_5_0_std', '13_5_0_min', '13_5_0_max',
                '13_5_1_mea', '13_5_1_std', '13_5_1_min', '13_5_1_max',
                '13_5_2_mea', '13_5_2_std', '13_5_2_min', '13_5_2_max',
                '13_6_0_mea', '13_6_0_std', '13_6_0_min', '13_6_0_max',
                '13_6_1_mea', '13_6_1_std', '13_6_1_min', '13_6_1_max',
                '13_6_2_mea', '13_6_2_std', '13_6_2_min', '13_6_2_max',
                '13_7_0_mea', '13_7_0_std', '13_7_0_min', '13_7_0_max',
                '13_7_1_mea', '13_7_1_std', '13_7_1_min', '13_7_1_max',
                '13_7_2_mea', '13_7_2_std', '13_7_2_min', '13_7_2_max',
                '13_8_0_mea', '13_8_0_std', '13_8_0_min', '13_8_0_max',
                '13_8_1_mea', '13_8_1_std', '13_8_1_min', '13_8_1_max',
                '13_8_2_mea', '13_8_2_std', '13_8_2_min', '13_8_2_max',
                '13_9_0_mea', '13_9_0_std', '13_9_0_min', '13_9_0_max',
                '13_9_1_mea', '13_9_1_std', '13_9_1_min', '13_9_1_max',
                '13_9_2_mea', '13_9_2_std', '13_9_2_min', '13_9_2_max',
                '13_10_0_me', '13_10_0_st', '13_10_0_mi', '13_10_0_ma',
                '13_10_1_me', '13_10_1_st', '13_10_1_mi', '13_10_1_ma',
                '13_10_2_me', '13_10_2_st', '13_10_2_mi', '13_10_2_ma',
                '14_1_0_mea', '14_1_0_std', '14_1_0_min', '14_1_0_max',
                '14_1_1_mea', '14_1_1_std', '14_1_1_min', '14_1_1_max',
                '14_1_2_mea', '14_1_2_std', '14_1_2_min', '14_1_2_max',
                '15_1_0_mea', '15_1_0_std', '15_1_0_min', '15_1_0_max',
                '15_1_1_mea', '15_1_1_std', '15_1_1_min', '15_1_1_max',
                '15_1_2_mea', '15_1_2_std', '15_1_2_min', '15_1_2_max',
                '16_1_0_mea', '16_1_0_std', '16_1_0_min', '16_1_0_max',
                '16_1_1_mea', '16_1_1_std', '16_1_1_min', '16_1_1_max',
                '16_1_2_mea', '16_1_2_std', '16_1_2_min', '16_1_2_max',
                '17_1_0_mea', '17_1_0_std', '17_1_0_min', '17_1_0_max',
                '17_1_1_mea', '17_1_1_std', '17_1_1_min', '17_1_1_max',
                '17_1_2_mea', '17_1_2_std', '17_1_2_min', '17_1_2_max',
                '18_1_0_mea', '18_1_0_std', '18_1_0_min', '18_1_0_max',
                '18_1_1_mea', '18_1_1_std', '18_1_1_min', '18_1_1_max',
                '18_1_2_mea', '18_1_2_std', '18_1_2_min', '18_1_2_max',
                '19_1_0_mea', '19_1_0_std', '19_1_0_min', '19_1_0_max',
                '19_1_1_mea', '19_1_1_std', '19_1_1_min', '19_1_1_max',
                '19_1_2_mea', '19_1_2_std', '19_1_2_min', '19_1_2_max',
                '20_1_0_mea', '20_1_0_std', '20_1_0_min', '20_1_0_max',
                '20_1_1_mea', '20_1_1_std', '20_1_1_min', '20_1_1_max',
                '20_1_2_mea', '20_1_2_std', '20_1_2_min', '20_1_2_max',
                '21_1_0_mea', '21_1_0_std', '21_1_0_min', '21_1_0_max',
                '21_1_1_mea', '21_1_1_std', '21_1_1_min', '21_1_1_max',
                '21_1_2_mea', '21_1_2_std', '21_1_2_min', '21_1_2_max',
                '22_1_0_mea', '22_1_0_std', '22_1_0_min', '22_1_0_max',
                '22_1_1_mea', '22_1_1_std', '22_1_1_min', '22_1_1_max',
                '22_1_2_mea', '22_1_2_std', '22_1_2_min', '22_1_2_max',
                '23_1_0_mea', '23_1_0_std', '23_1_0_min', '23_1_0_max',
                '23_1_1_mea', '23_1_1_std', '23_1_1_min', '23_1_1_max',
                '23_1_2_mea', '23_1_2_std', '23_1_2_min', '23_1_2_max',
                '24_1_0_mea', '24_1_0_std', '24_1_0_min', '24_1_0_max',
                '24_1_1_mea', '24_1_1_std', '24_1_1_min', '24_1_1_max',
                '24_1_2_mea', '24_1_2_std', '24_1_2_min', '24_1_2_max',
                '25_1_0_mea', '25_1_0_std', '25_1_0_min', '25_1_0_max',
                '25_1_1_mea', '25_1_1_std', '25_1_1_min', '25_1_1_max',
                '25_1_2_mea', '25_1_2_std', '25_1_2_min', '25_1_2_max',
                '26_1_0_mea', '26_1_0_std', '26_1_0_min', '26_1_0_max',
                '26_1_1_mea', '26_1_1_std', '26_1_1_min', '26_1_1_max',
                '26_1_2_mea', '26_1_2_std', '26_1_2_min', '26_1_2_max',
                '27_1_0_mea', '27_1_0_std', '27_1_0_min', '27_1_0_max',
                '27_1_1_mea', '27_1_1_std', '27_1_1_min', '27_1_1_max',
                '27_1_2_mea', '27_1_2_std', '27_1_2_min', '27_1_2_max',
                'geometry']


SEVERAL_COLUMN_NAMES = ['id', 'gridcellid', 'age', 'basalarea', 'volume',
                        'sampleplot', 'Class',
                        '0_1_0_mean', '0_1_0_std', '0_1_0_min', '0_1_0_max',
                        '1_1_0_mean', '1_1_0_std', '1_1_0_min', '1_1_0_max',
                        '2_1_0_mean', '2_1_0_std', '2_1_0_min', '2_1_0_max',
                        '3_1_0_mean', '3_1_0_std', '3_1_0_min', '3_1_0_max',
                        '4_1_0_mean', '4_1_0_std', '4_1_0_min', '4_1_0_max',
                        '5_1_0_mean', '5_1_0_std', '5_1_0_min', '5_1_0_max',
                        '6_1_0_mean', '6_1_0_std', '6_1_0_min', '6_1_0_max',
                        '7_1_0_mean', '7_1_0_std', '7_1_0_min', '7_1_0_max',
                        '8_1_0_mean', '8_1_0_std', '8_1_0_min', '8_1_0_max',
                        '9_1_0_mean', '9_1_0_std', '9_1_0_min', '9_1_0_max',
                        '10_1_0_mea', '10_1_0_std', '10_1_0_min', '10_1_0_max',
                        '11_1_0_mea', '11_1_0_std', '11_1_0_min', '11_1_0_max',
                        '12_1_0_mea', '12_1_0_std', '12_1_0_min', '12_1_0_max',
                        '13_1_0_mea', '13_1_0_std', '13_1_0_min', '13_1_0_max',
                        '13_2_0_mea', '13_2_0_std', '13_2_0_min', '13_2_0_max',
                        '13_3_0_mea', '13_3_0_std', '13_3_0_min', '13_3_0_max',
                        '13_4_0_mea', '13_4_0_std', '13_4_0_min', '13_4_0_max',
                        '13_5_0_mea', '13_5_0_std', '13_5_0_min', '13_5_0_max',
                        '13_6_0_mea', '13_6_0_std', '13_6_0_min', '13_6_0_max',
                        '13_7_0_mea', '13_7_0_std', '13_7_0_min', '13_7_0_max',
                        '13_8_0_mea', '13_8_0_std', '13_8_0_min', '13_8_0_max',
                        '13_9_0_mea', '13_9_0_std', '13_9_0_min', '13_9_0_max',
                        '13_10_0_me', '13_10_0_st', '13_10_0_mi', '13_10_0_ma',
                        '14_1_0_mea', '14_1_0_std', '14_1_0_min', '14_1_0_max',
                        '15_1_0_mea', '15_1_0_std', '15_1_0_min', '15_1_0_max',
                        '16_1_0_mea', '16_1_0_std', '16_1_0_min', '16_1_0_max',
                        '17_1_0_mea', '17_1_0_std', '17_1_0_min', '17_1_0_max',
                        '18_1_0_mea', '18_1_0_std', '18_1_0_min', '18_1_0_max',
                        '19_1_0_mea', '19_1_0_std', '19_1_0_min', '19_1_0_max',
                        '20_1_0_mea', '20_1_0_std', '20_1_0_min', '20_1_0_max',
                        '21_1_0_mea', '21_1_0_std', '21_1_0_min', '21_1_0_max',
                        '22_1_0_mea', '22_1_0_std', '22_1_0_min', '22_1_0_max',
                        '23_1_0_mea', '23_1_0_std', '23_1_0_min', '23_1_0_max',
                        '24_1_0_mea', '24_1_0_std', '24_1_0_min', '24_1_0_max',
                        '25_1_0_mea', '25_1_0_std', '25_1_0_min', '25_1_0_max',
                        '26_1_0_mea', '26_1_0_std', '26_1_0_min', '26_1_0_max',
                        '27_1_0_mea', '27_1_0_std', '27_1_0_min', '27_1_0_max',
                        'geometry']


def clip_by_columns():
    """ Algorithm clip the initial files columns """
    file_with_results = Path(get_data_folder_path(), 'extracted', 'extraction_result.shp')
    vector_layer = gpd.read_file(file_with_results)

    vector_layer = vector_layer[SEVERAL_COLUMN_NAMES]
    vector_layer.to_file(Path(get_data_folder_path(), 'extracted', 'extraction_result_clipped.shp'))

    print(f'Columns: {list(vector_layer.columns)}. Len: {len(vector_layer)}')


def visualize_features_and_target_dependencies():
    """ Algorithm allows to show matrices """
    file_with_results = Path(get_data_folder_path(), 'extracted', 'extraction_result_clipped.shp')
    vector_layer = gpd.read_file(file_with_results)

    print(f'Columns: {list(vector_layer.columns)}. Len: {len(vector_layer)}')

    sns.catplot(data=vector_layer, x="Class", y="age")
    plt.show()


if __name__ == "__main__":
    visualize_features_and_target_dependencies()
