

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


file = "Downloads/MN_lidar_tile_-120-114_dem.tif" #Locates file
lidar_tile_120 = rasterio.open(file) #Opens file

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


with rasterio.open(file) as src:
    band1 = src.read(1)
    
hshade_array = hillshade(band1, 45, 45)
plt.imshow(hshade_array, cmap = 'Greys')
plt.show()
