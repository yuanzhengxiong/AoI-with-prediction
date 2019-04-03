from __future__ import division
from random import shuffle
from funcs import get_reverse
import random

def equalize(l, n):
    b = (l-n)%(n+1) 
    k = (l-n)//(n+1)
    zero_nums = [k]*(n+1-b)+[k+1]*b         
    shuffle(zero_nums)
    ret = []
    for x in zero_nums:
        ret = ret+[0]*x+[1] 
    return ret[:-1]
