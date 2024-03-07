import geopandas as gpd
from pathlib import Path

import rasterio
from rasterio import features

from pymetsa.paths import get_arbonaut_vector_path, get_data_folder_path, \
    get_arbonaut_raster_path


def vector_to_raster():
    vector_file = Path(get_arbonaut_vector_path(), 'old_growth_forest.shp')
    template_raster_path = Path(get_arbonaut_raster_path(), 'DTM.tif')
    output_raster_file = Path(get_data_folder_path(), 'old_growth_forest.tif')

    # Start transformation
    vector_layer = gpd.read_file(vector_file)
    rst = rasterio.open(template_raster_path)
    meta = rst.meta.copy()
    meta.update(compress='lzw')

    with rasterio.open(output_raster_file, 'w+', **meta) as out:
        out_arr = out.read(1)

        # this is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value) for geom, value in zip(vector_layer.geometry,
                                                       [1] * len(vector_layer)))

        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr,
                                    transform=out.transform)
        out.write_band(1, burned)


if __name__ == "__main__":
    vector_to_raster()
