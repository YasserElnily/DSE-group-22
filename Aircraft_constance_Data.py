#Input file
"""In this file all inputs that are not depended on the tools that are being created. Feel free to add more variables that need to be set.
This file can be used by writing (from Aircraft_constance_Data.py) in your program. At that point you can use all these constance like you would 
in a normal python document. The same steps should be taken for all tools that are beeing created"""

from numpy import pi
"""General inputs"""

#General 
g = 9.80665 #[m/s^2]
rho_sl = 1.225
rho_cruise = 0.905
mu = 0.04 #Dynamic friction coeff, used by book.
n_v     = 0.96 
a     = 340.294 #used for aileron sizing to calc beta. 

#Speeds
V = 61 #[m/s] Ratio Vh/V need to be 1
Vh = V #[m/s] Speed of flow over tail is same as over main wing for canard
Vcruise = V #[m/s]
Vstall = 44 #[kts]

"""Geometry"""

#Fuselage
lf = 6 #[m] The length of the fuselage
Iyy = 150000 #[kgm^2], MOI of the aircraft when turning about its cg.
hf = 0.8 #[m] (from catia?)
wf = 1 #[m] (from catia?)


#wing section - Structures
airfoil     = 'airfoil.dat' #this is the dat file of the coordinates of the airfoil geometry 
frontspar   = .15 #front spar at 15% of the chord.
rearspar    = .60  #rear spar at 60% of the chord.
chord       = 1.72 #m
span        = 7 #m
taper       = 0 

#Wing geometry: rectangle - Aero and control
S = 10.5 #[m^2]
S_ref = 10.22
b = 7 #[m]
c = 1.5 #[m]
MAC = 1.5 #[m] The length of the mean aerodynamic cord.
AR = 8
lambda_w = 1

#Horizontal tail:
ih = 4 #[deg]
lambda_h = 1
eta_h = 0.96
xac_h = 11.2
epsilon0 = 0
epsilon = 0 #For a canard, this would be 0.

###Control surfaces

#Elevator
bEbh = 1

#Aileron
b1        = 2.45                    #Start point of the aileron (spanwise)
b2        = 3.5                     #end point of the aileron (spanwise)
tau       = 0.6                      #Aileron effectiveness


"""Propulsion section"""

#Thrust data
deltaTe = 100 # *(assumed) [N] #differential thrust after engine failure
Tmax = 2*28*10**3 #[N]
Tw = 37.5*10**3 #[N]
Th = 18.5*10**3 #[N]


"""Aerodynamics"""

#Some AoA
alpha = 2 #[deg]
a_s_TO = 12 #[deg]
ah_s = 14 #[deg]

#Airfoil characteristics
n_foil= 0.95 
#...

#Wing characteristics
xac = 0.2726537216828479 #[%MAC] #Assumed 0.25 for now
Cmac = -0.105
#CLh = 0.317625
CLh = 0.47
CLah = 3.80062
CLAh = 0.3084
CLaAh = 8
#CLaAh = 3.25
C_L_av  = 4.5
deda = 0 #no downwash over the tail due main wing in front of canard
CL0 = 0.24 #CL at zero AoA
CD0c = 0.024 #CD0 clean
CD0_TO = 0.038 #CD0 during TO
e = 0.88 #Oswald eff
Cmac_wf = 0.05  #moment coeff of wing anf fuselage together
Cm0 = Cmac_wf #assume that the base moment on the aircraft is the one from the wing and fus.
iw = 0 #[deg] #angle if incidence of main wing.


"""Stability and Control"""

#masses - used for potato diagram (mTO for el sizing)
OEW = 585 #[kg]
mpayload = 150 #[kg]
mfuel = 40 #[kg]
mTO = OEW + mpayload + mfuel#[kg]

#Wing pos
xLEMAC = 3.15 #[m]
lh =  -3 #[m], <0 for canard

#CGs of particular masses
x0 = 2.8 #[m]
xcgpayload = 2.5 #[m]
xcgfuel = xLEMAC + 0.5*MAC #[m]

#Some more XPlot data
SM = 0.05 #Stability Margin (SM)

#V- tail sizing
bv = 1.5 #[m], the span of the v tail, can be chosen accordingly
B = 25 #[deg] The acceptable side slip angle for the aircraft: chosen by engineers.
#lv = lf - ShSmin(3, 'no')[0] #Assuming the Y acts at the end of the fuselage and lv is the length to xLEMAC


#Control surface inputs
delta_e_max = -25
thetadotdot = 12/(180/pi) #[rad/s^2] Angular accel to be achieved during TO: from CS 23?
deltaCLflap_TO = 0 #We dont have flaps atm.
CLa_w = CLaAh

#moment arms
xmg = 3.5 #[m] from nose of a/c
zmg = 1 #[m] from zcg to bottom of wheels
zcg = 0.2 #[m] with as ref bottom of fuselage (from catia?)
zd = hf - zcg #[m] assumed that wing is a top of fuselage, need z pos of cg range, from catia maybe?
zTw = zd #[m] need z pos of cg range, from catia maybe?
zTh = zcg #[m] assumed that canard at bottom of fuselage
xac_wf = xac #[m] assumed that ac of wing and fus is at ac of w. ==> or AVL?


"""Structural inputs"""
#materials
#AL6061
def material(typ):
    if typ == "AL6061":
        alpha_Al = 0.8
        n_Al = 0.6
        sig_y = 280 * 10**6
        sig_ult = 338 * 10**6   
        E = 70 * 10**9 
        G = 27 * 10**9
    else: print("Material_Error")
    return alpha_Al, n_Al, sig_y, sig_ult, E, G

#stringerdimension
def stringer(material):
    alpha_Al, n_al, sig_y6061, sig_ulti6061, E_6061, G_6061 = material
    #dimensions
    h_s = 0.002 #hight of the stringer
    t_s = 0.020 #thickness of the stringer
    return h_s, t_s, alpha_Al, n_al, sig_y6061, sig_ulti6061, E_6061, G_6061



