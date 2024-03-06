from pymetsa.visualization.visualize_ndvi import plot_ndvi

# Example usage of the function
INPUT_PATH = 'examples/temp_storage/ndvi_from_geotif_example.tif'
OUTPUT_PATH = 'examples/temp_storage/ndvi.png'


if __name__=="__main__":
    plot_ndvi(INPUT_PATH, OUTPUT_PATH)
