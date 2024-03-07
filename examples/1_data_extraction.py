from typing import List
from copy import deepcopy
from pathlib import Path
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from matplotlib import cm

from rasterio.mask import mask
from shapely.geometry import shape, mapping

from pymetsa.paths import get_arbonaut_raster_path, get_arbonaut_vector_path

FILE_NAMES = ["CHM.tif"]

def extract_values_by_extend_through_files(file_names_tif: List,
                                           shp_mask: str,
                                           result_name: str):
    """
    Rasterio example.
    Extract values from raster using saved geotiff file
    """
    vector_layer = gpd.read_file(Path(get_arbonaut_vector_path(), shp_mask))

    result_vector = deepcopy(vector_layer)

    for file_tif in file_names_tif:
        raster_path = Path(get_arbonaut_raster_path(), file_tif)

        # Create
        for id, row in vector_layer.iterrows():
            geometry = [mapping(row.geometry)]

            # It's important not to set crop as True because it distort output
            mins = []
            with rasterio.open(raster_path) as src:
                out_image, _ = mask(src, geometry, crop=False, nodata=-100.0)
                for layer in range(out_image.shape[0]):
                    clipped_matrix = out_image[layer, :, :]
                    clipped_matrix = clipped_matrix[clipped_matrix > -90]
                    
                    result_vector.iloc[id][f"{file_tif}_{layer}_mean"] = np.mean(clipped_matrix)
                    result_vector.iloc[id][f"{file_tif}_{layer}_std"] = np.std(clipped_matrix)
                    mins.append(np.min(clipped_matrix))
                    result_vector.iloc[id][f"{file_tif}_{layer}_max"] = np.max(clipped_matrix)

                        # row[f"CHM_mean"] = 

            # masked_array = np.ma.masked_where(clipped_matrix == -100.0,
            #                                   clipped_matrix)
            # cmap = cm.get_cmap('Blues')
            # cmap.set_bad(color='#C0C0C0')
            # plt.imshow(masked_array, interpolation='nearest', cmap=cmap)
            # plt.colorbar()
            # plt.title('Matrix in the extend')
            # plt.savefig(f"output_filepath_{id}.png", dpi=600, bbox_inches='tight')
            # plt.close()


if __name__ == '__main__':
    extract_values_by_extend_through_files(file_names_tif=FILE_NAMES,
                                           shp_mask="Age_grid.shp",
                                           result_name="result.csv")
