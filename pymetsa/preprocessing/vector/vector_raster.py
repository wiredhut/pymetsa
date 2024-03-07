import geopandas as gpd
from pathlib import Path

import rasterio
from rasterio import features
import matplotlib.pyplot as plt

from pymetsa.constants import POINT_TO_RASTER_BUFFER


def vector_to_raster(vector_layer: gpd.GeoDataFrame,
                     template_raster_path: Path,
                     output_raster_file: Path,
                     transformation_type: str = 'polygon'):
    """ Convert vector layer into raster format (for example, geotiff file)

    Args:
        vector_layer: geo dataframe with geometry to be converted
        template_raster_path: path to the file with source parameters to be copied
        output_raster_file: path to the final path
        transformation_type: convert vectors to raster type.
            Possible options are: 'polygon' and 'point'
    """
    rst = rasterio.open(template_raster_path)
    meta = rst.meta.copy()
    meta.update(compress='lzw')

    if transformation_type == 'point':
        vector_layer = vector_layer.geometry.buffer(POINT_TO_RASTER_BUFFER)

    with rasterio.open(output_raster_file, 'w+', **meta) as out:
        out_arr = out.read(1)

        # this is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value) for geom, value in zip(vector_layer.geometry,
                                                       [1] * len(vector_layer)))

        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr,
                                    transform=out.transform)

        plt.imshow(burned)
        plt.show()

        out.write_band(1, burned)
