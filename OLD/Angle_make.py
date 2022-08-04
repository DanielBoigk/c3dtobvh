import numpy as np
# from Parent array creates all relevant other Arrays for Angles.py
"""
Parents       Integer Array         Position data
A_Parent      Integer Array         Gives Angle Parent of i-th Angle element 
V_Parent      Integer Array         Gives Value Parent of i-th Angle element
Offset        2-Tensor              Gives Offset
Use_multiple  boolean Array         Tells whether bone has more than one vector
A_items       Integer               Number of Items 
Item_dict     Dict of int pairs     Relates multiple angles to their related Values
AtoV          Dict of integers      Relates a single angle to its related Value
"""


class Angles():
    def __init__(self,Parents, Offset):
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
        self.AtoV[0] = np.array([0], dtype = "int64")

        test =  np.zeros((self.V_items), dtype = "bool")
        test[0] = True
        test = test.reshape((1,self.V_items))
        f = 1
        for i in range(1,self.A_items):
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
      

    def init_use_multiple(self):
        for i in range(self.A_items):
            h = self.AtoV[i].shape[0]
            if h == 1:
                self.Use_multiple[i] = False
            else: 
                self.Use_multiple[i] = True

    def init_V_Parent(self):
        for i in range(self.A_items):
            self.V_Parent[i] = self.Parents[self.AtoV[i][0]]
            
    def init_A_Parent(self):
        self.A_Parent[0] = -1
        for i in range(1,self.A_items):
            vp = self.V_Parent[i]
            for j in range(self.A_items):
                if vp in self.AtoV[j]:
                    self.A_Parent[i] = j
                    break

    def Item_dict_entry(self, ind, vec):
        print("To be implemented")
        comb  = np.empty((2), dtype="int64")
        test = False
        l = len(ind)
        norms = np.linalg.norm(vec, axis = 1)
        if np.inner(norms,norms) < 1e-20:
            return comb, False
        j = 0
        # Find first vector which is non zero
        for i in range(l):
            if norms[i] > 1e-20:
                comb[0] = ind[i]
                j = i
                break
        # Look for first independent vector
        if j == l-1:
            print("This is a case is not yet implemented and will produce an error further sown the line!!!")
        else:
            for i in range(j,l):
                v = np.cross(vec[j], vec[i]) 
                if np.inner(v, v) > 1e-20:
                    comb[1] = ind[i]
                    return comb, True
        # Maybe I should look for the bigest angle between two vectors instead.
        print(ind, vec, "Normen:",norms)
        if comb[0] != 0:
            print("This is a case is not yet implemented and will produce an error further sown the line!!!")
        return comb, False

    def init_Item_dict(self):
        print("To be implemented")

        # Go through use multiple
        for i in range(self.A_items):
            if self.Use_multiple[i] == True:

        # Use Atov to get indices corresponding to use_multiple == True
                ind = self.AtoV[i]
                vec = np.copy(self.Offset[ind])
                comb, test = self.Item_dict_entry(ind, vec)
                if test:
                    self.Item_dict[i] = comb
                else: 
                    #Doesn't catch the case where the first entry is zero, assumes the first indice is zero.
                    self.multiplicity[i] = False
        


    def initialize(self):
        # Go through all init Methods. order matters.
        if self.Parents.shape[0] > 1:
            self.init_AtoV()
            self.init_use_multiple()
            self.init_V_Parent()
            self.init_A_Parent()

            self.init_Item_dict()


            self.is_init = True

    def update(self, Parents, Offset):
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
        self.initialize()