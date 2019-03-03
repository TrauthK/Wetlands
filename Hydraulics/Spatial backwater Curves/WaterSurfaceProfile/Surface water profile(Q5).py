import math
import arcpy
from arcpy import env
import os, sys, math
import numpy

#setup environment
env.workspace = r'H:\Euler method comperison'
outpath = env.workspace

#Refresh gp object and permit overwriting
arcpy.env.overwriteOutput = True

#Remove problematic files
if os.path.exists("schema.ini"):
    os.remove("schema.ini")

#input FC
inFC1 = outpath + "\\" + "third.shp"
inFC2 = outpath + "\\" + "second.shp"
inFC3 = outpath + "\\" + "first.shp"
field = "GRID_CODE"


##### Process: Create Table
##arcpy.CreateTable_management(outpath, "channelP.dbf", "", "")
##results = outpath + "\\channelP.dbf"
##
##### Add fields
##arcpy.AddField_management(results, "step", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##arcpy.AddField_management(results, "height", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##arcpy.AddField_management(results, "elevation", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##arcpy.AddField_management(results, "area", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##arcpy.AddField_management(results, "width", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##arcpy.AddField_management(results, "wparameter", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
##arcpy.AddField_management(results, "hydraulicR", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")


Q =5
cellsize=1/1.3
n = 0.025   ##
s = 0.003612  ##
y0 = 0.3##
channelL=76.35
x=[0, 0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6, 0.8, 1]
for i in range(2,78):
    x.append(i)
WaterSur=0
min = 227.5241

for num in range(0,len(x)-1):
    WaterSur = min+(x[num]-x[0])*s + y0
    rows = arcpy.da.SearchCursor(inFC3, field)
    A1 = 0
    width = 0
    P1 = 0
    R1 = 0
    B1 = 0
    temp = 0
    temp = WaterSur
    for row in rows:
        
        val = float(row[0])-(227.64679 -min)+(x[num]-x[0])*s
        if val < WaterSur:

            A1 = A1 + (WaterSur - val)*cellsize
            B1 = B1 + cellsize
            P1=P1+math.sqrt((temp-val)**2+ cellsize**2)
            temp = val
            R1 = A1/P1
    
    print   WaterSur
    yi = y0
    V=Q/A1
    Se= (n**2)*(V**2)/(R1**1.333)
    F2= (V**2)*B1/9.81/A1
    fy1= (s-Se)/(1-F2)
    y2p= y0+(fy1*(-x[num+1]+x[num]))
    del rows
    del row

    WaterSur = min+(x[num]-x[0])*s + y2p
    rows = arcpy.da.SearchCursor(inFC3, field)
    A2 = 0
    width = 0
    P2 = 0
    R2 = 0
    B2 = 0
    temp = 0
    temp = WaterSur
    for row in rows:
        
        val = float(row[0])-(227.64679 -min)+(x[num]-x[0])*s
        if val < WaterSur:

            A2 = A2 + (WaterSur - val)*cellsize
            B2 = B2 + cellsize
            P2=P2+math.sqrt((temp-val)**2+ cellsize**2)
            temp = val
            R2 = A2/P2
    V= Q/A2
    Se=(n**2)*(V**2)/(R2**1.333)
    F2= (V**2)*B2/9.81/A2
    fy2= (s-Se)/(1-F2)
    
    y0= y0+((fy1+fy2)/2*(-x[num+1]+x[num]))
    del rows
    del row
print "###################"
min = min+channelL*s
s = 0.004672  ##
cellsize=1/1.41
y0 = yi
n=0.05
print min,y0

for num in range(0,len(x)-1):
    WaterSur = min+(x[num]-x[0])*s + y0
    rows = arcpy.da.SearchCursor(inFC2, field)
    A1 = 0
    width = 0
    P1 = 0
    R1 = 0
    B1 = 0
    temp = 0
    temp = WaterSur
    for row in rows:
        
        val = float(row[0])-(227.961792 -min)+(x[num]-x[0])*s
        if val < WaterSur:

            A1 = A1 + (WaterSur - val)*cellsize
            B1 = B1 + cellsize
            P1=P1+math.sqrt((temp-val)**2+ cellsize**2)
            temp = val
            R1 = A1/P1
    
    print   WaterSur
    yi = y0
    V=Q/A1
    Se= (n**2)*(V**2)/(R1**1.333)
    F2= (V**2)*B1/9.81/A1
    fy1= (s-Se)/(1-F2)
    y2p= y0+(fy1*(-x[num+1]+x[num]))
    del rows
    del row

    WaterSur = min+(x[num]-x[0])*s + y2p
    rows = arcpy.da.SearchCursor(inFC2, field)
    A2 = 0
    width = 0
    P2 = 0
    R2 = 0
    B2 = 0
    temp = 0
    temp = WaterSur
    for row in rows:
        
        val = float(row[0])-(227.961792 -min)+(x[num]-x[0])*s
        if val < WaterSur:

            A2 = A2 + (WaterSur - val)*cellsize
            B2 = B2 + cellsize
            P2=P2+math.sqrt((temp-val)**2+ cellsize**2)
            temp = val
            R2 = A2/P2
    V= Q/A2
    Se=(n**2)*(V**2)/(R2**1.333)
    F2= (V**2)*B2/9.81/A2
    fy2= (s-Se)/(1-F2)
    y0= y0+((fy1+fy2)/2*(-x[num+1]+x[num]))
    del rows
    del row
print "###################"
min = min +s*channelL
s = 0.006483  ##
cellsize=1/1.17
y0 = yi
n=0.025
print y0,min

for num in range(0,len(x)-1):
    WaterSur = min+(x[num]-x[0])*s + y0
    rows = arcpy.da.SearchCursor(inFC1, field)
    A1 = 0
    width = 0
    P1 = 0
    R1 = 0
    B1 = 0
    temp = 0
    temp = WaterSur
    for row in rows:
        
        val = float(row[0])-(228.361115 -min)+(x[num]-x[0])*s
        if val < WaterSur:

            A1 = A1 + (WaterSur - val)*cellsize
            B1 = B1 + cellsize
            P1=P1+math.sqrt((temp-val)**2+ cellsize**2)
            temp = val
            R1 = A1/P1
    
    print   WaterSur
    yi = y0
    V=Q/A1
    Se= (n**2)*(V**2)/(R1**1.333)
    F2= (V**2)*B1/9.81/A1
    fy1= (s-Se)/(1-F2)
    y2p= y0+(fy1*(-x[num+1]+x[num]))
    del rows
    del row

    WaterSur = min+(x[num]-x[0])*s + y2p
    rows = arcpy.da.SearchCursor(inFC1, field)
    A2 = 0
    width = 0
    P2 = 0
    R2 = 0
    B2 = 0
    temp = 0
    temp = WaterSur
    for row in rows:
        
        val = float(row[0])-(228.361115 -min)+(x[num]-x[0])*s
        if val < WaterSur:

            A2 = A2 + (WaterSur - val)*cellsize
            B2 = B2 + cellsize
            P2=P2+math.sqrt((temp-val)**2+ cellsize**2)
            temp = val
            R2 = A2/P2
    V= Q/A2
    Se=(n**2)*(V**2)/(R2**1.333)
    F2= (V**2)*B2/9.81/A2
    fy2= (s-Se)/(1-F2)

    y0= y0+((fy1+fy2)/2*(-x[num+1]+x[num]))
    del rows
    del row
