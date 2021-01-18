# -*- coding: utf-8 -*-
import arcpy 
from arcpy import env
import os, sys, math
import string
import numpy
from arcpy.sa import *
from numpy import inf
 
#setup environment
#env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\Papers\\infiltration\\Paper3_Raster"
env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\\Data_Weather\\linn\\Paper3Raster.gdb"
#env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\\Reports\\Nov.2017\\Outputs"
outpath=env.workspace
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
#arcpy.BuildPyramidsandStatistics_management(arcpy.env.workspace)

##### delete the existing raster data from preivous run
##inRaster = outpath + "\\" + "infi" +str()
##if arcpy.Exists(inRaster):
##    arcpy.Delete_management(inRaster)
##os.makedirs(inRaster)
##
##### delete the existing raster data from preivous run
##inRaster = outpath + "\\" + "Evapot"+str()
##if arcpy.Exists(inRaster):
##    arcpy.Delete_management(inRaster)
##os.makedirs(inRaster)
##
##### delete the existing raster data from preivous run
##inRaster = outpath + "\\" + "Wco"+str()
##if arcpy.Exists(inRaster):
##    arcpy.Delete_management(inRaster)
##os.makedirs(inRaster)
##
##### delete the existing raster data from preivous run
##inRaster = outpath + "\\" + "Drai"+str()
##if arcpy.Exists(inRaster):
##    arcpy.Delete_management(inRaster)
##os.makedirs(inRaster)

print"#######################################################################################################################"
print"|The Spatail&Temporal Wetland Water Elevations and Volumes based on GREEN-AMPT Infiltration & Evapotranspiration Models|"
print"#######################################################################################################################"
print ""

################
#Local variables
#p= [0.4,0.42,0.45,0.5,0.4,0.3,0.27,0.15,0.0,0,0.0,0.3,0.4,0.5,0.45,0.2,0.05,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
#p= [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.254,0.0,0.0,0.0,0.0,0.254,0.254,0.0,0.254,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

#################################################################################
### Read the rainfall Data  from the text file-long time period from this option.
#################################################################################


timestep=1
p=[]
with open('F:\\MissouriDo\\GeneralSearch\\EPA\Papers\\infiltration\\Paper3_Raster\\Inputs\\Rain2new.txt', 'r') as f:
    data0 = f.readlines()                        #read all data from text file  
    for line in data0:  
        odom0 = line.split()                     #seperate all single data  
        numbers_float = map(float, odom0)        #convert number to float
        #for n in range(1, int(3600/tim)):
        p.append(numbers_float[0]/1/timestep)
print ("rainfall data has been read successfully from the text file") 

### Local time Data can be read in case of long time period from this option.
#################################################################################
###Read the Local Time from a text Ltime.txt file 
#################################################################################
Ltime=[]
with open('F:\\MissouriDo\\GeneralSearch\\EPA\Papers\\infiltration\\Paper3_Raster\\Inputs\\Ltime.txt', 'r') as ff:  
    data1 = ff.readlines()                       #read all data from text file  
    for line in data1:  
        odom1 = line.split()                     #seperate all single data  
        numbers_float = map(float, odom1)        #convert number to float
        Ltime.append(numbers_float[0]/timestep)
print ("Local time data has been read successfully from the text file") 

#################################################################################
###Read the Evaporanspiration from a text ET12.txt file 
#################################################################################

##ET=[]
##with open('F:\\MissouriDo\\GeneralSearch\\EPA\Papers\\infiltration\\Paper3_Raster\\Inputs\\ET12.txt', 'r') as fff:  
##    data2 = fff.readlines()                     #read all data from text file  
##    for line in data2:  
##        odom2 = line.split()                     #seperate all single data  
##        numbers_float = map(float, odom2)        #convert number to float
##        ET.append(numbers_float[0]/timestep)
##print ("Evapotraspiration data has been read successfully from the text file")

#################################################################################
###Read the Evaporanspiration from a text kco.txt file 
#################################################################################

