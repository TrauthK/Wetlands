import arcpy 
from arcpy import env
import os, sys, math
import numpy
from arcpy.sa import *
from numpy import inf

#setup environment
# Ask the user to locate the workspapce or the raster catalog
#env.workspace=arcpy.GetParameterAsText(0)
#env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\\Data_Weather\\Infiltration.gdb"
env.workspace="H:\\MissouriDo\\EPA\\Reports\\FinalReport\\infiltration\\Infiltration.gdb"
outpath=env.workspace

# ask the user to enter the integer time for running the model in hrs.
#duration=arcpy.GetParameterAsText(1)
duration=10 # Enter the total time to run the script in hrs.
num=int(duration)


#Inpath = env.workspace
#outpath="F:\\MissouriDo\\GeneralSearch\\EPA\Data_Weather\\AugResults.gdb"
#Results=outpath+"\\"+ "Outputs"

#Refresh gp object and permit overwriting
arcpy.env.overwriteOutput = True

###Remove problematic files
if os.path.exists("schema.ini"):
    os.remove("schema.ini")

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# build the pyramids and statitics to easy enable visoulize the raster
arcpy.BuildPyramidsandStatistics_management(arcpy.env.workspace)

print"#######################################################################################################################"
print"|The Spatail&Temporal Wetland Water Elevations and Volumes based on GREEN&AMPT Infiltration & Evapotranspiration Models|"
print"#######################################################################################################################"
print ""

################################################################
#Local variables
p=Raster("p")

to=Raster("to")
to=0.0
t=Raster("to")
watermask3=Raster("watermask3")

# note that the Fp that meets your inputs theata initial =0.25,0.27 and = 0.30
#Fp=1.2422, 1.1057    and 0.9009 respectively

# note that the tp that meets your inputs theata initial =0.25 , 0.27 and =0.30
#tp=0.6143, 2.2113 and 1.8018 hrs.
fd=Raster("fd")
f_rate=Raster("p")
ETd=Raster("ETd")
ETd=0.0
#wp= Willting point 
wp=0.11              

# fc= feild capacity; fc=0.34                     

# D=root zone 20 cm
D=20                 

# Enter here the evapotraspiration for a certain month -Aspen Vegetaion old value was 0.0157
Et0=0.0147           

#Enter here the evapotraspiration for a certain month -Miscellaneaous Vegetation  was 0.0118
Et1=0.0111           

# Enter here the evapotraspiration for a certain month -Bare or No Vegetaion was  0.0191
Ev=0.0191            

# minimum elevation from DEM 1 meter resolution
minElevation=216.320 

# maximum elevation from Dem 1 meter resolution
maxElevation=216.964 

#Soil Propertiessa raster data
phead=Raster("phead")
ks=Raster("ks")
wci=Raster("wci")
wc=Raster("wci")
wcs=Raster("wcs")
fc=Raster("fc")
exc=Raster("exc")
dw=Raster("to")
Dr=Raster("to")
AcRain=Raster("to")
excm=Raster("to")
#################################################################################
##Create the Lists  and the time for running the script num



p_t=[]
p_v=[]
p_wa=[]
Elevation=Raster("to")

# enter the minimum Elevation in the DEM raster of the Site 
p_min=[216.320,]*num    

# enter the maximum Elevation in the DEM raster of the Site
p_max=[216.964,]*num   

#################################################################################
####### delete the existing Fp
##inRaster = outpath + "Fp"
##if arcpy.Exists(inRaster):
##    arcpy.Delete_management(inRaster)
##os.makedirs(inRaster)
#################################################################################

# FP=phead*Ks(wcs-wci)/(p-ks), Fp = the accu. depth of water at ponding in (cm.)
Fp=phead*ks*(wcs-wci)/(p-ks)
Fp=Con(Fp>0,Fp,0)
#Fp.save(outpath + "\\Fp")
print"1- The(FP)accu. infiltrated depth has been computed successfully"

# tp= Fp/p ,tp= The(tp)time up to ponding in (hrs.)

tp=Fp/p
tp=Con(tp>0,tp,0)
tp.save(outpath + "\\tp")
print"2- The(tp)time up to ponding has been computed successfully "

