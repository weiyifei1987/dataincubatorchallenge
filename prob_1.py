# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:18:06 2016

@author: Yifei Wei
"""

import numpy as np
from decimal import *
getcontext().prec = 50

# T numbers in total and N numbers in a register
def M_L(T,N): # calculate M-L
    # --------------------------------------
    # Generate a series of random numbers ( “discrete uniform” distribution)
    Series = np.random.random_integers(1,high=10, size=T)
    # Last register
    last_register = Series[-N:]
    # Max register
    temp = Series.copy()
    temp.sort()
    max_register = temp[-N:]
        
    
    # --------------------------------------
    # M: product of max register
    M = np.prod(max_register)
    # L: product of last register
    L = np.prod(last_register)
    return M-L
    
# a: lower bound; b: upper bound
def avg_std(T,N,a, b):    
    Array = []
    for i in range(10000):
        # iterate for 10000 times to generate relatively consistant results
        Array.append(M_L(T,N))
    Array = np.array(Array)
    Array.astype(np.float64)    
    # calculate probability
    con_prob = np.all([Array>=a,Array>=b], axis=0).astype(np.float64).sum()/len(Array)
    # calculate mean and std
    Avg = Array.mean()
    Std = Array.std()
    return np.array([Avg,Std,con_prob])
result_1 = avg_std(8,2,32,64)
result_2 = avg_std(32,4,2048,4096)
print result_1, result_2

# --------------------------------------------
