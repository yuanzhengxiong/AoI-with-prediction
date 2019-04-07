from __future__ import division
import numpy as np

class AoI:
    def __init__(self, arrival_seq, init_age=0):
        self.cur = init_age
        self.seq = [init_age]
        for arrival in arrival_seq:
            self.op(arrival)
        self.seq = np.array(self.seq) 
        self.max = self.seq.max()
        self.avg = self.seq.mean()
    
    def op(self, arrival): # AoI operator
        self.cur = self.cur+1 if arrival==0 else 0
        self.seq.append(self.cur) 
