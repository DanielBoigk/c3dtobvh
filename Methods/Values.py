import numpy as np

import Geometry as G

"""
Parents_      Integer Array         Position data
A_Parent_     Integer Array         Gives Angle Parent of i-th Angle element 
V_Parent_     Integer Array         Gives Value Parent of i-th Angle element
Offset_       2-Tensor              Gives Offset
Use_multiple_ boolean Array         Tells whether bone has more than one vector
Is_zero_      boolean Array         Tells whether the bone has length zero
A_items_      Integer               Number of Angles per Line
V_items_      Integer               Number of Values per Line   
Item_dict_    Dict of int pairs     Relates multiple angles to their related Values
AtoV_         Dict of integers      Relates a single angle to its related Value
VtoA_         Array of integers     Relates V Values to their respective A Value

A             3-Tensor Float        Angle Data (BVH)
V             3-Tensor Float        Position values
MS            4-Tensor Float        Rotation Value Single
MM            4-Tensor Float        Rotation Value Aggregated

length_       Integer               Lines of the BVH File
"""
#Position to Vectors in between and the reverse
def VS_to_V_line(self, i):
    V[i,0] = VS[i,0]
    for j in range(1,self.V_items_):
        V[i,j] = VS[i,j] + VS[i,self.V_Parent_[j]]
    
def V_to_VS_line(self, i):
    VS[i,0] = V[i,0]
    for j in range(1, self.V_items_):
        VS[i,j] = V[i,j] - V[i,self.V_Parent_[j]]

def VS_to_V(self):
    for i in range(self.length_):
        VS_to_V_line(i)

def V_to_VS(self):
    for i in range(self.length_):
        V_to_VS_line(i)

#Matrix to Position and the other way around
def MM_to_VS_line(self, i):
    for j in range(1, self.V_items_):
        self.VS[i,j] = self.MM[i,VtoA_[j]] @ self.Offset_[j] #Maybe the other way around

def MM_to_VS(self):
    for i in range(self.length_):
        MM_to_VS_line(i)
#The complicated Stuff: 

def VS_to_MM_line(self, i):
    self.MM[i,0] = np.identity(3)
    for j in range(1, self.A_items_):
        if self.Is_zero[i,j]:
            self.MS[i,j] = np.identity(3)
        elif self.Use_multiple[i,j] == False:
            o1 = self.Offset_[self.AtoV_[j]] @ self.MM[i,self.A_Parent_[j]]
            v1 = self.VS[i,self.AtoV_[j]]
            self.MS[i,j] = self.single_vec(o1, v1)
        else:
            o1 = self.Offset_[Item_dict_[j][0]] @ self.MM[i,self.A_Parent_[j]]
            o2 = self.Offset_[Item_dict_[j][1]] @ self.MM[i,self.A_Parent_[j]]
            v1 = self.VS[i,self.Item_dict_[j][0]]
            v2 = self.VS[i,self.Item_dict_[j][1]] 
            self.MS[i,j] = self.multi_vec(o1, o2, v1, v2)
        self.MM[i,j] = self.MS[i,j] @ self.MM[i,A_Parent_[j]] 
            
def VS_to_MM(self):
    for i in range(self.length_):
        VS_to_MM_line(i)
        