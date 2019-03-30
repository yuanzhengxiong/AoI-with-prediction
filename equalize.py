from __future__ import division
from funcs import get_reverse

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
