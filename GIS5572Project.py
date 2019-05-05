import arcpy

inputras = arcpy.GetParameter(0)
outputhill = arcpy.GetParameter(1)
outputslope = arcpy.GetParameter(2)
outputaspect = arcpy.GetParameter(3)

#Hillshade parameters
azimuth = 180
altitude = 75
modelShadows = "SHADOWS"
zFactor = 0.5

#Slope and Aspect parameters
outMeasurement = "DEGREE"
zFactorslope = ""
method = "GEODESIC"
zUnit = "FOOT"

#Execute hillshade with set parameters for input
arcpy.HillShade_3d(inputras, outputhill, azimuth, altitude, modelShadows, zFactor)

#Execute Slope with set parameters
arcpy.Slope_3d(inputras, outputslope, outMeasurement, zFactorslope, method, zUnit)

#Execute Aspect with set parameters
arcpy.Aspect_3d(inputras, outputaspect, method, zUnit)