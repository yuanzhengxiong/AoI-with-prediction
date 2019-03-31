from equalize import equalize
import sys

l = equalize(int(sys.argv[1]), int(sys.argv[2]))

print l

def get_inter_arrival_time_seq(seq):
    i = 0
    inter_seq = []
    for j, n in enumerate(seq):
        j = j+1
        if n==1: 
            inter_seq.append(j-i) 
            i = j
    inter_seq.append(len(seq)+1-i)
    
    return inter_seq

print get_inter_arrival_time_seq(l)
