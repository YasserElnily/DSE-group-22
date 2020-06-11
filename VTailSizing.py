# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 11:16:58 2020

@author: Thomas
"""

#Import
import numpy as np
from Aircraft_constance_Data import *
from Xplot import ShSmin

"""
This whole code is based on slide 26 of the SEAD course
The critical case for V-Tail sizing is one engine inoperative
"""
# #inputs
# bv = 1.5 #[m], the span of the v tail, assumed for now
# deltaTe = 500 #[N]
# CL = 1.1 #CL of the wing of the a/c, assumed for now
# B = 25 #[deg]


lv = lf - ShSmin(3, 'no')[0] #Assuming the Y acts at the end of the fuselage and lv is the length to xLEMAC
#lv = 6.5
def VTailSize(Bequil, bv, accuracy):
    #inputs
    ye = span/2
    W = OEW + mpayload #+ mfuel, the smallest weight is critical
    
    #Determining the CLvB
    CyvB = (np.pi/2) * bv**2
    #Clv = CyvB*B
    
    #Implementing the sizing figure in code
    nv = 0.95 #[-] the ratio of Vv/V.
    x = (deltaTe*ye*CLAh) / (W*lv)
    print("x needs to be <= 0.16 for ths method to work.")
    #x = 0.13
    print(x)
    
    """ 
    FUNCTION: This function can determine the verticle size (Sv/S) as well as the verticle tail area (Sv) for the inputs in the input file.
    INPUTS: 
            - Bequil (type=integer): The equilibrium slide slip angle of the aircraft after the engine failure, when the aircraft is \
                flying in equilibrium again. Options are: [-4, -2, 0, 2, 4]. #[deg].
            - bv (type=float): The (chosen) span of the verticle tail.
            - (lv (type=float): The arm from where the side force of the v-tail (Y) acts to the xLEMAC of the aircraft. \
                Engine failure on main wing is critical for Sv.)
            - accuracy (type=integer): The amount of decimal points you want the function to determine the Sv/S.
            
    OUTPUTS:
            - (New) Leading edge of he MAC: xLEMAC (type=float)
            - Tail size: Sh/H (type=float)
            - A plot of the Loading (Potato diagram)
            - Xplot with the CG Range. 
    """
    
    if Bequil == 4:
        maxpoint = [0.16, 1]
        slope = maxpoint[1]/maxpoint[0]
        tailsize = slope * x
        SvS = tailsize / (nv*CyvB)
        Sv = SvS * S
        
        if x > maxpoint[0]:
            return "This situation results in a too high bank angle and a Sv/S > 1.\
            The Sv need to be bigger then the S.\
            No feasible SvS can be determined with this method."
        
        else:
            return round(SvS, accuracy), round(Sv, accuracy)
        
    elif Bequil == 2:
        maxpoint = [0.16, 0.8]
        slope = maxpoint[1]/maxpoint[0]
        tailsize = slope * x
        SvS = tailsize / (nv*CyvB)
        Sv = SvS * S
        
        if x >= maxpoint[0]:
            return "This situation (Bequil = 2) results in a too high bank angle after engine failure. \
            Bequil = 4 can still be tried."
        
        else:
            return round(SvS, accuracy), round(Sv, accuracy)
        
    elif Bequil == 0:
        maxpoint = [0.145, 0.62]
        slope = maxpoint[1]/maxpoint[0]
        tailsize = slope * x
        SvS = tailsize / (nv*CyvB)
        Sv = SvS * S
        
        if x >= maxpoint[0]:
            return "This situation (Bequil = 0) results in a too high bank angle after engine failure.\
            Bequil = 2 or 4 can still be tried."
        
        else:
            return round(SvS, accuracy), round(Sv, accuracy)
        
    elif Bequil == -2:
        maxpoint = [0.13, 0.5]
        slope = maxpoint[1]/maxpoint[0]
        tailsize = slope * x
        SvS = tailsize / (nv*CyvB)
        Sv = SvS * S
        
        if x >= maxpoint[0]:
            return "This situation (Bequil = -2) results in a too high bank angle after engine failure. \
            Bequil = 0, 2 or 4 can still be tried."
        
        else:
            return round(SvS, accuracy), round(Sv, accuracy)
    
    elif Bequil == -4:
        maxpoint = [0.125, 0.42]
        slope = maxpoint[1]/maxpoint[0]
        tailsize = slope * x
        SvS = tailsize / (nv*CyvB)
        Sv = SvS * S
        
        if x >= maxpoint[0]:
            return "This situation (Bequil = -4) results in a too high bank angle after engine failure. \
            Bequil = -2, 0, 2 or 4 can still be tried."
        
        else:
            return round(SvS, accuracy), round(Sv, accuracy)
    
    else:
        return "This equilibrium side slip angle is not included in \
              the sizing, please choose of the following options: \
                  [-4, -2, 0, 2, 4]."
