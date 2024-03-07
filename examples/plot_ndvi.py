from pathlib import Path

from pymetsa.paths import get_tmp_folder_path
from pymetsa.visualization.visualize_ndvi import plot_ndvi

# Example usage of the function
INPUT_PATH = Path(get_tmp_folder_path(), 'ndvi_from_geotiff_example.tif')
OUTPUT_PATH = Path(get_tmp_folder_path(), 'ndvi.png')


if __name__ == "__main__":
    plot_ndvi(INPUT_PATH, OUTPUT_PATH)