"""
Created on Fri Jun 12 14:41:33 2020

@author: Yasser Elnily
"""

"""
The variables in this code were entered manually for now, once the file with
all the cosntants is ready they can be imported to this file so that everything 
updates/iterates automatically once any other parameter is changed.
"""

from math import *

g     = 9.80665
rho   = 1.225                       #density

a     = 340.294
V_s   = 31                          #Stall speed
V     = 1.2*V_s                     #from the vn diagram
M     = V/a
beta  = sqrt(1-M**2)

#Wing info
S_ref = 10.22
b     = 7
MAC   = 1.46
spar_r= 0.6                         #% spar location
b_half= b/2
AR    = b**2/S_ref                  #Aspect ratio

#Aerodynamics
n_foil= 0.95                        #Airfoil efficieny factor
Cd0   = 0.003079761569              

#Aileron sizing
#b1        = 2.45                    #Start point of the aileron (spanwise)
#b2        = 3.5                     #end point of the aileron (spanwise)
c_aileron = MAC*(1-spar_r)           #Aileron chord
tau       = 0.6                      #Aileron effectiveness
            

#Sweep angles calculations
quarter_sweep = atan(0)
LE_sweep = atan(tan(quarter_sweep)+0.25*(2*spar_r/b)*(1-MAC))
half_sweep = atan(tan(LE_sweep)-0.5*(2*spar_r/b)*(1-MAC))


###-----------------------------Aileron Sizing Function-----------------------------###
def aileron_deflection(b2, b1):
    
    C_L_a  = (2*AR*pi)/(2+sqrt(4+(AR*beta/n_foil)**2*(1+(tan(half_sweep)/beta)**2)))
    
    #Rolling moment coefficient
    C_l_da = ((2*C_L_a*tau)/(S_ref*b))*((MAC/2)*(b2**2-b1**2))
    
    #Roll damping coefficient
    int_clp = MAC/3*b_half**3
    C_l_p   = -4*(C_L_a+Cd0)/(S_ref*b**2)*int_clp
    
    
    #P_req = 60/1.3
    
    da   = radians(1) 
    time = 10
    while time > 1.3:
        P         = degrees(-C_l_da/C_l_p*da*(2*V/b))
        time      = 60/P
        da        += radians(0.001)
        
    return (degrees(da))







