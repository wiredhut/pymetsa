import rasterio
from rasterio.transform import from_origin
import numpy as np

# Define the file path for the new GeoTIFF
file_path = "pymetsa/sample/tif_files/geotif_example.tif"

# Create an array of shape (12, 100, 100) with random values to simulate RGB bands
data = np.random.randint(0, 255, (12, 100, 100), dtype=np.uint8)

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
    count=12,
    dtype=data.dtype,
    crs=crs,
    transform=transform
) as dst:
    dst.write(data)
