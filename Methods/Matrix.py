import numpy as np

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

length_       Integer               Lines of the BVH File
"""


def MS_to_MM_line(self ,i): #Converts on Line of single Matrices into aggregated Matrices
    for j in range(self.A_items_):
        if j==0:
            self.MM[i,0] = np.idendity(3)
        else:
            self.MM[i,j] = self.MS[i,j] @ self.MM[i,A_Parent_[j]]     # Maybe false Order


def MM_to_MS_line(self, i): #Converts on Line of aggregated Matrices into single Matrices
    for j in range(self.A_items_):
        if j==0:
            self.MS[i,0] = np.idendity(3)
        else:
            self.MS[i,j] = self.MM[i,j] @ self.MM[i,A_Parent_[j]].T    # Maybe false Order


def update_MM(self,i,j, M): #Updates a single aggregated Matrix
    self.MM[i,j] = M
    self.MS[i,j] = M @ self.MM[i,A_Parent_[j]].T    # Maybe false Order

def update_MS(self,i,j, M): # Updated a single single Matrix
    self.MS[i,j] = M
    self.MM[i,j] = M @ self.MM[i,A_Parent_[j]]      # Maybe false Order

def MS_to_MM(self): # Converts all single Matrices to aggegated Matrices
    for i in range(self.length_):
        self.MS_to_MM_line(i):


def MM_to_MS(self): # Converts all aggregated Matrices to single Matrices
    for i in range(self.length_):
        self.MM_to_MS_line(i):



def Orthonormalize(self):
    print("To be implemented")