# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:44:59 2020

@author: jappe
"""

from numpy import *
from matplotlib import pyplot as plt
from ISA_calculator import ISA
from v_max_calculator import get_max_velocity

h=0
rho=ISA(h)[2]
A=4
e=0.8
k=1/(pi*A*e)
P_a_max=10000# Watt
S=11
W=1100*9.81
C_D_0=0.03

data = (P_a_max, k, S, W, C_D_0)

results2= get_max_velocity(h, data)
print(results2)