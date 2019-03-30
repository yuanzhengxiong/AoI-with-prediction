from __future__ import division
import sys, getopt

def parse_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hw:t:a:l:p:s:", ["window_size=", "time_range=", "arrival_type=", "lambda=","policy=", "step_size="])
    except getopt.GetoptError:
        print 'python main.py -w <window_size> -t <time_range> -a <arrival_type> -l <lambda> -p <policy> -s <step_size>' 
        sys.exit(2)
    window_size = ''
    time_range = ''
    arrival_type = ''
    lam = ''
    policy = ''
    step_size=""
    for opt, arg in opts:
        if opt == '-h':
            print 'python main.py -w <window_size> -t <time_range> -a <arrival_type> -l <lambda> -p <policy> -s <step_size>' 
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
