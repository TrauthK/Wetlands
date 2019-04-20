ET12months_vector script needs to enter these inputs inside the script:
 Inputs:-
        watermask3= 0 if the vegetation is deciduous, 1 if the vegetation is miscellanous (grass), and 2 if no vegetation (bare)
  	WContent; water content at any time
	WCper; water content at willting point
	WCper; water content at field capacity
	d; depth of root zoon
	Apan; list of class A evaporation in cm/day
	KcoA; plant water-use for first vegetation (deciduous in this case)
	KcoM; plant water-use for second vegetation ( miscellanous - grass)
Outputs:-
     a text file named (ET_12months.txt)  will be sent to the path defined in the script with the mean evapotranspiration in cm/hr for all months 
    

   
***make sure that folder path in python script is right***