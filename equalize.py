from __future__ import division
from random import shuffle
from funcs import get_reverse
import random

def equalize(l, n):
    if n==0:
        return [0]*l
    if l==n:
        return [1]*l
    if n > l/2:
        return [1-x for x in equalize(l, l-n)]
    b = (l-n)%(n+1) 
    k = (l-n)//(n+1)
    zero_nums = [k]*(n+1-b)+[k+1]*b         
    shuffle(zero_nums)
    ret = []
    for x in zero_nums:
        ret = ret+[0]*x+[1] 
    return ret[:-1]
