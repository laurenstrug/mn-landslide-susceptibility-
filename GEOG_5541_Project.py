

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import glob


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

def slope(array)
    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    return slope

def aspect(array)
    x, y = np.gradient(array)
    aspect = np.arctan2(-x, y)
    return aspect

with rasterio.open(file) as src:
    band1 = src.read(1)
    
hshade_array = hillshade(band1, 45, 45)
plt.imshow(hshade_array, cmap = 'Greys')
plt.show()

#empyt 4 geodatabases: one for hillshade45, hillshade315, slope, and aspect

for filename in folder.glob("*.tif"): #Figure out how to loop through geodatabase with tif
    with rasterio.open(filename) as src:
        band1 = src.read(1)
    hillshade(band1, 45, 45)
    hillshade(band1, 315, 45)
    slope(band1)
    aspect(band1)
    #Add each function to appropriate geodatabase 
