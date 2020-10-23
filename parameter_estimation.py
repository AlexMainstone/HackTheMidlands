#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 03:35:28 2020

@author: francesco
"""

import numpy as np
from sklearn.linear_model import Linear_Regression
import matplotlib.pyplot as plt

S = []
I = []
R = []

T = []
def estimate(T, I):
    T = np.array(T).reshape(-1, 1)
    I = [np.log(i) - np.log(I[0]) for i in I]
    
    regr = Linear_Regression(fit_intercept = False)
    regr.fit(T, I)
    return regr.coef_[0]

