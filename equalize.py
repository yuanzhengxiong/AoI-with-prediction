from __future__ import division
#from random import shuffle
from funcs import get_reverse
import random
import numpy as np

def equalize(l, n):
    if n==0:
        return np.zeros((l,), dtype=int)
    if l==n:
        return np.ones((l,), dtype=int)
    if n > l/2:
        return 1-equalize(l, l-n)
    b = (l-n)%(n+1) 
    k = (l-n)//(n+1)
    zero_nums = np.concatenate((np.zeros((n+1-b,), dtype=int)+k,np.zeros((b,), dtype=int)+(k+1)))
    np.random.shuffle(zero_nums)
    ret = np.zeros((l,), dtype=int)
    t = 0
    for x in zero_nums[:-1]:
        ret[t+x] = 1
        t = t+x+1
    return ret
