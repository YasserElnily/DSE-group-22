# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:37:48 2020

@author: Thomas
"""

#Imports
import numpy as np
import matplotlib.pyplot as plt
from PotatoDiagramAndCGRange import *
from Aircraft_constance_Data import *

# #Input variables

# Aero
# Cmac = -0.6943728618
# CLh = 2.5
# CLah = 3.961586125
# CLAh = 0.8 #1.956904453
# CLaAh = 7.489196376 
# deda = 0 #no downwash over the tail due main wing for canard
# SM = 0.05

# #geometry
# lh =  -5 #[m], <0 for canard
# cbar = 1.56 #[m]
# Vh = 1 #Speed of flow over tail is same as over main wing for canard
# V = 1
# xac = 0.25 #[%MAC] #Assumed 0.25 for now
# MAC = 1.56 #[m]
# lf = 7 #[m]

# #Wing pos
# xLEMAC = 5 #[m]


#Stability equation: Sh/S = stabslope*xcgbar - bstab
def Stability(xcg):
    """ 
    FUNCTION: This function Calculates the point on the Stability Xplot line for a particular xcg, with the inputs specified in the input sheet.
    INPUTS: 
            - xcg (type=float): A CG position in [m].
           
    OUTPUTS:
            - Point on the Stability line: Sh/S (type=float).
    """
    
    stabdenominator = ((CLah/CLaAh)*(1-deda)*(lh/MAC)*(Vh/V)**2)
    
    stabslope = 1 / stabdenominator
    bstab = (xac - SM) / stabdenominator
    #print(stabslope, bstab)
    
    return stabslope*xcg - bstab

#Controllability equation: Sh/S = controlslope*xcg + bcontrol
def Controllability(xcg):
    """ 
    FUNCTION: This function Calculates the point on the Controllability Xplot line for a particular xcg, with the inputs specified in the input sheet.
    INPUTS: 
            - xcg (type=float): A CG position in [m].
           
    OUTPUTS:
            - Point on the Controllability line: Sh/S (type=float).
    """
    
    contrdenominator = ((CLh/CLAh)*(lh/MAC)*(Vh/V)**2)
    
    controlslope = 1/ contrdenominator
    bcontrol = ((Cmac/CLAh) - xac) / contrdenominator
    #print(controlslope, bcontrol)
    
    return controlslope*xcg + bcontrol

#Calcs the xcg pos for a particular ShS
def Stabilityxcg(ShS):
    """ 
    FUNCTION: It is the exact reserve of Stability(xcg). This function Calculates the xcg for a particular point on the Stability Xplot line, with the inputs specified in the input sheet.
    INPUTS: 
            - Point on the Stability line: Sh/S (type=float).
           
    OUTPUTS:
            - xcg (type=float): A CG position in [m].        
    """
    
    stabdenominator = ((CLah/CLaAh)*(1-deda)*(lh/MAC)*(Vh/V)**2)
    
    stabslope = 1 / stabdenominator
    bstab = (xac - SM) / stabdenominator
    #print(stabslope, bstab)
    
    return (ShS + bstab) / stabslope

#Calcs the xcg pos for a particular ShS
def Controllabilityxcg(ShS):
    """ 
    FUNCTION: It is the exact reserve of Controllability(xcg). This function Calculates the xcg for a particular point on the Controllability Xplot line, with the inputs specified in the input sheet.
    INPUTS: 
            - Point on the Controllability line: Sh/S (type=float).
           
    OUTPUTS:
            - xcg (type=float): A CG position in [m].        
    """
    
    contrdenominator = ((CLh/CLAh)*(lh/MAC)*(Vh/V)**2)
    
    controlslope = 1/ contrdenominator
    bcontrol = ((Cmac/CLAh) - xac) / contrdenominator
    #print(controlslope, bcontrol)
    
    return (ShS - bcontrol) / controlslope

#Xplot
def TailSize(xLEMAC, accuracy, plot):

    """ 
    FUNCTION: This function can determine the tail size (Sh/S) of the canard for a particular xLEMAC.
    INPUTS: 
            - xLEMAC (type=integer): The location of the leading edge of the MAC in [m].
            - accuracy (type=integer): The amount of decimal points you want the function to determine the Sh/S: 
                        3 is computed relatively quickly, with 4 it takes quite soe time.
            - plot: if answered with 'yes' the function will also give a plot, if 'no' then only numbers are returned.
    OUTPUTS:
            - Tail size: Sh/H (type=float)
            - A plot of the Loading (Potato diagram)
            - Xplot with the CG Range. 
    """
    #Defining the possible xcg range based on the dimensions of the a/c
    xfrontaircraft = ((lf - xLEMAC) - lf)/MAC #expressen in [%MAC]
    xrearaircraft = (lf-xLEMAC)/MAC #expressen in [%MAC]
    #print(xrearaircraft, xfrontaircraft)
    #xcg = np.arange(round(xfrontaircraft, accuracy), round(xrearaircraft, accuracy), 10**-accuracy) #[%MAC]
    xcg = np.arange(Controllabilityxcg(0), Controllabilityxcg(1), -10**-accuracy)
    #print(xcg)
    
    #Creating the controllability and Stability bound lines for the XPlot.
    stab = []
    contr = []
    for pos in xcg:
        #Calculating the stability line points
        stabpoint = Stability(pos)
        stab.append(stabpoint)
        
        #Calculating the stability line points
        controlpoint = Controllability(pos)
        contr.append(controlpoint)
    
    #stab = np.array(stab)
    #contr = np.array(contr)
    
    #CG Range
    CGRange = Potato(xLEMAC, 'no')
    
    if plot == "yes":
    #Plotting the Xplot and the CG Range
        plt.subplot(2,1,2)
        plt.plot(xcg, stab, label="Stability with SM")
        plt.plot(xcg, contr, label="Controllability")
        plt.plot([xfrontaircraft, xfrontaircraft], [0,1], linestyle='dashed', label="Physical front bound of the A/C")
        plt.plot([xrearaircraft, xrearaircraft], [0,1], linestyle='dashed', label="Physical rear bound of the A/C")
        plt.title("Xplot")
        plt.xlabel("xcg/MAC [%]")
        plt.ylabel("Sh/S [-]")
        plt.ylim(0,1)
        plt.xlim(xfrontaircraft - 0.05, xrearaircraft + 0.05)
        #plt.xlim(Controllabilityxcg(1), Controllabilityxcg(0))
        plt.legend()
    
    #Tail sizing 
    #location of the tail
    taillocsize = []
    for point1 in contr:
        #The MAC locations of certain control and stab points
        xcg1 = xcg[contr.index(point1)] 
        #print("first pos of cg=", xcg1)
        
        margin = CGRange[0] - xcg1   #"""The difference between the first cg point and the control region"""
        #print("margin=", margin)
        
        #The first CG-range point must be in front of the controllability line
        if margin < 0: #"""in this situtation, the horizontal stabelizer would be in the uncontrollable region."""
            #print()
            continue #"""So the next point in looked at"""
        
        elif 0 <= margin <= 10**(-accuracy): #"""Here, the horizontal stabelizer is in the perfect location."""
            #print(margin, xcg1, point1)
            #Now it still needs to be checked if the last point of the in within the stable region.
            #point2 = stab[contr.index(point1)] #for the index of point 1, find point 2 in the tab list
            #xcg2 = xcg[stab.index(point2)] #the stability bound for a particular contr point
            xcg2 = Stabilityxcg(point1)
            #print(point1, CGRange[1], xcg2)
            
            if CGRange[1] <= xcg2:
                stabmargin = abs(CGRange[1] - xcg2) 
                #print(CGRange[1], xcg2)
                #taillocsize = [xLEMAC, point1]
                ShS = [point1, point1]
                
                if plot == "yes":
                    plt.subplot(2,1,2)
                    plt.plot(CGRange, ShS, label = "CG Range")
                    plt.legend()
                    plt.show()
                    #continue
                    
                return round(ShS[0], accuracy), stabmargin
                break
            
            else: #The CG range is not in the stability region, so next point in looked at
                #print()
                continue
                
        else:
            #print()
            continue
        
    print("No Sh/S ratio exists to make the aircraft stable.")
    return None 

#accuracy = 3   
def ShSmin(accuracy, plot):
    """ 
    FUNCTION: This function can determine the minimum tail size (Sh/S) of the canard for the specified canard pos in the input file.
    INPUTS: 
            - accuracy (type=integer): The amount of decimal points you want the function to determine the Sh/S: 
                        3 is computed relatively quickly, with 4 it takes quite soe time.
            - plot: if answered with 'yes' the function will also give a plot, if 'no' then only numbers are returned.
            
    OUTPUTS:
            - (New) Leading edge of he MAC: xLEMAC (type=float).
            - Tail size: Sh/H (type=float).
            - A plot of the Loading (Potato diagram) if plot = 'yes'.
            - Xplot with the CG Range if plot = 'yes'.
    """
    #Finding the min ShS possible
    for xcontr in np.arange(Controllabilityxcg(0), Controllabilityxcg(1), -10**-accuracy):
        contrpoint = Controllability(xcontr)
        xstab = Stabilityxcg(contrpoint)
        ShSmargin =  xstab - xcontr
        
        #This code was used to plot the location its checking on the control and stab lines
        # plt.subplot(2,1,2)
        # plt.plot(xcontr, contrpoint, marker='o')
        # plt.plot(xstab, contrpoint, marker="x")
        
        #print(ShSmargin)
        
        CGRange = Potato(xLEMAC, 'no')
        CGlength = (CGRange[0] - CGRange[1])
        
        if ShSmargin < 0:
            continue
        
        elif ShSmargin > abs(CGlength):
            #print(ShSmargin, CGlength)
            ShS = contrpoint
            #print("ShS= ", ShS)
            break
            
        else:
            continue
    
    
    #Finding the xLEMAC for the specific ShS
    xcgMAC = Controllabilityxcg(ShS)
    
    #plt.subplot(2,1,2)
    plt.plot([xcontr, xstab], [ShS, ShS], marker='o')
    
    
    for xlf in np.arange(lf, 0, -10**-accuracy):
        CGRange = Potato(xlf, 'no')
        #print(abs(CGRange[0] - CGRange[1]))
        xcgMACguess = CGRange[0]
        cgmargin = xcgMAC -  xcgMACguess
        #print(cgmargin)
    
        if cgmargin <= 10**-accuracy:
            xLEMACmin = xlf
            break
    
    #making sure that the results are printed and plotted
    result = TailSize(xLEMACmin, accuracy, plot)
    result2 = Potato(xLEMACmin, plot)
    #plt.tight_layout()
    #print(xLEMACmin, result[0])
    return xLEMACmin, result[0]
