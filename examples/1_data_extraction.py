from typing import List
import os
import json
from pathlib import Path

import geopandas as gpd
import rasterio
from loguru import logger
from rasterstats import zonal_stats

from pymetsa.paths import get_arbonaut_raster_path, get_arbonaut_vector_path

import warnings
warnings.filterwarnings("ignore")


FILE_NAMES = (os.listdir(get_arbonaut_raster_path()))


def extract_values_by_extend_through_files(file_names_tif: List,
                                           shp_mask: str,
                                           result_name: str,
                                           buffers: List[int] = False):
    """
    Rasterio example.
    Extract values from raster using saved geotiff file
    """


    vector_layer = gpd.read_file(Path(get_arbonaut_vector_path(), shp_mask))
    geometries = ["geometry"]
    if buffers:
        for buf in buffers:
            vector_layer[f'geometry_{buf}'] = vector_layer.geometry.buffer(buf)
            geometries.append(f'geometry_{buf}')

    file_number = 1
    total_files = len(file_names_tif)

    file_coding = {}
    for id, file_tif in enumerate(file_names_tif):
        logger.info(f"START {file_tif} ({file_number}/{total_files})")
        raster_path = Path(get_arbonaut_raster_path(), file_tif)
        file_coding[str(id)] = file_tif
        with rasterio.open(raster_path) as src:
            for layer in range(1, len(src.indexes) + 1):
                logger.info(f"Band {layer}")
                for g_id, geometry in enumerate(geometries):
                    logger.info(f"Geometry {geometry}")
                    vector_layer[f"{id}_{layer}_{g_id}_mean"] = [x["mean"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                                raster=raster_path,
                                                                                                stats="mean",
                                                                                                band=layer)]
                    vector_layer[f"{id}_{layer}_{g_id}_std"] = [x["std"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                              raster=raster_path,
                                                                                              stats="std",
                                                                                              band=layer)]
                    vector_layer[f"{id}_{layer}_{g_id}_min"] = [x["min"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                              raster=raster_path,
                                                                                              stats="min",
                                                                                              band=layer)]
                    vector_layer[f"{id}_{layer}_{g_id}_max"] = [x["max"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                              raster=raster_path,
                                                                                              stats="max",
                                                                                              band=layer)]
        file_number += 1

    geometries.pop(0)
    if len(geometries) > 0:
        vector_layer.drop(labels=geometries, axis=1, inplace=True)
    vector_layer.to_file(result_name)
    with open('coding_names.json', 'w') as fp:
        json.dump(file_coding, fp)


if __name__ == '__main__':
    extract_values_by_extend_through_files(file_names_tif=FILE_NAMES,
                                           shp_mask="Age_grid.shp",
                                           result_name="extraction_result.shp",
                                           buffers=[-6, 12])
