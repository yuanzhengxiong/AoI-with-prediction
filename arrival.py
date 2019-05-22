import itertools
import numpy as np
import random
import sys
from aoi import AoI
from equalize import equalize

class Arrival:
    def __init__(self, time_range, arrival_type, p):
        self.time_range = time_range
        self.seq = []
        if(arrival_type == "Bernoulli"):
            self.seq = np.random.binomial(1, p, time_range)
        elif(arrival_type == "Markovian"):
            transition_matrix = np.array([[1-p, p], [p, 1-p]])
            initial_state = random.randint(0, 1) 
            self.seq = MarkovChain(transition_matrix).generate_seq(initial_state=initial_state, length=time_range)
        elif(arrival_type == "test"):
            self.seq=[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        self.replanned_seq = list(self.seq)
    
    def initialize_replanned_seq(self):
        self.replanned_seq = list(self.seq)

    def get_inter_arrival_time_seq(self):
        inter_seq = []
        i = 0
        first = 1
        for j, n in enumerate(self.replanned_seq):
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
            for j, x in enumerate(self.replanned_seq[t:t+window_size]):
                if x==1:
                    if j!=i:
                        self.replanned_seq[t+i] = 1
                        self.replanned_seq[t+j] = 0
                    i = i+1
        elif(policy == "receding_horizon_control"):
            min_sum = self.replanned_age_sum(t, np.zeros(window_size), aoi.seq[t])
            for arr in itertools.permutations(self.replanned_seq[t:t+window_size]):
                window_age_sum = self.replanned_age_sum(t, np.asarray(arr), aoi.seq[t])
                if(window_age_sum <= min_sum):
                    min_sum = window_age_sum
                    replanned_arrival = np.array(arr)
            self.replanned_seq[t:t+window_size] = replanned_arrival
            return self.replanned_age_sum(t, self.replanned_seq[t:t+window_size], aoi.seq[t])
        elif(policy == "equal_spreading"):
            l = len(self.replanned_seq[t:t+window_size])
            n = sum(self.replanned_seq[t:t+window_size])
            replanned_arrival = np.array(equalize(l, n))
            # print l, n, replanned_arrival
            self.replanned_seq[t:t+window_size] = replanned_arrival
        else:
            print "Error: no such policy yet."
            sys.exit(2)
            
class MarkovChain:
    def __init__(self, transition_matrix):
        self.transition_matrix = transition_matrix;
        
    def next_state(self, current_state):
        return np.random.choice([0,1], p=self.transition_matrix[current_state, :])
    
    def generate_seq(self, initial_state, length):
        seq = []
        current_state = initial_state
        for i in range(length):
            next_state = self.next_state(current_state)
            seq.append(next_state)
            current_state = next_state
        return seq 
