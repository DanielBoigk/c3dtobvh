import numpy as np
import re

#Reads and writes a BVH

class BVH_IO():
    def __init__(self, path = ""):
        self.Entries = {}
        self.length_ = 0 
        self.Framerate_ = 0
        self.A_items = 0
        self.V_items = 0
        self.Parents = 0
        
    def open_bvh(path):
        Name_dict = {}
        Names = []
        Offset_dict = {}
        Offset = []
        Depth_Dict = {}
        Parent_dict = {}
        Parents = []

        File = open(path, "r")
        test =    File.readline()
        O_i = 0
        N_i = 0
        root_prev = False
        delimiter = ""
        dl_len = 1
        while "MOTION" not in test.upper():

            test =    File.readline()
            if root_prev:
                if "{" not in test:
                    delimiter = test.split("O",1)[0].replace("O","")
                    dl_len= len(delimiter)
                    root_prev = False

            if ("JOINT" in test.upper()):
                Name_dict[N_i] = test.split("JOINT ",1)[1].replace("\n","")
                helpstr =  test.split("J",1)[0].replace("J","")
                Depth_Dict[N_i] = len(helpstr) // dl_len
                prev_name = Name_dict[N_i]
                N_i += 1

            if ("END SITE" in test.upper()):
                Name_dict[N_i] = prev_name + " End"
                helpstr =  test.split("E",1)[0].replace("E","")
                Depth_Dict[N_i] = len(helpstr) // dl_len
                N_i += 1

            if ("ROOT" in test.upper()):
                Name_dict[N_i] = test.split("ROOT ",1)[1].replace("\n","")
                prev_name = Name_dict[N_i]
                Depth_Dict[N_i] = 0
                root_prev = True
                N_i += 1

            if "OFFSET" in test.upper():
                Offset_dict[O_i] = [float(s) for s in re.findall(r'-?\d+\.?\d*', test)]
                O_i +=1

        test = File.readline()
        Frames = int( test.split("Frames: ",1)[1].replace("\n","") )
        test = File.readline()
        Frame_Time = float( test.split("Frame Time: ",1)[1].replace("\n","") )

        if (O_i != N_i) or (N_i != len(Depth_Dict)):
            print("Error: Inequal Length of Names and Offset.")
            return -1

        # Convert Dictionaries into Arrays:
        Names = [v for k, v in Name_dict.items()]
        Offset = np.array([v for k, v in Offset_dict.items()] , dtype="float64")
        Parent_dict[0] = -1
        for i in range(1,N_i):
            for j in range(i,0, -1):
                if Depth_Dict[j-1] < Depth_Dict[i]:
                    Parent_dict[i] = j-1
                    break
        Parents = np.array([v for k, v in Parent_dict.items()] , dtype="int64")

        # Extracts Values for each timeframe
        items = 0
        if Frames !=0:
            test = File.readline()
            arr = [float(s) for s in re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", test)]
            items = len (arr)//3
            if len(arr)%3 ==0:
                arr = np.reshape(arr,(items,3) )
            else:
                print("Too many entries in Data")
                arr = np.reshape(arr,(items,3) )

        Values = np.zeros((Frames, items ,3), dtype = "float64")
        if Frames !=0:
            Values[0] = arr

        for i in range(1, Frames):
            test = File.readline()
            arr = [float(s) for s in re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", test)]
            Values[i] = np.reshape(arr,(items,3) )

        return Names, Offset, Parents, delimiter, Frames, Frame_Time , Values

