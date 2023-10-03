# Roof Material Detection - Zurich
This repository contains all data files and methods to recreate the building footprint point cloud segmentation using WebODM, QGIS, and CloudCompare. All referenced sample data will be found in the repository.

# Resources
- Sample Data - https://drive.google.com/drive/folders/1oHafnQikcp2WWGg_-9QnJHNmybf0KZK9
- ODM Output - https://drive.google.com/file/d/1wDCRQjRzcwcxEG1J9Gw5VRFgao6-bn3h/view?usp=sharing
- Python Script - CloudCompareCrop2DScript.py

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

Download and install WebODM by following the steps in their documentation (https://docs.opendronemap.org/installation/). We are ready to process the data once it's up and running.

![image](https://github.com/Var-run/ETHProject/assets/99962766/0428a6cc-11dd-4c70-b122-4acc01513a0d)

Create a new Project and import the data. Once the data has been uploaded, you will be able to either process the job on your own hardware or take the help of ODMs cloud processing cluster called Lightning Network for larger datasets. There are a number of presets and options to define the processing parameters finely. For the sake of simplicity, we select the preset - Buildings Ultra Quality or 3D Mesh, following which we begin processing.

![image](https://github.com/Var-run/ETHProject/assets/99962766/7fcb7eb3-a9a0-4da9-a6e0-dd8e8ce41781)

OpenDroneMap's output can then be downloaded as a zip file for further processing. The output contains a lot of files (shown below), but the one we are interested in is the .laz file present in the odm_georeferences folder, as it contains the georeferenced point cloud of the area of interest.

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

Building footprints, by definition, are the boundaries of the  provides the outline of a building drawn along the exterior walls. They fail to account for building overhangs and other protrusions, so it is imperative to extend each polygon outwards to create a "buffer" to capture all features of each building completely. This can be achieved by employing the "Buffer" algorithm from the QGIS Toolbox. Once you open the dialog box, you will be greeted by the following window.

![image](https://github.com/Var-run/ETHProject/assets/99962766/94fbefed-ffe9-42ad-a322-d123950bbcb4)

The parameters here are highly suggested as they work well with the sample data. The distance is given in degrees and we select join style as miter to prevent rounding off of edges to ensure that fewer points are needed to the computer to represent the polygon thus resulting in fewer total calculations. The final result should look like the image attached below. Here we can see that we have the desired effect of enclosing an area that is slightly larger than the original building footprints to accommodate overhang and protrusions.

![image](https://github.com/Var-run/ETHProject/assets/99962766/2442d825-3728-4f5d-96c3-33e8facf686a)

The next step is to export these files under a specific projection system, "EPSG:32632 - WGS 84 / UTM zone 32N". We choose this because, as per our experiments, this projection system works best when we need further to process the shapefile and the point cloud in CloudCompare. This results in a perfect recreation of geographic overlap between the point cloud and the shapefile.

Export the buffered shapefile as a GeoJson with the settings displayed below, and similarly export it as a shapefile too with the same parameters. (NOTE: Use "Current Layer Extent")

![image](https://github.com/Var-run/ETHProject/assets/99962766/5a6bd4be-3c6d-4ac6-8d96-e855bbb82052)

Now export the point cloud similarly.

![image](https://github.com/Var-run/ETHProject/assets/99962766/a6b72c65-f30f-4bba-86e1-41d60fdec09b)

# Step 4: CloudCompare

Before we start to manipulate the point cloud, we should test to see if the export from QGIS is as per our expectations. So open CloudCompare and drag and drop the point cloud. When asked for the global shift, use the "Suggested" option and import the cloud as shown here.

![image](https://github.com/Var-run/ETHProject/assets/99962766/0d198af0-7982-42ae-b9fc-d62eef598674)

Next, when importing the .shp shapefile, do the same and select "Suggested" ONLY. This ensures that both the point cloud and the shapefile are in the same points in space and overlap as we expect them to be.

![image](https://github.com/Var-run/ETHProject/assets/99962766/ba4ae41c-a4eb-4a06-b0b3-d48301d085b3)

To view it without "Perspective" turned on, press F3 on the keyboard or turn it off manually. Once you do so, you should expect to see a display similar to the screenshot below. The shapefile and the point cloud have aligned as expected. The main reason for importing the shapefile is to take note of the GLOBAL SHIFT values for the point cloud and the shapefile which will be useful later on.

![image](https://github.com/Var-run/ETHProject/assets/99962766/bf60cbd0-6039-48c8-84d3-ff5611d87748)

Now, go to the properties window for the shapefile and the point cloud individually and take note of the "Global Shift" values. We would need this for our segmentation task that's coming up next.

![image](https://github.com/Var-run/ETHProject/assets/99962766/d7d0986d-cf23-4668-ae0a-23a62a62daae)

# Step 5: Segmentation using CloudCompare's Segmentation Tool via Command Line

Since we now have everything we need, we must use the shapefiles to crop out sections from the point cloud. In order to do so, we use CloudCompare's segmentation tool. After selecting the point cloud and using the segmentation tool, we would be greeted by the following window, followed by selecting the "Use existing polyline" option from the dropdown.

![image](https://github.com/Var-run/ETHProject/assets/99962766/926b467a-1263-40bd-85c5-40f2c5fa16b5)

There are two main drawbacks to segmenting the cloud in this way.
- It does not allow the user to select multiple polylines once to parallelize the operation and thus leads to poor automation capabilities.
- It also does not allow the user to easily rename the resulting cropped point cloud as per their specification (OSM ID/ EGID)

So in order to fix this, we turn to CloudCompares Command Line Mode to quickly segment a city's point cloud. By doing so, we eliminate both drawbacks by writing a Python script to loop through all polygons and having control over how to name each one according to our preferences. By default, this mode only opens a small console window, applies the requested actions, and eventually saves the result in a file in the same directory(ies) as the input file(s). Commands are applied in the order they are written (like a state machine). https://www.cloudcompare.org/doc/wiki/index.php/Command_line_mode

The segmentation tool is specified as a "CROP 2D" command in the command line mode and has the following specifications. 

![image](https://github.com/Var-run/ETHProject/assets/99962766/c971bd3d-7d69-4cb6-a3a2-2fb9633af00e)

Since the input format is not convenient with the shapefile format of the polygons that we currently have, we must turn to export the shapefile as a GeoJSON for easy manipulation in the Python script that would allow a seamless integration into the command line mode of CloudCompare. As per previous steps, this file should already be present in your machine, and now we can use it to generate a command line script for CloudCompare using Python. (Code can be found in the repository)

The final command that is being passed would look something like this. (NOTE: This is generated by the Python script where the destination and data file paths for point cloud and GeoJSON have to be explicitly changed for different use cases)
```
CloudCompare -SILENT -AUTO_SAVE OFF -O -GLOBAL_SHIFT -464000 -5247000 0 "C:\Crop2DTest\odm_georeferenced_model.laz" -CROP2D Z 14 233.542228180042 169.37840106990188 240.66421426046873 183.67630102299154 243.42336298833834 187.27241455577314 247.55219471349847 189.56099961232394 252.2847958728089 190.33349316194654 254.36182424088474 190.0786071512848 256.41002038581064 189.33001640439034 260.3230039589689 186.38172638602555 263.0054321034695 181.95552292931825 263.88300173473544 177.3445346672088 263.6980859042378 161.79339593835175 251.46847207017709 162.12427388876677 245.05494656821247 163.74126004986465 233.542228180042 169.37840106990188  -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE C:\Crop2DTest\Output\w39985864.las
```
Here are a few points to take note of:
- This code runs in the same directory as CloudCompare.exe, usually found in Program Files in your C:/ directory.
- "-SILENT" prevents the dialog box from popping up and speeds up computation time marginally.
- "-AUTO_SAVE OFF" prevents autosaving of point clouds as .bin files which can bloat up memory usage.
- "-O -GLOBAL_SHIFT -454000 -5247000 0" opens that point cloud and shifts it globally based on values specified in the Python script. These are the same values we had to note down earlier via CloudCompare UI.
- "-CROP2D" is the segmentation command, it is followed by Z which is the cropping dimension, and "14" is the number of (X, Y) pair of points, and it is followed by the values of these 14 pairs of points.
- "-C_EXPORT_FMT LAS" defines the export format of the resultant cropped point cloud.
- "-SAVE_CLOUDS FILE" helps us specify the location and name of the cropped point cloud.

There is internal handling of scenarios where a modified command is being run to check whether there are any points inside a given point cloud. This is necessary because if CloudCompare runs into a scenario where Crop2D saves the original complete point cloud as the cropped point cloud (hence creating more duplicates of the original point cloud with incorrect nomenclature) if there are no points inside a specific polygon.

For further clarification, the commented Python script will help clear any doubts. Finally, a sample test run is also uploaded to the repository to show you the expected output behavior when recreating these results with the sample test data.

# Step 6: Instance Segmentation

Now, using the Material Detection in Zurich Jupyter Notebook, we can segment and classify the rooftops once we have a labelled dataset.
