from typing import List
import os
import json
from pathlib import Path

import geopandas as gpd
import rasterio
import pandas as pd
from loguru import logger
from rasterstats import zonal_stats

from pymetsa.paths import get_arbonaut_raster_path, get_arbonaut_vector_path, \
    get_tmp_folder_path

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
        tmp_df = pd.DataFrame()
        logger.info(f"START {file_tif} ({file_number}/{total_files})")
        raster_path = Path(get_arbonaut_raster_path(), file_tif)
        file_coding[str(id)] = file_tif
        with rasterio.open(raster_path) as src:
            for layer in range(1, len(src.indexes) + 1):
                logger.info(f"Band {layer}")
                for g_id, geometry in enumerate(geometries):
                    logger.info(f"Geometry {geometry}")
                    tmp_df[f"{id}_{layer}_{g_id}_mean"] = [x["mean"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                          raster=raster_path,
                                                                                          stats="mean",
                                                                                          band=layer)]
                    logger.info("mean calculated")
                    tmp_df[f"{id}_{layer}_{g_id}_std"] = [x["std"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                        raster=raster_path,
                                                                                        stats="std",
                                                                                        band=layer)]
                    logger.info("std calculated")
                    tmp_df[f"{id}_{layer}_{g_id}_min"] = [x["min"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                        raster=raster_path,
                                                                                        stats="min",
                                                                                        band=layer)]
                    logger.info("min calculated")
                    tmp_df[f"{id}_{layer}_{g_id}_max"] = [x["max"] for x in zonal_stats(vectors=vector_layer[geometry],
                                                                                        raster=raster_path,
                                                                                        stats="max",
                                                                                        band=layer)]
                    logger.info("max calculated")
        file_number += 1
        tmp_df.to_csv(Path(get_tmp_folder_path(), f"{file_tif.replace('.tif', '')}_result.csv"))

    geometries.pop(0)
    if len(geometries) > 0:
        vector_layer.drop(labels=geometries, axis=1, inplace=True)
    vector_layer.to_file(result_name)
    with open(Path(get_tmp_folder_path(), 'coding_names.json'), 'w') as fp:
        json.dump(file_coding, fp)


if __name__ == '__main__':
    executed_files = (os.listdir(get_tmp_folder_path()))
    executed_files = [x.replace("_result.csv", "") for x in executed_files]
    file_names = [x.replace(".tif", "") for x in FILE_NAMES]
    to_be_calculated = [x+".tif" for x in file_names if x not in executed_files]
    extract_values_by_extend_through_files(file_names_tif=to_be_calculated,
                                           shp_mask="Grid_lidar_variables..shp",
                                           result_name="extraction_result.shp")
