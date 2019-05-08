import arcpy

class ToolValidator(object):
    """Class for validating a tool's parameter values and controlling
    the behavior of the tool's dialog."""

    def __init__(self):
        """Setup arcpy and the list of tool parameters.""" 
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self): 
        """Refine the properties of a tool's parameters. This method is 
        called when the tool is opened."""

    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed. This method is called whenever a parameter
        has been changed."""
        # Update the value list filter in the second parameter based on the 
        #   shape type in the first parameter
        #
        stringFilter = self.params[1].filter

        if self.params[0].valueAsText:
            shapetype = arcpy.Describe(self.params[0]).shapeType.lower()
            if shapetype == "point" or shapetype == "multipoint":
                stringFilter.list = ["RED", "GREEN", "BLUE"]
            elif shapetype == "polygon":
                stringFilter.list = ["WHITE", "GRAY", "BLACK"]
            else:
                stringFilter.list = ["ORANGE", "INDIGO", "VIOLET"]
        else:
            stringFilter.list = ["RED", "GREEN", "BLUE"]

        # If the user hasn't changed the keyword value, set it to the default value
        #  (first value in the value list filter).
        #
        if not self.params[1].altered:
            self.params[1].value = stringFilter.list[0]
            
        return
    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""