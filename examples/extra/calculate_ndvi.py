from pathlib import Path

from pymetsa.paths import get_tmp_folder_path, get_data_folder_path
from pymetsa.preprocessing.raster.ndvi_from_tif import calculate_ndvi


INPUT_PATH = Path(get_data_folder_path(), 'geotif_example.tif')
OUTPUT_PATH = Path(get_tmp_folder_path(), 'ndvi_from_geotiff_example.tif')


if __name__ == "__main__":
    calculate_ndvi(INPUT_PATH, OUTPUT_PATH)