kco=[]
with open('F:\\MissouriDo\\GeneralSearch\\EPA\Papers\\infiltration\\Paper3_Raster\\Inputs\\kco.txt', 'r') as ff:  
    data = ff.readlines()                     #read all data from text file  
    for line in data:  
        odom = line.split()                     #seperate all single data  
        numbers_float = map(float, odom)        #convert number to float
        kco.append(numbers_float[0]/timestep)
print ("kco data has been read successfully from the text file")

#################################################################################
###Read the PET from a text PET.txt file 
#################################################################################

PET=[]
with open('F:\\MissouriDo\\GeneralSearch\\EPA\Papers\\infiltration\\Paper3_Raster\\Inputs\\PET.txt', 'r') as ff:  
    data = ff.readlines()                     #read all data from text file  
    for line in data:  
        odom = line.split()                     #seperate all single data  
        numbers_float = map(float, odom)        #convert number to float
        PET.append(numbers_float[0]/timestep)
print ("PET data has been read successfully from the text file")

#################################################################################
###Read the Direct Evaporation from a text Ev12.txt file 
#################################################################################

Ev=[]
with open('F:\\MissouriDo\\GeneralSearch\\EPA\Papers\\infiltration\\Paper3_Raster\\Inputs\\Ev12.txt', 'r') as ff:  
    data = ff.readlines()                     #read all data from text file  
    for line in data:  
        odom = line.split()                     #seperate all single data  
        numbers_float = map(float, odom)        #convert number to float
        Ev.append(numbers_float[0]/timestep)
print ("Evaporation data has been read successfully from the text file")
#################################################################################
to=0.0
t=to
watermask3=1 # ENTER watermask=0  for Aspen Vege., and ENTER watermask= 1 for Miscell. vege., and ENTER watermask=2 for bare (no vegetation)
fd=0.0
ETd=0.0
#ETdd0=0.0
wp=0.11              #wp= Willting point 
D=20                 # D=root zone 20 cm
minElevation=216.320 # minimum elevation from DEM 1 meter resolution
maxElevation=216.964 # maximum elevation from Dem 1 meter resolution
phead=27.3
ks=0.10
wci=0.27             # for Apin =0.25; Grass=0.27; and Bare=0.3
wc=wci
wcs=0.432
fc=0.34
exc=0.0
dw=0.0
#Dr=0.0 # this value is replaced by 0.10 which is =ks  Case1 and =0.01 for Case 2
Dr=0.10
AcRain=0.0
excm=0.0
fdp=0.0    # the initial cmulative infiltration depth for the previous time step
ETdp=0.0   # the initial cmulative evapotranspiration depth for the previous time step
Drp=0.0    # the initial cmulative draingaed depth for the previous time step
#Vol1=Raster("Vol1")
Mask=Raster("Mask")
Wco=Raster("Mask")

#################################################################################
##Create the Lists  and the time for running the script num
#################################################################################
#num=10*24      # Enter the total time in num (day) to run the script here
num=len(p)      # num represnts the total duraion based on p text files's values
################################################################################

p_t=[]
p_v=[]
p_wa=[]
Elevation=0.0
p_min=[216.320,]*num    # enter the minimum Elevation in the DEM raster of the Site 
p_max=[216.964,]*num    # enter the maximum Elevation in the DEM raster of the Site

#################################################################################
# Creating empty lists
#################################################################################

frate=[]
fdd=[]
ETdd=[0,]
ET=[]
dww=[]
wcc=[]
Drr=[]
AcRainn=[]
excc=[]  # culalative excess
excmm=[]
vzonee=[]
Voll=[]
WaElevv=[]
outIntt=[]
Fpp=[]
tpp=[]

#################################################################################
####### delete the existing Fp
##inRaster = outpath + "Fp"
##if arcpy.Exists(inRaster):
##    arcpy.Delete_management(inRaster)
##os.makedirs(inRaster)
#################################################################################

