from typing import List
from loguru import logger

import geopandas as gpd
from pathlib import Path

import rasterio
from rasterio import features
import matplotlib.pyplot as plt

from pymetsa.constants import POINT_TO_RASTER_BUFFER


def vector_to_raster(vector_layer: gpd.GeoDataFrame,
                     template_raster_path: Path,
                     output_raster_file: Path,
                     field: str):
    """ Convert vector layer into raster format (for example, geotiff file)

    Args:
        vector_layer: geo dataframe with geometry to be converted
        template_raster_path: path to the file with source parameters to be copied
        output_raster_file: path to the final path
        field: field to store into the cells
    """
    rst = rasterio.open(template_raster_path)
    meta = rst.meta.copy()
    meta.update(compress='lzw')

    with rasterio.open(output_raster_file, 'w+', **meta) as out:
        out_arr = out.read(1)

        # this is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value) for geom, value in zip(vector_layer.geometry, vector_layer[field]))

        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr,
                                    transform=out.transform)
        out.write_band(1, burned)


class Rasterizer:
    """ Convert defined vector layers into raster objects """

    fields_by_file = {'Age_grid.shp': ['age', 'basalarea', 'volume',
                                       'sampleplot', 'Class'],
                      'Canopy_structure.shp': ['H_stdev'],
                      'final_prediction.shp': ['p_age', 'p_class'],
                      'Grid_lidar_variables..shp': ['INV_UNIT', 'OBJECTID',
                                                    'Shape_Leng', 'Shape_Area',
                                                    'L_DDate', 'L_VEG_Z95',
                                                    'L_VEG_VD', 'L_X_VD',
                                                    'L_X_ZP95', 'L_L30M_02',
                                                    'L_L30M_12', 'L_L30M_14',
                                                    'L_L30M_15', 'L_L30M_20',
                                                    'L_L27M_11', 'L_L27M_13',
                                                    'L_L27M_18', 'L_L27M_26',
                                                    'L_FI5_IP1', 'L_FI5_IP2',
                                                    'L_FI5_IP3', 'L_FI5_IA1',
                                                    'L_FI5_IA2', 'L_FI5_IA3']}

    def __init__(self, vector_paths: List[Path], results_folder: Path):
        self.vector_paths = vector_paths
        self.results_folder = results_folder

        if self.results_folder.exists() is False:
            self.results_folder.mkdir(exist_ok=True, parents=True)

    def run(self, template_raster_path: Path):
        """ Create raster layers based on geometries """
        for vector_file in self.vector_paths:
            gdf = gpd.read_file(vector_file)

            for field in self.fields_by_file[vector_file.name]:
                logger.info(f'Rasterize {vector_file.name}. Field: {field}')

                raster_name = vector_file.name.split('.')[0]
                raster_name = f'{raster_name}_{field}.tif'
                output_raster_file = Path(self.results_folder, raster_name)
                vector_to_raster(vector_layer=gdf, template_raster_path=template_raster_path,
                                 output_raster_file=output_raster_file, field=field)
