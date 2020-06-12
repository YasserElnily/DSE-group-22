# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 09:37:12 2020

@author: Andrei
"""

#Inputs

span = 7   #[m]
halfspan = span/2   #[m]
chord = 1.46   #[m]
m = 1000       #[Kg]

Ixx = 121312332   #[m4]
Iyy = 123123123   #[m4]
Izz = 123123123   #[m4]

def reaction_forces (condition, halfspan, m, Ixx, Iyy, Izz): #Conditions: VTO, cruise, VL
    
    #Reaction forces and moments at fuselage
    #LEFT WING TAKEN FOR REFERENCE
    #Convention, x pointing forward, y pointing toward left wing tip, z pointing up
    #All reaction forces drawn in the positive axis direction
    #All reaction moments drawn counterclockwise (x to y, y to z, x to z)
        
    #General forces and loads
    T_vtol = 5000   #[N]
    T_cruise = 4000   #[N]
    w_drag =  2.5   #[N/m]
    W_eng = 400     #[N]
    w_weight = 2.5  #[N/m]
    w_lift = 2.5    #[N/m]
         
    if condition == "VTO":
        #Accelerations  
        ax = 0    #[m/s2]
        ay = 0    #[m/s2]
        az = 1    #[m/s2]
        a_angx = 0    #[rad/s2]
        a_angy = 0    #[rad/s2]
        a_angz = 0    #[rad/s2] 
        
        #Reaction forces and moments at fuselage VTOL Case:
        Rx = m*ax 
        Ry = m*ay
        Rz = m*az+halfspan*w_weight-T_vtol+W_eng
        Mx = Ixx*a_angx + w_weight*halfspan*halfspan/2 - T_vtol*halfspan + W_eng*halfspan
        My = Iyy*a_angy
        Mz = Izz*a_angz
        
    elif condition == "cruise":
        #Accelerations
        ax = 0
        ay = 0
        az = 0
        a_angx = 0
        a_angy = 0
        a_angz = 0 

        #Reaction forces and moments at fuselage Cruise Case
        Rx = m*ax - T_cruise + w_drag*halfspan
        Ry = m*ay
        Rz = m*az + w_weight*halfspan - w_lift*halfspan + W_eng
        Mx = Ixx*a_angx - w_lift*halfspan**2 /2 + w_weight*halfspan**2 /2 + W_eng*halfspan
        My = Iyy*a_angy
        Mz = Izz*a_angz - w_drag*halfspan**2 /2 + T_cruise*halfspan
    
    elif condition == "VL":
        #Forces and loads
        ax = 0
        ay = 0
        az = -1
        a_angx = 0
        a_angy = 0
        a_angz = 0 
        
        #Reaction forces and moments at fuselage Landing Case
        Rx = m*ax
        Ry = m*ay 
        Rz = m*az+halfspan*w_weight-T_vtol+W_eng 
        Mx = Ixx*a_angx + w_weight*halfspan*halfspan/2 - T_vtol*halfspan + W_eng*halfspan 
        My = Iyy*a_angy
        Mz = Izz*a_angz
    
    return (Rx, Ry, Rz, Mx, My, Mz)
