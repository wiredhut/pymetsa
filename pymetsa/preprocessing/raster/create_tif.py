import rasterio
from rasterio.transform import from_origin
import numpy as np

# Define the file path for the new GeoTIFF
file_path = "pymetsa/sample/tif_files/geotif_example.tif"

def create_tif(file_path, bands:int = 12):
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
