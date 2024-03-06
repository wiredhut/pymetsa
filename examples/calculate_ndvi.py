from pymetsa.preprocessing.raster.ndvi_from_tif import calculate_ndvi


INPUT_PATH = "pymetsa/sample/tif_files/geotif_example.tif"
OUTPUT_PATH = "examples/temp_storage/ndvi_from_geotif_example.tif"


if __name__=="__main__":
    calculate_ndvi(INPUT_PATH, OUTPUT_PATH)