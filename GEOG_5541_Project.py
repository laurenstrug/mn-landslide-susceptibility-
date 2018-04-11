

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import gdal 


file = "Downloads/MN_lidar_tile_-120-114_dem.tif" #Locates file
lidar_tile_120 = rasterio.open(file) #Opens file

folder = "Downloads/Lidar tiles" #Locates folder with three tiles

import os.path
os.path.isfile(file)

lidar_tile_120.profile #Gets metadata

lidar_tile_120.indexes #Checks number of bands

lidar_tile_120.read(1) #Reads first band

def hillshade(array, azimuth, angle_altitude): # Based on ESRI hillshade
    x, y = np.gradient(array) # http://geologyandpython.com/dem-processing.html
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth*np.pi / 180.
    altituderad = angle_altitude*np.pi / 180.

    shaded = np.sin(altituderad) * np.sin(slope) \
    + np.cos(altituderad) * np.cos(slope) \
    * np.cos(azimuthrad - aspect)
    return 255*(shaded + 1)/2

def slope(array):
    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    return slope

def aspect(array):
    x, y = np.gradient(array)
    aspect = np.arctan2(-x, y)
    return aspect

with rasterio.open(file) as src:
    band1 = src.read(1)
    
hshade_array = hillshade(band1, 45, 45)
plt.imshow(hshade_array, cmap = 'Greys')
plt.show()

#empyt 4 geodatabases: one for hillshade45, hillshade315, slope, and aspect
from osgeo import ogr
import os 
import glob

path = 'C:\\Users\\Lauren\\Downloads\\Lidar tiles'


#Below I am commenting out the way we were trying before with .gdb files

#driver = ogr.GetDriverByName("OpenFileGDB")
#ds = driver.Open(r"C:\Users\Lauren\Downloads\Lidar tiles", 0)

#hillshade45 = ("C:\Users\Lauren\Downloads\Hillshade45.gdb")
#hillshade315 = ("C:\Users\Lauren\Downloads\Hillshade315.gdb")
#slopelist = ("C:\Users\Lauren\Downloads\Slopelist.gdb")
#aspectlist = ("C:\Users\Lauren\Downloads\Aspectlist.gdb")

hillshade45array =[] #Empty arrays to store the output of the loop
hillshade315array = []
slopelistarray = []
aspectlistarray = []

for filename in glob.glob(os.path.join(path, '*.tif')): #Loop through folder
    with rasterio.open(filename) as src: #Opens tif in folder with rasterio
        band1 = src.read(1)

    hillshade45array.append(hillshade(band1, 45, 45))#Appends the output of the 
    hillshade315array.append(hillshade(band1, 315, 45))#function to the appropriate array
    slopelistarray.append(slope(band1))
    aspectlistarray.append(aspect(band1))
    
    #outhillshade45 = hillshade45 + "_hillshade45.tif" 
    
    
    #Below is a potential way to add each function to appropriate geodatabase 
    #for i in xrange(10):
       #with open('file_{0}.dat'.format(i),'w') as f:
          #f.write(str(func(i)))

print(hillshade45)
print(hillshade45array)
