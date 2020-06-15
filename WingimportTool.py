# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import math



def interpolation(x1,x2,y1,y2,a):
    interp = y2 + ((y1-y2)/(x1-x2)) * (a-x2)
    return interp


def wingboxcoordinates(filename,sparxloc):
    inpu = np.loadtxt(fname = filename,dtype=str)[1:]
    data = inpu.astype(np.float)
    sparxlocx = 0
    narr= 0
    for x in data:
        if abs(x[0]-sparxloc) < abs(sparxlocx-sparxloc):
            sparxlocx = x[0]
            sparxlocy = x[1]
            narrhit = narr
        if narr is round(len(data)/2)-1 :
            narr1 = narrhit
            sparxlocx = 0
        narr = narr + 1
    narr2 = narrhit
    
    #interpolation of the data
    if (sparxloc - data[narr1,0])<0:
        B = interpolation(data[narr1,0],data[narr1+1,0],data[narr1,1],data[narr1+1,1],sparxloc)
    elif (sparxloc - data[narr1,0])>0:
        B = interpolation(data[narr1-1,0],data[narr1,0],data[narr1-1,1],data[narr1,1],sparxloc)
    else:
        B = data[narr1,1]
    
    if (sparxloc - data[narr2,0])<0:
        C = interpolation(data[narr2,0],data[narr2-1,0],data[narr2,1],data[narr2-1,1],sparxloc)
    elif (sparxloc - data[narr2,0])>0:
        C = interpolation(data[narr2+1,0],data[narr2,0],data[narr2+1,1],data[narr2,1],sparxloc)
    else:
        C = data[narr2,1]
        
    
    return sparxloc,B,C


# #frontspar
# x,y1,y2 = wingboxcoordinates(airfoil,frontspar)
# print(x,y1,y2)


# #rearspar
# x,y1,y2 = wingboxcoordinates(airfoil,rearspar)
# print(x,y1,y2)

def andreiinput(airfoil,frontspar,rearspar):
    xf, yf1,yf2 =  wingboxcoordinates(airfoil,frontspar)
    xr, yr1, yr2 = wingboxcoordinates(airfoil,rearspar)
    return np.array([[xf,xr,xr,xf],[yf1,yr1,yr2,yf2]])


#wingbox dimensions
def wingboxdimension(airfoil,frontspar,rearspar):
    xf, yf1,yf2 =  wingboxcoordinates(airfoil,frontspar)
    xr, yr1, yr2 = wingboxcoordinates(airfoil,rearspar)
    
    #frontspar
    hf = abs(yf1) + abs(yf2)
    
    #rearspar
    hr = abs(yr1) + abs(yr2)
    
    
    #topskin
    ltop = math.sqrt((xr-xf)**2 + (yf1-yr1)**2)
    thethat1 = math.atan((xr-xf)/abs(yf1-yr1))
    thethat2 = math.atan(abs(yf1-yr1)/(xr-xf))
    
    #bottom skin
    lbottom = math.sqrt((xr-xf)**2 + (yf2-yr2)**2)
    thethab1 = math.atan((xr-xf)/abs(yf2-yr2))
    thethab2 = math.atan(abs(yf2-yr2)/(xr-xf))
    return hf, hr, ltop, lbottom, thethat2, thethab2
