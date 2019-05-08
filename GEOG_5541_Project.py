import arcpy
#Defining input and output parameters
inputras = arcpy.GetParameter(0)
outputhill = arcpy.GetParameterAsText(8)
outputslope = arcpy.GetParameterAsText(9)
outputaspect = arcpy.GetParameterAsText(10)

#Hillshade parameters
azimuth = arcpy.GetParameter(1)
altitude = arcpy.GetParameter(2)
modelShadows = arcpy.GetParameter(3)
zFactor = arcpy.GetParameter(6)

#Slope and Aspect parameters
outMeasurement = arcpy.GetParameter(4)
method = arcpy.GetParameter(5)
zUnit = arcpy.GetParameter(7)

count = 0
for ras in inputras:
	#Execute hillshade with set parameters for input
	arcpy.HillShade_3d(ras, outputhill + str(count), azimuth, altitude, modelShadows, zFactor)

	#Execute Slope with set parameters
	arcpy.Slope_3d(ras, outputslope + str(count), outMeasurement, zFactor, method, zUnit)

	#Execute Aspect with set parameters
	arcpy.Aspect_3d(ras, outputaspect + str(count), method, zUnit)
	
	count += 1
    