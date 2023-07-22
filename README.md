# ETH Project
This repository contains all data files and methods to recreate the building footprint point cloud segmentation using WebODM, QGIS, and CloudCompare. 

# Introduction
This project aims to develop a pipeline to convert drone imagery of cityscapes to extract individual point clouds of buildings in the sampled area. For which the primary input is drone images that are captured and georeferenced over the area of interest. Following this, photogrammetry software is used to reconstruct the point cloud using the data collected. The reconstructed point cloud is then fed into GIS (QGIS in our case) to correct any Coordinate Reference Systems (CRS) issues (if any) and to process the point cloud further. 

To find the building footprints, we can either use an existing labeled shapefile or take the help of OpenStreetMap's (OSM) data to extract building footprint information using the QGIS plugin called "QuickOSM." The next step would be to ensure the overlap between the point cloud and shapefile is to our convenience and apply a buffer to the shapefiles to include building overhangs if needed. 

Finally, the shapefile and point clouds are exported and reimported into CloudCompare for further processing. CloudCompares segmentation tool allows us to edit point clouds, and this functionality would enable us to segment buildings and save them as individual shape files individually. The shapefiles would act as a guide to communicate with CloudCompare's segmentation tool.



