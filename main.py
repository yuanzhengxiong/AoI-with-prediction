import numpy as np
import csv
from aoi import AoI
from arrival import Arrival 
from funcs import get_args
import os

def check_path(args):
    path = "/work/LAS/jialiu-lab/zyuan/github-aoi/AoI/data/"
    if not os.path.isdir(path):
        os.mkdir(path)

    if args[0]=='Bernoulli':
        arrival_type, p, w, time_range, avg_num, policy, sew = args
    elif args[0]=='Markovian':
        arrival_type, p1, p2, w, time_range, avg_num, policy, sew = args
    
    path = path+"av_{0}_tr_{1}_ar_{2}/".format(avg_num, time_range, arrival_type)
    if not os.path.isdir(path):
        os.mkdir(path)

    if sew==0:
        path = path+'raw/'
    elif sew==1:
        path = path+'sew/'
    else: sys.exit(-1)
    if not os.path.isdir(path):
        os.mkdir(path)
    
    if args[0]=='Bernoulli':
        path = path+'{0}/'.format(p)
    elif args[0]=='Markovian':
        path = path+'{0}_{1}/'.format(p1, p2)
    if not os.path.isdir(path):
        os.mkdir(path)

    return path

def write_files(path, args):
    if args[0]=='Bernoulli':
        arrival_type, p, w, time_range, avg_num, policy, sew = args
    elif args[0]=='Markovian':
        arrival_type, p1, p2, w, time_range, avg_num, policy, sew = args

    filename = "{0:03d}.csv".format(w)
    with open(path+filename, mode='w') as csv_file:
        if arrival_type=='Bernoulli':
            fieldnames=['i', 'p', 'w', 's', 'avg_age', 'max_age']
        elif arrival_type=='Markovian':
            fieldnames=['i', 'p1', 'p2', 'w', 's', 'avg_age', 'max_age']
        else: sys.exit(-1)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(avg_num):
            if arrival_type=='Bernoulli':
                arrival = Arrival(time_range, arrival_type, p)
            elif arrival_type=='Markovian':
                arrival = Arrival(time_range, arrival_type, p1, p2)
            else: sys.exit(-1)
            if sew==0:
                t = 1
            elif sew==1:
                t = w
            else:
                sys.exit(-1)
            for s in range(t, w+1):
                arrival.initialize_replanned_seq()
                for t in range(0, time_range-w+1, s):
                    arrival.replan(t, w, policy)
                aoi = AoI(arrival.replanned_seq)
                if arrival_type=='Bernoulli':
                    data_dict = {'i': i, 'p': p, 'w': w, 's': s, 'avg_age': aoi.avg, 'max_age': aoi.max}
                elif arrival_type=='Markovian':
                    data_dict = {'i': i, 'p1': p1, 'p2': p2, 'w': w, 's': s, 'avg_age': aoi.avg, 'max_age': aoi.max}
                else: sys.exit(-1)
                writer.writerow(data_dict)
                csv_file.flush()

def write_data(args):
    path = check_path(args)
    write_files(path, args)

def generate_data():
    args = get_args()
    print(args)
    write_data(args)

if __name__ == "__main__":
    generate_data()
