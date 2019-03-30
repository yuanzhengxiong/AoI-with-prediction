from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from aoi import AoI
from arrival import Arrival 
from funcs import parse_args

seed = 3
reset_val = 0

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