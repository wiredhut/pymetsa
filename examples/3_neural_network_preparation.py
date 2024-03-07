from pathlib import Path
from typing import List

import rasterio
from loguru import logger

from pymetsa.paths import prepared_folder, get_arbonaut_raster_path, \
    get_data_folder_path


def clip_and_normalize_matrix(features_matrices: List[Path], target_matrix: Path):
    """ This function allow to normalize matrix and clip it into small pieces """
    folder_for_results = prepared_folder()

    for feature in features_matrices:
        logger.info(f'Prepare feature matrix {feature.name}')
        rst = rasterio.open(feature)
        band = rst.read(1)


if __name__ == "__main__":
    features = [Path(get_arbonaut_raster_path(), 'DTM.tif')]
    target = Path(get_data_folder_path(), 'old_growth_forest.tif')
    clip_and_normalize_matrix(features_matrices=features, target_matrix=target)
