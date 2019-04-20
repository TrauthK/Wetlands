ET12months_vector script needs to prepare these inputs as raster data first inside the geodatabase file (i.e.,SaxtonOc17.gdb for saxton site and October17.gdb for pershing state park site) :
 Inputs:-
        watermask3= MaskSaxton
  	WContent; water content at any time -(Raster)
	WCper; water content at willting point-(Raster)
	WCper; water content at field capacity -(Raster)
	d; depth of root zoon -(Raster)
	Apan; list of class A evaporation in cm/day -( List)
	KcoA; list of plant water-use for first vegetation (deciduous in this case)- ( List)
	KcoM; list of plant water-use for second vegetation ( miscellanous - grass)-( List)
Outputs:-
     a text file named (ET_12months.txt)  will be sent to the path defined in the script with the mean evapotranspiration in cm/hr for all months 
     Raster maps for each month in cm/hr - need to use the symbology to see the unique values for each month
    

   
***make sure that folder path in python script is right***