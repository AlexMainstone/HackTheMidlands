# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt

class SIR(object):
    
    def __init__(self, S, I, R, beta, gamma):
        self.S = S
        self.I = I
        self.R = R
        
        self.beta = beta
        self.gamma = gamma
        
        self.N = S+I+R
        self.T = 0
        
    def event_S_I(self):
        self.S -= 1
        self.I += 1
    
    def event_I_R(self):
        self.I -= 1
        self.R += 1
        
    def get_population(self):
        return (self.S, self.I, self.R, self.T)
    
    def rate_SI(self):
        return self.beta * self.I * self.S / self.N
    
    def rate_IR(self):
        return self.gamma * self.I / self.N
    
    def next_event(self):
        X = np.random.uniform(size=2)
        
        r_SI = self.rate_SI()
        r_IR = self.rate_IR()
        try:
            dt_SI = (-1/r_SI) * np.log(X[0])
        except:
            dt_SI = np.inf
        try:
            dt_IR = (-1/r_IR) * np.log(X[1])
        except:
            dt_IR = np.inf
        
        if dt_SI <= dt_IR:
            if self.S != 0:
                self.event_S_I()
            self.T += dt_SI
            
        else: 
            if self.I != 0:
                self.event_I_R()
            self.T += dt_IR
                
        

sir = SIR(100, 1, 0, beta=10, gamma=12)

S = []
I = []
R = []
T = []

for _ in range(5000):

    (s,i,r,t) = sir.get_population()
    S.append(s)
    I.append(i)
    R.append(r)
    T.append(t)
    

    sir.next_event()

    
      
plt.plot(T, S, c='g')
plt.plot(T, I, c='r')
plt.plot(T, R, c='k')
plt.show()