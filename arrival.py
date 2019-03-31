import itertools
import numpy as np
import sys
from aoi import AoI
from equalize import equalize

class Arrival:
    def __init__(self, time_range, arrival_type, lam):
        self.time_range = time_range
        self.seq = []
        if(arrival_type == "Bernoulli"):
            self.seq = np.random.binomial(1, lam, time_range)
        elif(arrival_type == "test"):
            self.seq=[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]

    def get_inter_arrival_time_seq(self):
        inter_seq = []
        i = 0
        first = 1
        for j, n in enumerate(self.seq):
            if n==1: 
                if first==1:
                    i = j
                    first = 0
                else:
                    inter_seq.append(j-i) 
                    i = j
                    
        return inter_seq    
    
    def replanned_age_sum(self, t, replanned_arrival, init_age):
        replanned_window_aoi = AoI(replanned_arrival, init_age) 
        return sum(replanned_window_aoi.seq)-init_age
    
    def replan(self, t, window_size, policy, aoi=''):
        if(policy == "all_shift_to_earliest"):
            i = 0
            for j, x in enumerate(self.seq[t:t+window_size]):
                if x==1:
                    if j!=i:
                        self.seq[t+i] = 1
                        self.seq[t+j] = 0
                    i = i+1
        elif(policy == "receding_horizon_control"):
            min_sum = self.replanned_age_sum(t, np.zeros(window_size), aoi.seq[t])
            for arr in itertools.permutations(self.seq[t:t+window_size]):
                window_age_sum = self.replanned_age_sum(t, np.asarray(arr), aoi.seq[t])
                if(window_age_sum <= min_sum):
                    min_sum = window_age_sum
                    replanned_arrival = np.array(arr)
            self.seq[t:t+window_size] = replanned_arrival
        elif(policy == "equalize_window"):
            l = len(self.seq[t:t+window_size])
            n = sum(self.seq[t:t+window_size])
            replanned_arrival = np.array(equalize(l, n))
            # print l, n, replanned_arrival
            self.seq[t:t+window_size] = replanned_arrival
        else:
            print "Error: no such policy yet."
            sys.exit(2)
            
        return self.replanned_age_sum(t, self.seq[t:t+window_size], aoi.seq[t])
