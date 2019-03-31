from __future__ import division
from funcs import get_reverse
import random

def equalize(l, n):
    if (n==0):
        return [0]*l
    if (l==n):
        return [1]*l
    if (l==2):
        return random.choice([[1, 0], [0, 1]])
    if (n==1 and l%2==0):
        return random.choice([equalize(l-1, 1)+[0], [0]+equalize(l-1, 1)])

    if (l%2 != 0): # l is odd, l >= 3
        if (n%2 != 0): # n is odd
            return equalize(l//2, n//2)+[1]+equalize(l//2, n//2)
        else: # n is even
            return equalize(l//2, n//2)+[0]+equalize(l//2, n//2)
    else: # l is even, l >= 4
        if (n<=l/2): 
            if (n%2==0): # n is even
                return equalize(l//2, n//2)+equalize(l//2, n//2)
            else: # n is odd
                # method 1
                l1 = equalize(l//2, (n-1)//2)
                l2 = equalize(l//2, (n+1)//2)
                return random.choice([l1+l2, l2+l1])
                # method 2
                
        else:
            return [1-x for x in equalize(l, l-n)]
