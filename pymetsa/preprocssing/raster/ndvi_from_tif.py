import rasterio
import numpy as np

def calculate_ndvi(input_tif_path, output_ndvi_path):
    """
    Calculates the NDVI for a given Sentinel-2 .tif file and saves the result to a new file.

    Parameters:
    - input_tif_path: str, path to the input .tif file.
    - output_ndvi_path: str, path where the NDVI .tif file will be saved.
    """

    # Open the input .tif file
    with rasterio.open(input_tif_path) as src:
        # Assuming that the RED band is at position 4 (B4) and the NIR band is at position 8 (B8) in Sentinel-2 data
        red = src.read(4)
        nir = src.read(8)

        # Calculate NDVI
        ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)

        # Mask out invalid values
        ndvi[np.isnan(ndvi)] = -9999

        # Copy the metadata from the source .tif file
        meta = src.meta
        meta.update(driver='GTiff')
        meta.update(dtype=rasterio.float32)

        # Write the NDVI to the output .tif file
        with rasterio.open(output_ndvi_path, 'w', **meta) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)
