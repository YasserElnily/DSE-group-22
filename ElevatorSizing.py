# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:29:55 2020

@author: Thomas
"""

#imports
import numpy as np
import matplotlib.pyplot as plt
#from Aircraft_constance_Data import *


###Inputs
#General a/c
mTO = 20000#[kg]
g = 9.81 #[m/s^2]
Vstall = 85*0.5144 #[kts]
Iyy = 150000 #[kgm^2]
Tmax = 2*28*10**3 #[N]
lf = 23 #[m]
Vcruise = 360*0.5144 #[m/s]
CL0 = 0.24
CD0c = 0.024
CD0_TO = 0.038
CLa = 5.7 #[1/rad]
rho_sl = 1.225
rho_cruise = 0.549
mu = 0.04
thetadotdot = 12/57.3
delta_e_max = -25
alpha = 2 #[deg]
deda = 0.454


#Wing:
S = 70 #[m^2]
AR = 8
b = np.sqrt(S*AR)
c = S/b
CLa_w = 5.7
e = 0.88
lambda_w = 1
deltaCLflap_TO = 0.5 #We dont have flaps atm.
Cmac_wf = 0.05
iw = 2 #[deg]
h = 0.8/c
h0 = 0.5/c
a_s_TO = 12 #[deg]
Cm0 = 0.05

#Horizontal tail:
Sh = 16 #[m^2]
bh = 9 #[m]
CLah = 4.3
ih = -1 #[deg]
lambda_h = 1
eta_h = 0.96
ah_s = 14 #[deg]
xac_h = 11.2
epsilon = 4.54 #For a canard, this would be 0.
bEbh = 1
lh = 11.3 + 0.5

#moment arms
xmg = -0.1
xcg = 1
zd = 2.2
zmg = 0.3
zT = -1.7
xac_wf = -0.9
zcg = 2

# xmg = -0.1
# xcg = 1
# zd = 2.2
# zmg = 0.3
# zT = -0.3
# xac_wf = -0.9
# zcg = 2

def ElevatorDeflection(bEbh, Vcruise):
    #print(Vcruise)
    """ 
    FUNCTION: This function calculates the elevator deflection for a particular elevator size
    INPUTS: 
            - bEbh (type=float): The ratio of the elevator and horizontal stabeliser span.
           
    OUTPUTS:
            - Elevator deflection: de (type=float).
    """
    #Calculating the drag, lift and M at TO (Step 5)
    K = 1 / (np.pi*e*AR)
    CLc = (2*mTO*g) / (rho_cruise*(Vcruise**2)*S)
    CL_TO = CLc + deltaCLflap_TO
    CD_TO = CD0_TO + K*CL_TO**2
    VR = Vstall
    Sref = S
    
    D_TO = 0.5*rho_sl*(VR**2)*S*CD_TO
    L_TO = 0.5*rho_sl*(VR**2)*Sref*CL_TO
    Mac_wf = 0.5*rho_sl*(VR**2)*Cmac_wf*Sref*c
    
    #Calculating he linear accel (Step 6)
    Ff = mu*(mTO*g - L_TO)
    a = (Tmax - D_TO - Ff) / mTO
    
    #Calculating all pitching moments contributions at TO (Step 7)
    #Most forward a/c cg considered as gives biggest moments
    M_w = mTO*g*(xmg - xcg)
    M_D = D_TO*(zd - zmg)
    M_T = Tmax*(zT - zmg)
    M_L_wf = L_TO*(xmg - xac_wf)
    M_a = mTO*a*(zcg- zmg)
    
    #Calulating the lift the horizontal tail needs to generate
    Lh = ( L_TO*(xmg - xac_wf) + Mac_wf + mTO*a*(zcg - zmg) + mTO*g*(xmg - xcg) \
          + D_TO*(zd - zmg) + Tmax*(zT - zmg) - Iyy*thetadotdot ) / (xac_h - xmg)
    
        
    #Calculating the desired horizontal tail CL_h (Step 9)
    CLh = 2*Lh / (rho_sl*(VR**2)*Sh) #use VR!
    
    #Calculating the AoA effectiveness of the elevator (toa_e) (Step 10)
    ah = (alpha + ih - epsilon) #in [deg]
    toa_e = ((ah/180*np.pi) + (CLh/CLah)) / ((delta_e_max)/180*np.pi)
    #print(toa_e, "ah", (ah/180*np.pi), CLh, CLah, (delta_e_max)/180*np.pi)
    
    #Determining the currisponsing CE/Ch ratio (Step 11)
    
    if toa_e >= 0.55:
        bgraph = 0.35
        slope = (0.8 - 0.55) / (0.7 - 0.35)
        CECh = (toa_e - bgraph) / slope
    
    elif toa_e <= 0.55 and toa_e >= 0.4:
        bgraph = 0.2
        slope = (0.55 - 0.4) / (0.35 - 0.2)
        CECh = (toa_e - bgraph) / slope
        
    else:
        #Approximating the last bit using a sqrt function
        a = 0.4**2/0.2
        CECh = toa_e**2 / a
        #print(CECh)
        
        # print("AoA effectiveness of the elevator, toa_e = ", toa_e)
        # CECh = input("The AoA effectiveness of the elevator (toa_e) is outside the range of where the code \
        #              'MohammadH.Sadraey-AircraftDesignASystemsEngineeringApproach-JohnWileyamp_Sons2012' (page 682 in the pdf) \
        #                  Read the value on the x-axis for a value of toa shown above and fill it in here: ")
              
    
    #Calculating the elevator effectiveness derivs (Step 16)
    #Most fwd or aft cg used for this, depends on ...?
    
    Vol_h = (lh*Sh) / (S*c)
    Cmde = - CLah * eta_h * Vol_h * bEbh * toa_e
    CLde = - CLah * eta_h * (Sh/S) * bEbh *toa_e
    CLhde = CLah * toa_e
    
    #Calculating the elevator deflection (Step 17)
    Cma = CLa*(h - h0) - CLah*eta_h*(Sh/S)*(lh/c)*(1-deda)
    q = 0.5*rho_sl*(Vcruise**2)
    CL1 = (2*mTO*g) / (rho_sl*(Vcruise**2)*S)
    
    de = -(((Tmax*-0.3)/(q*S*c) + Cm0)*CLa + (CL1 - CL0)*Cma) / ((CLa*Cmde) - (Cma*CLde)) #in [rad]
    #print(Tmax, zT, q, S, c, Cm0, CLa, CL1, CL0, Cma, CLa, Cmde, Cma, CLde)
    
    return de

#Calculating the differene in CLh when elevator max negatively deflected
#delta_alpha_0e = -1.15 * CECh * delta_e_max
    
"""Going to use Matlab?!"""
#Vlist = np.arange(50*0.5144, 400*0.5144, 0.01)
Vlist = np.arange(50*0.5144, 400*0.5144, 1)
delist = []
for V in Vlist:
    de = ElevatorDeflection(bEbh, V)
    delist.append(de)
    
dedeg = np.array(delist)*180/np.pi # in [deg]
    
#plotting the results
plt.plot(Vlist, dedeg, label='elevator deflection')
plt.show()
    

    









