# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 12:26:57 2021

@author: Jonas
"""

qs  = list(range(100, 205, 5))
ps = []
prod = []
cnst = 1.5 * 150 ** 3
for q in qs:
    p = int(cnst/(q * q))
    ps += [p]
    prod += [p * q * q]

mx = prod[0]
mn = prod[0]
for x in prod[1:]:
    if x < mn:
        mn = x
    elif x > mx:
        mx = x
print(qs)
print(ps)
print(prod)
print((mx-mn)/mx)
print(qs[int(len(qs)/2)])

    