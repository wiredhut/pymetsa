import pickle
from copy import deepcopy
from pathlib import Path
import geopandas as gpd
import numpy as np
import pandas as pd

from pymetsa.paths import get_arbonaut_vector_path, get_data_folder_path


FEATURES_NAMES = ['0_1_0_mean', '0_1_0_std', '0_1_0_min', '0_1_0_max',
                  '1_1_0_mean', '1_1_0_std', '1_1_0_min', '1_1_0_max',
                  '2_1_0_mean', '2_1_0_std', '2_1_0_min', '2_1_0_max',
                  '3_1_0_mean', '3_1_0_std', '3_1_0_min', '3_1_0_max',
                  '4_1_0_mean', '4_1_0_std', '4_1_0_min', '4_1_0_max',
                  '5_1_0_mean', '5_1_0_std', '5_1_0_min', '5_1_0_max',
                  '6_1_0_mean', '6_1_0_std', '6_1_0_min', '6_1_0_max',
                  '7_1_0_mean', '7_1_0_std', '7_1_0_min', '7_1_0_max',
                  '8_1_0_mean', '8_1_0_std', '8_1_0_min', '8_1_0_max',
                  '9_1_0_mean', '9_1_0_std', '9_1_0_min', '9_1_0_max',
                  '10_1_0_mean', '10_1_0_std', '10_1_0_min', '10_1_0_max',
                  '11_1_0_mean', '11_1_0_std', '11_1_0_min', '11_1_0_max',
                  '12_1_0_mean', '12_1_0_std', '12_1_0_min', '12_1_0_max',
                  '13_1_0_mean', '13_1_0_std', '13_1_0_min', '13_1_0_max',
                  '13_2_0_mean', '13_2_0_std', '13_2_0_min', '13_2_0_max',
                  '13_3_0_mean', '13_3_0_std', '13_3_0_min', '13_3_0_max',
                  '13_4_0_mean', '13_4_0_std', '13_4_0_min', '13_4_0_max',
                  '13_5_0_mean', '13_5_0_std', '13_5_0_min', '13_5_0_max',
                  '13_6_0_mean', '13_6_0_std', '13_6_0_min', '13_6_0_max',
                  '13_7_0_mean', '13_7_0_std', '13_7_0_min', '13_7_0_max',
                  '13_8_0_mean', '13_8_0_std', '13_8_0_min', '13_8_0_max',
                  '13_9_0_mean', '13_9_0_std', '13_9_0_min', '13_9_0_max',
                  '13_10_0_mean', '13_10_0_std', '13_10_0_min', '13_10_0_max',
                  '14_1_0_mean', '14_1_0_std', '14_1_0_min', '14_1_0_max',
                  '15_1_0_mean', '15_1_0_std', '15_1_0_min', '15_1_0_max',
                  '16_1_0_mean', '16_1_0_std', '16_1_0_min', '16_1_0_max',
                  '17_1_0_mean', '17_1_0_std', '17_1_0_min', '17_1_0_max',
                  '18_1_0_mean', '18_1_0_std', '18_1_0_min', '18_1_0_max',
                  '19_1_0_mean', '19_1_0_std', '19_1_0_min', '19_1_0_max',
                  '20_1_0_mean', '20_1_0_std', '20_1_0_min', '20_1_0_max',
                  '21_1_0_mean', '21_1_0_std', '21_1_0_min', '21_1_0_max',
                  '22_1_0_mean', '22_1_0_std', '22_1_0_min', '22_1_0_max',
                  '23_1_0_mean', '23_1_0_std', '23_1_0_min', '23_1_0_max',
                  '24_1_0_mean', '24_1_0_std', '24_1_0_min', '24_1_0_max',
                  '25_1_0_mean', '25_1_0_std', '25_1_0_min', '25_1_0_max',
                  '26_1_0_mean', '26_1_0_std', '26_1_0_min', '26_1_0_max',
                  '27_1_0_mean', '27_1_0_std', '27_1_0_min', '27_1_0_max']

OLD_CLASS = 1
YOUNG_CLASS = 2


def apply_model(path_to_shp_file: Path, path_to_features_file: Path, path_to_result_file: Path):
    """ Make final prediction """
    class_threshold = 85

    with open('old_model.pkl', 'rb') as pkl:
        reg_model = pickle.load(pkl)
        max_depth = reg_model.max_depth
        min_samples_split = reg_model.min_samples_split
        max_leaf_nodes = reg_model.max_leaf_nodes

        print(f'max_depth: {max_depth}. min_samples_split: {min_samples_split}. max_leaf_nodes: {max_leaf_nodes}')

    features = pd.read_csv(path_to_features_file)
    features = np.array(features[FEATURES_NAMES])

    predicted_age = reg_model.predict(features)
    predicted_class = deepcopy(predicted_age)

    predicted_class[predicted_class < class_threshold] = YOUNG_CLASS
    predicted_class[predicted_class >= class_threshold] = OLD_CLASS

    df = gpd.read_file(path_to_shp_file)
    df['p_age'] = predicted_age
    df['p_class'] = predicted_class

    df.to_file(path_to_result_file)


if __name__ == "__main__":
    apply_model(path_to_shp_file=Path(get_arbonaut_vector_path(), 'Grid_lidar_variables..shp'),
                path_to_features_file=Path(get_data_folder_path(), 'PREDICTION_extraction.csv'),
                path_to_result_file=Path(get_data_folder_path(), 'final_prediction.shp'))
