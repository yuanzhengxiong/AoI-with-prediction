from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import csv
from aoi import AoI
from arrival import Arrival 
from funcs import parse_args

seed = 3
reset_val = 0

def show_policy_effect():
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

def test_equal_spreading():
    avg_num = int(1e3) 
    time_range = int(1e3)
    arrival_type = 'Bernoulli'
    policy = 'equal_spreading'
    with open('./data/data_for_equal_spreading.csv', mode='w') as csv_file:
        fieldnames=['w', 's', 'p', 'T', 'avg_age', 'max_age'] 
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for p in [x/10 for x in range(5, 6)]:
            for w in range(67, 101):
                for s in range(1, w+1):
                    aoi_avgs = []
                    aoi_maxs = []
                    for i in range(avg_num):
                        arrival = Arrival(time_range, arrival_type, p) 
                        for t in range(0, time_range-w+1, s):
                            arrival.replan(t, w, policy)
                        aoi = AoI(arrival.seq)
                        aoi_avgs.append(aoi.avg)
                        aoi_maxs.append(aoi.max)

                    data_dict = {'w': w, 's': s, 'p': p, 'T': time_range, 'avg_age': sum(aoi_avgs)/avg_num, 'max_age': sum(aoi_maxs)/avg_num}
                    print data_dict
                    writer.writerow(data_dict)

if __name__ == "__main__":
    #show_policy_effect()
    test_equal_spreading()
