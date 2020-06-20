 #-*- coding: utf-8 -*-
"""
Created on Sat June 20 10:13:00 2020

@author: Elise
"""

#imports
import matplotlib.pyplot as plt
import numpy as np
ROC_VTOL= 5*60 #m/min
ROC_trans = 1*60 #m/min
ROC_horiz = 2.5*60 #m/min
V_cruise = 61*60 #m/min
ROD_horiz =2*60 #m/min
ROD_trans = 1*60 #m/min
ROD_VTOL = 1*60 #m/s

hmax = 3048# m
hmin = 304.8

Endurance =3*60 #min
Divergeendurance = 45 #min
Range = 300*1000 #m

#from start to end of VTOL
h1 = 5 #m set by Kushagra book
t1 = h1/ROC_VTOL

#from VTOL to end of transition
#h2 = 11 #m #V2
t2 = 5 # 5 mins for full VTOL power
h2 = ROC_trans*t2

# end of transition to end of horizontal climb
t3_min = t2+ (hmin-h2)/ROC_horiz
t3_max = t2+(hmax-h2)/ROC_horiz


#end VTOL
t_end = Endurance

#VTOL to end
h6 = 5#m
t6 = t_end - h6/ROD_VTOL

#transition to vtol
t5 = t6 - 5 #min for full VTOL power
h5 = h6 + ROD_trans*(t6-t5)

#horizontal to transition
t4_max = t5 - hmax/ROD_trans
t4_min = t5 - hmin/ROD_trans




# """
# #cruise profiles
timemax = [0, t1, t2, t3_max,t4_max, t5, t6, t_end]
timemin = [0, t1, t2, t3_min,t4_min, t5, t6, t_end]
altitudemax = [0, h1, h2, hmax, hmax,h5, h6, 0]
altitudemin = [0, h1, h2, hmin, hmin, h5, h6,  0]
#
#loiter
#
hl = hmin
tl = t_end + Divergeendurance - hmin/ROD_trans

tloiter = [t5,tl,t_end+Divergeendurance]
altitudeloiter = [hmin,hl,0]
#altitudeloiter = [304.8, 304.8, 0]
#
# Example flight
ROC_horiz_examp = 2*60
hexam = 1500 #m
hlexam = 600
tlexam = t_end +Divergeendurance - hexam/ROD_horiz
texam = t2+ (hexam-h2)/(ROC_horiz_examp)
texam2 = t5 - hexam/ROD_trans
timeexamp = [0,t1,t2,texam,texam2,t5,tlexam,t_end+Divergeendurance]
examplealts = [0,h1,h2,hexam,hexam,hlexam,hlexam,0]
#timeexamp = [0, 20, 160, 175, 215, 225]
#
 #plotting results
plt.title("Flight mission profile")
plt.ylabel("Altitude [m]")
plt.xlabel("Time [min]")
plt.xlim(0, 225)
plt.ylim(0, 3500)
plt.plot(timemax, altitudemax, label = "Cruise at service ceiling")
plt.plot(timemin, altitudemin, label = "Cruise at minimum altitude")
plt.plot(tloiter, altitudeloiter, label = "Loitering and diverting")
plt.plot(timeexamp, examplealts, label = "Example flight", linestyle='dashed')
plt.legend()
plt.grid()
plt.show()