#dfc= phead*ks*(fc-wci)/(p-ks), wci=0.25,0.27,0.30, dfc= is the depth of water in (cm.) required to reach the field capacity 
dfc=(phead*ks)*(fc-wci)/(p-ks)
dfc.save(outpath + "\\dfc")
print "3- The(dfc)depth of water has been computed"
print ""
print"------------------------------------------------------------"
 ############################################################################
 ##Iteraion through the time increment 1 hr. to compute f_rate in cm/hr.
for j in range (1,num,1):
  t=j/1.00
  p_t.append(t)
  print"iteration time step t in hrs.=",t
  p=Con((t<=7)|((t>=11) &(t<=16)),0.5,0)
  print "p=",p


   ## # 1-Process: Raster Calculator estimtaed f_rate based on power equation from GreenAmpt Equation in f_rate in (cm./hr)

  f_rate= Con(t <= tp,p,Con(watermask3==0,0.7919*t**(-0.547),Con(watermask3==1,0.7093*t**(-0.514),0.6269*t**(-0.492))))

  ## to update the infilitration ratef_rate.save(outpath + "\\f_rate"+ str(j))
  f_rate= Con(t <= tp,Con((p>0) | (exc>= f_rate*(t-to)),p,0),Con((p>0) | (exc>= f_rate*(t-to)),f_rate,0)) 
  f_rate.save(outpath + "\\f_rate" + str(j))
  print "1- The infiltration f_rate"+ str(j)+ " has been computed successfully"

  
  ## ## # 2- compute fd in (cm.), the acumalated infiltrated depth in the soil
  fd=Con((t>0),(fd+(f_rate*(t-to))),0.0)  # the incremental time 3600 sec= 1 hr
  fd.save(outpath + "\\fd" + str(j))
  print"2- The accu.infiltration depth fd"+ str(j)+ " has been computed successfully"

  ## ## #3- ETd accumulated evapotranspiration  depth in cm, ET for Aspen =0.0157,Evapotranspiration for Miscellaneuos =0.0118, for Bare zone evaportaion 0.0191 (cm/hr)
  #ETd=Con((wc<=wp),ETd,ETd+(ET*(t-to)))
  ETd=Con(wc<=wp,ETd,Con(watermask3==0,ETd+Et0*(t-to),Con(watermask3==1,ETd+Et1*(t-to),Con((watermask3==2) & (wc<fc),ETd,ETd+Ev*(t-to)))))
  ETd.save(outpath + "\\ETd" + str(j))
  print"3- The accu.evapotranspiration depth ETd"+ str(j)+ " has been computed successfully"

  ## ## #4- fd-ETd= dw is the accumuated ifilitration- evapotranspiration  depth in (cm.)
  dw=fd-ETd
  dw.save(outpath + "\\dw" + str(j))
  print"4- The accu.(infilitraion - evapotranspiration) depth dw"+ str(j)+ " has been computed successfully"



  ## #5-wc= water content at the end of time step =[wci+(dw/dfc)*(fc-wci)]
  wc=Con((wci+(dw/dfc)*(fc-wci))<=wp,wp,Con((wci+(dw/dfc)*(fc-wci))<fc,(wci+(dw/dfc)*(fc-wci)),fc))
  wc.save(outpath + "\\wc"+ str(j))
  print"5- The (wc) water content spatially  wc"+ str(j)+ "  has been computed successfully" 



  ## ## #6- Dr-Drainage ( water depth that exceeds the field capacity Fc in (cm.)
  
  Dr=Con(wc>=fc,dw-(fc-wc)*D,0)
  Dr.save(outpath + "\\Dr" + str(j))
  print"6- The Drainage depth Dr"+ str(j)+ " has been computed successfully"

  ## #7-exc= Excess water rainfall (accum rain depth- ETD evapotranspiration), exc= the Net accu. depth in (cm.) on the surface
  AcRain=AcRain+p*(t-to)
  exc=Con(AcRain-fd>=0,Con((AcRain-fd-Ev*(t-to))>=0,(AcRain-fd-Ev*(t-to)),AcRain-fd),AcRain)
  exc=Con(AcRain-fd>=0,Con((AcRain-fd-Ev*(t-to))>=0,(AcRain-fd-Ev*(t-to)),AcRain-fd),AcRain)
  exc.save(outpath + "\\exc"+ str(j))
  print"7-a The net accu. excess depth (cm)on the surface  exc"+ str(j)+ " has been computed successfully"
  excm= exc/100
  excm.save(outpath + "\\excm"+ str(j))
  print" -b The net accu. excess depth (m)on the surface  excm"+ str(j)+ " has been computed successfully" 
  
  ## #8-vol= total volume of the Excess rainfall (excess depth * zone area  in (m3.) on the surface
  vzone=Con(watermask3==0,exc*703/100,Con(watermask3==1,exc*3062/100,Con(watermask3==2,exc*2998/100)))
  vzone.save(outpath + "\\vzone"+ str(j))
  print"8-a The net accu. zone excess volume on the surface vzone"+ str(j)+ " has been computed successfully"

  # Execute ZonalStatistics
  Vol = ZonalStatistics("D", "value", "excm"+ str(j), "SUM","NODATA")
  WaElev=Vol/6578.0+ minElevation
  #Volume=Vol
  #print"Vol=",Vol, "WaElev=",WaElevarc
  
  # Save the output
  Vol.save(outpath + "\\Vol"+ str(j))
  print" -b The (Vol) total excess volume in m3 for the wetland has been computed successfully"

  #p_v.append(Volume)
  WaElev.save(outpath + "\\WaElev"+ str(j))
  print" -c The (WaElev)Water Elevation level in the Wetland has been computed successfully"
    
    
  ## 9-p-wa= Extracting Surface water elevation in a list form
  Elevation=Times("WaElev"+str(j),1000)

  # take integer of the elevation in mm
  outInt=Int(Elevation)
  # Save the output
  outInt.save(outpath + "\\outInt"+ str(j))
  
  #############################################################
  #Search cursor
  fcc = outpath+ "\\"+ "outInt"+str(j)
  field = "Value"
  rows = arcpy.SearchCursor(fcc)
  for row in rows:
     p_wa.append(float(row.getValue(field))/1000)
  
  del rows
  del row
  ############################################################# 
  print"9- The(p_wa)Surface Water Elevation has been extracted into a list form successfully"
  to=t
