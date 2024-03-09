<img src="./docs/pymetsa_logo.png" width="750"/>

Stands for finnish word "`metsä`" which means "`forest`". So, `pymetsa` is a library for forest-related spatial data processing

## Before start 

To use this library there is a need to place the following files in the **[data](./data)** folder in this repository:

* `arbonaUT` / `Raster_data`
* `arbonaUT` / `Vector_data`
* `arbonaUT` / `Lidar_variables.xlsx`

## Documentation 

The architecture og the module is multi-layer: 

* `Download` - access to data sources using bindings above APIs
* `Preprocessing` - set of functions to preprocess raw spatial data (both raster and vector)
* `Sample` - layer for preparing the data for neural networks training (clipping, augmentation, saving objects into files, etc.)
* `Model` - module for machine learning model fitting

And `visualization` for creating plots and save them into files.

## Examples 

The **[examples](./examples)** folder contain all necessary launch demo scenarios for this library

## Data sources 

- Landsat: https://earthexplorer.usgs.gov/. Dataset: `Landsat 8-9 OLI/TIRS C2 L2`. Product: `Landsat Collection 2 Level-2 Product Bundle`


## Pymetsa as a service 

Current module deployed on Heroku using the following instructions: 

[Deploy FastAPI on Heroku using Docker Container](https://akshaykhatale.medium.com/deploy-fastapi-on-heroku-using-docker-container-a920f839de9b)

```
heroku login
```

Launch docker daemon and then 
```
heroku container:login
```

```
heroku container:push web --app pymetsa-demo
```

```
heroku container:release web --app pymetsa-demo
```

Swagger UI available via URL: <span style="color:orange">In progress</span>

- `login`: `demo`
- `password`: `demo`

For local launch there is a need to start `launch.py`

## Contacts 

<span style="color:orange">In progress</span>
