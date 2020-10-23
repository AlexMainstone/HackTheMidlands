#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 03:35:28 2020

@author: francesco
"""

import numpy as np
from sklearn.linear_model import LinearRegression

def estimate(T, S, I, R):
    
    T = np.array(T).reshape(-1, 1)
    log_I = [np.log(i) - np.log(I[0]) for i in I]
    
    regr0 = LinearRegression(fit_intercept = False)
    regr0.fit(T, log_I)
    
    beta_gamma = regr0.coef_[0]
    
    log_ratio = [np.log(i/I[0]) for i in I]
    
    regr1 = LinearRegression(fit_intercept = False)
    
    regr1.fit(T, log_ratio)
    
    m_hat = regr1.coef_
    
    beta = (m_hat - beta_gamma) / (S[-1]/(S[-1] + I[-1] + R[-1]) - 1)
    gamma = (m_hat - beta_gamma * S[-1]/(S[-1] + I[-1] + R[-1])) / (S[-1]/(S[-1] + I[-1] + R[-1]) - 1)
    
    return beta, gamma

