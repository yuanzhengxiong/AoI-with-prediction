from __future__ import division
import numpy as np

class AoI:
    def __init__(self, arrival_seq):
        self.seq = np.zeros((arrival_seq.size+1,), dtype=int)
        for i, arrival in enumerate(arrival_seq):
            if arrival==0:
                self.seq[i+1] = self.seq[i]+1
        self.max = self.seq.max()
        self.avg = self.seq.mean()