#Fp   # enter this value Fp in case the of constant rainfall or for the first value
Fp=phead*ks*(wcs-wci)/(p[0]-ks)
Fp=Con(Fp>0,Fp,0)
print ("Fp intial="),Fp
Fpi=Fp
po=Con(p[0]>0,p[0],0.001)  # to ensure non zero value that may led to infinity
tp=Fp/po
tp=Con(tp>0,tp,0)
print ("tp intial="),tp
tpi=tp
dfc=phead*ks*(wcs-wci)/(0.254-ks)  # can be used when p>ks  based on GreenAmpt principle. The 0.254 is the first p>ks
print "3- The(dfc)depth of water has been computed"
print ""
print"------------------------------------------------------------"

############################################################################
##Iteraion through the time increment 1 hr. to compute f_rate in cm/hr.
############################################################################
for j in range (1,num,1):
  t=j/1.00
  p_t.append(t)     # t wetland clock  global time
  print"iteration time step t in hrs.=",t
  Lt=Ltime[j]       # read the strom clock local time from the text file Ltime.txt and the associated  Ltime list
  print "p=",p[j]

  #Read the value for daily Evaportraspiration based on the comparison
  if (j<=758):
      kc=kco[0] ; PETT=PET[0] 
  if (j>758 and j<=1478):
      kc=kco[1] ; PETT=PET[1] 
  if (j>1478 and j<=2222):
      kc=kco[2] ; PETT=PET[2] 
  if (j>2222 and j<=2942):
      kc=kco[3] ; PETT=PET[3] 
  if (j>2942 and j<=3686):
     kc=kco[4] ; PETT=PET[4] 
  if (j>3686  and j<=4430):
      kc=kco[5] ; PETT=PET[5] 
  if (j>4430 and j<=5102):
      kc=kco[6] ; PETT=PET[6] 
  if(j>5102 and j<=5846):
      kc=kco[7] ; PETT=PET[7] 
  if (j>5846 and j<=6566):
     kc=kco[8] ; PETT=PET[8] 
  if (j>6566  and j<=7310):
     kc=kco[9] ; PETT=PET[9] 
  if (j>7310  and j<=8030):
     kc=kco[10];  PETT=PET[10] 
  elif (j>8030 and j<=8774):
     kc=kco[11] ; PETT=PET[11] 
     #kc=kco[0] ; PETT=PET[0]
     
  ###################################

  if (j<=758):
    Evv=Ev[0] 
  if (j>758 and j<=1478):
    Evv=Ev[1] 
  if (j>1478 and j<=2222):
     Evv=Ev[2]  
  if (j>2222 and j<=2942):
    Evv=Ev[3]  
  if (j>2942 and j<=3686):
    Evv=Ev[4]  
  if (j>3686  and j<=4430):
    Evv=Ev[5]  
  if (j>4430 and j<=5102):
    Evv=Ev[6]  
  if (j>5102 and j<=5846):
    Evv=Ev[7]  
  if (j>5846 and j<=6566):
    Evv=Ev[8] 
  if (j>6566  and j<=7310):
     Evv=Ev[9] 
  if (j>7310  and j<=8030):
    Evv=Ev[10] 
  elif (j>8030 and j<=8774):
     Evv=Ev[11] 
  print "j=",j,"Evv=",Evv,"kc=",kc,"PETT=",PETT
    
  ########################################################################################################################
  ########################################################################################################################
  ## # 1-Process: Raster Calculator estimtaed f_rate based on power equation from GreenAmpt Equation in f_rate in (cm./hr)

  f_rate= Con(watermask3==0,0.4366*Lt**(-0.261),Con(watermask3==1,0.406*Lt**(-0.252),0.3566*Lt**(-0.233)))
  
  ## to update the infilitration ratef_rate.save(outpath + "\\f_rate"+ str(j))
  ##  f_rate= Con(t <= tp,Con((p[j]>0) | (exc>= f_rate*(t-to)),p[j],0),Con((p[j]>0) | (exc>= f_rate*(t-to)),f_rate,0))
  f_rate= Con(Lt <= tp,Con((p[j]>0) | (exc>= f_rate*(t-to)),p[j],0),Con((p[j]>0) | (exc>= f_rate*(t-to)),min(f_rate,p[j]),0)) 
  print "f_rate=",f_rate
  #f_rate.save(outpath + "\\f_rate" + str(j))
  frate.append(f_rate)
  print "1- The infiltration f_rate"+ str(j)+ " has been computed successfully"

  ##  infi=Con(Mask==0,f_rate )                #Create Raster data for infiltartion 
  ##  infi.save(outpath + "\\infi" + str(j))
  # p=Con((t<=7)|((t>=11) &(t<=16)),0.5,0)

  infi=Con(Mask==0,f_rate)               #Create Raster data for infiltartion 
  infi.save(outpath + "\\f" + str(j))

  ## ## # 2- compute fd in (cm.), the acumalated infiltrated depth in the soil
  fd=Con((t>0),(fd+(f_rate*(t-to))),0.0)  # the incremental time 3600 sec= 1 hr
  #fd.save(outpath + "\\fd" + str(j))
  fdd.append(fd)
  print"2- The accu.infiltration depth fd"+ str(j)+ " has been computed successfully"

  ## ## #3- ETd accumuated evapotranspiration  depth in cm, ET for Aspen =0.0157,Evapotranspiration for Miscellaneuos =0.0118, for Bare zone evaportaion 0.0191 (cm/hr)
  #ETd=Con(p[j]==0,Con(wc<=wp,ETd,Con(watermask3==0,ETd+(kco*PET/4.61512)*Ln(434.7826*(wc-wp)+1)*(t-to)/24,Con(watermask3==1,ETd+(kco*PET/4.61512)*Ln(434.7826*(wc-wp)+1)*(t-to)/24,Con((watermask3==2) & (wc<fc),ETd,ETd+Ev*(t-to)/24)))),ETd)
  Et0=(kc*PETT/4.61512)*Ln(434.7826*(wc-wp)+1)
  Et1=(kc*PETT/4.61512)*Ln(434.7826*(wc-wp)+1)
  Et2=Evv
  print "j=",j,"Et0=",Et0,"Et1=",Et1,"Et2=",Et2
  ETd=Con(p[j]==0,Con(wc<=wp,ETd,Con(watermask3==0,ETd+Et0*(t-to)/24,Con(watermask3==1,ETd+Et1*(t-to)/24,Con((watermask3==2) & (wc<fc),ETd,ETd+Et2*(t-to))))),ETd)
  #ETd.save(outpath + "\\ETd" + str(j))
  ETdd.append(ETd)
  print"3- The accu.evapotranspiration depth ETd"+ str(j)+ " has been computed successfully"

  dET=ETdd[j]-ETdd[j-1]

  Evapot = Con(Mask==0,dET)  #Create Raster data for water content 
  Evapot.save(outpath + "\\ET" + str(j))

  ## ## #4- fd-ETd= dw is the accumuated ifilitration- evapotranspiration  depth in (cm.)
  ##dw=fd-ETd  ## this valued has been updated
  dw=fd-ETd-Drp
  
  #dw.save(outpath + "\\dw" + str(j))
  dww.append(dw)
  print"4- The accu.(infilitraion - evapotranspiration) depth dw"+ str(j)+ " has been computed successfully"
  
  ## #5-wc= water content at the end of time step =[wci+(dw/dfc)*(fc-wci)]
  ##wc=Con((wci+(dw/dfc)*(fc-wci))<=wp,wp,Con((wci+(dw/dfc)*(fc-wci))<fc,(wci+(dw/dfc)*(fc-wci)),fc))# the fc replaced by wcs
  wc=Con((wci+(dw/dfc)*(wcs-wci))<=wp,wp,Con((wci+(dw/dfc)*(wcs-wci))<wcs,(wci+(dw/dfc)*(wcs-wci)),wcs))
             
  #wc.save(outpath + "\\wc"+ str(j))
  wcc.append(wc)
  print"5- The (wc) water content spatially  wc"+ str(j)+ "  has been computed successfully" 

  ##  Wco=Con(Mask==0,wc)              #Create Raster data for water content 
  ##  Wco.save(outpath + "\\Wco" + str(j))

  Wco=Con(Mask==0,wc)                   #Create Raster data for water content 
  Wco.save(outpath + "\\WC" + str(j))
  
  ## ## #6- Dr-Drainage ( water depth that exceeds the field capacity Fc in (cm.)
  #Dr=Con(wc>=fc,dw-(fc-wc)*D,0)
  ##Dr=Con(wc>=fc,Con((((fd-fdp)-(ETd-ETdp))>0),((fd-fdp)-(ETd-ETdp)+Drp),Drp),Drp) # this has been updated below
  Dr=Con(wc>fc,0.10,0)
  Drp=Drp+Dr
  #Dr.save(outpath + "\\Dr" + str(num))
  Drr.append(Dr)
  print"6- The Drainage depth Dr"+ str(j)+ " has been computed successfully"
  fdp=fd     # the cmulative infiltration depth for the previous time step
  ETdp=ETd   # the cmulative evapotranspiration depth for the previous time step
  ##Drp=Dr     # the cmulative drainged depth for the previous time step## this step has been updated

  Drai=Con(Mask==0,Dr)                  #Create Raster data for water content 
  Drai.save(outpath + "\\DR" + str(j))
  print " infi, Evapot, Wco, and Drai convetred into a raster format at t=",j
  
  ## #7-exc= Excess water rainfall (accum rain depth- ETD evapotranspiration), exc= the Net accu. depth in (cm.) on the surface
  AcRain=AcRain+p[j]*(t-to)
  AcRainn.append(AcRain)
  #exc=Con(AcRain-fd>=0,Con((AcRain-fd-Ev*(t-to))>=0,(AcRain-fd-Ev*(t-to)),AcRain-fd),AcRain)
  ##exc=Con(AcRain-fd>=0,Con((AcRain-fd-Et2*(t-to))>=0,(AcRain-fd-Et2*(t-to)),AcRain-fd),exc)## has been updated

  pr=p[j]
  fr=f_rate
  Evu=Con(pr==0,Evv,0) # this is to neglect Ev during rain
  ex=Con(wc==wcs,Con((pr-fr-Evu)>0,(pr-fr-Evu),(pr-fr)),0)  # ex is the excess rate
  exc=exc+ex

  #exc.save(outpath + "\\exc"+ str(j))
  excc.append(exc)
  print"7-a The net accu. excess depth (cm)on the surface  exc"+ str(j)+ " has been computed successfully"
  excm= exc/100
  #excm.save(outpath + "\\excm"+ str(j))
  excmm.append(excm)
  print" -b The net accu. excess depth (m)on the surface  excm"+ str(j)+ " has been computed successfully" 
  
  ## #8-vol= total volume of the Excess rainfall (excess depth * zone area  in (m3.) on the surface
  #vzone=Con(watermask3==0,exc*703/100,Con(watermask3==1,exc*3062/100,Con(watermask3==2,exc*2998/100)))
  vzone=Con(watermask3==0,exc*703/100,Con(watermask3==1,exc*3062/100,Con(watermask3==2,exc*2998/100,0)))
  #vzone.save(outpath + "\\vzone"+ str(j))
  #vzone=100
  vzonee.append(vzone)
  print"8-a The net accu. zone excess volume on the surface vzone"+ str(j)+ " has been computed successfully"

  # Execute ZonalStatistics
  #Vol = ZonalStatistics("D", "value", "excm"+ str(j), "SUM","NODATA")
  Vol=vzone
  #WaElev=Vol/6578.0+ minElevation #Total zone
  #WaElev=Vol/703.0+ minElevation  # Aspin Zone
  #WaElev=Vol/3062.0+ minElevation  # Grass zone
  WaElev=Vol/5805.0+ minElevation  # Grass zone for the whole watershed area
  # Save the output
  #Vol.save(outpath + "\\Vol"+ str(j))
  Voll.append(Vol)
  print" -b The (Vol) total excess volume in m3 for the wetland has been computed successfully"

  #p_v.append(Volume)
  #WaElev.save(outpath + "\\WaElev"+ str(j))
  WaElevv.append(WaElev)
  print" -c The (WaElev)Water Elevation level in the Wetland has been computed successfully"
    
  ## #9-p-wa= appending Surface water elevation in a list form
  p_wa.append(WaElev)
  print"9- The(p_wa)Surface Water Elevation has been extracted into a list form successfully"
  to=t
  print"------------------------------------------------------------------------------------"
  print ""
  # FP=phead*Ks(wcs-wci)/(p-ks), Fp = the accu. depth of water at ponding in (cm.)
  Fp=phead*ks*(wcs-wc)/(p[j]-ks)
  Fp=Con(Fp>0,Fp,0.0)
  print ("Fp="),Fp,("phead="),phead,("ks="),ks,("wcs="),wcs,("wci="),wc,("p="),p[j]
  #Fp.save(outpath + "\\Fp")
  Fpp.append(Fp)
  print"1- The(FP)accu. infiltrated depth has been computed successfully"

  # tp= Fp/p ,tp= The(tp)time up to ponding in (hrs.)
  if p[j]>0:
     tp=Fp/p[j]
  #tp=Con(p[j]>0.0,Fp/p[j],0.0)
  else:
      tp=0.0
  print ("tp="),tp
  #tp.save(outpath + "\\tp")
  tpp.append(tp)
  print"2- The(tp)time up to ponding has been computed successfully "

