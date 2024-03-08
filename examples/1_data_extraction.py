from typing import List
from copy import deepcopy
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from loguru import logger
from rasterio.mask import mask
from shapely.geometry import mapping

from pymetsa.paths import get_arbonaut_raster_path, get_arbonaut_vector_path


FILE_NAMES = ["CHM.tif"]


def extract_values_by_extend_through_files(file_names_tif: List,
                                           shp_mask: str,
                                           result_name: str,
                                           buffer: int = False):
    """
    Rasterio example.
    Extract values from raster using saved geotiff file
    """
    vector_layer = gpd.read_file(Path(get_arbonaut_vector_path(), shp_mask))

    result_vector = deepcopy(vector_layer)

    for file_tif in file_names_tif:
        raster_path = Path(get_arbonaut_raster_path(), file_tif)
        logger.info(f"Start to extract {file_tif}")
        # Create
        step = 0
        for id, row in vector_layer.iterrows():
            if buffer:
                geometry = [mapping(row.geometry.buffer(buffer))]
            else:
                geometry = [mapping(row.geometry)]

            # It's important not to set crop as True because it distort output
            with rasterio.open(raster_path) as src:
                out_image, _ = mask(src, geometry, crop=False, nodata=-100.0)
                total_steps = len(vector_layer) * int(out_image.shape[0])
                for layer in range(out_image.shape[0]):
                    clipped_matrix = out_image[layer, :, :]
                    clipped_matrix = clipped_matrix[clipped_matrix > -90]
                    logger.debug(f"Clipped matrix has {len(clipped_matrix)} values for calculate statistics")

                    result_vector.loc[result_vector.index[id], f"{file_tif}_{layer}_mean"] = np.mean(clipped_matrix)
                    result_vector.loc[result_vector.index[id], f"{file_tif}_{layer}_std"] = np.std(clipped_matrix)
                    result_vector.loc[result_vector.index[id], f"{file_tif}_{layer}_min"] = np.min(clipped_matrix)
                    result_vector.loc[result_vector.index[id], f"{file_tif}_{layer}_max"] = np.max(clipped_matrix)

                    logger.info(f"It's done with ({step}/{total_steps}) steps")
                    step += 1

    result_vector.to_file(result_name)


if __name__ == '__main__':
    extract_values_by_extend_through_files(file_names_tif=FILE_NAMES,
                                           shp_mask="Age_grid.shp",
                                           result_name="extraction_result.shp")
