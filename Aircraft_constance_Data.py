#Input file
"""In this file all inputs that are not depended on the tools that are being created. Feel free to add more variables that need to be set.
This file can be used by writing (from Aircraft_constance_Data.py) in your program. At that point you can use all these constance like you would 
in a normal python document. The same steps should be taken for all tools that are beeing created"""

###Fuselage section

#Geometry
lf = 7 #[m] The length of the fuselage


#wing section
airfoil     = 'airfoil.dat' #this is the dat file of the coordinates of the airfoil geometry 
frontspar   = .15 #front spar at 15% of the chord.
rearspar    = .60  #rear spar at 60% of the chord.
chord       = 2 #m
span        = 7 #m
taper       = 0 

###propulsion section
#...
deltaTe = 500 # *(assumed) [N] #differential thrust after engine failure



###Aerodynamics

#Airfoil characteristics
#...

#Wing characteristics
xac = 0.25 #[%MAC] #Assumed 0.25 for now
Cmac = -0.6943728618 
CLh = 1.5
CLah = 3.961586125
CLAh = 0.8 
CLaAh = 7.489196376 
deda = 0 #no downwash over the tail due main wing in front of canard

#Wing geometry: rectangle
S = 12.04 #[m^2]
MAC = 1.72 #[m] The length of the mean aerodynamic cord.


###Stability and Control

#masses - used for potato diagram
OEW = 729 #[kg]
mpayload = 150 #[kg]
mfuel = 92 #[kg]

#Wing pos
xLEMAC = 5 #[m]
lh =  -4.5 #[m], <0 for canard

#CGs of particular masses
x0 = 4.5 #[m]
xcgpayload = 1 #[m]
xcgfuel = xLEMAC + 0.5*MAC #[m]

#Some more XPlot data
SM = 0.05 #Stability Margin (SM)
Vh = 160 #[km/h] Speed of flow over tail is same as over main wing for canard
V = 160 #[km/h] Ratio Vh/V need to be 1.

#V- tail sizing
bv = 1.5 #[m], the span of the v tail, can be chosen accordingly
B = 25 #[deg] The acceptable side slip angle for the aircraft: chosen by engineers.
#lv = lf - ShSmin(3, 'no')[0] #Assuming the Y acts at the end of the fuselage and lv is the length to xLEMAC

"""structural inputs"""
#materials
alpha_Al = 0.8
n_Al = 0.6
sig_y6061 = 280 * 10**6
sig_ult6061 = 338 * 10**6   
E_6061 = 70 * 10**9 
G_6061 = 27 * 10**9

#stringerdimensions
t_s = 0.02 #Stringer thickness
h_s = 0.02 #Stringer dimension