print" All infilitration, Evapotranspiration, Drainage, Excess Rainfall components have been completed and created successfuly"
print"#########################################################################################################################"
print"Potential Water Surface Elevation at Pershing State Park Wetland as follows"

# to upadte the lists to be drawn form t=0 instead of t=1 , use the following functions
p_t.insert(0,0)              # to insert the value of 0 in the index 0 in P_t
p_wa.insert(0,minElevation) # to insert the value of minElevation in the index 0 in P_min
#p_v.insert(0,maxElevation) # to insert the value of maxElevation in the index 0 in P_max
frate.insert(0,p[0])
fdd.insert(0,0)
#ETdd.insert(0,0)
dww.insert(0,0)
wcc.insert(0,wci)
Drr.insert(0,0)
AcRainn.insert(0,0)
excc.insert(0,0)
excmm.insert(0,0)
vzonee.insert(0,0)
Voll.insert(0,0)
WaElevv.insert(0,minElevation)
outIntt.insert(0,0)
Fpp.insert(0,Fpi)
tpp.insert(0,tpi)

#to set initial values for raster fomat
infi=Con(Mask==0, p[0])  # set the initial value for infilitrartion
infi.save(outpath + "\\infi" +str(0))
Wco=Con(Mask==0,wci)   # set the initial value for water content
Wco.save(outpath + "\\Wco" +str(0))
Evap=Con(Mask==0,0.0)  # set the initial value for ET
Evap.save(outpath + "\\Evap" +str(0))
Drai=Con(Mask==0, 0.0)  # set the initial value for ET
Drai.save(outpath + "\\Drai" +str(0))

