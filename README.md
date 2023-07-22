# ETH Project
This repository contains all data files and methods to recreate the building footprint point cloud segmentation using WebODM, QGIS, and CloudCompare. 

# Introduction
This project aims to develop a pipeline to convert drone imagery of cityscapes to extract individual point clouds of buildings in the sampled area. For which the primary input is drone images that are captured and geotagged over the area of interest. Following this, photogrammetry software is used to reconstruct the point cloud using the data collected. The reconstructed point cloud is then fed into GIS (QGIS in our case) to correct any Coordinate Reference Systems (CRS) issues (if any) and to process the point cloud further. 

To find the building footprints, we can either use an existing labeled shapefile or take the help of OpenStreetMap's (OSM) data to extract building footprint information using the QGIS plugin called "QuickOSM." The next step would be to ensure the overlap between the point cloud and shapefile is to our convenience and apply a buffer to the shapefiles to include building overhangs if needed. 

Finally, the shapefile and point clouds are exported and reimported into CloudCompare for further processing. CloudCompares segmentation tool allows us to edit point clouds, and this functionality would enable us to segment buildings and save them as individual shape files individually. The shapefiles would act as a guide to communicate with CloudCompare's segmentation tool.

# Step 1: Raw Data

The data used for this project is taken from Wingtra. Wingtra is an ETH spin-off drone producer for mapping, survey, and mining industry professionals and also publishes drone photography datasets at (https://wingtra.com/mapping-drone-wingtraone/aerial-map-types/data-sets-and-maps/) and encourages others to use this data. We used their publicly available sample data for the city of Zurich.

![image](https://github.com/Var-run/ETHProject/assets/99962766/e6ec8f52-54e5-40b5-9ca8-1ddb6b2bc1b7)

The sample data contains geotagged images of stretching over a segment of Langstrasse in Zurich. 

# Step 2: Photogrammetry using WebODM

The next step is to run the data through photogrammetry software, and we chose to go ahead with free non-proprietary software like OpenDroneMap's WebODM. OpenDroneMap is an open-source photogrammetry toolkit to process aerial imagery into maps and 3D models. The software is hosted and distributed freely on GitHub. WebODM is a user-friendly, extendable application and API for drone image processing. It provides a web interface to ODM with visualization, storage, and data analysis functionality.

![image](https://github.com/Var-run/ETHProject/assets/99962766/b4c6aa1f-8d50-4f7e-931b-c174e6fcdbcb)

