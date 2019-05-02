

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import gdal 
#TESTING 

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
import os 
import glob
import gdal 

path = 'C:\\Users\\Lauren\\Downloads\\Lidar tiles' #Locates folder with multiple tif files stored in it

def create_tif(outfilename, arr_out, rows, cols):
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(outfilename, rows, cols, 1, gdal.GDT_UInt32)
    outband = outdata.GetRasterBand(1)
    outdata.SetProjection(ds.GetProjection())#sets same projection as input
    outband.WriteArray(arr_out)
    outdata.FlushCache() #saves to disk

    
for filename in glob.glob(os.path.join(path, '*.tif')): #Loop through folder with files ending in .tif
    ds = gdal.Open(filename) #Open file using gdal
    band = ds.GetRasterBand(1)
    band1 = band.ReadAsArray() #Reads band 1 as an array

    shapelist = band1.shape #Gets the size of the array with numpy
    cols = shapelist[0] #Stores the width of the raster
    rows = shapelist[1] #stores the height of the raster
    
    input_functions = [hillshade(band1, 45, 45), hillshade(band1, 315, 45), slope(band1), aspect(band1)] #List of functions
    folder = ['hillshade45','hillshade315','slope','aspect'] #List of folders where the output of functions will be stored
    endings = ['_shd45.tif','_shd315.tif','slp.tif','apt.tif'] #List of endings for each folder type 
    
    for i in range(0,4): #Loops through four times
        folderpath = path + "\\" + folder[i] + "\\" + filename[:3] + endings[i] #output folder is equal to the lidar tiles folder 
        create_tif(folderpath, input_functions[i], rows, cols)                  #plus the folder we are iterating through, plus
                                                                                #the filename minus the last 4 characters, plus
                                                                                #the file ending. 
    outdata = None #important to close the files
    band = None
    ds = None 
    