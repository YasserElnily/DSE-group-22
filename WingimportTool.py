# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np


#importing the Airfoildata
inpu = np.loadtxt(fname = 'NACA2415.dat',dtype=str)[1:]
data = inpu.astype(np.float)

#frontspar
fr = 0.15


def interpolation(x1,x2,y1,y2,a):
    interp = y2 + ((y1-y2)/(x1-x2)) * (a-x2)
    return interp


def wingboxdimension(filename,sparxloc):
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
    print(narr1,narr2)
    #interpolation of the data
    if (sparxloc - data[narr1,0])<0:
        B = interpolation(data[narr1,0],data[narr1+1,0],data[narr1,1],data[narr1+1,1],sparxloc)
    elif (sparxloc - data[narr1,0])>0:
        B = interpolation(data[narr1-1,0],data[narr1,0],data[narr1-1,1],data[narr1,1],sparxloc)
    else:
        B = data[narr1,1]
    print(B)
    if (sparxloc - data[narr2,0])<0:
        C = interpolation(data[narr2,0],data[narr2-1,0],data[narr2,1],data[narr2-1,1],sparxloc)
    elif (sparxloc - data[narr2,0])>0:
        C = interpolation(data[narr2+1,0],data[narr2,0],data[narr2+1,1],data[narr2,1],sparxloc)
    else:
        C = data[narr2,1]
        print("c",C)
    
    return sparxloc,B,C

airfoil = 'NACA2415.dat'
frontspar   = .15
rearspar    = .50

#frontspar
x,y1,y2 = wingboxdimension(airfoil,frontspar)
print(x,y1,y2)

#rearspar
x,y1,y2 = wingboxdimension(airfoil,rearspar)
print(x,y1,y2)
 
