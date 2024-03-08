import pickle
from copy import deepcopy
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

import numpy as np
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt

from pymetsa.paths import get_data_folder_path

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
                  '27_1_0_mea', '27_1_0_std', '27_1_0_min', '27_1_0_max']

OLD_CLASS = 1
YOUNG_CLASS = 2


def fit_regression_model(class_threshold: int = 85):
    """ Algorithm allows to show matrices """
    file_with_results = Path(get_data_folder_path(), 'extracted',
                             'extraction_result_clipped.shp')
    vector_layer = gpd.read_file(file_with_results)
    vector_layer = vector_layer.replace(np.nan, 0)

    # Prepare samples
    features = np.array(vector_layer[FEATURES_NAMES])
    target = np.array(vector_layer['age'])
    target_class = np.array(vector_layer['Class'])
    x_train, x_test, y_train, y_test = train_test_split(features, target,
                                                        test_size=0.25, shuffle=True,
                                                        random_state=2000)
    _, _, y_class_train, y_class_test = train_test_split(features, target_class,
                                                         test_size=0.25,
                                                         shuffle=True,
                                                         random_state=2000)

    ###################
    # BALANCE SAMPLES #
    ###################
    names = deepcopy(FEATURES_NAMES)
    names.extend(['age', 'Class'])
    df = pd.DataFrame(np.hstack([x_train, y_train.reshape((-1, 1)), y_class_train.reshape((-1, 1))]),
                      columns=names)
    # Take minor class
    for i in [1, 2, 3]:
        df_minor = df[df['Class'] == OLD_CLASS]
        # Add some noise
        features_noise = np.random.normal(0, 0.025, size=(len(df_minor), len(FEATURES_NAMES)))
        print(f'{i}. Features min noise: {np.min(features_noise)}, Features max noise: {np.max(features_noise)}')

        target_noise = np.random.normal(0, 0.35, size=(len(df_minor), 1))
        print(f'{i}. Target min noise: {np.min(target_noise)}, Target max noise: {np.max(target_noise)}')
        df_minor[FEATURES_NAMES] = df_minor[FEATURES_NAMES] + (df_minor[FEATURES_NAMES] * features_noise)
        df_minor['age'] = df_minor[['age']] + target_noise

        df = pd.concat([df, df_minor])

    df = df.dropna()
    x_train = np.array(df[FEATURES_NAMES])
    y_train = np.array(df['age'])
    y_class_train = np.array(df['Class'])
    ###################
    # BALANCE SAMPLES #
    ###################

    print(f'Train sample size: {len(x_train)}. test sample size: {len(x_test)}. Features number: {len(FEATURES_NAMES)}')

    ###############
    # Brute force #
    ###############
    max_depth = [100, 150, 170]
    min_samples_split = [4, 5, 6]
    max_leaf_nodes = [90, 100, 110]
    param_grid = {'max_depth': max_depth,
                  'min_samples_split': min_samples_split,
                  'max_leaf_nodes': max_leaf_nodes}
    estimator = RandomForestRegressor(n_estimators=300, n_jobs=-1)
    optimizer = GridSearchCV(estimator, param_grid, cv=3,
                             scoring='neg_mean_absolute_error')
    optimizer.fit(x_train, y_train)
    # Optimal model was found
    reg = optimizer.best_estimator_

    with open('model.pkl', 'wb') as pkl:
        pickle.dump(reg, pkl)

    reg.fit(x_train, y_train)
    predicted_train = reg.predict(x_train).round()
    predicted_test = reg.predict(x_test).round()

    # Calculate metrics on train and test
    mae_metric_train = mean_absolute_error(y_true=y_train, y_pred=predicted_train)
    mae_metric_test = mean_absolute_error(y_true=y_test, y_pred=predicted_test)

    print(f'Train MAE: {mae_metric_train:.2f}, Test MAE: {mae_metric_test:.2f}')

    plt.scatter(y_test, predicted_test, c='blue', alpha=0.5, s=20, edgecolor='#BCE7FF')
    plt.plot([np.min(y_test), np.max(y_test)], [np.min(y_test), np.max(y_test)],
             c='black')
    plt.grid()
    plt.title(f'Actual vs predicted')
    plt.show()

    # Classification task - assign labels
    predicted_train_class = deepcopy(predicted_train)
    predicted_train_class[predicted_train_class < class_threshold] = YOUNG_CLASS
    predicted_train_class[predicted_train_class >= class_threshold] = OLD_CLASS

    predicted_test_class = deepcopy(predicted_test)
    predicted_test_class[predicted_test_class < class_threshold] = YOUNG_CLASS
    predicted_test_class[predicted_test_class >= class_threshold] = OLD_CLASS

    matrix_train = confusion_matrix(y_class_train, predicted_train_class, normalize='all') * 100
    train_accuracy = accuracy_score(y_class_train, predicted_train_class)

    matrix_test = confusion_matrix(y_class_test, predicted_test_class, normalize='all') * 100
    test_accuracy = accuracy_score(y_class_test, predicted_test_class)

    print('Predicted values:', predicted_test[:10])
    print('Predicted classes:', predicted_test_class[:10])
    print('Real values:', y_test[:10])
    print('Real classes:', y_class_test[:10])

    print(train_accuracy, matrix_train)
    print(test_accuracy, matrix_test)

    disp = ConfusionMatrixDisplay(confusion_matrix=matrix_test,
                                  display_labels=['old', 'young'])
    disp.plot(cmap='Blues')
    plt.show()

    matrix_test = confusion_matrix(y_class_test, predicted_test_class)
    disp = ConfusionMatrixDisplay(confusion_matrix=matrix_test,
                                  display_labels=['old', 'young'])
    disp.plot(cmap='Blues')
    plt.show()


if __name__ == "__main__":
    fit_regression_model()
