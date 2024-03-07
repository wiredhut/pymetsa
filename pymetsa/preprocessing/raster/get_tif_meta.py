import rasterio

def get_tif_metadata(path):
    """
    Open a TIF file and return its metadata using rasterio.

    Parameters:
    - path: str, the path to the TIF file.

    Returns:
    - dict, containing the metadata of the TIF file.
    """
    try:
        with rasterio.open(path) as src:
            metadata = src.meta.copy()  # Get a copy of the metadata
            # Optionally, add more detailed metadata components
            metadata["bounds"] = src.bounds
            metadata["resolution"] = src.res
            metadata["tags"] = src.tags()
            return metadata
    except Exception as e:
        return {"error": str(e)}
