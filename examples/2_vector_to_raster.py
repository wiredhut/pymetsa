from pathlib import Path

from pymetsa.paths import get_arbonaut_vector_path, get_data_folder_path, \
    get_arbonaut_raster_path
from pymetsa.preprocessing.vector.vector_raster import vector_to_raster, \
    Rasterizer


def vector_to_raster_launch():
    """ Launch algorithm which transform vector attributes table into raster """
    files_names = ['Canopy_structure.shp', 'Grid_lidar_variables..shp']
    vector_paths = []
    for i in files_names:
        vector_paths.append(Path(get_arbonaut_vector_path(), i))

    # Launch the algorithm of vector to raster
    save_to = Path(get_data_folder_path(), 'rasterized').resolve()
    processor = Rasterizer(vector_paths, save_to)
    processor.run(Path(get_arbonaut_raster_path(), 'DTM.tif'))


if __name__ == "__main__":
    vector_to_raster_launch()
