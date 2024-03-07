import geopandas as gpd
from pathlib import Path

import rasterio
from rasterio import features

from pymetsa.paths import get_arbonaut_vector_path, get_data_folder_path, \
    get_arbonaut_raster_path
from pymetsa.preprocessing.vector.vector_raster import vector_to_raster


def vector_to_raster_launch():
    vector_file = Path(get_arbonaut_vector_path(), 'Dead_trees.shp')
    template_raster_path = Path(get_arbonaut_raster_path(), 'DTM.tif')
    output_raster_file = Path(get_data_folder_path(), 'Dead_trees.tif')

    # Start transformation
    vector_layer = gpd.read_file(vector_file)
    vector_to_raster(vector_layer, template_raster_path, output_raster_file, 'point')


if __name__ == "__main__":
    vector_to_raster_launch()
