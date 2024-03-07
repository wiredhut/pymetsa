from pathlib import Path
from typing import Union

import rasterio
from rasterio.transform import from_origin
import numpy as np


def create_tif(file_path: Union[str, Path], bands: int = 12):
    if isinstance(file_path, str):
        file_path = Path(file_path)

    file_path = file_path.resolve()
    if file_path.is_file() is False:
        file_path.parent.mkdir(exist_ok=True, parents=True)

    data = np.random.randint(0, 255, (bands, 100, 100), dtype=np.uint8)

    # Define the transform and CRS (Coordinate Reference System) for Helsinki
    transform = from_origin(24.941, 60.170, 0.0001, 0.0001)  # Dummy values, for illustration
    crs = "EPSG:3067"  # WGS84

    # Create a new GeoTIFF file
    with rasterio.open(
        file_path,
        'w',
        driver='GTiff',
        height=data.shape[1],
        width=data.shape[2],
        count=bands,
        dtype=data.dtype,
        crs=crs,
        transform=transform
    ) as dst:
        dst.write(data)
