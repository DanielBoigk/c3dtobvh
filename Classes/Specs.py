import numpy as np

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

class Specs():
    def __init__(self,Parents, Offset):
        self.length_ = 1
        self.V_items_ = 1
        self.A_items_ = 1
        print("To be implemented")
        if len(Parents) > 1:
            self.Parents = Parents
            self.Offset = Offset
            self.V_items = self.Parents.shape[0]
            self.multiplicity = np.zeros(self.V_items, dtype = "int64")
            # Extract number of A_items from parent list
            self.A_items = self.V_items
            for i in self.Parents:
                self.multiplicity[i] += 1
                if self.multiplicity[i] > 1:
                    self.A_items -= 1
            self.multiplicity[-1] = 0

            self.Use_multiple = np.zeros((self.A_items), dtype = "bool")
            self.A_Parent = np.zeros((self.A_items), dtype= "int64")
            self.V_Parent = np.zeros((self.A_items), dtype= "int64")
            self.Item_dict = {}
            self.AtoV = {}

            self.is_init = False
        else:
            print("To be implemented")        

    def init_AtoV(self): # This function is supposed to return a dictionary relating A to all it's V's
        self.AtoV_[0] = np.array([0], dtype = "int64")

        test =  np.zeros((self.V_items_), dtype = "bool")
        test[0] = True
        test = test.reshape((1,self.V_items_))
        f = 1
        for i in range(1,self.A_items_):
            #Pick first element which is False
            f = np.where(test == False)[1][0]
            #What is it's parent?
            p = self.Parents[f]
            #Look  for all other elements with the same parent. Get their indices
            test2 = [self.Parents == p] # This is not a numpy array and therefore a stupid source for errors
            #Include that tuple in AtoV
            self.AtoV[i] = np.where(test2)[1]
            #set their respective value in test to True
            #print(i, type(test2), test2.shape)
            test = np.logical_or(test,test2)
            #Repeat