##  print"------------------------------------------------------------------------------------"
##  print ""
##print" All infilitration, Evapotranspiration, Drainage, Excess Rainfall components have been completed and created successfuly"
##print"#########################################################################################################################"
##print"Potential Water Surface Elevation at Pershing State Park Wetland as follows"
##
### to upadte the lists to be drawn form t=0 instead of t=1 , use the following functions
##p_t.insert(0,0)              # to insert the value of 0 in the index 0 in P_t
##p_wa.insert(0,minElevation) # to insert the value of minElevation in the index 0 in P_min
###p_v.insert(0,0) # to insert the value of maxElevation in the index 0 in P_max
##
##for i in range (0,num+1,1):
##    print "time(hrs.)=",p_t[i],"; Surface Water Elevation (m.)=",p_wa[i]


##############################################################################################################################
##
########Ploting the Water surface Elevation over time #########
### step1-for each ploting
##import numpy as np                 
##import matplotlib.pyplot as plt
##
###step 1-numpy to store the data in array
##
###step-2 setup plots
##plt.plot(p_t,p_wa,'bo-',label='Potentail Surface water Elevation') # adding the x-axis with y-axies array
##plt.plot(p_t,p_min,'r--',label='Minimum Potentail Surface water Elevation') # adding the x-axis with y-axies array
##plt.plot(p_t,p_max,'m--',label='Maximum Potentail Surface water Elevation') # adding the x-axis with y-axies array
##
###plt.plot(p_t,prim_s,'r^-',label='Water Volume ')
##plt.ylim(216.20,217.20)
##
### to add the legend defind previoulsy
##plt.legend()                                  
##plt.xlabel('Time in hours')
##plt.ylabel('Water Surface Elevation in meters')
##plt.title('Water Profile at wetland based on Green&Ampt Infiltration Model')
##
### fancy stuff
##plt.grid()  # you can write alpha inside the paranthisis to show the darkness
##plt.fill_between(p_t,p_wa,color='m',alpha=0.1)  # alpha to show the darkness value
###plt.fill_between(p_t,prim_f,color='r',alpha=0.3)
##
###step-4 now, make the plot already
##plt.show()