for i in range (0,num,1):
    print "time(hrs.)=",p_t[i],"; Surface Water Elevation (m.)=",p_wa[i]

print""
print("_______________________________________________")
print("The infiltration rate f (cm/hrs.)is as follows:")
for i in range (0,len(frate),1):
	print("{0:.5f}".format(frate[i]))," t=",p_t[i]

###########################################################
#### compute ET rate in new matrix based on ETdd
###########################################################
for j in range (1,num,1):
  t=j/1.00
  ET_rate=ETdd[j]-ETdd[j-1]  # to save the ET rate in separate matrix
  ET.append(ET_rate)
print"3- The evapotranspiration rate ET"+ str(j)+ " has been computed successfully"
  

###########################################################
#### write the infiltration data into a text file.txt
###########################################################
import arcpy
from arcpy import env
import os, sys, math
env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\\Papers\\infiltration\\Paper3_Raster\\Outputs"
outpath = env.workspace
def writetofile():
    outputname=outpath+"\\" + "f_rate.txt "
    aa=frate

    #for i in range (0,len(aa),1):
    myfile=open(outputname,'w')
    myfile.write(str(aa)+'\n')
    #myfile.write(str(aa[i])+'\n')
    #print("frate","{0:.3f}".format(frate))
    myfile.close()
    #check the average .ext file has been populated
    if os.stat(outputname).st_size>0:
       print("f_rate.txt file has been poplated")
    else:
      print ("The output file is ampty, you need to check")
