# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:21:58 2020

@author: Timo


functions in this file are:
loadcase1() returns [ylocation,Ixx,Iyy,Ixy,shearz,shearx,Momentz,Momentx,Torsion] #Take-off loadcase 
loadcase2() returns [ylocation,Ixx,Iyy,Ixy,shearz,shearx,Momentz,Momentx,Torsion] #Normalflight loadcase
loadcase2() returns [ylocation,Ixx,Iyy,Ixy,shearz,shearx,Momentz,Momentx,Torsion] #Landing load case

stiffendskincalculation(chord,t,nstring,E,v) returns crippeling stress of the stiffend panel 
rivetbuckling(rivet,E,t,s) returns interrivetbuckling stress 
"""
import numpy as np
import math

#aluminium values
alpha_Al = 0.8
n_Al = 0.6
sig_y6061 = 280 * 10**6
sig_ult6061 = 338 * 10**6   
E_6061 = 70 * 10**9 
G_6061 = 27 * 10**9

G = G_6061
E = E_6061
sig_y = sig_y6061
sig_ult = sig_ult6061

#stringer dimensions
w_s = 0
h_s = 0
t_s = 0
b = 0

import matplotlib.pyplot as plt

def plotting(x,y,name):
    plt.title(name)
    plt.plot(x,y)
    plt.show()
    
 
def stiffendskincalculation(chord,t,nstring,E,v,stringer):
    h_s, t_s, alpha_Al, n_al, sig_y6061, sig_ulti6061, E_6061, G_6061 = stringer
    #stiffener components: Assuming L stiffener, both parts SSFS 
    C_s = 0.425
    sigma_cc_base = sig_y * alpha_Al * (C_s/sig_y * np.pi**2 * E/(12*(1-v**2)) * (t_s/h_s)**2)**(1-n_Al)
    area_base = (h_s)*t_s
    sigma_cc_vertical = sig_y * alpha_Al * (C_s/sig_y * np.pi**2 * E/(12*(1-v**2)) * (t_s/h_s)**2)**(1-n_Al)
    area_vertical = (h_s*t_s)

    sigma_cc_stiffener = (sigma_cc_base*area_base + sigma_cc_vertical*area_vertical)/(area_base+area_vertical)
    area_stiffener = area_base+area_vertical



    if nstring < 1:
        C = 6.98
        b = chord
        sigma_cc_panel = C * (np.pi**2 * E)*(t/b)**2 / (12*(1-v**2))   

    elif nstring < 2:
        C = 5.41  
        Cst = 6.98

        we = (t/2)*math.sqrt(Cst*math.pi**2*E/(12*(1-v**2)*sigma_cc_stiffener))
        b = chord/(nstring+1)- we
        sigma_cr_skin = C * (np.pi**2 * E)*(t/b)**2 / (12*(1-v**2))
        sigma_cc_panel = ((sigma_cc_stiffener*area_stiffener)+(sigma_cc_stiffener*t*we)+(sigma_cr_skin*t*b))/(area_stiffener+t*we+t*b)


    else:
        C1 = 5.41
        C2 = 4.00
        Cst = 6.98

        we = (t/2)*math.sqrt(Cst*math.pi**2*E/(12*(1-v**2)*sigma_cc_stiffener))
        b = chord / (nstring+1)
        bacc1 = b - we
        bacc2 = b - 2*we
        #the sides of the wingbox
        sigma_cr_skin = C1 * (np.pi**2 * E)*(t/bacc1)**2 / (12*(1-v**2)) 
        sigma_cc_panel1 = (sigma_cc_stiffener*area_stiffener + sigma_cc_stiffener*2*we*t + sigma_cr_skin*b*t) / ( b*t + area_stiffener)
        #between the stringers
        sigma_cr_skin = C2 * (np.pi**2 * E)*(t/b)**2 / (12*(1-v**2)) 
        sigma_cc_panel2 = (sigma_cc_stiffener*area_stiffener + sigma_cc_stiffener*2*we*t + sigma_cr_skin*b*t) / ( b*t + area_stiffener)
        sigma_cc_panel = min([sigma_cc_panel1,sigma_cc_panel2])
    return sigma_cc_panel

def rivetbuckling(rivet,E,t,s):
    #rivet spacing
    if s==0:
        print("Sigma_ir is 0")
        return 0
        
        
    else:
        if rivet == "countersunk":
            c = 1
        elif rivet == "pop":
            c = 2.1
        elif rivet == "brazier":
            c = 3
        
        sig_ir = 0.9 * c * E * (t/s)**2 
        return sig_ir
    
def shearbucklingstress(D,t,E,v,a,halfspan):
    if D != 0:
        a_b_ratio = halfspan/a/D
        if a_b_ratio>2:
            k = 6
        elif a_b_ratio>1.5 and a_b_ratio=<2:
            k = 7
        elif a_b_ratio>1 and a_b_ratio=<1.5:
            k = 8
        elif a_b_ratio=<1:
            k = 9
        tau_cr = k * np.pi**2 * E* (t/D)**2 /(12*(1-v**2))
        return tau_cr
    else:
        print("tau_cr is 0")
        return 0

def stiff_weight(t_s,h_s,density,number_of_stiff,stepsize):
    #area of stiffeners
    w_s = h_s + t_s
    A_s = h_s*t_s + w_s*t_s

    stiffeners_area = number_of_stiff*A_s
    stiffeners_vol = stiffeners_area*stepsize
    stiffeners_weight = stiffeners_vol*density
    
    return stiffeners_weight
