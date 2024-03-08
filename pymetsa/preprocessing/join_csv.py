from typing import List
import os
from pathlib import Path

import pandas as pd
from loguru import logger

from pymetsa.paths import get_tmp_folder_path


files_list = (os.listdir(get_tmp_folder_path()))
FILE_NAMES = [x for x in files_list if '.csv' in x]


def join_many_csv(file_names_csv: List,
                  result_file_name: str):

    dataframes = []
    for file in file_names_csv:
        df = pd.read_csv(Path(get_tmp_folder_path(), file))
        df.drop(["Unnamed: 0"], axis=1, inplace=True)
        dataframes.append(df)
        logger.info(f"{file} size = {len(df)}, columns={len(df.columns)}")
        print(df.columns)
    full_df = pd.concat(dataframes, axis=1)

    full_df.to_csv(result_file_name)


if __name__ == '__main__':
    join_many_csv(file_names_csv=FILE_NAMES,
                  result_file_name="PREDICTION_extraction.csv")
