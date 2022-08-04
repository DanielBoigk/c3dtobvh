import numpy as np

from Classes.Specs import Specs # Class that contains build Information for actual BVH Data
from Classes.IOClass import BVH_IO #Class that reads and writes BVH files

class BVH(Specs, BVH_IO):
    def __init__(self, path = ''):
        print("To be implemented")
        if len(path) == 0:
            print("To be implemented")
        else:
            print("To be implemented")

        Specs.__init__(self) # Calls Init function of Parent Class
        self.V = np.zeros((self.length_, self.V_items_, 3),dtype="float64") # Contains all Information about
        self.A = np.zeros((self.length_, self.A_items_, 3),dtype="float64")
        self.C = np.zeros((self.length_, 3),dtype="float64")
        self.MS = np.zeros((self.length_, self.A_items_, 3, 3),dtype="float64")
        self.MM = np.zeros((self.length_, self.A_items_, 3, 3),dtype="float64")
    #from Methods.Values
    from Methods.Angles import Test_func
    #from Methods.Matrix 
    #from IO.Read
    #from IO.Write