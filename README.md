# SDV602-Milestone2-QuangThanhDao

## MVC model

### Model

Used to process the information and data to provide to views

### View

Present the information and allow users interact

### Control

Control the view and process information

## Install geopandas

In order to run the application, geopandas is required as a dependency to display tagging location for on New Zealand map with longitude and latitude. 

While installing geopandas, you would need to also install Fiona which in turn require to install GDAL so to simplify the process, the two .whl files for GDAL and Fiona installation is included in src folder at root directory.

How to install .whl file? 

```bash
cd src
pip install GDAL-3.3.2-cp39-cp39-win_amd64
pip install Fiona-1.8.20-cp39-cp39-win_amd64
pip install geopandas

```

