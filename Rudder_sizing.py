"""
Created on Mon Jun 15 09:48:29 2020

@author: Yasser Elnily
"""

"""
The variables in this code were entered manually for now, once the file with
all the cosntants is ready they can be imported to this file so that everything 
updates/iterates automatically once any other parameter is changed.
"""

from math import *

#Rudder parameters
C_L_av  = 4.5
n_v     = 0.96  
l_v     = 1.775
S_v     = 1.86          #vertical tail surface area
b_rTOb_v= 1             #spans ratio, rudder to vertical tail

#Wing/aircraft parameters and charactersitics
S       = 12.04
b       = 7
T       = 500           #Thurst of the operational engine after the failure
y_t     = 3.5           #half span
rho     = 0.905         #air dnesity at cruise altitude

V_s     = 31            #stall speed
V_MC    = 0.8*V_s       #minimum controllable speed


###-------------------------Rudder Sizing Function-------------------------###
def rudder_deflection(S_v):
    
    V_v     = (l_v*S_v)/(b*S)
    q       = 0.5*rho*V_MC**2
    
    C_rTOC_v = 0.1            #chords ratio, rudder to vertical tail
    dr       = radians(90)    #Maximum rudder deflection --> value initialization
    while dr >= radians(30):  #designing for a maximum deflection of 30 degrees
              
        tau     = C_rTOC_v*0.8 + 0.28            #rudder angle of attack effectiveness
        C_n_dr  = -C_L_av*V_v*0.96*tau*b_rTOb_v  #rudder control derivative
    
        dr       = (T*y_t)/(-q*S*b*C_n_dr)       #maximum deflection
        
        C_rTOC_v += 0.001       
        
    return (C_rTOC_v)
