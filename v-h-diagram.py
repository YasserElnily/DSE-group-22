# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:12:47 2020

@author: jappe
"""

from numpy import *
from matplotlib import pyplot as plt
from ISA_calculator import ISA
h=0
rho=ISA[2]
A=6
e=0.8
k=1/(pi()*A*e)

def v(C_L, W, S, rho):
    return sqrt((W*2)/(S*rho*C_L))
def