# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 16:49:26 2020

@author: Thomas
"""

#Import
import numpy as np
import matplotlib.pyplot as plt
from Aircraft_constance_Data import *

# #Input variables
# #Wing location
# xLEMAC = 5 #[m]
# MAC = 1.56 #[m]
# lf = 7


# #masses
# OEW = 729
# mpayload = 150 #[kg]
# mfuel = 92 #[kg]

# #Xcg inputs
# # x0 = 0.3 #[%MAC]
# # xcgpayload = -3.00 #[%MAC]
# # xcgfuel = 0.8 #[%MAC]

# #lf = 7 m
# x0 = 4.5 #[m]
# xcgpayload = 1 #[m]
# xcgfuel = xLEMAC + 0.5*MAC #[m]

def Potato(xLEMAC, plot):
    """ 
    FUNCTION: This function can determine the CG Range of the aircraft while loading, with the specified canard pos in the input file.
    INPUTS: 
            - xLEMAC (type=integer): The Leading edge position of the Mean Aero Cord (MAC) in x [m].
            - plot (type=string): If answered with 'yes' the function will also give a plot, if 'no' then only numbers are returned.
    OUTPUTS:
            - The most forward and aft cg positions during loading: [fwd cg, aft cg] (type=list)
            - A plot of the Loading (Potato diagram)
    """
    ###Mass points
    m0 = OEW
    m1 = OEW + mpayload
    m2 = m1 + mfuel
    massesfront = [m0, m1, m2]
    
    m3 = OEW + mfuel
    m4 = m3 + mpayload
    massesback = [m0, m3, m4]
    
    
    ###Payload first, fuel second
    #xcg locations
    # xcg new = (oldcg*mass + oldcg * small mass) / tot mass = (xcg0*m0 + xi*mi)/mtot
    x1 = (x0*OEW + mpayload*xcgpayload) / (OEW + mpayload)
    x2 = (x1*(OEW+mpayload) + xcgfuel*mfuel) / (OEW + mpayload + mfuel)
    xcgfront = [x0, x1, x2] #in [m]
    xcgfront = (np.array(xcgfront) - xLEMAC) / MAC #in [%MAC]
    
    ###Fuel first, payload second
    x3 = (OEW*x0 + mfuel*xcgfuel) / (OEW + mfuel)
    x4 = ((OEW + mfuel)*x3 + mpayload*xcgpayload) / (OEW + mfuel + mpayload)
    xcgback = [x0, x3, x4] #in [m]
    xcgback = (np.array(xcgback) - xLEMAC) / MAC #in [%MAC]
    
    ###Potato diagram plot
    if plot=='yes':
        plt.subplot(2,1,1)
        plt.plot(xcgfront, massesfront, label="Payload loaded first")
        plt.plot(xcgback, massesback, label="Fuel loaded first")
        plt.title("Potato/Loading diagram")
        plt.xlabel("xcg/MAC [%]")
        plt.ylabel("m [kg]")
        plt.legend()
        plt.show()
        
    #CG Range determination
    CGRange = [min(xcgfront), max(xcgback)]
    #print(CGRange, "in [%MAC]") 
    
    return CGRange
"""
#Plotting the loading diagram for the whole fuselage length of cg locs
accuracy = 2
xfrontaircraft = ((lf-xLEMAC)-lf)/MAC #expressen in [%MAC]
xrearaircraft = (lf-xLEMAC))/MAC #expressen in [%MAC]
xMAClist = np.arange(round(xfrontaircraft, accuracy), round(xrearaircraft, accuracy), 10**-accuracy) #[%MAC]

cgfrontbound = []
cgrearbound = []
for xLEMAC in xMAClist:
    point = Potato(xLEMAC)
    
    cgfrontbound.append(point[0])
    cgrearbound.append(point[1])

#plotting the result
plt.title("CG Range for x_LEMAC over the entire fuselage length")
plt.plot(np.array(cgfrontbound)/MAC, np.array(xMAClist)/lf, label="Front cg range bound")
plt.plot(np.array(cgrearbound)/MAC, np.array(xMAClist)/lf, label = "Rear cg range bound")
plt.ylabel("x_LEMAC/lf [-]")
plt.xlabel("xcg/MAC [-]")
plt.show()
""" 
    
    





