import json
import os
import subprocess
  
# Opening JSON file
f = open('GeoJsonTestBuffered.geojson')   #Specify name and location of buffered GeoJSON file
data=json.load(f)

GLOBAL_SHIFT_X=-464000  #Global shift values noted down from CloudCompare using "Suggested" shift
GLOBAL_SHIFT_Y=-5247000
cloudpath='"C:\Crop2DTest\odm_georeferenced_model.laz"'   #Path of the input point cloud
savepath="C:\\Crop2DTest\\Output\\"     #Path of the output folder

s="CloudCompare -SILENT -AUTO_SAVE OFF -O -GLOBAL_SHIFT "+str(GLOBAL_SHIFT_X)+" "+str(GLOBAL_SHIFT_Y)+" 0 "+cloudpath+" -CROP2D Z " # Base Command
s1=s # Storing template for reuse
flag=0
vertices=0
temp=""

for key in data["features"]:
    id=key["properties"]["full_id"]
    for i in key["geometry"]["coordinates"]:
        for k in i:
            for j in k:
                for p in j:
                    vertices+=1     #Counting number of vertices
                    if flag%2==0:
                        temp=temp+str(p+GLOBAL_SHIFT_X)+" "     #Shifting all X coordinates by corresponding global shift
                    else:
                        temp=temp+str(p+GLOBAL_SHIFT_Y)+" "     #Shifting all Y coordinates by corresponding global shift
                    flag+=1
            s=s+str(int(vertices/2))+" "+temp                   #Appending number of vertices and points to the command
            os.chdir(r"C:\Program Files\CloudCompare")          #Changing directory to where CloudCompare.exe exists
            result = subprocess.run(s, capture_output=True, text=True,shell= True)  #Running partial command without saving to check whether points exist within given polygon
            if "No point of cloud" in result.stdout:
                print("No point found inside this region of interest!")
            else:
                s=s+" "+"-C_EXPORT_FMT LAS -SAVE_CLOUDS FILE "+savepath+id+".las" #If points exists, then crop and save it to the id
                print(s)
                os.system(s) #Passing command to the system
            s=s1        #Reusing the template for next polygon
            temp=""     #Resetting all other variables
            flag=0
            vertices=0
            print()