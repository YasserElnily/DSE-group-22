# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:44:59 2020

@author: jappe
"""

from numpy import *
from matplotlib import pyplot as plt
from ISA_calculator import ISA
from v_max_calculator import get_max_velocity


rho=ISA(h)[2]
A=4
e=0.8
k=1/(pi*A*e)
P_a_max=10000# Watt
S=11
W=1100*9.81
C_D_0=0.03
data = (P_a_max, k, S, W, C_D_0)
n=4000
h = linspace(0,4000, n)

v_max_line = zeros(h.shape)
v_min_line = zeros(h.shape)

for i in range(n):
    v_max_line[i] = get_max_velocity(h[i], data)
    v_min_line[i] = get_min_velocity(h[i], data)
    
    



results2= get_max_velocity(h, data)
