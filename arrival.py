import itertools
import numpy as np
import random
import sys
from aoi import AoI
from equalize import equalize

class Arrival:
    def __init__(self, time_range, arrival_type, p1, p2=0.0):
        self.time_range = time_range
        self.seq = []
        if(arrival_type == "Bernoulli"):
            self.seq = list(np.random.binomial(1, p1, time_range))
        elif(arrival_type == "Markovian"):
            transition_matrix = np.array([[1-p1, p1], [p2, 1-p2]])
            s0 = p2/(p1+p2)
            s1 = p1/(p1+p2)
            initial_state = np.random.choice([0,1], p=[s0, s1]) 
            self.seq = MarkovChain(transition_matrix).generate_seq(initial_state=initial_state, length=time_range)
        elif(arrival_type == "test"):
            self.seq=[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        self.replanned_seq = list(self.seq)
    
    def initialize_replanned_seq(self):
        self.replanned_seq = list(self.seq)
    
    def replanned_age_sum(self, t, replanned_arrival, init_age):
        replanned_window_aoi = AoI(replanned_arrival, init_age) 
        return sum(replanned_window_aoi.seq)-init_age
    
    def replan(self, t, window_size, policy, aoi=''):
        if(policy == "equal_spreading"):
            l = len(self.replanned_seq[t:t+window_size])
            n = sum(self.replanned_seq[t:t+window_size])
            replanned_arrival = equalize(l, n)
            self.replanned_seq[t:t+window_size] = replanned_arrival
        else:
            print("Error: no such policy yet.")
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