writetofile()

###########################################################
#### write the ET data into a text file.txt
###########################################################
import arcpy
from arcpy import env
import os, sys, math
env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\\Papers\\infiltration\\Paper3_Raster\\Outputs"
outpath = env.workspace
def writetofile():
    outputname=outpath+"\\" + "ET_rate.txt "
    bb=ET
    #for i in range (0,len(aa),1):
    myfile1=open(outputname,'w')
    myfile1.write(str(bb)+'\n')
    #myfile.write(str(aa[i])+'\n')
    #print("frate","{0:.3f}".format(frate))
    myfile1.close()
    #check the average .ext file has been populated
    if os.stat(outputname).st_size>0:
       print("ET_rate.txt file has been poplated")
    else:
      print ("The output file is ampty, you need to check")
writetofile()

###########################################################
#### write the WC data into a text file.txt
###########################################################
import arcpy
from arcpy import env
import os, sys, math
env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\\Papers\\infiltration\\Paper3_Raster\\Outputs"
outpath = env.workspace
def writetofile():
    outputname=outpath+"\\" + "Wc.txt "
    cc=wcc
    #for i in range (0,len(aa),1):
    myfile1=open(outputname,'w')
    myfile1.write(str(cc)+'\n')
    #myfile.write(str(aa[i])+'\n')
    #print("frate","{0:.3f}".format(frate))
    myfile1.close()
    #check the average .ext file has been populated
    if os.stat(outputname).st_size>0:
       print("Wc.txt file has been poplated")
    else:
      print ("The output file is ampty, you need to check")
