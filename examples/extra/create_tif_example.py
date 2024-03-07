from pathlib import Path

from pymetsa.paths import get_tmp_folder_path
from pymetsa.preprocessing.raster.create_tif import create_tif


if __name__ == "__main__":
    generated_file = Path(get_tmp_folder_path(),
                          'ndvi_from_geotiff_example.tif')
    create_tif(generated_file)
