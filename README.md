# pymetsa

Stands for finnish word "`metsä`" which means "`forest`". So, `pymetsa` is a library for forest-related spatial data processing

## Documentation 

The architecture og the module is multi-layer: 

* `Download` - access to data sources using bindings above APIs
* `Preprocessing` - set of functions to preprocess raw spatial data (both raster and vector)
* `Sample` - layer for preparing the data for neural networks training (clipping, augmentation, saving objects into files, etc.)
* `Model` - module for machine learning model fitting

And `visualization` for creating plots and save them into files.

## Examples 

In progress 

## Data sources 

- Landsat: https://earthexplorer.usgs.gov/. Dataset: `Landsat 8-9 OLI/TIRS C2 L2`. Product: `Landsat Collection 2 Level-2 Product Bundle`

## Contacts 

In progress