writetofile()
###########################################################
###convertig Vecor to Raster fomat
###########################################################
##env.workspace="F:\\MissouriDo\\GeneralSearch\\EPA\\Data_Weather\\linn\\Paper3Raster.gdb"
##outpath=env.workspace
##for j in range (1,num,1):
##  infi=Con(Mask==0,frate[j] )               #Create Raster data for infiltartion 
##  infi.save(outpath + "\\infi" + str(j))
##  Evapot = Con(Mask==0, ETdd[j]-ETdd[j-1])  #Create Raster data for water content 
##  Evapot.save(outpath + "\\Evapot" + str(j))
##  Wco=Con(Mask==0,wcc[j])                   #Create Raster data for water content 
##  Wco.save(outpath + "\\Wco" + str(j))
##  Drai=Con(Mask==0,Drr[j])                  #Create Raster data for water content 
##  Drai.save(outpath + "\\Drai" + str(j))
##  print " infi, Evapot, Wco, and Drai convetred into a raster format at t=",j
  
###########################################################
####Ploting the Water surface Elevation over time 
###########################################################
# step1-for each ploting
import numpy as np                 
import matplotlib.pyplot as plt

#step 1-numpy to store the data in array

#step-2 setup plots
plt.plot(p_t,p_wa,'b-',label='Potential Water Surface Elevation') # adding the x-axis with y-axies array
plt.plot(p_t,p_min,'r--',label='Minimum Water Surface Elevation') # adding the x-axis with y-axies array
plt.plot(p_t,p_max,'g--',label='Maximum Water Surface Elevation') # adding the x-axis with y-axies array
##plt.plot(p_t,prim_s,'r^-',label='Water Volume ')
plt.ylim(216.20,217.80)
# to add the legend defind previoulsy
plt.legend()                                  
plt.xlabel('Time (hrs.)')
##plt.ylabel('Water Surface Elevation in meters')
plt.title('The Annual Predicated Water Elevation at the Wetland')
plt.ylabel('Water Surface Elevation (m)')
# fancy stuff
plt.grid()  # you can write alpha inside the paranthisis to show the darkness
plt.fill_between(p_t,p_wa,color='m',alpha=0.1)  # alpha to show the darkness value

