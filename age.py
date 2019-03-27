from __future__ import division
import random
import numpy as np
import matplotlib.pyplot as plt
import pickle
import itertools
import sys, getopt

seed = 3
reset_val = 0

def parse_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hw:t:a:l:p:s:", ["window_size=", "time_range=", "arrival_type=", "lambda=","policy=", "step_size="])
    except getopt.GetoptError:
        print 'age.py -w <window_size> -t <time_range> -a <arrival_type> -l <lambda> -p <policy> -s <step_size>' 
        sys.exit(2)
    window_size = ''
    time_range = ''
    arrival_type = ''
    lam = ''
    policy = ''
    step_size=""
    for opt, arg in opts:
        if opt == '-h':
            print 'age.py -w <window_size> -t <time_range> -a <arrival_type> -l <lambda> -p <policy>' 
            sys.exit()
        elif opt in ('-w', '--window_size'):
            window_size = int(arg)
        elif opt in ('-t', '--time_range'):
            time_range = int(arg)
        elif opt in ('-a', '--arrival_type'):
            arrival_type = arg
        elif opt in ('-l', '--lambda'):
            lam = float(arg)
        elif opt in ('-p', '--policy'):
            policy = arg
        elif opt in ('-s', '--step_size'):
            step_size = int(arg)
    return window_size, time_range, arrival_type, lam, policy, step_size

def get_reverse(seq):
    rev = [x for x in seq]
    rev.reverse()
    return rev

def equalize(l, n):
    if (n==0):
        return [0]*l
    if (l==n):
        return [1]*l
    if (l==2):
        return [1, 0]

    if (l%2 != 0): # l is odd, l >= 3
        if (n%2 != 0): # n is odd
            half = equalize(l//2, n//2)
            return half+[1]+get_reverse(half)
        else: # n is even
            half = equalize(l//2, n//2)
            return half+[0]+get_reverse(half)
    else: # l is even, l >= 4
        if (n==l/2): 
            if (n%2==0): # n is even
                half = equalize(l//2, n//2)
                return half+get_reverse(half)
            else: # n is odd
                return equalize(l-1, n)+[0]
        elif (n<l/2):
            if (n%2 != 0): # n is odd
                return equalize(l-1, n)+[0]
            else: # n is even
                half = equalize(l//2, n//2)
                return half+get_reverse(half)
        else:
            return [1-x for x in equalize(l, l-n)]

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
    
    def replan(self, t, window_size, policy, aoi):
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
            
        return self.replanned_age_sum(t, self.seq[t:t+window_size], aoi.seq[t])
        
class AoI:
    def __init__(self, arrival_seq, init_age=0):
        self.cur = init_age
        self.seq = [init_age]
        for arrival in arrival_seq:
            self.op(arrival)
        self.max = max(self.seq)
        self.avg = sum(self.seq)/len(self.seq)
    
    def op(self, arrival): # AoI operator
        self.cur = self.cur+1 if arrival==0 else reset_val
        self.seq.append(self.cur) 

def main():
    window_size, time_range, arrival_type, lam, policy, step_size = parse_args()
    np.random.seed(seed)

    print " "
    print "##########  NO REPLAN POLICY  ##########"
    print " "
    arrival = Arrival(time_range, arrival_type, lam) 
    aoi = AoI(arrival.seq, 0)
    print "arrival sequence: ", arrival.seq
    print "number of arrivals: ", sum(arrival.seq)
    inter_seq = arrival.get_inter_arrival_time_seq() 
    print "inter arrival time sequence: ", inter_seq
    print "max inter arrival time", max(inter_seq)
    print "MAX AGE: ", aoi.max
    print "AVG AGE: ", aoi.avg

    fig, axs = plt.subplots(2, sharex=True)
    x = range(-1, time_range+1)
    axs[0].scatter(x[1:-1], arrival.seq, label='arrival')
    axs[1].step(x, [0]+aoi.seq, label='age') 

    print " "
    print "##########  APPLY REPLAN POLICY  ##########"
    print " "
    print "WINDOW SIZE: ", window_size
    print "POLICY: ", policy
    for t in range(0, time_range-window_size+1, step_size):
        arrival.replan(t, window_size, policy, aoi)
        
    aoi = AoI(arrival.seq)
    print "arrival sequence: ", arrival.seq
    print "number of arrivals: ", sum(arrival.seq)
    inter_seq = arrival.get_inter_arrival_time_seq() 
    print "inter arrival time sequence: ", inter_seq
    print "max inter arrival time", max(inter_seq)
    print "MAX AGE: ", aoi.max
    print "AVG AGE: ", aoi.avg

    axs[0].scatter(x[1:-1], arrival.seq, color='red', marker='^', label='reshaped arrival')
    axs[1].step(x, [0]+aoi.seq, color='red', label='reshaped age') 

    axs[0].legend()
    axs[1].legend()
    plt.xlim(-1, time_range)
    plt.savefig(arrival_type+'_t_'+str(time_range)+'_p_'+str(lam)+'_w_'+str(window_size)+'_s_'+str(step_size)+'.png')

    plt.show()

if __name__ == "__main__":
    main()
