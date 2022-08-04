import numpy as np
from Values import make_use



Names =     [0,1,2,3,4,5,6,7,8,9]
Parents =  [-1,0,1,2,3,4,3,6,0,8]
Depth =     [0,1,2,3,4,5,4,5,2,3]
sol =       [0,1,2,3,4,5,4,6,1,7]
V_items = 10
A_items = 8
print(sol)
print(make_use(Parents, Depth, A_items, V_items))