from pymetsa.preprocessing.raster.get_tif_meta import get_tif_metadata

"""
====================================
      ORTHOPHOTO.tif
====================================
{
'driver': 'GTiff',
'dtype': 'uint8',
'nodata': None,
'width': 34305,
'height': 31948,
'count': 4,
'crs': CRS.from_epsg(3067),
'transform': Affine(0.25, 0.0, 596816.5, 0.0, -0.25, 6922194.0),
'bounds': BoundingBox(left=596816.5, bottom=6914207.0, right=605392.75, top=6922194.0),
'resolution': (0.25, 0.25),
'tags': {'AREA_OR_POINT': 'Area'}
}
"""

"""
=====================================
        CHM.tif
=====================================
{
'driver': 'GTiff',
'dtype': 'float32',
'nodata': -3.4028234663852886e+38,
'width': 8000,
'height': 7000,
'count': 1,
'crs': CRS.from_epsg(3067),
'transform': Affine(1.0, 0.0, 597000.0, 0.0, -1.0, 6921999.999),
'bounds': BoundingBox(left=597000.0, bottom=6914999.999, right=605000.0, top=6921999.999),
'resolution': (1.0, 1.0),
'tags': {'AREA_OR_POINT': 'Area'}
}
"""

"""
=====================================
        DTM.tif
=====================================
{
'driver': 'GTiff',
'dtype': 'float32',
'nodata': -3.4028234663852886e+38,
'width': 8000,
'height': 7000,
'count': 1,
'crs': CRS.from_epsg(3067),
'transform': Affine(1.0, 0.0, 597000.0001, 0.0, -1.0, 6922000.0001),
'bounds': BoundingBox(left=597000.0001, bottom=6915000.0001, right=605000.0001, top=6922000.0001),
'resolution': (1.0, 1.0),
'tags': {'AREA_OR_POINT': 'Area'}
}
"""

"""
=====================================
        Sentinel2.tif
=====================================
{
'driver': 'GTiff',
'dtype': 'uint16',
'nodata': None,
'width': 432,
'height': 400,
'count': 10,
'crs': CRS.from_epsg(3067),
'transform': Affine(20.0, 0.0, 596840.0, 0.0, -20.0, 6922139.9999),
'bounds': BoundingBox(left=596840.0, bottom=6914139.9999, right=605480.0, top=6922139.9999),
'resolution': (20.0, 20.0),
'tags': {'AREA_OR_POINT': 'Area'}}
"""


if __name__=="__main__":
    INPUT = 'pymetsa/sample/tif_files/Sentinel2.tif'
    metadata = get_tif_metadata(INPUT)
    print(metadata)
