# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:12:47 2020

@author: jappe
"""

from numpy import *
from matplotlib import pyplot as plt
from ISA_calculator import ISA
from scipy.optimize import fsolve

h=0
rho=ISA(h)[2]
A=6
e=0.8
k=1/(pi*A*e)
P_a_max=200000# Watt
S=9
W=1100*9.81
C_D_0=0.03

def v(C_L, W, S, rho):
    return sqrt((W*2)/(S*rho*C_L))

def C_L_function(C_L, *data):        # https://stackoverflow.com/questions/19843116/passing-arguments-to-fsolve
    P_a_max, S, rho, W, k, C_D_0 = data
    return C_L**4 - (P_a_max**2 * S * rho/(2*W**3))*C_L**3 + 2*k*C_D_0*C_L**2 - C_D_0**2

def get_solution(P_a_max, S, rho, W, k, C_D_0):
    initial_guess = 1
    data = (P_a_max, S, rho, W, k, C_D_0)
    solutions = fsolve(C_L_function, initial_guess, args=data, full_output = 1)
    return solutions
    
result =get_solution(P_a_max, S, rho, W, k, C_D_0)
print(result)

n = 1000
C_L_x = linspace(-5, 10, n)
fx = empty(n)
for i in range(n):
    fx[i]=C_L_function(C_L_x[i], P_a_max, S, rho, W, k, C_D_0)
    
plt.plot(C_L_x, fx)
plt.plot([-4,4],[0,0],'r-')
plt.ylim([-0.01,0.01])
plt.show()