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

