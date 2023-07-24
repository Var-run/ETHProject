# ETH Project
This repository contains all data files and methods to recreate the building footprint point cloud segmentation using WebODM, QGIS, and CloudCompare. 

# Introduction
This project aims to develop a pipeline to convert drone imagery of cityscapes to extract individual point clouds of buildings in the sampled area. For which the primary input is drone images that are captured and geotagged over the area of interest. Following this, photogrammetry software is used to reconstruct the point cloud using the data collected. The reconstructed point cloud is then fed into GIS (QGIS in our case) to correct any Coordinate Reference Systems (CRS) issues (if any) and to process the point cloud further. 

To find the building footprints, we can either use an existing labeled shapefile or take the help of OpenStreetMap's (OSM) data to extract building footprint information using the QGIS plugins. The next step would be to ensure the overlap between the point cloud and shapefile is to our convenience and apply a buffer to the shapefiles to include building overhangs if needed. 

Finally, the shapefile and point clouds are exported and reimported into CloudCompare for further processing. CloudCompares segmentation tool allows us to edit point clouds, and this functionality would enable us to segment buildings and save them as individual shape files individually. The shapefiles would act as a guide to communicate with CloudCompare's segmentation tool.

# Step 1: Raw Data

The data used for this project is taken from Wingtra. Wingtra is an ETH spin-off drone producer for mapping, survey, and mining industry professionals and also publishes drone photography datasets at (https://wingtra.com/mapping-drone-wingtraone/aerial-map-types/data-sets-and-maps/) and encourages others to use this data. We used their publicly available sample data for the city of Zurich.

![image](https://github.com/Var-run/ETHProject/assets/99962766/e6ec8f52-54e5-40b5-9ca8-1ddb6b2bc1b7)

The sample data contains geotagged images of stretching over a segment of Langstrasse in Zurich. 

# Step 2: Photogrammetry using WebODM

The next step is to run the data through photogrammetry software, and we chose to go ahead with free non-proprietary software like OpenDroneMap's WebODM. OpenDroneMap is an open-source photogrammetry toolkit to process aerial imagery into maps and 3D models. The software is hosted and distributed freely on GitHub. WebODM is a user-friendly, extendable application and API for drone image processing. It provides a web interface to ODM with visualization, storage, and data analysis functionality.

![image](https://github.com/Var-run/ETHProject/assets/99962766/b4c6aa1f-8d50-4f7e-931b-c174e6fcdbcb)

Download and install WebODM by following the steps given in their documentation (https://docs.opendronemap.org/installation/). We are ready to process the data once it's up and running.

![image](https://github.com/Var-run/ETHProject/assets/99962766/0428a6cc-11dd-4c70-b122-4acc01513a0d)

Create a new Project and import the data. Once the data has been uploaded, you will be able to either process the job on your own hardware or take the help of ODMs cloud processing cluster called Lightning Network for larger datasets. There are a number of presets and options to define the processing parameters finely. For the sake of simplicity, we select the preset - Buildings Ultra Quality or 3D Mesh, following which we begin processing.

![image](https://github.com/Var-run/ETHProject/assets/99962766/7fcb7eb3-a9a0-4da9-a6e0-dd8e8ce41781)

OpenDrneMap's output can then be downloaded as a zip file to begin further processing. The output contains a lot of files (shown below), but the one we are interested in is the .laz file present in the odm_georeferences folder, as it contains the georeferenced point cloud of the area of interest.

![image](https://github.com/Var-run/ETHProject/assets/99962766/9fcd2c2b-b3e6-4b0f-bee4-08a52243ea39)

# Step 3: QGIS

We now import the point cloud into QGIS, which is a free and open-source cross-platform desktop geographic information system application that supports viewing, editing, printing, and analysis of geospatial data. We do so for a number of reasons.
  1. To fix/reproject the point clouds onto the correct geographical coordinates.
  2. To import OpenStreetMap data containing the building footprint data.
  3. To generate buffers around individual building footprints (more on this later).
  4. To have control over the export formats and specifications for further processing in CloudCompare.

To start with, we import the point cloud into QGIS, and by default, it would be imported as expected over the relevant matching area on the globe. To verify this, import an OpenStreetMap layer (under XYZ Tiles) below this to gain visual confirmation.

![image](https://github.com/Var-run/ETHProject/assets/99962766/2873d345-4106-4608-9fe4-043ad1482355)

Next, we use the QuickOSM QGIS plugin to import the building footprint data (or use an existing shapefile). This is not installed by default, and instructions for installation can be found here - https://docs.3liz.org/QuickOSM/. Now import building footprint data for the region of interest. by running the plugin and specifying the key value as "building" and spatial extent for the query as "Layer Extent" followed by selecting the "odm_georeferenced_model" as the layer.

![image](https://github.com/Var-run/ETHProject/assets/99962766/d2fad40c-7776-4aa4-9119-8b55c5b1e166)

Upon running this query, the plugin imports all building footprints as a vector layer, as shown below. Along with the building footprints, it also imports the centroids of each building's footprint as a separate layer. We do not need this layer, so it can be ignored.

![image](https://github.com/Var-run/ETHProject/assets/99962766/b23ebd74-cbaf-4c0c-8126-8f9bb815c942)







