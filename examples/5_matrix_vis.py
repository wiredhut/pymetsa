from pathlib import Path

import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib import cm

from pymetsa.paths import get_data_folder_path


def show_matrices():
    """ Algorithm allows to show matrices """
    folder_with_files = Path(get_data_folder_path(), 'rasterized').resolve()
    for file in folder_with_files.iterdir():
        rst = rasterio.open(file)
        band = rst.read(1)

        masked_array = np.ma.masked_where(band < -10.0, band)
        cmap = cm.get_cmap('viridis')
        cmap.set_bad(color='#C0C0C0')
        plt.imshow(masked_array, interpolation='nearest', cmap=cmap)
        plt.colorbar()
        plt.title(file.name)
        plt.show()


if __name__ == "__main__":
    show_matrices()
