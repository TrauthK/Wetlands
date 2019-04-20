###  this script to read the value of Estimated Plant-Water-Use coffecient Kco for Native Vegetaion
import arcpy
from arcpy import env
import os, sys, math
import numpy
from arcpy.sa import *
###setup environment
###env.workspace

# Ask the user to locate the workspapce or the raster catalog
env.workspace=arcpy.GetParameterAsText(0)
#env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\Data_Weather\\October17.gdb"
outpath = env.workspace

###Refresh gp object and permit overwriting
arcpy.env.overwriteOutput = True

watermask3=Raster("watermask3")
#####Remove problematic files
##if os.path.exists("schema.ini"):
##    os.remove("schema.ini")

### Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

##delete the existing ET4
inRaster = outpath + "\\ET4"
if arcpy.Exists(inRaster):
    arcpy.Delete_management(inRaster)
    
print"###############################################################################################################"
print"| This program is to compute the Spatail Evaportasnspiration rate  by using McWhorter and Sunada 1977 Equation|"
print"###############################################################################################################"
### inputs  Kco a crop coefficient for Aspen_Forest form the table for month ,April =
###WContent=Ɵ= the water content , WCPer=Ɵwp= water content at the permenant wiliting point; Wfc=Ɵfc= water content at the field capacity;
###d= is the rooting depth; AW= available water content; ET= potential evaportaspiration 

PET=[]
Eevap=[]

# Define Input for physical properties
WContent=Raster("WContent")
WContent=0.25
WCper=Raster("WCper")
Wfc=Raster("Wfc")
d=Raster("d")

#WCper=Raster("WCper")
WCper=0.11

#Wfc=Raster("Wfc")
Wfc=0.34

#Define the inputs and compute the evaporation from open surfaces
for i in range (0,12):
 # Enter the value of class A pan Evaportaion in cm/day form NOAA station for Pershing State Park from April to October
 Apan=[0,0,0,0.445, 0.497, 0.594, 0.655, 0.572, 0.413, 0.310,0,0]

 # define Kco crope for Aspen_Forst from April through October. For double vegetation, raster data will be used instead matrix
 KcoA=[0.60, 0.60 ,0.60, 0.67, 0.85, 0.90, 0.86, 0.75, 0.65, 0.60, 0.60, 0.60]
 # define Kco crope for Miscellaneaous from April through October. For double vegetation, raster data will be used instead matrix
 KcoM=[0.50, 0.50, 0.50, 0.60, 0.65, 0.65, 0.65, 0.60, 0.50, 0.50, 0.5,0.50]
 #PET this parameter has been computed upon the equation PET=0.70* Class A pan value  for peshing parke for a single vegetation
 m=0.70*Apan[i]
 PET.append(m)
 W=0.041667*PET[i] # use the watermask3 to compute the evaporation
 Eevap.append(W)
print "PET=",PET
#print("{0:.4f}".format(PET))
print"Eevap=",Eevap
#print("{0:.4f}".format(EvapW))
  
### Computing the AW availbel water content
AW=(WContent-WCper)*Raster("d")
print "the water content has been computed AW"

###Coputing Awmax= a  maximum available water content
Awmax=(Wfc-WCper)*Raster("d")
print "The maximum available water conent has been computed Awmax"
for i in range (0,12):

 #### computing Kc crop coefficient from the value of Kco
 
 ETA=(Ln((100*AW)/Awmax+1)/Ln(101))* KcoA[i]* PET[i]/24
 ETM=(Ln((100*AW)/Awmax+1)/Ln(101))* KcoM[i]* PET[i]/24
 print "The crop coefficient Kc has been computed Kc for Month=",i+1

 #####PET= the potential evaportaspiration; Kc= a crop coefficient; ET= the actual evaportranspiration
 ET=Con(watermask3==0,ETA,Con(watermask3==1,ETM,Con(watermask3==2,Eevap[i])))

 #ET=Kc*PET[i]/24
 ET.save(outpath + "\\" + "ET"+str(i+1))
 print "Actual Evaportanspiration (cm/hr.) has been successfully calculated as  ET",i+1
 print"--------------------------------------------------------------------------"
 print ""

