from __future__ import division
from random import shuffle
from funcs import get_reverse
import random

def equalize(l, n):
    #if (n == l/2):
    #    return random.choice([[0,1], [1,0]])*n
    #if (n > l/2):
    #    return [1-x for x in equalize(l, l-n)]
    b = (l-n)%(n+1) 
    k = (l-n)//(n+1)
    zero_nums = [k]*(n+1-b)+[k+1]*b         
    shuffle(zero_nums)
    ret = []
    for x in zero_nums:
        ret = ret+[0]*x+[1] 
    return ret[:-1]

# def equalize(l, n):
#     if (n==0):
#         return [0]*l
#     if (l==n):
#         return [1]*l
#     if (l==2):
#         return random.choice([[1, 0], [0, 1]])
#     if (n==1):
#         if (l%2==0):
#             return random.choice([equalize(l-1, 1)+[0], [0]+equalize(l-1, 1)])
#         else:
#             return [0]*(l//2)+[1]+[0]*(l//2)
#     if (n>l/2):
#         return [1-x for x in equalize(l,l-n)]
#     if (n==l/2):
#         return random.choice([[0,1]*n, [1,0]*n]) 
#     if (n+n+1==l):
#         return [0,1]*n+[0]
# 
#     if (l==6):
#         if (n==2):
#             return [0,1,0,0,1,0]
#     if (l==7):
#         if (n==2):
#             return [0,0,1,0,1,0,0]
#     if (l==8):
#         if (n==2):
#             return [0,0,1,0,0,1,0,0]
#         if (n==3):
#             return [0]+[1]+random.choice([[0]+[1]+[0,0], [0,0]+[1]+[0]])+[1]+[0]
#     if (l==9):
#         if (n==2):
#             return [0,0,1,0,0,0,1,0,0]
#         if (n==3):
#             return random.choice([[0,0,1,0,1,0,1,0,0], [0,1,0,0,1,0,0,1,0]])
#     if (l==10):
#         if (n==2):
#             return random.choice([[0]+equalize(9,2), equalize(9,2)+[0]])
#         if (n==3):
#             return [0]*2+[1]+random.choice([[0]+[1]+[0,0], [0,0]+[1]+[0]])+[1]+[0]*2
#         if (n==4):
#             return equalize(5,2)*2
            
        
# def equalize(l, n):
#     if (n==0):
#         return [0]*l
#     if (l==n):
#         return [1]*l
#     if (l==2):
#         return random.choice([[1, 0], [0, 1]])
#     if (n==1 and l%2==0):
#         return random.choice([equalize(l-1, 1)+[0], [0]+equalize(l-1, 1)])
# 
#     if (l%2 != 0): # l is odd, l >= 3
#         if (n%2 != 0): # n is odd
#             return equalize(l//2, n//2)+[1]+equalize(l//2, n//2)
#         else: # n is even
#             return equalize(l//2, n//2)+[0]+equalize(l//2, n//2)
#     else: # l is even, l >= 4
#         if (n<=l/2): 
#             if (n%2==0): # n is even
#                 return random.choice([equalize(l-1, n)+[0], [0]+equalize(l-1, n)])
#                 # return equalize(l//2, n//2)+equalize(l//2, n//2)
#             else: # n is odd
#                 # method 1
#                 l1 = equalize(l//2, (n-1)//2)
#                 l2 = equalize(l//2, (n+1)//2)
#                 return random.choice([l1+l2, l2+l1])
#                 # method 2
#                 
#         else:
#             return [1-x for x in equalize(l, l-n)]
