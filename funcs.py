import sys
import argparse

def get_args():
    policy = 'equal_spreading'

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=float)
    parser.add_argument('-p1', type=float)
    parser.add_argument('-p2', type=float)
    parser.add_argument('-w', type=int)
    parser.add_argument('-t', type=int)
    parser.add_argument('-a')
    parser.add_argument('-av', type=int)
    parser.add_argument('-sew', type=int)

    args = parser.parse_args()
    w = args.w
    time_range = args.t
    arrival_type = args.a
    avg_num = args.av
    sew = args.sew

    if(arrival_type=='Bernoulli'):
        p = args.p
        return [arrival_type, p, w, time_range, avg_num, policy, sew]
    elif(arrival_type=='Markovian'):
        p1 = args.p1
        p2 = args.p2
        return [arrival_type, p1, p2, w, time_range, avg_num, policy, sew]
    else:
        print("No such arrival type.")
        sys.exit(-1)

def get_reverse(seq):
    rev = [x for x in seq]
    rev.reverse()
    return rev

