import numpy as np
from scipy.spatial.transform import Rotation as RT

"""
Parents_      Integer Array         Position data
A_Parent_     Integer Array         Gives Angle Parent of i-th Angle element 
V_Parent_     Integer Array         Gives Value Parent of i-th Angle element
Offset_       2-Tensor              Gives Offset
Use_multiple_ boolean Array         Tells whether bone has more than one vector
A_items_      Integer               Number of Angles per Line
V_items_      Integer               Number of Values per Line   
Item_dict_    Dict of int pairs     Relates multiple angles to their related Values
AtoV_         Dict of integers      Relates a single angle to its related Value

A             3-Tensor Float        Angle Data (BVH)
V             3-Tensor Float        Position values
MS            4-Tensor Float        Rotation Value Single
MM            4-Tensor Float        Rotation Value Aggregated
"""

# This part will become problematic once I start to use numba:
def make_matrix(A): # Makes Rotationmatrix from Euler Angles
    Rot = RT.from_euler('zxy', degrees = True)
    return Rot.as_matrix()

def make_angles(M): # Makes Euler Angles from Rotationmatrix
    Rot = RT.from_matrix(M)
    return Rot.as_euler('zxy', degrees = True)


def matrix_to_angles(self):
    for i in range(self.length_):
        self.A[i,0] = self.C[i]
        for j in range(1,self.A_items_):
            self.A[i,j] = make_angles(self.MS[i,j])
   
   
def angles_to_matrix(self):
    for i in  range(self.length_):
        for j in range(self.A_items_):
            if j==0:
                self.C[i] = self.A[i,0]
                self.M[i,j] = np.identity(3)
            else:
                self.M[i,j] = self.M[i,self.A_Parent_[j]] @  