#step-4 now, make the plot already
plt.savefig("Elevation_1.png")
plt.show()
#plt.savefig("g3.pdf")

##########################################################
#### Infiltration rate graph over time
##########################################################
plt.plot(p_t,frate,'m--',label='Infiltration Rate cm/hr.') # adding the x-axis with y-axies array
plt.ylim(0,2)
plt.legend()
plt.title('The Annual Infiltration by Green-Ampt Model')
plt.xlabel('Time (hrs.)')
plt.ylabel('Infiltration Rate (cm/hr.)')
plt.grid()
plt.fill_between(p_t,frate,color='r',alpha=0.3)                     
##y=p
##x=range(len(p))
##plt.bar(x,y,color="blue")
#width=1/1.5
plt.savefig("infiltration_1.png")
plt.show()

############################################################
###### Water Volume graph over time
############################################################
##plt.plot(p_t,Voll,'m--',label='Water Volume (m3)') # adding the x-axis with y-axies array
###plt.ylim(0,2)
##plt.legend()
##plt.title('The Annual Wetland Water Volume')
##plt.xlabel('Time (hrs.)')
##plt.ylabel('Water Volume (m3)')
##plt.grid()
##plt.fill_between(p_t,Voll,color='r',alpha=0.3)                     
####y=p
####x=range(len(p))
####plt.bar(x,y,color="blue")
###width=1/1.5
##plt.savefig("Volume_1.png")
##plt.show()

############################################################
###### Accumulated Volume graph over time
############################################################
plt.plot(p_t,fdd,'m--',label='Acc.Infiltrated Depth (cm)') # adding the x-axis with y-axies array
plt.plot(p_t,ETdd,'r--',label='Acc.Evapotraspirated Depth (cm)') # adding the x-axis with y-axies array
plt.plot(p_t,Drr,'b--',label='Acc.Drainage depth (cm)') # adding the x-axis with y-axies array
plt.plot(p_t,AcRainn,'y--',label='Acc.Rained depth (cm)') # adding the x-axis with y-axies array
plt.plot(p_t,excc,'g--',label='Acc.Excessed depth (cm)') # adding the x-axis with y-axies array
#plt.ylim(0,2)
plt.legend()
plt.title('The Annual Infiltrated,Evapotranspirated,Rained,Drainage,Excessed Depthes')
plt.xlabel('Time (hrs.)')
plt.ylabel('Water depthes (cm)')
plt.grid()
plt.fill_between(p_t,fdd,color='y',alpha=0.3)                     
##y=p
##x=range(len(p))
##plt.bar(x,y,color="blue")
#width=1/1.5
plt.savefig("Accu.f_Et_Dr_P_Ev1.png")
plt.show()

##########################################################
#### water content over time
##########################################################
plt.plot(p_t,wcc,'m--',label='Volumetric Water Content ') # adding the x-axis with y-axies array
plt.ylim(0,2)
plt.legend()
plt.title('The Annual Water Content')
plt.xlabel('Time (hrs.)')
plt.ylabel('% Water Content')
plt.grid()
plt.fill_between(p_t,wcc,color='b',alpha=0.3)                     
##y=p
##x=range(len(p))
##plt.bar(x,y,color="blue")
#width=1/1.5
plt.savefig("WaterContent_1.png")
plt.show()
